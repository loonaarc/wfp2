# E16 — Boundaries: Does Closing the Community to Outsiders Matter?

**Date:** 2026-08-07, reworked 2026-08-09 · **Script:**
[`scripts/experiment_boundaries_full_sweep.py`](../../scripts/experiment_boundaries_full_sweep.py)
(supersedes the original `scripts/experiment_groups_boundaries.py`, whose
outsider-*type* sub-study is still reused directly — see Method) ·
**Outputs:** `results/E16_boundaries_full_sweep/` · **Mechanism:**
[ADR-0013](../decisions/0013-boundaries-via-groups-reuse.md)

## Question

[E15](E15-groups.md) found that nested (group-scoped)
enforcement, even at full coverage, leaves the shared pool exposed to any
group that goes unmonitored. Ostrom's principle 1 (clearly defined
**boundaries**) suggests a different lever entirely: instead of monitoring
harder, exclude non-members from the pool outright. Does actually closing
the community off — rather than just watching it more closely — change the
outcome, and does that depend on *which kind* of outsider you're excluding?

## Method — reworked 2026-08-09

**The original version crossed E15's old 2-type `k`-sweep against a single,
fixed adversarial outsider (`selfish`).** Once E15 itself moved to a full
5-type compositional sweep, leaving E16 on the old narrow governed-side
sweep would have made the "closed vs. open" comparison inconsistent with
what "closed" now means in E15. This version:

- **Governed side: reuses E15's full sweep exactly** — every joint
  combination of per-group compositions, `m ∈ {1, 2, 4}` (495 / 4,900 /
  50,625 configurations respectively; see E15's Method for the
  combinatorics). The `closed` numbers below are E15's own results,
  unchanged, not recomputed.
