"""The simulation engine.

The engine advances the common-pool-resource game one round at a time. Each round
follows a fixed, deterministic sequence:

1. Snapshot the incoming stock, then regenerate it.
2. Build each agent's observation of the regrown stock (subject to the
   information model).
3. Collect every agent's requested consumption.
4. Scale requests down proportionally if their sum exceeds the stock (feasibility).
5. Assign harvests, update payoffs, withdraw the total, and check for collapse.

All randomness is drawn from per-agent generators derived from the run seed, so a
run is a pure function of ``(config, seed)``.
"""

from __future__ import annotations

import numpy as np

from ..agents.agent import Agent
from ..agents.observation import Observation
from ..disturbances.shocks import build_disturbances
from ..environment.resource import ResourcePool
from ..strategies.base import Strategy
from ..strategies.registry import make_strategy
from . import rng as rng_module
from .config import ResourceConfig, SimulationConfig
from .state import RoundRecord, RunResult


def _ring_lattice(n: int, k: int) -> list[tuple[int, ...]]:
    """A circulant ring lattice used for network reciprocity (ADR-0015).

    Agent ``i``'s fixed neighbours are the ``k/2`` nearest agents on each
    side, in agent-order. ``k`` is validated even and ``< n`` by
    :class:`~emergent_cooperation.core.config.NetworkConfig` and
    :class:`SimulationConfig` before this is ever called.
    """
    half = k // 2
    offsets = list(range(-half, 0)) + list(range(1, half + 1))
    return [tuple((i + off) % n for off in offsets) for i in range(n)]


