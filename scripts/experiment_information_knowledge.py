"""Experiment E1: information, ecological knowledge, and sustainable cooperation.

Tests hypotheses H1 and H6 (see docs/research-questions.md) with an all-cooperative
population, isolating two factors:

* **Sweep A (information x initial stock).** Does an all-cooperative population sustain
  the resource from any starting stock, and does that depend on whether agents can
  observe the stock (global vs private information)?
* **Sweep B (ecological knowledge).** When agents are blind (private info), how does a
  biased estimate of the sustainable yield (``knowledge_bias``) affect sustainability
  — and is global information robust to the same bias (information substituting for
  knowledge)?

Outputs go to ``results/E1_information_knowledge/``: tidy CSVs and a two-panel figure.
Run with::

    python scripts/experiment_information_knowledge.py

The write-up lives in ``docs/experiments/E1-information-and-knowledge.md``.
"""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # headless: render to file, no display needed
import matplotlib.pyplot as plt  # noqa: E402

from emergent_cooperation.core.config import (  # noqa: E402
    AgentSpec,
    ExperimentConfig,
    ResourceConfig,
    SimulationConfig,
)
from emergent_cooperation.experiments.sweep import run_grid, with_resource  # noqa: E402

OUT_DIR = Path(__file__).resolve().parent.parent / "results" / "E1_information_knowledge"
SEEDS = (1, 2, 3, 4, 5)


def base_experiment() -> ExperimentConfig:
    """All-cooperative population with accurate knowledge, at the healthy stock."""
    simulation = SimulationConfig(
        name="E1",
        rounds=100,
        information_model="global",
        resource=ResourceConfig(
            initial_level=50.0, capacity=100.0, regeneration_rate=0.4, collapse_threshold=1.0
        ),
        agents=(
            AgentSpec(
                strategy="cooperative",
                count=8,
                params={"regeneration_rate": 0.4, "capacity": 100.0, "knowledge_bias": 1.0},
            ),
        ),
    )
    return ExperimentConfig(simulation=simulation, seeds=SEEDS, record_history=False)


def _set_knowledge_bias(simulation: SimulationConfig, bias: float) -> SimulationConfig:
    """Return a copy with every cooperative agent group's knowledge_bias set."""
    new_agents = tuple(
        replace(spec, params={**spec.params, "knowledge_bias": bias})
        if spec.strategy == "cooperative"
        else spec
        for spec in simulation.agents
    )
    return replace(simulation, agents=new_agents)


def sweep_information(base: ExperimentConfig):
    """Sweep A: initial stock x information model (knowledge accurate)."""
    axes = {
        "initial_level": [10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0],
        "information_model": ["global", "private"],
    }

    def make(sim: SimulationConfig, combo: dict) -> SimulationConfig:
        sim = with_resource(sim, initial_level=combo["initial_level"])
        return replace(sim, information_model=combo["information_model"])

    return run_grid(base, axes, make)


def sweep_knowledge(base: ExperimentConfig):
    """Sweep B: knowledge bias x information model (initial stock at K/2)."""
    axes = {
        "knowledge_bias": [0.6, 0.8, 1.0, 1.2, 1.4],
        "information_model": ["global", "private"],
    }

    def make(sim: SimulationConfig, combo: dict) -> SimulationConfig:
        sim = _set_knowledge_bias(sim, combo["knowledge_bias"])
        return replace(sim, information_model=combo["information_model"])

    return run_grid(base, axes, make)


def _mean_by(df, group_cols, value="sustainability_ratio"):
    """Mean of ``value`` grouped by ``group_cols`` (seeds averaged out)."""
    return df.groupby(group_cols)[value].mean().reset_index()


def make_figure(info_df, knowledge_df, path: Path) -> None:
    """Two-panel figure: sustainability vs initial stock, and vs knowledge bias."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2))

    a = _mean_by(info_df, ["information_model", "initial_level"])
    for model in ["global", "private"]:
        sub = a[a["information_model"] == model].sort_values("initial_level")
        ax1.plot(sub["initial_level"], sub["sustainability_ratio"], marker="o", label=model)
    ax1.axvline(50, color="grey", ls=":", lw=1, label="K/2 (healthy stock)")
    ax1.set_xlabel("initial stock")
    ax1.set_ylabel("sustainability ratio (final stock / K)")
    ax1.set_title("A. Information vs initial stock\n(accurate knowledge)")
    ax1.set_ylim(-0.02, 1.0)
    ax1.legend()

    b = _mean_by(knowledge_df, ["information_model", "knowledge_bias"])
    for model in ["global", "private"]:
        sub = b[b["information_model"] == model].sort_values("knowledge_bias")
        ax2.plot(sub["knowledge_bias"], sub["sustainability_ratio"], marker="s", label=model)
    ax2.axvline(1.0, color="grey", ls=":", lw=1, label="accurate knowledge")
    ax2.set_xlabel("knowledge bias (blind yield estimate / true MSY)")
    ax2.set_ylabel("sustainability ratio")
    ax2.set_title("B. Ecological knowledge\n(initial stock = K/2)")
    ax2.set_ylim(-0.02, 1.0)
    ax2.legend()

    fig.suptitle("E1: cooperation sustains the resource only with information OR knowledge")
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)


def main() -> None:
    """Run both sweeps, export CSVs and the figure, and print summaries."""
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    base = base_experiment()

    info_df = sweep_information(base)
    knowledge_df = sweep_knowledge(base)

    info_df.to_csv(OUT_DIR / "sweep_information.csv", index=False)
    knowledge_df.to_csv(OUT_DIR / "sweep_knowledge.csv", index=False)
    make_figure(info_df, knowledge_df, OUT_DIR / "figure.png")

    print("Sweep A — sustainability ratio by information model x initial stock:")
    print(
        _mean_by(info_df, ["information_model", "initial_level"])
        .pivot(index="initial_level", columns="information_model", values="sustainability_ratio")
        .round(3)
        .to_string()
    )
    print("\nSweep B — sustainability ratio by information model x knowledge bias:")
    print(
        _mean_by(knowledge_df, ["information_model", "knowledge_bias"])
        .pivot(index="knowledge_bias", columns="information_model", values="sustainability_ratio")
        .round(3)
        .to_string()
    )
    print(f"\nWrote CSVs and figure.png to: {OUT_DIR}")


if __name__ == "__main__":
    main()