- **Outsider side: Monte Carlo sampled, not exhaustively enumerated.**
  Crossing the governed sweep against all 70 possible 4-agent outsider
  compositions would be `56,020 × 70 ≈ 3.9M` simulations (~2+ hours) —
  intractable, and exactly the problem this project's own adopted
  methodology (GLUE, Beven & Binley 1992/2014; see
  `docs/literature-review.md`) already has an answer for: sample instead of
  enumerating, and report the near-optimal **fraction** with a confidence
  interval instead of an exact count. This experiment is where that
  procedure was first needed — see
  [experiment-design.md#sampling-a-large-configuration-space-monte-carlo--glue](../experiment-design.md#sampling-a-large-configuration-space-monte-carlo--glue)
  for the general recipe (now reused by the live demo too). **Validated
  first against E15's own exact `m=4` result** (18,737/50,625 = 0.3701): a
  5,000-sample estimate landed at 0.3628 ± 0.0133 (95% CI), comfortably
  containing the true value — see the script's own docstring. `N_SAMPLES =
  5,000` per `m` is used below for the same reason.
- Sampling is uniform over the **distinct composition space** (matching how
  E14/E15 count near-optimal-set-size: each composition is one "approach,"
  not weighted by how many agent-labelings realize it) — achieved by
  independently sampling each group's own sub-composition, and the
  outsider's composition, uniformly from their own enumerated lists.
- **Outsider-*type* sub-study kept exactly as originally designed**: at full
  coverage (every group uniformly `sanctioning`) and boundary open, the
  outsider's own strategy is varied across 4 named types — small and exact,
  unaffected by the rework above (it never touched the governed-composition
  dimension this rework generalizes).
- Metric: `welfare_efficiency`, same provisional `≥ 0.80` threshold as
  E14/E15.

## Results

![Near-optimal-set-size vs. m x boundary](../../results/E16_boundaries_full_sweep/near_optimal_by_m_boundary.png)

| m | closed count (exact) | closed fraction | open count (estimated) | open fraction | open 95% CI (fraction) |
| -: | -: | -: | -: | -: | -: |
| 1 | 383 / 495 | 0.774 | 16,812 / 34,650 | 0.485 | [0.451, 0.520] |
| 2 | 2,820 / 4,900 | 0.576 | 101,391 / 343,000 | 0.296 | [0.257, 0.335] |
| 4 | 18,737 / 50,625 | 0.370 | 503,921 / 3,543,750 | 0.142 | [0.113, 0.171] |

**Read the count column carefully — it is not a fair "which is bigger"
comparison, and reporting it without this caveat would repeat, in a new
shape, the exact mistake this project has now corrected three times (see
`docs/complexity-synthesis.md`'s methodological lessons).** `closed` and
`open` are counts over **different-sized spaces** — closed only has the
governed population's own choices; open has the governed population's
choices *combined with* the outsider's, so its total space is 70× bigger at
every `m`. Open's count looking larger than closed's (16,812 vs. 383 at
`m=1`) is mostly an artifact of that bigger denominator, not evidence that
opening the boundary creates more good options. **The fraction column is
the fair comparison**, since it normalises for each condition's own space
size:

**By fraction, opening the boundary consistently costs roughly half the
success rate, at every `m`:** 0.774→0.485 (m=1), 0.576→0.296 (m=2),
0.370→0.142 (m=4) — a near-constant ~1.9–2.6× reduction, not a collapse to
zero the way the old (adversarial-only) reading suggested, but a real,
substantial, and consistent cost. This reconciles the two earlier,
seemingly contradictory readings of "does boundary matter": against the
adversarial-only slice (the outsider-type sub-study below, and the earlier
narrow sweep), it looked catastrophic (near-optimal count driven to 0);
against the *full* outsider-composition space, most outsider draws are
actually tolerable (matching the outsider-type sub-study's own finding that
`cooperative`/`compensating_cooperator` outsiders cost nothing) — so the
*average* cost across all possible outsiders lands at "meaningfully worse,
not existentially worse."

## Outsider-type sub-study (unchanged methodology)

At full coverage (every group uniformly `sanctioning`), boundary open, the
outsider's own strategy varied across 4 named types:

| m | closed | selfish outsiders | cooperative outsiders | conditional outsiders | compensating outsiders | set size |
| - | -: | -: | -: | -: | -: | -: |
| 1 | 0.84 ✅ | −0.00 ❌ | 0.84 ✅ | 0.01 ❌ | 0.84 ✅ | 3/5 |
| 2 | 0.84 ✅ | −0.00 ❌ | 0.84 ✅ | 0.01 ❌ | 0.84 ✅ | 3/5 |
| 4 | 0.84 ✅ | −0.00 ❌ | 0.84 ✅ | 0.01 ❌ | 0.84 ✅ | 3/5 |

Only `selfish` and `conditional_cooperator` outsiders fail; `cooperative`
and `compensating_cooperator` pass exactly at the closed-baseline level
(`0.84`), regardless of `m`. `conditional_cooperator`'s failure is a
rediscovery of E14's own finding: a reactive/retaliatory response gets
tripped by the governed population's own harvest swings, independent of
whether the reactor is inside or outside the boundary. See E14's
Interpretation for the mechanism.

## Interpretation

1. **The honest headline is now two-part, not one number**: opening the
   boundary essentially never *eliminates* the near-optimal set (unlike the
   old adversarial-only reading), but it reliably *halves* your odds of
   landing in it, across every group count tested. Both the "it's not
   catastrophic" and "it's a real, consistent cost" halves of that claim are
   true simultaneously, and reporting only one would be the same kind of
   selective-reporting mistake this project keeps having to correct.
2. **The mechanism is exactly what the outsider-type sub-study already
   named**: most possible outsiders (sampled uniformly across the
   composition space) don't contain enough `selfish` presence, or contain a
   `conditional_cooperator` presence, to actually threaten the pool — see
   E14/E15's own "unprotected group" finding, which generalizes directly to
   an *unprotected outsider batch* here.
3. **Count and fraction disagreeing about which condition looks "bigger"
   is itself the finding worth remembering going forward**: any time an
   axis changes what the *total* space being measured even is (not just how
   large a fixed-shape space is), raw counts across conditions stop being
   comparable, and only within-condition fractions (or a matched,
   same-space count) are safe to compare directly.

## Threats to validity / limitations

- **The open-boundary numbers are estimates, not exact counts** — the
  95% CIs above are real and should be carried into any downstream claim
  (e.g. `docs/complexity-synthesis.md`), not dropped once the point
  estimate is quoted.
- **Fixed outsider count (4)** — the open/closed contrast isn't swept by
  outsider *count* (1, 2, 4, 8); a smaller outsider batch is plausibly more
  tolerable.
- **The near-optimal-set-size threshold (`0.80`) is provisional**, same
  caveat as E14/E15.
- **Outsider composition sampling uses one seed (42) for the RNG stream**
  — re-running with a different seed would give a slightly different point
  estimate within the same CI, not a different qualitative story; not
  independently re-verified with a second seed here.
- **Boundaries here is a *simplified* operationalization of Ostrom
  principle 1** (see ADR-0013's own "Consequences"): outsiders are
  unmonitored, not literally barred from the pool.

## Follow-ups

- **A matched, same-space count comparison** — e.g. "of the governed
  compositions that pass when closed, what fraction *also* pass against a
  randomly drawn outsider when open" — a paired statistic that would avoid
  the count-comparability problem entirely, rather than relying on fraction
  alone.
- Sweep outsider count by degree (1, 2, 4, 8) to find the tolerance
  threshold, rather than only testing the binary on/off contrast.
- A literal "hard exclusion" variant (outsiders never participate at all,
  vs. participate unmonitored) to test the stronger reading of principle 1.
- Re-run the Monte Carlo sample with a second seed to confirm the CI
  behaves as expected, now that it's load-bearing for a headline number.
- See also [E15](E15-groups.md)'s follow-ups for the groups
  axis this one builds on, and [E14](E14-population-diversity.md)'s
  revised-diversity-axis follow-up, which both `m` and `boundary` now
  inherit compositional richness from.
