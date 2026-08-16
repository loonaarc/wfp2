"""Tests for the wealth-based participation floor (E23, ADR-0019).

Chen & Szolnoki (2016): gating participation on accumulated wealth
self-corrects against defectors on a spatial lattice, because sustained
defection erodes a defector's own local resource base. These tests pin
what actually happens in this project's well-mixed, single-shared-pool
engine instead: the gate excludes the exploited majority (or the monitors),
not the free-rider -- a real, mechanistically-explained non-transfer, not a
bug.
"""

import pytest

from emergent_cooperation.core.config import AgentSpec, ResourceConfig, SimulationConfig
from emergent_cooperation.core.simulation import run_simulation

COOP_PARAMS = {"regeneration_rate": 0.4, "capacity": 100.0}
SELFISH_PARAMS = {"greed": 1.0}
SANCTION_PARAMS = {"regeneration_rate": 0.4, "capacity": 100.0, "monitoring_cost": 0.2}


def _resource() -> ResourceConfig:
    return ResourceConfig(
        initial_level=50.0, capacity=100.0, regeneration_rate=0.4, collapse_threshold=1.0
    )


def test_none_is_byte_identical_to_no_wealth_gate():
    agents = (AgentSpec("cooperative", 6, COOP_PARAMS), AgentSpec("selfish", 2, SELFISH_PARAMS))
    cfg_off = SimulationConfig(
        name="off", rounds=50, information_model="global", resource=_resource(), agents=agents
    )
    cfg_none = SimulationConfig(
        name="none", rounds=50, information_model="global", resource=_resource(),
        agents=agents, wealth_floor_fraction=None,
    )
    a = run_simulation(cfg_off, seed=1)
    b = run_simulation(cfg_none, seed=1)
    assert a.total_payoffs() == b.total_payoffs()


def test_wealth_floor_fraction_must_be_non_negative():
    with pytest.raises(ValueError):
        SimulationConfig(
            name="bad", rounds=10, resource=_resource(),
            agents=(AgentSpec("cooperative", 8, COOP_PARAMS),), wealth_floor_fraction=-0.1,
        )


def test_round_zero_never_excludes_anyone():
    """Everyone starts at total_payoff=0, exactly the round-0 average -- the
    strict '<' comparison must never exclude anyone before any wealth has
    had a chance to diverge."""
    agents = (AgentSpec("cooperative", 6, COOP_PARAMS), AgentSpec("selfish", 2, SELFISH_PARAMS))
    cfg = SimulationConfig(
        name="r0", rounds=1, information_model="global", resource=_resource(),
        agents=agents, wealth_floor_fraction=0.99,
    )
    result = run_simulation(cfg, seed=1)
    assert sum(result.rounds[0].requested) > 0


def test_wealth_gate_excludes_the_exploited_majority_not_the_freerider():
    """E23's own Q1 finding: in a well-mixed shared pool, a free-rider's
    request scales with the *global* level, not a personal local
    neighbourhood it exhausts -- so it consistently out-earns cooperators,
    and a 'below-average wealth' gate ends up excluding the cooperative
    majority instead, hurting welfare rather than protecting the pool."""
    agents = (AgentSpec("cooperative", 7, COOP_PARAMS), AgentSpec("selfish", 1, SELFISH_PARAMS))

    def _run(wealth_floor):
        cfg = SimulationConfig(
            name="q1", rounds=100, information_model="global", resource=_resource(),
            agents=agents, wealth_floor_fraction=wealth_floor,
        )
        return run_simulation(cfg, seed=1)

    baseline = _run(None)
    gated = _run(0.9)
    # The free-rider (last agent) is never excluded -- it stays far above
    # the population average throughout.
    assert gated.rounds[-1].requested[-1] > 0
    # Net welfare is *worse* with the gate on, not better.
    assert sum(gated.total_payoffs()) < sum(baseline.total_payoffs())


def test_wealth_gate_excludes_monitors_once_sanctioning_is_present():
    """E23's own Q2 finding: with sanctioning present, the quota already
    equalizes harvest across non-monitor agents -- the wealth gap that
    remains is between monitors (who pay monitoring_cost, and can end up
    with *negative* net payoff) and everyone else. The gate then excludes
    the monitors, removing enforcement precisely because enforcing was
    costly."""
    agents = (
        AgentSpec("sanctioning", 2, SANCTION_PARAMS),
        AgentSpec("cooperative", 4, COOP_PARAMS),
        AgentSpec("selfish", 2, SELFISH_PARAMS),
    )
    cfg = SimulationConfig(
        name="q2", rounds=100, information_model="global", resource=_resource(),
        agents=agents, wealth_floor_fraction=0.9,
    )
    result = run_simulation(cfg, seed=1)
    final = result.rounds[-1]
    # The two sanctioning agents (indices 0, 1) end up net-negative --
    # poorer than the population's own average -- and stop requesting.
    payoffs = [sum(r.requested[i] - r.penalties[i] for r in result.rounds) for i in range(8)]
    assert payoffs[0] < 0 and payoffs[1] < 0
    assert final.requested[0] == pytest.approx(0.0)
    assert final.requested[1] == pytest.approx(0.0)
