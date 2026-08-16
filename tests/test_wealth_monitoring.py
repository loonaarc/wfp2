"""Tests for wealth-triggered ad-hoc voluntary monitoring (E22, ADR-0020).

Olson (1965): a group member has an individual incentive to unilaterally
provide a collective good exactly when its own share of the benefit clears
the good's cost relative to its total value (F_i > C/V_g). Here, an agent's
own accumulated total_payoff, relative to the population's current average,
operationalizes F_i: the single wealthiest eligible agent volunteers as
monitor each round, re-evaluated fresh every round.
"""

import pytest

from emergent_cooperation.core.config import (
    AgentSpec,
    ResourceConfig,
    SimulationConfig,
    WealthMonitoringConfig,
)
from emergent_cooperation.core.simulation import run_simulation

COOP_PARAMS = {"regeneration_rate": 0.4, "capacity": 100.0}
SELFISH_PARAMS = {"greed": 1.0}
SANCTION_PARAMS = {"regeneration_rate": 0.4, "capacity": 100.0, "monitoring_cost": 0.2}


def _resource() -> ResourceConfig:
    return ResourceConfig(
        initial_level=50.0, capacity=100.0, regeneration_rate=0.4, collapse_threshold=1.0
    )


def test_none_is_byte_identical_to_no_wealth_monitoring():
    agents = (AgentSpec("cooperative", 8, COOP_PARAMS),)
    cfg_off = SimulationConfig(
        name="off", rounds=50, decision_noise=0.2, resource=_resource(), agents=agents
    )
    cfg_none = SimulationConfig(
        name="none", rounds=50, decision_noise=0.2, resource=_resource(),
        agents=agents, wealth_monitoring=None,
    )
    a = run_simulation(cfg_off, seed=1)
    b = run_simulation(cfg_none, seed=1)
    assert a.total_payoffs() == b.total_payoffs()


def test_threshold_and_cost_must_be_non_negative():
    with pytest.raises(ValueError):
        WealthMonitoringConfig(threshold=-0.1)
    with pytest.raises(ValueError):
        WealthMonitoringConfig(threshold=1.1, monitoring_cost=-0.1)


def test_round_zero_never_triggers_a_volunteer():
    """Everyone starts at total_payoff=0, exactly the round-0 average -- the
    strict '>' comparison must never trigger before any wealth has diverged,
    even with the most permissive threshold."""
    agents = (AgentSpec("cooperative", 8, COOP_PARAMS),)
    cfg = SimulationConfig(
        name="r0", rounds=1, resource=_resource(), agents=agents,
        wealth_monitoring=WealthMonitoringConfig(threshold=0.0, monitoring_cost=0.2),
    )
    result = run_simulation(cfg, seed=1)
    assert sum(result.rounds[0].penalties) == pytest.approx(0.0)


def test_selfish_agents_are_never_eligible_even_when_wealthiest():
    """A selfish agent massively out-earns cooperators here (the standard
    tragedy-of-the-commons pattern since E2) -- easily clearing any wealth
    threshold -- but must never be charged a wealth-triggered monitoring
    cost: enforcement would cap its own over-extraction too, a pure loss no
    rational free-rider would choose, and outside what Olson's F_i (a share
    of a good the volunteer actually values) is about."""
    agents = (AgentSpec("cooperative", 7, COOP_PARAMS), AgentSpec("selfish", 1, SELFISH_PARAMS))
    cfg = SimulationConfig(
        name="q-selfish", rounds=60, resource=_resource(), agents=agents,
        wealth_monitoring=WealthMonitoringConfig(threshold=1.02, monitoring_cost=0.2),
    )
    result = run_simulation(cfg, seed=1)
    selfish_index = 7
    assert all(r.penalties[selfish_index] == pytest.approx(0.0) for r in result.rounds)


