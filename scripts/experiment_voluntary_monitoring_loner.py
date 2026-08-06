"""Experiment E11: does an opt-out ("loner") rescue voluntary monitoring?

E5 found voluntary monitoring is *not* evolutionarily stable: sanctioners pay a
flat monitoring cost every round, free-riding cooperators out-earn them, monitors
erode, and the commons then collapses to all-selfish. Hauert, Traulsen, Brandt,
Nowak & Sigmund (2007) show that adding an *optional-participation* ("loner")
strategy rescues costly punishment in this exact kind of second-order dilemma —
but only because their model also makes punishing cheaper when free-riders are
rare (punishment cost scales with the number of defectors actually present).

This experiment adds both ingredients, on top of the same replicator-dynamics
harness E5 uses (ADR-0006; no core-engine change):

1. A fourth strategy, ``loner``, that opts out of the shared resource entirely
   and earns a fixed payoff ``SIGMA`` (see ``docs/decisions/0009-loner-and-
   defector-scaled-monitoring-cost.md`` for how ``SIGMA`` was chosen). Loners do
   not enter the simulation at all -- only sanctioning/cooperative/selfish agents
   share the pool each generation.
2. The sanctioner's ``monitoring_cost`` is no longer a flat constant. It scales
   with the *current* share of selfish agents among the active (non-loner)
   population: ``monitoring_cost = BASE_MONITORING_COST * selfish_share``. When
   almost nobody defects, monitoring is nearly free; when defectors are common,
   it costs the full base rate.

Strategies: ``sanctioning``, ``cooperative``, ``selfish``, ``loner``. Outputs go
to ``results/E11_voluntary_monitoring_loner/``. Run::

    python scripts/experiment_voluntary_monitoring_loner.py

Write-up: ``docs/experiments/E11-loner-rescue.md``.
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
    ResourceConfig,
    SimulationConfig,
)
from emergent_cooperation.core.simulation import run_simulation
from emergent_cooperation.metrics.metrics import compute_metrics  # noqa: E402

OUT_DIR = Path(__file__).resolve().parent.parent / "results" / "E11_voluntary_monitoring_loner"
N = 40
GENERATIONS = 80
SELECTION = 0.3
STRATEGIES = ["sanctioning", "cooperative", "selfish", "loner"]
ACTIVE_STRATEGIES = ["sanctioning", "cooperative", "selfish"]  # strategies that enter the pool
LABELS = {
    "sanctioning": "sanctioning (monitor)",
    "cooperative": "cooperator (free)",
    "selfish": "selfish",
    "loner": "loner (opt-out)",
}
BASE_MONITORING_COST = 0.2
# Fixed payoff a loner earns, independent of the resource. Chosen so
# collapse_payoff (~1.5, all-selfish) < SIGMA < healthy_payoff (~15.0,
# all-cooperative) -- see the ADR for the diagnostic run that produced those
# reference numbers. Opting out must be a real refuge from a failing commons,
# without being able to out-earn a thriving one (Hauert's 0 < s < (r-1)c).
SIGMA = 6.0
BASE_PARAMS = {
    "sanctioning": {"regeneration_rate": 0.4, "capacity": 100.0},
    "cooperative": {"regeneration_rate": 0.4, "capacity": 100.0},
    "selfish": {"greed": 1.0},
}


def _largest_remainder(shares: dict[str, float], total: int) -> dict[str, int]:
    """Round fractional shares to integer counts summing exactly to ``total``."""
    raw = {s: shares[s] * total for s in shares}
    counts = {s: int(v) for s, v in raw.items()}
    remainder = total - sum(counts.values())
    order = sorted(shares, key=lambda s: raw[s] - counts[s], reverse=True)
    for s in order[:remainder]:
        counts[s] += 1
    return counts


def _measure(counts: dict[str, int]) -> tuple[dict[str, float], float, float]:
    """Run one simulation on the *active* (non-loner) agents at ``counts``.

    Returns per-strategy payoff (loner's is fixed at ``SIGMA``), sustainability,
    and the monitoring cost actually charged this generation (for logging).
    """
    n_active = sum(counts[s] for s in ACTIVE_STRATEGIES)
    selfish_share = (counts["selfish"] / n_active) if n_active > 0 else 0.0
    monitoring_cost = BASE_MONITORING_COST * selfish_share

    params = {**BASE_PARAMS, "sanctioning": {**BASE_PARAMS["sanctioning"], "monitoring_cost": monitoring_cost}}
    agents = [AgentSpec(s, counts[s], params[s]) for s in ACTIVE_STRATEGIES if counts[s] > 0]

    fitness = {"loner": SIGMA}
    if not agents:
        # Everyone opted out: no simulation to run, resource neither harvested nor observed.
        return fitness, float("nan"), monitoring_cost

    cfg = SimulationConfig(
        name="E11",
        rounds=60,
        information_model="global",
        resource=ResourceConfig(
            initial_level=50.0, capacity=100.0, regeneration_rate=0.4, collapse_threshold=1.0
        ),
        agents=tuple(agents),
    )
    result = run_simulation(cfg, seed=1)
    sums: dict[str, list[float]] = defaultdict(list)
    for strat, payoff in zip(result.agent_strategies, result.total_payoffs(), strict=True):
        sums[strat].append(payoff)
    for s, v in sums.items():
        fitness[s] = sum(v) / len(v) if v else 0.0
    m = compute_metrics(result, capacity=100.0, regeneration_rate=0.4, collapse_threshold=1.0)
    return fitness, m["sustainability_ratio"], monitoring_cost


def run_dynamics(initial: dict[str, float]) -> pd.DataFrame:
    """Iterate replicator dynamics from an initial strategy composition."""
    shares = dict(initial)
    rows = []
    for gen in range(GENERATIONS):
        counts = _largest_remainder(shares, N)
        fitness, sustainability, monitoring_cost = _measure(counts)
        row = {"generation": gen, "sustainability": sustainability, "monitoring_cost": monitoring_cost}
        row.update({f"share_{s}": shares[s] for s in STRATEGIES})
        rows.append(row)

        f_avg = sum(shares[s] * fitness.get(s, 0.0) for s in STRATEGIES)
        f_avg = max(f_avg, 1e-9)
        new = {}
        for s in STRATEGIES:
            f = max(fitness.get(s, 0.0), 0.0)
            new[s] = max(0.0, shares[s] * (1 + SELECTION * (f / f_avg - 1)))
        z = sum(new.values()) or 1.0
        shares = {s: new[s] / z for s in STRATEGIES}
    return pd.DataFrame(rows)


def make_figure(df: pd.DataFrame, path: Path) -> None:
    """Two panels: strategy shares over generations, and the resource over generations."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.4))
    for s in STRATEGIES:
        ax1.plot(df["generation"], df[f"share_{s}"], marker="", label=LABELS[s])
    ax1.set_xlabel("generation")
    ax1.set_ylabel("share of population")
    ax1.set_title("A. Does the opt-out rescue monitoring?")
    ax1.set_ylim(-0.02, 1.0)
    ax1.legend(fontsize=8)

    ax2.plot(df["generation"], df["sustainability"], color="tab:red")
    ax2.axhline(0.5, color="grey", ls=":", lw=1)
    ax2.set_xlabel("generation")
    ax2.set_ylabel("sustainability ratio")
    ax2.set_title("B. ...and what happens to the commons")
    ax2.set_ylim(-0.02, 0.6)

    fig.suptitle("E11: loner opt-out + defector-scaled monitoring cost")
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)


def main() -> None:
    """Run the dynamics from E5's healthy starting mix, with loners added, and report."""
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    # Replicator dynamics cannot bootstrap a strategy from an exact 0% share (0
    # times any fitness ratio is still 0) -- there is no mutation term here (see
    # E5's own limitations note), so the loner must start present, not absent.
    initial = {"sanctioning": 0.35, "cooperative": 0.35, "selfish": 0.15, "loner": 0.15}
    df = run_dynamics(initial)
    df.to_csv(OUT_DIR / "dynamics.csv", index=False)
    make_figure(df, OUT_DIR / "figure.png")

    first = df.iloc[0]
    last = df.iloc[-1]
    print(f"Initial: {initial}")
    print(
        "Gen  0: "
        + ", ".join(f"{s}={first[f'share_{s}']:.2f}" for s in STRATEGIES)
        + f", sustainability={first['sustainability']:.2f}"
    )
    print(
        f"Gen {GENERATIONS - 1}: "
        + ", ".join(f"{s}={last[f'share_{s}']:.2f}" for s in STRATEGIES)
        + f", sustainability={last['sustainability']:.2f}"
    )
    print(f"\nWrote dynamics.csv and figure.png to: {OUT_DIR}")


if __name__ == "__main__":
    main()
