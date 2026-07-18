"""Tests for the renewable resource pool."""

import pytest

from emergent_cooperation.core.config import ResourceConfig
from emergent_cooperation.environment.resource import ResourcePool


def test_logistic_growth_peaks_at_half_capacity():
    cfg = ResourceConfig(initial_level=50.0, capacity=100.0, regeneration_rate=0.4)
    pool = ResourcePool(cfg)
    pool.regenerate()
    # dR = 0.4 * 50 * (1 - 50/100) = 10 -> 60
    assert pool.level == pytest.approx(60.0)


def test_growth_is_capped_at_capacity():
    cfg = ResourceConfig(initial_level=99.0, capacity=100.0, regeneration_rate=1.0)
    pool = ResourcePool(cfg)
    pool.regenerate()
    assert pool.level <= cfg.capacity


def test_depleted_pool_cannot_recover_under_logistic():
    cfg = ResourceConfig(initial_level=0.0, capacity=100.0, regeneration_rate=0.5)
    pool = ResourcePool(cfg)
    pool.regenerate()
    assert pool.level == 0.0


def test_withdraw_is_clipped_to_available_stock():
    cfg = ResourceConfig(initial_level=10.0, capacity=100.0)
    pool = ResourcePool(cfg)
    removed = pool.withdraw(25.0)
    assert removed == 10.0
    assert pool.level == 0.0


def test_collapse_flag():
    cfg = ResourceConfig(initial_level=0.5, capacity=100.0, collapse_threshold=1.0)
    pool = ResourcePool(cfg)
    assert pool.is_collapsed


def test_negative_withdrawal_rejected():
    pool = ResourcePool(ResourceConfig())
    with pytest.raises(ValueError):
        pool.withdraw(-1.0)
