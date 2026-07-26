"""Animate a single run: a central resource pool with agents around it, over time.

This is an **illustrative** view of the (non-spatial) model, for intuition and
presentations — *not* a spatial simulation. The ring layout is decorative: our agents
have no positions and the resource is one shared scalar. Each frame is one round; the
central disc's area tracks the resource stock, agents are coloured by strategy and grow
with cumulative payoff, and a line from an agent to the centre shows how much it
harvested that round.

Outputs animated GIFs to ``results/animations/``. Run with::

    python scripts/animate_run.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.animation import FuncAnimation, PillowWriter  # noqa: E402

from emergent_cooperation.core.config import (  # noqa: E402
    AgentSpec,
    ResourceConfig,
    SimulationConfig,
)
from emergent_cooperation.core.simulation import run_simulation
from emergent_cooperation.core.state import RunResult  # noqa: E402

OUT_DIR = Path(__file__).resolve().parent.parent / "results" / "animations"
CAPACITY = 100.0
ROUNDS = 40
STRATEGY_COLORS = {
    "selfish": "#d62728",
    "cooperative": "#1f77b4",
    "conditional_cooperator": "#ff7f0e",
    "compensating_cooperator": "#9467bd",
    "sanctioning": "#2ca02c",
}


def _run(agents: list[AgentSpec]) -> RunResult:
    cfg = SimulationConfig(
        name="anim",
        rounds=ROUNDS,
        information_model="global",
        resource=ResourceConfig(
            initial_level=CAPACITY / 2,
            capacity=CAPACITY,
            regeneration_rate=0.4,
            collapse_threshold=1.0,
        ),
        agents=tuple(agents),
    )
    return run_simulation(cfg, seed=1)


def _pool_color(ratio: float):
    """Green when full, red when empty."""
    ratio = max(0.0, min(1.0, ratio))
    return (1.0 - ratio, 0.35 + 0.45 * ratio, 0.25)


def make_animation(result: RunResult, label: str, capacity: float = CAPACITY):
    """Build a ``(fig, FuncAnimation)`` of a run: a central pool with agents in a ring.

    Reusable by both the GIF exporter here and the interactive notebook (via
    ``anim.to_jshtml()``). The cumulative payoff is recomputed from scratch each frame,
    so re-rendering (as ``to_jshtml`` does) stays correct.
    """
    n = result.num_agents
    strategies = result.agent_strategies
    total = len(result.rounds)
    harvested = np.array([r.harvested for r in result.rounds])  # (rounds, agents)
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False) + np.pi / 2
    ax_x, ax_y = np.cos(angles), np.sin(angles)  # agent positions on a unit ring (decorative)
    colors = [STRATEGY_COLORS.get(s, "grey") for s in strategies]

    fig, ax = plt.subplots(figsize=(6, 6))

    def draw(t: int):
        ax.clear()
        ax.set_xlim(-1.4, 1.4)
        ax.set_ylim(-1.4, 1.4)
        ax.set_aspect("equal")
        ax.axis("off")

        rec = result.rounds[t]
        stock = rec.resource_after_harvest
        ratio = stock / capacity
        # Central pool: area tracks the stock.
        pool_r = 0.15 + 0.45 * np.sqrt(max(ratio, 0.0))
        ax.add_patch(plt.Circle((0, 0), pool_r, color=_pool_color(ratio), zorder=1))
        ax.text(0, 0, f"{stock:.0f}", ha="center", va="center", color="white",
                fontweight="bold", zorder=3)

        # Harvest lines (agent -> pool); width/alpha tracks this round's harvest.
        max_h = max(rec.harvested) if any(rec.harvested) else 1.0
        for i in range(n):
            h = rec.harvested[i]
            if h > 1e-6:
                ax.plot([ax_x[i], 0], [ax_y[i], 0], color="grey",
                        lw=0.5 + 4 * h / max_h, alpha=0.2 + 0.6 * h / max_h, zorder=2)

        # Agents: colour by strategy, size grows with cumulative payoff so far.
        sizes = 120 + 12 * harvested[: t + 1].sum(axis=0)
        ax.scatter(ax_x, ax_y, s=sizes, c=colors, edgecolors="white", linewidths=1.2, zorder=4)

        status = "COLLAPSED" if rec.collapsed else "alive"
        ax.set_title(
            f"{label}\nround {t + 1}/{total}   stock={stock:.0f}/{capacity:.0f}   {status}",
            fontsize=11,
        )

    return fig, FuncAnimation(fig, draw, frames=total, interval=250)


def animate(agents: list[AgentSpec], label: str, path: Path) -> None:
    """Render one run to an animated GIF file."""
    fig, anim = make_animation(_run(agents), label)
    anim.save(path, writer=PillowWriter(fps=4))
    plt.close(fig)
    print(f"Wrote {path}")


def main() -> None:
    """Render a sustaining and a collapsing scenario."""
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    coop = {"regeneration_rate": 0.4, "capacity": 100.0}
    sanction = {"regeneration_rate": 0.4, "capacity": 100.0, "monitoring_cost": 0.2}
    animate(
        [AgentSpec("cooperative", 6, coop), AgentSpec("selfish", 2, {"greed": 1.0})],
        "6 cooperative + 2 selfish (tragedy unfolds)",
        OUT_DIR / "cooperative_vs_selfish.gif",
    )
    animate(
        [AgentSpec("sanctioning", 4, sanction), AgentSpec("selfish", 4, {"greed": 1.0})],
        "4 sanctioning + 4 selfish (enforcement holds)",
        OUT_DIR / "sanctioning_vs_selfish.gif",
    )


if __name__ == "__main__":
    main()
