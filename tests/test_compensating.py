"""Tests for the compensating cooperator (restraint response to over-extraction)."""

import numpy as np
import pytest

from emergent_cooperation.agents.observation import Observation
from emergent_cooperation.core.config import AgentSpec, ResourceConfig, SimulationConfig
from emergent_cooperation.core.simulation import run_simulation
from emergent_cooperation.strategies.registry import available_strategies, make_strategy


def _obs(level, signal=None, n=8):
    return Observation(
        round_index=1,
        num_agents=n,
        capacity=100.0,
        resource_level=level,
        own_last_harvest=0.0,
        own_total_payoff=0.0,
        signal=signal,
    )


def test_registered():
    assert "compensating_cooperator" in available_strategies()


def test_withholds_on_communicated_over_extraction():
    strat = make_strategy("compensating_cooperator", {"regeneration_rate": 0.4, "capacity": 100.0})
    rng = np.random.default_rng(0)
    # Blind (no stock) + signal above MSY (10) -> withhold entirely.
    assert strat.decide(_obs(None, signal=40.0), rng) == 0.0
    # Sustainable signal -> cooperate (MSY share = 10/8).
    assert strat.decide(_obs(None, signal=8.0), rng) == pytest.approx(10.0 / 8)


def test_withholds_when_observed_stock_declines():
    strat = make_strategy("compensating_cooperator", {"capacity": 100.0})
    rng = np.random.default_rng(0)
    strat.decide(_obs(60.0), rng)  # establish reference
    assert strat.decide(_obs(55.0), rng) == 0.0  # declined -> withhold


def test_all_compensating_population_sustains():
    cfg = SimulationConfig(
        name="all_comp",
        rounds=100,
        information_model="global",
        resource=ResourceConfig(initial_level=50.0, capacity=100.0, regeneration_rate=0.4),
        agents=(AgentSpec("compensating_cooperator", 8, {"capacity": 100.0}),),
    )
    result = run_simulation(cfg, seed=1)
    assert not result.rounds[-1].collapsed
