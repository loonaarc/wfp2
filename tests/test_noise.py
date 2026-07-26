"""Tests for decision noise (the stochastic knob that makes seeds matter)."""

import pytest

from emergent_cooperation.core.config import (
    AgentSpec,
    ResourceConfig,
    SimulationConfig,
)
from emergent_cooperation.core.simulation import run_simulation


def _cfg(decision_noise, strategy="cooperative"):
    return SimulationConfig(
        name="noise",
        rounds=60,
        information_model="global",
        decision_noise=decision_noise,
        resource=ResourceConfig(initial_level=50.0, capacity=100.0, regeneration_rate=0.4),
        agents=(
            AgentSpec("cooperative", 4, {"capacity": 100.0}),
            AgentSpec("selfish", 4, {"greed": 1.0}),
        )
        if strategy == "mixed"
        else (AgentSpec(strategy, 8, {"capacity": 100.0}),),
    )


def test_zero_noise_is_deterministic_across_seeds_for_selfcorrecting_pop():
    # Without noise, the self-correcting cooperative population is seed-independent.
    a = run_simulation(_cfg(0.0), seed=1).total_payoffs()
    b = run_simulation(_cfg(0.0), seed=999).total_payoffs()
    assert a == b


def test_same_seed_reproducible_with_noise():
    a = run_simulation(_cfg(0.1, "mixed"), seed=7).total_payoffs()
    b = run_simulation(_cfg(0.1, "mixed"), seed=7).total_payoffs()
    assert a == b  # reproducible: identical (config, seed) -> identical run


def test_noise_makes_seeds_differ():
    a = run_simulation(_cfg(0.1, "mixed"), seed=1).total_payoffs()
    b = run_simulation(_cfg(0.1, "mixed"), seed=2).total_payoffs()
    assert a != b  # different seeds now produce different outcomes


def test_decision_noise_out_of_range_rejected():
    with pytest.raises(ValueError):
        SimulationConfig(decision_noise=1.0, agents=(AgentSpec("selfish", 1),))
    with pytest.raises(ValueError):
        SimulationConfig(decision_noise=-0.1, agents=(AgentSpec("selfish", 1),))


def test_harvest_stays_feasible_under_noise():
    result = run_simulation(_cfg(0.3, "mixed"), seed=3)
    for r in result.rounds:
        assert r.total_harvested <= r.resource_after_regen + 1e-9
