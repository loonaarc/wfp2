"""Experiment E6: can communication substitute for missing information?

E1 showed cooperation needs information (or knowledge). Communication is a way to
*acquire* information. Here, under **private** information (agents cannot see the
stock), we switch on a broadcast channel (ADR-0007): each round an agent hears the
group's total harvest with probability `broadcast_reliability`. A conditional
cooperator uses that signal to detect over-extraction it otherwise could not see.

We sweep the broadcast reliability (0 = silence, 1 = perfect) for a private-info
population of conditional cooperators + selfish free-riders, and compare against the
global-information reference. Addresses SQ-6 (does communication help), SQ-7 (message
loss / reliability), SQ-8 (can communication fail to help / harm).

Outputs go to ``results/E6_communication/``. Run with::

    python scripts/experiment_communication.py

Write-up: ``docs/experiments/E6-communication.md``.
"""

from __future__ import annotations

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

OUT_DIR = Path(__file__).resolve().parent.parent / "results" / "E6_communication"
SEEDS = tuple(range(1, 21))
N_SELFISH = 2
RELIABILITIES = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]


def _experiment(information_model, reliability):
    sim = SimulationConfig(
        name=f"E6_{information_model}_r{reliability}",
        rounds=100,
        information_model=information_model,
        broadcast_reliability=reliability,
        resource=ResourceConfig(
            initial_level=50.0, capacity=100.0, regeneration_rate=0.4, collapse_threshold=1.0
        ),
        agents=(
            AgentSpec("conditional_cooperator", 8 - N_SELFISH, {"capacity": 100.0}),
            AgentSpec("selfish", N_SELFISH, {"greed": 1.0}),
        ),
    )
    return ExperimentConfig(simulation=sim, seeds=SEEDS, record_history=False)


def run_sweep() -> pd.DataFrame:
    """Private info: sweep broadcast reliability; record fairness and sustainability."""
    rows = []
    for r in RELIABILITIES:
        m = run_experiment(_experiment("private", r)).metrics
        rows.append(
            {
                "reliability": r,
                "gini_mean": m["payoff_gini"].mean(),
                "gini_std": m["payoff_gini"].std(),
                "sustain_mean": m["sustainability_ratio"].mean(),
            }
        )
    return pd.DataFrame(rows)


def references() -> dict[str, float]:
    """Global-info and private-no-comms reference points (mean Gini)."""
    g = run_experiment(_experiment("global", 0.0)).metrics["payoff_gini"].mean()
    p = run_experiment(_experiment("private", 0.0)).metrics["payoff_gini"].mean()
    return {"global": g, "private_silent": p}


def make_figure(df: pd.DataFrame, ref: dict[str, float], path: Path) -> None:
    """Two panels: fairness vs reliability (with references), and sustainability."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.4))

    ax1.plot(
        df["reliability"],
        df["gini_mean"],
        marker="o",
        color="tab:purple",
        label="private + broadcast",
    )
    ax1.fill_between(
        df["reliability"],
        df["gini_mean"] - df["gini_std"],
        df["gini_mean"] + df["gini_std"],
        alpha=0.2,
        color="tab:purple",
    )
    ax1.axhline(ref["global"], color="tab:blue", ls="--", label="global info (reference)")
    ax1.set_xlabel("broadcast reliability (1 = no message loss)")
    ax1.set_ylabel("payoff Gini (lower = fairer)")
    ax1.set_title("A. Communication reduces exploitation\n(substitutes for observation)")
    ax1.set_ylim(0, 0.6)
    ax1.legend()

    ax2.plot(df["reliability"], df["sustain_mean"], marker="s", color="tab:red")
    ax2.set_xlabel("broadcast reliability")
    ax2.set_ylabel("sustainability ratio")
    ax2.set_title("B. ...but does not save the resource\n(reciprocity still collapses it)")
    ax2.set_ylim(-0.02, 0.6)

    fig.suptitle(
        "E6: communication substitutes for information — but its value depends on the response"
    )
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)


def main() -> None:
    """Run the reliability sweep, export CSV + figure, and print a summary."""
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    df = run_sweep()
    ref = references()
    df.to_csv(OUT_DIR / "sweep.csv", index=False)
    make_figure(df, ref, OUT_DIR / "figure.png")

    print(
        f"References: global Gini={ref['global']:.3f}, "
        f"private-silent Gini={ref['private_silent']:.3f}"
    )
    print("\nPrivate info, broadcast reliability sweep:")
    print(df.round(3).to_string(index=False))
    print(f"\nWrote sweep.csv and figure.png to: {OUT_DIR}")


if __name__ == "__main__":
    main()
