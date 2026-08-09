"""Experiment E15: nested enforcement and boundaries — how many groups need a
monitor, and does closing the community off matter?

ADR-0012 added group-scoped ("nested enterprise") enforcement: a `sanctioning`
agent's quota now only protects its own group, not the whole population.
ADR-0013 showed that "boundaries" (open access vs. closed community, Ostrom
principle 1) needs no separate mechanism -- it's the same groups machinery,
compared with vs. without an extra, unmonitored outsider group.

This experiment sweeps both together. The governed population is fixed at
N = 8 agents, split into `m` equal groups of size `n = 8/m` (m in {1, 2, 4}).
Within each `m`, `k` of the `m` groups are `sanctioning`, the rest `selfish`
free-riders (k = 0..m) -- `selfish`, not `cooperative`, is what actually
exercises what nested enforcement was built for: an internal free-rider
group for the sanctioning groups to be protected *from*. (An earlier version
of this script used `cooperative` as the fallback, which never gave the
sanctioners anything to protect against, and only reproduced E3's
already-known "monitoring costs more than it's worth with no threat"
result -- kept here as a note, not a finding.) Crossed with boundaries:
`closed` (no outsiders) vs. `open` (+4 unmonitored `selfish` outsiders in
their own, ungoverned group).

Reports raw `welfare_efficiency` and `sustainability_ratio` -- not a
behavioural/non-behavioural classification, since the tolerance-band
threshold for that (docs/thesis-direction-equifinality.md) is still an open,
undecided number, not yet independently settled. Deterministic strategies
(cooperative, sanctioning) draw no randomness, so a single seed is exact,
not a noisy mean (same reasoning as E1).

Outputs go to ``results/E15_groups_boundaries/``. Run with::

    python scripts/experiment_groups_boundaries.py
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

OUT_DIR = Path(__file__).resolve().parent.parent / "results" / "E15_groups_boundaries"
SEEDS = (1,)  # deterministic strategies only -> exact, not a noisy mean (see E1)
ROUNDS = 100
CAPACITY = 100.0
G = 0.4
N = 8  # governed population, fixed across the sweep
OUTSIDERS = 4  # size of the ungoverned "open access" outsider group
GROUP_COUNTS = (1, 2, 4)  # m: how many groups the governed population is split into

# Provisional tolerance-band threshold (docs/thesis-direction-equifinality.md --
# still not independently settled). Picked from the actual E15 numbers below,
# not guessed blind: full sanctioning coverage
# tops out at welfare_efficiency=0.84 (monitoring cost mechanically prevents 1.0),
# so a 0.95-style bar (the earlier placeholder) would disqualify enforcement by
# construction, before any comparison even starts. 0.80 sits just below that
# structural ceiling: a well-executed enforcement regime can still pass, while the
# wasted partial-coverage cells (0.01-0.53) clearly fail. Revisit once a real
# threshold is agreed.
THRESHOLD = 0.80

# Strategies that can occupy the *outsider* group in the boundaries sweep below --
# not "which institution protects a group" (sanctioning is currently the only
# registered strategy that exposes a SanctionPolicy at all, so that axis has
# exactly one option today), but "what does the excluded-or-not population do."
OUTSIDER_STRATEGIES = ("selfish", "cooperative", "conditional_cooperator", "compensating_cooperator")


def _fmt(x: float | None) -> str:
    return "n/a" if x is None or pd.isna(x) else f"{x:.2f}"


def _params(strategy: str) -> dict:
    if strategy == "selfish":
        return {"greed": 1.0}
    p = {"regeneration_rate": G, "capacity": CAPACITY}
    if strategy == "sanctioning":
        p["monitoring_cost"] = 0.2
    return p


def _experiment(m: int, k: int, *, outsiders: bool) -> ExperimentConfig:
    """`m` groups of size `n = N/m`; the first `k` are sanctioning, rest selfish."""
    n = N // m
    agents = [
        AgentSpec(
            "sanctioning" if g < k else "selfish",
            n,
            _params("sanctioning" if g < k else "selfish"),
            group=g,
        )
        for g in range(m)
    ]
    if outsiders:
        # Own, ungoverned group -> never covered by any group's sanctioning quota,
        # and governed=False so it's also excluded from the quota *denominator*
        # (ADR-0012's allocation correction) -- not counted and then left
        # unconstrained anyway.
        agents.append(AgentSpec("selfish", OUTSIDERS, {"greed": 1.0}, group=m, governed=False))
    sim = SimulationConfig(
        name=f"E15_m{m}_k{k}_{'open' if outsiders else 'closed'}",
        rounds=ROUNDS,
        information_model="global",
        resource=ResourceConfig(
            initial_level=CAPACITY / 2,
            capacity=CAPACITY,
            regeneration_rate=G,
            collapse_threshold=1.0,
        ),
        agents=tuple(agents),
    )
    return ExperimentConfig(simulation=sim, seeds=SEEDS, record_history=False)


def _payoff_by_strategy(result) -> dict[str, float]:
    """Mean net payoff per strategy present in a single run -- stays meaningful
    even when payoff_gini is undefined (negative net payoff breaks Gini's
    formula; a raw per-strategy mean never does). Single seed here, so no
    averaging across runs is needed."""
    from collections import defaultdict

    sums: dict[str, list[float]] = defaultdict(list)
    for strat, payoff in zip(result.agent_strategies, result.total_payoffs(), strict=True):
        sums[strat].append(payoff)
    return {s: sum(v) / len(v) for s, v in sums.items()}


def summarise() -> pd.DataFrame:
    """welfare_efficiency, sustainability_ratio, payoff_gini, per-strategy mean
    payoff, and collapsed, per (m, k, boundary). Single seed (SEEDS=(1,)), so
    every value below is exact, not an average across runs."""
    rows = []
    for m in GROUP_COUNTS:
        for k in range(m + 1):
            for outsiders in (False, True):
                outcome = run_experiment(_experiment(m, k, outsiders=outsiders))
                metrics = outcome.metrics
                breakdown = _payoff_by_strategy(outcome.results[0])
                gini = metrics["payoff_gini"].iloc[0]
                rows.append(
                    {
                        "m": m,
                        "k": k,
                        "fraction_sanctioning": k / m,
                        "boundary": "open" if outsiders else "closed",
                        "welfare_efficiency": float(metrics["welfare_efficiency"].mean()),
                        "sustainability_ratio": float(metrics["sustainability_ratio"].mean()),
                        "payoff_gini": None if pd.isna(gini) else float(gini),
                        "sanctioning_mean_payoff": breakdown.get("sanctioning"),
                        "selfish_mean_payoff": breakdown.get("selfish"),
                        "collapsed": bool(metrics["collapsed"].any()),
                    }
                )
    return pd.DataFrame(rows)


def complexity_curve(summary: pd.DataFrame) -> pd.DataFrame:
    """The actual "near-optimal-set-size vs. complexity" curve this project's
    equifinality direction is about: for each `m` (the complexity dial -- how many
    groups the governed population is split into), how many of the `m+1` possible
    coverage levels (`k = 0..m`, sanctioning vs. selfish per group) clear THRESHOLD?
    Reuses the (m, k, boundary) grid already computed by `summarise()` -- no new
    simulation runs.
    """
    rows = []
    for m in GROUP_COUNTS:
        for boundary in ("closed", "open"):
            sub = summary[(summary["m"] == m) & (summary["boundary"] == boundary)]
            passing = int((sub["welfare_efficiency"] >= THRESHOLD).sum())
            rows.append(
                {
                    "m": m,
                    "boundary": boundary,
                    "configs_tested": len(sub),
                    "near_optimal_count": passing,
                    "near_optimal_fraction": passing / len(sub),
                }
            )
    return pd.DataFrame(rows)


def _outsider_experiment(m: int, outsider_strategy: str) -> ExperimentConfig:
    """Full coverage (every one of the `m` governed groups is sanctioning) plus an
    open, ungoverned outsider group running `outsider_strategy` instead of the
    fixed `selfish` used in the main sweep above."""
    n = N // m
    agents = [AgentSpec("sanctioning", n, _params("sanctioning"), group=g) for g in range(m)]
    agents.append(
        AgentSpec(outsider_strategy, OUTSIDERS, _params(outsider_strategy), group=m, governed=False)
    )
    sim = SimulationConfig(
        name=f"E15_outsider_m{m}_{outsider_strategy}",
        rounds=ROUNDS,
        information_model="global",
        resource=ResourceConfig(
            initial_level=CAPACITY / 2,
            capacity=CAPACITY,
            regeneration_rate=G,
            collapse_threshold=1.0,
        ),
        agents=tuple(agents),
    )
    return ExperimentConfig(simulation=sim, seeds=SEEDS, record_history=False)


def near_optimal_set(summary: pd.DataFrame) -> pd.DataFrame:
    """For each `m`, with every group covered (full coverage), classify every
    candidate outsider strategy as behavioural/non-behavioural at THRESHOLD, and
    count how many pass -- the near-optimal-set-size for that setting. The closed
    baseline (no outsiders at all) is included as its own always-available "approach".
    """
    rows = []
    for m in GROUP_COUNTS:
        closed_row = summary[(summary["m"] == m) & (summary["k"] == m) & (summary["boundary"] == "closed")]
        rows.append(
            {
                "m": m,
                "outsider_strategy": "(closed -- no outsiders)",
                "welfare_efficiency": float(closed_row["welfare_efficiency"].iloc[0]),
                "payoff_gini": float(closed_row["payoff_gini"].iloc[0]),
                "behavioural": bool(closed_row["welfare_efficiency"].iloc[0] >= THRESHOLD),
            }
        )
        for strategy in OUTSIDER_STRATEGIES:
            metrics = run_experiment(_outsider_experiment(m, strategy)).metrics
            we = float(metrics["welfare_efficiency"].mean())
            rows.append(
                {
                    "m": m,
                    "outsider_strategy": strategy,
                    "welfare_efficiency": we,
                    "payoff_gini": float(metrics["payoff_gini"].mean()),
                    "behavioural": we >= THRESHOLD,
                }
            )
    return pd.DataFrame(rows)


BOUNDARY_STYLE = {"closed": dict(linestyle="-", alpha=1.0), "open": dict(linestyle=":", alpha=0.6)}
M_COLOR = {1: "#1f77b4", 2: "#d55e00", 4: "#009e73"}


def make_figure(summary: pd.DataFrame, path: Path) -> None:
    """Panel A: welfare_efficiency vs fraction sanctioning, one line per m, closed vs open.
    Panel B: same for sustainability_ratio."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 4.6))

    for ax, col, title in (
        (ax1, "welfare_efficiency", "A. Welfare efficiency"),
        (ax2, "sustainability_ratio", "B. Sustainability ratio"),
    ):
        for m in GROUP_COUNTS:
            for boundary in ("closed", "open"):
                sub = summary[(summary["m"] == m) & (summary["boundary"] == boundary)].sort_values(
                    "fraction_sanctioning"
                )
                ax.plot(
                    sub["fraction_sanctioning"],
                    sub[col],
                    marker="o",
                    color=M_COLOR[m],
                    lw=2 if boundary == "closed" else 1.3,
                    label=f"m={m} groups · {boundary}",
                    **BOUNDARY_STYLE[boundary],
                )
        ax.set_xlabel("fraction of groups with a sanctioner (k/m)")
        ax.set_title(title)
        ax.set_xlim(-0.05, 1.05)
    ax1.set_ylabel("welfare_efficiency")
    ax1.axhline(1.0, color="grey", ls=":", lw=0.8)
    ax2.set_ylabel("sustainability_ratio")
    ax2.legend(fontsize=7, loc="lower right")

    fig.suptitle(
        "E15: nested enforcement (m groups, k sanctioning) x boundaries (closed vs open)"
    )
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)


