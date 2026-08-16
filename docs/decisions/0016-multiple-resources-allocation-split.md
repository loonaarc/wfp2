# ADR-0016: Multiple resources / specialization via a second pool and a per-agent allocation split

- **Status:** Accepted
- **Date:** 2026-08-15
- **Deciders:** project owner (approved scope), assistant (implementing)

## Context

GovSim (Piatti et al., 2024) names "varying regeneration rates and multiple
resource types" directly as its own future work — the next axis by grounding
in the ranked list (`thesis-direction-equifinality.md`), now that reputation
(E18, ADR-0014) and network reciprocity (E19, ADR-0015) are both built. The
project owner's explicit brief, same as for network reciprocity: build the
version that "makes the most sense," is "well-argued," and has "added
value" — not the cheapest one that merely ticks the box.

Two design questions had to be resolved before this was buildable: how does
an agent's existing decision rule extend to more than one resource, and does
every other mechanism (sanctioning, reputation, collective choice,
disturbances) need to extend too.

## Considered Options

1. **Widen `Strategy.decide()`'s interface** to return a request *per pool*
   and widen `Observation` to carry per-pool state. Rejected: this touches
   every existing strategy (`selfish`, `cooperative`, `conditional`,
   `compensating`, `sanctioning`, `reputation`) and the core `Agent`/
   `Observation` contract — a far larger, more invasive change than the
   axis needs, and it would make every future strategy addition carry
   multi-resource complexity whether or not it cares.
2. **Two identical pools with a single shared allocation number split
   arithmetically, sanctioning left untouched (a monitor "just covers
   everything" for free), specialization a cosmetic label only.** *(The
   cheap version, considered and rejected — not built.)* Symmetric pools
   give an agent no actual reason to prefer one over the other, so
   "specializing" carries no real stakes; and monitoring both resources for
   free removes the one institutional-design tradeoff (specialized vs.
   generalist monitors) that makes this axis more than a repeat of E1's
   single-pool story with an extra dial.
3. **A second, independent `ResourcePool`, existing strategies reused
   completely unchanged, each called once per pool against that pool's own
   observation, scaled by a new per-agent `AgentSpec.allocation_split`; the
   two pools deliberately asymmetric; sanctioning extended per-pool at real
   cost.** *(Chosen.)*

## Decision

Option 3. `SimulationConfig.second_resource: ResourceConfig | None = None`
(a plain `ResourceConfig`, no wrapper type needed) and
`AgentSpec.allocation_split: float = 1.0` (fraction of the agent's request
routed to the first pool; `1.0` is a no-op, reproducing today's
single-pool behaviour exactly). `Simulation` builds a second `ResourcePool`
when configured; each active agent's *existing* `decide()` runs once
against each pool's own `Observation` (own capacity, own current level),
and the two raw requests are scaled by `allocation_split` / `1 -
allocation_split` before being allocated and enforced — one call each to
the *unmodified* `_allocate`/`_enforce`, now parameterized by which pool/
resource config they're acting on instead of hardcoded to `self.pool`.

The two pools used in the built experiment (E20) are deliberately
asymmetric — Pool A: `K=100, g=0.4` (the project's existing default,
"reliable"); Pool B: `K=100, g=0.2` ("fragile," half the growth rate) — so
specialization is a real choice with real consequences, not an arbitrary
label.

