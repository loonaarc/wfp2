"""Experiment E12: does second-order sanctioning stabilise monitoring?

E11 tried Hauert et al. (2007)'s opt-out ("loner") rescue for E5's collapsing
voluntary monitoring and found it only delays the collapse, because our
continuous replicator dynamics lack the finite-population fixation step the
mechanism depends on (see ADR-0009).

Sigmund, De Silva, Traulsen & Hauert (2010) offer a *different* fix for the same
second-order free-rider problem, built on a different property: **pool
punishment** is pre-committed (paid every round, unconditionally, unlike E11's
defector-scaled cost), and because paying into the pool is a declared act, the
pool can also punish **second-order free-riders** -- plain cooperators who
benefit from enforcement without paying for it. This experiment isolates that
one new ingredient, changing only one thing relative to plain E5 (experiment-
design.md's "change one factor at a time"): monitoring cost stays flat (as in
E5), and a **second-order fine** is added, charged to cooperators and paid out
to sanctioners, both computed at the replicator/fitness level (no core-engine
change; ADR-0006's approach, same as E11).

Strategies: ``sanctioning``, ``cooperative``, ``selfish`` (no loner -- isolating
the second-order-fine mechanism on its own, cf. E11's loner-only test).

Note on getting this right: Sigmund's pool already fines actual defectors before
any second-order addition -- our engine's harvest-cap enforcement does not
(selfish and cooperative earn identically once capped, see the diagnostic in
ADR-0010), so the fine below is charged to *both* ``cooperative`` and
``selfish`` agents, not ``cooperative`` alone. Charging only ``cooperative``
(the first version of this script) made cooperators worse off than untaxed
selfish agents and made the collapse *faster*, not slower -- see ADR-0010 for
that failed first attempt and why it failed.

Outputs go to ``results/E12_pool_punishment/``. Run::

    python scripts/experiment_pool_punishment.py

Write-up: ``docs/experiments/E12-pool-punishment.md``.
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

OUT_DIR = Path(__file__).resolve().parent.parent / "results" / "E12_pool_punishment"
N = 40
ROUNDS = 60
GENERATIONS = 60
SELECTION = 0.3
STRATEGIES = ["sanctioning", "cooperative", "selfish"]
LABELS = {
    "sanctioning": "sanctioning (pool monitor)",
    "cooperative": "cooperator (free)",
    "selfish": "selfish",
}
PARAMS = {
    "sanctioning": {"regeneration_rate": 0.4, "capacity": 100.0, "monitoring_cost": 0.2},
    "cooperative": {"regeneration_rate": 0.4, "capacity": 100.0},
    "selfish": {"greed": 1.0},
}
# The pool fine: every non-monitor (cooperative *and* selfish) loses this much
# per round, redistributed evenly across sanctioners -- "a non-monitor pays
# exactly what a monitor pays, whether it's a defector (the ordinary fine
# Sigmund's model already assumes) or a free-riding cooperator (the
# second-order fine)". Only collectable if a pool (>=1 sanctioner) exists.
POOL_FINE_PER_ROUND = 0.2


def _largest_remainder(shares: dict[str, float], total: int) -> dict[str, int]:
    """Round fractional shares to integer counts summing exactly to ``total``."""
    raw = {s: shares[s] * total for s in shares}
    counts = {s: int(v) for s, v in raw.items()}
    remainder = total - sum(counts.values())
    order = sorted(shares, key=lambda s: raw[s] - counts[s], reverse=True)
    for s in order[:remainder]:
        counts[s] += 1
    return counts


def _measure(counts: dict[str, int]) -> tuple[dict[str, float], float]:
    """Run one simulation at ``counts``; apply the second-order fine; return
    per-strategy payoff and sustainability.
    """
    agents = [AgentSpec(s, c, PARAMS[s]) for s, c in counts.items() if c > 0]
    cfg = SimulationConfig(
        name="E12",
        rounds=ROUNDS,
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

    # Pool fine: every non-monitor -- cooperative (second-order free-rider) and
    # selfish (ordinary defector) alike -- pays into the pool, redistributed
    # evenly across sanctioners. Only collectable if a pool actually exists.
    n_coop = counts.get("cooperative", 0)
    n_self = counts.get("selfish", 0)
    n_sanction = counts.get("sanctioning", 0)
    fine_per_agent = POOL_FINE_PER_ROUND * ROUNDS
    if n_sanction > 0:
        if n_coop > 0:
            fitness["cooperative"] = fitness.get("cooperative", 0.0) - fine_per_agent
        if n_self > 0:
            fitness["selfish"] = fitness.get("selfish", 0.0) - fine_per_agent
        fine_total = fine_per_agent * (n_coop + n_self)
        fitness["sanctioning"] = fitness.get("sanctioning", 0.0) + (fine_total / n_sanction)

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
    ax1.set_title("A. Does the second-order fine stabilise monitoring?")
    ax1.set_ylim(-0.02, 1.0)
    ax1.legend(fontsize=9)

    ax2.plot(df["generation"], df["sustainability"], color="tab:red")
    ax2.axhline(0.5, color="grey", ls=":", lw=1)
    ax2.set_xlabel("generation")
    ax2.set_ylabel("sustainability ratio")
    ax2.set_title("B. ...and what happens to the commons")
    ax2.set_ylim(-0.02, 0.6)

    fig.suptitle("E12: pool punishment + second-order sanctioning")
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)


def main() -> None:
    """Run the dynamics from E5's healthy starting mix and report the outcome."""
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
