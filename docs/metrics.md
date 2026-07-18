# Metrics

Candidate and implemented metrics for evaluating runs. Each entry gives a
definition, formula, assumptions, what it is good for, and its limitations.
Implemented metrics are produced by `metrics.compute_metrics` (one row per run).

Notation: `N` agents, `T` rounds. For round `t`: `R_t` = stock after harvest,
`H_t` = total harvest. Agent `i` accumulates payoff `P_i = Σ_t h_{i,t}`. `K` =
carrying capacity, `g` = regeneration rate.

## Implemented (v0.1.0)

### System performance — `total_harvest`, `mean_agent_payoff`
- **Definition:** total resource harvested over the run; and its mean per agent.
- **Formula:** `total_harvest = Σ_i P_i`; `mean_agent_payoff = (Σ_i P_i)/N`.
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

## Candidate (planned)

### Cooperation rate
- **Idea:** how much agents restrain relative to a selfish benchmark.
- **Candidate formula:** `1 − (mean actual harvest) / (mean selfish-benchmark
  harvest)`, or the fraction of rounds an agent harvests ≤ its sustainable share.
- **Open question:** which benchmark is fairest and comparable across configs.

### Recovery time / resilience (needs disturbances)
- **Idea:** rounds to return within `ε` of the pre-shock stock (or payoff rate)
  after a disturbance; and whether recovery occurs at all.
- **Good for:** RQ-C. **Depends on:** the `disturbances` module.

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
