"""A grim-trigger strategy: defect forever after the first over-extraction.

Friedman (1971), "A Non-cooperative Equilibrium for Supergames": a
non-cooperative equilibrium that sustains a Pareto-improving outcome purely
out of fear of permanent reversion to the one-shot (selfish) equilibrium,
with no external enforcement or binding agreement required. This is the
literal grim-trigger construction (E21, ADR-0018) -- a genuine strategy-space
gap this project's engine had: :class:`~.conditional.ConditionalCooperatorStrategy`
detects the same kind of decline but re-evaluates fresh every round, so a
single bad round resolves as soon as the stock stops falling. Grim trigger
never forgives.
"""

from __future__ import annotations

import numpy as np

from ..agents.observation import Observation
from .base import Strategy


class GrimTriggerStrategy(Strategy):
    """Cooperate like :class:`ConditionalCooperatorStrategy`, but permanently.

    Harvest rule is identical to ``conditional_cooperator``: take only the
    surplus above the reference stock while nothing looks wrong, or a
    selfish-sized share once something does. The one difference is memory --
    the first detected decline latches ``_triggered = True`` forever; every
    round after that, regardless of what the stock does next, is treated as
    still-triggered.
    """

    name = "grim_trigger"

    def __init__(
        self,
        regeneration_rate: float = 0.4,
        capacity: float = 100.0,
        target_fraction: float = 0.5,
        restraint: float = 1.0,
        defection_greed: float = 1.0,
        knowledge_bias: float = 1.0,
        sensitivity: float = 1e-9,
    ) -> None:
        """Create a grim-trigger strategy (see the module docstring for parameters)."""
        if not 0 < target_fraction <= 1:
            raise ValueError("target_fraction must be in (0, 1]")
        if not 0 < restraint <= 1:
            raise ValueError("restraint must be in (0, 1]")
        if defection_greed < 0 or knowledge_bias < 0 or sensitivity < 0:
            raise ValueError("defection_greed, knowledge_bias, sensitivity must be non-negative")
        self.regeneration_rate = regeneration_rate
        self.capacity = capacity
        self.target_fraction = target_fraction
        self.restraint = restraint
        self.defection_greed = defection_greed
        self.knowledge_bias = knowledge_bias
        self.sensitivity = sensitivity
        self._last_level: float | None = None
        self._triggered: bool = False

    def reset_state(self) -> None:
        """Clear the permanent trigger, as if a fresh, never-provoked agent took this role (E24)."""
        self._last_level = None
        self._triggered = False

    def decide(self, observation: Observation, rng: np.random.Generator) -> float:
        """Cooperate until a decline is ever detected; defect for good after."""
        n = max(1, observation.num_agents)
        g, k = self.regeneration_rate, self.capacity
        sustainable_total = g * k / 4.0

        if observation.resource_level is None:
            over_threshold = sustainable_total + self.sensitivity
            if observation.signal is not None and observation.signal > over_threshold:
                self._triggered = True
            if self._triggered:
                return self.defection_greed * k / n
            return self.restraint * self.knowledge_bias * sustainable_total / n

        level = observation.resource_level
        declined = self._last_level is not None and level < self._last_level - self.sensitivity
        self._last_level = level
        if declined:
            self._triggered = True

        if self._triggered:
            return self.defection_greed * level / n
        target = self.target_fraction * k
        surplus = max(0.0, level - target)
        return self.restraint * surplus / n
