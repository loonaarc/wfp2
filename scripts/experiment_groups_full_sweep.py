"""Experiment E15: nested enforcement, reworked to sweep the *full*
population-composition matrix per group, not just "k groups sanctioning, rest
selfish".

The original E15 (before this rework) only varied `k`: how many of the `m`
groups were fully `sanctioning` vs. fully `selfish` -- a 2-type sweep,
exactly the kind of narrow composition E14 (population-type diversity) was
built to generalize away from. This script applies E14's *full* 5-type
compositional sweep independently to each group: every group of size
`N/m` gets its own composition across (`cooperative`,
`conditional_cooperator`, `compensating_cooperator`, `selfish`,
`sanctioning`), and every combination of per-group compositions is tested --
not just uniform, single-strategy groups.

Combinatorics (stars-and-bars per group, then a cross-product across groups):
  m=1: C(8+5-1,4)   = 495 compositions              (= E14 itself)
  m=2: C(4+5-1,4)^2 = 70^2  = 4,900 joint configs
  m=4: C(2+5-1,4)^4 = 15^4  = 50,625 joint configs
  total: 56,020 simulations, ~2ms each -> ~2 minutes

Deliberately *not* extended the same way to boundaries (E16)'s outsider
side: crossing this same full sweep against a fully-explored outsider
composition would be `56,020 x 70 ~= 3.9M` simulations (~2+ hours) for a
result that would be unwieldy to summarise. E16 keeps the outsider side at
its existing, already-validated treatment (a handful of named types) and
crosses only the *governed* side with this full sweep -- see
scripts/experiment_boundaries_full_sweep.py.

Uses `run_simulation`/`compute_metrics` directly rather than
`run_experiment` to avoid per-call DataFrame construction overhead at this
scale (measured ~2ms/sim vs. meaningfully more through the experiment
runner's pandas path).

Outputs go to ``results/E15_groups_full_sweep/``. Run with::

    python scripts/experiment_groups_full_sweep.py
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
    ResourceConfig,
    SimulationConfig,
)
from emergent_cooperation.core.simulation import run_simulation  # noqa: E402
from emergent_cooperation.metrics.metrics import compute_metrics  # noqa: E402

OUT_DIR = Path(__file__).resolve().parent.parent / "results" / "E15_groups_full_sweep"
ROUNDS = 100
CAPACITY = 100.0
G = 0.4
N = 8  # governed population size, matching E14/E16
GROUP_COUNTS = (1, 2, 4)
TYPES = (
    "cooperative",
    "conditional_cooperator",
    "compensating_cooperator",
    "selfish",
    "sanctioning",
)
THRESHOLD = 0.80  # same provisional threshold as E14/E16
# Invariant across the whole sweep -- only `agents` varies per call, so build
# it once instead of on every one of the (tens of) thousands of simulations.
RESOURCE = ResourceConfig(
    initial_level=CAPACITY / 2, capacity=CAPACITY, regeneration_rate=G, collapse_threshold=1.0
)


def _params(strategy: str) -> dict:
    if strategy == "selfish":
        return {"greed": 1.0}
    p = {"regeneration_rate": G, "capacity": CAPACITY}
    if strategy == "sanctioning":
        p["monitoring_cost"] = 0.2
    return p


def _sub_compositions(size: int) -> list[tuple[int, ...]]:
    """Every composition of TYPES's counts (each >= 0) summing to `size`."""
    out = []
    for free in product(range(size + 1), repeat=len(TYPES) - 1):
        last = size - sum(free)
        if 0 <= last <= size:
            out.append((*free, last))
    return out


def _welfare_efficiency(specs: list[AgentSpec], name: str = "E15_full") -> tuple[float, bool]:
    cfg = SimulationConfig(
        name=name,
        rounds=ROUNDS,
        information_model="global",
        resource=RESOURCE,
        agents=tuple(specs),
    )
    result = run_simulation(cfg, seed=1)
    metrics = compute_metrics(result, capacity=CAPACITY, regeneration_rate=G)
    return metrics["welfare_efficiency"], metrics["collapsed"]


def _specs_for(group_compositions: tuple[tuple[int, ...], ...]) -> list[AgentSpec]:
    specs = []
    for g, composition in enumerate(group_compositions):
        for strategy, count in zip(TYPES, composition, strict=True):
            if count > 0:
                specs.append(AgentSpec(strategy, count, _params(strategy), group=g))
    return specs


