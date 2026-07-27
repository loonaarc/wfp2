"""Communication models.

**A first broadcast model is already implemented** — but in :mod:`core`, not here:
``SimulationConfig.broadcast_reliability`` makes the engine deliver an aggregate
signal (the group's total harvest last round) into each agent's
:class:`~emergent_cooperation.agents.observation.Observation` (see ADR-0007), and
experiments E6/E7 rely on it.

This package holds the *reserved interface* for the fuller channel still to come:
per-agent message-passing with range, budget, delay, loss, and changing topologies
(see ``docs/research-direction.md``). The broadcast model grew inside ``core`` rather
than through this Protocol; :class:`CommunicationModel` fixes the intended per-agent
signature so that work can adopt it without churning the engine.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class CommunicationModel(Protocol):
    """Reserved interface for a *per-agent* communication channel (not yet used).

    The implemented broadcast model (ADR-0007) lives in :mod:`core` and does not go
    through this Protocol. A concrete per-agent model will receive the messages agents
    wish to send in a round and return, per agent, the messages that agent actually
    receives — applying range limits, budgets, delays, and drops. The exact message
    payload type will be fixed when that channel is implemented.
    """

    def exchange(self, outgoing: dict[int, list[object]]) -> dict[int, list[object]]:
        """Route ``outgoing`` messages and return each agent's inbox."""
        ...
