"""The strategy interface.

A strategy maps an :class:`~emergent_cooperation.agents.observation.Observation`
to a requested consumption. Strategies must be *pure* with respect to hidden
global state: any randomness must be drawn from the ``rng`` passed in, never from
module-level or global generators, so that runs stay reproducible.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

import numpy as np

from ..agents.observation import Observation


@dataclass(frozen=True)
class SanctionPolicy:
    """A monitoring-and-enforcement rule an agent is willing to uphold.

    A strategy that exposes a policy makes the engine enforce a per-round harvest
    quota on *every* agent (over-extraction is confiscated back to the pool), in
    exchange for the sanctioner paying a monitoring cost. See ADR-0005 and
    :meth:`Strategy.sanction_policy`.

    Attributes:
        quota_total: The sustainable *total* harvest the quota targets; the engine
            enforces a per-capita cap of ``quota_total / num_agents``.
        monitoring_cost: Payoff the sanctioner forfeits each round for monitoring.
    """

    quota_total: float
    monitoring_cost: float = 0.0


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

    def sanction_policy(self) -> SanctionPolicy | None:
        """Return this strategy's enforcement policy, or ``None`` if it does not sanction.

        The default is ``None`` (no sanctioning). A monitoring strategy overrides
        this to make the engine enforce a harvest quota (see ADR-0005).
        """
        return None

    def reset_state(self) -> None:
        """Clear any per-round memory, as if a fresh individual took this role.

        The default is a no-op. Strategies that track history across rounds
        (``conditional_cooperator``, ``compensating_cooperator``,
        ``grim_trigger``) override this to clear it, for the ``agent_turnover``
        disturbance (E24, ADR-0021) — a strategy with no memory has nothing to
        reset, so turnover is a verified no-op wherever this isn't overridden.
        """
        return None
