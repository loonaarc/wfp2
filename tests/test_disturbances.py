"""Tests for environmental disturbances and the resilience metrics (E8)."""

import pytest

from emergent_cooperation.core.config import (
    AgentSpec,
    DisturbanceConfig,
    ResourceConfig,
    SimulationConfig,
)
from emergent_cooperation.core.simulation import Simulation, run_simulation
from emergent_cooperation.disturbances import AgentFailure, ResourceShock, build_disturbances
from emergent_cooperation.environment.resource import ResourcePool
from emergent_cooperation.metrics.metrics import compute_metrics


def _cfg(information_model="global", *, shock=True, strategy="cooperative", rounds=120):
    disturbances = (
        (DisturbanceConfig("resource_shock", round=60, magnitude=0.7),) if shock else ()
    )
    return SimulationConfig(
        name=f"dist_{information_model}",
        rounds=rounds,
        information_model=information_model,
        resource=ResourceConfig(initial_level=50.0, capacity=100.0, regeneration_rate=0.4),
        agents=(AgentSpec(strategy, 8, {"regeneration_rate": 0.4, "capacity": 100.0}),),
        disturbances=disturbances,
    )


# --- config validation ---------------------------------------------------------


def test_unknown_disturbance_kind_rejected():
    with pytest.raises(ValueError, match="kind"):
        DisturbanceConfig(kind="volcano", round=10, magnitude=0.5)


@pytest.mark.parametrize("magnitude", [0.0, -0.1, 1.5])
def test_shock_magnitude_out_of_range_rejected(magnitude):
    with pytest.raises(ValueError, match="magnitude"):
        DisturbanceConfig(kind="resource_shock", round=10, magnitude=magnitude)


def test_disturbance_after_run_end_rejected():
    with pytest.raises(ValueError, match="outside the run"):
        SimulationConfig(rounds=50, disturbances=(DisturbanceConfig(round=60, magnitude=0.5),))


# --- the ResourceShock mechanism ----------------------------------------------


def test_resource_shock_cuts_stock_only_on_its_round():
    pool = ResourcePool(ResourceConfig(initial_level=100.0, capacity=100.0))
    shock = ResourceShock(round=5, magnitude=0.7)
    assert shock.apply(4, pool, []) is False
    assert pool.level == 100.0  # untouched before its round
    assert shock.apply(5, pool, []) is True
    assert pool.level == pytest.approx(30.0)  # lost 70%
    assert shock.apply(6, pool, []) is False
    assert pool.level == pytest.approx(30.0)  # fires only once


def test_build_disturbances_from_config():
    built = build_disturbances((DisturbanceConfig("resource_shock", round=3, magnitude=0.4),))
    assert len(built) == 1 and isinstance(built[0], ResourceShock)
    assert built[0].round == 3 and built[0].magnitude == 0.4


def test_run_records_the_disturbed_round():
    result = run_simulation(_cfg("global"), seed=1)
    disturbed = [r.round_index for r in result.rounds if r.disturbed]
    assert disturbed == [60]


def test_disturbed_run_is_reproducible():
    a = run_simulation(_cfg("private"), seed=3).final_resource_level
    b = run_simulation(_cfg("private"), seed=3).final_resource_level
    assert a == b


# --- resilience metrics & the headline result ---------------------------------


def _metrics(cfg, seed=1):
    return compute_metrics(
        run_simulation(cfg, seed=seed), capacity=100.0, regeneration_rate=0.4,
        collapse_threshold=1.0,
    )


def test_no_disturbance_leaves_resilience_metrics_empty():
    m = _metrics(_cfg("global", shock=False))
    assert m["shock_round"] is None
    assert m["recovered"] is False
    assert m["recovery_time"] is None


def test_observing_cooperators_recover_but_blind_ones_collapse():
    # The central E8 finding: same strategy, resilience decided by information.
    observing = _metrics(_cfg("global"))
    blind = _metrics(_cfg("private"))

    assert observing["shock_round"] == 60
    assert observing["recovered"] is True
    assert observing["recovery_time"] is not None and observing["recovery_time"] > 0
    assert observing["final_resource_level"] > 40  # climbed back toward K/2

    assert blind["recovered"] is False
    assert blind["recovery_time"] is None
    assert blind["final_resource_level"] < 1  # collapsed and stayed down


