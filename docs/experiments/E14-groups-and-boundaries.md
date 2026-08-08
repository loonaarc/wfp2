# E14 — Nested Enforcement: How Many Groups Need a Monitor?

**Date:** 2026-08-07 · **Script:**
[`scripts/experiment_groups_boundaries.py`](../../scripts/experiment_groups_boundaries.py)
(shared with [E15](E15-boundaries.md) — designed as one joint sweep per the
"Sweep design" resolution in
[thesis-direction-equifinality.md](../thesis-direction-equifinality.md); this
report covers the `closed`-boundary slice only) · **Outputs:**
`results/E14_groups_boundaries/` · **Mechanism:**
[ADR-0012](../decisions/0012-nested-enterprise-groups.md)

## Question

The first structural axis for the equifinality thesis direction (see
[thesis-direction-equifinality.md](../thesis-direction-equifinality.md)):
does *nested* enforcement (each group polices only itself, Ostrom principle 8)
behave differently from the flat, population-wide enforcement every prior
experiment (E3–E13) used — and, as group-count complexity (`m`) increases,
does the near-optimal set grow, per the equifinality conjecture (see
[thesis-direction-equifinality.md](../thesis-direction-equifinality.md))?

## Method

- Population: **fixed at 8 governed agents, closed community** (no outsiders —
  see [E15](E15-boundaries.md) for the open-access comparison), split into
  `m` equal groups of size `n = 8/m`, for `m ∈ {1, 2, 4}`.
- Within each `m`, **`k` of the `m` groups are `sanctioning`, the rest
  `selfish`** free-riders (`k = 0..m`) — `selfish`, not `cooperative`, is what
  actually exercises nested enforcement: it gives the sanctioning groups an
  internal free-rider group to be protected *from*.
- Resource: logistic, `K = 100`, `g = 0.4` (`MSY = 10`), collapse threshold
  1.0, 100 rounds, `initial_level = 50`.
- Metric: `welfare_efficiency` (net payoff relative to the `MSY·T` benchmark;
  see `docs/metrics.md`) and `sustainability_ratio`. Raw values, not a
  behavioural/non-behavioural classification, except in the dedicated
  "complexity curve" section below, which uses a clearly-flagged provisional
  threshold.
- Deterministic strategies (`sanctioning`, `selfish` both draw no randomness),
  single seed — exact, not a noisy mean (same reasoning as E1).

![E14/E15 results](../../results/E14_groups_boundaries/figure.png)

**See it live:** [`web/commons-demo.html`](../../web/commons-demo.html) has a
"Groups (nested)" dial in the Governance column. Set 4 monitors + 4 selfish
agents, then step "Groups" from 1 → 2 → 4 and watch the ring's group dividers
appear and the outcome flip — that's the `k=m/2` dip and the `k=m` recovery
from the table below, live.

## Results

**`welfare_efficiency` by (`m` groups, `k` sanctioning), closed community:**

| | k=0 | k=1 | k=2 | k=3 | k=4 |
| --- | --: | --: | --: | --: | --: |
| m=1 | 0.06 | 0.84 | | | |
| m=2 | 0.06 | 0.01 | 0.84 | | |
| m=4 | 0.06 | 0.03 | 0.01 | 0.53 | 0.84 |

## Near-optimal-set-size vs. group count (`m`) — not "complexity"

**Correction:** an earlier version of this section called this "the
complexity curve." That overclaimed what it actually shows. `m = 1, 2, 4` is
one axis's own internal range (how many groups), the same shape as sweeping
`information_model ∈ {global, private}` — which this project already
treated as *not* complexity on its own, just a value change too narrow to
show a trend by itself. Real complexity, per the original framing
("richer... richer *still*"), means combining *multiple different* axes into
one ordered dial — which this chart does not do. What follows is a real,
honest, single-axis finding — just not the complexity story.

**As `m` increases, does the near-optimal set grow?** Reusing the grid
above, classified at a **provisional `welfare_efficiency ≥ 0.80` threshold**
— picked from the numbers actually observed, not guessed blind: full
sanctioning coverage tops out at `0.84` (the monitoring cost mechanically
prevents `1.0`), so a `0.95`-style bar would disqualify enforcement by
construction before any comparison could even happen. `0.80` sits just below
that structural ceiling. **This is still provisional, not yet finalized.**
For each `m`, how many of the `m+1` possible coverage
levels (`k = 0..m`) are behavioural?

| m | near-optimal / tested |
| - | -: |
| 1 | 1/2 |
| 2 | 1/3 |
| 4 | 1/5 |

![Near-optimal-set-size vs. group count](../../results/E14_groups_boundaries/complexity_curve.png)

**No — within this one axis, more groups does not grow the near-optimal
set. It also never shrinks below where it started; it simply never moves.**
Two different questions, shown as the chart's two panels, because
conflating them into one number can manufacture a "shrinking" story that
isn't really there (see the [thesis-direction
note](../thesis-direction-equifinality.md) for the general version of this
mistake, caught here first): the **count** (left panel) of successful
configurations stays flat at exactly **1** for every `m` (only full
coverage, `k=m`, ever clears the bar) — more groups never produces more than
one path to a good outcome, but it doesn't produce fewer either. The
**fraction** of the *tested* space that succeeds (right panel) does drop —
1/2 → 1/3 → 1/5 — but only because finer-grained partitioning creates more
ways to land in the partial-coverage trap (see "Interpretation" below) while
the count of ways to avoid it stays fixed at one; that's a statement about
how hard the good answer is to stumble into, not about the good answer
itself disappearing. **A real complexity curve — combining this axis with
others (information, boundaries, resources) into one ordered dial — has not
been built yet** beyond the minimal 2-axis version in
[E15](E15-boundaries.md). See the note's "Sweep design" section for what a
fuller one would take.

