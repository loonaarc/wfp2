"""Run an experiment (a seed sweep) and export reproducible results.

The runner executes one :class:`~emergent_cooperation.core.simulation.Simulation`
per seed, computes summary metrics for each, and can write a self-contained
output directory: the resolved config, per-seed metrics, optional per-round
history, and a provenance record. Nothing here mutates global state; a caller can
run many experiments in one process safely.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import pandas as pd
import yaml

from ..core.config import ExperimentConfig
from ..core.simulation import run_simulation
from ..core.state import RunResult
from ..metrics.metrics import compute_metrics
from .provenance import Provenance


@dataclass
class ExperimentOutcome:
    """Everything an experiment produces, before it is written to disk.

    Attributes:
        config: The experiment configuration that was run.
        results: One :class:`RunResult` per seed, in seed order.
        metrics: One metric row per seed (a tidy DataFrame).
        provenance: Reproducibility metadata for the whole experiment.
    """

    config: ExperimentConfig
    results: list[RunResult]
    metrics: pd.DataFrame
    provenance: Provenance = field(default_factory=Provenance)


def run_experiment(config: ExperimentConfig) -> ExperimentOutcome:
    """Run one simulation per seed and collect metrics.

    Args:
        config: The experiment configuration (base run plus seed sweep).

    Returns:
        The in-memory outcome; use :func:`export_outcome` to persist it.
    """
    resource = config.simulation.resource
    results: list[RunResult] = []
    rows: list[dict] = []
    for seed in config.seeds:
        result = run_simulation(config.simulation, seed=seed)
        results.append(result)
        rows.append(
            compute_metrics(
                result,
                capacity=resource.capacity,
                regeneration_rate=resource.regeneration_rate,
                collapse_threshold=resource.collapse_threshold,
                regeneration_rule=resource.regeneration_rule,
            )
        )

    provenance = Provenance(seeds=tuple(config.seeds), status="completed")
    return ExperimentOutcome(
        config=config,
        results=results,
        metrics=pd.DataFrame(rows),
        provenance=provenance,
    )


def history_frame(results: list[RunResult]) -> pd.DataFrame:
    """Flatten per-round history across seeds into one long-format DataFrame."""
    records: list[dict] = []
    for result in results:
        for r in result.rounds:
            records.append(
                {
                    "seed": result.seed,
                    "round": r.round_index,
                    "resource_start": r.resource_start,
                    "resource_after_regen": r.resource_after_regen,
                    "total_requested": r.total_requested,
                    "total_harvested": r.total_harvested,
                    "resource_after_harvest": r.resource_after_harvest,
                    "collapsed": r.collapsed,
                    "disturbed": r.disturbed,
                }
            )
    return pd.DataFrame(records)


def _config_to_dict(config: ExperimentConfig) -> dict:
    """Serialise an experiment config back to a plain, YAML-friendly dict."""
    sim = config.simulation
    return {
        "name": sim.name,
        "rounds": sim.rounds,
        "information_model": sim.information_model,
        "decision_noise": sim.decision_noise,
        "broadcast_reliability": sim.broadcast_reliability,
        "seeds": list(config.seeds),
        "record_history": config.record_history,
        "resource": {
            "initial_level": sim.resource.initial_level,
            "capacity": sim.resource.capacity,
            "regeneration_rate": sim.resource.regeneration_rate,
            "regeneration_rule": sim.resource.regeneration_rule,
            "collapse_threshold": sim.resource.collapse_threshold,
        },
        "agents": [
            {"strategy": a.strategy, "count": a.count, "params": dict(a.params)} for a in sim.agents
        ],
        "disturbances": [
            {"kind": d.kind, "round": d.round, "magnitude": d.magnitude} for d in sim.disturbances
        ],
    }


def export_outcome(outcome: ExperimentOutcome, output_dir: str | Path) -> Path:
    """Write an experiment's outputs to ``output_dir`` and return the path.

    The directory is created if needed and contains:

    - ``resolved_config.yaml`` — the exact config that was run.
    - ``metrics.csv`` — one row per seed.
    - ``round_history.csv`` — long-format per-round history (if ``record_history``).
    - ``provenance.json`` — reproducibility metadata.

    Args:
        outcome: The in-memory experiment outcome.
        output_dir: Destination directory (created if absent).

    Returns:
        The output directory path.
    """
    import json

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    (out / "resolved_config.yaml").write_text(
        yaml.safe_dump(_config_to_dict(outcome.config), sort_keys=False),
        encoding="utf-8",
    )
    outcome.metrics.to_csv(out / "metrics.csv", index=False)
    if outcome.config.record_history:
        history_frame(outcome.results).to_csv(out / "round_history.csv", index=False)
    (out / "provenance.json").write_text(
        json.dumps(outcome.provenance.to_dict(), indent=2),
        encoding="utf-8",
    )
    return out
