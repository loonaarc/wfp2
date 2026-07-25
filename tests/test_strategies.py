"""Tests for the baseline strategies and the registry."""

import numpy as np
import pytest

from emergent_cooperation.agents.observation import Observation
from emergent_cooperation.strategies.registry import (
    available_strategies,
    make_strategy,
)


def _obs(resource_level, n=4, capacity=100.0):
    return Observation(
        round_index=0,
        num_agents=n,
        capacity=capacity,
        resource_level=resource_level,
        own_last_harvest=0.0,
        own_total_payoff=0.0,
    )


def test_registry_contains_baselines():
    assert set(available_strategies()) >= {"selfish", "cooperative"}


def test_selfish_requests_equal_share_of_visible_stock():
    strat = make_strategy("selfish", {"greed": 1.0})
    request = strat.decide(_obs(80.0, n=4), np.random.default_rng(0))
    assert request == pytest.approx(20.0)  # 1.0 * 80 / 4


def test_selfish_falls_back_to_capacity_when_blind():
    strat = make_strategy("selfish", {"greed": 1.0})
    request = strat.decide(_obs(None, n=4, capacity=100.0), np.random.default_rng(0))
    assert request == pytest.approx(25.0)  # 1.0 * 100 / 4


def test_cooperative_requests_share_of_surplus_above_reference():
    strat = make_strategy("cooperative", {"regeneration_rate": 0.4, "capacity": 100.0})
    # target = 0.5 * 100 = 50; surplus at R=60 is 10; per agent (n=4) -> 2.5
    request = strat.decide(_obs(60.0, n=4), np.random.default_rng(0))
    assert request == pytest.approx(2.5)


def test_cooperative_harvests_nothing_below_reference_stock():
    strat = make_strategy("cooperative", {"capacity": 100.0})
    request = strat.decide(_obs(40.0, n=4), np.random.default_rng(0))
    assert request == 0.0


def test_cooperative_blind_fallback_claims_share_of_msy():
    strat = make_strategy("cooperative", {"regeneration_rate": 0.4, "capacity": 100.0})
    # MSY = g*K/4 = 10; per agent (n=8) -> 1.25
    request = strat.decide(_obs(None, n=8), np.random.default_rng(0))
    assert request == pytest.approx(1.25)


def test_cooperative_knowledge_bias_scales_blind_estimate():
    # Overconfident blind cooperator claims proportionally more than the true share.
    strat = make_strategy(
        "cooperative", {"regeneration_rate": 0.4, "capacity": 100.0, "knowledge_bias": 1.5}
    )
    request = strat.decide(_obs(None, n=8), np.random.default_rng(0))
    assert request == pytest.approx(1.5 * 1.25)


def test_cooperative_knowledge_bias_ignored_under_global_info():
    # With the stock observed, the self-correcting rule ignores knowledge_bias.
    accurate = make_strategy("cooperative", {"capacity": 100.0, "knowledge_bias": 1.0})
    biased = make_strategy("cooperative", {"capacity": 100.0, "knowledge_bias": 2.0})
    obs = _obs(60.0, n=4)
    rng = np.random.default_rng(0)
    assert accurate.decide(obs, rng) == biased.decide(obs, rng)


def test_cooperative_is_more_restrained_than_selfish_at_same_state():
    obs = _obs(60.0, n=4)
    selfish = make_strategy("selfish").decide(obs, np.random.default_rng(0))
    coop = make_strategy("cooperative", {"regeneration_rate": 0.4, "capacity": 100.0}).decide(
        obs, np.random.default_rng(0)
    )
    assert coop < selfish


def test_unknown_strategy_raises():
    with pytest.raises(KeyError):
        make_strategy("does_not_exist")