**A real bug was caught and fixed during implementation, not just
considered up front:** `conditional_cooperator` and `compensating_cooperator`
each keep their own per-instance state across rounds (`_last_level`, "did
the stock I'm watching decline since I last looked"). The first version of
this engine change called `agent.decide()` once per pool using the *same*
strategy instance both times — which meant that instance's `_last_level`
alternated between two unrelated pools' levels every round, corrupting the
"declined" comparison for both. E20's own experiment doesn't use either
strategy (it uses `cooperative`/`selfish`/`sanctioning`), so this never
showed up in E20's own results — but it would have silently produced wrong
behaviour for anyone combining `conditional_cooperator` or
`compensating_cooperator` with `second_resource`. Fixed by giving each agent
a *second*, independent strategy instance (`Simulation._strategy_b`,
built via the new `_build_strategies` from the same spec) used only for
pool B's own `decide()` call — `Agent.decide()` gained an optional
`strategy` override for exactly this — so each pool's trend-tracking stays
scoped to that pool, as if it had its own dedicated agent. Covered by
`test_stateful_strategies_track_each_pool_independently`.

**A second, more consequential bug was caught later, after E20's report had
already been written — not during implementation this time, but while
explaining the mechanism in detail, checking the actual numbers by hand
turned up a real miscalibration.** `SanctioningStrategy.sanction_policy()`
sets `quota_total = regeneration_rate * capacity / 4` from that strategy
instance's own params. Two compounding bugs meant this was always pool A's
number: (1) `_build_strategies()` originally built pool B's strategy copies
from the *same* `AgentSpec.params` as pool A, so a sanctioning agent's
pool-B copy never learned pool B's own (lower) growth rate; and (2)
`_enforce()` never even asked that pool-B copy for its policy — it always
read `agent.strategy.sanction_policy()` (the pool-A instance) regardless of
which pool it was enforcing. Net effect: every quota enforced on pool B was
double what pool B could actually sustain (`MSY_A` instead of `MSY_B`), so
a monitor that looked like it was protecting the fragile pool was silently
letting free-riders take twice its sustainable yield. This produced a
specific, plausible-looking, and **wrong** finding in E20's first draft —
"the near-optimal set shrinks at every diversity level" and "pool B
collapses at 5 free-riders regardless of arrangement" — both artifacts of
the too-loose quota, not real properties of the axis; see
[E20's own correctness-fix note](../experiments/E20-multiple-resources.md)
for the corrected numbers and what they actually say (mostly: this axis
looks much more like groups, E15 — real equifinality gains at several
diversity levels — once the quota is right). Both `_build_strategies()`
(now overrides `regeneration_rate`/`capacity` to the second pool's own
values wherever a strategy's params carry them) and `_enforce()` (now reads
`self._strategy_b[i]`'s policy when enforcing pool B) are fixed, pinned by
`test_sanctioning_quota_uses_each_pools_own_growth_rate`. The web demo's own
JS engine never had this specific bug — `enforcePool()` always took the
correct pool-specific MSY as an explicit argument — but the analogous
*blind*/private-information estimate (`decide()`'s fallback branches reusing
a single module-level `MSY` constant regardless of which pool the call was
for) was real there too and is fixed alongside it.

## Rationale

- **Reuses every existing strategy verbatim.** No `Strategy` subclass
  changed; `cooperative`'s "surplus above `K/2`" computation, `sanctioning`'s
  quota logic, `reputation_cooperator`'s partner-conditioning — all run
  exactly as designed, just once per pool. This is the same "additive,
  doesn't disturb what's already there" discipline as groups (ADR-0012) and
  reputation (ADR-0014).
- **A fixed, sweepable split — not a dynamically-adaptive one — is a
  deliberate scope decision, not laziness.** A fixed split per agent folds
  directly into this project's own established methodology: sweep a
  parameter, count how many settings clear the near-optimal bar (the same
  shape as `visibility` in E18, `degree` in E19). A dynamically-adaptive
  split ("shift effort toward whichever pool needs it") is a different,
  larger question — closer to adaptive/learning behaviour, which this
  project has already and explicitly deferred (see research-questions.md's
  postponed RL item) — logged as a follow-up, not a first-cut requirement.
- **Sanctioning extends per-pool, at real doubled cost, because that's
  where the actual new institutional-design question lives.** A monitor
  enforcing both pools pays `monitoring_cost` twice (`_enforce` is called
  once per pool; its existing cost side-effect fires each time) — this
  opens a genuine question no earlier axis could ask: does a population do
  better with *specialized* monitors (one agent watches pool A, another
  watches pool B) than with *generalist* monitors trying to cover both?
  Leaving this out to save engineering effort would have gutted the part
  of this axis that is actually new.
- **Reputation's fair-share reference sums both pools' sustainable yields**
  when combined, so a well-behaved agent splitting a fair share across two
  resources isn't scored as if only one pool existed (verified by
  `test_reputation_fair_share_sums_both_pools_when_combined`).

## Consequences

- **Collective choice (ADR-0011), disturbances (ADR-0008), and the
  broadcast signal all stay scoped to the *first* pool only** — a
  deliberate, documented scope limit, not an oversight. Extending all
  three to a second pool is untested and was judged secondary to the two
  pools' own harvest/enforcement mechanics for a first cut; if
  `collective_choice` is combined with `second_resource` in a future
  config, both pools would receive collective enforcement whenever the
  vote passes (same shared `_collective_enforcement_active` flag), which
  has not been specifically validated.
- **A real, non-obvious empirical result exists** (E20): see
  `docs/experiments/E20-multiple-resources.md` for the validated finding
  on whether splitting effort/protection across two resources changes the
  near-optimal set, and whether specialized or generalist monitoring wins.
- **Orthogonal to reputation/network** in the same sense those two are
  orthogonal to groups/boundaries: combining `second_resource` with
  `reputation`/`network` works mechanically (tested:
  `test_reputation_fair_share_sums_both_pools_when_combined`) but a fixed
  neighbour graph scoped *per pool* (rather than one shared graph across
  both) is untested.
- **`RoundRecord` gained five new fields** (`resource_start_b`,
  `resource_after_regen_b`, `resource_after_harvest_b`, `collapsed_b`,
  `requested_b`, `harvested_b`) for the second pool's own trajectory and
  per-agent pool-B breakdown. `requested`/`harvested` (unqualified) keep
  their existing meaning — an agent's *total* across every pool it draws
  from — so `RunResult.total_payoffs()`, `payoff_gini`, and
  `welfare_efficiency` all continue to work correctly and completely
  unchanged whether there are one or two pools.
- **`compute_metrics` (`metrics.py`) was deliberately left single-pool-only**
  (reports pool A's own `capacity`/`sustainability_ratio`/etc.) rather than
  widened for every caller — a change to the shared metrics contract used
  by every experiment. E20's own script computes pool-B-specific and
  combined figures directly from `RoundRecord`'s new fields instead.

## Status Notes

Built as **E20** (`scripts/experiment_multiple_resources.py`,
[docs/experiments/E20-multiple-resources.md](../experiments/E20-multiple-resources.md)).
Ported to the browser demo (`web/commons-demo.html`) with a second pool
visualized alongside the first, and a "+ Multiple resources" rung on the
complexity staircase alongside diversity/groups/boundary/reputation/network.
