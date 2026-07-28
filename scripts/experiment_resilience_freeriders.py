"""Experiment E9: resilience with free-riders — does enforcement matter under a shock?

E8 shocked *homogeneous* cooperative populations and found recovery is decided by
**information** (observing agents self-correct and recover; blind ones collapse), and
that enforcement was irrelevant there. This experiment adds **free-riders** and asks
the complementary question: once selfish agents are present, does enforcement provide
shock-resilience that plain cooperation lacks?

Setup (global information throughout, so this isolates the free-rider effect from the
information effect of E8): a group of 8 agents = `(8 − s)` cooperators (plain
`cooperative`, or `sanctioning` for the enforced regime) plus `s` selfish free-riders.
A 70% resource shock hits at round 60; a no-shock control runs alongside. `s` is swept
0…4, 20 seeds, `decision_noise = 0.1`.

The result:

* **Enforcement recovers at every free-rider count.** Sanctioning returns the stock to
  ~0.5·K after the shock for all `s` — the quota caps free-riders during the fragile
  low-stock recovery window.
* **Plain cooperation recovers only as far as its free-rider tolerance.** Because
  greedy extraction scales *down* with the depleted stock, observing cooperators *do*
  climb back from the shock (E8) — but only to the level free-riders have already
  dragged them to, which collapses past ~1 free-rider. The shock adds little; the
  free-riders are the killer.

Headline: **information lets a commons recover from a shock (E8); enforcement decides
how many free-riders it can survive while doing so (E9). Resilience needs both.**

Outputs go to ``results/E9_resilience_freeriders/``. Run with::

    python scripts/experiment_resilience_freeriders.py
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

OUT_DIR = Path(__file__).resolve().parent.parent / "results" / "E9_resilience_freeriders"
SEEDS = tuple(range(1, 21))
NOISE = 0.1
ROUNDS = 120
SHOCK_ROUND = 60
SHOCK_MAGNITUDE = 0.7
CAPACITY = 100.0
G = 0.4
N = 8
FREE_RIDERS = [0, 1, 2, 3, 4]

REGIMES = {"cooperative": "cooperation (no enforcement)", "sanctioning": "enforcement"}
REGIME_COLOR = {"cooperative": "#d55e00", "sanctioning": "#1f77b4"}


def _params(strategy: str) -> dict:
    p = {"regeneration_rate": G, "capacity": CAPACITY}
    if strategy == "sanctioning":
        p["monitoring_cost"] = 0.2
    return p


def _experiment(strategy: str, s: int, *, shock: bool) -> ExperimentConfig:
    agents = []
    if N - s > 0:
        agents.append(AgentSpec(strategy, N - s, _params(strategy)))
    if s > 0:
        agents.append(AgentSpec("selfish", s, {"greed": 1.0}))
    disturbances = (
        (DisturbanceConfig("resource_shock", round=SHOCK_ROUND, magnitude=SHOCK_MAGNITUDE),)
        if shock
        else ()
    )
    sim = SimulationConfig(
        name=f"E9_{strategy}_s{s}_{'shock' if shock else 'calm'}",
        rounds=ROUNDS,
        information_model="global",
        decision_noise=NOISE,
        resource=ResourceConfig(
            initial_level=CAPACITY / 2,
            capacity=CAPACITY,
            regeneration_rate=G,
            collapse_threshold=1.0,
        ),
        agents=tuple(agents),
        disturbances=disturbances,
    )
    return ExperimentConfig(simulation=sim, seeds=SEEDS, record_history=False)


def summarise() -> pd.DataFrame:
    """Final sustainability and recovered rate per (regime, free-riders, shock)."""
    rows = []
    for strategy in REGIMES:
        for s in FREE_RIDERS:
            for shock in (True, False):
                metrics = run_experiment(_experiment(strategy, s, shock=shock)).metrics
                rows.append(
                    {
                        "regime": strategy,
                        "free_riders": s,
                        "shock": shock,
                        "final_sustainability": float(metrics["sustainability_ratio"].mean()),
                        "recovered_rate": float(metrics["recovered"].mean()),
                    }
                )
    return pd.DataFrame(rows)


def _mean_trajectory(strategy: str, s: int) -> np.ndarray:
    outcome = run_experiment(_experiment(strategy, s, shock=True))
    stacked = np.array(
        [[r.resource_after_harvest for r in result.rounds] for result in outcome.results]
    )
    return stacked.mean(axis=0)


def make_figure(summary: pd.DataFrame, path: Path, *, traj_s: int = 2) -> None:
    """Panel A: final stock vs free-riders (shock vs calm). Panel B: trajectories at s=2."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 4.6))

    for strategy in REGIMES:
        for shock in (True, False):
            sub = summary[
                (summary["regime"] == strategy) & (summary["shock"] == shock)
            ].sort_values("free_riders")
            ax1.plot(
                sub["free_riders"],
                sub["final_sustainability"],
                marker="o",
                color=REGIME_COLOR[strategy],
                linestyle="-" if shock else ":",
                lw=2 if shock else 1.3,
                alpha=1.0 if shock else 0.5,
                label=f"{REGIMES[strategy]} · {'shock' if shock else 'calm'}",
            )
    ax1.set_xlabel("number of selfish free-riders (of 8)")
    ax1.set_ylabel("final resource (fraction of K)")
    ax1.set_ylim(-0.02, 0.62)
    ax1.set_xticks(FREE_RIDERS)
    ax1.set_title(
        "A. Enforcement stays resilient across free-riders\n(solid = shock, dotted = calm)"
    )
    ax1.legend(fontsize=8)

    for strategy in REGIMES:
        traj = _mean_trajectory(strategy, traj_s)
        ax2.plot(
            range(len(traj)),
            traj,
            color=REGIME_COLOR[strategy],
            lw=2,
            label=REGIMES[strategy],
        )
    ax2.axvline(SHOCK_ROUND, color="grey", ls=":", lw=1)
    ax2.text(SHOCK_ROUND + 1, 92, f"−{int(SHOCK_MAGNITUDE * 100)}% shock", color="grey", fontsize=9)
    ax2.axhline(CAPACITY / 2, color="grey", ls=":", lw=0.8)
    ax2.set_xlabel("round")
    ax2.set_ylabel("resource stock (mean over seeds)")
    ax2.set_ylim(-2, 100)
    ax2.set_title(
        f"B. Recovery with {traj_s} free-riders\n"
        "enforcement returns to K/2; cooperation does not"
    )
    ax2.legend(loc="center left", fontsize=8)

    fig.suptitle(
        "E9: with free-riders, enforcement — not observation alone — "
        "restores the commons after a shock"
    )
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)


def main() -> None:
    """Run the grid, export the summary CSV + figure, print the headline."""
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    summary = summarise()
    summary.to_csv(OUT_DIR / "summary.csv", index=False)
    make_figure(summary, OUT_DIR / "figure.png")

    print("E9 — final resource (fraction of K) after a 70% shock, by free-rider count:")
    shocked = summary[summary["shock"]]
    for strategy in REGIMES:
        sub = shocked[shocked["regime"] == strategy].sort_values("free_riders")
        cells = "  ".join(
            f"s={int(r.free_riders)}:{r.final_sustainability:.2f}" for r in sub.itertuples()
        )
        print(f"  {REGIMES[strategy]:26s}: {cells}")
    print(f"\nWrote summary.csv and figure.png to: {OUT_DIR}")


if __name__ == "__main__":
    main()
