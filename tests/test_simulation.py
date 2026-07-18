"""Tests for the simulation engine: determinism and expected dynamics."""

from emergent_cooperation.core.config import (
    AgentSpec,
    ResourceConfig,
    SimulationConfig,
)
from emergent_cooperation.core.simulation import run_simulation


def _config(strategy, count=8, information_model="global", **params):
    return SimulationConfig(
        name=f"test_{strategy}",
        rounds=60,
        information_model=information_model,
        resource=ResourceConfig(initial_level=50.0, capacity=100.0, regeneration_rate=0.4),
        agents=(AgentSpec(strategy=strategy, count=count, params=params),),
    )


def test_run_is_deterministic_for_same_seed():
    cfg = _config("selfish", greed=1.0)
    a = run_simulation(cfg, seed=123)
    b = run_simulation(cfg, seed=123)
    assert a.total_payoffs() == b.total_payoffs()
    assert a.final_resource_level == b.final_resource_level


def test_all_selfish_population_collapses_the_resource():
    cfg = _config("selfish", greed=1.0)
    result = run_simulation(cfg, seed=1)
    assert result.rounds[-1].collapsed
    assert result.final_resource_level <= cfg.resource.collapse_threshold


def test_all_cooperative_population_sustains_the_resource():
    cfg = _config("cooperative", regeneration_rate=0.4, capacity=100.0)
    result = run_simulation(cfg, seed=1)
    assert not result.rounds[-1].collapsed
    assert result.final_resource_level > 10.0


def test_harvest_never_exceeds_available_stock():
    cfg = _config("selfish", greed=2.0)
    result = run_simulation(cfg, seed=1)
    for record in result.rounds:
        assert record.total_harvested <= record.resource_after_regen + 1e-9


def test_agent_count_matches_specs():
    cfg = SimulationConfig(
        name="mix",
        rounds=10,
        agents=(
            AgentSpec("selfish", count=3),
            AgentSpec("cooperative", count=2, params={"capacity": 100.0}),
        ),
    )
    result = run_simulation(cfg, seed=0)
    assert result.num_agents == 5
    assert result.agent_strategies == (
        "selfish",
        "selfish",
        "selfish",
        "cooperative",
        "cooperative",
    )


def test_private_information_hides_resource_level():
    # Cooperative agents under private info act on assumed ecology, not true R.
    # They should still avoid collapse here (assumption is conservative).
    cfg = _config("cooperative", information_model="private", capacity=100.0)
    result = run_simulation(cfg, seed=1)
    assert not result.rounds[-1].collapsed
