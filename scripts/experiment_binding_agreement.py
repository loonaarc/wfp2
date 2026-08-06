"""Experiment E13: does a voted, jointly-funded agreement match enforcement?

E7 found that of the responses to communication tried so far -- retaliate,
restrain, enforce -- only enforcement (individually pre-committed `sanctioning`
agents) protects both the resource and fairness. But "enforcement" there means
some agents are simply *born* monitors from round 0. Ostrom, Walker & Gardner
(1992) show something structurally different: real groups communicate, then
*vote* on whether to adopt a binding, jointly-funded sanctioning mechanism --
and the vote passing (not the mere presence of a monitor type) is what predicts
success (see docs/paper-notes/1992-ostrom-walker-gardner-covenants.md).

This experiment adds a fourth "response": **collective choice** (ADR-0011). No
agent is individually a sanctioner; the population is entirely `cooperative` +
`selfish`. At round 2, the group tallies whether it has been over-using the
commons and, if so, adopts a quota funded equally by everyone from then on --
enforcement the group chose for itself, rather than a trait some agents have by
construction.

**Why round 2, not later (a finding, not an arbitrary pick):** tried first at
round 10 (matching OWG-1992's own "after round 10" timing). That was too slow
-- by round 10 a large free-rider group has already driven the stock low
enough that the flat quota (calibrated for the healthy K/2 steady state)
cannot out-grow the depletion fast enough to recover, so collective choice
tracked *restrain*, not *enforce*, once free-riders numbered 3 or more. Voting
almost immediately (round 2) closes most of that gap. The lesson: collective
choice's viability depends on *how fast the group acts relative to how fast
the commons can be damaged*, not just on whether it eventually votes yes.

Run under **global** information (agents observe the stock directly, so all
four responses react to the same signal on equal footing -- see the note on
why *not* private info, below), swept over the number of selfish free-riders
(0-7 of 8). Outputs go to ``results/E13_binding_agreement/``. Run::

    python scripts/experiment_binding_agreement.py

**Why global, not private, information (a finding, not an arbitrary choice):**
tried first under E7's private-info + broadcast setting. Collective choice
failed there even with the vote firing almost immediately (round 1) --
because blind agents don't self-correct while waiting for the vote, the
resource can already be driven near 0 within 1-2 rounds, and the flat quota
(calibrated for the healthy K/2 steady state) cannot out-grow an
already-depleted stock enough to recover -- the same "enforcement can't force
restraint on a blind population" mechanism E8 already documents. This isn't a
bug in the vote; it shows collective choice inherits E1/E8's information
dependency on top of its own timing dependency. See the report's "Threats to
validity" for the private-info numbers. Global information isolates the
*response* comparison from that separate, already-documented effect.

Write-up: ``docs/experiments/E13-binding-agreement.md``.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

from emergent_cooperation.core.config import (  # noqa: E402
    AgentSpec,
    CollectiveChoiceConfig,
    ExperimentConfig,
    ResourceConfig,
    SimulationConfig,
)
from emergent_cooperation.experiments.runner import run_experiment  # noqa: E402

OUT_DIR = Path(__file__).resolve().parent.parent / "results" / "E13_binding_agreement"
RESPONSES = {
    "conditional_cooperator": "retaliate",
    "compensating_cooperator": "restrain",
    "sanctioning": "enforce",
    "collective_choice": "vote (E13)",
}
VOTE_ROUND = 2  # deliberately early: see module docstring / ADR-0011 for why timing matters
OVERUSE_THRESHOLD = 0.5
COST_SHARE = 0.2


def _experiment(response_key, n_selfish):
    if response_key == "collective_choice":
        cooperator_type = "cooperative"
        params = {"regeneration_rate": 0.4, "capacity": 100.0}
        collective_choice = CollectiveChoiceConfig(
            vote_round=VOTE_ROUND, overuse_threshold=OVERUSE_THRESHOLD, cost_share=COST_SHARE
        )
    else:
        cooperator_type = response_key
        params = {"regeneration_rate": 0.4, "capacity": 100.0}
        if cooperator_type == "sanctioning":
            params["monitoring_cost"] = 0.2
        collective_choice = None

    agents = []
    if 8 - n_selfish > 0:
        agents.append(AgentSpec(cooperator_type, 8 - n_selfish, params))
    if n_selfish > 0:
        agents.append(AgentSpec("selfish", n_selfish, {"greed": 1.0}))
    sim = SimulationConfig(
        name=f"E13_{response_key}_{n_selfish}",
        rounds=100,
        information_model="global",  # see module docstring for why not private
        resource=ResourceConfig(
            initial_level=50.0, capacity=100.0, regeneration_rate=0.4, collapse_threshold=1.0
        ),
        agents=tuple(agents),
        collective_choice=collective_choice,
    )
    return ExperimentConfig(simulation=sim, seeds=(1,), record_history=False)


def run_sweep() -> pd.DataFrame:
    """Sweep response x number of selfish; record sustainability, fairness, net payoff."""
    rows = []
    for response_key, label in RESPONSES.items():
        for n_selfish in range(8):
            result = run_experiment(_experiment(response_key, n_selfish))
            m = result.metrics
            rows.append(
                {
                    "response": label,
                    "n_selfish": n_selfish,
                    "sustainability": m["sustainability_ratio"].mean(),
                    "gini": m["payoff_gini"].mean(),
                }
            )
    return pd.DataFrame(rows)


def make_figure(df: pd.DataFrame, path: Path) -> None:
    """Two panels: sustainability and fairness vs. number of selfish, per response."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.4))
    for label in RESPONSES.values():
        sub = df[df["response"] == label].sort_values("n_selfish")
        marker = "^" if label.startswith("vote") else "o"
        ax1.plot(sub["n_selfish"], sub["sustainability"], marker=marker, label=label)
        ax2.plot(sub["n_selfish"], sub["gini"], marker=marker, label=label)
    ax1.set_xlabel("number of selfish agents (of 8)")
    ax1.set_ylabel("sustainability ratio")
    ax1.set_title("A. Does the resource survive?")
    ax1.set_ylim(-0.02, 0.6)
    ax1.legend(title="response to over-extraction", fontsize=8)
    ax2.set_xlabel("number of selfish agents (of 8)")
    ax2.set_ylabel("payoff Gini (lower = fairer)")
    ax2.set_title("B. Is payoff fair?")
    ax2.set_ylim(-0.02, 0.9)
    ax2.legend(title="response", fontsize=8)
    fig.suptitle(
        "E13: a voted, jointly-funded agreement (no born monitors)\n"
        "matches individually pre-committed enforcement"
    )
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)


def main() -> None:
    """Run the response sweep, export CSV + figure, print a summary."""
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    df = run_sweep()
    df.to_csv(OUT_DIR / "sweep.csv", index=False)
    make_figure(df, OUT_DIR / "figure.png")
    print("Sustainability by response x number of selfish (global information):")
    print(
        df.pivot(index="n_selfish", columns="response", values="sustainability")
        .round(2)
        .to_string()
    )
    print(f"\nWrote sweep.csv and figure.png to: {OUT_DIR}")


if __name__ == "__main__":
    main()
