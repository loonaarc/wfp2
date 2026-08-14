"""Experiment E14: population-type diversity -- does the near-optimal set grow
as more *distinct* strategies coexist in one population, before any group or
boundary structure gets added on top?

This is the axis E15/E16 (nested enforcement, boundaries) were quietly relying
on without ever testing alone: E15's own `k`-sweep and E16's outsider-type
sweep both vary population composition, but neither isolates "how many
distinct types are present" as its own question. This script does exactly
that, in the same closed/flat/global-information baseline E15 used, before
any group or boundary structure exists at all.

Population: fixed at N = 8 agents, closed, flat (one group), global
information -- the same baseline E15/E16 build on top of. Every reachable
composition across all five registered non-loner strategies (`cooperative`,
`conditional_cooperator`, `compensating_cooperator`, `selfish`,
`sanctioning`) is swept -- 495 compositions in total (stars-and-bars:
C(8+5-1, 5-1)). `sanctioning` is included deliberately, even though it is
also what E15/E16 vary: here it is one *option* among several a population
can include, on equal footing with the others, not the sole axis being
studied -- diversity is about how many distinct strategies coexist,
`sanctioning` being one candidate strategy is exactly what that means.
`loner` is still excluded: it is an evolution-mode-only opt-out, not a
harvesting decision available in a single run.

"Diversity" = how many of the five types have a non-zero count in a given
composition (1..5). For each diversity level, near-optimal-set-size is
reported both as an absolute count and as a fraction of compositions tested
at that level (see docs/complexity-synthesis.md for why both, never just
one).

Outputs go to ``results/E14_population_diversity/``. Run with::

    python scripts/experiment_population_diversity.py
"""

from __future__ import annotations

from itertools import product
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

OUT_DIR = Path(__file__).resolve().parent.parent / "results" / "E14_population_diversity"
SEEDS = (1,)  # deterministic strategies only -> exact, not a noisy mean (see E1)
ROUNDS = 100
CAPACITY = 100.0
G = 0.4
N = 8  # population size, matching E15/E16's governed population

# All five registered strategies usable in a single (non-evolution) run.
# `loner` is excluded: it's an evolution-mode-only opt-out, not a harvesting
# decision available here.
TYPES = (
    "cooperative",
    "conditional_cooperator",
    "compensating_cooperator",
    "selfish",
    "sanctioning",
)

# Same provisional threshold as E15/E16, for direct comparability across axes
# (see docs/experiments/E15-groups.md for why 0.80, not 0.95).
THRESHOLD = 0.80


def _params(strategy: str) -> dict:
    if strategy == "selfish":
        return {"greed": 1.0}
    p = {"regeneration_rate": G, "capacity": CAPACITY}
    if strategy == "sanctioning":
        p["monitoring_cost"] = 0.2
    return p


def _compositions() -> list[tuple[int, ...]]:
    """Every composition of TYPES's counts (each >= 0) summing to N.

    Stars-and-bars over len(TYPES)-1 free cut points; the last type's count is
    derived so every tuple sums to exactly N: C(N + len(TYPES) - 1, len(TYPES)
    - 1) = C(12, 4) = 495 for 5 types.
    """
    out = []
    for free in product(range(N + 1), repeat=len(TYPES) - 1):
        last = N - sum(free)
        if 0 <= last <= N:
            out.append((*free, last))
    return out


def _experiment(composition: tuple[int, ...]) -> ExperimentConfig:
    """One closed, flat (group=0) population for this exact composition."""
    agents = [
        AgentSpec(strategy, count, _params(strategy))
        for strategy, count in zip(TYPES, composition, strict=True)
        if count > 0
    ]
    label = "_".join(f"{s[:4]}{c}" for s, c in zip(TYPES, composition, strict=True) if c > 0)
    sim = SimulationConfig(
        name=f"E14_pop_{label}",
        rounds=ROUNDS,
        information_model="global",
        resource=ResourceConfig(
            initial_level=CAPACITY / 2,
            capacity=CAPACITY,
            regeneration_rate=G,
            collapse_threshold=1.0,
        ),
        agents=tuple(agents),
    )
    return ExperimentConfig(simulation=sim, seeds=SEEDS, record_history=False)


