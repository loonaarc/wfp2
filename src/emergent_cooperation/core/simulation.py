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
from ..strategies.registry import make_strategy
from . import rng as rng_module
from .config import SimulationConfig
from .state import RoundRecord, RunResult


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
        self.agents = self._build_agents(config)
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

    def _sustainable_yield(self) -> float:
        """Reference sustainable total harvest for logistic growth (``g*K/4``)."""
        r = self.config.resource
        return r.regeneration_rate * r.capacity / 4.0

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

    def _observe(self, agent: Agent, round_index: int, rng: np.random.Generator) -> Observation:
        """Construct an agent's observation for the given round.

        Includes the communicated ``signal`` (the *whole population's* total
        harvest last round -- not scoped to the agent's own ``AgentSpec.group``;
        the broadcast predates ADR-0012's nested-enforcement groups and was never
        rescoped to them) when broadcasting is on and this agent receives the
        message this round.
        """
        share_level = self.config.information_model == "global"
        signal = None
        p = self.config.broadcast_reliability
        if p > 0.0 and round_index > 0 and rng.random() < p:
            signal = self._last_total_harvest
        # A governed agent's "fair share" reasoning is scoped to the governed
        # community (ADR-0012's allocation correction); an outsider (ADR-0013)
        # isn't part of that accounting, so it sees the literal total instead
        # -- it has no community to exclude itself from.
        num_agents = self._n_governed if agent.governed else len(self.agents)
        return Observation(
            round_index=round_index,
            num_agents=num_agents,
            capacity=self.config.resource.capacity,
            resource_level=self.pool.level if share_level else None,
            own_last_harvest=agent.last_harvest,
            own_total_payoff=agent.total_payoff,
            signal=signal,
        )

    def _allocate(self, requests: list[float]) -> tuple[list[float], float]:
        """Scale requests to fit the available stock and return realised harvests.

        Args:
            requests: Non-negative per-agent requested consumption.

        Returns:
            A ``(harvests, total_harvested)`` pair. When the summed request
            exceeds the stock, every agent is scaled by the same factor, which
            keeps the rationing rule neutral across strategies.
        """
        total_request = sum(requests)
        available = self.pool.level
        if total_request <= available or total_request == 0.0:
            harvests = list(requests)
        else:
            scale = available / total_request
            harvests = [r * scale for r in requests]
        return harvests, sum(harvests)

    def _enforce(self, harvests: list[float]) -> tuple[list[float], float, list[float]]:
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

        # A failed (inactive) sanctioner no longer enforces.
        own_policies = [
            agent.strategy.sanction_policy() if agent.active else None for agent in self.agents
        ]

        capped = list(harvests)
        for member_indices in self._groups.values():
            active = [own_policies[i] for i in member_indices if own_policies[i] is not None]
            if not active and not collective:
                continue
            quota_per_capita = (
                min(p.quota_total for p in active) / n_governed
                if active
                else self._sustainable_yield() / n_governed
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
        """
        resource_start = self.pool.level

        self.pool.regenerate()
        disturbed = self._disturb(round_index)
        resource_after_regen = self.pool.level

        # Failed agents (agent_failure disturbance) request nothing; active ones decide.
        requests = [
            agent.decide(
                self._observe(agent, round_index, self._agent_rngs[i]), self._agent_rngs[i]
            )
            if agent.active
            else 0.0
            for i, agent in enumerate(self.agents)
        ]
        harvests, total_harvested = self._allocate(requests)
        # The collective-choice vote (ADR-0011), if scheduled this round, is
        # tallied before enforcement so a passing vote takes effect immediately.
        vote_taken = self._maybe_vote(round_index)
        harvests, total_harvested, penalties = self._enforce(harvests)
        self._track_overuse(total_harvested)

        for agent, amount in zip(self.agents, harvests, strict=True):
            agent.record_harvest(amount)
        self.pool.withdraw(total_harvested)
        self._last_total_harvest = total_harvested
        resource_after_harvest = self.pool.level

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
