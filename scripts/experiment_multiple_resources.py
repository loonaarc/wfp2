"""Experiment E20: multiple resources -- diversifying effort, specialist vs. generalist monitors.

GovSim (Piatti et al., 2024) names "varying regeneration rates and multiple
resource types" directly as its own future work -- the next axis by
grounding once reputation (E18) and network reciprocity (E19) were both
built. Every existing strategy (`cooperative`, `sanctioning`, ...) is reused
completely unchanged (ADR-0016): the engine calls `decide()` once per pool
against that pool's own observation and scales the two results by each
agent's `AgentSpec.allocation_split`. The two pools are deliberately
asymmetric -- Pool A ("reliable", g=0.4) and Pool B ("fragile", g=0.2, half
the growth rate) -- so specialization is a real choice with real stakes, not
an arbitrary label between interchangeable copies.

Three questions:

A. **Does diversifying across two resources change total welfare, compared
   to concentrating on one?** Sweep `allocation_split` for an all-cooperative
   population (no free-riders, no monitors) from "pool A only" (1.0) through
   "pool B only" (0.0).
B. **Specialized vs. generalist monitors, under growing free-rider
   pressure.** Two monitors either both watch *both* pools (generalist,
   `allocation_split=0.5` each, full redundant coverage at double cost) or
   each watches exactly *one* pool (specialist: one `allocation_split=1.0`,
   one `allocation_split=0.0`, full coverage at half the cost) -- sweep the
   number of selfish free-riders filling the remaining 6 slots.
C. **Does adding a second resource change the near-optimal composition
   count?** The exact same 495 compositions E14 (population-type diversity)
   already swept, at a fixed representative `allocation_split=0.5` for every
   agent -- the composition-space analogue of Question A, and what makes this
   axis (unlike E18/E19) a genuine 4th row in `complexity-synthesis.md`'s
   count/fraction table rather than a "related but distinct" carve-out (see
   ADR-0016's Status Notes).

Outputs go to ``results/E20_multiple_resources/``. Run::

    python scripts/experiment_multiple_resources.py

Write-up: ``docs/experiments/E20-multiple-resources.md``.
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

OUT_DIR = Path(__file__).resolve().parent.parent / "results" / "E20_multiple_resources"
ROUNDS = 100
GROUP_SIZE = 8
N_MONITORS = 2
POOL_A = ResourceConfig(
    initial_level=50.0, capacity=100.0, regeneration_rate=0.4, collapse_threshold=1.0
)
POOL_B = ResourceConfig(
    initial_level=50.0, capacity=100.0, regeneration_rate=0.2, collapse_threshold=1.0
)
MSY_A = POOL_A.regeneration_rate * POOL_A.capacity / 4.0
MSY_B = POOL_B.regeneration_rate * POOL_B.capacity / 4.0
MSY_TOTAL = MSY_A + MSY_B
COOP_PARAMS = {"regeneration_rate": 0.4, "capacity": 100.0}
SANCTION_PARAMS = {"regeneration_rate": 0.4, "capacity": 100.0, "monitoring_cost": 0.2}
SELFISH_PARAMS = {"greed": 1.0}


def _welfare_efficiency(result) -> float:
    """Net payoff relative to the combined sustainable yield of both pools.

    compute_metrics() is deliberately single-pool-only (ADR-0016), so this is
    E20's own combined-pool analogue.
    """
    return sum(result.total_payoffs()) / (MSY_TOTAL * ROUNDS)


def run_split_sweep(splits=(1.0, 0.75, 0.5, 0.25, 0.0)) -> pd.DataFrame:
    """Question A: does splitting effort across both pools beat one?

    An all-cooperative population, no free-riders, no monitors.
    """
    rows = []
    for split in splits:
        agents = (AgentSpec("cooperative", GROUP_SIZE, COOP_PARAMS, allocation_split=split),)
        cfg = SimulationConfig(
            name=f"E20_split_{split}",
            rounds=ROUNDS,
            information_model="global",
            resource=POOL_A,
            second_resource=POOL_B,
            agents=agents,
        )
        result = run_simulation(cfg, seed=1)
        final = result.rounds[-1]
        rows.append(
            {
                "allocation_split": split,
                "welfare_efficiency": _welfare_efficiency(result),
                "final_level_a": final.resource_after_harvest,
                "final_level_b": final.resource_after_harvest_b,
            }
        )
    return pd.DataFrame(rows)


def _monitor_specs(arrangement: str) -> list[AgentSpec]:
    if arrangement == "generalist":
        return [AgentSpec("sanctioning", N_MONITORS, SANCTION_PARAMS, allocation_split=0.5)]
    return [
        # pool-A-only specialist
        AgentSpec("sanctioning", 1, SANCTION_PARAMS, allocation_split=1.0),
        # pool-B-only specialist
        AgentSpec("sanctioning", 1, SANCTION_PARAMS, allocation_split=0.0),
    ]


N_SELFISH_VALUES = range(7)


def run_monitor_arrangement_sweep(n_selfish_values=N_SELFISH_VALUES) -> pd.DataFrame:
    """Question B: specialized vs. generalist monitoring, as free-riders grow.

    Specialized: one monitor per pool. Generalist: every monitor watches
    every pool. Free-riders fill the remaining slots (of the 6 non-monitor
    seats).
    """
    rows = []
    for n_selfish in n_selfish_values:
        n_coop = GROUP_SIZE - N_MONITORS - n_selfish
        for arrangement in ("generalist", "specialist"):
            agents = _monitor_specs(arrangement)
            if n_coop > 0:
                agents.append(AgentSpec("cooperative", n_coop, COOP_PARAMS, allocation_split=0.5))
            if n_selfish > 0:
                agents.append(AgentSpec("selfish", n_selfish, SELFISH_PARAMS, allocation_split=0.5))
            cfg = SimulationConfig(
                name=f"E20_{arrangement}_{n_selfish}sel",
                rounds=ROUNDS,
                information_model="global",
                resource=POOL_A,
                second_resource=POOL_B,
                agents=tuple(agents),
            )
            result = run_simulation(cfg, seed=1)
            final = result.rounds[-1]
            total_monitoring_cost = sum(rec.total_penalty for rec in result.rounds)
            rows.append(
                {
                    "n_selfish": n_selfish,
                    "arrangement": arrangement,
                    "welfare_efficiency": _welfare_efficiency(result),
                    "total_monitoring_cost": total_monitoring_cost,
                    "final_level_a": final.resource_after_harvest,
                    "final_level_b": final.resource_after_harvest_b,
                    "collapsed_a": final.resource_after_harvest <= POOL_A.collapse_threshold,
                    "collapsed_b": final.resource_after_harvest_b <= POOL_B.collapse_threshold,
                }
            )
    return pd.DataFrame(rows)


# Question C: the same 495-composition sweep as E14 (population-type
# diversity), with a second resource on -- reusing E14's own five registered
# non-loner strategies and N=8 population so the two are directly comparable
# composition-for-composition, not just axis-for-axis.
COMPOSITION_TYPES = (
    "cooperative",
    "conditional_cooperator",
    "compensating_cooperator",
    "selfish",
    "sanctioning",
)
# Fixed representative split for every agent in the sweep -- matches
# CX_RESOURCE_SPLIT, the same value the web demo's "+ Resources"
# complexity-panel toggle uses, so the two stay comparable.
COMPOSITION_SPLIT = 0.5
# Same provisional threshold as E14/E15/E16, for direct comparability.
COMPOSITION_THRESHOLD = 0.80


def _composition_params(strategy: str) -> dict:
    if strategy == "selfish":
        return dict(SELFISH_PARAMS)
    p = dict(COOP_PARAMS)
    if strategy == "sanctioning":
        p["monitoring_cost"] = 0.2
    return p


def _compositions() -> list[tuple[int, ...]]:
    """Every composition of COMPOSITION_TYPES's counts summing to GROUP_SIZE.

    The identical stars-and-bars enumeration as E14's own ``_compositions()``
    (495 compositions for 5 types over 8 agents).
    """
    out = []
    for free in product(range(GROUP_SIZE + 1), repeat=len(COMPOSITION_TYPES) - 1):
        last = GROUP_SIZE - sum(free)
        if 0 <= last <= GROUP_SIZE:
            out.append((*free, last))
    return out


def run_composition_sweep() -> pd.DataFrame:
    """welfare_efficiency and diversity for every one of the 495 compositions.

    Second resource on, every agent split 0.5. compute_metrics()/
    run_experiment() are single-pool-only (ADR-0016), so
    this calls run_simulation() directly and uses _welfare_efficiency(), the
    same combined-pool metric Questions A/B above already use.
    """
    rows = []
    for composition in _compositions():
        agents = tuple(
            AgentSpec(
                strategy, count, _composition_params(strategy), allocation_split=COMPOSITION_SPLIT
            )
            for strategy, count in zip(COMPOSITION_TYPES, composition, strict=True)
            if count > 0
        )
        cfg = SimulationConfig(
            name="E20_comp",
            rounds=ROUNDS,
            information_model="global",
            resource=POOL_A,
            second_resource=POOL_B,
            agents=agents,
        )
        result = run_simulation(cfg, seed=1)
        diversity = sum(1 for c in composition if c > 0)
        rows.append({"diversity": diversity, "welfare_efficiency": _welfare_efficiency(result)})
    return pd.DataFrame(rows)


def near_optimal_by_diversity(summary: pd.DataFrame) -> pd.DataFrame:
    """For each diversity level, how many tested compositions clear the threshold.

    Count and fraction, matching E14's own ``near_optimal_by_diversity()``
    exactly so the two curves overlay.
    """
    rows = []
    for diversity in sorted(summary["diversity"].unique()):
        sub = summary[summary["diversity"] == diversity]
        passing = int((sub["welfare_efficiency"] >= COMPOSITION_THRESHOLD).sum())
        rows.append(
            {
                "diversity": diversity,
                "configs_tested": len(sub),
                "near_optimal_count": passing,
                "near_optimal_fraction": passing / len(sub),
            }
        )
    return pd.DataFrame(rows)


def make_figure(split_df: pd.DataFrame, monitor_df: pd.DataFrame, path: Path) -> None:
    """Two panels: welfare vs. allocation_split, and monitor arrangement vs. free-riders."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 4.4))

    ax1.plot(
        split_df["allocation_split"], split_df["welfare_efficiency"], marker="o", color="#2ca02c"
    )
    pool_a_alone = MSY_A * ROUNDS / (MSY_TOTAL * ROUNDS)
    ax1.axhline(pool_a_alone, color="grey", ls=":", lw=1, label="pool A alone")
    ax1.set_xlabel("allocation_split (1.0 = pool A only, 0.0 = pool B only)")
    ax1.set_ylabel("combined welfare_efficiency")
    ax1.set_title("A. Does splitting effort beat concentrating on one pool?")
    ax1.set_ylim(0, 1.05)
    ax1.legend(fontsize=8)

    for arrangement, color in [("generalist", "#1f77b4"), ("specialist", "#d62728")]:
        sub = monitor_df[monitor_df["arrangement"] == arrangement].sort_values("n_selfish")
        ax2.plot(
            sub["n_selfish"], sub["welfare_efficiency"], marker="o", color=color, label=arrangement
        )
    ax2.set_xlabel("number of selfish free-riders (of 8, 2 always monitors)")
    ax2.set_ylabel("combined welfare_efficiency")
    ax2.set_title("B. Specialized vs. generalist monitors")
    ax2.set_ylim(0, 1.05)
    ax2.legend(fontsize=8)

    fig.suptitle("E20: multiple resources -- diversifying effort, specialist vs. generalist")
    fig.tight_layout(rect=(0.0, 0.0, 1.0, 0.94))
    fig.savefig(path, dpi=130)
    plt.close(fig)


