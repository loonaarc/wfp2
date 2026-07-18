"""Run the four baseline configs and print a side-by-side summary.

This is a convenience script for quickly seeing the core contrast (cooperative vs
selfish, global vs private information). It is not part of the reproducible
experiment pipeline — for that, use ``emergent-coop run --config ...``.

Run with::

    python scripts/run_baselines.py
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from emergent_cooperation.core.config import load_experiment
from emergent_cooperation.experiments.runner import run_experiment

CONFIG_DIR = Path(__file__).resolve().parent.parent / "configs"
BASELINES = [
    "all_cooperative_global.yaml",
    "all_selfish_global.yaml",
    "mixed_global.yaml",
    "all_cooperative_private.yaml",
]


def main() -> None:
    """Run each baseline and print mean metrics across seeds."""
    rows = []
    for filename in BASELINES:
        config = load_experiment(CONFIG_DIR / filename)
        outcome = run_experiment(config)
        summary = outcome.metrics.select_dtypes("number").mean()
        rows.append(
            {
                "config": config.simulation.name,
                "total_harvest": round(summary["total_harvest"], 2),
                "final_level": round(summary["final_resource_level"], 2),
                "sustainability": round(summary["sustainability_ratio"], 3),
                "collapsed": round(outcome.metrics["collapsed"].mean(), 2),
                "payoff_gini": round(summary["payoff_gini"], 3),
            }
        )
    print(pd.DataFrame(rows).to_string(index=False))


if __name__ == "__main__":
    main()
