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
- **Strategy composition:** counts of the six strategies (`selfish`, `cooperative`,
  `conditional_cooperator`, `compensating_cooperator`, `sanctioning`, `loner`) — see
  [terminology.md](terminology.md#cooperation-mechanisms-the-strategies).
- **Ecological knowledge:** `knowledge_bias` (cooperative / conditional strategies).
- **Decision noise:** `decision_noise` (stochastic perturbation of requests).
- **Communication:** `broadcast_reliability` (broadcast channel; message loss).
- **Disturbances:** scheduled `resource_shock` and `agent_failure` (ADR-0008; E8–E10).
- **Collective choice:** whether `collective_choice` is configured, and its
  `vote_round`, `overuse_threshold`, `cost_share` (ADR-0011; E13).
- **Group size (N):** total number of agents.
- **Resource parameters:** `initial_level`, `capacity` (K), `regeneration_rate` (g),
  `regeneration_rule`, `collapse_threshold`.
- *(Planned)* per-agent communication (deception, delay, topology); communication
  failure and *press* disturbances.

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
grid of parameter values; worked examples are the thirteen experiments E1–E13
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

## Sampling a large configuration space (Monte Carlo / GLUE)

The recipe above assumes the configuration space of interest is small enough to
enumerate (a handful of strategy mixes, a grid of parameter values). The
complexity axes (population-type diversity, groups, boundaries — see
[complexity-synthesis.md](complexity-synthesis.md)) instead sweep every
*composition* of a population, which grows combinatorially: 495 compositions
for one population of 8 across 5 types, tens of thousands once groups multiply
that, millions once a second population (outsiders) crosses it. First needed
in [E16](experiments/E16-boundaries.md), reused since — this is the general
procedure so every future axis doesn't re-derive or re-justify it from
scratch.

**When to switch from exhaustive to sampled:** once enumerating every joint
configuration stops being tractable (this project's practical ceiling: low
hundreds of thousands of simulations — beyond that, both the Python export and
the live JS demo stop being usable). E16's governed × outsider cross would
have been ~3.9M simulations (~2+ hours); sampling was the only option.

**Procedure:**

1. Enumerate each axis's own choice set once (e.g. all compositions of a
   group's agents across the 5 strategies).
2. Draw `N_SAMPLES` independent joint configurations, choosing uniformly at
   random *with replacement* from each axis's choice set. Uniform over the
   **distinct composition space**, not weighted by how many agent-labelings
   realize a composition — this has to match how the near-optimal-set-size is
   *counted* everywhere else in this project (each composition is one
   "approach," full stop).
3. Run the real simulation and the real `welfare_efficiency` threshold check
   on every sampled configuration — sampling covers *which configurations get
   tried*, never the model itself.
4. Report the near-optimal **fraction** (passes / `N_SAMPLES`) with a binomial
   95% CI. If the total space size is known, also report an *estimated*
   count = fraction × space size — always labelled as an estimate (`~`), never
   presented like an exhaustive count.
5. **Validate before trusting an estimate you can't otherwise check**: run the
   identical procedure against a case whose true answer is already known
   exactly, and confirm the estimate's CI actually contains it. E16's own
   validation: a 5,000-sample estimate of E15's exact `m=4` answer
   (18,737/50,625 = 0.3701) landed at 0.3628 ± 0.0133 — contains the true
   value.
6. Use a seeded RNG so the estimate is reproducible: `random.Random(SEED)` in
   Python, `mulberry32(seed)` in the JS demo port (same idea, different
   runtime — they will *not* produce identical draws, only equally
   reproducible ones each on their own side).
7. Size `N_SAMPLES` for the CI width the comparison needs, not just "big
   enough": 5,000/axis-level in the canonical Python scripts (~±1.3% CI),
   3,000/axis-level in the live JS demo (~±1.8% CI, traded down for
   in-browser responsiveness).

**Demo-only sampling is not a new experimental result.** The live browser
demo (`web/commons-demo.html`'s Complexity panel) goes one step further than
the Python scripts: it Monte Carlo-samples axes that the canonical experiment
computes *exactly*. E15's own closed-side sweep is exhaustive and exact in
`scripts/experiment_groups_full_sweep.py` (383/495, 2,820/4,900,
18,737/50,625), but the demo samples it too, purely because enumerating all
56,020 configurations synchronously froze the browser tab for several
seconds. That's a rendering-performance tradeoff, not a change to any
reported finding — the exact numbers always live in the experiment's own
doc/script; the demo's live numbers are representative, not canonical (same
caveat the demo already states for decision-noise/communication runs).
