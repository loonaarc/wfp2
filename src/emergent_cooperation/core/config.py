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
DISTURBANCE_KINDS = ("resource_shock", "agent_failure")


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
            requesting, harvesting, and — if a sanctioner — enforcing).
        round: Zero-based round at which the disturbance fires.
        magnitude: Kind-specific size, always a fraction in ``(0, 1]``. For
            ``"resource_shock"`` it is the fraction of the stock removed (``0.7`` =
            lose 70%); for ``"agent_failure"`` it is the fraction of agents that fail
            (``0.25`` = one in four; agents fail in index/spec order).
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
class AgentSpec:
    """A homogeneous group of agents sharing one strategy.

    Attributes:
        strategy: Registered strategy name (see :mod:`strategies.registry`).
        count: Number of agents instantiated with this strategy.
        params: Strategy-specific keyword arguments.
    """

    strategy: str
    count: int = 1
    params: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.count < 0:
            raise ValueError("count must be non-negative")


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
        return cls(resource=resource, agents=agents, disturbances=disturbances, **data)


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
