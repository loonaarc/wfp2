# E15 — Boundaries: Does Closing the Community to Outsiders Matter?

**Date:** 2026-08-07 · **Script:**
[`scripts/experiment_groups_boundaries.py`](../../scripts/experiment_groups_boundaries.py)
(shared with [E14](E14-groups-and-boundaries.md) — one joint sweep, per the
"Sweep design" resolution in
[thesis-direction-equifinality.md](../thesis-direction-equifinality.md); this
report covers the `open`-vs-`closed` contrast) · **Outputs:**
`results/E14_groups_boundaries/` · **Mechanism:**
[ADR-0013](../decisions/0013-boundaries-via-groups-reuse.md)

## Question

E14 found that nested (group-scoped) enforcement, even at full coverage,
leaves the shared pool exposed to any group that goes unmonitored. Ostrom's
principle 1 (clearly defined **boundaries**) suggests a different lever
entirely: instead of monitoring harder, exclude non-members from the pool
outright. Does actually closing the community off — rather than just
watching it more closely — change the outcome, and does that depend on
*which kind* of outsider you're excluding?

## Method

- Same population and resource setup as [E14](E14-groups-and-boundaries.md):
  8 governed agents split into `m` groups (`m ∈ {1, 2, 4}`), `k` of them
  `sanctioning`, the rest `selfish` (`k = 0..m`).
- **Boundary**: `closed` (no outsiders, = E14's results exactly) vs. `open`
  (+4 unmonitored `selfish` outsiders in their own, permanently ungoverned
  group — ADR-0013's reuse pattern: no new mechanism, just an extra
  `AgentSpec` with no sanctioner assigned to its group).
- **Outsider-strategy sweep**: at full coverage (`k=m`, closed vs. E14's
  established trap otherwise) and `open` boundary, which strategy the
  outsider group runs is varied across `selfish`, `cooperative`,
  `conditional_cooperator`, `compensating_cooperator` — i.e. what happens if
  the community *can't* exclude a given kind of outsider, only monitor its
  own members.
- Metric: `welfare_efficiency`, provisional threshold `≥ 0.80` (see E14 for
  why this number, not `0.95`).

**See it live:** [`web/commons-demo.html`](../../web/commons-demo.html)'s
"Boundary" dial (next to "Groups (nested)" in the Governance column) toggles
`closed`/`open access (+4 outsiders)` on the same live simulation.

## Results

**`welfare_efficiency`, open boundary, by (`m` groups, `k` sanctioning)** —
compare row-by-row against E14's closed table:

| | k=0 | k=1 | k=2 | k=3 | k=4 |
| --- | --: | --: | --: | --: | --: |
| m=1 | 0.06 | 0.01 | | | |
| m=2 | 0.06 | −0.01 | 0.01 | | |
| m=4 | 0.06 | 0.02 | −0.01 | −0.03 | 0.01 |

## Near-optimal-set-size vs. complexity: groups (`m`) × boundary

**This is the first genuine complexity result** — not a relabeling of E14's
single-axis correction. `m` (groups) and `boundary` (closed/open) are two
different structural axes (ADR-0012 and ADR-0013 respectively, built
independently), and every one of the resulting `3 × 2 = 6` cells is tested
below — a real, if minimal, factorial, unlike the earlier `m`-alone chart
this project correctly declined to call "the complexity curve" (see E14).

**Left panel below (count) vs. right panel (fraction) are two different
questions — keep them separate.** Combining them into one number is exactly
the mistake this project corrected once already for `m` alone (see E14); it
would be easy to repeat it here by accident now that a second axis is in
the mix, so this section reports both explicitly rather than picking one.

![Near-optimal-set-size vs. group count](../../results/E14_groups_boundaries/complexity_curve.png)

| m | closed (E14) count | open count |
| - | -: | -: |
| 1 | 1/2 | **0/2** |
| 2 | 1/3 | **0/3** |
| 4 | 1/5 | **0/5** |

**By count: adding boundary as an axis doesn't shrink anything — it adds
nothing.** The closed column is the exact same 1 winning configuration at
every `m` that E14 already found; boundary=open contributes zero *additional*
winning configurations at any `m`, but it doesn't take away the closed ones
either. Even the one configuration that always worked when closed (full
coverage, `k=m`) itself fails once 4 unmonitored outsiders are added:
`m=4, k=4` drops from `0.84` (closed) to `0.01` (open) — but that's a
statement about the *open* branch specifically having zero winners of its
own, not about the previously-closed winners disappearing.

**By fraction: the picture looks much worse, and that's worth flagging as
its own, different finding.** Once boundary=open is something you'd actually
consider, half of every space you'd have to search (all the open-boundary
configurations) is pure failure — 0 out of `m+1` at every `m` — which drags
the overall density of good outcomes in the *considered* space down
sharply. That's a real cost if you're searching by trial rather than by
design, even though it's not a cost to the *best available* answer, which
never gets worse than it already was under `boundary=closed` alone. No
amount of *internal* reorganisation — more groups, finer monitoring, full
coverage — substitutes for the ability to simply exclude an outsider that a
sanctioner, by construction, can never reach in a different, ungoverned
group; that's what the fraction collapsing to zero is actually showing.

