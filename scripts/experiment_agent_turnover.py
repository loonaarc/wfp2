"""Experiment E24: agent turnover, and can it recover a triggered population?

Duffy & Lafky (2015): replacing a fixed cohort with staggered overlapping-
generations turnover (new subjects entering as old ones exit) significantly
flattens the usual decay of public-goods contributions over time. This
project's agents are fixed, deterministic strategies, not learning subjects
-- there is no experience-driven decay to arrest, except for one strategy
with genuine per-round memory of a permanent decline: `grim_trigger` (E21),
whose trigger never resets on its own ("no return path", ADR-0018). A new
`agent_turnover` disturbance (ADR-0021) resets a fraction of agents' own
strategy memory at a scheduled round -- as if a fresh individual, with no
memory of any prior trigger, took over that role. Two questions, both
checked directly against the engine before this script was written:

A. **Can turnover recover a triggered grim_trigger population, and does
   timing matter?** E21's own scenario (1 sensitive agent among 7
   cooperative, hit by a one-time recoverable shock) settles into a
   permanently depressed equilibrium with no return path. Does a full-
   population turnover event after the shock recover it, and does welfare
   scale with how quickly the reset happens, mirroring E21's own timing
   sensitivity in reverse?
B. **Is turnover a genuine no-op everywhere there's nothing to reset?**
   Cooperative/selfish/sanctioning populations have no per-round decline
   memory at all -- turnover should have exactly zero effect.

Outputs go to ``results/E24_agent_turnover/``. Run::

    python scripts/experiment_agent_turnover.py

Write-up: ``docs/experiments/E24-agent-turnover.md``.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from emergent_cooperation.core.config import (  # noqa: E402
    AgentSpec,
    DisturbanceConfig,
    ResourceConfig,
    SimulationConfig,
)
from emergent_cooperation.core.simulation import run_simulation  # noqa: E402

OUT_DIR = Path(__file__).resolve().parent.parent / "results" / "E24_agent_turnover"
ROUNDS = 100
CAPACITY = 100.0
G = 0.4
MSY = G * CAPACITY / 4.0
SHOCK_ROUND = 30
SHOCK_MAGNITUDE = 0.15
COOP_PARAMS = {"regeneration_rate": G, "capacity": CAPACITY}
SELFISH_PARAMS = {"greed": 1.0}
SANCTION_PARAMS = {"regeneration_rate": G, "capacity": CAPACITY, "monitoring_cost": 0.2}
TURNOVER_ROUNDS = (31, 35, 40, 50, 60, 70, 80, 90, 95)
N_SELFISH_VALUES = range(4)


def _resource() -> ResourceConfig:
    return ResourceConfig(
        initial_level=50.0, capacity=CAPACITY, regeneration_rate=G, collapse_threshold=1.0
    )


def _welfare(result) -> float:
    return sum(result.total_payoffs()) / (MSY * ROUNDS)


def run_q1_recovery_timing(turnover_rounds=TURNOVER_ROUNDS) -> pd.DataFrame:
    """1 grim_trigger + 7 cooperative, shocked at round 30.

    Does a full-population turnover event recover it, and does timing matter?
    """
    agents = (AgentSpec("grim_trigger", 1, COOP_PARAMS), AgentSpec("cooperative", 7, COOP_PARAMS))

    def _run(turnover_round: int | None):
        disturbances = [
            DisturbanceConfig(kind="resource_shock", round=SHOCK_ROUND, magnitude=SHOCK_MAGNITUDE)
        ]
        if turnover_round is not None:
            disturbances.append(
                DisturbanceConfig(kind="agent_turnover", round=turnover_round, magnitude=1.0)
            )
        cfg = SimulationConfig(
            name=f"E24_q1_{turnover_round}",
            rounds=ROUNDS,
            information_model="global",
            resource=_resource(),
            agents=agents,
            disturbances=tuple(disturbances),
        )
        return run_simulation(cfg, seed=1)

    baseline = _run(None)
    rows = [
        {
            "turnover_round": SHOCK_ROUND,  # sentinel row: no turnover at all
            "turnover_applied": False,
            "welfare_efficiency": _welfare(baseline),
            "final_level": baseline.rounds[-1].resource_after_harvest,
            "rounds_after_shock": None,
        }
    ]
    for t in turnover_rounds:
        result = _run(t)
        rows.append(
            {
                "turnover_round": t,
                "turnover_applied": True,
                "welfare_efficiency": _welfare(result),
                "final_level": result.rounds[-1].resource_after_harvest,
                "rounds_after_shock": t - SHOCK_ROUND,
            }
        )
    return pd.DataFrame(rows)


def _run_q2_one(strategy: str, n_selfish: int, agents: list, turnover: bool):
    disturbances = (
        tuple(
            DisturbanceConfig(kind="agent_turnover", round=r, magnitude=0.5)
            for r in range(10, 90, 7)
        )
        if turnover
        else ()
    )
    cfg = SimulationConfig(
        name=f"E24_q2_{strategy}_{n_selfish}_{turnover}",
        rounds=ROUNDS,
        information_model="global",
        resource=_resource(),
        agents=tuple(agents),
        disturbances=disturbances,
    )
    return run_simulation(cfg, seed=1)


def run_q2_noop_verification(n_selfish_values=N_SELFISH_VALUES) -> pd.DataFrame:
    """Cooperative/selfish/sanctioning populations: turnover on vs off must be identical."""
    rows = []
    for strategy in ("cooperative", "sanctioning"):
        params = SANCTION_PARAMS if strategy == "sanctioning" else COOP_PARAMS
        for n_selfish in n_selfish_values:
            agents = [AgentSpec(strategy, 8 - n_selfish, params)]
            if n_selfish > 0:
                agents.append(AgentSpec("selfish", n_selfish, SELFISH_PARAMS))

            off = _run_q2_one(strategy, n_selfish, agents, False)
            on = _run_q2_one(strategy, n_selfish, agents, True)
            rows.append(
                {
                    "strategy": strategy,
                    "n_selfish": n_selfish,
                    "welfare_off": _welfare(off),
                    "welfare_on": _welfare(on),
                    "byte_identical": off.total_payoffs() == on.total_payoffs(),
                }
            )
    return pd.DataFrame(rows)


def make_figure(q1: pd.DataFrame, path: Path) -> None:
    """One panel: welfare recovered vs. how long after the shock turnover fires."""
    fig, ax = plt.subplots(figsize=(6.5, 4.6))
    applied = q1[q1["turnover_applied"]].sort_values("rounds_after_shock")
    baseline = q1[~q1["turnover_applied"]]["welfare_efficiency"].iloc[0]
    ax.plot(
        applied["rounds_after_shock"], applied["welfare_efficiency"],
        marker="o", color="#2ca02c", label="turnover applied",
    )
    ax.axhline(baseline, color="#d62728", ls="--", lw=1.5, label="no turnover (stuck)")
    ax.set_xlabel("rounds between the shock and the turnover event")
    ax.set_ylabel("welfare_efficiency")
    ax.set_title(
        "E24: recovering a triggered grim_trigger agent\n"
        "via turnover -- worth it only if it comes soon enough"
    )
    ax.set_ylim(0.97, 1.0)
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)


def main() -> None:
    """Run both questions, export tables and figure, print a summary."""
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    q1 = run_q1_recovery_timing()
    q1.to_csv(OUT_DIR / "q1_recovery_timing.csv", index=False)
    q2 = run_q2_noop_verification()
    q2.to_csv(OUT_DIR / "q2_noop_verification.csv", index=False)
    make_figure(q1, OUT_DIR / "figure.png")

    print("Q1 -- recovery timing after a shock:")
    print(q1.round(4).to_string(index=False))
    print("\nQ2 -- no-op verification (cooperative/sanctioning, no memory to reset):")
    print(q2.round(4).to_string(index=False))
    print(f"\nAll Q2 rows byte-identical: {q2['byte_identical'].all()}")
    print(f"\nWrote q1_recovery_timing.csv, q2_noop_verification.csv, and figure.png to: {OUT_DIR}")


if __name__ == "__main__":
    main()
