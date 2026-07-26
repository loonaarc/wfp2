"""Experiment E4: robustness (to noise) and sensitivity (to N and g).

Now that agents can act stochastically (``decision_noise``), the random seed matters
and between-seed variance is meaningful. This experiment does two things:

* **Robustness (Panel A).** Re-run the mechanism comparison (cooperative /
  conditional / sanctioning vs. selfish) with ``decision_noise = 0.1`` across many
  seeds, and show the mean sustainability with a ±1 s.d. band. Are the E3 conclusions
  robust to noise?
* **Sensitivity (Panels B, C).** How does an unconditional-cooperator + selfish
  population depend on the regeneration rate ``g`` (Panel B) and the group size ``N``
  (Panel C)?

Answers SQ-11 (robustness across seeds) and SQ-12 (sensitivity). Outputs go to
``results/E4_robustness/``. Run with::

    python scripts/experiment_robustness.py
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

OUT_DIR = Path(__file__).resolve().parent.parent / "results" / "E4_robustness"
SEEDS = tuple(range(1, 21))  # 20 seeds
NOISE = 0.1
TYPES = ["cooperative", "conditional_cooperator", "sanctioning"]
LABELS = {
    "cooperative": "unconditional",
    "conditional_cooperator": "conditional",
    "sanctioning": "sanctioning",
}


def _params(strategy):
    p = {"regeneration_rate": 0.4, "capacity": 100.0}
    if strategy == "sanctioning":
        p["monitoring_cost"] = 0.2
    return p


def _experiment(agents, *, capacity=100.0, g=0.4, noise=NOISE, name="E4"):
    sim = SimulationConfig(
        name=name,
        rounds=100,
        information_model="global",
        decision_noise=noise,
        resource=ResourceConfig(
            initial_level=capacity / 2,
            capacity=capacity,
            regeneration_rate=g,
            collapse_threshold=1.0,
        ),
        agents=tuple(agents),
    )
    return ExperimentConfig(simulation=sim, seeds=SEEDS, record_history=False)


def _mix(cooperator_type, n_coop, n_selfish):
    agents = []
    if n_coop > 0:
        agents.append(AgentSpec(cooperator_type, n_coop, _params(cooperator_type)))
    if n_selfish > 0:
        agents.append(AgentSpec("selfish", n_selfish, {"greed": 1.0}))
    return agents


def sweep_robustness() -> pd.DataFrame:
    """Panel A: mechanism x number of selfish, with noise; mean and s.d. of sustainability."""
    rows = []
    for ctype in TYPES:
        for n_selfish in range(7):
            metrics = run_experiment(_experiment(_mix(ctype, 8 - n_selfish, n_selfish))).metrics
            s = metrics["sustainability_ratio"]
            rows.append(
                {
                    "cooperator_type": ctype,
                    "n_selfish": n_selfish,
                    "sustain_mean": s.mean(),
                    "sustain_std": s.std(),
                }
            )
    return pd.DataFrame(rows)


def sweep_regeneration() -> pd.DataFrame:
    """Panel B: unconditional cooperators + selfish; sensitivity to g."""
    rows = []
    for g in [0.2, 0.4, 0.6, 0.8]:
        for n_selfish in range(8):
            metrics = run_experiment(
                _experiment(_mix("cooperative", 8 - n_selfish, n_selfish), g=g)
            ).metrics
            rows.append(
                {
                    "g": g,
                    "n_selfish": n_selfish,
                    "sustain_mean": metrics["sustainability_ratio"].mean(),
                }
            )
    return pd.DataFrame(rows)


def sweep_group_size() -> pd.DataFrame:
    """Panel C: unconditional cooperators + selfish; sensitivity to N (by selfish fraction)."""
    rows = []
    for n in [4, 8, 16, 32]:
        for frac in [0.0, 0.125, 0.25, 0.375, 0.5]:
            n_selfish = round(frac * n)
            metrics = run_experiment(
                _experiment(_mix("cooperative", n - n_selfish, n_selfish), name=f"N{n}")
            ).metrics
            rows.append(
                {
                    "N": n,
                    "selfish_fraction": frac,
                    "sustain_mean": metrics["sustainability_ratio"].mean(),
                }
            )
    return pd.DataFrame(rows)


def make_figure(rob, reg, grp, path: Path) -> None:
    """Three panels: robustness band, g-sensitivity, N-sensitivity."""
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 4.4))

    for ctype in TYPES:
        sub = rob[rob["cooperator_type"] == ctype].sort_values("n_selfish")
        ax1.plot(sub["n_selfish"], sub["sustain_mean"], marker="o", label=LABELS[ctype])
        ax1.fill_between(
            sub["n_selfish"],
            sub["sustain_mean"] - sub["sustain_std"],
            sub["sustain_mean"] + sub["sustain_std"],
            alpha=0.2,
        )
    ax1.set_xlabel("number of selfish agents (of 8)")
    ax1.set_ylabel("sustainability ratio")
    ax1.set_title(f"A. Robustness to noise (±1 s.d.)\ndecision_noise={NOISE}, {len(SEEDS)} seeds")
    ax1.set_ylim(-0.02, 0.6)
    ax1.legend()

    for g in sorted(reg["g"].unique()):
        sub = reg[reg["g"] == g].sort_values("n_selfish")
        ax2.plot(sub["n_selfish"], sub["sustain_mean"], marker="o", label=f"g = {g}")
    ax2.set_xlabel("number of selfish agents (of 8)")
    ax2.set_ylabel("sustainability ratio")
    ax2.set_title("B. Sensitivity to regeneration rate\n(unconditional cooperators)")
    ax2.set_ylim(-0.02, 0.6)
    ax2.legend()

    for n in sorted(grp["N"].unique()):
        sub = grp[grp["N"] == n].sort_values("selfish_fraction")
        ax3.plot(sub["selfish_fraction"], sub["sustain_mean"], marker="o", label=f"N = {n}")
    ax3.set_xlabel("fraction of selfish agents")
    ax3.set_ylabel("sustainability ratio")
    ax3.set_title("C. Sensitivity to group size\n(unconditional cooperators)")
    ax3.set_ylim(-0.02, 0.6)
    ax3.legend()

    fig.suptitle("E4: robustness to noise, and sensitivity to regeneration rate and group size")
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)


def main() -> None:
    """Run all three sweeps, export CSVs + figure, print summaries."""
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rob, reg, grp = sweep_robustness(), sweep_regeneration(), sweep_group_size()
    rob.to_csv(OUT_DIR / "robustness.csv", index=False)
    reg.to_csv(OUT_DIR / "sensitivity_g.csv", index=False)
    grp.to_csv(OUT_DIR / "sensitivity_N.csv", index=False)
    make_figure(rob, reg, grp, OUT_DIR / "figure.png")

    print("A. Robustness — sustainability mean (s.d.) at decision_noise =", NOISE)
    for ctype in TYPES:
        sub = rob[rob["cooperator_type"] == ctype]
        worst = sub["sustain_std"].max()
        print(f"  {LABELS[ctype]:14s}: max between-seed s.d. across selfish counts = {worst:.4f}")
    print(f"\nWrote CSVs and figure.png to: {OUT_DIR}")


if __name__ == "__main__":
    main()
