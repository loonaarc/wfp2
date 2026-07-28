"""Concrete disturbances that perturb the resource.

This module implements the disturbance kinds declared in
:data:`~emergent_cooperation.core.config.DISTURBANCE_KINDS`. Each class satisfies
the :class:`~emergent_cooperation.disturbances.Disturbance` protocol: it holds its
own schedule and mutates the world in place when its round arrives.
"""

from __future__ import annotations

from ..core.config import DisturbanceConfig
from ..environment.resource import ResourcePool


class ResourceShock:
    """A single-round "pulse" loss of resource stock.

    At round :attr:`round`, the pool's standing stock is multiplied by
    ``(1 - magnitude)`` — e.g. ``magnitude = 0.7`` instantly removes 70% of the
    resource, modelling a drought, disease die-off, or pollution event. The shock is
    applied after regeneration, so agents observing the stock (``global`` model) see
    and can react to the depleted level in the same round.
    """

    def __init__(self, round: int, magnitude: float) -> None:
        """Create a shock that fires once at ``round``, removing ``magnitude`` of stock."""
        self.round = round
        self.magnitude = magnitude

    def apply(self, round_index: int, pool: ResourcePool, agents: list) -> bool:
        """Cut the stock by ``magnitude`` when ``round_index`` matches the schedule."""
        if round_index != self.round:
            return False
        pool.level = max(0.0, pool.level * (1.0 - self.magnitude))
        return True


def _build_one(config: DisturbanceConfig):
    """Construct the concrete disturbance for one :class:`DisturbanceConfig`."""
    if config.kind == "resource_shock":
        return ResourceShock(round=config.round, magnitude=config.magnitude)
    # Unreachable: DisturbanceConfig validates kind against DISTURBANCE_KINDS.
    raise ValueError(f"unsupported disturbance kind: {config.kind!r}")


def build_disturbances(configs: tuple[DisturbanceConfig, ...]) -> list:
    """Turn the config's disturbance specs into concrete disturbance objects."""
    return [_build_one(c) for c in configs]
