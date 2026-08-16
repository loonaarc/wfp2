"""Experiment E23: a wealth-based participation floor, and why it backfires.

Chen & Szolnoki (2016): gating participation in a public-goods round on
accumulated wealth self-corrects on a spatial lattice -- sustained defection
erodes a defector's own local resource base, so the gate disproportionately
excludes defectors, not cooperators. This project's engine has a single,
globally shared pool, not a spatial lattice. Two questions test whether the
mechanism transfers anyway, checked directly before this script was written
(see ADR-0019):

A. **Wealth gate alone.** Cooperative agents + a growing number of selfish
   free-riders, no monitor. Does a wealth floor (relative to the
   population's own average payoff) protect the pool by excluding the
   free-rider, or does it end up excluding the exploited cooperative
   majority instead?
B. **Wealth gate + sanctioning.** The same sweep, with two monitors added.
   Sanctioning's quota already equalizes harvest across non-monitor agents
   -- does the wealth gate then complement enforcement, or does it end up
   excluding the monitors themselves (who pay `monitoring_cost` and can run
   a net-negative payoff)?

Outputs go to ``results/E23_wealth_participation/``. Run::

    python scripts/experiment_wealth_participation.py

Write-up: ``docs/experiments/E23-wealth-based-participation.md``.
"""

from __future__ import annotations

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

OUT_DIR = Path(__file__).resolve().parent.parent / "results" / "E23_wealth_participation"
ROUNDS = 100
CAPACITY = 100.0
G = 0.4
MSY = G * CAPACITY / 4.0
COOP_PARAMS = {"regeneration_rate": G, "capacity": CAPACITY}
SELFISH_PARAMS = {"greed": 1.0}
SANCTION_PARAMS = {"regeneration_rate": G, "capacity": CAPACITY, "monitoring_cost": 0.2}
WEALTH_FLOOR = 0.9  # aggressive on purpose -- see ADR-0019 for why even this
N_SELFISH_VALUES = range(7)


def _resource() -> ResourceConfig:
    return ResourceConfig(
        initial_level=50.0, capacity=CAPACITY, regeneration_rate=G, collapse_threshold=1.0
    )


def _welfare(result) -> float:
    return sum(result.total_payoffs()) / (MSY * ROUNDS)


def run_q1_gate_alone(n_selfish_values=N_SELFISH_VALUES) -> pd.DataFrame:
    """No monitor -- does the gate protect the pool, or exclude cooperators?"""
    rows = []
    for n_selfish in n_selfish_values:
        agents = [AgentSpec("cooperative", 8 - n_selfish, COOP_PARAMS)]
        if n_selfish > 0:
            agents.append(AgentSpec("selfish", n_selfish, SELFISH_PARAMS))
        for wealth_floor in (None, WEALTH_FLOOR):
            cfg = SimulationConfig(
                name=f"E23_q1_{n_selfish}_{wealth_floor}",
                rounds=ROUNDS,
                information_model="global",
                resource=_resource(),
                agents=tuple(agents),
                wealth_floor_fraction=wealth_floor,
            )
            result = run_simulation(cfg, seed=1)
            final = result.rounds[-1]
            freerider_still_active = n_selfish > 0 and final.requested[-1] > 1e-6
            rows.append(
                {
                    "n_selfish": n_selfish,
                    "wealth_gate": wealth_floor is not None,
                    "welfare_efficiency": _welfare(result),
                    "final_level": final.resource_after_harvest,
                    "freerider_still_active": freerider_still_active,
                }
            )
    return pd.DataFrame(rows)


def run_q2_gate_with_sanctioning(n_selfish_values=N_SELFISH_VALUES) -> pd.DataFrame:
    """Two monitors -- does the gate complement enforcement, or exclude the monitors?"""
    rows = []
    for n_selfish in n_selfish_values:
        n_coop = 8 - 2 - n_selfish
        agents = [AgentSpec("sanctioning", 2, SANCTION_PARAMS)]
        if n_coop > 0:
            agents.append(AgentSpec("cooperative", n_coop, COOP_PARAMS))
        if n_selfish > 0:
            agents.append(AgentSpec("selfish", n_selfish, SELFISH_PARAMS))
        for wealth_floor in (None, WEALTH_FLOOR):
            cfg = SimulationConfig(
                name=f"E23_q2_{n_selfish}_{wealth_floor}",
                rounds=ROUNDS,
                information_model="global",
                resource=_resource(),
                agents=tuple(agents),
                wealth_floor_fraction=wealth_floor,
            )
            result = run_simulation(cfg, seed=1)
            final = result.rounds[-1]
            monitors_still_active = final.requested[0] > 1e-6 or final.requested[1] > 1e-6
            rows.append(
                {
                    "n_selfish": n_selfish,
                    "wealth_gate": wealth_floor is not None,
                    "welfare_efficiency": _welfare(result),
                    "final_level": final.resource_after_harvest,
                    "monitors_still_active": monitors_still_active,
                }
            )
    return pd.DataFrame(rows)


def make_figure(q1: pd.DataFrame, q2: pd.DataFrame, path: Path) -> None:
    """Two panels: welfare with/without the gate, alone and with sanctioning."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 4.4))

    gate_styles = [(False, "#1f77b4", "no wealth gate"), (True, "#d62728", "wealth gate")]
    for gate, color, label in gate_styles:
        sub = q1[q1["wealth_gate"] == gate].sort_values("n_selfish")
        ax1.plot(sub["n_selfish"], sub["welfare_efficiency"], marker="o", color=color, label=label)
    ax1.set_xlabel("number of selfish free-riders (of 8)")
    ax1.set_ylabel("welfare_efficiency")
    ax1.set_title("A. Gate alone -- does it protect\nthe pool, or hurt it?")
    ax1.set_ylim(0, 1.05)
    ax1.legend(fontsize=8)

    for gate, color, label in gate_styles:
        sub = q2[q2["wealth_gate"] == gate].sort_values("n_selfish")
        ax2.plot(sub["n_selfish"], sub["welfare_efficiency"], marker="o", color=color, label=label)
    ax2.set_xlabel("number of selfish free-riders (2 of 8 always monitors)")
    ax2.set_ylabel("welfare_efficiency")
    ax2.set_title("B. Gate + sanctioning -- complement\nor undermine enforcement?")
    ax2.set_ylim(0, 1.05)
    ax2.legend(fontsize=8)

    fig.suptitle("E23: wealth-based participation floor -- does it transfer to a shared pool?")
    fig.tight_layout(rect=(0.0, 0.0, 1.0, 0.92))
    fig.savefig(path, dpi=130)
    plt.close(fig)


def main() -> None:
    """Run both questions, export tables and figure, print a summary."""
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    q1 = run_q1_gate_alone()
    q1.to_csv(OUT_DIR / "q1_gate_alone.csv", index=False)
    q2 = run_q2_gate_with_sanctioning()
    q2.to_csv(OUT_DIR / "q2_gate_with_sanctioning.csv", index=False)
    make_figure(q1, q2, OUT_DIR / "figure.png")

    print("Q1 -- wealth gate alone (no monitor):")
    print(q1.round(3).to_string(index=False))
    print("\nQ2 -- wealth gate + sanctioning:")
    print(q2.round(3).to_string(index=False))
    print(f"\nWrote q1_gate_alone.csv, q2_gate_with_sanctioning.csv, and figure.png to: {OUT_DIR}")


if __name__ == "__main__":
    main()