def main() -> None:
    """Run both sweeps, export tables and figure, print a summary."""
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    split_df = run_split_sweep()
    split_df.to_csv(OUT_DIR / "split_sweep.csv", index=False)
    monitor_df = run_monitor_arrangement_sweep()
    monitor_df.to_csv(OUT_DIR / "monitor_arrangement_sweep.csv", index=False)
    comp_summary = run_composition_sweep()
    comp_summary.to_csv(OUT_DIR / "composition_sweep_summary.csv", index=False)
    comp_curve = near_optimal_by_diversity(comp_summary)
    comp_curve.to_csv(OUT_DIR / "composition_sweep_curve.csv", index=False)
    make_figure(split_df, monitor_df, OUT_DIR / "figure.png")

    print("Split sweep (all-cooperative, no free-riders, no monitors):")
    print(split_df.round(3).to_string(index=False))
    print("\nMonitor arrangement sweep (welfare_efficiency, total_monitoring_cost):")
    show = monitor_df[
        ["n_selfish", "arrangement", "welfare_efficiency", "total_monitoring_cost", "collapsed_b"]
    ].round(3)
    print(show.to_string(index=False))
    print("\nComposition sweep (near-optimal count by diversity, split=0.5, both pools):")
    print(comp_curve.round(3).to_string(index=False))
    print(
        "\nWrote split_sweep.csv, monitor_arrangement_sweep.csv, composition_sweep_summary.csv, "
        f"composition_sweep_curve.csv, and figure.png to: {OUT_DIR}"
    )


if __name__ == "__main__":
    main()
