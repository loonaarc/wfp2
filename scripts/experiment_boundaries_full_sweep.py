"""Experiment E16: boundaries, reworked to cross the *governed* side's full
population-composition sweep (E15) against the *outsider* side's own full
composition space -- Monte Carlo sampled, not exhaustively enumerated.

Exhaustively crossing E15's 56,020 governed configurations against all 70
possible 4-agent outsider compositions would be ~3.9M simulations (~2+
hours) -- intractable, and the kind of problem this project's own adopted
methodology (GLUE, Beven & Binley 1992/2014; see docs/literature-review.md)
already has an answer for: Monte Carlo sample instead of enumerating
exhaustively, and report the near-optimal fraction with a confidence
interval instead of an exact count. Validated first against E15's own
already-exact m=4 result (18,737/50,625 = 0.3701): a 5,000-sample estimate
landed at 0.3628 +/- 0.0133 (95% CI), comfortably containing the true value
-- see the validation note in the commit/PR this script was introduced in.

Sampling is uniform over the *distinct composition space*, matching how
E14/E15 count near-optimal-set-size (each composition is one "approach,"
regardless of how many agent-labelings realize it) -- not uniform over
agent-level assignments, which would (via the multinomial distribution)
over-weight near-even splits relative to extreme ones. Achieved by
independently sampling each group's own sub-composition uniformly from its
own enumerated list (and the outsider's composition uniformly from its own
list) -- the product of independent uniforms over each factor is uniform
over the joint space, without ever materializing it.

The outsider-*type* sub-study (full coverage, outsider strategy varied
across 4 named types) stays a separate, small, exact analysis -- unaffected
by this rework, see outsider_type_sweep() below.

Outputs go to ``results/E16_boundaries_full_sweep/``. Run with::

    python scripts/experiment_boundaries_full_sweep.py
"""

from __future__ import annotations

import random
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
from experiment_groups_full_sweep import (  # noqa: E402
    CAPACITY,
    G,
    GROUP_COUNTS,
    N,
    ROUNDS,
    THRESHOLD,
    TYPES,
    _params,
    _specs_for,
    _sub_compositions,
)

from emergent_cooperation.core.config import AgentSpec, ResourceConfig, SimulationConfig  # noqa: E402
from emergent_cooperation.core.simulation import run_simulation  # noqa: E402
from emergent_cooperation.metrics.metrics import compute_metrics  # noqa: E402

OUT_DIR = Path(__file__).resolve().parent.parent / "results" / "E16_boundaries_full_sweep"
OUTSIDERS = 4
N_SAMPLES = 5000  # per m; ~+/-0.013 95% CI on the fraction, validated against E15's m=4 exact answer
SEED = 42


def _welfare_efficiency(specs: list[AgentSpec]) -> tuple[float, bool]:
    cfg = SimulationConfig(
        name="E16_full",
        rounds=ROUNDS,
        information_model="global",
        resource=ResourceConfig(
            initial_level=CAPACITY / 2,
            capacity=CAPACITY,
            regeneration_rate=G,
            collapse_threshold=1.0,
        ),
        agents=tuple(specs),
    )
    result = run_simulation(cfg, seed=1)
    metrics = compute_metrics(result, capacity=CAPACITY, regeneration_rate=G)
    return metrics["welfare_efficiency"], metrics["collapsed"]


def sample_m_open(m: int, n_samples: int, rng: random.Random) -> pd.DataFrame:
    """Monte Carlo sample of the full (governed composition x outsider
    composition) space for this m, boundary open. Each factor is sampled
    uniformly and independently from its own enumerated list, so the joint
    sample is uniform over the full cross product without materializing it."""
    size = N // m
    governed_choices = _sub_compositions(size)
    outsider_choices = _sub_compositions(OUTSIDERS)
    rows = []
    for _ in range(n_samples):
        group_compositions = tuple(rng.choice(governed_choices) for _ in range(m))
        outsider_composition = rng.choice(outsider_choices)
        specs = _specs_for(group_compositions)
        for strategy, count in zip(TYPES, outsider_composition, strict=True):
            if count > 0:
                specs.append(AgentSpec(strategy, count, _params(strategy), group=m, governed=False))
        we, collapsed = _welfare_efficiency(specs)
        row: dict[str, object] = {"m": m}
        for g, composition in enumerate(group_compositions):
            for strategy, count in zip(TYPES, composition, strict=True):
                row[f"g{g}_{strategy}"] = count
        for strategy, count in zip(TYPES, outsider_composition, strict=True):
            row[f"outsider_{strategy}"] = count
        row["welfare_efficiency"] = we
        row["collapsed"] = collapsed
        rows.append(row)
    return pd.DataFrame(rows)


