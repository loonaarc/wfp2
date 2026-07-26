"""A compensating cooperator: restrain harder when others over-extract.

Where the conditional cooperator *retaliates* on detected over-extraction (grabbing a
selfish share, which protects its payoff but collapses the resource), the compensating
cooperator does the opposite: it *withholds* — harvesting nothing that round — to leave
the pool room to recover. This is the restraint/agreement response to communication
(cf. Janssen et al. 2022: communication → trust → restraint), the natural counterpart
to E6's retaliation response.

It detects over-extraction the same way the conditional cooperator does: from the
observed stock declining (global information) or from a communicated `signal` that the
group's harvest exceeded the sustainable yield (broadcast communication, ADR-0007).
"""

from __future__ import annotations

import numpy as np

from ..agents.observation import Observation
from .base import Strategy


class CompensatingCooperatorStrategy(Strategy):
    """Cooperate; on detected over-extraction, withhold to let the resource recover."""

    name = "compensating_cooperator"

    def __init__(
        self,
        regeneration_rate: float = 0.4,
        capacity: float = 100.0,
        target_fraction: float = 0.5,
        restraint: float = 1.0,
        knowledge_bias: float = 1.0,
        sensitivity: float = 1e-9,
    ) -> None:
        """Create a compensating cooperator (see the module docstring for parameters)."""
        if not 0 < target_fraction <= 1:
            raise ValueError("target_fraction must be in (0, 1]")
        if not 0 < restraint <= 1:
            raise ValueError("restraint must be in (0, 1]")
        if knowledge_bias < 0 or sensitivity < 0:
            raise ValueError("knowledge_bias and sensitivity must be non-negative")
        self.regeneration_rate = regeneration_rate
        self.capacity = capacity
        self.target_fraction = target_fraction
        self.restraint = restraint
        self.knowledge_bias = knowledge_bias
        self.sensitivity = sensitivity
        self._last_level: float | None = None

    def decide(self, observation: Observation, rng: np.random.Generator) -> float:
        """Cooperate unless over-extraction is detected; then withhold (harvest 0)."""
        n = max(1, observation.num_agents)
        g, k = self.regeneration_rate, self.capacity
        sustainable_total = g * k / 4.0  # MSY

        if observation.resource_level is None:
            # Blind: use the communicated signal to monitor the group, if available.
            if (
                observation.signal is not None
                and observation.signal > sustainable_total + self.sensitivity
            ):
                return 0.0  # over-extraction communicated: withhold to compensate
            return self.restraint * self.knowledge_bias * sustainable_total / n

        level = observation.resource_level
        declined = self._last_level is not None and level < self._last_level - self.sensitivity
        self._last_level = level
        if declined:
            return 0.0  # over-extraction observed: withhold to let the pool recover
        target = self.target_fraction * k
        surplus = max(0.0, level - target)
        return self.restraint * surplus / n
