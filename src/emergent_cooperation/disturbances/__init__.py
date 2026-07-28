"""Environmental disturbances for resilience experiments.

A disturbance is an external perturbation the engine applies at a scheduled round:
it may cut the standing stock, remove agents, or degrade communication. The world
runs normally, a shock lands at a known round, and the resilience metrics measure
how (and whether) cooperation recovers.

Disturbances are **deterministic and config-driven** (scheduled by round, not by a
random draw), so a run stays a pure function of ``(config, seed)``: the shock is
part of the configuration, not a source of hidden randomness. See ADR-0008.

Implemented kinds: :class:`~emergent_cooperation.disturbances.shocks.ResourceShock`
(a pulse loss of stock) and
:class:`~emergent_cooperation.disturbances.shocks.AgentFailure` (agents dropping out).
Communication failure and misleading information are the next kinds to add against
the same interface.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from ..core.config import DisturbanceConfig
from .shocks import AgentFailure, ResourceShock, build_disturbances


@runtime_checkable
class Disturbance(Protocol):
    """Interface for an environmental perturbation applied at a round boundary.

    A concrete disturbance carries its own schedule (which round it fires on) and
    mutates the world in place — the pool and/or the agent population. It is invoked
    every round by the engine and decides for itself whether to act.
    """

    def apply(self, round_index: int, pool: object, agents: list) -> bool:
        """Apply the disturbance in place if scheduled for ``round_index``.

        Returns:
            ``True`` if the disturbance fired this round, ``False`` otherwise. The
            engine uses this to mark disturbed rounds in the run record.
        """
        ...


__all__ = [
    "AgentFailure",
    "Disturbance",
    "DisturbanceConfig",
    "ResourceShock",
    "build_disturbances",
]