This is a genuine, reportable negative result for the equifinality
conjecture, specific to this axis: nested enforcement granularity is a case
where more structure never produces more than one working approach, and
makes that one approach proportionally harder to find by chance — worth
stating plainly, not reframed to sound more positive than the numbers
support. (See [E15](E15-boundaries.md) for the same comparison
under open access — spoiler: it's empty at every `m`.)

## Interpretation

1. **Partial nested coverage can be *worse* than no coverage at all.**
   `m=2, k=1` (one sanctioning group, one still-selfish group) scores `0.01`
   — *below* `m=2, k=0` (`0.06`, both groups selfish, nobody paying to
   monitor). The sanctioning group pays its monitoring cost and restrains
   itself, but the pool still collapses because the other, still-unmonitored
   group alone is enough to crash it — so that group paid a cost for
   protection that never materialised. The same dip appears at `m=4, k=1,2`.
2. **The `k=3` "recovery" is not a success story — it's the majority getting
   exploited.** Aggregate welfare jumps from `0.01` to `0.53` between `k=2`
   and `k=3`, which originally read as "the sanctioning majority's restraint
   finally becomes sufficient." **The per-strategy payoff breakdown shows the
   opposite:** at `m=4, k=3`, the 6 sanctioning agents net **`−18.75` each**
   — below zero, worse than doing nothing — while the 2 still-unmonitored
   selfish agents net **`323.26` each**, roughly 3× what a *fully protected*
   sanctioning agent earns in the `k=4` case (`105`). The mechanism: 6
   disciplined agents barely touch the pool, so it stays well-regenerated —
   which the 2 free-riders then get to repeatedly harvest from. **The
   majority's restraint doesn't fix the problem, it subsidises it** — a
   healthier pool for two agents to keep exploiting harder. The aggregate
   `welfare_efficiency` number alone hid this completely; it only surfaced
   once a per-agent payoff breakdown was added (see `docs/metrics.md`'s
   `payoff_gini` note — the mean-absolute-difference Gini formula is
   undefined here too, since the sanctioning agents' payoff is negative, and
   silently produced nonsense numbers like `13` or `−8` before that was
   fixed). This does **not** change which configurations were classified
   near-optimal (only the *fully-covered*, uniformly-fair cells ever cleared
   the `0.80` threshold), but it means the qualitative story for every
   *non*-passing partial-coverage cell was wrong as originally written: they
   don't fail by "not quite working yet," several of them fail by actively
   enriching a small minority at the disciplined majority's expense.
3. **Full coverage (`k=m`) always reaches the same `0.84`, regardless of
   `m`.** One group of 8, two of 4, or four of 2 — as long as every group has
   its own sanctioner, welfare is identical. This matches ADR-0012's own
   design guarantee (dividing the quota by total population, not group size,
   keeps every fully-covered configuration equivalent to the original flat
   case) — confirmed here as an experimental result, not just a formula.

## Threats to validity / limitations

- **Only two `m` "shapes" beyond the flat baseline** (`m=2`, `m=4`); `m=8`
  (every agent its own group) is untested.
- **`k` groups are always the *first* `k`**, not randomized — with
  deterministic strategies this doesn't matter for the numbers reported
  (symmetry across which specific groups are covered), but it means no
  seed-to-seed variation was explored for *which* groups end up monitored.
- **The near-optimal-set-size threshold (`0.80`) is provisional**, picked
  from the observed numbers rather than independently settled in advance —
  treat the complexity-curve figures above as illustrative of the *method*,
  not a final result.
- **`sanctioning` is currently the only registered strategy that exposes a
  `SanctionPolicy`** — no other strategy (`cooperative`,
  `conditional_cooperator`, `compensating_cooperator`, `selfish`, `loner`)
  can act as a group's covering institution. So "how many *institution
  types* can protect a group" is not yet a testable question here.
- **Not yet connected to Nowak (2006)'s `b/c > 1+n/m` formula** — that
  requires a group-selection (replicator, groups reproduce/split) setup,
  which this experiment does not build; the `n`/`m` sweep here is inspired by
  and comparable to that logic, not a literal reproduction of it. Worth being
  explicit about this distinction in the thesis write-up.

## Follow-ups

- Sweep `m=8` and randomize which `k` groups are covered, to check whether
  the tipping-point location depends on which specific groups are covered or
  only on the count.
- Fix and apply a tolerance-band threshold (the still-open question from
  `thesis-direction-equifinality.md`) for real, and extend the sweep to the
  rest of the existing strategy roster (conditional cooperator, compensating,
  pool punishment, voted agreement), not just sanctioning vs. selfish.
- A genuine Nowak-style group-selection variant (groups reproduce/split by
  fitness) as a distinct, explicitly-labelled follow-up, not conflated with
  this static-partition experiment.
- See also [E15](E15-boundaries.md)'s follow-ups for the boundaries axis.