def test_enforcement_does_not_confer_resilience_when_blind():
    # Sanctioning (a policed quota) collapses under the shock just like plain
    # cooperation when agents are blind: the quota caps over-use, it does not force
    # restraint on a shrunken pool.
    blind_sanction = _metrics(_cfg("private", strategy="sanctioning"))
    assert blind_sanction["recovered"] is False


def _mixed_cfg(strategy, n_selfish, *, rounds=120):
    # Global info; (8 - n_selfish) cooperators/sanctioners + n_selfish free-riders.
    params = {"regeneration_rate": 0.4, "capacity": 100.0}
    if strategy == "sanctioning":
        params["monitoring_cost"] = 0.2
    return SimulationConfig(
        name=f"mixed_{strategy}",
        rounds=rounds,
        information_model="global",
        resource=ResourceConfig(initial_level=50.0, capacity=100.0, regeneration_rate=0.4),
        agents=(
            AgentSpec(strategy, 8 - n_selfish, params),
            AgentSpec("selfish", n_selfish, {"greed": 1.0}),
        ),
        disturbances=(DisturbanceConfig("resource_shock", round=60, magnitude=0.7),),
    )


def test_enforcement_outlasts_cooperation_under_shock_with_free_riders():
    # The E9 finding: with free-riders present and observation available, enforcement
    # recovers the commons after the shock where plain cooperation cannot.
    coop = _metrics(_mixed_cfg("cooperative", 2))
    enforced = _metrics(_mixed_cfg("sanctioning", 2))
    assert coop["final_resource_level"] < 25  # cooperation degraded / not restored
    assert enforced["final_resource_level"] > 40  # enforcement back toward K/2
    assert enforced["final_resource_level"] > coop["final_resource_level"]


# --- agent failure (E10) -------------------------------------------------------


def test_agent_failure_kind_validates_magnitude():
    with pytest.raises(ValueError, match="magnitude"):
        DisturbanceConfig(kind="agent_failure", round=5, magnitude=1.5)


def test_agent_failure_deactivates_agents_in_index_order():
    failure = AgentFailure(round=3, fraction=0.25)
    agents = [type("A", (), {"active": True})() for _ in range(8)]
    assert failure.apply(2, None, agents) is False  # not its round
    assert all(a.active for a in agents)
    assert failure.apply(3, None, agents) is True
    assert [a.active for a in agents] == [False, False, True, True, True, True, True, True]


def _e10_cfg(agents, *, fail=True, rounds=60):
    disturbances = (
        (DisturbanceConfig("agent_failure", round=30, magnitude=0.25),) if fail else ()
    )
    return SimulationConfig(
        name="e10",
        rounds=rounds,
        information_model="global",
        resource=ResourceConfig(initial_level=50.0, capacity=100.0, regeneration_rate=0.4),
        agents=agents,
        disturbances=disturbances,
    )


_SANCTION = {"regeneration_rate": 0.4, "capacity": 100.0, "monitoring_cost": 0.2}
_COOP = {"regeneration_rate": 0.4, "capacity": 100.0}


def test_failed_agent_goes_inactive_and_stops_harvesting():
    # Agent 0 fails at round 30; afterwards it must be inactive and harvest nothing.
    cfg = _e10_cfg((AgentSpec("cooperative", 8, _COOP),))
    sim = Simulation(cfg, seed=1)
    sim.run()
    failed = sim.agents[0]
    assert failed.active is False
    assert failed.last_harvest == 0.0  # nothing harvested in the final (post-failure) round


def test_losing_the_enforcer_collapses_a_commons_that_holds_without_failure():
    # E10 headline: enforcement is a single point of failure.
    enforced = (AgentSpec("sanctioning", 2, _SANCTION), AgentSpec("selfish", 6, {"greed": 1.0}))
    held = run_simulation(_e10_cfg(enforced, fail=False), seed=1).final_resource_level
    lost = run_simulation(_e10_cfg(enforced, fail=True), seed=1).final_resource_level
    assert held > 40  # enforcement holds the commons when nobody fails
    assert lost < 5  # failing the 2 sanctioners removes enforcement -> collapse


def test_self_correcting_commons_is_robust_to_losing_members():
    # Contrast: losing cooperators does not endanger a self-organizing commons.
    coop = (AgentSpec("cooperative", 8, _COOP),)
    lost = run_simulation(_e10_cfg(coop, fail=True), seed=1).final_resource_level
    assert lost > 40  # the remaining cooperators still self-correct
