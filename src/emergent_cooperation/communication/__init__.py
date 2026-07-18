"""Communication models (planned extension point).

This package will host message-passing between agents: no-communication,
peer-to-peer, broadcast, range-limited, budget-limited, delayed, and lossy
channels, plus changing network topologies (see ``docs/research-direction.md``).

Status: not yet implemented. The first prototype compares information models
(``global`` vs ``private``) rather than explicit messaging, because information
availability is the cheaper, more fundamental variable to isolate first. The
:class:`CommunicationModel` protocol below fixes the intended interface so the
engine can adopt it without churn once messaging work begins.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class CommunicationModel(Protocol):
    """Planned interface for a communication channel between agents.

    A concrete model will receive the messages agents wish to send in a round and
    return, per agent, the messages that agent actually receives — applying range
    limits, budgets, delays, and drops. The exact message payload type will be
    fixed when the first model is implemented.
    """

    def exchange(self, outgoing: dict[int, list[object]]) -> dict[int, list[object]]:
        """Route ``outgoing`` messages and return each agent's inbox."""
        ...
