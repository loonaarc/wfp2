"""Strategy registry.

Configs refer to strategies by name; the registry maps those names to classes and
constructs instances with config-supplied parameters. New strategies register
themselves here, which is the single extension point for adding decision rules.
"""

from __future__ import annotations

from typing import Any

from .base import Strategy
from .compensating import CompensatingCooperatorStrategy
from .conditional import ConditionalCooperatorStrategy
from .cooperative import CooperativeStrategy
from .loner import LonerStrategy
from .reputation import ReputationCooperatorStrategy
from .sanctioning import SanctioningStrategy
from .selfish import SelfishStrategy

STRATEGY_REGISTRY: dict[str, type[Strategy]] = {}


def register_strategy(cls: type[Strategy]) -> type[Strategy]:
    """Register a strategy class under its ``name`` attribute.

    Args:
        cls: A concrete :class:`Strategy` subclass with a unique ``name``.

    Returns:
        The class unchanged (usable as a decorator).
    """
    name = cls.name
    if name in STRATEGY_REGISTRY and STRATEGY_REGISTRY[name] is not cls:
        raise ValueError(f"strategy name {name!r} is already registered")
    STRATEGY_REGISTRY[name] = cls
    return cls


def make_strategy(name: str, params: dict[str, Any] | None = None) -> Strategy:
    """Instantiate a registered strategy by name.

    Args:
        name: Registered strategy key.
        params: Keyword arguments passed to the strategy constructor.

    Returns:
        A ready-to-use strategy instance.
    """
    if name not in STRATEGY_REGISTRY:
        raise KeyError(f"unknown strategy {name!r}; available: {sorted(STRATEGY_REGISTRY)}")
    return STRATEGY_REGISTRY[name](**(params or {}))


def available_strategies() -> list[str]:
    """Return the sorted names of all registered strategies."""
    return sorted(STRATEGY_REGISTRY)


register_strategy(SelfishStrategy)
register_strategy(CooperativeStrategy)
register_strategy(ConditionalCooperatorStrategy)
register_strategy(SanctioningStrategy)
register_strategy(CompensatingCooperatorStrategy)
register_strategy(LonerStrategy)
register_strategy(ReputationCooperatorStrategy)
