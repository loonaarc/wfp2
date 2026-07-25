"""A sustainability-oriented strategy.

The cooperative agent aims to keep the shared stock at a healthy reference level
(the maximum-sustainable-yield stock ``K/2``) and harvests only its share of the
*surplus* above that level. An all-cooperative population therefore holds the
stock steady and keeps harvesting indefinitely at the maximum sustainable yield.
The rule is self-correcting: when the stock is below the reference level the agent
harvests nothing and lets it recover, which is exactly the behaviour that makes
cooperation robust to disturbances.
"""

from __future__ import annotations

import numpy as np

from ..agents.observation import Observation
from .base import Strategy


class CooperativeStrategy(Strategy):
    """Harvest an equal share of the surplus above the reference stock.

    Under the ``global`` model the agent sees the (regrown) stock ``R`` and claims
    ``1/N`` of ``max(0, R - target)``, where ``target = target_fraction * K``.
    Under the ``private`` model it cannot see ``R``; it falls back to claiming
    ``1/N`` of the maximum sustainable yield ``g*K/4`` — sustainable when the pool
    happens to sit near ``K/2``, but blind to drift, which makes private
    cooperation fragile to initial conditions and disturbances.

    A ``restraint`` factor in ``(0, 1]`` optionally leaves an extra safety margin.
    """

    name = "cooperative"

    def __init__(
        self,
        regeneration_rate: float = 0.4,
        capacity: float = 100.0,
        target_fraction: float = 0.5,
        restraint: float = 1.0,
        knowledge_bias: float = 1.0,
    ) -> None:
        """Create a cooperative strategy.

        The decision fuses a *social preference* (restraint: take only a share of the
        surplus) with *ecological knowledge* (an estimate of the sustainable yield).
        ``knowledge_bias`` makes the second factor explicit and possibly wrong, so
        that "cooperative intent" and "sustainable outcome" can come apart (see
        ADR-0004 and Schill et al. 2016).

        Args:
            regeneration_rate: Assumed intrinsic growth rate ``g`` (blind fallback).
            capacity: Assumed carrying capacity ``K``.
            target_fraction: Reference stock as a fraction of ``K`` to maintain
                (``0.5`` is the maximum-sustainable-yield point).
            restraint: Multiplier in ``(0, 1]`` applied to the harvested share.
            knowledge_bias: Multiplier on the agent's estimate of the sustainable
                yield used when it *cannot observe* the stock (private information).
                ``1.0`` = accurate; ``> 1`` overestimates (drives over-extraction);
                ``< 1`` underestimates (over-conservative). With global information
                the agent observes the stock and self-corrects, so this has little
                effect — observation substitutes for ecological knowledge.
        """
        if regeneration_rate < 0:
            raise ValueError("regeneration_rate must be non-negative")
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        if not 0 < target_fraction <= 1:
            raise ValueError("target_fraction must be in (0, 1]")
        if not 0 < restraint <= 1:
            raise ValueError("restraint must be in (0, 1]")
        if knowledge_bias < 0:
            raise ValueError("knowledge_bias must be non-negative")
        self.regeneration_rate = regeneration_rate
        self.capacity = capacity
        self.target_fraction = target_fraction
        self.restraint = restraint
        self.knowledge_bias = knowledge_bias

    def decide(self, observation: Observation, rng: np.random.Generator) -> float:
        """Request an equal share of the surplus above the reference stock."""
        n = max(1, observation.num_agents)
        g, k = self.regeneration_rate, self.capacity
        if observation.resource_level is not None:
            # Observed stock: self-correct toward the healthy reference level.
            target = self.target_fraction * k
            surplus = max(0.0, observation.resource_level - target)
            return self.restraint * surplus / n
        # Blind: rely on the (possibly biased) estimate of the sustainable yield g*K/4.
        estimated_yield = self.knowledge_bias * (g * k / 4.0)
        return self.restraint * estimated_yield / n
