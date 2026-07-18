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
        resource: Resource parameters.
        agents: Ordered agent-group specifications.
    """

    name: str = "unnamed"
    rounds: int = 100
    seed: int = 0
    information_model: str = "global"
    resource: ResourceConfig = field(default_factory=ResourceConfig)
    agents: tuple[AgentSpec, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if self.rounds <= 0:
            raise ValueError("rounds must be positive")
        if self.information_model not in INFORMATION_MODELS:
            raise ValueError(
                f"information_model must be one of {INFORMATION_MODELS}, "
                f"got {self.information_model!r}"
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
        return cls(resource=resource, agents=agents, **data)


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
