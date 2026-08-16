"""Tests for multiple resources / specialization (ADR-0016).

Two independent pools; every existing ``Strategy.decide()`` is reused
unchanged, called once per pool against that pool's own observation, and the
engine scales the two results by ``AgentSpec.allocation_split`` (fraction
routed to the first pool). ``allocation_split=1.0`` (the default) is a no-op
that reproduces today's single-pool behaviour exactly.
"""

import pytest

from emergent_cooperation.core.config import (
    AgentSpec,
    ReputationConfig,
    ResourceConfig,
    SimulationConfig,
)
from emergent_cooperation.core.simulation import run_simulation

POOL_A = ResourceConfig(
    initial_level=50.0, capacity=100.0, regeneration_rate=0.4, collapse_threshold=1.0
)
POOL_B = ResourceConfig(
    initial_level=50.0, capacity=100.0, regeneration_rate=0.2, collapse_threshold=1.0
)
COOP_PARAMS = {"regeneration_rate": 0.4, "capacity": 100.0}


def _sim(agents, second_resource=None, reputation=None, rounds=30):
    return SimulationConfig(
        name="multi_resource_test",
        rounds=rounds,
        information_model="global",
        resource=POOL_A,
        second_resource=second_resource,
        agents=tuple(agents),
        reputation=reputation,
    )


def test_allocation_split_must_be_in_unit_interval():
    AgentSpec("cooperative", 1, allocation_split=0.0)  # fine
    AgentSpec("cooperative", 1, allocation_split=1.0)  # fine
    with pytest.raises(ValueError):
        AgentSpec("cooperative", 1, allocation_split=1.5)
    with pytest.raises(ValueError):
        AgentSpec("cooperative", 1, allocation_split=-0.1)


def test_no_second_resource_is_byte_identical_to_before():
    """second_resource=None must reproduce single-pool behaviour exactly,
    regardless of what allocation_split says (it's meaningless without a
    second pool to route to)."""
    agents_default = [AgentSpec("cooperative", 8, COOP_PARAMS)]
    agents_explicit_split = [AgentSpec("cooperative", 8, COOP_PARAMS, allocation_split=0.3)]
    a = run_simulation(_sim(agents_default), seed=1)
    b = run_simulation(_sim(agents_explicit_split), seed=1)
    assert a.total_payoffs() == b.total_payoffs()
    levels_a = [r.resource_after_harvest for r in a.rounds]
    levels_b = [r.resource_after_harvest for r in b.rounds]
    assert levels_a == levels_b


def test_full_specialist_never_touches_the_second_pool():
    """allocation_split=1.0 (the default): every request goes to pool A, none to B."""
    agents = [AgentSpec("cooperative", 8, COOP_PARAMS, allocation_split=1.0)]
    result = run_simulation(_sim(agents, second_resource=POOL_B), seed=1)
    assert all(r == 0.0 for record in result.rounds for r in record.requested_b)
    # Pool B is never harvested, so it just grows toward capacity on its own.
    assert result.rounds[-1].resource_after_harvest_b > POOL_B.initial_level


def test_full_pool_b_specialist_never_touches_pool_a():
    """allocation_split=0.0: every request goes to pool B, none to A."""
    agents = [AgentSpec("cooperative", 8, COOP_PARAMS, allocation_split=0.0)]
    result = run_simulation(_sim(agents, second_resource=POOL_B), seed=1)
    # Every request is entirely in pool B; pool A's own requested total is 0.
    total_a_requests = sum(record.requested[i] for record in result.rounds for i in range(8)) - sum(
        record.requested_b[i] for record in result.rounds for i in range(8)
    )
    assert total_a_requests == pytest.approx(0.0, abs=1e-9)
    assert result.rounds[-1].resource_after_harvest > POOL_A.initial_level  # pool A ungrazed, grows


def test_generalist_draws_from_both_pools():
    agents = [AgentSpec("cooperative", 8, COOP_PARAMS, allocation_split=0.5)]
    result = run_simulation(_sim(agents, second_resource=POOL_B), seed=1)
    assert any(r.requested_b[0] > 0 for r in result.rounds)
    assert any((r.requested[0] - r.requested_b[0]) > 0 for r in result.rounds)


def test_pools_evolve_independently_given_different_regeneration_rates():
    """Pool A (g=0.4) and pool B (g=0.2) start identical but diverge, since an
    all-generalist population harvests proportionally to each pool's own
    surplus, which differs once growth rates differ."""
    agents = [AgentSpec("cooperative", 8, COOP_PARAMS, allocation_split=0.5)]
    result = run_simulation(_sim(agents, second_resource=POOL_B), seed=1)
    final = result.rounds[-1]
    assert final.resource_after_harvest != pytest.approx(final.resource_after_harvest_b, abs=0.5)


def test_sanctioning_pays_monitoring_cost_once_per_pool_it_enforces():
    """A sanctioner enforcing both pools pays its monitoring_cost twice per
    round (ADR-0016's deliberate "watching two resources costs more" choice)
    -- verified by comparing net payoff loss vs. the single-pool case."""
    sanction_params = {"regeneration_rate": 0.4, "capacity": 100.0, "monitoring_cost": 0.2}
    agents_single = [AgentSpec("sanctioning", 1, sanction_params, allocation_split=0.5)]
    agents_double = [AgentSpec("sanctioning", 1, sanction_params, allocation_split=0.5)]
    single = run_simulation(_sim(agents_single, second_resource=None, rounds=10), seed=1)
    double = run_simulation(_sim(agents_double, second_resource=POOL_B, rounds=10), seed=1)
    # Single pool: 1 agent, alone, harvests everything with no cap ever binding
    # (n_governed=1) -- cost is still charged every round regardless of cap.
    single_cost = 10 * sanction_params["monitoring_cost"]
    double_cost = 2 * 10 * sanction_params["monitoring_cost"]
    assert double.rounds[0].penalties[0] == pytest.approx(2 * single.rounds[0].penalties[0])
    assert double_cost == pytest.approx(2 * single_cost)


