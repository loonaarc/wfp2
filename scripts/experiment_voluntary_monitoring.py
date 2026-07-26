"""Experiment E5: is voluntary monitoring evolutionarily stable?

E3 showed sanctioning protects the commons but that monitors earn less than the
cooperators they protect (the second-order free-rider problem). If agents are free to
*choose* whether to monitor, does monitoring survive?

We answer with replicator dynamics *on top of* the simulator (ADR-0006): over
"generations", instantiate a population at the current strategy shares, run one
simulation, measure each strategy's mean payoff, and grow the above-average
strategies. No core-engine change; the whole trajectory is deterministic.

Strategies: ``sanctioning`` (monitor), ``cooperative`` (free-riding cooperator),
``selfish`` (defector). Outputs go to ``results/E5_voluntary_monitoring/``. Run::

    python scripts/experiment_voluntary_monitoring.py

Write-up: ``docs/experiments/E5-voluntary-monitoring.md``.
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

OUT_DIR = Path(__file__).resolve().parent.parent / "results" / "E5_voluntary_monitoring"
N = 40
GENERATIONS = 40
SELECTION = 0.3  # replicator step size in (0, 1]
STRATEGIES = ["sanctioning", "cooperative", "selfish"]
LABELS = {
    "sanctioning": "sanctioning (monitor)",
    "cooperative": "cooperator (free)",
    "selfish": "selfish",
}
PARAMS = {
    "sanctioning": {"regeneration_rate": 0.4, "capacity": 100.0, "monitoring_cost": 0.2},
    "cooperative": {"regeneration_rate": 0.4, "capacity": 100.0},
    "selfish": {"greed": 1.0},
}


def _largest_remainder(shares: dict[str, float], total: int) -> dict[str, int]:
    """Round fractional shares to integer counts summing exactly to ``total``."""
    raw = {s: shares[s] * total for s in shares}
    counts = {s: int(v) for s, v in raw.items()}
    remainder = total - sum(counts.values())
    # Hand out the remaining slots to the largest fractional parts.
    order = sorted(shares, key=lambda s: raw[s] - counts[s], reverse=True)
    for s in order[:remainder]:
        counts[s] += 1
    return counts


def _measure(counts: dict[str, int]) -> tuple[dict[str, float], float]:
    """Run one simulation at ``counts``; return per-strategy payoff and sustainability."""
    agents = [AgentSpec(s, c, PARAMS[s]) for s, c in counts.items() if c > 0]
    cfg = SimulationConfig(
        name="E5",
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
    fitness = {s: (sum(v) / len(v) if v else 0.0) for s, v in sums.items()}
    m = compute_metrics(result, capacity=100.0, regeneration_rate=0.4, collapse_threshold=1.0)
    return fitness, m["sustainability_ratio"]


def run_dynamics(initial: dict[str, float]) -> pd.DataFrame:
    """Iterate replicator dynamics from an initial strategy composition."""
    shares = dict(initial)
    rows = []
    for gen in range(GENERATIONS):
        counts = _largest_remainder(shares, N)
        fitness, sustainability = _measure(counts)
        row = {"generation": gen, "sustainability": sustainability}
        row.update({f"share_{s}": shares[s] for s in STRATEGIES})
        rows.append(row)

        # Softened replicator update on the strategies actually present.
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
    ax1.set_title("A. Do monitors survive selection?")
    ax1.set_ylim(-0.02, 1.0)
    ax1.legend()

    ax2.plot(df["generation"], df["sustainability"], color="tab:red")
    ax2.axhline(0.5, color="grey", ls=":", lw=1)
    ax2.set_xlabel("generation")
    ax2.set_ylabel("sustainability ratio")
    ax2.set_title("B. ...and what happens to the commons")
    ax2.set_ylim(-0.02, 0.6)

    fig.suptitle("E5: voluntary monitoring erodes, and the commons collapses with it")
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)


def main() -> None:
    """Run the dynamics from a healthy, monitored commons and report the outcome."""
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    initial = {"sanctioning": 0.4, "cooperative": 0.4, "selfish": 0.2}
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
