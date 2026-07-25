"""Tests for the conditional cooperator (reciprocity) strategy."""

import numpy as np

from emergent_cooperation.agents.observation import Observation
from emergent_cooperation.core.config import AgentSpec, ResourceConfig, SimulationConfig
from emergent_cooperation.core.simulation import run_simulation
from emergent_cooperation.strategies.registry import available_strategies, make_strategy


def _obs(level, n=8, capacity=100.0):
    return Observation(
        round_index=0,
        num_agents=n,
        capacity=capacity,
        resource_level=level,
        own_last_harvest=0.0,
        own_total_payoff=0.0,
    )


def test_registered():
    assert "conditional_cooperator" in available_strategies()


def test_cooperates_then_retaliates_on_decline_then_cooperates_again():
    strat = make_strategy("conditional_cooperator", {"capacity": 100.0})
    rng = np.random.default_rng(0)
    # Round 0: no history -> cooperate -> surplus (60-50)/8 = 1.25.
    assert strat.decide(_obs(60.0, n=8), rng) == 1.25
    # Round 1: stock fell 60 -> 55 -> defect -> selfish share 1.0*55/8 = 6.875.
    assert strat.decide(_obs(55.0, n=8), rng) == 6.875
    # Round 2: stock rose 55 -> 57 -> cooperate again -> (57-50)/8 = 0.875.
    assert strat.decide(_obs(57.0, n=8), rng) == 0.875


def test_blind_fallback_is_cooperative_restraint():
    strat = make_strategy("conditional_cooperator", {"regeneration_rate": 0.4, "capacity": 100.0})
    # Private info (level None): MSY share = g*K/4/n = 10/8 = 1.25.
    assert strat.decide(_obs(None, n=8), np.random.default_rng(0)) == 1.25


def test_all_conditional_population_sustains_like_cooperators():
    cfg = SimulationConfig(
        name="all_conditional",
        rounds=100,
        information_model="global",
        resource=ResourceConfig(initial_level=50.0, capacity=100.0, regeneration_rate=0.4),
        agents=(AgentSpec("conditional_cooperator", count=8, params={"capacity": 100.0}),),
    )
    result = run_simulation(cfg, seed=1)
    # No one over-extracts, so no decline is ever detected -> stable cooperation.
    assert not result.rounds[-1].collapsed
    assert result.final_resource_level > 10.0


def test_state_does_not_leak_between_runs():
    cfg = SimulationConfig(
        name="c",
        rounds=30,
        information_model="global",
        resource=ResourceConfig(initial_level=50.0, capacity=100.0, regeneration_rate=0.4),
        agents=(AgentSpec("conditional_cooperator", count=4, params={"capacity": 100.0}),),
    )
    a = run_simulation(cfg, seed=1).total_payoffs()
    b = run_simulation(cfg, seed=1).total_payoffs()
    assert a == b  # fresh strategy state each run -> identical, reproducible
