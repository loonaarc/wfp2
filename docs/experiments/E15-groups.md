# E15 — Nested Enforcement: How Many Groups Need a Monitor?

**Date:** 2026-08-07, reworked 2026-08-09 · **Script:**
[`scripts/experiment_groups_full_sweep.py`](../../scripts/experiment_groups_full_sweep.py)
(supersedes the original `scripts/experiment_groups_boundaries.py` k-sweep,
kept for E16's outsider-side use) · **Outputs:**
`results/E15_groups_full_sweep/` · **Mechanism:**
[ADR-0012](../decisions/0012-nested-enterprise-groups.md)

## Question

The first structural axis for the equifinality thesis direction (see
[thesis-direction-equifinality.md](../thesis-direction-equifinality.md)):
does *nested* enforcement (each group polices only itself, Ostrom principle 8)
behave differently from the flat, population-wide enforcement every prior
experiment (E3–E13) used — and, as group-count complexity (`m`) increases,
does the near-optimal set grow, per the equifinality conjecture?

## Method — reworked 2026-08-09

**The original version of this experiment only varied `k`: how many of the
`m` groups were fully `sanctioning` vs. fully `selfish`** — a 2-type sweep,
exactly the kind of narrow composition [E14](E14-population-diversity.md)
(population-type diversity) was built to generalize away from. Once E14
existed, leaving E15 on the old 2-type sweep would have meant testing groups
and population-composition as if they were independent, when the whole
point of building E14 first was that they aren't. This version applies
E14's full 5-type compositional sweep *independently to each group*: every
group of size `N/m` gets its own composition across `cooperative`,
`conditional_cooperator`, `compensating_cooperator`, `selfish`, and
`sanctioning`, and every combination of per-group compositions is tested —
not just uniform, single-strategy groups.

- Population: **fixed at 8 governed agents, closed community**, split into
  `m` equal groups of size `n = 8/m`, for `m ∈ {1, 2, 4}`.
- **Every joint combination of per-group compositions** (stars-and-bars per
  group, crossed across groups):

  | m | compositions per group | joint configurations |
  | -: | -: | -: |
  | 1 | `C(8+5-1,4) = 495` | 495 *(= E14 itself)* |
  | 2 | `C(4+5-1,4) = 70` | `70² = 4,900` |
  | 4 | `C(2+5-1,4) = 15` | `15⁴ = 50,625` |

  **56,020 simulations total.**
- Resource: logistic, `K = 100`, `g = 0.4` (`MSY = 10`), collapse threshold
  1.0, 100 rounds, `initial_level = 50`.
- Metric: `welfare_efficiency`, same provisional `≥ 0.80` threshold as E14.
- Single seed, deterministic strategies — exact, not a noisy mean.
- **Deliberately not extended the same way to boundaries (E16)'s outsider
  side**: crossing this same full sweep against a fully-explored outsider
  composition would be `56,020 × 70 ≈ 3.9M` simulations (~2+ hours) for a
  result that would be unwieldy to summarise. E16 keeps the outsider side at
  its existing, already-validated treatment and crosses only the *governed*
  side with this full sweep.

**See it live:** [`web/commons-demo.html`](../../web/commons-demo.html) has a
"Groups (nested)" dial in the Governance column, though the demo's own
population dials still only reach the simpler compositions (monitor/selfish/
one cooperator type at a time) — the full 56,020-configuration sweep is a
batch analysis, not something animated round-by-round.

## Results

![Near-optimal-set-size vs. group count, full sweep](../../results/E15_groups_full_sweep/near_optimal_by_m.png)

| m | configs tested | near-optimal count | fraction |
| -: | -: | -: | -: |
| 1 | 495 | 383 | 0.774 |
| 2 | 4,900 | 2,820 | 0.576 |
| 4 | 50,625 | 18,737 | 0.370 |

**By count, the near-optimal set genuinely grows — 383 → 2,820 → 18,737 —
not a denominator artifact this time.** Unlike E14's diversity axis (where
the tested-space size ballooned and shrank for reasons unrelated to
difficulty), here the growing space *is* the thing being tested: more
groups means more independent slots, each of which can itself be either
"safe" or "unprotected," and the number of ways to combine safe slots
grows combinatorially with how many slots exist. This is the most positive
finding for the equifinality conjecture so far in this project — see
Interpretation for why, and why the fraction still drops even though the
count doesn't.

**The driver, decomposed (at `m=4`):** call a group *unprotected* if it has
at least one `selfish` agent and zero `sanctioning` agents in it — nested
enforcement means a group's own sanctioner never reaches a different group
(ADR-0012), so an unprotected group is a real, uncontained liability to the
shared pool.

| unprotected groups (of 4) | passing | tested | rate |
| -: | -: | -: | -: |
| 0 | 14,641 | 14,641 | **100%** |
| 1 | 4,096 | 21,296 | 19% |
| 2+ | 0 | 14,688 | **0%** |

**Zero unprotected groups always passes. Two or more never passes. Exactly
one sometimes does** — depending on how weak that one group's selfish
presence is and what the rest of its own composition looks like (the same
compensating-vs-reciprocal distinction E14 found matters within a group
also matters here). This single rule accounts for nearly all of the count
growth: as `m` increases, "zero unprotected groups" has combinatorially more
ways to happen (more independent all-or-nothing slots to fill safely), which
is a real richness of the space, not an artifact.

## Interpretation

