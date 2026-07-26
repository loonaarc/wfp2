"""A conditional cooperator (reciprocity) strategy.

Conditional cooperation is the *dominant* realistic behaviour observed in common-pool
experiments (Janssen et al. 2022 fit ~75% conditional cooperators). Such an agent
restrains like a cooperator **as long as the group also restrains**, but reciprocates
over-extraction by grabbing a selfish share itself — refusing to be the "sucker" that
subsidises free-riders.

It monitors the group indirectly through the shared stock: in an all-cooperative
equilibrium the observed (regrown) stock is steady, so a *decline* between rounds
signals that someone over-harvested. This needs no message passing — it is
monitoring via the environment (cf. Ostrom's monitoring principle). The strategy is
stateful (it remembers the previously observed stock); a fresh instance is created
per run, so no state leaks across runs.
"""

from __future__ import annotations

import numpy as np

from ..agents.observation import Observation
from .base import Strategy


class ConditionalCooperatorStrategy(Strategy):
    """Cooperate while the group does; reciprocate over-extraction selfishly.

    Under the ``global`` model the agent watches the shared stock. If the observed
    stock fell since last round (someone over-harvested), it *defects* this round and
    claims a selfish share; otherwise it *cooperates* and takes only its share of the
    surplus above the reference stock. Under the ``private`` model it cannot monitor
    the group and falls back to blind cooperative restraint.
    """

    name = "conditional_cooperator"

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
        """Create a conditional cooperator.

        Args:
            regeneration_rate: Assumed growth rate ``g`` (blind fallback).
            capacity: Assumed carrying capacity ``K``.
            target_fraction: Reference stock as a fraction of ``K`` (cooperate mode).
            restraint: Multiplier in ``(0, 1]`` on the cooperative share.
            defection_greed: Selfish share multiplier used when reciprocating.
            knowledge_bias: Bias on the blind yield estimate (private info).
            sensitivity: Minimum stock drop (absolute) that counts as
                over-extraction and triggers defection. Small by default so a steady
                equilibrium never spuriously triggers.
        """
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

    def decide(self, observation: Observation, rng: np.random.Generator) -> float:
        """Cooperate unless over-extraction is detected; then reciprocate.

        Over-extraction is detected from the *observed stock* (global information) or,
        when blind, from a *communicated signal* of the group's total harvest if one
        was received this round (broadcast communication, ADR-0007). With neither, the
        agent cannot monitor and simply restrains like a cooperator.
        """
        n = max(1, observation.num_agents)
        g, k = self.regeneration_rate, self.capacity
        sustainable_total = g * k / 4.0  # MSY

        if observation.resource_level is None:
            # Blind: use the communicated signal to monitor the group, if available.
            if observation.signal is not None:
                if observation.signal > sustainable_total + self.sensitivity:
                    # Communicated over-extraction: reciprocate with a selfish share.
                    return self.defection_greed * k / n
                return self.restraint * self.knowledge_bias * sustainable_total / n
            # No stock, no message: restrain like a cooperator.
            return self.restraint * self.knowledge_bias * sustainable_total / n

        level = observation.resource_level
        declined = self._last_level is not None and level < self._last_level - self.sensitivity
        self._last_level = level

        if declined:
            # Over-extraction detected: reciprocate by claiming a selfish share.
            return self.defection_greed * level / n
        # Otherwise cooperate: take only the surplus above the reference stock.
        target = self.target_fraction * k
        surplus = max(0.0, level - target)
        return self.restraint * surplus / n
