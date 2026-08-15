"""Experiment E18: reputation (indirect reciprocity) vs. blanket retaliation.

Nowak & Sigmund (1998): cooperation can be sustained via a public reputation
score, without repeated interaction between the same two individuals --
condition your own generosity on a partner's observed reputation, not on
personal history with them or on the population's aggregate state. See
ADR-0014 for why this is implemented as a partner-*specific* trigger rather
than a population-wide one (the design that would just reproduce
conditional_cooperator's retaliation, one level of detection better).

Compares three cooperator types against a growing minority of selfish
free-riders, same structure as E2:

* ``compensating_cooperator`` (unconditional restraint -- never retaliates),
* ``conditional_cooperator`` (retaliates against the population's aggregate
  trend -- E2's finding: collapses the resource with even one free-rider), and
* ``reputation_cooperator`` (retaliates only against a randomly-assigned
  partner it happens to distrust this round -- ADR-0014).

A second sweep holds the free-rider count fixed at 1 and varies
``visibility`` (Nowak & Sigmund's `q`, the probability a partner's reputation
is actually observed) from 0 to 1, to see whether more accurate information
helps or costs the resource.

Outputs go to ``results/E18_reputation/``. Run with::

    python scripts/experiment_reputation.py

Write-up: ``docs/experiments/E18-reputation.md``.
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
    ReputationConfig,
    ResourceConfig,
    SimulationConfig,
)
from emergent_cooperation.experiments.runner import run_experiment  # noqa: E402

OUT_DIR = Path(__file__).resolve().parent.parent / "results" / "E18_reputation"
SEEDS = (1, 2, 3)
GROUP_SIZE = 8
COOP_PARAMS = {"regeneration_rate": 0.4, "capacity": 100.0}
SELFISH_PARAMS = {"greed": 1.0}
COOPERATOR_TYPES = ["compensating_cooperator", "conditional_cooperator", "reputation_cooperator"]
LABELS = {
    "compensating_cooperator": "compensating (unconditional)",
    "conditional_cooperator": "conditional (aggregate retaliation)",
    "reputation_cooperator": "reputation (partner-specific, q=1.0)",
}


def _config(cooperator_type: str, n_selfish: int, visibility: float = 1.0) -> ExperimentConfig:
    """A group of GROUP_SIZE agents: n_selfish selfish, the rest cooperators."""
    n_coop = GROUP_SIZE - n_selfish
    agents = []
    if n_coop > 0:
        agents.append(AgentSpec(cooperator_type, count=n_coop, params=dict(COOP_PARAMS)))
    if n_selfish > 0:
        agents.append(AgentSpec("selfish", count=n_selfish, params=dict(SELFISH_PARAMS)))
    reputation = ReputationConfig(visibility=visibility) if cooperator_type == "reputation_cooperator" else None
    sim = SimulationConfig(
        name=f"E18_{cooperator_type}_{n_selfish}sel",
        rounds=100,
        information_model="global",
        resource=ResourceConfig(
            initial_level=50.0, capacity=100.0, regeneration_rate=0.4, collapse_threshold=1.0
        ),
        agents=tuple(agents),
        reputation=reputation,
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
    for cooperator_type in COOPERATOR_TYPES:
        for n_selfish in range(GROUP_SIZE + 1):
            outcome = run_experiment(_config(cooperator_type, n_selfish))
            m = outcome.metrics
            payoffs = _payoff_by_strategy(outcome.results)
            rows.append(
                {
                    "cooperator_type": cooperator_type,
                    "n_selfish": n_selfish,
                    "sustainability_ratio": m["sustainability_ratio"].mean(),
                    "welfare_efficiency": m["welfare_efficiency"].mean(),
                    "collapsed": m["collapsed"].mean(),
                    "selfish_payoff": payoffs.get("selfish", float("nan")),
                }
            )
    return pd.DataFrame(rows)


def run_visibility_sweep(n_selfish: int = 1, visibilities=(0.0, 0.2, 0.4, 0.6, 0.8, 1.0)) -> pd.DataFrame:
    """At a fixed 1-free-rider population, how does q (visibility) change the outcome?"""
    rows = []
    for q in visibilities:
        outcome = run_experiment(_config("reputation_cooperator", n_selfish, visibility=q))
        m = outcome.metrics
        rows.append(
            {
                "visibility": q,
                "sustainability_ratio": m["sustainability_ratio"].mean(),
                "welfare_efficiency": m["welfare_efficiency"].mean(),
                "collapsed": m["collapsed"].mean(),
            }
        )
    return pd.DataFrame(rows)


def make_figure(df: pd.DataFrame, vis_df: pd.DataFrame, path: Path) -> None:
    """Three panels: resource survival by cooperator type, free-rider earnings, and the visibility sweep."""
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15.5, 4.2))

    for ctype in COOPERATOR_TYPES:
        sub = df[df["cooperator_type"] == ctype].sort_values("n_selfish")
        ax1.plot(sub["n_selfish"], sub["sustainability_ratio"], marker="o", label=LABELS[ctype])
    ax1.set_xlabel("number of selfish agents (of 8)")
    ax1.set_ylabel("sustainability ratio (final stock / K)")
    ax1.set_title("A. Does the resource survive?")
    ax1.set_ylim(-0.02, 0.6)
    ax1.legend(fontsize=8)

    for ctype in COOPERATOR_TYPES:
        sub = df[(df["cooperator_type"] == ctype) & (df["n_selfish"].between(1, 7))].sort_values("n_selfish")
        ax2.plot(sub["n_selfish"], sub["selfish_payoff"], marker="s", label=LABELS[ctype])
    ax2.set_xlabel("number of selfish agents (of 8)")
    ax2.set_ylabel("mean payoff of a selfish free-rider")
    ax2.set_title("B. How much do free-riders earn?")
    ax2.legend(fontsize=8)

    ax3.plot(vis_df["visibility"], vis_df["sustainability_ratio"], marker="o", color="#17becf")
    ax3.set_xlabel("reputation visibility (q)")
    ax3.set_ylabel("sustainability ratio")
    ax3.set_title("C. 1 free-rider: does more\naccurate detection help?")
    ax3.set_ylim(-0.02, 0.6)

    fig.suptitle("E18: reputation (partner-specific) vs. blanket retaliation vs. unconditional restraint")
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)


def main() -> None:
    """Run both sweeps, export the tables and figure, and print a summary."""
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    df = run_sweep()
    df.to_csv(OUT_DIR / "sweep.csv", index=False)
    vis_df = run_visibility_sweep()
    vis_df.to_csv(OUT_DIR / "visibility_sweep.csv", index=False)
    make_figure(df, vis_df, OUT_DIR / "figure.png")

    show = df[["cooperator_type", "n_selfish", "sustainability_ratio", "welfare_efficiency", "selfish_payoff"]].round(3)
    print(show.to_string(index=False))
    print("\nVisibility sweep (1 free-rider):")
    print(vis_df.round(3).to_string(index=False))
    print(f"\nWrote sweep.csv, visibility_sweep.csv, and figure.png to: {OUT_DIR}")


if __name__ == "__main__":
    main()