**So does the near-optimal set grow as complexity increases, now that two
real axes are combined?** By count: no, but it doesn't shrink either — it
stays exactly flat at 1, the same as `m` alone (see E14). By fraction: yes,
it drops further than `m` alone ever did, because the open branch is a
100%-failure region added on top with nothing to offset it. Both are honest
readings of the same data; reporting only the fraction would overstate how
bad this is, and reporting only the count would understate how much harder
open access makes the search — worth keeping both, rather than waiting for
a bigger factorial to average them into one more favourable-sounding number.

## Near-optimal-set-size by outsider type, at full coverage

The result above uses a fixed `selfish` outsider. But is boundaries-matter a
general statement about *any* unmonitored outsider, or specifically about
outsiders who would actually over-harvest if left unexcluded? With every
governed group fully covered (`k=m`) and the boundary open, the outsider
group's own strategy is varied:

| m | closed | selfish outsiders | cooperative outsiders | conditional outsiders | compensating outsiders | set size |
| - | -: | -: | -: | -: | -: | -: |
| 1 | 0.84 ✅ | 0.01 ❌ | 0.84 ✅ | 0.84 ✅ | 0.84 ✅ | 4/5 |
| 2 | 0.84 ✅ | 0.01 ❌ | 0.84 ✅ | 0.84 ✅ | 0.84 ✅ | 4/5 |
| 4 | 0.84 ✅ | 0.01 ❌ | 0.84 ✅ | 0.84 ✅ | 0.84 ✅ | 4/5 |

**Only `selfish` outsiders fail — every other outsider type passes exactly
at the closed-baseline level (`0.84`), regardless of `m`.** This sharpens
the headline finding: boundaries don't matter *in general* — they matter
specifically against outsiders who would actually over-harvest if left
unexcluded. An unmonitored `cooperative`, `conditional_cooperator`, or
`compensating_cooperator` outsider group restrains itself on its own (it
still observes the shared stock under `global` information and behaves
accordingly), so exclusion buys nothing against it — the pool doesn't care
*why* an agent restrains, only that it does. **The near-optimal-set-size
here is constant across `m` (4/5 in every case)** — this slice (full
coverage only) doesn't show group count affecting the set size at all; `m`
only mattered in E14's partial-coverage tipping point, a different slice of
the same sweep. Reported as two separate findings deliberately, not merged
into one curve that would overstate either.

## Interpretation

1. **Boundaries dominate nested enforcement entirely, when the outsider is
   actually a threat.** Every `open` row in the main sweep stays at or below
   `0.06` regardless of `m` or `k` — internal group structure cannot
   substitute for exclusion against a genuinely greedy outsider.
2. **But boundaries are not a blanket requirement — they're conditional on
   who you'd be excluding.** Against outsiders who restrain themselves
   anyway (any of the three non-`selfish` types tested), an open boundary
   costs nothing. This is a real qualification of "boundaries dominate," not
   a contradiction of it: the mechanism that matters is *whether the
   excluded party would over-harvest*, not exclusion for its own sake.
3. **This is the concrete payoff of treating boundaries as a genuinely
   separate axis from groups (ADR-0013)**, rather than assuming "more
   internal monitoring" is a general fix for any external pressure on the
   commons.

## Threats to validity / limitations

- **Fixed outsider count (4) and a single boundary "size"** — the
  open/closed contrast isn't itself swept by degree (e.g. 1, 2, 4, 8
  outsiders); it's plausible a small number of outsiders is tolerable where
  4 is not.
- **The near-optimal-set-size threshold (`0.80`) is provisional** — see
  E14's equivalent note; the same caveat applies here.
- **Outsider strategies are homogeneous within the group** — all 4 outsiders
  always share one strategy; a mixed outsider group (some selfish, some
  restrained) is untested.
- **Boundaries here is a *simplified* operationalization of Ostrom principle
  1** (see ADR-0013's own "Consequences"): outsiders are unmonitored, not
  literally barred from the pool. A harder-exclusion variant (outsiders
  never instantiated, vs. instantiated-but-unwatched) would test the
  stronger reading of the principle.

## Follow-ups

- Sweep outsider count by degree (1, 2, 4, 8) to find the tolerance
  threshold, rather than only testing the binary on/off contrast.
- Mixed-strategy outsider groups, not just homogeneous ones.
- A literal "hard exclusion" variant (outsiders never participate at all,
  vs. participate unmonitored) to test the stronger reading of principle 1
  against the current, softer one.
- See also [E14](E14-groups-and-boundaries.md)'s follow-ups for the groups
  axis this one builds on.
