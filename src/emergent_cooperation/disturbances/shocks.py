"""Concrete disturbances.

This module implements the disturbance kinds declared in
:data:`~emergent_cooperation.core.config.DISTURBANCE_KINDS`. Each class satisfies
the :class:`~emergent_cooperation.disturbances.Disturbance` protocol: it holds its
own schedule and mutates the world (the pool and/or the agents) in place when its
round arrives.
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


class AgentFailure:
    """Agents dropping out at a scheduled round (equipment failure, exit, sabotage).

    At round :attr:`round`, the first ``fraction`` of the agents (by index / spec
    order) are **deactivated**: from then on they request nothing, harvest nothing,
    and — crucially — a failed sanctioner stops enforcing. Because agents fail in
    index order, an experiment controls *who* fails by ordering the population (put
    the group meant to fail first). This tests tolerance to agent loss: a commons
    held up by a monitor is fragile to losing it; a self-correcting one is not.
    """

    def __init__(self, round: int, fraction: float) -> None:
        """Create a failure that fires once at ``round``, failing ``fraction`` of agents."""
        self.round = round
        self.fraction = fraction

    def apply(self, round_index: int, pool: ResourcePool, agents: list) -> bool:
        """Deactivate the first ``fraction`` of still-active agents on the scheduled round."""
        if round_index != self.round:
            return False
        to_fail = max(1, round(self.fraction * len(agents)))
        fired = False
        for a in agents:
            if to_fail <= 0:
                break
            if getattr(a, "active", True):
                a.active = False
                to_fail -= 1
                fired = True
        return fired


class AgentTurnover:
    """A fraction of agents' own strategy memory reset at a scheduled round.

    At round :attr:`round`, :attr:`fraction` of the *active* agents, starting
    from a deterministic rotation offset (``round_index % len(agents)``),
    each have their strategy's :meth:`~..strategies.base.Strategy.reset_state`
    called and their reputation cleared -- as if a fresh individual, with no
    memory of any prior decline or trigger, took over that role (Duffy &
    Lafky 2015's overlapping-generations turnover; E24, ADR-0021). Unlike
    :class:`AgentFailure`, the agent stays active and keeps its accumulated
    ``total_payoff`` -- this models a *replacement*, not a loss. The
    rotation offset is a pure function of the round, not shared cursor state,
    so multiple scheduled turnover events naturally touch different agents
    without needing cross-instance coordination.
    """

    def __init__(self, round: int, fraction: float) -> None:
        """Create a turnover event firing once at ``round``, resetting ``fraction`` of agents."""
        self.round = round
        self.fraction = fraction

    def apply(self, round_index: int, pool: ResourcePool, agents: list) -> bool:
        """Reset the strategy state of a rotating fraction of agents on the scheduled round."""
        if round_index != self.round:
            return False
        n = len(agents)
        if n == 0:
            return False
        to_reset = max(1, round(self.fraction * n))
        offset = round_index % n
        fired = False
        for j in range(to_reset):
            agent = agents[(offset + j) % n]
            if not getattr(agent, "active", True):
                continue
            agent.strategy.reset_state()
            agent.reputation = 0
            fired = True
        return fired


def _build_one(config: DisturbanceConfig):
    """Construct the concrete disturbance for one :class:`DisturbanceConfig`."""
    if config.kind == "resource_shock":
        return ResourceShock(round=config.round, magnitude=config.magnitude)
    if config.kind == "agent_failure":
        return AgentFailure(round=config.round, fraction=config.magnitude)
    if config.kind == "agent_turnover":
        return AgentTurnover(round=config.round, fraction=config.magnitude)
    # Unreachable: DisturbanceConfig validates kind against DISTURBANCE_KINDS.
    raise ValueError(f"unsupported disturbance kind: {config.kind!r}")


def build_disturbances(configs: tuple[DisturbanceConfig, ...]) -> list:
    """Turn the config's disturbance specs into concrete disturbance objects."""
    return [_build_one(c) for c in configs]
