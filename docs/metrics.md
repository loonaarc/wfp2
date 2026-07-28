# Metrics

Candidate and implemented metrics for evaluating runs. Each entry gives a
definition, formula, assumptions, what it is good for, and its limitations.
Implemented metrics are produced by `metrics.compute_metrics` (one row per run).

Notation: `N` agents, `T` rounds. For round `t`: `R_t` = stock after harvest,
`H_t` = total harvest. Agent `i` accumulates payoff `P_i = Σ_t h_{i,t}`. `K` =
carrying capacity, `g` = regeneration rate.

## Implemented (v0.1.0)

### System performance — `total_harvest`, `mean_agent_payoff`, `total_sanction_penalty`
- **Definition:** `total_harvest` is the **gross** resource extracted over the run;
  `mean_agent_payoff` is the mean **net** payoff per agent (harvest minus sanction
  penalties); `total_sanction_penalty` is the total monitoring cost paid (0 without
  sanctioners).
- **Formula:** `total_harvest = Σ_t H_t` (gross); `mean_agent_payoff = (Σ_i P_i)/N`
  where `P_i` is agent `i`'s net payoff.
- **Gross vs. net:** the two coincide unless a sanctioning agent is present; then
  `total_harvest` (what left the pool) exceeds the summed net payoff (what agents
  kept) by `total_sanction_penalty`. Fairness (`payoff_gini`) is computed on net
  payoffs.
- **Good for:** overall throughput / efficiency of the system.
- **Limitations:** high short-term harvest can precede collapse — must be read
  together with sustainability. Not comparable across different `T` without
  normalising.

### Sustainability — `final_resource_level`, `sustainability_ratio`, `mean_resource_level`
- **Definition:** stock at the end; final stock relative to capacity; average
  standing stock.
- **Formula:** `sustainability_ratio = R_T / K`; `mean_resource_level = (Σ_t R_t)/T`.
- **Good for:** whether the resource is left healthy; distinguishing "sustained"
  from "mined-out" runs with similar total harvest.
- **Assumption:** exact `K` supplied by the runner (else approximated by max
  observed stock, giving an upper-bound ratio).

### Collapse — `collapsed`, `collapse_round`
- **Definition:** whether/when the stock first fell to/below `collapse_threshold`.
- **Formula:** `collapsed = ∃t: R_t ≤ θ`; `collapse_round = min{t: R_t ≤ θ}` or none.
- **Good for:** a binary failure indicator and time-to-failure.
- **Limitation:** threshold `θ` is a modelling choice; report it alongside.

### Fairness — `payoff_gini`
- **Definition:** inequality of accumulated payoffs across agents.
- **Formula (mean-absolute-difference):**
  `G = (Σ_i Σ_j |P_i − P_j|) / (2 N Σ_i P_i)`, with `G = 0` for all-zero payoffs.
- **Range:** `0` (perfect equality) to `→ (N−1)/N` (one agent takes everything).
- **Good for:** detecting free-riding (selfish agents out-earning cooperators).
- **Limitations:** Gini ignores *who* is unequal (which strategy benefits) and is
  undefined-then-defined-as-0 for zero total; pair it with per-strategy payoff
  breakdowns for interpretation.

### Survival time — `survival_time`
- **Definition:** rounds sustained before the first collapse (all rounds if it never
  collapses). Standard in CPR simulations (GovSim).
- **Formula:** `collapse_round` if collapsed, else `T`.
- **Good for:** a graded resilience/time-to-failure signal (finer than the binary
  `collapsed`).

### Efficiency — `efficiency`
- **Definition:** total harvest relative to the optimal *sustainable* harvest.
- **Formula:** `total_harvest / (MSY · T)` with `MSY = g·K/4` (logistic).
  `1.0` = extracted exactly the sustainable yield each round; `>1` = out-harvested it
  by drawing down stock; `<1` = under-harvested. `None` if `g`/`K` unknown or the
  rule is non-logistic.
- **Good for:** distinguishing "sustained but wastefully under-using" from "optimally
  sustainable" — e.g. an under-confident cooperator scores <1 (see E1).

### Over-usage rate — `over_usage_rate`
- **Definition:** fraction of *active* rounds (regrown stock above the collapse
  threshold) whose total harvest exceeded the sustainable yield MSY (GovSim).
- **Formula:** `|{active rounds: total_harvested > MSY}| / |active rounds|`; `None`
  if MSY unknown, `0.0` if no active rounds.
- **Good for:** directly measuring *over-extraction* — separates cooperative intent
  from sustainable behaviour (the ADR-0004 / Schill et al. distinction).

## Candidate (planned)

### Cooperation rate
- **Idea:** how much agents restrain relative to a selfish benchmark.
- **Candidate formula:** `1 − (mean actual harvest) / (mean selfish-benchmark
  harvest)`, or the fraction of rounds an agent harvests ≤ its sustainable share.
- **Open question:** which benchmark is fairest and comparable across configs.

### Recovery time / resilience — **implemented** (E8, ADR-0008)
- **What:** measured around the first disturbance and emitted by `compute_metrics`
  (all `None`/`False` when no disturbance fired): `shock_round`, `pre_shock_level`
  (the recovery baseline), `post_shock_min_level` (how deep the dip went),
  `recovery_time` (rounds until the stock returns to ≥ 90% of `pre_shock_level`;
  `None` = right-censored, never recovered), and `recovered` (bool).
- **Good for:** RQ-C. Used by [E8](experiments/E8-resilience.md), which finds
  recovery is decided by *information*, not enforcement.
- **Next:** cumulative post-shock shortfall (an integral, not just time-to-90%);
  recovery under agent/communication failure.

### Robustness across seeds
- **Idea:** dispersion of a metric across seeds for a fixed config
  (e.g. coefficient of variation). Distinct from resilience.
- **Good for:** SQ-11; reporting how trustworthy a single run is.

### Sensitivity
- **Idea:** ∂(metric)/∂(parameter) estimated from a sweep (group size,
  regeneration rate, initial stock).
- **Good for:** SQ-12; mapping where regimes change (e.g. collapse thresholds).

### Role formation / stability, spatial organization
- **Idea:** emergence and persistence of distinct agent roles or spatial patterns.
- **Status:** requires heterogeneity/space not yet modelled; deferred.

## Reporting conventions

- Always report metrics as distributions across seeds (mean + spread), never a
  single seed.
- Always pair a performance metric with a sustainability metric — neither alone
  characterises a run.
- State `K`, `g`, `θ`, `N`, `T`, and the seed set alongside any metric table.

## Validation status

- `gini` extremes tested (`tests/test_experiment.py`).
- Sustainability/collapse behaviour tested via baseline dynamics
  (`tests/test_simulation.py`): all-selfish collapses, all-cooperative sustains.
