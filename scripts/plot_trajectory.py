"""Plot round-by-round trajectories — see the dynamics, not just the summary.

The summary metrics (sustainability, Gini, ...) hide *how* an outcome unfolds. This
script plots the standing resource stock and the per-round harvest over time for four
representative scenarios, making the dynamics visceral: selfish agents crash the pool
in one round; cooperators hold a steady sawtooth; reciprocity ratchets to collapse;
sanctioning holds the line against free-riders.

This is a generated static plot (the project's intended visualization; the CLI +
plots remain the reproducible interface). For interactive exploration see
``notebooks/explore.ipynb``.

Outputs ``results/trajectories/figure.png``. Run with::

    python scripts/plot_trajectory.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from emergent_cooperation.core.config import (  # noqa: E402
    AgentSpec,
    ResourceConfig,
    SimulationConfig,
)
from emergent_cooperation.core.simulation import run_simulation
from emergent_cooperation.core.state import RunResult  # noqa: E402

OUT_DIR = Path(__file__).resolve().parent.parent / "results" / "trajectories"
ROUNDS = 40
COOP = {"regeneration_rate": 0.4, "capacity": 100.0}
SANCTION = {"regeneration_rate": 0.4, "capacity": 100.0, "monitoring_cost": 0.2}
SELFISH = {"greed": 1.0}

# label -> (agent groups, line style). All 8 agents, global information. Distinct
# styles keep overlapping lines legible (cooperative and sanctioning both sit at 50).
SCENARIOS: dict[str, tuple[list[AgentSpec], dict]] = {
    "8 selfish": (
        [AgentSpec("selfish", 8, SELFISH)],
        {"color": "tab:blue", "ls": "-"},
    ),
    "8 cooperative": (
        [AgentSpec("cooperative", 8, COOP)],
        {"color": "tab:orange", "ls": "-", "lw": 3, "alpha": 0.9},
    ),
    "4 conditional + 4 selfish": (
        [AgentSpec("conditional_cooperator", 4, COOP), AgentSpec("selfish", 4, SELFISH)],
        {"color": "tab:green", "ls": "--"},
    ),
    "4 sanctioning + 4 selfish": (
        [AgentSpec("sanctioning", 4, SANCTION), AgentSpec("selfish", 4, SELFISH)],
        {"color": "tab:red", "ls": ":", "lw": 2},
    ),
}


def _run(agents: list[AgentSpec]) -> RunResult:
    cfg = SimulationConfig(
        name="trajectory",
        rounds=ROUNDS,
        information_model="global",
        resource=ResourceConfig(
            initial_level=50.0, capacity=100.0, regeneration_rate=0.4, collapse_threshold=1.0
        ),
        agents=tuple(agents),
    )
    return run_simulation(cfg, seed=1)


def make_figure(path: Path) -> None:
    """Plot standing stock and per-round harvest over time for each scenario."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.6))
    for label, (agents, style) in SCENARIOS.items():
        result = _run(agents)
        rounds = [r.round_index for r in result.rounds]
        stock = [r.resource_after_harvest for r in result.rounds]
        harvest = [r.total_harvested for r in result.rounds]
        ax1.plot(rounds, stock, label=label, **style)
        ax2.plot(rounds, harvest, label=label, **style)

    ax1.axhline(50, color="grey", ls=":", lw=1)  # healthy stock K/2
    ax1.set_xlabel("round")
    ax1.set_ylabel("standing stock (after harvest)")
    ax1.set_title("A. Resource over time")
    ax1.set_ylim(-2, 100)
    ax1.legend(fontsize=8)

    ax2.axhline(10, color="grey", ls=":", lw=1)  # MSY
    ax2.set_xlabel("round")
    ax2.set_ylabel("total harvest this round")
    ax2.set_title("B. Harvest over time (dotted = sustainable yield)")
    ax2.legend(fontsize=8)

    fig.suptitle("Round-by-round dynamics: how each mechanism plays out over time")
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)


def main() -> None:
    """Generate the trajectory comparison figure."""
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    make_figure(OUT_DIR / "figure.png")
    print(f"Wrote {OUT_DIR / 'figure.png'}")


if __name__ == "__main__":
    main()