def sweep_m(m: int) -> pd.DataFrame:
    """Every joint combination of `m` groups' own compositions, each summing
    to `N/m`. Returns one row per joint configuration.
    """
    size = N // m
    sub_comps = _sub_compositions(size)
    rows = []
    for group_compositions in product(sub_comps, repeat=m):
        specs = _specs_for(group_compositions)
        we, collapsed = _welfare_efficiency(specs)
        row: dict[str, object] = {"m": m}
        for g, composition in enumerate(group_compositions):
            for strategy, count in zip(TYPES, composition, strict=True):
                row[f"g{g}_{strategy}"] = count
        row["welfare_efficiency"] = we
        row["collapsed"] = collapsed
        rows.append(row)
    return pd.DataFrame(rows)


def near_optimal_by_m(summaries: dict[int, pd.DataFrame]) -> pd.DataFrame:
    """Near-optimal count and fraction at each `m`, from each m's own summary."""
    rows = []
    for m, df in summaries.items():
        passing = int((df["welfare_efficiency"] >= THRESHOLD).sum())
        rows.append(
            {
                "m": m,
                "configs_tested": len(df),
                "near_optimal_count": passing,
                "near_optimal_fraction": passing / len(df),
            }
        )
    return pd.DataFrame(rows)


def make_figure(curve: pd.DataFrame, path: Path) -> None:
    """Two panels: near-optimal count and fraction vs. m."""
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.8))
    color = "#1f77b4"

    ax = axes[0]
    ax.plot(curve["m"], curve["near_optimal_count"], lw=2.2, marker="o", color=color)
    for row in curve.itertuples():
        ax.annotate(
            f"{row.near_optimal_count}/{row.configs_tested}",
            (row.m, row.near_optimal_count),
            textcoords="offset points", xytext=(0, 8), fontsize=8, ha="center", color=color,
        )
    ax.set_xticks(curve["m"])
    ax.set_xlabel("m -- number of groups")
    ax.set_ylabel("near-optimal count")
    ax.set_title("Absolute count -- does the set of viable\nconfigurations actually grow?", fontsize=10.5)

    ax = axes[1]
    ax.plot(curve["m"], curve["near_optimal_fraction"], lw=2.2, marker="o", color=color)
    for row in curve.itertuples():
        ax.annotate(
            f"{row.near_optimal_count}/{row.configs_tested}",
            (row.m, row.near_optimal_fraction),
            textcoords="offset points", xytext=(0, 8), fontsize=8, ha="center", color=color,
        )
    ax.set_xticks(curve["m"])
    ax.set_xlabel("m -- number of groups")
    ax.set_ylabel("near-optimal fraction (of configs tested)")
    ax.set_ylim(-0.05, 1.05)
    ax.set_title("Fraction of the tried space -- does it get\nharder to stumble into one?", fontsize=10.5)

    fig.suptitle(
        "Near-optimal-set-size vs. m (E15, full per-group compositional sweep)\n"
        "(closed community; threshold = welfare_efficiency >= 0.80, provisional)",
        fontsize=10,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.92))
    fig.savefig(path, dpi=130)
    plt.close(fig)


def main() -> None:
    """Run the full sweep at every m; export CSVs, the near-optimal curve, and figure."""
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    summaries: dict[int, pd.DataFrame] = {}
    for m in GROUP_COUNTS:
        print(f"Sweeping m={m}...")
        df = sweep_m(m)
        df.to_csv(OUT_DIR / f"summary_m{m}.csv", index=False)
        summaries[m] = df
        passing = int((df["welfare_efficiency"] >= THRESHOLD).sum())
        print(f"  m={m}: {passing}/{len(df)} pass (threshold={THRESHOLD})")

    curve = near_optimal_by_m(summaries)
    curve.to_csv(OUT_DIR / "near_optimal_by_m.csv", index=False)
    make_figure(curve, OUT_DIR / "near_optimal_by_m.png")

    print("\nE15 (full sweep) -- near-optimal-set-size vs. m:")
    for row in curve.itertuples():
        print(f"  m={row.m}: {row.near_optimal_count}/{row.configs_tested} ({row.near_optimal_fraction:.3f})")

    print(f"\nWrote per-m summaries, near_optimal_by_m.csv/.png to: {OUT_DIR}")


if __name__ == "__main__":
    main()