class Simulation:
    """A single seeded run of the common-pool-resource game."""

    def __init__(self, config: SimulationConfig, seed: int | None = None) -> None:
        """Build the world and agents for one run.

        Args:
            config: The run configuration.
            seed: Overrides ``config.seed`` when provided (used by the experiment
                runner to sweep seeds without rewriting the config).
        """
        self.config = config
        self.seed = config.seed if seed is None else seed
        self.pool = ResourcePool(config.resource)
        # Multiple resources / specialization (ADR-0016): a second,
        # independent pool. ``None`` unless configured, so every code path
        # below that checks ``self.pool_b is not None`` falls back to exactly
        # today's single-pool behaviour.
        self.pool_b: ResourcePool | None = (
            ResourcePool(config.second_resource) if config.second_resource is not None else None
        )
        self.agents = self._build_agents(config)
        # Per-agent fraction of its request routed to the first pool (the
        # rest to the second) -- mirrors ``_build_agents``' own spec-order,
        # count-expansion loop so ``self._agent_split[i]`` lines up with
        # ``self.agents[i]``. ``1.0`` (AgentSpec's default) is a no-op: the
        # entire request goes to the first pool, exactly today's behaviour.
        self._agent_split: list[float] = [
            spec.allocation_split for spec in config.agents for _ in range(spec.count)
        ]
        # A second, independent strategy instance per agent, used only for
        # pool-B's own decide() call (ADR-0016). Several strategies keep
        # per-instance state across rounds (``ConditionalCooperatorStrategy``/
        # ``CompensatingCooperatorStrategy``'s own ``_last_level``, "did the
        # stock I'm watching decline since I last looked") -- calling the
        # *same* instance once per pool per round would have that state
        # alternate between two unrelated pools' levels, corrupting the
        # "declined" comparison for both. A fresh, separate instance per pool
        # keeps each pool's own trend-tracking independent, exactly as if
        # each pool had its own dedicated agent. ``None`` unless a second
        # pool is configured.
        self._strategy_b: list[Strategy] | None = (
            self._build_strategies(config) if config.second_resource is not None else None
        )
        # Size of the governed community for fair-share reasoning (ADR-0012's
        # allocation correction): excludes any AgentSpec(governed=False)
        # outsider batch (ADR-0013) from both the enforcement quota's
        # denominator *and* every governed agent's own "fair share" request --
        # fixing only the former left the latter silently diluted by the same
        # root cause, since a self-request already below the (correctly-sized)
        # quota never triggers the cap at all. Fixed once per run: group
        # membership never changes mid-run.
        self._n_governed = sum(1 for a in self.agents if a.governed) or len(self.agents)
        # Agent indices bucketed by AgentSpec.group (ADR-0012), for _enforce()'s
        # per-group quota loop. Fixed once per run for the same reason as
        # _n_governed above: group membership never changes mid-run.
        self._groups: dict[int, list[int]] = {}
        for i, agent in enumerate(self.agents):
            self._groups.setdefault(agent.group, []).append(i)
        # Network reciprocity (ADR-0015): a fixed ring-lattice neighbour list,
        # built once from agent order -- unlike group membership this has no
        # existing per-agent field to derive from, so it's computed directly
        # from position in ``self.agents``. ``None`` unless configured, so
        # ``_observe`` falls back to ADR-0014's original population-wide
        # partner selection exactly.
        self._neighbors: list[tuple[int, ...]] | None = (
            _ring_lattice(len(self.agents), config.network.degree)
            if config.network is not None
            else None
        )
        # One independent, reproducible RNG stream per agent.
        self._agent_rngs = rng_module.spawn_streams(self.seed, len(self.agents))
        # The whole population's total harvest last round (for the broadcast
        # signal) -- not scoped to any AgentSpec.group.
        self._last_total_harvest: float = 0.0
        # Scheduled environmental disturbances (empty unless configured).
        self._disturbances = build_disturbances(config.disturbances)
        # Collective-choice enforcement (ADR-0011): rounds so far whose total
        # harvest exceeded the sustainable yield, whether the vote has fired yet,
        # and whether it passed.
        self._overuse_rounds: int = 0
        self._vote_taken: bool = False
        self._collective_enforcement_active: bool = False

    def _sustainable_yield(self, resource: ResourceConfig | None = None) -> float:
        """Reference sustainable total harvest for logistic growth (``g*K/4``).

        Defaults to the first pool's own config; pass ``config.second_resource``
        explicitly to get the second pool's own yield (ADR-0016) -- the two
        pools are deliberately allowed to have different ``g``/``K``, so this
        must never be hardcoded to one config.
        """
        r = resource or self.config.resource
        return r.regeneration_rate * r.capacity / 4.0

    @staticmethod
    def _build_strategies(config: SimulationConfig) -> list[Strategy]:
        """A flat, spec-order list of *fresh* strategy instances, one per agent.

        Mirrors ``_build_agents``' own spec-order/count-expansion loop
        exactly, so index ``i`` here lines up with ``self.agents[i]``. Used
        for the second pool's own decide() calls (ADR-0016) so its
        stateful strategies (``conditional``/``compensating``'s own
        ``_last_level``) track *that pool's* trend independently of the
        first pool's, instead of sharing -- and corrupting -- one instance's
        state across two unrelated observations.

        ``regeneration_rate``/``capacity`` are overridden to the *second*
        pool's own values wherever a strategy's params already carry them --
        a bug caught after the fact, not a day-one design choice: without
        this, every pool-B strategy instance was built from pool A's params
        (whatever ``spec.params`` said), so a sanctioning agent's own
        ``sanction_policy()`` quota -- and any strategy's blind/private-info
        fallback estimate -- silently used pool A's growth rate even while
        actually protecting/deciding for pool B. Concretely: a sanctioning
        quota of ``g_A * K / 4`` enforced on pool B lets free-riders take
        double what pool B (``g_B = g_A / 2`` in E20's own asymmetric
        pools) can actually sustain, even with a monitor nominally active.
        Strategies without these params (e.g. ``selfish``) are untouched.
        """
        second = config.second_resource
        strategies: list[Strategy] = []
        for spec in config.agents:
            params = dict(spec.params)
            if "regeneration_rate" in params:
                params["regeneration_rate"] = second.regeneration_rate  # type: ignore[union-attr]
            if "capacity" in params:
                params["capacity"] = second.capacity  # type: ignore[union-attr]
            strategies.extend(make_strategy(spec.strategy, params) for _ in range(spec.count))
        return strategies

    @staticmethod
    def _build_agents(config: SimulationConfig) -> list[Agent]:
        """Instantiate agents from the config's agent specs, in order."""
        agents: list[Agent] = []
        for spec in config.agents:
            for _ in range(spec.count):
                strategy = make_strategy(spec.strategy, spec.params)
                agents.append(
                    Agent(
                        agent_id=len(agents),
                        strategy=strategy,
                        decision_noise=config.decision_noise,
                        group=spec.group,
                        governed=spec.governed,
                    )
                )
        return agents

    def _observation_context(
        self, agent: Agent, round_index: int, rng: np.random.Generator
    ) -> tuple[float | None, float | None, int]:
        """The parts of an observation shared across every pool an agent draws from.

        The broadcast ``signal``, the reputation ``partner_reputation``
        lookup, and the governed population size. Computed exactly **once**
        per agent per round regardless of how many pools exist (multiple
        resources, ADR-0016) -- calling this twice (once per pool) would
        double-roll the broadcast and reputation RNG draws and could reveal a
        *different* partner to the same agent in the same round, which is not
        what either mechanism means.

        Includes the communicated ``signal`` (the *whole population's* total
        harvest last round -- not scoped to the agent's own ``AgentSpec.group``;
        the broadcast predates ADR-0012's nested-enforcement groups and was never
        rescoped to them) when broadcasting is on and this agent receives the
        message this round.
        """
        signal = None
        p = self.config.broadcast_reliability
        if p > 0.0 and round_index > 0 and rng.random() < p:
            signal = self._last_total_harvest
        # A governed agent's "fair share" reasoning is scoped to the governed
        # community (ADR-0012's allocation correction); an outsider (ADR-0013)
        # isn't part of that accounting, so it sees the literal total instead
        # -- it has no community to exclude itself from.
        num_agents = self._n_governed if agent.governed else len(self.agents)
        # Reputation (ADR-0014): pair with one random *other* agent this round
        # and, with probability `visibility`, reveal their current score --
        # individually targeted, unlike `signal`'s population-wide aggregate.
        # Network reciprocity (ADR-0015): if a fixed neighbour graph is
        # configured, the partner is drawn only from that agent's own
        # *persistent* neighbour set instead of the whole population --
        # otherwise this is exactly ADR-0014's original well-mixed draw.
        # Either way exactly two rng calls happen (partner index, then the
        # visibility roll), so sweeping visibility or degree never shifts any
        # other draw.
        partner_reputation = None
        rep = self.config.reputation
        if rep is not None and len(self.agents) > 1:
            if self._neighbors is not None:
                neighbors = self._neighbors[agent.agent_id]
                partner_idx = neighbors[int(rng.integers(0, len(neighbors)))]
            else:
                other = int(rng.integers(0, len(self.agents) - 1))
                partner_idx = other if other < agent.agent_id else other + 1
            if rng.random() < rep.visibility:
                partner_reputation = self.agents[partner_idx].reputation
        return signal, partner_reputation, num_agents

    def _observe_for_pool(
        self,
        agent: Agent,
        pool: ResourcePool,
        round_index: int,
        context: tuple[float | None, float | None, int],
    ) -> Observation:
        """Build the observation of one specific pool from a shared context.

        Reuses the (non-pool-specific) ``context`` from
        :meth:`_observation_context` (multiple resources, ADR-0016). With a
        single pool this is called once, with ``pool=self.pool``, and is
        identical to the pre-ADR-0016 ``_observe``.
        """
        signal, partner_reputation, num_agents = context
        share_level = self.config.information_model == "global"
        return Observation(
            round_index=round_index,
            num_agents=num_agents,
            capacity=pool.config.capacity,
            resource_level=pool.level if share_level else None,
            own_last_harvest=agent.last_harvest,
            own_total_payoff=agent.total_payoff,
            signal=signal,
            partner_reputation=partner_reputation,
        )

    def _update_reputation(self, requests: list[float]) -> None:
        """Update every active agent's own reputation score (ADR-0014).

        ``+1`` for a round at/below the governed community's fair share,
        ``-1`` above it -- scored from the raw *request* (intent), not the
        realised post-rationing/enforcement harvest, and always tracked
        regardless of whether ``ReputationCooperatorStrategy`` is even
        present in this run (a real number, not a fiction specific to one
        strategy). No-op if reputation isn't configured. ``requests`` is each
        agent's *total* request this round; when a second pool is configured
        (ADR-0016) the fair-share reference is the sum of both pools' own
        sustainable yields, so an agent legitimately splitting a fair share
        across two resources isn't scored as if only one pool existed.
        """
        if self.config.reputation is None:
            return
        fair_share = self._sustainable_yield()
        if self.config.second_resource is not None:
            fair_share += self._sustainable_yield(self.config.second_resource)
        fair_share /= self._n_governed
        for agent, request in zip(self.agents, requests, strict=True):
            if agent.active:
                agent.reputation += 1.0 if request <= fair_share else -1.0

    def _allocate(self, requests: list[float], pool: ResourcePool) -> tuple[list[float], float]:
        """Scale requests to fit ``pool``'s available stock and return realised harvests.

        Args:
            requests: Non-negative per-agent requested consumption.
            pool: The pool being allocated from -- ``self.pool`` or
                ``self.pool_b`` (multiple resources, ADR-0016); each pool is
                allocated independently, one call per pool.

        Returns:
            A ``(harvests, total_harvested)`` pair. When the summed request
            exceeds the stock, every agent is scaled by the same factor, which
            keeps the rationing rule neutral across strategies.
        """
        total_request = sum(requests)
        available = pool.level
        if total_request <= available or total_request == 0.0:
            harvests = list(requests)
        else:
            scale = available / total_request
            harvests = [r * scale for r in requests]
        return harvests, sum(harvests)

    def _enforce(
        self,
        harvests: list[float],
        resource: ResourceConfig | None = None,
        pool_side: str | None = None,
    ) -> tuple[list[float], float, list[float]]:
        """Apply sanctioning: cap harvests at the quota and charge monitoring costs.

        Individual sanctioning is scoped to **groups** (``AgentSpec.group``,
        ADR-0012 — nested enforcement, Ostrom design principle 8): within each
        group, if any member exposes a :class:`SanctionPolicy`, a per-capita quota
        (``min(quota_total among that group's sanctioners) / N_governed``,
        ``N_governed`` the *governed* population -- see the "Allocation
        correction" in ADR-0012 -- so the shared pool's overall sustainable
        draw is unaffected when every governed group is monitored) is enforced
        on that group's members only — harvest above the quota is confiscated
        (left in the pool, not withdrawn), and each sanctioner forfeits its
        monitoring cost. A group with no sanctioner of its own is left
        unprotected by individual enforcement even if another group has one — unlike
        the population-wide "any one sanctioner protects everyone" of a flat model.
        Every ``AgentSpec`` defaults to ``group=0``, so with no group configured
        this reduces exactly to the original flat, population-wide behaviour (see
        ADR-0005). The same partition, with an ``AgentSpec(governed=False)``
        outsider group and no new enforcement mechanism, is also how
        "boundaries"/open-access experiments are expressed (ADR-0013) --
        outsiders are structurally excluded from ``N_governed``, not counted
        and then left unconstrained anyway.

        If the group has voted to adopt **collective-choice enforcement** (ADR-0011),
        the same per-capita quota is enforced population-wide regardless of
        grouping — a separate mechanism (Ostrom principle 3, not 8) — funded by a
        ``cost_share`` charged to every active agent that does not already carry its
        own :class:`SanctionPolicy` (avoids double-charging an agent that already
        pays individually).

        Args:
            harvests: Per-agent realised harvests after feasibility scaling.
            resource: Which pool's own sustainable yield backs the no-sanctioner
                quota fallback below -- ``self.config.resource`` (the default)
                or ``self.config.second_resource`` (multiple resources,
                ADR-0016), matching whichever pool's harvest list was passed.
                A sanctioner enforcing both pools pays its ``monitoring_cost``
                once per pool it is called for -- a deliberate consequence of
                extending enforcement per-pool, not a double-charge bug (see
                ADR-0016): watching two resources costs more than watching one.
            pool_side: ``"a"``/``"b"`` (multiple resources, ADR-0016) -- a
                monitor's enforcement reach follows its own specialization:
                a pure pool-A specialist (``allocation_split=1.0``) never
                enforces, or pays to enforce, pool B, and vice versa. Only
                applied when ``self.pool_b`` is configured; ``None`` (the
                single-pool default) enforces with every active policy,
                unfiltered, exactly as before.

        Returns:
            A ``(harvests, total_harvested, penalties)`` triple, where ``penalties``
            is the per-agent monitoring/collective-fee cost paid this round (0 for
            agents subject to neither).
        """
        penalties = [0.0] * len(self.agents)
        collective = self._collective_enforcement_active
        # The per-capita quota rations the *governed* community's own
        # sustainable share -- an outsider (AgentSpec.governed=False, ADR-0013)
        # was never part of that accounting, so including it in the
        # denominator would silently shrink everyone else's allocation to
        # make room for a draw it does nothing to actually constrain.
        n_governed = self._n_governed

        # A failed (inactive) sanctioner no longer enforces. Pool B's own
        # quota comes from pool B's own strategy instance (self._strategy_b),
        # not the pool-A instance reused for both -- a bug caught after the
        # fact: without this, enforcing pool B always asked the pool-A
        # strategy's sanction_policy() for its quota, silently protecting
        # pool B at pool A's (too generous) sustainable yield regardless of
        # what pool B's own strategy instance -- now correctly built with
        # pool B's own regeneration_rate, see _build_strategies -- would say.
        policy_strategies = (
            self._strategy_b if pool_side == "b" and self._strategy_b is not None else None
        )
        own_policies = []
        for i, agent in enumerate(self.agents):
            if not agent.active:
                own_policies.append(None)
                continue
            strategy = policy_strategies[i] if policy_strategies is not None else agent.strategy
            own_policies.append(strategy.sanction_policy())
        # Multiple resources (ADR-0016): filter out a specialist's policy for
        # the pool it has no stake in at all, so a pure pool-A monitor
        # (allocation_split=1.0) neither enforces nor pays to enforce pool B.
        if self.pool_b is not None and pool_side is not None:
            if pool_side == "a":
                own_policies = [
                    p if self._agent_split[i] > 0.0 else None for i, p in enumerate(own_policies)
                ]
            else:
                own_policies = [
                    p if self._agent_split[i] < 1.0 else None for i, p in enumerate(own_policies)
                ]

        capped = list(harvests)
        for member_indices in self._groups.values():
            active = [own_policies[i] for i in member_indices if own_policies[i] is not None]
            if not active and not collective:
                continue
            quota_per_capita = (
                min(p.quota_total for p in active) / n_governed
                if active
                else self._sustainable_yield(resource) / n_governed
            )
            for i in member_indices:
                capped[i] = min(capped[i], quota_per_capita)
                policy = own_policies[i]
                if policy is not None:
                    penalties[i] = policy.monitoring_cost
                    self.agents[i].total_payoff -= policy.monitoring_cost

        # Collective-choice enforcement is jointly funded by everyone who does not
        # already pay individually (ADR-0011); unaffected by grouping.
        if collective:
            share = self.config.collective_choice.cost_share  # type: ignore[union-attr]
            for i, agent in enumerate(self.agents):
                if agent.active and own_policies[i] is None:
                    penalties[i] += share
                    agent.total_payoff -= share

        return capped, sum(capped), penalties

    def _maybe_vote(self, round_index: int) -> bool:
        """Tally the collective-choice vote at its scheduled round (ADR-0011).

        Called *before* :meth:`_enforce` so that, if the vote passes, enforcement
        applies starting this very round. Decided from over-use tracked over rounds
        ``0..round_index-1`` (this round hasn't happened yet).

        Returns:
            ``True`` exactly in the round the vote is tallied (whichever way it
            goes), for the round record; ``False`` otherwise.
        """
        cc = self.config.collective_choice
        if cc is None or self._vote_taken or round_index != cc.vote_round:
            return False
        self._vote_taken = True
        if round_index > 0:
            overuse_fraction = self._overuse_rounds / round_index
            self._collective_enforcement_active = overuse_fraction > cc.overuse_threshold
        return True

    def _track_overuse(self, total_harvested: float) -> None:
        """Record whether this round's harvest exceeded the sustainable yield.

        Only affects the still-pending vote; a no-op once the vote has fired.
        """
        if self.config.collective_choice is not None and total_harvested > self._sustainable_yield():
            self._overuse_rounds += 1

    def _disturb(self, round_index: int) -> bool:
        """Apply any scheduled disturbances for this round; report if any fired."""
        fired = False
        for disturbance in self._disturbances:
            fired |= disturbance.apply(round_index, self.pool, self.agents)
        return fired

    def step(self, round_index: int) -> RoundRecord:
        """Advance the simulation by exactly one round and return its record.

        Order: regenerate -> disturb -> observe -> harvest. The stock first regrows,
        any scheduled disturbance then perturbs it, agents observe the resulting
        stock, then harvest from it. Applying the shock before observation means
        agents that can see the stock (``global`` model) react to the depleted level
        the same round; blind (``private``) agents do not, which is what the
        resilience experiment (E8) exploits.

        With a second pool configured (multiple resources / specialization,
        ADR-0016), each active agent's *existing* ``decide()`` runs once
        against each pool's own observation (unmodified -- no strategy code
        changes), and the engine scales the two results by that agent's own
        ``AgentSpec.allocation_split`` before allocating/enforcing each pool
        independently. Disturbances, the collective-choice vote/overuse
        tally, and the broadcast ``signal`` all stay scoped to the *first*
        pool only -- a deliberate, documented scope limit (ADR-0016), not an
        oversight: extending all three to a second pool is untested.
        """
        resource_start = self.pool.level
        resource_start_b = self.pool_b.level if self.pool_b is not None else None

        self.pool.regenerate()
        if self.pool_b is not None:
            self.pool_b.regenerate()
        disturbed = self._disturb(round_index)
        resource_after_regen = self.pool.level
        resource_after_regen_b = self.pool_b.level if self.pool_b is not None else None

        # Failed agents (agent_failure disturbance) request nothing; active ones
        # decide once per pool and are split by their own allocation_split.
        requests_a: list[float] = []
        requests_b: list[float] = []
        for i, agent in enumerate(self.agents):
            if not agent.active:
                requests_a.append(0.0)
                requests_b.append(0.0)
                continue
            rng = self._agent_rngs[i]
            context = self._observation_context(agent, round_index, rng)
            obs_a = self._observe_for_pool(agent, self.pool, round_index, context)
            raw_a = agent.decide(obs_a, rng)
            if self.pool_b is not None:
                obs_b = self._observe_for_pool(agent, self.pool_b, round_index, context)
                raw_b = agent.decide(obs_b, rng, strategy=self._strategy_b[i])
                split = self._agent_split[i]
                requests_a.append(raw_a * split)
                requests_b.append(raw_b * (1.0 - split))
            else:
                requests_a.append(raw_a)
                requests_b.append(0.0)

        harvests_a, total_harvested_a = self._allocate(requests_a, self.pool)
        # The collective-choice vote (ADR-0011), if scheduled this round, is
        # tallied before enforcement so a passing vote takes effect immediately.
        # Scoped to the first pool's own overuse pattern (ADR-0016).
        vote_taken = self._maybe_vote(round_index)
        harvests_a, total_harvested_a, penalties_a = self._enforce(
            harvests_a, self.config.resource, pool_side="a"
        )
        self._track_overuse(total_harvested_a)

        if self.pool_b is not None:
            harvests_b, total_harvested_b = self._allocate(requests_b, self.pool_b)
            harvests_b, total_harvested_b, penalties_b = self._enforce(
                harvests_b, self.config.second_resource, pool_side="b"
            )
        else:
            harvests_b = [0.0] * len(self.agents)
            total_harvested_b = 0.0
            penalties_b = [0.0] * len(self.agents)

        # An agent's total request/harvest/penalty this round, summed across
        # both pools -- this is what payoff/Gini/welfare_efficiency already
        # correctly consume unchanged (ADR-0016).
        requests = [a + b for a, b in zip(requests_a, requests_b, strict=True)]
        harvests = [a + b for a, b in zip(harvests_a, harvests_b, strict=True)]
        penalties = [a + b for a, b in zip(penalties_a, penalties_b, strict=True)]

        # Reputation is scored from this round's raw requests (ADR-0014), so it
        # reflects intent, not what feasibility/enforcement happened to allow.
        self._update_reputation(requests)

        for agent, amount in zip(self.agents, harvests, strict=True):
            agent.record_harvest(amount)
        self.pool.withdraw(total_harvested_a)
        if self.pool_b is not None:
            self.pool_b.withdraw(total_harvested_b)
        # The broadcast signal stays scoped to the first pool only (ADR-0016).
        self._last_total_harvest = total_harvested_a
        resource_after_harvest = self.pool.level
        resource_after_harvest_b = self.pool_b.level if self.pool_b is not None else None

        return RoundRecord(
            round_index=round_index,
            resource_start=resource_start,
            resource_after_regen=resource_after_regen,
            requested=tuple(requests),
            harvested=tuple(harvests),
            resource_after_harvest=resource_after_harvest,
            collapsed=self.pool.is_collapsed,
            penalties=tuple(penalties),
            disturbed=disturbed,
            vote_taken=vote_taken,
            collective_enforcement_active=self._collective_enforcement_active,
            reputations=(
                tuple(a.reputation for a in self.agents) if self.config.reputation is not None else ()
            ),
            resource_start_b=resource_start_b,
            resource_after_regen_b=resource_after_regen_b,
            resource_after_harvest_b=resource_after_harvest_b,
            collapsed_b=self.pool_b.is_collapsed if self.pool_b is not None else False,
            requested_b=tuple(requests_b) if self.pool_b is not None else (),
            harvested_b=tuple(harvests_b) if self.pool_b is not None else (),
        )

    def run(self) -> RunResult:
        """Run all rounds and return the collected result."""
        result = RunResult(
            config_name=self.config.name,
            seed=self.seed,
            information_model=self.config.information_model,
            agent_strategies=tuple(a.strategy_name for a in self.agents),
            agent_groups=tuple(a.group for a in self.agents),
        )
        for round_index in range(self.config.rounds):
            result.rounds.append(self.step(round_index))
        return result


def run_simulation(config: SimulationConfig, seed: int | None = None) -> RunResult:
    """Convenience wrapper: build a :class:`Simulation` and run it."""
    return Simulation(config, seed=seed).run()
