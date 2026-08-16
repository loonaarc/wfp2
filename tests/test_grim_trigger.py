"""Tests for the grim-trigger strategy (E21, ADR-0018).

Friedman (1971): cooperate as long as no deviation has ever been observed;
the instant one is, revert permanently to the one-shot (selfish) outcome --
no forgiveness, no return path. The single behavioural claim these tests
pin: `grim_trigger` never recovers from a triggered state, unlike
`conditional_cooperator`, which re-evaluates fresh every round.
"""

import numpy as np
import pytest

from emergent_cooperation.agents.observation import Observation
from emergent_cooperation.core.config import (
    AgentSpec,
    DisturbanceConfig,
    ResourceConfig,
    SimulationConfig,
)
from emergent_cooperation.core.simulation import run_simulation
from emergent_cooperation.strategies.conditional import ConditionalCooperatorStrategy
from emergent_cooperation.strategies.grim_trigger import GrimTriggerStrategy

RNG = np.random.default_rng(0)


def _obs(level: float, num_agents: int = 8) -> Observation:
    return Observation(
        round_index=0,
        num_agents=num_agents,
        capacity=100.0,
        resource_level=level,
        own_last_harvest=0.0,
        own_total_payoff=0.0,
    )


def test_cooperates_normally_while_nothing_has_ever_declined():
    strategy = GrimTriggerStrategy(regeneration_rate=0.4, capacity=100.0)
    # A steady, never-declining sequence at/above target -- should keep
    # taking only the surplus above K/2, same as plain cooperative.
    r1 = strategy.decide(_obs(60.0), RNG)
    r2 = strategy.decide(_obs(60.0), RNG)
    assert r1 == pytest.approx((60.0 - 50.0) / 8)
    assert r2 == pytest.approx((60.0 - 50.0) / 8)


def test_triggers_and_never_recovers_even_after_the_stock_rebounds():
    strategy = GrimTriggerStrategy(regeneration_rate=0.4, capacity=100.0)
    strategy.decide(_obs(60.0), RNG)  # baseline, no decline yet
    triggered_request = strategy.decide(_obs(40.0), RNG)  # a real decline -> triggers
    assert triggered_request == pytest.approx(40.0 / 8)  # selfish-sized share

    # Stock fully recovers past the old target on the next round --
    # conditional_cooperator would resume cooperating; grim_trigger must not.
    still_defecting = strategy.decide(_obs(90.0), RNG)
    assert still_defecting == pytest.approx(90.0 / 8)  # still a selfish share, not (90-50)/8

    # And forever after that, regardless of what the stock does.
    later = strategy.decide(_obs(55.0), RNG)
    assert later == pytest.approx(55.0 / 8)


def test_conditional_cooperator_forgives_the_same_scenario_grim_trigger_does_not():
    """Direct contrast, same input sequence, two different strategy instances."""
    cc = ConditionalCooperatorStrategy(regeneration_rate=0.4, capacity=100.0)
    gt = GrimTriggerStrategy(regeneration_rate=0.4, capacity=100.0)
    levels = [60.0, 40.0, 90.0]  # steady, decline (triggers both), full rebound
    cc_last, gt_last = None, None
    for level in levels:
        cc_last = cc.decide(_obs(level), RNG)
        gt_last = gt.decide(_obs(level), RNG)
    # Same final observation (90.0), same trigger history up to that point --
    # conditional_cooperator resumes cooperating (surplus rule); grim_trigger
    # stays locked into defection (selfish share).
    assert cc_last == pytest.approx((90.0 - 50.0) / 8)
    assert gt_last == pytest.approx(90.0 / 8)
    assert cc_last != gt_last


def test_one_sensitive_agent_diverges_after_a_recoverable_shock():
    """E21's own load-bearing empirical finding: with exactly one sensitive
    (decline-detecting) agent among 7 plain cooperative ones, a one-time
    recoverable shock lets conditional_cooperator forgive and return to the
    full K/2 target, while grim_trigger stays locked into defection forever
    -- a real, measurable welfare cost for refusing to forgive."""
    params = {"regeneration_rate": 0.4, "capacity": 100.0}

    def _run(kind):
        agents = (AgentSpec(kind, 1, params), AgentSpec("cooperative", 7, params))
        cfg = SimulationConfig(
            name=f"e21_{kind}",
            rounds=100,
            information_model="global",
            resource=ResourceConfig(initial_level=50.0, capacity=100.0, regeneration_rate=0.4),
            agents=agents,
            disturbances=(DisturbanceConfig(kind="resource_shock", round=30, magnitude=0.15),),
        )
        return run_simulation(cfg, seed=1)

    cc = _run("conditional_cooperator")
    gt = _run("grim_trigger")
    assert cc.rounds[-1].resource_after_harvest == pytest.approx(50.0)
    assert gt.rounds[-1].resource_after_harvest < 45.0  # stuck below target, never recovers
    assert sum(cc.total_payoffs()) > sum(gt.total_payoffs())


def test_grim_trigger_population_sustains_with_no_free_riders():
    """A population that never actually deviates should never trigger at all."""
    agents = [AgentSpec("grim_trigger", 8, {"regeneration_rate": 0.4, "capacity": 100.0})]
    cfg = SimulationConfig(
        name="grim_no_freeriders",
        rounds=100,
        information_model="global",
        resource=ResourceConfig(initial_level=50.0, capacity=100.0, regeneration_rate=0.4),
        agents=tuple(agents),
    )
    result = run_simulation(cfg, seed=1)
    assert not result.rounds[-1].collapsed
    assert result.rounds[-1].resource_after_harvest == pytest.approx(50.0)
