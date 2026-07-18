"""The renewable common-pool resource.

The resource holds a scalar stock that agents draw from and that regenerates each
round. Regeneration is deterministic given the stock; all stochasticity in the
project lives in agent decisions, not (yet) in the environment. Disturbances that
perturb the environment will be layered on top of this in :mod:`disturbances`.
"""

from __future__ import annotations

from ..core.config import ResourceConfig


class ResourcePool:
    """A single scalar renewable resource with a configurable regeneration rule.

    The pool tracks only its stock and how it grows. It does *not* decide how a
    round's total harvest is split among agents; that allocation lives in the
    engine, because it needs per-agent information the pool has no reason to know.
    """

    def __init__(self, config: ResourceConfig) -> None:
        """Initialise the pool at ``config.initial_level``."""
        self._config = config
        self.level: float = config.initial_level

    @property
    def config(self) -> ResourceConfig:
        """The immutable configuration of this pool."""
        return self._config

    @property
    def is_collapsed(self) -> bool:
        """Whether the stock is at or below the collapse threshold."""
        return self.level <= self._config.collapse_threshold

    def withdraw(self, amount: float) -> float:
        """Remove up to ``amount`` from the stock and return what was removed.

        Withdrawals are clipped to the available stock; the pool never goes
        negative. Feasibility across multiple agents is handled by the caller.

        Args:
            amount: Requested non-negative withdrawal.

        Returns:
            The amount actually removed.
        """
        if amount < 0:
            raise ValueError("withdrawal amount must be non-negative")
        removed = min(amount, self.level)
        self.level -= removed
        return removed

    def regenerate(self) -> None:
        """Grow the stock in place according to the configured rule.

        ``logistic``: ``dR = g * R * (1 - R / K)`` — self-limiting growth that
        peaks at ``R = K/2`` and vanishes at 0 and ``K``. A stock driven to 0
        cannot recover, which is what makes over-extraction irreversible.

        ``linear``: ``dR = g * R`` — exponential growth, capped at ``K``.
        """
        cfg = self._config
        r, k, g = self.level, cfg.capacity, cfg.regeneration_rate
        if cfg.regeneration_rule == "logistic":
            growth = g * r * (1.0 - r / k)
        else:  # "linear"; validated in ResourceConfig
            growth = g * r
        self.level = min(k, max(0.0, r + growth))
