"""Experiment E2: reciprocity in mixed populations — resource vs. fairness.

Compares two cooperator types against a growing minority of selfish free-riders:

* **unconditional** ``cooperative`` agents (self-correcting restraint), and
* ``conditional_cooperator`` agents (cooperate until the group over-extracts, then
  reciprocate by grabbing a selfish share).

For each cooperator type we sweep the number of selfish agents (0..8 of 8) and
measure whether the resource survives, how unequal the payoffs are, and how much the
free-riders earn. Tests SQ-4/SQ-5 (see docs/research-questions.md).

Outputs go to ``results/E2_reciprocity/``. Run with::

    python scripts/experiment_reciprocity.py

Write-up: ``docs/experiments/E2-reciprocity.md``.
"""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

from emergent_cooperation.core.config import (  # noqa: E402
    AgentSpec,
    ExperimentConfig,
    ResourceConfig,
    SimulationConfig,
)
from emergent_cooperation.experiments.runner import run_experiment  # noqa: E402

OUT_DIR = Path(__file__).resolve().parent.parent / "results" / "E2_reciprocity"
SEEDS = (1, 2, 3)
GROUP_SIZE = 8
COOP_PARAMS = {"regeneration_rate": 0.4, "capacity": 100.0}
SELFISH_PARAMS = {"greed": 1.0}


def _config(cooperator_type: str, n_selfish: int) -> ExperimentConfig:
    """A group of ``GROUP_SIZE`` agents: ``n_selfish`` selfish, the rest cooperators."""
    n_coop = GROUP_SIZE - n_selfish
    agents = []
    if n_coop > 0:
        agents.append(AgentSpec(cooperator_type, count=n_coop, params=dict(COOP_PARAMS)))
    if n_selfish > 0:
        agents.append(AgentSpec("selfish", count=n_selfish, params=dict(SELFISH_PARAMS)))
    sim = SimulationConfig(
        name=f"E2_{cooperator_type}_{n_selfish}sel",
        rounds=100,
        information_model="global",
        resource=ResourceConfig(
            initial_level=50.0, capacity=100.0, regeneration_rate=0.4, collapse_threshold=1.0
        ),
        agents=tuple(agents),
    )
    return ExperimentConfig(simulation=sim, seeds=SEEDS, record_history=False)


def _payoff_by_strategy(results) -> dict[str, float]:
    """Mean per-agent total payoff for each strategy, averaged over seeds."""
    sums: dict[str, list[float]] = defaultdict(list)
    for result in results:
        for strategy, payoff in zip(result.agent_strategies, result.total_payoffs(), strict=True):
            sums[strategy].append(payoff)
    return {s: sum(v) / len(v) for s, v in sums.items()}


def run_sweep() -> pd.DataFrame:
    """Run every (cooperator type, number of selfish) combination and summarise."""
    rows = []
    for cooperator_type in ["cooperative", "conditional_cooperator"]:
        for n_selfish in range(GROUP_SIZE + 1):
            outcome = run_experiment(_config(cooperator_type, n_selfish))
            m = outcome.metrics
            payoffs = _payoff_by_strategy(outcome.results)
            rows.append(
                {
                    "cooperator_type": cooperator_type,
                    "n_selfish": n_selfish,
                    "sustainability_ratio": m["sustainability_ratio"].mean(),
                    "collapsed": m["collapsed"].mean(),
                    "total_harvest": m["total_harvest"].mean(),
                    "payoff_gini": m["payoff_gini"].mean(),
                    "cooperator_payoff": payoffs.get(cooperator_type, float("nan")),
                    "selfish_payoff": payoffs.get("selfish", float("nan")),
                }
            )
    return pd.DataFrame(rows)


def make_figure(df: pd.DataFrame, path: Path) -> None:
    """Two panels: resource survival, and how much the free-riders earn."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2))
    labels = {"cooperative": "unconditional", "conditional_cooperator": "conditional"}

    for ctype, label in labels.items():
        sub = df[df["cooperator_type"] == ctype].sort_values("n_selfish")
        ax1.plot(sub["n_selfish"], sub["sustainability_ratio"], marker="o", label=label)
    ax1.set_xlabel("number of selfish agents (of 8)")
    ax1.set_ylabel("sustainability ratio (final stock / K)")
    ax1.set_title("A. Does the resource survive?")
    ax1.set_ylim(-0.02, 0.6)
    ax1.legend()

    for ctype, label in labels.items():
        sub = df[(df["cooperator_type"] == ctype) & (df["n_selfish"].between(1, 7))]
        sub = sub.sort_values("n_selfish")
        ax2.plot(sub["n_selfish"], sub["selfish_payoff"], marker="s", label=f"{label} neighbours")
    ax2.set_xlabel("number of selfish agents (of 8)")
    ax2.set_ylabel("mean payoff of a selfish free-rider")
    ax2.set_title("B. How much do free-riders earn?")
    ax2.legend()

    fig.suptitle("E2: reciprocity protects fairness (starves free-riders) but not the commons")
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)


def main() -> None:
    """Run the sweep, export the table and figure, and print a summary."""
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    df = run_sweep()
    df.to_csv(OUT_DIR / "sweep.csv", index=False)
    make_figure(df, OUT_DIR / "figure.png")

    show = df[
        [
            "cooperator_type",
            "n_selfish",
            "sustainability_ratio",
            "payoff_gini",
            "cooperator_payoff",
            "selfish_payoff",
        ]
    ].round(2)
    print(show.to_string(index=False))
    print(f"\nWrote sweep.csv and figure.png to: {OUT_DIR}")


if __name__ == "__main__":
    main()
