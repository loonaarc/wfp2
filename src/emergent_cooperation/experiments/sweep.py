"""Parameter sweeps: run an experiment across a grid of parameter values.

A *sweep* runs the seed-controlled :func:`run_experiment` once for every
combination of a set of parameter *axes* (e.g. ``initial_level`` x
``information_model``) and returns one tidy table with the swept parameters added
as columns next to the per-seed metrics. This is the tool for systematic,
comparable studies (see ``docs/experiment-design.md``).

The generic machinery here (take the Cartesian product of the axes, run each
combination, tag the rows) is kept separate from the *specific* knowledge of how a
parameter maps onto a config — that is supplied by the caller as a small
``make_config`` function, so the same runner serves any study.
"""

from __future__ import annotations

import itertools
from collections.abc import Callable
from dataclasses import replace
from typing import Any

import pandas as pd

from ..core.config import ExperimentConfig, SimulationConfig
from .runner import run_experiment

#: A function that applies one parameter combination to the base simulation config.
MakeConfig = Callable[[SimulationConfig, dict[str, Any]], SimulationConfig]


def with_resource(simulation: SimulationConfig, **resource_changes: Any) -> SimulationConfig:
    """Return a copy of ``simulation`` with its (nested) resource fields changed.

    A convenience for sweeps that vary resource parameters, since the config
    objects are immutable and the resource is nested one level down.

    Example:
        ``with_resource(sim, initial_level=20.0)``
    """
    return replace(simulation, resource=replace(simulation.resource, **resource_changes))


def run_grid(
    base: ExperimentConfig,
    axes: dict[str, list[Any]],
    make_config: MakeConfig,
) -> pd.DataFrame:
    """Run ``base`` for every combination of the ``axes`` values.

    Args:
        base: The base experiment (its seed list is reused for every combination).
        axes: Mapping of axis name to the list of values to sweep. The Cartesian
            product of all axes defines the combinations.
        make_config: Callable ``(base_simulation, combo) -> SimulationConfig`` that
            applies one combination (``combo`` maps each axis name to a value) to
            the base simulation config.

    Returns:
        A tidy DataFrame with one row per (combination x seed): the axis columns
        followed by all per-seed metric columns.
    """
    axis_names = list(axes)
    frames: list[pd.DataFrame] = []
    for combo_values in itertools.product(*(axes[name] for name in axis_names)):
        combo = dict(zip(axis_names, combo_values, strict=True))
        simulation = make_config(base.simulation, combo)
        experiment = replace(base, simulation=simulation)
        metrics = run_experiment(experiment).metrics.copy()
        # Tag each metric row with the parameter combination that produced it.
        for name, value in combo.items():
            metrics[name] = value
        frames.append(metrics)
    tidy = pd.concat(frames, ignore_index=True)
    # Put the swept axis columns first for readability.
    ordered = axis_names + [c for c in tidy.columns if c not in axis_names]
    return tidy[ordered]
