"""Experiment E8: resilience to a resource shock — information vs. enforcement.

Every earlier experiment studied the *calm* commons. This one disturbs it: a
homogeneous cooperative population runs to its steady state (stock held at K/2),
then a **resource shock** removes 70% of the stock at round 60, and we measure
whether — and how fast — the resource recovers.

The manipulated factors:

* **Information** — ``global`` (agents observe the stock) vs. ``private`` (blind).
* **Enforcement** — plain ``cooperative`` vs. ``sanctioning`` (a policed quota).

The non-obvious result: in calm conditions all four conditions look identical
(the stock sits at K/2). Under the shock they split cleanly by **information, not
enforcement**. Agents that can *see* the stock harvest nothing while it is
depleted and let it regrow (recovery in a handful of rounds); blind agents keep
taking the steady-state quota out of a shrunken pool and drive it to collapse.
Enforcement does not help — the sanctioning quota is a ceiling on over-extraction,
not a floor that forces restraint, so it cannot fix a blind harvest rule.

A no-shock control confirms every condition is stable *without* the disturbance —
so the collapse is a fragility exposed by the shock, not a pre-existing failure.

Outputs go to ``results/E8_resilience/``. Run with::

    python scripts/experiment_resilience.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from emergent_cooperation.core.config import (  # noqa: E402
    AgentSpec,
    DisturbanceConfig,
    ExperimentConfig,
    ResourceConfig,
    SimulationConfig,
)
from emergent_cooperation.experiments.runner import run_experiment  # noqa: E402

OUT_DIR = Path(__file__).resolve().parent.parent / "results" / "E8_resilience"
SEEDS = tuple(range(1, 21))  # 20 seeds
NOISE = 0.1
ROUNDS = 120
SHOCK_ROUND = 60
SHOCK_MAGNITUDE = 0.7  # remove 70% of the stock
CAPACITY = 100.0
G = 0.4
N = 8

# (strategy, information_model) conditions, in plot order.
CONDITIONS = [
    ("cooperative", "global"),
    ("sanctioning", "global"),
    ("cooperative", "private"),
    ("sanctioning", "private"),
]
STRAT_LABEL = {"cooperative": "cooperative", "sanctioning": "sanctioning"}
# Colour-blind-safe (Okabe-Ito): blue = can observe, vermillion = blind.
INFO_COLOR = {"global": "#1f77b4", "private": "#d55e00"}
STRAT_STYLE = {"cooperative": "-", "sanctioning": "--"}


def _params(strategy: str) -> dict:
    p = {"regeneration_rate": G, "capacity": CAPACITY}
    if strategy == "sanctioning":
        p["monitoring_cost"] = 0.2
    return p


def _experiment(strategy: str, info: str, *, shock: bool) -> ExperimentConfig:
    disturbances = (
        (DisturbanceConfig("resource_shock", round=SHOCK_ROUND, magnitude=SHOCK_MAGNITUDE),)
        if shock
        else ()
    )
    sim = SimulationConfig(
        name=f"E8_{strategy}_{info}_{'shock' if shock else 'calm'}",
        rounds=ROUNDS,
        information_model=info,
        decision_noise=NOISE,
        resource=ResourceConfig(
            initial_level=CAPACITY / 2,
            capacity=CAPACITY,
            regeneration_rate=G,
            collapse_threshold=1.0,
        ),
        agents=(AgentSpec(strategy, N, _params(strategy)),),
        disturbances=disturbances,
    )
    return ExperimentConfig(simulation=sim, seeds=SEEDS, record_history=False)


def _mean_trajectory(strategy: str, info: str) -> np.ndarray:
    """Mean resource-after-harvest per round across seeds, for the shock condition."""
    outcome = run_experiment(_experiment(strategy, info, shock=True))
    stacked = np.array(
        [[r.resource_after_harvest for r in result.rounds] for result in outcome.results]
    )
    return stacked.mean(axis=0)


def summarise() -> pd.DataFrame:
    """Recovery statistics per condition, with and without the shock."""
    rows = []
    for strategy, info in CONDITIONS:
        for shock in (True, False):
            metrics = run_experiment(_experiment(strategy, info, shock=shock)).metrics
            recovered = metrics["recovered"]
            rec_time = metrics["recovery_time"].dropna()
            rows.append(
                {
                    "strategy": strategy,
                    "information": info,
                    "shock": shock,
                    "recovered_rate": float(recovered.mean()),
                    "mean_recovery_time": float(rec_time.mean()) if len(rec_time) else np.nan,
                    "final_sustainability": float(metrics["sustainability_ratio"].mean()),
                }
            )
    return pd.DataFrame(rows)


def make_figure(summary: pd.DataFrame, path: Path) -> None:
    """Two panels: mean stock trajectories through the shock, and recovered-rate bars."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 4.6))

    # Panel A: trajectories through the shock.
    for strategy, info in CONDITIONS:
        traj = _mean_trajectory(strategy, info)
        ax1.plot(
            range(len(traj)),
            traj,
            color=INFO_COLOR[info],
            linestyle=STRAT_STYLE[strategy],
            lw=2,
            label=f"{STRAT_LABEL[strategy]} · {info}",
        )
    ax1.axvline(SHOCK_ROUND, color="grey", ls=":", lw=1)
    ax1.text(SHOCK_ROUND + 1, 92, f"−{int(SHOCK_MAGNITUDE * 100)}% shock", color="grey", fontsize=9)
    ax1.axhline(CAPACITY / 2, color="grey", ls=":", lw=0.8)
    ax1.set_xlabel("round")
    ax1.set_ylabel("resource stock (mean over seeds)")
    ax1.set_ylim(-2, 100)
    ax1.set_title("A. Recovery from a 70% resource shock\n(blue = can observe stock, red = blind)")
    ax1.legend(loc="center left", fontsize=8)

    # Panel B: recovered rate under the shock, by condition.
    shocked = summary[summary["shock"]].copy()
    labels = [
        f"{STRAT_LABEL[s]}\n{i}"
        for s, i in zip(shocked["strategy"], shocked["information"], strict=True)
    ]
    colors = [INFO_COLOR[i] for i in shocked["information"]]
    ax2.bar(labels, shocked["recovered_rate"], color=colors)
    ax2.set_ylabel("fraction of runs that recovered")
    ax2.set_ylim(0, 1.05)
    ax2.set_title("B. Recovery splits by information, not enforcement")
    for x, v in enumerate(shocked["recovered_rate"]):
        ax2.text(x, v + 0.02, f"{v:.0%}", ha="center", fontsize=9)

    fig.suptitle(
        "E8: information, not enforcement, decides whether cooperation survives a shock"
    )
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)


def main() -> None:
    """Run all conditions, export the summary CSV + figure, print the headline."""
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    summary = summarise()
    summary.to_csv(OUT_DIR / "summary.csv", index=False)
    make_figure(summary, OUT_DIR / "figure.png")

    print("E8 resilience — recovered rate (final sustainability) after a 70% shock:")
    shocked = summary[summary["shock"]]
    for _, row in shocked.iterrows():
        print(
            f"  {row['strategy']:12s} {row['information']:7s}: "
            f"recovered {row['recovered_rate']:.0%}, "
            f"final stock {row['final_sustainability']:.2f}·K"
        )
    calm = summary[~summary["shock"]]
    print(
        "\nNo-shock control: all conditions stable "
        f"(min final sustainability = {calm['final_sustainability'].min():.2f}·K)."
    )
    print(f"\nWrote summary.csv and figure.png to: {OUT_DIR}")


if __name__ == "__main__":
    main()
