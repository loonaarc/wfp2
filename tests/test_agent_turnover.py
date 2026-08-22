"""Tests for the agent-turnover disturbance (E24, ADR-0021).

Duffy & Lafky (2015): replacing a fixed cohort with staggered overlapping-
generations turnover flattens the usual decay of public-goods contributions.
This project's fixed strategies don't decay from experience, except for the
one strategy with genuine per-round memory of a permanent decline:
`grim_trigger` (E21) never forgives on its own. These tests pin (a) that
turnover is a verified no-op wherever there's no memory to reset, and (b)
that it can recover a triggered `grim_trigger` population where nothing else
in this engine could -- E21's own "no return path" finding, revisited.
"""

import pytest

from emergent_cooperation.core.config import (
    AgentSpec,
    DisturbanceConfig,
    ResourceConfig,
    SimulationConfig,
)
from emergent_cooperation.core.simulation import run_simulation
from emergent_cooperation.disturbances import AgentTurnover
from emergent_cooperation.strategies.conditional import ConditionalCooperatorStrategy
from emergent_cooperation.strategies.grim_trigger import GrimTriggerStrategy

COOP_PARAMS = {"regeneration_rate": 0.4, "capacity": 100.0}
SELFISH_PARAMS = {"greed": 1.0}


def _resource() -> ResourceConfig:
    return ResourceConfig(
        initial_level=50.0, capacity=100.0, regeneration_rate=0.4, collapse_threshold=1.0
    )


# --- config validation -----------------------------------------------------


def test_agent_turnover_kind_validates_magnitude():
    with pytest.raises(ValueError, match="magnitude"):
        DisturbanceConfig(kind="agent_turnover", round=5, magnitude=1.5)


# --- reset_state() on the strategies themselves -----------------------------


def test_grim_trigger_reset_state_clears_the_permanent_lock():
    strat = GrimTriggerStrategy(**COOP_PARAMS)
    strat._last_level = 40.0
    strat._triggered = True
    strat.reset_state()
    assert strat._last_level is None
    assert strat._triggered is False


def test_conditional_cooperator_reset_state_clears_last_level():
    strat = ConditionalCooperatorStrategy(**COOP_PARAMS)
    strat._last_level = 40.0
    strat.reset_state()
    assert strat._last_level is None


def test_base_strategy_reset_state_is_a_harmless_default():
    from emergent_cooperation.strategies.cooperative import CooperativeStrategy

    strat = CooperativeStrategy(**COOP_PARAMS)
    strat.reset_state()  # must not raise, even though there's nothing to reset


# --- the AgentTurnover disturbance mechanism --------------------------------


def test_agent_turnover_resets_a_rotating_window_of_active_agents():
    turnover = AgentTurnover(round=3, fraction=0.25)
    agents = []
    for _ in range(8):
        strat = GrimTriggerStrategy(**COOP_PARAMS)
        strat._triggered = True
        agents.append(type("A", (), {"strategy": strat, "active": True, "reputation": 5.0})())
    assert turnover.apply(2, None, agents) is False  # not its round
    assert all(a.strategy._triggered for a in agents)
    assert turnover.apply(3, None, agents) is True
    # round_index=3, n=8 -> offset=3, to_reset=round(0.25*8)=2 -> indices 3,4
    reset_flags = [not a.strategy._triggered for a in agents]
    assert reset_flags == [False, False, False, True, True, False, False, False]
    assert agents[3].reputation == 0 and agents[4].reputation == 0


def test_agent_turnover_skips_inactive_agents():
    turnover = AgentTurnover(round=0, fraction=1.0)
    strat = GrimTriggerStrategy(**COOP_PARAMS)
    strat._triggered = True
    agent = type("A", (), {"strategy": strat, "active": False, "reputation": 1.0})()
    turnover.apply(0, None, [agent])
    assert agent.strategy._triggered is True  # inactive agent left untouched


# --- verified no-op where there's nothing to reset --------------------------


def test_turnover_is_a_byte_for_byte_noop_with_no_stateful_strategies():
    agents = (AgentSpec("cooperative", 6, COOP_PARAMS), AgentSpec("selfish", 2, SELFISH_PARAMS))

    def _run(turnover: bool):
        disturbances = (
            tuple(
                DisturbanceConfig(kind="agent_turnover", round=r, magnitude=0.5)
                for r in range(10, 90, 7)
            )
            if turnover
            else ()
        )
        cfg = SimulationConfig(
            name="noop", rounds=100, information_model="global", resource=_resource(),
            agents=agents, disturbances=disturbances,
        )
        return run_simulation(cfg, seed=1)

    assert _run(False).total_payoffs() == _run(True).total_payoffs()


# --- the headline finding: turnover can recover a triggered grim_trigger ---


def test_turnover_recovers_a_triggered_grim_trigger_agent_after_a_shock():
    """E21's own scenario (1 sensitive agent among 7 cooperative, hit by a
    one-time recoverable shock) found grim_trigger settles into a
    permanently depressed equilibrium with no return path. Resetting that
    one agent's state via turnover, right after it locks, recovers the pool
    to full health -- something nothing else in this engine could do to an
    already-triggered grim_trigger agent."""
    agents = (AgentSpec("grim_trigger", 1, COOP_PARAMS), AgentSpec("cooperative", 7, COOP_PARAMS))

    def _run(with_turnover: bool):
        disturbances = [DisturbanceConfig(kind="resource_shock", round=30, magnitude=0.15)]
        if with_turnover:
            # round 32 % 8 == 0 -> hits agent index 0, the grim_trigger agent.
            disturbances.append(DisturbanceConfig(kind="agent_turnover", round=32, magnitude=0.125))
        cfg = SimulationConfig(
            name="e24", rounds=100, information_model="global", resource=_resource(),
            agents=agents, disturbances=tuple(disturbances),
        )
        return run_simulation(cfg, seed=1)

    locked = _run(False)
    recovered = _run(True)
    assert locked.rounds[-1].resource_after_harvest < 45  # stuck below the healthy target
    assert recovered.rounds[-1].resource_after_harvest == pytest.approx(50.0)
    assert sum(recovered.total_payoffs()) > sum(locked.total_payoffs())
