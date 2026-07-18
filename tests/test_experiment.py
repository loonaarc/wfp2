"""Tests for config loading, metrics, and the experiment runner/export."""

import json

from emergent_cooperation.core.config import ExperimentConfig, load_experiment
from emergent_cooperation.experiments.runner import export_outcome, run_experiment
from emergent_cooperation.metrics.metrics import gini


def test_gini_extremes():
    assert gini([1.0, 1.0, 1.0]) == 0.0  # perfect equality
    assert gini([0.0, 0.0, 0.0]) == 0.0  # degenerate -> defined as 0
    # One agent takes everything -> approaches (n-1)/n.
    assert gini([0.0, 0.0, 0.0, 4.0]) > 0.6


def _experiment_dict():
    return {
        "name": "unit_experiment",
        "rounds": 30,
        "information_model": "global",
        "seeds": [1, 2, 3],
        "resource": {"initial_level": 50.0, "capacity": 100.0, "regeneration_rate": 0.4},
        "agents": [{"strategy": "cooperative", "count": 4, "params": {"capacity": 100.0}}],
    }


def test_experiment_config_from_dict_roundtrips_fields():
    cfg = ExperimentConfig.from_dict(_experiment_dict())
    assert cfg.seeds == (1, 2, 3)
    assert cfg.simulation.rounds == 30
    assert cfg.simulation.num_agents == 4


def test_run_experiment_produces_one_metric_row_per_seed():
    cfg = ExperimentConfig.from_dict(_experiment_dict())
    outcome = run_experiment(cfg)
    assert len(outcome.metrics) == 3
    assert set(outcome.metrics["seed"]) == {1, 2, 3}
    assert "sustainability_ratio" in outcome.metrics.columns


def test_export_writes_expected_files(tmp_path):
    cfg = ExperimentConfig.from_dict(_experiment_dict())
    outcome = run_experiment(cfg)
    out = export_outcome(outcome, tmp_path / "exp")
    assert (out / "resolved_config.yaml").exists()
    assert (out / "metrics.csv").exists()
    assert (out / "round_history.csv").exists()
    provenance = json.loads((out / "provenance.json").read_text())
    assert provenance["seeds"] == [1, 2, 3]
    assert provenance["status"] == "completed"
    assert provenance["package_version"]


def test_loading_bundled_configs(tmp_path):
    # Sanity: every shipped config parses into a valid experiment.
    import pathlib

    config_dir = pathlib.Path(__file__).resolve().parent.parent / "configs"
    for path in sorted(config_dir.glob("*.yaml")):
        cfg = load_experiment(path)
        assert cfg.simulation.num_agents > 0
