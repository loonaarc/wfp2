"""Experiment E7: given communication, does the *response rule* save the commons?

E6 showed communication lets agents detect free-riders but that a *retaliation*
response protects fairness, not the resource. Does a *restraint* response do better —
and can any peer response match *enforcement*?

Under private information with a reliable broadcast (so every cooperator can detect
over-extraction), we compare three responses to detected over-extraction, each mixed
with a growing number of selfish free-riders:

* ``conditional_cooperator`` — **retaliate** (grab a selfish share),
* ``compensating_cooperator`` — **restrain** (withhold to let the pool recover),
* ``sanctioning`` — **enforce** (cap everyone's harvest; ignores the signal).

Outputs go to ``results/E7_response_rules/``. Run with::

    python scripts/experiment_response_rules.py

Write-up: ``docs/experiments/E7-response-rules.md``.
"""

from __future__ import annotations

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

OUT_DIR = Path(__file__).resolve().parent.parent / "results" / "E7_response_rules"
RESPONSES = {
    "conditional_cooperator": "retaliate",
    "compensating_cooperator": "restrain",
    "sanctioning": "enforce",
}


def _experiment(cooperator_type, n_selfish):
    params = {"regeneration_rate": 0.4, "capacity": 100.0}
    if cooperator_type == "sanctioning":
        params["monitoring_cost"] = 0.2
    agents = []
    if 8 - n_selfish > 0:
        agents.append(AgentSpec(cooperator_type, 8 - n_selfish, params))
    if n_selfish > 0:
        agents.append(AgentSpec("selfish", n_selfish, {"greed": 1.0}))
    sim = SimulationConfig(
        name=f"E7_{cooperator_type}_{n_selfish}",
        rounds=100,
        information_model="private",
        broadcast_reliability=1.0,  # perfect communication: isolate the response rule
        resource=ResourceConfig(
            initial_level=50.0, capacity=100.0, regeneration_rate=0.4, collapse_threshold=1.0
        ),
        agents=tuple(agents),
    )
    # Broadcast at reliability 1.0 is deterministic; a single seed suffices.
    return ExperimentConfig(simulation=sim, seeds=(1,), record_history=False)


def run_sweep() -> pd.DataFrame:
    """Sweep response rule x number of selfish; record sustainability and fairness."""
    rows = []
    for ctype in RESPONSES:
        for n_selfish in range(8):
            m = run_experiment(_experiment(ctype, n_selfish)).metrics
            rows.append(
                {
                    "response": RESPONSES[ctype],
                    "n_selfish": n_selfish,
                    "sustainability": m["sustainability_ratio"].mean(),
                    "gini": m["payoff_gini"].mean(),
                }
            )
    return pd.DataFrame(rows)


def make_figure(df: pd.DataFrame, path: Path) -> None:
    """Two panels: sustainability and fairness vs. number of selfish, per response."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.4))
    for response in RESPONSES.values():
        sub = df[df["response"] == response].sort_values("n_selfish")
        ax1.plot(sub["n_selfish"], sub["sustainability"], marker="o", label=response)
        ax2.plot(sub["n_selfish"], sub["gini"], marker="s", label=response)
    ax1.set_xlabel("number of selfish agents (of 8)")
    ax1.set_ylabel("sustainability ratio")
    ax1.set_title("A. Does the resource survive?")
    ax1.set_ylim(-0.02, 0.6)
    ax1.legend(title="response to over-extraction")
    ax2.set_xlabel("number of selfish agents (of 8)")
    ax2.set_ylabel("payoff Gini (lower = fairer)")
    ax2.set_title("B. Is payoff fair?")
    ax2.set_ylim(-0.02, 0.9)
    ax2.legend(title="response")
    fig.suptitle(
        "E7: given communication, only enforcement saves the commons —\n"
        "peer responses (retaliate / restrain) do not"
    )
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)


def main() -> None:
    """Run the response-rule sweep, export CSV + figure, print a summary."""
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    df = run_sweep()
    df.to_csv(OUT_DIR / "sweep.csv", index=False)
    make_figure(df, OUT_DIR / "figure.png")
    print("Sustainability by response x number of selfish (private info, perfect broadcast):")
    print(
        df.pivot(index="n_selfish", columns="response", values="sustainability")
        .round(2)
        .to_string()
    )
    print(f"\nWrote sweep.csv and figure.png to: {OUT_DIR}")


if __name__ == "__main__":
    main()
