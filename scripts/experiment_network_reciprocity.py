"""Experiment E19: network reciprocity -- does fixed graph position matter?

Nowak (2006), "Five Rules for the Evolution of Cooperation," rule 4 (network
reciprocity): relax the well-mixed assumption -- individuals occupy the
vertices of a graph and interact only with their `k` graph neighbours, not
the whole population. Cooperators can then survive by forming clusters that
mutually protect each other, favoured when `b/c > k`.

E18 (ADR-0014) already made reputation *partner-specific* rather than
population-wide, but the partner is a fresh, uniformly random draw every
round -- closer to Nowak's rule 3 (indirect reciprocity) than rule 4. This
experiment adds the one ingredient E18 doesn't have: a *fixed, persistent*
neighbour graph (a ring lattice, ADR-0015), built once per run from agent
order. That persistence is what lets an agent's outcome depend on its graph
*position* -- something no well-mixed mechanism in this project (E18's
reputation, E14's diversity) can produce even in principle, since none of
them have a notion of position at all.

Two questions, both testing the same mechanism from different angles:

A. **Position-dependent inequality.** With a sparse ring (k=2) and one
   free-rider at a fixed position, do the free-rider's two fixed neighbours
   pay a real, measurable cost that agents on the opposite side of the ring
   never see -- something well-mixed reputation (E18) cannot produce, because
   every agent there has equal expected exposure to the free-rider?
B. **Aggregate effect of degree.** Sweeping k from sparse to well-mixed
   (k = N-2, "almost everyone is a neighbour"), does a sparser network
   protect the *population's* sustainability better, worse, or about the
   same as well-mixed reputation?

Note on scope (see ADR-0015): this does NOT literally test `b/c > k`.
Monitoring/enforcement's benefit in this project's single shared pool is a
population-wide public good (protecting the pool benefits everyone equally,
regardless of who paid to protect it), so it cannot produce the local payoff
variance Nowak's formalism assumes -- which is why an earlier draft of this
experiment (graph-structured *evolutionary* dynamics on top of E5/E11/E12)
was abandoned. Reputation's partner-conditioned harvest decision, by
contrast, *is* a genuinely individual, position-dependent interaction, so
fixing its partner graph is where this project's mechanics can actually
support Nowak's qualitative claim (persistence changes outcomes), even
though the exact threshold formula does not transfer.

Outputs go to ``results/E19_network_reciprocity/``. Run::

    python scripts/experiment_network_reciprocity.py

Write-up: ``docs/experiments/E19-network-reciprocity.md``.
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
    NetworkConfig,
    ReputationConfig,
    ResourceConfig,
    SimulationConfig,
)
from emergent_cooperation.experiments.runner import run_experiment  # noqa: E402

OUT_DIR = Path(__file__).resolve().parent.parent / "results" / "E19_network_reciprocity"
SEEDS = tuple(range(1, 21))  # 20 seeds -- a 2-vs-5-agent split needs averaging
N = 8
COOP_PARAMS = {"regeneration_rate": 0.4, "capacity": 100.0}
SELFISH_PARAMS = {"greed": 1.0}
# The free-rider sits at agent index 0 (first AgentSpec). On an N=8 ring with
# degree=2, its only fixed neighbours are agents 1 and 7.
ADJACENT_IDX = (1, 7)
FAR_IDX = (2, 3, 4, 5, 6)
DEGREES = (2, 4, 6)  # 6 = N-2, the sparsest even degree still short of "everyone" (N-1=7, odd)


def _config(network: NetworkConfig | None) -> ExperimentConfig:
    """1 selfish (index 0) + 7 reputation_cooperator (indices 1-7), full visibility."""
    agents = (
        AgentSpec("selfish", count=1, params=dict(SELFISH_PARAMS)),
        AgentSpec("reputation_cooperator", count=N - 1, params=dict(COOP_PARAMS)),
    )
    sim = SimulationConfig(
        name=f"E19_deg{network.degree if network else 'mixed'}",
        rounds=100,
        information_model="global",
        resource=ResourceConfig(
            initial_level=50.0, capacity=100.0, regeneration_rate=0.4, collapse_threshold=1.0
        ),
        agents=agents,
        reputation=ReputationConfig(visibility=1.0),
        network=network,
    )
    return ExperimentConfig(simulation=sim, seeds=SEEDS, record_history=False)


def run_degree_sweep() -> pd.DataFrame:
    """Question B: population-level sustainability/welfare vs. degree, plus well-mixed."""
    rows = []
    configs = [(k, NetworkConfig(degree=k)) for k in DEGREES] + [("well-mixed", None)]
    for label, network in configs:
        outcome = run_experiment(_config(network))
        m = outcome.metrics
        rows.append(
            {
                "degree": label,
                "sustainability_ratio": m["sustainability_ratio"].mean(),
                "welfare_efficiency": m["welfare_efficiency"].mean(),
                "collapsed": m["collapsed"].mean(),
            }
        )
    return pd.DataFrame(rows)


def run_position_comparison() -> pd.DataFrame:
    """Question A: does fixed graph position change individual payoff?

    At degree=2, do the free-rider's fixed neighbours earn differently than
    agents on the far side of the ring? Compared against well-mixed, where
    "position" doesn't exist, as the control.
    """
    rows = []
    for label, network in [("network (k=2)", NetworkConfig(degree=2)), ("well-mixed", None)]:
        outcome = run_experiment(_config(network))
        adjacent, far = [], []
        for result in outcome.results:
            payoffs = result.total_payoffs()
            adjacent.extend(payoffs[i] for i in ADJACENT_IDX)
            far.extend(payoffs[i] for i in FAR_IDX)
        rows.append(
            {
                "condition": label,
                "adjacent_mean": sum(adjacent) / len(adjacent),
                "adjacent_std": pd.Series(adjacent).std(),
                "far_mean": sum(far) / len(far),
                "far_std": pd.Series(far).std(),
            }
        )
    return pd.DataFrame(rows)


def make_figure(degree_df: pd.DataFrame, position_df: pd.DataFrame, path: Path) -> None:
    """Two panels: A. sustainability/welfare vs. degree; B. adjacent-vs-far payoff by condition."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 4.4))

    x = range(len(degree_df))
    labels = [str(d) for d in degree_df["degree"]]
    ax1.bar(x, degree_df["sustainability_ratio"], color="#2ca02c", alpha=0.85)
    ax1.set_xticks(list(x))
    ax1.set_xticklabels(labels)
    ax1.set_xlabel("graph degree k (neighbours per node) -- 'well-mixed' = E18's own setup")
    ax1.set_ylabel("sustainability ratio (mean of 20 seeds)")
    ax1.set_title("A. Population outcome vs. network degree")
    ax1.set_ylim(0, max(0.55, degree_df["sustainability_ratio"].max() * 1.15))

    width = 0.35
    conds = position_df["condition"].tolist()
    xpos = range(len(conds))
    ax2.bar(
        [p - width / 2 for p in xpos], position_df["adjacent_mean"], width,
        yerr=position_df["adjacent_std"], capsize=4, label="agents adjacent to the free-rider",
        color="#d62728",
    )
    ax2.bar(
        [p + width / 2 for p in xpos], position_df["far_mean"], width,
        yerr=position_df["far_std"], capsize=4, label="agents on the far side of the ring",
        color="#1f77b4",
    )
    ax2.set_xticks(list(xpos))
    ax2.set_xticklabels(conds)
    ax2.set_ylabel("mean individual payoff (± sd, 20 seeds)")
    ax2.set_title("B. Does graph position change individual payoff?")
    ax2.legend(fontsize=8)

    fig.suptitle("E19: network reciprocity -- fixed graph position, not a fresh random partner")
    fig.tight_layout(rect=(0.0, 0.0, 1.0, 0.94))
    fig.savefig(path, dpi=130)
    plt.close(fig)


def main() -> None:
    """Run both comparisons, export tables and figure, print a summary."""
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    degree_df = run_degree_sweep()
    degree_df.to_csv(OUT_DIR / "degree_sweep.csv", index=False)
    position_df = run_position_comparison()
    position_df.to_csv(OUT_DIR / "position_comparison.csv", index=False)
    make_figure(degree_df, position_df, OUT_DIR / "figure.png")

    print("Degree sweep (population-level, mean of 20 seeds):")
    print(degree_df.round(3).to_string(index=False))
    print("\nPosition comparison (individual payoff, mean +/- sd, 20 seeds):")
    print(position_df.round(2).to_string(index=False))
    print(f"\nWrote degree_sweep.csv, position_comparison.csv, and figure.png to: {OUT_DIR}")


if __name__ == "__main__":
    main()
