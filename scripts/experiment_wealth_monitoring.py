"""Experiment E22: wealth-triggered voluntary monitoring (Olson 1965).

Olson (1965), *The Logic of Collective Action*: a group member has an
individual incentive to unilaterally provide a collective good exactly when
its own share of the group's benefit clears the good's cost relative to its
total value (`F_i > C/V_g`, p. 33) -- and, where members are unequal in size,
the largest member ends up bearing a disproportionate share of the burden
("exploitation of the great by the small," p. 29). E22 operationalizes `F_i`
as an agent's own accumulated ``total_payoff`` relative to the population's
current average: the single wealthiest agent with no intrinsic sanction
policy volunteers as monitor each round its wealth clears the threshold (see
ADR-0020). Two questions, both checked directly against the engine before
this script was written:

A. **Does it emerge and protect the commons with zero designated monitors?**
   Sweeping the free-rider count: no. A free-rider's own dominant payoff (E2's
   standing finding) inflates the population average so far above any single
   cooperator's own wealth that the mechanism never engages once a free-rider
   is present -- structurally inert in exactly the population it would need
   to protect.
B. **Exploitation of the great by the small, without a free-rider present.**
   In an all-cooperative population, ``decision_noise`` is the only source
   of wealth divergence (deterministic strategies never organically diverge).
   Does the mechanism engage, does it concentrate disproportionately on a
   small subset rather than rotating uniformly, and does it mildly reduce
   payoff inequality by taxing whoever is currently ahead?

Outputs go to ``results/E22_wealth_monitoring/``. Run::

    python scripts/experiment_wealth_monitoring.py

Write-up: ``docs/experiments/E22-wealth-triggered-monitoring.md``.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

from emergent_cooperation.core.config import (  # noqa: E402
    AgentSpec,
    ResourceConfig,
    SimulationConfig,
    WealthMonitoringConfig,
)
from emergent_cooperation.core.simulation import run_simulation  # noqa: E402

OUT_DIR = Path(__file__).resolve().parent.parent / "results" / "E22_wealth_monitoring"
ROUNDS = 100
CAPACITY = 100.0
G = 0.4
MSY = G * CAPACITY / 4.0
NOISE = 0.15  # the only source of organic wealth divergence -- see module docstring
THRESHOLD = 1.02
MONITORING_COST = 0.2
COOP_PARAMS = {"regeneration_rate": G, "capacity": CAPACITY}
SELFISH_PARAMS = {"greed": 1.0}
N_SELFISH_VALUES = range(8)
N_SEEDS_Q2 = 50
THRESHOLD_VALUES = (1.005, 1.01, 1.02, 1.05, 1.1, 1.2)


def _resource() -> ResourceConfig:
    return ResourceConfig(
        initial_level=50.0, capacity=CAPACITY, regeneration_rate=G, collapse_threshold=1.0
    )


def _welfare(result) -> float:
    return sum(result.total_payoffs()) / (MSY * ROUNDS)


def _gini(values: list[float]) -> float:
    x = np.sort(np.array(values, dtype=float))
    n = len(x)
    cum = np.cumsum(x)
    if cum[-1] == 0:
        return 0.0
    return float((n + 1 - 2 * np.sum(cum) / cum[-1]) / n)


def run_q1_freerider_sweep(n_selfish_values=N_SELFISH_VALUES) -> pd.DataFrame:
    """Does wealth-triggered monitoring emerge and protect the pool as free-riders grow?"""
    rows = []
    for n_selfish in n_selfish_values:
        n_coop = 8 - n_selfish
        agents = []
        if n_coop > 0:
            agents.append(AgentSpec("cooperative", n_coop, COOP_PARAMS))
        if n_selfish > 0:
            agents.append(AgentSpec("selfish", n_selfish, SELFISH_PARAMS))
        wm_on = WealthMonitoringConfig(threshold=THRESHOLD, monitoring_cost=MONITORING_COST)
        for wm in (None, wm_on):
            cfg = SimulationConfig(
                name=f"E22_q1_{n_selfish}_{wm is not None}",
                rounds=ROUNDS,
                information_model="global",
                decision_noise=NOISE,
                resource=_resource(),
                agents=tuple(agents),
                wealth_monitoring=wm,
            )
            result = run_simulation(cfg, seed=1)
            total_penalty = sum(sum(r.penalties) for r in result.rounds)
            rows.append(
                {
                    "n_selfish": n_selfish,
                    "wealth_monitoring": wm is not None,
                    "welfare_efficiency": _welfare(result),
                    "total_wealth_penalty": total_penalty,
                    "final_level": result.rounds[-1].resource_after_harvest,
                }
            )
    return pd.DataFrame(rows)


def run_q2_exploitation_dynamics(n_seeds=N_SEEDS_Q2) -> pd.DataFrame:
    """All-cooperative, noise-only divergence: does burden concentrate, and shrink inequality?"""
    agents = (AgentSpec("cooperative", 8, COOP_PARAMS),)
    rows = []
    for seed in range(1, n_seeds + 1):

        def _run(wm, seed=seed):
            cfg = SimulationConfig(
                name=f"E22_q2_{seed}_{wm is not None}",
                rounds=ROUNDS,
                information_model="global",
                decision_noise=NOISE,
                resource=_resource(),
                agents=agents,
                wealth_monitoring=wm,
            )
            return run_simulation(cfg, seed=seed)

        off = _run(None)
        on = _run(WealthMonitoringConfig(threshold=THRESHOLD, monitoring_cost=MONITORING_COST))
        total_penalty = sum(sum(r.penalties) for r in on.rounds)
        per_agent_penalty = [sum(r.penalties[i] for r in on.rounds) for i in range(8)]
        engaged = total_penalty > 0
        top_payer = int(np.argmax(per_agent_penalty)) if engaged else None
        baseline_leader = int(np.argmax(off.total_payoffs()))
        concentration = (per_agent_penalty[top_payer] / total_penalty) if engaged else 0.0
        rows.append(
            {
                "seed": seed,
                "engaged": engaged,
                "total_wealth_penalty": total_penalty,
                "top_payer_concentration": concentration,
                "top_payer_is_baseline_leader": (top_payer == baseline_leader) if engaged else None,
                "gini_off": _gini(off.total_payoffs()),
                "gini_on": _gini(on.total_payoffs()),
            }
        )
    return pd.DataFrame(rows)


def run_q2b_threshold_sensitivity(
    thresholds=THRESHOLD_VALUES, n_seeds=20
) -> pd.DataFrame:
    """Sub-part of Q2: does engagement scale down smoothly as the threshold rises?"""
    agents = (AgentSpec("cooperative", 8, COOP_PARAMS),)
    rows = []
    for threshold in thresholds:
        penalties = []
        engaged_count = 0
        for seed in range(1, n_seeds + 1):
            cfg = SimulationConfig(
                name=f"E22_q2b_{threshold}_{seed}",
                rounds=ROUNDS,
                information_model="global",
                decision_noise=NOISE,
                resource=_resource(),
                agents=agents,
                wealth_monitoring=WealthMonitoringConfig(
                    threshold=threshold, monitoring_cost=MONITORING_COST
                ),
            )
            result = run_simulation(cfg, seed=seed)
            total_penalty = sum(sum(r.penalties) for r in result.rounds)
            penalties.append(total_penalty)
            if total_penalty > 0:
                engaged_count += 1
        rows.append(
            {
                "threshold": threshold,
                "mean_total_wealth_penalty": float(np.mean(penalties)),
                "engaged_fraction": engaged_count / n_seeds,
            }
        )
    return pd.DataFrame(rows)


def make_figure(q1: pd.DataFrame, q2: pd.DataFrame, q2b: pd.DataFrame, path: Path) -> None:
    """Three panels: freerider suppression, burden concentration, threshold sensitivity."""
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15.5, 4.4))

    styles = [(False, "#1f77b4", "no wealth monitoring"), (True, "#d62728", "wealth monitoring")]
    for wm, color, label in styles:
        sub = q1[q1["wealth_monitoring"] == wm].sort_values("n_selfish")
        ax1.plot(sub["n_selfish"], sub["welfare_efficiency"], marker="o", color=color, label=label)
    ax1.set_xlabel("number of selfish free-riders (of 8)")
    ax1.set_ylabel("welfare_efficiency")
    ax1.set_title("A. A free-rider suppresses\nthe trigger entirely")
    ax1.set_ylim(0, 1.05)
    ax1.legend(fontsize=8)

    engaged = q2[q2["engaged"]]
    ax2.hist(engaged["top_payer_concentration"], bins=12, color="#2ca02c", alpha=0.85)
    ax2.axvline(0.125, color="grey", ls="--", lw=1, label="uniform share (1/8)")
    ax2.set_xlabel("top payer's share of total wealth-penalty")
    ax2.set_ylabel(f"seeds (of {len(q2)})")
    ax2.set_title("B. Burden concentrates on a\nfew agents, not evenly")
    ax2.legend(fontsize=8)

    ax3.plot(q2b["threshold"], q2b["mean_total_wealth_penalty"], marker="o", color="#9467bd")
    ax3.set_xlabel("wealth threshold (× population average)")
    ax3.set_ylabel("mean total wealth-triggered\nmonitoring cost paid")
    ax3.set_title("C. Engagement fades smoothly\nas the bar rises")

    fig.suptitle("E22: wealth-triggered voluntary monitoring (Olson 1965)")
    fig.tight_layout(rect=(0.0, 0.0, 1.0, 0.92))
    fig.savefig(path, dpi=130)
    plt.close(fig)


def main() -> None:
    """Run both questions, export tables and figure, print a summary."""
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    q1 = run_q1_freerider_sweep()
    q1.to_csv(OUT_DIR / "q1_freerider_sweep.csv", index=False)
    q2 = run_q2_exploitation_dynamics()
    q2.to_csv(OUT_DIR / "q2_exploitation_dynamics.csv", index=False)
    q2b = run_q2b_threshold_sensitivity()
    q2b.to_csv(OUT_DIR / "q2b_threshold_sensitivity.csv", index=False)
    make_figure(q1, q2, q2b, OUT_DIR / "figure.png")

    print("Q1 -- free-rider sweep:")
    print(q1.round(3).to_string(index=False))

    engaged = q2[q2["engaged"]]
    print(f"\nQ2 -- exploitation dynamics ({len(engaged)}/{len(q2)} seeds engaged):")
    print(f"  mean top-payer concentration: {engaged['top_payer_concentration'].mean():.3f}"
          f" (uniform share would be {1/8:.3f})")
    print(f"  top payer matches the ungated-baseline wealth leader in "
          f"{engaged['top_payer_is_baseline_leader'].sum()}/{len(engaged)} engaged seeds")
    gini_decreased = (q2["gini_on"] < q2["gini_off"]).sum()
    print(
        f"  payoff Gini decreases (mechanism switched on vs off) in "
        f"{gini_decreased}/{len(q2)} seeds"
    )

    print("\nQ2b -- threshold sensitivity:")
    print(q2b.round(4).to_string(index=False))
    print(
        f"\nWrote q1_freerider_sweep.csv, q2_exploitation_dynamics.csv, "
        f"q2b_threshold_sensitivity.csv, and figure.png to: {OUT_DIR}"
    )


if __name__ == "__main__":
    main()
