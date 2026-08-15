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
        active: Whether the agent is still participating. An ``agent_failure``
            disturbance sets this ``False``; a failed agent requests and harvests
            nothing and (if a sanctioner) stops enforcing.
        group: Nested-enterprise membership (see
            :attr:`~emergent_cooperation.core.config.AgentSpec.group`, ADR-0012).
            Enforcement is scoped to agents sharing the same group.
        governed: Whether this agent is part of the community whose
            sustainable yield is being fairly allocated (see
            :attr:`~emergent_cooperation.core.config.AgentSpec.governed`).
            ``False`` for an outsider (ADR-0013) — excluded from every
            group's per-capita quota denominator, not just left unmonitored.
        reputation: Image score (Nowak & Sigmund 1998; ADR-0014) — updated by
            the engine every round regardless of this agent's own strategy
            (``+1`` for a round at/below the governed community's fair share,
            ``-1`` above it), so it is a real, always-tracked number, not a
            fiction specific to :class:`~emergent_cooperation.strategies.
            reputation.ReputationCooperatorStrategy`.
    """

    def __init__(
        self,
        agent_id: int,
        strategy: Strategy,
        decision_noise: float = 0.0,
        group: int = 0,
        governed: bool = True,
    ) -> None:
        """Create an agent bound to ``strategy``.

        Args:
            agent_id: Stable index identifying the agent.
            strategy: The decision rule this agent follows.
            decision_noise: Fractional noise on the request (see
                :class:`~emergent_cooperation.core.config.SimulationConfig`).
            group: Nested-enterprise membership (ADR-0012).
            governed: Whether this agent counts toward the governed
                population's fair-share allocation (ADR-0012 correction).
        """
        self.agent_id = agent_id
        self.strategy = strategy
        self.decision_noise = decision_noise
        self.group = group
        self.governed = governed
        self.total_payoff: float = 0.0
        self.last_harvest: float = 0.0
        self.active: bool = True
        self.reputation: float = 0.0

    @property
    def strategy_name(self) -> str:
        """Registered name of this agent's strategy."""
        return self.strategy.name

    def decide(self, observation: Observation, rng: np.random.Generator) -> float:
        """Return the agent's requested consumption for the round.

        If ``decision_noise`` is positive, the strategy's request is perturbed by a
        factor drawn uniformly from ``[1 - noise, 1 + noise]`` using the agent's own
        RNG, so the outcome depends reproducibly on the seed. The request is clamped
        to be non-negative; enforcing feasibility against the shared stock is the
        engine's responsibility, not the agent's.
        """
        request = self.strategy.decide(observation, rng)
        if self.decision_noise > 0.0:
            request *= 1.0 + rng.uniform(-self.decision_noise, self.decision_noise)
        return max(0.0, float(request))

    def record_harvest(self, amount: float) -> None:
        """Update payoff bookkeeping after the engine assigns a harvest."""
        self.last_harvest = amount
        self.total_payoff += amount
