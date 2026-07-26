"""Experiment E3: sanctioning — can enforcement protect resource *and* fairness?

Follows up E2. Compares three cooperator mechanisms against a growing selfish
minority:

* ``cooperative`` — unconditional restraint (self-correcting),
* ``conditional_cooperator`` — reciprocity (retaliate on over-extraction),
* ``sanctioning`` — cooperate *and* enforce a sustainable harvest quota, at a
  monitoring cost (ADR-0005).

It also measures the **second-order free-rider** problem: in a group of sanctioners
plus plain cooperators, do the non-monitoring cooperators out-earn the monitors?

Outputs go to ``results/E3_sanctioning/``. Run with::

    python scripts/experiment_sanctioning.py

Write-up: ``docs/experiments/E3-sanctioning.md``.
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
    ExperimentConfig,
    ResourceConfig,
    SimulationConfig,
)
from emergent_cooperation.experiments.runner import run_experiment  # noqa: E402

OUT_DIR = Path(__file__).resolve().parent.parent / "results" / "E3_sanctioning"
SEEDS = (1, 2, 3)
GROUP_SIZE = 8
COOP_PARAMS = {"regeneration_rate": 0.4, "capacity": 100.0}
SANCTION_PARAMS = {"regeneration_rate": 0.4, "capacity": 100.0, "monitoring_cost": 0.2}
SELFISH_PARAMS = {"greed": 1.0}
TYPES = ["cooperative", "conditional_cooperator", "sanctioning"]
LABELS = {
    "cooperative": "unconditional",
    "conditional_cooperator": "conditional",
    "sanctioning": "sanctioning",
}


def _params(strategy: str) -> dict:
    return dict(SANCTION_PARAMS) if strategy == "sanctioning" else dict(COOP_PARAMS)


def _resource() -> ResourceConfig:
    return ResourceConfig(
        initial_level=50.0, capacity=100.0, regeneration_rate=0.4, collapse_threshold=1.0
    )


def _experiment(agents: list[AgentSpec], name: str) -> ExperimentConfig:
    sim = SimulationConfig(
        name=name,
        rounds=100,
        information_model="global",
        resource=_resource(),
        agents=tuple(agents),
    )
    return ExperimentConfig(simulation=sim, seeds=SEEDS, record_history=False)


def _payoff_by_strategy(results) -> dict[str, float]:
    sums: dict[str, list[float]] = defaultdict(list)
    for result in results:
        for strategy, payoff in zip(result.agent_strategies, result.total_payoffs(), strict=True):
            sums[strategy].append(payoff)
    return {s: sum(v) / len(v) for s, v in sums.items()}


def run_sweep() -> pd.DataFrame:
    """Sweep cooperator type x number of selfish agents."""
    rows = []
    for cooperator_type in TYPES:
        for n_selfish in range(GROUP_SIZE + 1):
            n_coop = GROUP_SIZE - n_selfish
            agents = []
            if n_coop > 0:
                agents.append(AgentSpec(cooperator_type, n_coop, _params(cooperator_type)))
            if n_selfish > 0:
                agents.append(AgentSpec("selfish", n_selfish, dict(SELFISH_PARAMS)))
            outcome = run_experiment(_experiment(agents, f"E3_{cooperator_type}_{n_selfish}"))
            m = outcome.metrics
            payoffs = _payoff_by_strategy(outcome.results)
            rows.append(
                {
                    "cooperator_type": cooperator_type,
                    "n_selfish": n_selfish,
                    "sustainability_ratio": m["sustainability_ratio"].mean(),
                    "payoff_gini": m["payoff_gini"].mean(),
                    "cooperator_payoff": payoffs.get(cooperator_type, float("nan")),
                    "selfish_payoff": payoffs.get("selfish", float("nan")),
                }
            )
    return pd.DataFrame(rows)


def second_order_free_rider() -> pd.DataFrame:
    """Sanctioners mixed with plain cooperators (+ 1 selfish): who earns more?"""
    agents = [
        AgentSpec("sanctioning", 3, dict(SANCTION_PARAMS)),
        AgentSpec("cooperative", 4, dict(COOP_PARAMS)),
        AgentSpec("selfish", 1, dict(SELFISH_PARAMS)),
    ]
    outcome = run_experiment(_experiment(agents, "E3_second_order"))
    payoffs = _payoff_by_strategy(outcome.results)
    return pd.DataFrame([{"strategy": s, "mean_payoff": round(p, 2)} for s, p in payoffs.items()])


def make_figure(df: pd.DataFrame, path: Path) -> None:
    """Two panels: resource survival and payoff inequality vs. number of selfish."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2))
    for ctype in TYPES:
        sub = df[df["cooperator_type"] == ctype].sort_values("n_selfish")
        ax1.plot(sub["n_selfish"], sub["sustainability_ratio"], marker="o", label=LABELS[ctype])
        ax2.plot(sub["n_selfish"], sub["payoff_gini"], marker="s", label=LABELS[ctype])
    ax1.set_xlabel("number of selfish agents (of 8)")
    ax1.set_ylabel("sustainability ratio (final stock / K)")
    ax1.set_title("A. Does the resource survive?")
    ax1.set_ylim(-0.02, 0.6)
    ax1.legend()
    ax2.set_xlabel("number of selfish agents (of 8)")
    ax2.set_ylabel("payoff Gini (0 = equal)")
    ax2.set_title("B. Is payoff fair?")
    ax2.set_ylim(-0.02, 0.8)
    ax2.legend()
    fig.suptitle("E3: only sanctioning protects both the resource and fairness")
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)


def main() -> None:
    """Run the sweep and the second-order analysis; export and summarise."""
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    df = run_sweep()
    df.to_csv(OUT_DIR / "sweep.csv", index=False)
    make_figure(df, OUT_DIR / "figure.png")

    so = second_order_free_rider()
    so.to_csv(OUT_DIR / "second_order.csv", index=False)

    print("Sustainability ratio by cooperator type x number of selfish:")
    print(
        df.pivot(index="n_selfish", columns="cooperator_type", values="sustainability_ratio")
        .round(3)
        .to_string()
    )
    print("\nPayoff Gini by cooperator type x number of selfish:")
    print(
        df.pivot(index="n_selfish", columns="cooperator_type", values="payoff_gini")
        .round(3)
        .to_string()
    )
    print("\nSecond-order free-rider (3 sanctioning + 4 cooperative + 1 selfish):")
    print(so.to_string(index=False))
    print(f"\nWrote outputs to: {OUT_DIR}")


if __name__ == "__main__":
    main()