def make_complexity_figure(curve: pd.DataFrame, path: Path) -> None:
    """The near-optimal-set-size vs. complexity chart -- one line per boundary
    condition, `m` (group count) on the x-axis. This is a genuine 2-axis
    factorial (m x boundary): every one of the 3x2 = 6 cells is tested (see
    complexity_curve.csv), unlike the single-axis m-only sweep this project
    previously (and correctly) declined to call "the complexity curve."
    Shared by E15 (closed line only, in isolation) and E16 (both lines --
    the actual 2-axis reading).

    Two panels, not one line, because "count" and "fraction" answer two
    different questions that this project's own equifinality definition
    ("count how many different approaches land near-optimal") can otherwise
    conflate: adding a new axis whose new branch (open) contributes zero
    passing configurations mechanically drags the *fraction* down (bigger
    denominator, same numerator) without the achievable *count* actually
    shrinking. Plotting only the fraction reads as "complexity made things
    worse"; the count panel shows the more precise claim -- "complexity never
    made things better" -- which is what actually survived scrutiny. Never
    combined onto one dual-axis plot (the fraction panel would need a second,
    differently-scaled y-axis on the same figure, which the count line is not
    on the same footing to share).

    "open" here specifically means open *with a selfish outsider* -- the
    adversarial case, not "outsiders in general" (the outsider's own strategy
    is swept separately, see near_optimal_set.csv / E16's "by outsider type"
    section: at full coverage, count is 3/5 there, not 0/5, once the outsider
    isn't selfish). Labelled explicitly in the legend below so this chart
    doesn't get read as the general answer for "boundary" on its own."""
    fig, axes = plt.subplots(1, 2, figsize=(12.5, 4.8))
    style = {"closed": dict(color="#1f77b4", marker="o"), "open": dict(color="#d55e00", marker="s")}

    ax = axes[0]
    for boundary in ("closed", "open"):
        sub = curve[curve["boundary"] == boundary].sort_values("m")
        ax.plot(
            sub["m"], sub["near_optimal_count"], lw=2.2,
            label=f"{boundary}" + (" (E15)" if boundary == "closed" else ", selfish outsider (E16)"),
            **style[boundary],
        )
    ax.set_xticks(GROUP_COUNTS)
    ax.set_xlabel("m -- number of groups")
    ax.set_ylabel("near-optimal count (out of k=0..m tested)")
    ax.set_ylim(-0.3, 3)
    ax.set_yticks([0, 1, 2, 3])
    ax.set_title("Absolute count -- does the set of viable\napproaches actually grow?", fontsize=10.5)
    ax.legend(fontsize=9)

    ax = axes[1]
    for boundary in ("closed", "open"):
        sub = curve[curve["boundary"] == boundary].sort_values("m")
        ax.plot(
            sub["m"], sub["near_optimal_fraction"], lw=2.2,
            label=f"{boundary}" + (" (E15)" if boundary == "closed" else ", selfish outsider (E16)"),
            **style[boundary],
        )
        for row in sub.itertuples():
            ax.annotate(
                f"{row.near_optimal_count}/{row.configs_tested}",
                (row.m, row.near_optimal_fraction),
                textcoords="offset points", xytext=(0, 8), fontsize=8, ha="center",
                color=style[boundary]["color"],
            )
    ax.set_xticks(GROUP_COUNTS)
    ax.set_xlabel("m -- number of groups")
    ax.set_ylabel("near-optimal fraction (of configs tested)")
    ax.set_ylim(-0.05, 0.65)
    ax.set_title("Fraction of the tried space -- does it get\nharder to stumble into one?", fontsize=10.5)
    ax.legend(fontsize=9)

    fig.suptitle(
        "Near-optimal-set-size vs. complexity: groups (m) x boundary\n"
        "(\"open\" = selfish outsider, the adversarial case -- see E16 for the non-adversarial reading; "
        "threshold = welfare_efficiency >= 0.80, provisional)",
        fontsize=10,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    fig.savefig(path, dpi=130)
    plt.close(fig)


def main() -> None:
    """Run the grid, export the summary CSV + figure, print the headline."""
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    summary = summarise()
    summary.to_csv(OUT_DIR / "summary.csv", index=False)
    make_figure(summary, OUT_DIR / "figure.png")

    print("E15 -- welfare_efficiency (gini) by (m groups, k sanctioning, boundary):")
    for m in GROUP_COUNTS:
        for boundary in ("closed", "open"):
            sub = summary[(summary["m"] == m) & (summary["boundary"] == boundary)].sort_values("k")
            cells = "  ".join(
                f"k={int(r.k)}:{r.welfare_efficiency:.2f}"
                f"(gini={_fmt(r.payoff_gini)}"
                f", mon={_fmt(r.sanctioning_mean_payoff)}, self={_fmt(r.selfish_mean_payoff)})"
                for r in sub.itertuples()
            )
            print(f"  m={m} {boundary:6s}: {cells}")
    print(f"\nWrote summary.csv and figure.png to: {OUT_DIR}")

    curve = complexity_curve(summary)
    curve.to_csv(OUT_DIR / "complexity_curve.csv", index=False)
    make_complexity_figure(curve, OUT_DIR / "complexity_curve.png")
    print(f"\nE15 -- near-optimal-set-size vs. complexity (m), threshold={THRESHOLD}:")
    for boundary in ("closed", "open"):
        sub = curve[curve["boundary"] == boundary].sort_values("m")
        cells = "  ".join(f"m={int(r.m)}: {r.near_optimal_count}/{r.configs_tested}" for r in sub.itertuples())
        print(f"  {boundary:6s}: {cells}")

    noset = near_optimal_set(summary)
    noset.to_csv(OUT_DIR / "near_optimal_set.csv", index=False)
    print(f"\nE15 -- near-optimal set (threshold={THRESHOLD}), full coverage, by m:")
    for m in GROUP_COUNTS:
        sub = noset[noset["m"] == m]
        count = int(sub["behavioural"].sum())
        cells = "  ".join(
            f"{r.outsider_strategy}:{'PASS' if r.behavioural else 'fail'}({r.welfare_efficiency:.2f})"
            for r in sub.itertuples()
        )
        print(f"  m={m}  set size {count}/{len(sub)}:  {cells}")
    print(f"\nWrote near_optimal_set.csv to: {OUT_DIR}")


if __name__ == "__main__":
    main()
