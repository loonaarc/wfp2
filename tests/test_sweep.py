"""Tests for the parameter-sweep runner."""

from dataclasses import replace

from emergent_cooperation.core.config import (
    AgentSpec,
    ExperimentConfig,
    ResourceConfig,
    SimulationConfig,
)
from emergent_cooperation.experiments.sweep import run_grid, with_resource


def _base():
    sim = SimulationConfig(
        name="sweep_test",
        rounds=40,
        information_model="global",
        resource=ResourceConfig(initial_level=50.0, capacity=100.0, regeneration_rate=0.4),
        agents=(AgentSpec("cooperative", count=4, params={"capacity": 100.0}),),
    )
    return ExperimentConfig(simulation=sim, seeds=(1, 2))


def test_with_resource_changes_only_nested_field():
    sim = _base().simulation
    changed = with_resource(sim, initial_level=20.0)
    assert changed.resource.initial_level == 20.0
    assert changed.resource.capacity == sim.resource.capacity
    assert changed.rounds == sim.rounds  # untouched


def test_run_grid_covers_the_cartesian_product():
    base = _base()
    axes = {
        "initial_level": [20.0, 50.0, 80.0],
        "information_model": ["global", "private"],
    }

    def make(sim, combo):
        sim = with_resource(sim, initial_level=combo["initial_level"])
        return replace(sim, information_model=combo["information_model"])

    df = run_grid(base, axes, make)
    # 3 initial levels x 2 info models x 2 seeds = 12 rows.
    assert len(df) == 12
    # Axis columns exist and come first.
    assert list(df.columns[:2]) == ["initial_level", "information_model"]
    assert set(df["initial_level"]) == {20.0, 50.0, 80.0}
    assert set(df["information_model"]) == {"global", "private"}


def test_run_grid_is_deterministic():
    base = _base()
    axes = {"initial_level": [30.0, 60.0]}

    def make(sim, combo):
        return with_resource(sim, initial_level=combo["initial_level"])

    a = run_grid(base, axes, make)
    b = run_grid(base, axes, make)
    assert a.equals(b)
