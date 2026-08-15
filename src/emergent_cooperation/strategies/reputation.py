"""A reputation-based (indirect reciprocity) cooperator strategy.

Nowak & Sigmund (1998), "Evolution of Indirect Reciprocity by Image Scoring":
cooperation can be sustained without repeated interaction between the same two
individuals, as long as behaviour is at least partly observable and agents
condition their own generosity on a partner's observed reputation rather than
on personal history with them or on the population's aggregate state.

This is deliberately *not* a population-wide trigger the way
:class:`~emergent_cooperation.strategies.conditional.ConditionalCooperatorStrategy`
is (that strategy reacts to the whole group's aggregate stock trend, and
switches every instance of it to defection at once the moment the trend dips).
Here, each agent is paired with one random *other* agent every round
(``Simulation._observe``) and reacts only to that specific partner's
reputation -- so in a population that is mostly trustworthy, only whoever
happens to draw one of the few bad-reputation partners defects on a given
round, not everyone simultaneously. Requires ``SimulationConfig.reputation``
to be configured; every agent's own reputation score is tracked and updated by
the engine regardless of strategy (a real, always-on number, not a fiction
specific to this strategy) -- see ``Simulation._update_reputation``.
"""

from __future__ import annotations

import numpy as np

from ..agents.observation import Observation
from .base import Strategy


class ReputationCooperatorStrategy(Strategy):
    """Cooperate unless this round's randomly assigned partner is distrusted.

    Under the ``global`` model, cooperating means taking only the surplus above
    the reference stock, same formula as :class:`CooperativeStrategy`; defecting
    means claiming a selfish share of the current stock. Under ``private`` it
    falls back to the blind cooperative/defect formulas
    :class:`ConditionalCooperatorStrategy` already uses, for the same reason
    (no stock to size a share against). Distrust fires when
    ``Observation.partner_reputation`` is known and below :attr:`trust_threshold`;
    an *unknown* partner (not observed this round -- see ``ReputationConfig.
    visibility``) defaults to trusted, "innocent until proven guilty."
    """

    name = "reputation_cooperator"

    def __init__(
        self,
        regeneration_rate: float = 0.4,
        capacity: float = 100.0,
        target_fraction: float = 0.5,
        restraint: float = 1.0,
        defection_greed: float = 1.0,
        knowledge_bias: float = 1.0,
        trust_threshold: float = 0.0,
    ) -> None:
        """Create a reputation-based cooperator.

        Args:
            regeneration_rate: Assumed growth rate ``g`` (blind fallback).
            capacity: Assumed carrying capacity ``K``.
            target_fraction: Reference stock as a fraction of ``K`` (cooperate mode).
            restraint: Multiplier in ``(0, 1]`` on the cooperative share.
            defection_greed: Selfish share multiplier used when distrusting.
            knowledge_bias: Bias on the blind yield estimate (private info).
            trust_threshold: A partner's reputation must be at or above this to
                be trusted. ``0.0`` (the default, matching the engine's own
                +1/-1 scoring) trusts anyone whose recent behaviour was, on net,
                at or below its fair share.
        """
        if not 0 < target_fraction <= 1:
            raise ValueError("target_fraction must be in (0, 1]")
        if not 0 < restraint <= 1:
            raise ValueError("restraint must be in (0, 1]")
        if defection_greed < 0 or knowledge_bias < 0:
            raise ValueError("defection_greed and knowledge_bias must be non-negative")
        self.regeneration_rate = regeneration_rate
        self.capacity = capacity
        self.target_fraction = target_fraction
        self.restraint = restraint
        self.defection_greed = defection_greed
        self.knowledge_bias = knowledge_bias
        self.trust_threshold = trust_threshold

    def decide(self, observation: Observation, rng: np.random.Generator) -> float:
        """Cooperate unless this round's partner is known and distrusted."""
        n = max(1, observation.num_agents)
        g, k = self.regeneration_rate, self.capacity
        sustainable_total = g * k / 4.0  # MSY

        distrust = (
            observation.partner_reputation is not None
            and observation.partner_reputation < self.trust_threshold
        )

        if observation.resource_level is None:
            # Blind: no stock to size a share against, same fallback as
            # ConditionalCooperatorStrategy.
            if distrust:
                return self.defection_greed * k / n
            return self.restraint * self.knowledge_bias * sustainable_total / n

        if distrust:
            return self.defection_greed * observation.resource_level / n
        target = self.target_fraction * k
        surplus = max(0.0, observation.resource_level - target)
        return self.restraint * surplus / n