def test_at_most_one_agent_is_charged_a_wealth_triggered_penalty_per_round():
    """No designated sanctioning agent exists in this composition, so any
    nonzero penalty in a round can only come from the wealth trigger --
    exactly one, matching the 'single wealthiest volunteer' rule (this
    engine's existing 'any one monitor enforces fully' simplification)."""
    agents = (AgentSpec("cooperative", 8, COOP_PARAMS),)
    cfg = SimulationConfig(
        name="single-volunteer", rounds=100, decision_noise=0.2, resource=_resource(),
        agents=agents,
        wealth_monitoring=WealthMonitoringConfig(threshold=1.02, monitoring_cost=0.2),
    )
    result = run_simulation(cfg, seed=1)
    triggered_rounds = 0
    for r in result.rounds:
        charged = [p for p in r.penalties if p > 0]
        assert len(charged) <= 1
        if charged:
            triggered_rounds += 1
    # The mechanism must actually fire at least once for this test to mean
    # anything -- decision_noise=0.2 over 100 rounds reliably diverges wealth
    # enough to clear a 1.02x threshold.
    assert triggered_rounds > 0


def test_designated_sanctioning_agent_is_never_double_charged():
    """A sanctioning agent that is also the wealthiest keeps paying its own
    monitoring_cost -- the wealth trigger must not layer a second, different
    cost on top of an agent that already has an intrinsic policy."""
    agents = (
        AgentSpec("sanctioning", 1, SANCTION_PARAMS),
        AgentSpec("cooperative", 6, COOP_PARAMS),
        AgentSpec("selfish", 1, SELFISH_PARAMS),
    )
    cfg = SimulationConfig(
        name="no-double-charge", rounds=60, resource=_resource(), agents=agents,
        wealth_monitoring=WealthMonitoringConfig(threshold=1.02, monitoring_cost=0.9),
    )
    result = run_simulation(cfg, seed=1)
    sanctioner_index = 0
    for r in result.rounds:
        # Only ever 0.2 (its own SANCTION_PARAMS cost) or 0.0, never 0.9 (the
        # wealth_monitoring config's own, different, monitoring_cost).
        assert r.penalties[sanctioner_index] in (pytest.approx(0.0), pytest.approx(0.2))


def test_a_dominant_freerider_inflates_the_average_and_suppresses_the_trigger():
    """Q1 finding, caught here before the experiment script was written (the
    same 'verify before reporting' discipline as ADR-0017/0019): a free-rider
    consistently out-earns cooperators in this project's well-mixed pool
    (E2's own finding), which inflates the *population average* so far above
    any single cooperator's own wealth that no cooperator ever clears even a
    barely-above-average threshold -- the mechanism never engages at all with
    a free-rider present, mirroring E23's own free-rider-dominance problem
    from the opposite direction (there it broke a wealth *floor*; here it
    starves a wealth *trigger*)."""
    agents = (AgentSpec("cooperative", 7, COOP_PARAMS), AgentSpec("selfish", 1, SELFISH_PARAMS))
    cfg = SimulationConfig(
        name="q1-suppressed", rounds=100, decision_noise=0.2, resource=_resource(),
        agents=agents,
        wealth_monitoring=WealthMonitoringConfig(threshold=1.02, monitoring_cost=0.2),
    )
    result = run_simulation(cfg, seed=1)
    assert sum(sum(r.penalties) for r in result.rounds) == pytest.approx(0.0)


def test_wealth_triggered_monitoring_engages_without_a_freerider_present():
    """Contrast case: with no free-rider to inflate the average, the same
    threshold that never engages in the presence-of-a-freerider test above
    reliably engages here, purely from decision_noise-induced divergence
    among agents that all value the same collective good."""
    agents = (AgentSpec("cooperative", 8, COOP_PARAMS),)
    cfg = SimulationConfig(
        name="q1-engaged", rounds=100, decision_noise=0.2, resource=_resource(),
        agents=agents,
        wealth_monitoring=WealthMonitoringConfig(threshold=1.02, monitoring_cost=0.2),
    )
    result = run_simulation(cfg, seed=1)
    assert sum(sum(r.penalties) for r in result.rounds) > 0.0
