"""Tests for the loner (opt-out) strategy."""

import numpy as np
import pytest

from emergent_cooperation.agents.observation import Observation
from emergent_cooperation.strategies.registry import available_strategies, make_strategy


def _obs(resource_level, n=4, capacity=100.0):
    return Observation(
        round_index=0,
        num_agents=n,
        capacity=capacity,
        resource_level=resource_level,
        own_last_harvest=0.0,
        own_total_payoff=0.0,
    )


def test_registry_contains_loner():
    assert "loner" in available_strategies()


@pytest.mark.parametrize("resource_level", [0.0, 25.0, 100.0, None])
def test_loner_always_requests_nothing(resource_level):
    strat = make_strategy("loner")
    request = strat.decide(_obs(resource_level), np.random.default_rng(0))
    assert request == 0.0


def test_loner_has_no_sanction_policy():
    strat = make_strategy("loner")
    assert strat.sanction_policy() is None
