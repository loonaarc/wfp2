"""Interchangeable local decision rules and their registry."""

from .base import Strategy
from .registry import STRATEGY_REGISTRY, available_strategies, make_strategy, register_strategy

__all__ = [
    "Strategy",
    "STRATEGY_REGISTRY",
    "available_strategies",
    "make_strategy",
    "register_strategy",
]
