"""What an agent perceives at decision time.

The observation is the *only* channel through which a strategy learns about the
world, which is what makes information models meaningful: under the ``private``
model the shared ``resource_level`` is withheld (set to ``None``), so a strategy
must fall back on its own history and structural constants. Keeping this in one
dataclass makes the information boundary explicit and testable.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Observation:
    """A single agent's view of the world at the start of a round.

    Attributes:
        round_index: Zero-based current round.
        num_agents: Total number of agents in the system (structural knowledge).
        capacity: Resource carrying capacity ``K`` (structural knowledge).
        resource_level: Current shared stock, or ``None`` if withheld by the
            information model.
        own_last_harvest: This agent's realised harvest in the previous round
            (0.0 in the first round).
        own_total_payoff: This agent's accumulated harvest so far.
    """

    round_index: int
    num_agents: int
    capacity: float
    resource_level: float | None
    own_last_harvest: float
    own_total_payoff: float
