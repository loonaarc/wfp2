"""Experiment E21: grim trigger and the cost of a finite horizon (ADR-0018).

Friedman (1971): a non-cooperative equilibrium can sustain a Pareto-improving
outcome purely from the threat of permanent reversion to the one-shot
(selfish) equilibrium after any deviation -- "grim trigger." Fudenberg &
Maskin (1986): finite horizons compound the problem of sustaining
cooperation via backward induction, since a permanent punishment only has as
much of the game left to act on as remains.

Two questions:

A. **Does grim trigger's refusal to forgive cost welfare, compared to
   conditional_cooperator's forgiveness, when a decline turns out to be a
   one-time, recoverable event rather than genuine ongoing free-riding?**
   Sweep how many of the 8 agents are "sensitive" (decline-detecting)
   against a background of plain `cooperative` agents, all hit by the same
   modest, one-time resource shock.
B. **Does the finite horizon matter -- does an earlier permanent trigger
   cost more cumulative welfare than a later one?** An all-`grim_trigger`
   population, the identical shock, swept across which round it fires in a
   fixed 100-round run.

Outputs go to ``results/E21_grim_trigger/``. Run::

    python scripts/experiment_grim_trigger.py

Write-up: ``docs/experiments/E21-grim-trigger-finite-horizon.md``.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

from emergent_cooperation.core.config import (  # noqa: E402
    AgentSpec,
    DisturbanceConfig,
    ResourceConfig,
    SimulationConfig,
)
from emergent_cooperation.core.simulation import run_simulation  # noqa: E402

OUT_DIR = Path(__file__).resolve().parent.parent / "results" / "E21_grim_trigger"
ROUNDS = 100
CAPACITY = 100.0
G = 0.4
MSY = G * CAPACITY / 4.0
COOP_PARAMS = {"regeneration_rate": G, "capacity": CAPACITY}
SHOCK_MAGNITUDE = 0.15  # modest -- large enough to trigger decline-detection,
# nowhere near catastrophic on its own (see ADR-0018 / E17's own related finding
# that the *response*, not the shock's size, is usually what does the damage)
SHOCK_ROUND_Q1 = 30


def _resource() -> ResourceConfig:
    return ResourceConfig(
        initial_level=50.0, capacity=CAPACITY, regeneration_rate=G, collapse_threshold=1.0
    )


def _welfare(result) -> float:
    return sum(result.total_payoffs()) / (MSY * ROUNDS)


def run_q1_forgiveness_sweep(kinds=("conditional_cooperator", "grim_trigger")) -> pd.DataFrame:
    """How many 'sensitive' agents does permanence vs. forgiveness matter for.

    Tests a one-time, recoverable shock rather than ongoing free-riding.
    """
    rows = []
    for n_sensitive in range(9):
        for kind in kinds:
            agents = [AgentSpec(kind, n_sensitive, COOP_PARAMS)] if n_sensitive > 0 else []
            if n_sensitive < 8:
                agents.append(AgentSpec("cooperative", 8 - n_sensitive, COOP_PARAMS))
            cfg = SimulationConfig(
                name=f"E21_q1_{kind}_{n_sensitive}",
                rounds=ROUNDS,
                information_model="global",
                resource=_resource(),
                agents=tuple(agents),
                disturbances=(
                    DisturbanceConfig(
                        kind="resource_shock", round=SHOCK_ROUND_Q1, magnitude=SHOCK_MAGNITUDE
                    ),
                ),
            )
            result = run_simulation(cfg, seed=1)
            final = result.rounds[-1]
            rows.append(
                {
                    "n_sensitive": n_sensitive,
                    "kind": kind,
                    "welfare_efficiency": _welfare(result),
                    "final_level": final.resource_after_harvest,
                    "collapsed": final.collapsed,
                }
            )
    return pd.DataFrame(rows)


def run_q2_trigger_timing_sweep(shock_rounds=(10, 30, 50, 70, 90)) -> pd.DataFrame:
    """All grim_trigger, identical shock, swept by which round it fires.

    Does the fixed, finite 100-round horizon matter for the timing?
    """
    rows = []
    for shock_round in shock_rounds:
        agents = (AgentSpec("grim_trigger", 8, COOP_PARAMS),)
        cfg = SimulationConfig(
            name=f"E21_q2_{shock_round}",
            rounds=ROUNDS,
            information_model="global",
            resource=_resource(),
            agents=agents,
            disturbances=(
                DisturbanceConfig(
                    kind="resource_shock", round=shock_round, magnitude=SHOCK_MAGNITUDE
                ),
            ),
        )
        result = run_simulation(cfg, seed=1)
        rows.append(
            {
                "shock_round": shock_round,
                "rounds_remaining": ROUNDS - shock_round,
                "welfare_efficiency": _welfare(result),
                "final_level": result.rounds[-1].resource_after_harvest,
            }
        )
    return pd.DataFrame(rows)


def make_figure(q1: pd.DataFrame, q2: pd.DataFrame, path: Path) -> None:
    """Two panels: forgiveness-vs-permanence, and welfare vs. trigger round."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 4.4))

    for kind, color in [("conditional_cooperator", "#2ca02c"), ("grim_trigger", "#d62728")]:
        sub = q1[q1["kind"] == kind].sort_values("n_sensitive")
        ax1.plot(sub["n_sensitive"], sub["welfare_efficiency"], marker="o", color=color, label=kind)
    ax1.set_xlabel("number of 'sensitive' (decline-detecting) agents, of 8")
    ax1.set_ylabel("welfare_efficiency")
    ax1.set_title("A. Does forgiveness matter for a one-time,\nrecoverable shock?")
    ax1.set_ylim(0, 1.05)
    ax1.legend(fontsize=8)

    ax2.plot(q2["shock_round"], q2["welfare_efficiency"], marker="o", color="#1f77b4")
    ax2.set_xlabel("round the shock (and permanent trigger) fires")
    ax2.set_ylabel("welfare_efficiency (100-round run)")
    ax2.set_title("B. All grim_trigger -- does WHEN it\nfires matter, given a fixed horizon?")
    ax2.set_ylim(0, 1.05)

    fig.suptitle("E21: grim trigger and the cost of a finite horizon")
    fig.tight_layout(rect=(0.0, 0.0, 1.0, 0.92))
    fig.savefig(path, dpi=130)
    plt.close(fig)


def main() -> None:
    """Run both questions, export tables and figure, print a summary."""
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    q1 = run_q1_forgiveness_sweep()
    q1.to_csv(OUT_DIR / "q1_forgiveness_sweep.csv", index=False)
    q2 = run_q2_trigger_timing_sweep()
    q2.to_csv(OUT_DIR / "q2_trigger_timing_sweep.csv", index=False)
    make_figure(q1, q2, OUT_DIR / "figure.png")

    print("Q1 -- forgiveness vs. permanence, one-time shock at round 30:")
    print(q1.round(3).to_string(index=False))
    print("\nQ2 -- trigger timing, all grim_trigger:")
    print(q2.round(3).to_string(index=False))
    print(
        "\nWrote q1_forgiveness_sweep.csv, q2_trigger_timing_sweep.csv, "
        f"and figure.png to: {OUT_DIR}"
    )


if __name__ == "__main__":
    main()
