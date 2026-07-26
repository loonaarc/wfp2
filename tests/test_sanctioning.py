"""Tests for the sanctioning strategy and the engine enforcement phase."""

import pytest

from emergent_cooperation.core.config import AgentSpec, ResourceConfig, SimulationConfig
from emergent_cooperation.core.simulation import run_simulation
from emergent_cooperation.strategies.registry import available_strategies, make_strategy


def _sim(agents, rounds=100):
    return SimulationConfig(
        name="sanction_test",
        rounds=rounds,
        information_model="global",
        resource=ResourceConfig(initial_level=50.0, capacity=100.0, regeneration_rate=0.4),
        agents=tuple(agents),
    )


def _payoff_by_strategy(result):
    from collections import defaultdict

    sums = defaultdict(list)
    for strat, payoff in zip(result.agent_strategies, result.total_payoffs(), strict=True):
        sums[strat].append(payoff)
    return {s: sum(v) / len(v) for s, v in sums.items()}


def test_registered():
    assert "sanctioning" in available_strategies()


def test_only_sanctioning_exposes_a_policy():
    assert make_strategy("cooperative", {"capacity": 100.0}).sanction_policy() is None
    assert make_strategy("selfish").sanction_policy() is None
    policy = make_strategy(
        "sanctioning", {"regeneration_rate": 0.4, "capacity": 100.0}
    ).sanction_policy()
    assert policy is not None
    assert policy.quota_total == pytest.approx(10.0)  # MSY = g*K/4


def test_enforcement_protects_resource_against_selfish_agents():
    # 4 selfish agents collapse the pool with plain cooperators (see E2); with
    # sanctioners present the pool is protected.
    result = run_simulation(
        _sim(
            [
                AgentSpec("sanctioning", 4, {"regeneration_rate": 0.4, "capacity": 100.0}),
                AgentSpec("selfish", 4, {"greed": 1.0}),
            ]
        ),
        seed=1,
    )
    assert not result.rounds[-1].collapsed
    assert result.final_resource_level > 10.0


def test_monitoring_cost_reduces_sanctioner_payoff():
    # 8 sanctioners, cost 0.2/round, 100 rounds: net payoff = 125 - 20 = 105.
    result = run_simulation(
        _sim(
            [
                AgentSpec(
                    "sanctioning",
                    8,
                    {"regeneration_rate": 0.4, "capacity": 100.0, "monitoring_cost": 0.2},
                )
            ]
        ),
        seed=1,
    )
    payoff = _payoff_by_strategy(result)["sanctioning"]
    assert payoff == pytest.approx(105.0, abs=1e-6)
    total_penalty = sum(r.total_penalty for r in result.rounds)
    assert total_penalty == pytest.approx(8 * 0.2 * 100)


def test_second_order_free_rider_cooperators_out_earn_sanctioners():
    # Plain cooperators enjoy the enforced protection without paying to monitor,
    # so they out-earn the sanctioners who do.
    result = run_simulation(
        _sim(
            [
                AgentSpec(
                    "sanctioning",
                    3,
                    {"regeneration_rate": 0.4, "capacity": 100.0, "monitoring_cost": 0.2},
                ),
                AgentSpec("cooperative", 4, {"capacity": 100.0}),
                AgentSpec("selfish", 1, {"greed": 1.0}),
            ]
        ),
        seed=1,
    )
    payoffs = _payoff_by_strategy(result)
    assert not result.rounds[-1].collapsed
    assert payoffs["cooperative"] > payoffs["sanctioning"]


def test_no_sanctioner_leaves_dynamics_unchanged():
    # Without a sanctioner the enforcement phase is a no-op: all-selfish still collapses.
    result = run_simulation(_sim([AgentSpec("selfish", 8, {"greed": 1.0})]), seed=1)
    assert result.rounds[-1].collapsed
    assert all(r.total_penalty == 0.0 for r in result.rounds)