def outsider_type_sweep() -> pd.DataFrame:
    """Unchanged from the original E16: full coverage (every group uniformly
    sanctioning), boundary open, outsider's own strategy varied across 4
    named types -- a separate, small, exact sub-study."""
    types = ("selfish", "cooperative", "conditional_cooperator", "compensating_cooperator")
    rows = []
    for m in GROUP_COUNTS:
        n = N // m
        governed = [AgentSpec("sanctioning", n, _params("sanctioning"), group=g) for g in range(m)]
        closed_we, closed_collapsed = _welfare_efficiency(governed)
        rows.append({"m": m, "outsider_strategy": "(closed -- no outsiders)",
                      "welfare_efficiency": closed_we, "collapsed": closed_collapsed})
        for outsider_strategy in types:
            specs = [*governed, AgentSpec(outsider_strategy, OUTSIDERS, _params(outsider_strategy),
                                           group=m, governed=False)]
            we, collapsed = _welfare_efficiency(specs)
            rows.append({"m": m, "outsider_strategy": outsider_strategy,
                          "welfare_efficiency": we, "collapsed": collapsed})
    return pd.DataFrame(rows)


def near_optimal_by_m_boundary(closed: dict[int, pd.DataFrame], open_samples: dict[int, pd.DataFrame]) -> pd.DataFrame:
    """Closed side: exact (reused from E15). Open side: Monte Carlo estimate
    with a 95% confidence interval on both the fraction and the count
    (count = fraction x true total space size, which is known exactly even
    though the space itself isn't enumerated)."""
    rows = []
    for m in GROUP_COUNTS:
        closed_df = closed[m]
        closed_passing = int((closed_df["welfare_efficiency"] >= THRESHOLD).sum())
        rows.append({
            "m": m, "boundary": "closed", "configs_tested": len(closed_df),
            "near_optimal_count": closed_passing, "near_optimal_fraction": closed_passing / len(closed_df),
            "count_ci_low": closed_passing, "count_ci_high": closed_passing,
            "fraction_ci_low": closed_passing / len(closed_df), "fraction_ci_high": closed_passing / len(closed_df),
            "estimated": False,
        })

        open_df = open_samples[m]
        n = len(open_df)
        passing = int((open_df["welfare_efficiency"] >= THRESHOLD).sum())
        frac = passing / n
        se = (frac * (1 - frac) / n) ** 0.5
        ci = 1.96 * se
        total_space = len(_sub_compositions(N // m)) ** m * len(_sub_compositions(OUTSIDERS))
        rows.append({
            "m": m, "boundary": "open", "configs_tested": total_space,
            "near_optimal_count": round(frac * total_space), "near_optimal_fraction": frac,
            "count_ci_low": round(max(0, frac - ci) * total_space),
            "count_ci_high": round(min(1, frac + ci) * total_space),
            "fraction_ci_low": max(0, frac - ci), "fraction_ci_high": min(1, frac + ci),
            "estimated": True,
        })
    return pd.DataFrame(rows)


def make_figure(curve: pd.DataFrame, path: Path) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(12.5, 4.8))
    style = {"closed": dict(color="#1f77b4", marker="o"), "open": dict(color="#d55e00", marker="s")}

    ax = axes[0]
    for boundary in ("closed", "open"):
        sub = curve[curve["boundary"] == boundary].sort_values("m")
        ax.plot(sub["m"], sub["near_optimal_count"], lw=2.2,
                 label=f"{boundary}" + (" (E15, exact)" if boundary == "closed" else " (E16, estimated)"),
                 **style[boundary])
        if boundary == "open":
            ax.fill_between(sub["m"], sub["count_ci_low"], sub["count_ci_high"],
                             color=style[boundary]["color"], alpha=0.15)
    ax.set_xticks(GROUP_COUNTS)
    ax.set_xlabel("m -- number of groups")
    ax.set_ylabel("near-optimal count")
    ax.set_title("Absolute count -- does the set of viable\nconfigurations actually grow?", fontsize=10.5)
    ax.legend(fontsize=9)

    ax = axes[1]
    for boundary in ("closed", "open"):
        sub = curve[curve["boundary"] == boundary].sort_values("m")
        ax.plot(sub["m"], sub["near_optimal_fraction"], lw=2.2,
                 label=f"{boundary}" + (" (E15, exact)" if boundary == "closed" else " (E16, estimated)"),
                 **style[boundary])
        if boundary == "open":
            ax.fill_between(sub["m"], sub["fraction_ci_low"], sub["fraction_ci_high"],
                             color=style[boundary]["color"], alpha=0.15)
    ax.set_xticks(GROUP_COUNTS)
    ax.set_xlabel("m -- number of groups")
    ax.set_ylabel("near-optimal fraction (of full space)")
    ax.set_ylim(-0.05, 1.05)
    ax.set_title("Fraction of the full space -- does it get\nharder to stumble into one?", fontsize=10.5)
    ax.legend(fontsize=9)

    fig.suptitle(
        f"Near-optimal-set-size vs. m x boundary (E16, full governed x outsider space)\n"
        f"(closed = E15 exact; open = Monte Carlo, n={N_SAMPLES}/m, shaded = 95% CI; "
        f"threshold = welfare_efficiency >= 0.80, provisional)",
        fontsize=9.5,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.92))
    fig.savefig(path, dpi=130)
    plt.close(fig)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rng = random.Random(SEED)

    e15_dir = Path(__file__).resolve().parent.parent / "results" / "E15_groups_full_sweep"
    closed = {m: pd.read_csv(e15_dir / f"summary_m{m}.csv") for m in GROUP_COUNTS}

    open_samples: dict[int, pd.DataFrame] = {}
    for m in GROUP_COUNTS:
        print(f"Sampling m={m}, open boundary ({N_SAMPLES} draws)...")
        df = sample_m_open(m, N_SAMPLES, rng)
        df.to_csv(OUT_DIR / f"sample_open_m{m}.csv", index=False)
        open_samples[m] = df
        passing = int((df["welfare_efficiency"] >= THRESHOLD).sum())
        print(f"  m={m} open: {passing}/{N_SAMPLES} sampled pass (threshold={THRESHOLD})")

    curve = near_optimal_by_m_boundary(closed, open_samples)
    curve.to_csv(OUT_DIR / "near_optimal_by_m_boundary.csv", index=False)
    make_figure(curve, OUT_DIR / "near_optimal_by_m_boundary.png")

    print("\nE16 -- near-optimal-set-size vs. m x boundary:")
    for row in curve.itertuples():
        tag = "exact" if not row.estimated else f"estimated, CI=[{row.count_ci_low},{row.count_ci_high}]"
        print(f"  m={row.m} {row.boundary}: {row.near_optimal_count}/{row.configs_tested} "
              f"({row.near_optimal_fraction:.3f}) [{tag}]")

    print("\nOutsider-type sub-study (unchanged methodology, exact)...")
    outsiders = outsider_type_sweep()
    outsiders.to_csv(OUT_DIR / "outsider_type_sweep.csv", index=False)
    for m in GROUP_COUNTS:
        sub = outsiders[outsiders["m"] == m]
        print(f"  m={m}: " +
              ", ".join(f"{r.outsider_strategy}:{'PASS' if r.welfare_efficiency >= THRESHOLD else 'fail'}({r.welfare_efficiency:.2f})"
                        for r in sub.itertuples()))

    print(f"\nWrote results to: {OUT_DIR}")


if __name__ == "__main__":
    main()
