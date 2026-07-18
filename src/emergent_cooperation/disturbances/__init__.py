"""Environmental disturbances (planned extension point).

This package will host perturbations for resilience experiments: agent failure,
sudden resource loss, slower regeneration, communication failure, message delay,
misleading information, and agents joining or leaving (see
``docs/research-direction.md``).

Status: not yet implemented. The :class:`Disturbance` protocol fixes the intended
hook — a callback invoked by the engine at a round boundary that may mutate the
world — so resilience scenarios can be added without redesigning the engine.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class Disturbance(Protocol):
    """Planned interface for an environmental perturbation.

    A concrete disturbance inspects the round index and may mutate the pool and/or
    the agent population (e.g. remove an agent, cut the stock). Returning nothing;
    effects are applied in place. Scheduling (which rounds it fires on) is part of
    each concrete implementation.
    """

    def apply(self, round_index: int, pool: object, agents: list) -> None:
        """Apply the disturbance in place for the given round, if scheduled."""
        ...