def summarise() -> pd.DataFrame:
    """welfare_efficiency, sustainability_ratio, payoff_gini, collapsed, and
    diversity (count of non-zero types) for every one of the 495 compositions.
    Single seed (SEEDS=(1,)), deterministic strategies -> exact, not an average.
    """
    rows = []
    for composition in _compositions():
        outcome = run_experiment(_experiment(composition))
        metrics = outcome.metrics
        gini = metrics["payoff_gini"].iloc[0]
        diversity = sum(1 for c in composition if c > 0)
        row = {f"n_{strategy}": count for strategy, count in zip(TYPES, composition, strict=True)}
        row.update(
            {
                "diversity": diversity,
                "welfare_efficiency": float(metrics["welfare_efficiency"].mean()),
                "sustainability_ratio": float(metrics["sustainability_ratio"].mean()),
                "payoff_gini": None if pd.isna(gini) else float(gini),
                "collapsed": bool(metrics["collapsed"].any()),
            }
        )
        rows.append(row)
    return pd.DataFrame(rows)


def near_optimal_by_diversity(summary: pd.DataFrame) -> pd.DataFrame:
    """For each diversity level (1..4), how many of the tested compositions at
    that level clear THRESHOLD -- both as a count and as a fraction (see
    docs/complexity-synthesis.md's "report both" lesson).
    """
    rows = []
    for diversity in sorted(summary["diversity"].unique()):
        sub = summary[summary["diversity"] == diversity]
        passing = int((sub["welfare_efficiency"] >= THRESHOLD).sum())
        rows.append(
            {
                "diversity": diversity,
                "configs_tested": len(sub),
                "near_optimal_count": passing,
                "near_optimal_fraction": passing / len(sub),
            }
        )
    return pd.DataFrame(rows)


def make_figure(curve: pd.DataFrame, path: Path) -> None:
    """Near-optimal-set-size vs. population-type diversity -- two panels
    (count, fraction), same convention as E15/E16's complexity_curve.png.
    """
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.8))
    color = "#1f77b4"

    ax = axes[0]
    ax.plot(curve["diversity"], curve["near_optimal_count"], lw=2.2, marker="o", color=color)
    for row in curve.itertuples():
        ax.annotate(
            f"{row.near_optimal_count}/{row.configs_tested}",
            (row.diversity, row.near_optimal_count),
            textcoords="offset points", xytext=(0, 8), fontsize=8, ha="center", color=color,
        )
    ax.set_xticks(curve["diversity"])
    ax.set_xlabel("diversity -- number of distinct types present")
    ax.set_ylabel("near-optimal count")
    ax.set_ylim(bottom=-0.5)
    ax.set_title("Absolute count -- does the set of viable\ncompositions actually grow?", fontsize=10.5)

    ax = axes[1]
    ax.plot(curve["diversity"], curve["near_optimal_fraction"], lw=2.2, marker="o", color=color)
    for row in curve.itertuples():
        ax.annotate(
            f"{row.near_optimal_count}/{row.configs_tested}",
            (row.diversity, row.near_optimal_fraction),
            textcoords="offset points", xytext=(0, 8), fontsize=8, ha="center", color=color,
        )
    ax.set_xticks(curve["diversity"])
    ax.set_xlabel("diversity -- number of distinct types present")
    ax.set_ylabel("near-optimal fraction (of compositions tested)")
    ax.set_ylim(-0.05, 1.05)
    ax.set_title("Fraction of the tried space -- does it get\nharder to stumble into one?", fontsize=10.5)

    fig.suptitle(
        "Near-optimal-set-size vs. population-type diversity (E14)\n"
        "(closed, flat, global information; threshold = welfare_efficiency >= 0.80, provisional)",
        fontsize=10,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.92))
    fig.savefig(path, dpi=130)
    plt.close(fig)


def main() -> None:
    """Run the full compositional sweep; export the summary, curve, and figure."""
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    summary = summarise()
    summary.to_csv(OUT_DIR / "summary.csv", index=False)

    curve = near_optimal_by_diversity(summary)
    curve.to_csv(OUT_DIR / "diversity_curve.csv", index=False)
    make_figure(curve, OUT_DIR / "diversity_curve.png")

    print(f"E14 -- {len(summary)} compositions tested, threshold={THRESHOLD}:")
    for row in curve.itertuples():
        print(
            f"  diversity={row.diversity}: {row.near_optimal_count}/{row.configs_tested} "
            f"({row.near_optimal_fraction:.2f})"
        )

    passing = summary[summary["welfare_efficiency"] >= THRESHOLD].sort_values(
        ["diversity", "welfare_efficiency"], ascending=[True, False]
    )
    print(f"\nAll {len(passing)} passing compositions:")
    for row in passing.itertuples():
        print(
            f"  coop={row.n_cooperative} cond={row.n_conditional_cooperator} "
            f"comp={row.n_compensating_cooperator} self={row.n_selfish} "
            f"sanc={row.n_sanctioning} -> welfare_efficiency={row.welfare_efficiency:.2f}"
        )

    print(f"\nWrote summary.csv, diversity_curve.csv, diversity_curve.png to: {OUT_DIR}")


if __name__ == "__main__":
    main()
