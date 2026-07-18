"""The strategy interface.

A strategy maps an :class:`~emergent_cooperation.agents.observation.Observation`
to a requested consumption. Strategies must be *pure* with respect to hidden
global state: any randomness must be drawn from the ``rng`` passed in, never from
module-level or global generators, so that runs stay reproducible.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

import numpy as np

from ..agents.observation import Observation


class Strategy(ABC):
    """Abstract base class for local decision rules.

    Subclasses set :attr:`name` (used by the registry and in result records) and
    implement :meth:`decide`. Strategy parameters are supplied as keyword
    arguments at construction time and stored on the instance.
    """

    #: Registry key; overridden by every concrete subclass.
    name: str = "abstract"

    @abstractmethod
    def decide(self, observation: Observation, rng: np.random.Generator) -> float:
        """Return the requested consumption for this round.

        Args:
            observation: The agent's view of the world (see information models).
            rng: The agent's private, reproducible random generator.

        Returns:
            A non-negative requested consumption. The engine may scale it down if
            the collective request exceeds the available stock.
        """
        raise NotImplementedError
