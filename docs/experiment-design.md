# Experiment Design

This document defines how experiments are structured so that results are
reproducible and comparable. It is the contract every experiment should follow.

## Principles

1. **One experiment = one base config swept over seeds.** Every run in an
   experiment shares all parameters except the seed.
2. **Change one factor at a time.** To attribute an effect to a factor (e.g.
   information model), hold everything else constant across the compared configs.
3. **Always report across multiple seeds.** A single seed is an anecdote. Report
   the distribution (mean and spread) over a fixed seed set.
4. **Everything needed to reproduce is recorded.** Config, seeds, software
   version, git commit, platform, and timestamp are written with every export.

## Variables

### Independent variables (things we vary)
- **Information model:** `global` | `private` *(local/aggregated/outdated planned)*.
- **Strategy composition:** counts of the five strategies (`selfish`, `cooperative`,
  `conditional_cooperator`, `compensating_cooperator`, `sanctioning`) — see
  [terminology.md](terminology.md#cooperation-mechanisms-the-strategies).
- **Ecological knowledge:** `knowledge_bias` (cooperative / conditional strategies).
- **Decision noise:** `decision_noise` (stochastic perturbation of requests).
- **Communication:** `broadcast_reliability` (broadcast channel; message loss).
- **Group size (N):** total number of agents.
- **Resource parameters:** `initial_level`, `capacity` (K), `regeneration_rate` (g),
  `regeneration_rule`, `collapse_threshold`.
- *(Planned)* per-agent communication (deception, delay, topology); disturbances.

### Controlled variables (held fixed within a comparison)
Everything not being studied. E.g. when comparing information models, keep N,
resource parameters, strategy mix, rounds, and the seed set identical.

### Dependent variables (what we measure)
See [metrics.md](metrics.md): total harvest, sustainability ratio, collapse and
collapse round, mean resource level, payoff Gini (and, later, cooperation rate,
recovery time, resilience).

### Nuisance variables (controlled by design)
Random seed (swept, not fixed to one value); iteration order (fixed by construction).

## Baselines and control conditions

The four shipped configs form the reference frame:

| Config | Role |
| ------ | ---- |
| `all_cooperative_global` | Positive control: sustainable cooperation. |
| `all_selfish_global` | Negative control: tragedy of the commons (collapse). |
| `mixed_global` | Treatment: free-riding in a heterogeneous population. |
| `all_cooperative_private` | Treatment: same cooperation, less information. |

Any new mechanism (a strategy, a communication model, a disturbance) is evaluated
**against these baselines**, not in isolation.

Systematic studies use the sweep runner (`experiments.sweep.run_grid`) to cover a
grid of parameter values; worked examples are the seven experiments E1–E7
(`scripts/experiment_*.py`, written up in [experiments/](experiments/) and the
[findings summary](findings-summary.md)).

## Seeds and repetitions

- Default seed set: `[1, 2, 3, 4, 5]` (small, for fast iteration).
- For reported/thesis results, use a larger set (e.g. 20–50 seeds) so means and
  confidence intervals are meaningful.
- Seeds are explicit in the config (`seeds:`) and recorded in `provenance.json`.
- Identical `(config, seed)` ⇒ identical `RunResult` (deterministic; tested).

## A standard comparison recipe

To answer "does factor X matter?":

1. Write two (or more) configs identical except in X.
2. Use the **same** seed set for all of them.
3. Run each: `emergent-coop run --config <cfg> --output results/<name>`.
4. Load the `metrics.csv` files and compare distributions per metric across seeds.
5. Report effect size and variability, not just point means.

Example (information effect): compare `all_cooperative_global` vs
`all_cooperative_private` while sweeping `initial_level` — this tests hypothesis
**H1** (blind cooperation is sensitive to initial stock).

## Reproducibility requirements (checklist)

Every reported result must be backed by an export directory containing:

- [ ] `resolved_config.yaml` — the exact configuration run.
- [ ] `metrics.csv` — one row per seed.
- [ ] `round_history.csv` — per-round trajectory (when `record_history: true`).
- [ ] `provenance.json` — package version, git commit, python/platform, timestamp,
      seeds, status.

Additional requirements:

- [ ] Code committed (so `git_commit` in provenance is non-null).
- [ ] Dependencies pinned enough to reproduce (`pyproject.toml`; consider a lock
      file for thesis-grade results).
- [ ] Any figure cites the exact export directory it was produced from.

## Statistical analysis (planned depth)

- Report mean ± standard deviation (or IQR) across seeds per metric.
- For factor comparisons, report effect sizes and appropriate tests
  (e.g. Mann–Whitney U for non-normal metric distributions); avoid over-claiming
  from few seeds.
- Distinguish **variance between runs** (robustness) from **sensitivity to
  parameters** (a separate sweep).

## Pitfalls to avoid

- Comparing configs that differ in more than the studied factor.
- Reporting a single seed as if representative.
- Reading tendencies into differences smaller than the between-seed spread.
- Silent parameter drift between "baseline" and "treatment" configs — diff them.
