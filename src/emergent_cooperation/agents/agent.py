"""The agent container.

An :class:`Agent` is intentionally thin: it owns identity and mutable per-run
state (accumulated payoff, last harvest) and delegates every decision to a
pluggable :class:`~emergent_cooperation.strategies.base.Strategy`. This keeps
*what an agent is* separate from *how it decides*, so strategies can be swapped,
mixed, and compared without touching the agent or the engine.
"""

from __future__ import annotations

import numpy as np

from ..strategies.base import Strategy
from .observation import Observation


class Agent:
    """A single decision-making entity in the simulation.

    Attributes:
        agent_id: Stable index identifying the agent within a run.
        strategy: The decision rule this agent follows.
        total_payoff: Accumulated realised harvest over the run.
        last_harvest: Realised harvest from the most recent round.
    """

    def __init__(self, agent_id: int, strategy: Strategy) -> None:
        """Create an agent bound to ``strategy``."""
        self.agent_id = agent_id
        self.strategy = strategy
        self.total_payoff: float = 0.0
        self.last_harvest: float = 0.0

    @property
    def strategy_name(self) -> str:
        """Registered name of this agent's strategy."""
        return self.strategy.name

    def decide(self, observation: Observation, rng: np.random.Generator) -> float:
        """Return the agent's requested consumption for the round.

        The request is clamped to be non-negative; enforcing feasibility against
        the shared stock is the engine's responsibility, not the agent's.
        """
        request = self.strategy.decide(observation, rng)
        return max(0.0, float(request))

    def record_harvest(self, amount: float) -> None:
        """Update payoff bookkeeping after the engine assigns a harvest."""
        self.last_harvest = amount
        self.total_payoff += amount
