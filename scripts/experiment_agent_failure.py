"""Experiment E10: agent failure — is enforcement a single point of failure?

E8–E9 disturbed the *resource* (a shock). This one disturbs the *population*: at a
mid-run round a quarter of the agents drop out (``agent_failure`` — they stop
requesting, harvesting, and, if a sanctioner, enforcing). The question is whether a
commons tolerates losing members, and whether it matters *who* is lost.

Three scenarios (global information, 8 agents, fail 25% at round 30):

* **enforcer fails** — 2 sanctioners + 6 selfish. Enforcement holds the commons
  (E3); the 2 sanctioners are failed, so enforcement vanishes and the 6 selfish
  collapse the pool.
* **cooperator fails** — 8 self-correcting cooperators; 2 are failed. The rest still
  observe and self-correct, so the pool is unharmed (a little *healthier* — fewer
  mouths).
* **free-rider fails** — 2 selfish + 6 cooperators (a commons the free-riders are
  eroding); the 2 selfish are failed, and the pool *recovers* to health.

The result: **who fails decides the outcome.** Losing the enforcer collapses the
commons; losing a cooperator is harmless; losing a free-rider helps. Enforcement,
the mechanism that makes the commons robust to free-riders (E3/E9), makes it
**fragile to losing the monitor** — a single point of failure that the distributed,
self-correcting cooperative commons does not have. (Compare E5: there monitoring
erodes *endogenously*; here it is removed *exogenously*, with the same lesson.)

Outputs go to ``results/E10_agent_failure/``. Run with::

    python scripts/experiment_agent_failure.py
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

OUT_DIR = Path(__file__).resolve().parent.parent / "results" / "E10_agent_failure"
SEEDS = tuple(range(1, 21))
NOISE = 0.1
ROUNDS = 60
FAIL_ROUND = 30
FAIL_FRACTION = 0.25  # a quarter of the 8 agents = 2
CAPACITY = 100.0
G = 0.4


def _coop(n: int) -> AgentSpec:
    return AgentSpec("cooperative", n, {"regeneration_rate": G, "capacity": CAPACITY})


def _sanction(n: int) -> AgentSpec:
    params = {"regeneration_rate": G, "capacity": CAPACITY, "monitoring_cost": 0.2}
    return AgentSpec("sanctioning", n, params)


def _selfish(n: int) -> AgentSpec:
    return AgentSpec("selfish", n, {"greed": 1.0})


# Agents fail in spec order, so the group meant to fail is listed FIRST.
SCENARIOS = {
    "enforcer fails": [_sanction(2), _selfish(6)],
    "cooperator fails": [_coop(8)],
    "free-rider fails": [_selfish(2), _coop(6)],
}
SCEN_COLOR = {
    "enforcer fails": "#1f77b4",
    "cooperator fails": "#2ca02c",
    "free-rider fails": "#d55e00",
}


def _experiment(agents: list[AgentSpec], *, fail: bool) -> ExperimentConfig:
    disturbances = (
        (DisturbanceConfig("agent_failure", round=FAIL_ROUND, magnitude=FAIL_FRACTION),)
        if fail
        else ()
    )
    sim = SimulationConfig(
        name="E10",
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
    """Final sustainability per scenario, with and without the agent failure."""
    rows = []
    for name, agents in SCENARIOS.items():
        for fail in (True, False):
            metrics = run_experiment(_experiment(agents, fail=fail)).metrics
            rows.append(
                {
                    "scenario": name,
                    "failure": fail,
                    "final_sustainability": float(metrics["sustainability_ratio"].mean()),
                }
            )
    return pd.DataFrame(rows)


def _mean_trajectory(agents: list[AgentSpec]) -> np.ndarray:
    outcome = run_experiment(_experiment(agents, fail=True))
    stacked = np.array(
        [[r.resource_after_harvest for r in result.rounds] for result in outcome.results]
    )
    return stacked.mean(axis=0)


def make_figure(summary: pd.DataFrame, path: Path) -> None:
    """Panel A: trajectories through the failure. Panel B: final stock, fail vs no-fail."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 4.6))

    for name, agents in SCENARIOS.items():
        traj = _mean_trajectory(agents)
        ax1.plot(range(len(traj)), traj, color=SCEN_COLOR[name], lw=2, label=name)
    ax1.axvline(FAIL_ROUND, color="grey", ls=":", lw=1)
    ax1.text(FAIL_ROUND + 1, 92, "25% of agents fail", color="grey", fontsize=9)
    ax1.axhline(CAPACITY / 2, color="grey", ls=":", lw=0.8)
    ax1.set_xlabel("round")
    ax1.set_ylabel("resource stock (mean over seeds)")
    ax1.set_ylim(-2, 100)
    ax1.set_title("A. Losing 25% of agents — who fails decides")
    ax1.legend(loc="center left", fontsize=8)

    names = list(SCENARIOS)
    x = np.arange(len(names))

    def _final(name, failed):
        sub = summary[(summary.scenario == name) & (summary.failure == failed)]
        return sub.final_sustainability.iloc[0]

    nofail = [_final(n, False) for n in names]
    fail = [_final(n, True) for n in names]
    ax2.bar(x - 0.19, nofail, 0.36, label="no failure", color="#b0b7bd")
    ax2.bar(x + 0.19, fail, 0.36, label="25% fail", color=[SCEN_COLOR[n] for n in names])
    ax2.set_xticks(x)
    ax2.set_xticklabels(names, fontsize=9)
    ax2.set_ylabel("final resource (fraction of K)")
    ax2.set_ylim(0, 0.62)
    ax2.set_title("B. The failure flips each outcome differently")
    ax2.legend(fontsize=8)

    fig.suptitle("E10: enforcement is a single point of failure; self-correction is not")
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)


def main() -> None:
    """Run the scenarios, export the summary CSV + figure, print the headline."""
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    summary = summarise()
    summary.to_csv(OUT_DIR / "summary.csv", index=False)
    make_figure(summary, OUT_DIR / "figure.png")

    print("E10 — final resource (fraction of K), no failure vs. 25% of agents failing:")
    for name in SCENARIOS:
        nf = summary[(summary.scenario == name) & (~summary.failure)].final_sustainability.iloc[0]
        f = summary[(summary.scenario == name) & (summary.failure)].final_sustainability.iloc[0]
        print(f"  {name:18s}: no-failure {nf:.2f}  ->  failure {f:.2f}")
    print(f"\nWrote summary.csv and figure.png to: {OUT_DIR}")


if __name__ == "__main__":
    main()
