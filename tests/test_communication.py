"""Tests for the broadcast communication signal (ADR-0007)."""

import numpy as np
import pytest

from emergent_cooperation.agents.observation import Observation
from emergent_cooperation.core.config import AgentSpec, ResourceConfig, SimulationConfig
from emergent_cooperation.core.simulation import run_simulation
from emergent_cooperation.metrics.metrics import gini
from emergent_cooperation.strategies.registry import make_strategy


def _mixed(broadcast_reliability, information_model="private"):
    return SimulationConfig(
        name="comm",
        rounds=100,
        information_model=information_model,
        broadcast_reliability=broadcast_reliability,
        resource=ResourceConfig(initial_level=50.0, capacity=100.0, regeneration_rate=0.4),
        agents=(
            AgentSpec("conditional_cooperator", 6, {"capacity": 100.0}),
            AgentSpec("selfish", 2, {"greed": 1.0}),
        ),
    )


def test_broadcast_reliability_validated():
    with pytest.raises(ValueError):
        SimulationConfig(broadcast_reliability=1.5, agents=(AgentSpec("selfish", 1),))
    with pytest.raises(ValueError):
        SimulationConfig(broadcast_reliability=-0.1, agents=(AgentSpec("selfish", 1),))


def test_no_communication_is_backward_compatible():
    # broadcast_reliability=0 must reproduce the pre-communication behaviour exactly.
    a = run_simulation(_mixed(0.0), seed=1).total_payoffs()
    b = run_simulation(_mixed(0.0), seed=1).total_payoffs()
    assert a == b


def test_communication_reduces_exploitation_under_private_info():
    # Blind conditional cooperators are heavily exploited; a reliable broadcast lets
    # them detect over-extraction, lowering payoff inequality.
    without = gini(run_simulation(_mixed(0.0), seed=1).total_payoffs())
    with_comms = gini(run_simulation(_mixed(1.0), seed=1).total_payoffs())
    assert with_comms < without


def test_conditional_cooperator_reciprocates_on_communicated_over_extraction():
    strat = make_strategy("conditional_cooperator", {"regeneration_rate": 0.4, "capacity": 100.0})
    rng = np.random.default_rng(0)
    # MSY = 10. A signal above MSY (blind, no stock) -> defect (selfish share of K).
    over = Observation(
        round_index=1,
        num_agents=8,
        capacity=100.0,
        resource_level=None,
        own_last_harvest=0.0,
        own_total_payoff=0.0,
        signal=40.0,
    )
    assert strat.decide(over, rng) == pytest.approx(1.0 * 100.0 / 8)  # defection_greed*K/n
    # A sustainable signal -> cooperate (MSY share).
    ok = Observation(
        round_index=1,
        num_agents=8,
        capacity=100.0,
        resource_level=None,
        own_last_harvest=0.0,
        own_total_payoff=0.0,
        signal=8.0,
    )
    assert strat.decide(ok, rng) == pytest.approx(10.0 / 8)


def test_reproducible_with_communication():
    a = run_simulation(_mixed(0.5), seed=3).total_payoffs()
    b = run_simulation(_mixed(0.5), seed=3).total_payoffs()
    assert a == b
