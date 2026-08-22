"""Configuration objects and loading.

Experiments are configuration-driven: every run is fully described by a
:class:`SimulationConfig`, and every experiment (a sweep over seeds) by an
:class:`ExperimentConfig`. Configs are plain dataclasses that can be built from a
nested dict (e.g. parsed YAML) via :meth:`from_dict`, which keeps the on-disk
format decoupled from the in-memory representation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

# Information models decide what an agent may observe each round.
INFORMATION_MODELS = ("global", "private")

# Environmental disturbances the engine knows how to apply (see :mod:`disturbances`).
DISTURBANCE_KINDS = ("resource_shock", "agent_failure", "agent_turnover")


@dataclass(frozen=True)
class DisturbanceConfig:
    """A single scheduled environmental perturbation.

    Disturbances make the resilience experiments possible: the world runs
    normally, then a shock hits at a known round and we measure recovery. Keeping
    the schedule in the config (rather than in random events) preserves the
    ``run = f(config, seed)`` guarantee — a shock is deterministic.

    Attributes:
        kind: One of :data:`DISTURBANCE_KINDS`. ``"resource_shock"`` removes a
            fraction of the standing stock in a single round (a "pulse" shock);
            ``"agent_failure"`` deactivates a fraction of the agents (they stop
            requesting, harvesting, and — if a sanctioner — enforcing);
            ``"agent_turnover"`` (E24, ADR-0021) resets a fraction of agents'
            own per-round strategy memory to a fresh, untriggered state — as
            if a new individual took over that role, per Duffy & Lafky
            (2015)'s overlapping-generations finding — without deactivating
            them or touching accumulated payoff.
        round: Zero-based round at which the disturbance fires.
        magnitude: Kind-specific size, always a fraction in ``(0, 1]``. For
            ``"resource_shock"`` it is the fraction of the stock removed (``0.7`` =
            lose 70%); for ``"agent_failure"`` it is the fraction of agents that fail
            (``0.25`` = one in four; agents fail in index/spec order); for
            ``"agent_turnover"`` it is the fraction of agents reset, starting
            from a deterministic rotation offset (``round % num_agents``) so
            repeated turnover events touch different agents over time.
    """

    kind: str = "resource_shock"
    round: int = 0
    magnitude: float = 0.5

    def __post_init__(self) -> None:
        if self.kind not in DISTURBANCE_KINDS:
            raise ValueError(f"kind must be one of {DISTURBANCE_KINDS}, got {self.kind!r}")
        if self.round < 0:
            raise ValueError("round must be non-negative")
        if not 0 < self.magnitude <= 1:
            raise ValueError(f"{self.kind} magnitude must be in (0, 1]")


@dataclass(frozen=True)
class ResourceConfig:
    """Parameters of the shared renewable resource.

    Attributes:
        initial_level: Resource stock at round 0.
        capacity: Carrying capacity ``K``; growth and stock are capped here.
        regeneration_rate: Intrinsic growth rate ``g`` used by the regeneration rule.
        regeneration_rule: ``"logistic"`` (``g*R*(1-R/K)``) or ``"linear"`` (``g*R``).
        collapse_threshold: Stock at or below this is treated as collapsed.
    """

    initial_level: float = 50.0
    capacity: float = 100.0
    regeneration_rate: float = 0.4
    regeneration_rule: str = "logistic"
    collapse_threshold: float = 1.0

    def __post_init__(self) -> None:
        if self.capacity <= 0:
            raise ValueError("capacity must be positive")
        if not 0 <= self.initial_level <= self.capacity:
            raise ValueError("initial_level must be within [0, capacity]")
        if self.regeneration_rule not in ("logistic", "linear"):
            raise ValueError(f"unknown regeneration_rule: {self.regeneration_rule!r}")


@dataclass(frozen=True)
class CollectiveChoiceConfig:
    """A group vote on whether to adopt a binding, jointly-funded enforcement rule.

    Models Ostrom, Walker & Gardner (1992)'s "covenant with an endogenously chosen
    sword": the group observes its own over-use pattern and, at a scheduled round,
    votes on whether to adopt a binding harvest quota funded by *everyone* -- not
    only agents individually pre-committed to the ``sanctioning`` strategy. See
    ADR-0011.

    Attributes:
        vote_round: Zero-based round at which the vote is tallied, after the group
            has had rounds to build a track record.
        overuse_threshold: The vote passes if the fraction of rounds so far whose
            total harvest exceeded the sustainable yield (``g*K/4``) exceeds this
            threshold, in ``[0, 1]``.
        cost_share: Payoff each active agent without its own individual sanction
            policy forfeits per round once the vote passes, funding the quota.
    """

    vote_round: int = 10
    overuse_threshold: float = 0.5
    cost_share: float = 0.2

    def __post_init__(self) -> None:
        if self.vote_round < 0:
            raise ValueError("vote_round must be non-negative")
        if not 0 <= self.overuse_threshold <= 1:
            raise ValueError("overuse_threshold must be in [0, 1]")
        if self.cost_share < 0:
            raise ValueError("cost_share must be non-negative")


@dataclass(frozen=True)
class ReputationConfig:
    """Indirect reciprocity via reputation (Nowak & Sigmund 1998; ADR-0014).

    Every agent's own reputation score is tracked and updated by the engine
    every round regardless of strategy (``+1`` for staying at/below the
    governed community's fair share that round, ``-1`` above it) -- a real,
    always-on number. Separately, each agent is paired with one random
    *other* agent every round and, with probability ``visibility``, gets to
    see that specific partner's current score
    (``Observation.partner_reputation``). Only
    :class:`~emergent_cooperation.strategies.reputation.
    ReputationCooperatorStrategy` actually reads it; every other strategy
    ignores it, the same as an unread broadcast ``signal``.

    Attributes:
        visibility: Probability ``q`` that a given round's partner-lookup
            succeeds, in ``[0, 1]``. Structurally the same kind of parameter
            as ``broadcast_reliability`` -- an imperfect information channel,
            not a new kind of thing. Nowak & Sigmund's own stability
            condition for reputation-sustained cooperation is ``q > c/b``.
    """

    visibility: float = 1.0

    def __post_init__(self) -> None:
        if not 0 <= self.visibility <= 1:
            raise ValueError("visibility must be in [0, 1]")


@dataclass(frozen=True)
class NetworkConfig:
    """A fixed graph restricting who a partner-conditioned strategy can pair with.

    Nowak (2006)'s network reciprocity (rule 4): individuals occupy the
    vertices of a graph and interact only with their ``k`` graph neighbours,
    not the whole population -- cooperators can then survive by forming
    clusters that mutually protect each other, favoured when ``b/c > k``. In
    this project that ``k`` neighbours-only restriction is applied to
    :class:`ReputationConfig`'s partner selection specifically (see ADR-0015):
    instead of a fresh, uniformly random partner every round (ADR-0014's
    well-mixed default, closer to Nowak's *indirect* reciprocity), each agent
    is paired with a random member of its own *fixed, persistent* neighbour
    set on a ring lattice -- built once per run from agent order, unchanged
    across rounds. Persistence is the one ingredient this adds that neither
    groups (ADR-0012, a hard partition) nor well-mixed reputation (ADR-0014,
    a fresh random draw every round) has: it lets the *same* two agents
    repeatedly interact, so an agent's outcome can depend on its graph
    position, not just the population's aggregate composition.

    Requires ``SimulationConfig.reputation`` to also be configured -- it has
    no effect on its own, the same way ``ReputationConfig`` has no effect
    without a strategy that reads ``Observation.partner_reputation``.

    Attributes:
        degree: Number of fixed neighbours per agent (``k``), ``k/2`` on each
            side of the ring. Must be even and less than the population size.
    """

    degree: int = 4

    def __post_init__(self) -> None:
        if self.degree < 0:
            raise ValueError("degree must be non-negative")
        if self.degree % 2 != 0:
            raise ValueError("degree must be even (symmetric neighbours on each side)")


@dataclass(frozen=True)
class WealthMonitoringConfig:
    """Wealth-triggered ad-hoc voluntary monitoring (Olson 1965; E22, ADR-0020).

    Operationalizes Olson's own formal result: a group member has an
    individual incentive to unilaterally provide a collective good exactly
    when its own share of the benefit clears the good's cost relative to its
    total value (`F_i > C/V_g`, p. 33). Here, "share of benefit" is an
    agent's own accumulated ``total_payoff`` relative to the population's
    current average -- exactly Olson's own worked example ("an owner of vast
    estates... will have a larger F_i," p. 29). Re-evaluated fresh every
    round: an agent with no intrinsic :meth:`Strategy.sanction_policy`
    (i.e., not already a ``sanctioning``-strategy agent) and not
    ``selfish`` (enforcement would cap its own over-extraction too, so it is
    never a net gain for a fixed-greed extractor -- Olson's ``F_i`` presumes
    the volunteer actually values the good provided) whose own
    ``total_payoff`` exceeds ``threshold`` times the population's current
    average becomes this round's ad-hoc volunteer monitor -- only the single
    *wealthiest* eligible agent, matching this engine's existing "any one
    monitor enforces fully" simplification and Olson's own point that once
    the largest member has provided the amount it wants, no one else has any
    further incentive to also contribute.

    Attributes:
        threshold: Multiple of the population's current average
            ``total_payoff`` an agent's own wealth must exceed to volunteer.
            Values above ``1.0`` mean "above average," the range Olson's own
            argument is about; ``<= 1.0`` is a permissive degenerate case,
            not disallowed but not the motivating one.
        monitoring_cost: Payoff the volunteer forfeits each round it
            monitors -- the same quantity, and same default, as
            :class:`~emergent_cooperation.strategies.sanctioning.SanctioningStrategy`'s
            own ``monitoring_cost``.
    """

    threshold: float
    monitoring_cost: float = 0.2

    def __post_init__(self) -> None:
        if self.threshold < 0:
            raise ValueError("threshold must be non-negative")
        if self.monitoring_cost < 0:
            raise ValueError("monitoring_cost must be non-negative")


@dataclass(frozen=True)
class AgentSpec:
    """A homogeneous group of agents sharing one strategy.

    Attributes:
        strategy: Registered strategy name (see :mod:`strategies.registry`).
        count: Number of agents instantiated with this strategy.
        params: Strategy-specific keyword arguments.
        group: Nested-enterprise membership (Ostrom design principle 8; see
            ADR-0012). Agents with the same ``group`` id are monitored and
            enforced together, separately from other groups. ``0`` for every
            spec (the default) reproduces the original flat, population-wide
            enforcement exactly — this field is purely additive. Also reused,
            without any new mechanism, to express a "boundaries" experiment
            (Ostrom principle 1; see ADR-0013): an ungoverned outsider group
            with no sanctioner of its own models open access.
        governed: Whether this spec's agents are part of the community whose
            sustainable yield is being fairly allocated (ADR-0012's
            allocation correction). ``True`` for every governed group
            (default); set ``False`` for an outsider spec (ADR-0013) so its
            members are structurally excluded from every group's per-capita
            quota calculation, not silently included in the denominator and
            then left unconstrained anyway.
        allocation_split: Only meaningful when
            ``SimulationConfig.second_resource`` is configured (multiple
            resources, ADR-0016): the fraction of this spec's agents' request
            routed to the *first* pool, with the rest routed to the second.
            ``1.0`` (the default) means "ignore the second pool entirely",
            which is exactly today's single-resource behaviour — this field
            is purely additive, the same way ``group``/``governed`` are.
            ``0.5`` is an even generalist split; values near ``0`` or ``1``
            specialise in one resource.
    """

    strategy: str
    count: int = 1
    params: dict[str, Any] = field(default_factory=dict)
    group: int = 0
    governed: bool = True
    allocation_split: float = 1.0

    def __post_init__(self) -> None:
        if self.count < 0:
            raise ValueError("count must be non-negative")
        if self.group < 0:
            raise ValueError("group must be non-negative")
        if not 0 <= self.allocation_split <= 1:
            raise ValueError("allocation_split must be in [0, 1]")


@dataclass(frozen=True)
class SimulationConfig:
    """Full description of a single simulation run.

    Attributes:
        name: Human-readable identifier used in outputs.
        rounds: Number of discrete time steps to simulate.
        seed: Master seed for this run (may be overridden per repetition).
        information_model: One of :data:`INFORMATION_MODELS`.
        decision_noise: Fractional noise applied to each agent's request, in
            ``[0, 1)``. ``0`` is fully deterministic (the historical behaviour);
            ``d`` perturbs each request by a factor drawn uniformly from
            ``[1 - d, 1 + d]`` using the agent's own RNG. This is what makes the
            random seed consequential and between-seed variance meaningful.
        broadcast_reliability: Communication channel in ``[0, 1]``. ``0`` = no
            communication (default). ``p`` = each agent receives a broadcast of the
            group's total harvest last round with probability ``p`` (drawn from its
            own RNG), delivered via ``Observation.signal`` (see ADR-0007).
        resource: Resource parameters.
        agents: Ordered agent-group specifications.
        disturbances: Scheduled environmental perturbations (empty by default, so
            existing experiments are unchanged). Each fires at its own round.
        collective_choice: An optional group vote on jointly-funded enforcement
            (``None`` by default, so existing experiments are unchanged; see
            :class:`CollectiveChoiceConfig` and ADR-0011).
        reputation: Optional indirect-reciprocity tracking (``None`` by
            default, so existing experiments are unchanged; see
            :class:`ReputationConfig` and ADR-0014).
        network: Optional fixed-neighbour restriction on reputation's partner
            selection (``None`` by default -- partner selection stays
            population-wide, exactly ADR-0014's original behaviour; see
            :class:`NetworkConfig` and ADR-0015).
        second_resource: An optional second, independent renewable pool
            (multiple resources / specialization, ADR-0016). ``None`` by
            default, so existing experiments are unchanged and ``resource``
            is the only pool. When set, each agent's own request is computed
            once (unchanged, same ``Strategy.decide()`` every strategy
            already has) against *each* pool's own observation and split
            between them by its ``AgentSpec.allocation_split`` -- no strategy
            code changes, only the engine learns to run two pools.
        wealth_floor_fraction: Optional wealth-gated participation floor
            (Chen & Szolnoki 2016; E23, ADR-0019). ``None`` by default, so
            existing experiments are unchanged. When set, an agent whose own
            accumulated ``total_payoff`` falls below
            ``wealth_floor_fraction`` times the *governed* population's
            current average ``total_payoff`` is excluded from requesting
            (and, if a sanctioner, from enforcing) that round -- re-evaluated
            fresh every round, not permanent. Relative to the population's
            own average, not a fixed absolute number, so it scales with
            however much wealth has actually accumulated and never excludes
            anyone at round 0 (everyone starts at exactly the average: zero).
        wealth_monitoring: Optional wealth-triggered ad-hoc voluntary
            monitoring (Olson 1965; E22, ADR-0020). ``None`` by default, so
            existing experiments are unchanged. When set, the single
            wealthiest agent with no intrinsic sanction policy whose
            ``total_payoff`` exceeds the configured multiple of the
            population's current average volunteers as monitor for that
            round only -- see :class:`WealthMonitoringConfig`.
    """

    name: str = "unnamed"
    rounds: int = 100
    seed: int = 0
    information_model: str = "global"
    decision_noise: float = 0.0
    broadcast_reliability: float = 0.0
    resource: ResourceConfig = field(default_factory=ResourceConfig)
    agents: tuple[AgentSpec, ...] = field(default_factory=tuple)
    disturbances: tuple[DisturbanceConfig, ...] = field(default_factory=tuple)
    collective_choice: CollectiveChoiceConfig | None = None
    reputation: ReputationConfig | None = None
    network: NetworkConfig | None = None
    second_resource: ResourceConfig | None = None
    wealth_floor_fraction: float | None = None
    wealth_monitoring: WealthMonitoringConfig | None = None

    def __post_init__(self) -> None:
        if self.rounds <= 0:
            raise ValueError("rounds must be positive")
        if self.information_model not in INFORMATION_MODELS:
            raise ValueError(
                f"information_model must be one of {INFORMATION_MODELS}, "
                f"got {self.information_model!r}"
            )
        if not 0 <= self.decision_noise < 1:
            raise ValueError("decision_noise must be in [0, 1)")
        if not 0 <= self.broadcast_reliability <= 1:
            raise ValueError("broadcast_reliability must be in [0, 1]")
        for d in self.disturbances:
            if d.round >= self.rounds:
                raise ValueError(
                    f"disturbance round {d.round} is outside the run ({self.rounds} rounds)"
                )
        if self.collective_choice is not None and self.collective_choice.vote_round >= self.rounds:
            raise ValueError(
                f"collective_choice.vote_round {self.collective_choice.vote_round} is outside "
                f"the run ({self.rounds} rounds)"
            )
        if self.network is not None and self.network.degree >= self.num_agents:
            raise ValueError(
                f"network.degree {self.network.degree} must be less than the population size "
                f"({self.num_agents})"
            )
        if self.wealth_floor_fraction is not None and self.wealth_floor_fraction < 0:
            raise ValueError("wealth_floor_fraction must be non-negative")

    @property
    def num_agents(self) -> int:
        """Total number of agents across all groups."""
        return sum(spec.count for spec in self.agents)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> SimulationConfig:
        """Build a config from a nested dict (e.g. parsed YAML)."""
        data = dict(data)
        resource = ResourceConfig(**data.pop("resource", {}))
        agents = tuple(AgentSpec(**spec) for spec in data.pop("agents", []))
        disturbances = tuple(DisturbanceConfig(**d) for d in data.pop("disturbances", []))
        collective_choice_data = data.pop("collective_choice", None)
        collective_choice = (
            CollectiveChoiceConfig(**collective_choice_data)
            if collective_choice_data is not None
            else None
        )
        reputation_data = data.pop("reputation", None)
        reputation = ReputationConfig(**reputation_data) if reputation_data is not None else None
        network_data = data.pop("network", None)
        network = NetworkConfig(**network_data) if network_data is not None else None
        second_resource_data = data.pop("second_resource", None)
        second_resource = (
            ResourceConfig(**second_resource_data) if second_resource_data is not None else None
        )
        wealth_monitoring_data = data.pop("wealth_monitoring", None)
        wealth_monitoring = (
            WealthMonitoringConfig(**wealth_monitoring_data)
            if wealth_monitoring_data is not None
            else None
        )
        return cls(
            resource=resource,
            agents=agents,
            disturbances=disturbances,
            collective_choice=collective_choice,
            reputation=reputation,
            network=network,
            second_resource=second_resource,
            wealth_monitoring=wealth_monitoring,
            **data,
        )


@dataclass(frozen=True)
class ExperimentConfig:
    """A simulation config plus the seed sweep that turns it into an experiment.

    Attributes:
        simulation: The base run configuration. Its ``seed`` field is ignored in
            favour of the explicit ``seeds`` list below.
        seeds: Master seeds; one independent run is executed per seed.
        record_history: Whether to export the full per-round history in addition
            to summary metrics.
    """

    simulation: SimulationConfig = field(default_factory=SimulationConfig)
    seeds: tuple[int, ...] = (0,)
    record_history: bool = True

    def __post_init__(self) -> None:
        if len(self.seeds) == 0:
            raise ValueError("at least one seed is required")

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ExperimentConfig:
        """Build an experiment config from a nested dict."""
        data = dict(data)
        seeds = tuple(data.pop("seeds", (0,)))
        record_history = data.pop("record_history", True)
        # Remaining keys describe the simulation itself.
        simulation = SimulationConfig.from_dict(data)
        return cls(simulation=simulation, seeds=seeds, record_history=record_history)


def load_experiment(path: str | Path) -> ExperimentConfig:
    """Load an :class:`ExperimentConfig` from a YAML file.

    Args:
        path: Path to a YAML configuration file.

    Returns:
        The parsed experiment configuration.
    """
    text = Path(path).read_text(encoding="utf-8")
    data = yaml.safe_load(text) or {}
    return ExperimentConfig.from_dict(data)
