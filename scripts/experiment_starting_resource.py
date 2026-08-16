"""Experiment E17: starting resource level (R0), literal + GLUE equifinality.

Von Bertalanffy (1968) defines equifinality literally as: an open system that
reaches a *steady state* has a final value provably independent of its
initial conditions. Every experiment so far has implicitly fixed
`R0 = K/2` without ever naming that choice. This experiment tests the literal
claim directly, checks its limits, and -- kept deliberately separate, per the
literature note's own warning against blending the two senses of the term --
runs a GLUE-style composite sweep crossing R0 with E14's own composition
space, reusing the identical `welfare_efficiency >= 0.80` threshold.

Three questions:

A. **Q1 -- literal equifinality (von Bertalanffy 1968):** a fixed,
   well-behaved population (8 cooperative agents, no free-riders) swept
   across R0 from near the collapse threshold to near capacity. Does the
   final resource level converge to the same steady state regardless of R0?
B. **Q2 -- the guarantee's limits:** the identical R0 sweep, but with
   free-riders present. Does equifinality still hold once the population can
   actually drain the pool toward the R=0 absorbing state from an
   already-fragile start?
C. **Q3 -- GLUE-style composite (Beven & Binley 1992/2014):** three
   representative R0 levels crossed with the full 495-composition space E14
   already swept, reusing the same pre-declared threshold -- does the
   near-optimal set change with the starting condition?

Outputs go to ``results/E17_starting_resource/``. Run::

    python scripts/experiment_starting_resource.py

Write-up: ``docs/experiments/E17-starting-resource-level.md``.
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
from emergent_cooperation.core.simulation import run_simulation  # noqa: E402
from emergent_cooperation.experiments.runner import run_experiment  # noqa: E402

OUT_DIR = Path(__file__).resolve().parent.parent / "results" / "E17_starting_resource"
ROUNDS = 100
CAPACITY = 100.0
G = 0.4
N = 8
SEEDS = (1,)  # deterministic strategies -> exact, not a noisy mean (see E1)
R0_SWEEP = (1.0, 5.0, 20.0, 50.0, 80.0, 95.0)  # near-collapse .. near-capacity
COOP_PARAMS = {"regeneration_rate": G, "capacity": CAPACITY}
SELFISH_PARAMS = {"greed": 1.0}
THRESHOLD = 0.80  # same provisional threshold as E14-E16/E20, for comparability


def _resource(r0: float) -> ResourceConfig:
    return ResourceConfig(
        initial_level=r0, capacity=CAPACITY, regeneration_rate=G, collapse_threshold=1.0
    )


def _literal_sweep(agents: tuple[AgentSpec, ...]) -> pd.DataFrame:
    """R0-sweep for one fixed population -- shared by Q1 and Q2."""
    rows = []
    for r0 in R0_SWEEP:
        cfg = SimulationConfig(
            name=f"E17_r0_{r0}",
            rounds=ROUNDS,
            information_model="global",
            resource=_resource(r0),
            agents=agents,
        )
        result = run_simulation(cfg, seed=1)
        final = result.rounds[-1]
        rows.append(
            {
                "r0": r0,
                "final_level": final.resource_after_harvest,
                "collapsed_at_end": final.collapsed,
                "ever_collapsed": any(r.collapsed for r in result.rounds),
            }
        )
    return pd.DataFrame(rows)


def run_q1_literal_equifinality() -> pd.DataFrame:
    """8 cooperative agents, no free-riders -- does the steady state depend on R0?"""
    agents = (AgentSpec("cooperative", N, COOP_PARAMS),)
    return _literal_sweep(agents)


def run_q2_limits_with_freeriders() -> pd.DataFrame:
    """6 cooperative + 2 selfish -- same R0 sweep, does the guarantee survive?"""
    agents = (
        AgentSpec("cooperative", 6, COOP_PARAMS),
        AgentSpec("selfish", 2, SELFISH_PARAMS),
    )
    return _literal_sweep(agents)


# Q3: the identical 495-composition enumeration as E14 (scripts/experiment_population_diversity.py),
# crossed with R0 instead of held fixed at K/2.
TYPES = (
    "cooperative",
    "conditional_cooperator",
    "compensating_cooperator",
    "selfish",
    "sanctioning",
)
R0_COMPOSITE = (5.0, 50.0, 95.0)  # catastrophic / default / near-capacity


def _composition_params(strategy: str) -> dict:
    if strategy == "selfish":
        return dict(SELFISH_PARAMS)
    p = dict(COOP_PARAMS)
    if strategy == "sanctioning":
        p["monitoring_cost"] = 0.2
    return p


def _compositions() -> list[tuple[int, ...]]:
    """Every composition of TYPES's counts summing to N -- identical enumeration to E14."""
    out = []
    for free in product(range(N + 1), repeat=len(TYPES) - 1):
        last = N - sum(free)
        if 0 <= last <= N:
            out.append((*free, last))
    return out