1. **This reframes the equifinality question for this axis from "no" to
   "yes, substantially, but it gets proportionally harder to find by
   chance."** The count triples then grows another ~6.6× as `m` goes
   1→2→4; the fraction still nearly halves at each step (0.774 → 0.576 →
   0.370). Both are true and both matter — see
   [complexity-synthesis.md](../complexity-synthesis.md)'s lesson on
   reporting count and fraction separately, which applies here exactly as
   it did before, just with the growth finally showing up in the count too.
2. **"More groups helps" is conditional on covering every group, not on
   covering more of the population in aggregate.** A single unprotected
   group anywhere is enough to threaten the pool at `m=4` (94% of
   1-unprotected-group configs still fail); the near-optimal set grows
   because there are more ways to *avoid* ever having an unprotected group,
   not because partial protection becomes more forgiving.
3. **This supersedes, but doesn't erase, the original k-sweep's own
   findings** — see "Historical: the original k-sweep" below. Those
   findings (partial coverage can be worse than none; the `k=3` "recovery"
   secretly subsidises two free-riders) are still true statements about
   that narrower slice of the space; they just aren't the whole picture
   once every composition is considered, not only uniform sanctioning/
   selfish splits.

## Historical: the original k-sweep (superseded 2026-08-09)

The original version of this experiment tested only `k` of `m` groups fully
`sanctioning`, the rest fully `selfish` — kept here for continuity, not as
the current headline result.

**`welfare_efficiency` by (`m` groups, `k` sanctioning), closed community:**

| | k=0 | k=1 | k=2 | k=3 | k=4 |
| --- | --: | --: | --: | --: | --: |
| m=1 | 0.06 | 0.84 | | | |
| m=2 | 0.06 | 0.01 | 0.84 | | |
| m=4 | 0.06 | 0.03 | 0.01 | 0.53 | 0.84 |

Under this narrow 2-type reading, the near-optimal **count** stayed flat at
exactly 1 (only full coverage, `k=m`, ever passed) for every `m` — the
opposite conclusion from the full-sweep result above. That flat-count
finding wasn't wrong, it was *narrow*: restricting every group to be
uniformly one of only two types (rather than any of five) rules out almost
all of the compositions that the full sweep shows do work. The original
findings about *why* partial coverage fails remain accurate for that slice:

1. **Partial nested coverage can be *worse* than no coverage at all.**
   `m=2, k=1` (one sanctioning group, one still-selfish group) scores `0.01`
   — *below* `m=2, k=0` (`0.06`). The sanctioning group pays its monitoring
   cost and restrains itself, but the pool still collapses because the
   other, still-unmonitored group alone is enough to crash it.
2. **The `k=3` "recovery" was not a success story — it was the majority
   getting exploited.** At `m=4, k=3`, the 6 sanctioning agents net
   **`−18.75` each** — below zero — while the 2 still-unmonitored selfish
   agents net **`323.26` each**. Six disciplined agents barely touch the
   pool, keeping it well-regenerated for two free-riders to keep exploiting.
   The aggregate `welfare_efficiency` number alone hid this; it only
   surfaced once a per-agent payoff breakdown was added (see
   `docs/metrics.md`'s `payoff_gini` note).
3. **Full coverage (`k=m`) always reached the same `0.84`, regardless of
   `m`** — one group of 8, two of 4, or four of 2, as long as every group
   had its own sanctioner. This matches ADR-0012's design guarantee
   (dividing the quota by total population, not group size) and is still
   true: full-sanctioning-coverage is one of the many compositions the full
   sweep now also finds passing.

## Threats to validity / limitations

- **Only three `m` values** (`1, 2, 4`); `m=8` (every agent its own group)
  is untested, and would itself be `C(1+5-1,4)=1` composition per group ×
  `1^8=1` — actually trivial to add (every group is a single agent, so
  every group is automatically "one type"), worth doing as a follow-up.
- **The near-optimal-set-size threshold (`0.80`) is provisional**, same
  caveat as E14.
- **Single seed, deterministic strategies** — exact for what's tested, not
  a noisy mean; a `decision_noise > 0` variant would need seed averaging
  across all 56,020 configurations, a much larger compute budget.
- **Not yet connected to Nowak (2006)'s `b/c > 1+n/m` formula** — that
  requires a group-selection (replicator, groups reproduce/split) setup,
  which this experiment does not build.
- **Group composition is still uniform *within* the type-count** (e.g. "2
  cooperative" doesn't distinguish which 2 of the group's slots they fill —
  irrelevant here since agents of the same strategy are interchangeable,
  but worth noting for readers expecting agent-level, not strategy-level,
  enumeration).

## Follow-ups

- **`m = 8`** (every agent its own group) — cheap to add per the note above.
- **Randomize which groups get which composition**, rather than exploring
  the full deterministic assignment — with deterministic strategies this
  doesn't change any reported number (symmetry across which specific groups
  get which composition), but no seed-to-seed variation was explored.
- A genuine Nowak-style group-selection variant (groups reproduce/split by
  fitness) as a distinct, explicitly-labelled follow-up, not conflated with
  this static-partition experiment.
- See also [E16](E16-boundaries.md)'s follow-ups for the boundaries axis,
  and [E14](E14-population-diversity.md)'s follow-up on a revised,
  two-boolean diversity axis — worth reapplying here too, since "zero
  unprotected groups" is itself close to that same shape.
