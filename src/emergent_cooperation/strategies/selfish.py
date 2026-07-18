"""A short-horizon, self-interested strategy.

The selfish agent maximises its *immediate* harvest and ignores the resource's
future. When many selfish agents share the pool, their combined request exceeds
the sustainable yield, the engine scales everyone down, and the stock is driven
toward collapse — the classic tragedy of the commons. This strategy is the
primary non-cooperative baseline.
"""

from __future__ import annotations

import numpy as np

from ..agents.observation import Observation
from .base import Strategy


class SelfishStrategy(Strategy):
    """Grab a large slice of whatever appears available right now.

    Under the ``global`` information model the agent targets ``greed`` times an
    equal share of the *current* stock. With ``greed >= 1`` the collective demand
    of an all-selfish population meets or exceeds the whole stock, so the pool is
    emptied each round. Under the ``private`` model the stock is hidden, so the
    agent falls back to a fixed share of the carrying capacity.
    """

    name = "selfish"

    def __init__(self, greed: float = 1.0) -> None:
        """Create a selfish strategy.

        Args:
            greed: Multiplier on the agent's naive equal share. ``1.0`` means
                "try to take a full equal share of the visible stock".
        """
        if greed < 0:
            raise ValueError("greed must be non-negative")
        self.greed = greed

    def decide(self, observation: Observation, rng: np.random.Generator) -> float:
        """Request a greedy share of the visible (or assumed) stock."""
        n = max(1, observation.num_agents)
        if observation.resource_level is not None:
            visible = observation.resource_level
        else:
            # Blind fallback: assume the pool sits around its carrying capacity.
            visible = observation.capacity
        return self.greed * visible / n
