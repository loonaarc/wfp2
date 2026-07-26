"""A sanctioning strategy: cooperate *and* enforce a sustainable harvest quota.

A sanctioner harvests sustainably like a cooperator, but additionally *monitors* the
group and upholds a harvest quota: the engine confiscates any agent's over-extraction
back into the pool (see ADR-0005 and the enforcement phase in
:mod:`core.simulation`). Monitoring is not free — the sanctioner forfeits a small
payoff each round.

Unlike reciprocity (the conditional cooperator), enforcement reduces defectors'
*extraction*, not just their payoff, so it protects the resource even against fixed,
non-adaptive selfish agents. It also surfaces the classic **second-order free-rider**
problem: a plain cooperator that does not pay the monitoring cost out-earns a
sanctioner that does.
"""

from __future__ import annotations

import numpy as np

from ..agents.observation import Observation
from .base import SanctionPolicy, Strategy


class SanctioningStrategy(Strategy):
    """Harvest sustainably and enforce a per-capita sustainable quota.

    Harvest behaviour matches the cooperative strategy (take only the surplus above
    the reference stock, or a share of the maximum sustainable yield when blind). In
    addition it exposes a :class:`SanctionPolicy` so the engine caps every agent's
    harvest at ``quota_total / N`` and returns confiscated excess to the pool.
    """

    name = "sanctioning"

    def __init__(
        self,
        regeneration_rate: float = 0.4,
        capacity: float = 100.0,
        target_fraction: float = 0.5,
        restraint: float = 1.0,
        monitoring_cost: float = 0.2,
    ) -> None:
        """Create a sanctioning strategy.

        Args:
            regeneration_rate: Assumed growth rate ``g``. With ``capacity`` it sets
                the enforced quota to the maximum sustainable yield ``g*K/4``.
            capacity: Assumed carrying capacity ``K``.
            target_fraction: Reference stock as a fraction of ``K`` (harvest mode).
            restraint: Multiplier in ``(0, 1]`` on the harvested share.
            monitoring_cost: Payoff forfeited each round for monitoring the group.
        """
        if regeneration_rate < 0:
            raise ValueError("regeneration_rate must be non-negative")
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        if not 0 < target_fraction <= 1:
            raise ValueError("target_fraction must be in (0, 1]")
        if not 0 < restraint <= 1:
            raise ValueError("restraint must be in (0, 1]")
        if monitoring_cost < 0:
            raise ValueError("monitoring_cost must be non-negative")
        self.regeneration_rate = regeneration_rate
        self.capacity = capacity
        self.target_fraction = target_fraction
        self.restraint = restraint
        self.monitoring_cost = monitoring_cost

    def decide(self, observation: Observation, rng: np.random.Generator) -> float:
        """Harvest sustainably (same rule as the cooperative strategy)."""
        n = max(1, observation.num_agents)
        g, k = self.regeneration_rate, self.capacity
        if observation.resource_level is not None:
            target = self.target_fraction * k
            surplus = max(0.0, observation.resource_level - target)
            return self.restraint * surplus / n
        return self.restraint * (g * k / 4.0) / n

    def sanction_policy(self) -> SanctionPolicy:
        """Enforce a quota equal to the maximum sustainable yield ``g*K/4``."""
        quota_total = self.regeneration_rate * self.capacity / 4.0
        return SanctionPolicy(quota_total=quota_total, monitoring_cost=self.monitoring_cost)
