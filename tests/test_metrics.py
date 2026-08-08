"""Tests for the summary metrics (survival, efficiency, over-usage)."""

import pytest

from emergent_cooperation.core.config import (
    AgentSpec,
    ResourceConfig,
    SimulationConfig,
)
from emergent_cooperation.core.simulation import run_simulation
from emergent_cooperation.metrics.metrics import compute_metrics


def _run(strategy, count=8, information_model="global", rounds=100, **params):
    cfg = SimulationConfig(
        name=f"m_{strategy}",
        rounds=rounds,
        information_model=information_model,
        resource=ResourceConfig(initial_level=50.0, capacity=100.0, regeneration_rate=0.4),
        agents=(AgentSpec(strategy=strategy, count=count, params=params),),
    )
    return run_simulation(cfg, seed=1)


def _metrics(result):
    return compute_metrics(result, capacity=100.0, regeneration_rate=0.4, collapse_threshold=1.0)


def test_cooperative_run_is_efficient_and_never_over_uses():
    m = _metrics(_run("cooperative", regeneration_rate=0.4, capacity=100.0))
    # Harvests exactly the MSY (10) each round for 100 rounds → efficiency 1.0.
    assert m["efficiency"] == 1.0
    assert m["over_usage_rate"] == 0.0
    assert m["survival_time"] == 100
    assert not m["collapsed"]


def test_selfish_run_collapses_fast_and_over_uses():
    m = _metrics(_run("selfish", greed=1.0))
    assert m["collapsed"]
    assert m["survival_time"] == 0  # collapses in the very first round
    # The one active round (round 0) over-harvests → over-usage rate 1.0.
    assert m["over_usage_rate"] == 1.0


def test_efficiency_and_over_usage_are_none_without_growth_rate():
    m = compute_metrics(_run("cooperative", capacity=100.0), capacity=100.0)
    assert m["efficiency"] is None
    assert m["over_usage_rate"] is None
    # Metrics that don't need the growth rate are still present.
    assert m["survival_time"] == 100


def test_survival_time_equals_collapse_round_when_collapsing():
    result = _run("selfish", greed=0.5)
    m = _metrics(result)
    assert m["collapsed"]
    assert m["survival_time"] == m["collapse_round"]


def test_welfare_efficiency_matches_gross_efficiency_without_monitoring_cost():
    m = _metrics(_run("cooperative", regeneration_rate=0.4, capacity=100.0))
    assert m["welfare_efficiency"] == m["efficiency"] == 1.0


def test_welfare_efficiency_is_below_gross_efficiency_with_monitoring_cost():
    # 8 sanctioners, cost 0.2/round: net payoff 105.0 vs 1000 sustainable benchmark
    # -> welfare_efficiency = 840/1000 = 0.84, while gross efficiency stays 1.0.
    m = _metrics(
        _run("sanctioning", regeneration_rate=0.4, capacity=100.0, monitoring_cost=0.2)
    )
    assert m["efficiency"] == 1.0
    assert m["welfare_efficiency"] == pytest.approx(0.84)