def test_specialist_monitor_only_enforces_and_pays_for_its_own_pool():
    """A pure pool-A specialist monitor (allocation_split=1.0) never enforces,
    or pays to enforce, pool B -- and vice versa. Without this, a specialist
    would be charged for "watching" a resource it never even looks at, which
    would undermine any specialized-vs-generalist-monitor comparison (E20)."""
    sanction_params = {"regeneration_rate": 0.4, "capacity": 100.0, "monitoring_cost": 0.2}
    pool_a_only = [AgentSpec("sanctioning", 1, sanction_params, allocation_split=1.0)]
    pool_b_only = [AgentSpec("sanctioning", 1, sanction_params, allocation_split=0.0)]
    generalist = [AgentSpec("sanctioning", 1, sanction_params, allocation_split=0.5)]

    a_only = run_simulation(_sim(pool_a_only, second_resource=POOL_B, rounds=5), seed=1)
    b_only = run_simulation(_sim(pool_b_only, second_resource=POOL_B, rounds=5), seed=1)
    both = run_simulation(_sim(generalist, second_resource=POOL_B, rounds=5), seed=1)

    assert a_only.rounds[0].penalties[0] == pytest.approx(sanction_params["monitoring_cost"])
    assert b_only.rounds[0].penalties[0] == pytest.approx(sanction_params["monitoring_cost"])
    assert both.rounds[0].penalties[0] == pytest.approx(2 * sanction_params["monitoring_cost"])


def test_sanctioning_quota_uses_each_pools_own_growth_rate():
    """A sanctioning agent's enforced quota on pool B must come from pool B's
    own sustainable yield (g_B*K/4 = 5), not pool A's reused wholesale
    (g_A*K/4 = 10) -- a bug caught after the fact: pool B's strategy copy
    was originally built from pool A's params, and _enforce() originally
    always asked the pool-A strategy instance for its policy regardless of
    which pool it was enforcing. Both are fixed now; this pins the fix."""
    sanction_params = {"regeneration_rate": 0.4, "capacity": 100.0, "monitoring_cost": 0.2}
    agents = [
        AgentSpec("sanctioning", 4, sanction_params, allocation_split=0.5),
        AgentSpec("selfish", 4, {"greed": 1.0}, allocation_split=0.5),
    ]
    result = run_simulation(_sim(agents, second_resource=POOL_B, rounds=1), seed=1)
    record = result.rounds[0]
    n_governed = 8
    quota_b = (POOL_B.regeneration_rate * POOL_B.capacity / 4.0) / n_governed
    wrong_quota_a = (POOL_A.regeneration_rate * POOL_A.capacity / 4.0) / n_governed
    selfish_harvest_b = record.harvested_b[4]  # a selfish agent's own pool-B harvest
    assert selfish_harvest_b == pytest.approx(quota_b, abs=1e-6)
    assert selfish_harvest_b < wrong_quota_a


def test_reputation_fair_share_sums_both_pools_when_combined():
    """With a second pool, an agent legitimately splitting a fair share across
    both pools should not be scored as if only pool A's fair share applied."""
    agents = [
        AgentSpec("reputation_cooperator", 8, COOP_PARAMS, allocation_split=0.5),
    ]
    rep = ReputationConfig(visibility=1.0)
    result = run_simulation(
        _sim(agents, second_resource=POOL_B, reputation=rep, rounds=10),
        seed=1,
    )
    # A well-behaved generalist population should mostly earn positive reputation,
    # not be punished purely for existing under two pools.
    last = result.rounds[-1].reputations
    assert sum(1 for r in last if r > 0) >= 6


def test_stateful_strategies_track_each_pool_independently():
    """conditional_cooperator/compensating_cooperator keep their own
    per-instance "did the stock I'm watching decline" state
    (``_last_level``). Calling the *same* strategy instance once per pool
    per round would have that state alternate between two unrelated pools'
    levels, corrupting the comparison for both (see ADR-0016). The engine
    must give pool B its own, separate strategy instance per agent."""
    from emergent_cooperation.core.simulation import Simulation

    agents = [AgentSpec("conditional_cooperator", 1, COOP_PARAMS, allocation_split=0.5)]
    sim = Simulation(_sim(agents, second_resource=POOL_B, rounds=3), seed=1)
    record = sim.step(0)
    assert sim.agents[0].strategy is not sim._strategy_b[0]
    # _last_level is set from what was *observed* (post-regen, pre-harvest),
    # not the pool's current (post-harvest) level.
    assert sim.agents[0].strategy._last_level == pytest.approx(record.resource_after_regen)
    assert sim._strategy_b[0]._last_level == pytest.approx(record.resource_after_regen_b)


def test_deterministic_for_same_seed():
    agents = [
        AgentSpec("cooperative", 4, COOP_PARAMS, allocation_split=0.7),
        AgentSpec("selfish", 4, {"greed": 1.0}, allocation_split=0.3),
    ]
    cfg = _sim(agents, second_resource=POOL_B)
    a = run_simulation(cfg, seed=4)
    b = run_simulation(cfg, seed=4)
    assert a.total_payoffs() == b.total_payoffs()
    levels_b_a = [r.resource_after_harvest_b for r in a.rounds]
    levels_b_b = [r.resource_after_harvest_b for r in b.rounds]
    assert levels_b_a == levels_b_b