def _q3_experiment(composition: tuple[int, ...], r0: float) -> ExperimentConfig:
    agents = [
        AgentSpec(strategy, count, _composition_params(strategy))
        for strategy, count in zip(TYPES, composition, strict=True)
        if count > 0
    ]
    sim = SimulationConfig(
        name=f"E17_q3_r0{r0}",
        rounds=ROUNDS,
        information_model="global",
        resource=_resource(r0),
        agents=tuple(agents),
    )
    return ExperimentConfig(simulation=sim, seeds=SEEDS, record_history=False)


def run_q3_composite_sweep() -> pd.DataFrame:
    """welfare_efficiency for every composition, at each of the 3 representative R0 levels."""
    rows = []
    for r0 in R0_COMPOSITE:
        for composition in _compositions():
            outcome = run_experiment(_q3_experiment(composition, r0))
            welfare = float(outcome.metrics["welfare_efficiency"].mean())
            rows.append({"r0": r0, "welfare_efficiency": welfare})
    return pd.DataFrame(rows)


def near_optimal_by_r0(summary: pd.DataFrame) -> pd.DataFrame:
    """For each R0 level, how many of the 495 compositions clear THRESHOLD."""
    rows = []
    for r0 in sorted(summary["r0"].unique()):
        sub = summary[summary["r0"] == r0]
        passing = int((sub["welfare_efficiency"] >= THRESHOLD).sum())
        rows.append(
            {
                "r0": r0,
                "configs_tested": len(sub),
                "near_optimal_count": passing,
                "near_optimal_fraction": passing / len(sub),
            }
        )
    return pd.DataFrame(rows)


def make_figure(q1: pd.DataFrame, q2: pd.DataFrame, q3_curve: pd.DataFrame, path: Path) -> None:
    """Two panels: Q1/Q2's final level vs. R0, and Q3's near-optimal fraction vs. R0."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 4.4))

    ax1.plot(q1["r0"], q1["final_level"], marker="o", color="#2ca02c", label="Q1: all-cooperative")
    ax1.plot(q2["r0"], q2["final_level"], marker="s", color="#d62728", label="Q2: + 2 free-riders")
    ax1.axhline(50.0, color="grey", ls=":", lw=1, label="R0 = K/2 (the usual default)")
    ax1.set_xlabel("R0 (starting resource level)")
    ax1.set_ylabel("final resource level (round 100)")
    ax1.set_title("A/B. Does the steady state depend on R0?")
    ax1.set_ylim(0, 100)
    ax1.legend(fontsize=8)

    ax2.plot(q3_curve["r0"], q3_curve["near_optimal_fraction"], marker="o", color="#1f77b4")
    for row in q3_curve.itertuples():
        ax2.annotate(
            f"{row.near_optimal_count}/{row.configs_tested}",
            (row.r0, row.near_optimal_fraction),
            textcoords="offset points", xytext=(0, 8), fontsize=8, ha="center",
        )
    ax2.set_xlabel("R0 (starting resource level)")
    ax2.set_ylabel("near-optimal fraction (of 495 compositions)")
    ax2.set_title("C. Does the near-optimal composition set\nchange with the starting condition?")
    ax2.set_ylim(-0.05, 1.05)

    fig.suptitle("E17: starting resource level (R0) -- literal equifinality + GLUE composite")
    fig.tight_layout(rect=(0.0, 0.0, 1.0, 0.92))
    fig.savefig(path, dpi=130)
    plt.close(fig)


def main() -> None:
    """Run all three questions, export tables and figure, print a summary."""
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    q1 = run_q1_literal_equifinality()
    q1.to_csv(OUT_DIR / "q1_literal_equifinality.csv", index=False)
    q2 = run_q2_limits_with_freeriders()
    q2.to_csv(OUT_DIR / "q2_limits_with_freeriders.csv", index=False)
    q3_summary = run_q3_composite_sweep()
    q3_summary.to_csv(OUT_DIR / "q3_composite_summary.csv", index=False)
    q3_curve = near_optimal_by_r0(q3_summary)
    q3_curve.to_csv(OUT_DIR / "q3_composite_curve.csv", index=False)
    make_figure(q1, q2, q3_curve, OUT_DIR / "figure.png")

    print("Q1 -- literal equifinality (8 cooperative, no free-riders):")
    print(q1.round(3).to_string(index=False))
    print("\nQ2 -- limits under free-riders (6 cooperative + 2 selfish):")
    print(q2.round(3).to_string(index=False))
    print("\nQ3 -- GLUE composite (near-optimal count by R0, 495 compositions each):")
    print(q3_curve.round(3).to_string(index=False))
    print(
        "\nWrote q1_literal_equifinality.csv, q2_limits_with_freeriders.csv, "
        f"q3_composite_summary.csv, q3_composite_curve.csv, and figure.png to: {OUT_DIR}"
    )


if __name__ == "__main__":
    main()
