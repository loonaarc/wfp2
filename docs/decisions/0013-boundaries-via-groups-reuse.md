# ADR-0013: Boundaries (open access vs. closed community) via groups reuse — no new mechanism

- **Status:** Accepted *(2026-08-07)*
- **Date:** 2026-08-07
- **Deciders:** project owner (approved scope), assistant (implementing)

## Context

The second axis in the groups+boundaries pair recommended in
[`docs/thesis-direction-equifinality.md`](../thesis-direction-equifinality.md).
Ostrom (1990)'s first design principle, **clearly defined boundaries**, says a
durable commons institution can exclude non-members from harvesting at all —
"individuals or households who have rights to withdraw resource units from the
CPR must be clearly defined, as must the boundaries of the CPR itself." The
contrast is with Gordon (1954)'s founding open-access framing: without a
boundary, *anyone* can enter and harvest, which is what drives rent
dissipation to zero in the classical bioeconomic model. ADR-0012's own
"Consequences" section surfaced exactly this gap empirically: a well-monitored
group is not insulated from an unmonitored neighbour draining the same shared
pool — the natural next question is whether excluding that neighbour entirely,
rather than merely failing to monitor it, changes the outcome.

## Considered Options

1. **A new `boundary`/`excluded` field and exclusion logic.** Add a config
   flag that removes some agents' ability to request/harvest entirely (a
   permanent, config-time analogue of the `agent_failure` disturbance).
   Rejected on inspection: it would duplicate machinery that already exists.
2. **Reuse `AgentSpec.group` (ADR-0012), no new code.** "Closed community" is
   a config with only the governed roster present; "open access" is the same
   config with an additional, ungoverned outsider group added — a batch of
   agents present in the round, drawing from the same shared pool via the
   existing feasibility-scaling allocation (`_allocate`), but never covered by
   any group's sanctioning quota because their own group has no sanctioner in
   it. This already reproduces the qualitative signature of open access (an
   unconstrained draw on the commons that the existing feasibility scaling
   still rations proportionally when the pool is low, but never caps to the
   sustainable yield) without inventing anything new. *(Chosen.)*

## Decision

**Boundaries experiments are a config/experimental-design pattern, not a new
engine mechanism.** To compare closed vs. open access under otherwise
identical conditions:

- **Closed:** the governed roster only, e.g. `AgentSpec("sanctioning", 8,
  ...)`, group defaulted to `0`.
- **Open:** the same governed roster, `group=0`, **plus** an additional
  `AgentSpec` for outsiders (typically `selfish`) in their own group (e.g.
  `group=1`) with no sanctioner assigned to that group **and `governed=False`**
  (see ADR-0012's correction below) — so ADR-0012's `_enforce` never computes
  a quota for them, they're excluded from the governed population's own
  quota *denominator* too, and `_allocate`'s feasibility scaling still
  applies to everyone sharing the pool.

No changes to `config.py`, `agent.py`, `simulation.py`, or `state.py` beyond
what ADR-0012 already added. `tests/test_groups.py::test_boundaries_as_
ungoverned_outsider_group_no_new_mechanism_needed` demonstrates the pattern
directly: the closed config stays above the sustainable-yield level; the same
governed core, with 4 outsiders added, ends up worse off — the shared-pool
caveat from ADR-0012 made concrete as a deliberate experimental comparison.

## Rationale

- No new *engine* mechanism means less new engine code to get wrong — but
  **this turned out not to mean zero new correctness surface**, and the
  original version of this bullet overclaimed that it did. Reuse still
  crossed a boundary ADR-0012's original formula was never checked against:
  dividing by "total population" implicitly assumed every agent counted in
  that total was part of the same fair-share accounting, which stopped being
  true the moment an *ungoverned* outsider batch could exist. See ADR-0012's
  "Correction" section — the fix is `governed=False` on the outsider spec,
  not a new mechanism, so the reuse strategy itself still holds, just not the
  claim that it was correctness-surface-free by construction.
- Keeps the engine's surface area small — every additional structural axis
  that turns out to be expressible this way is one fewer place for a bug like
  ADR-0012's near-miss (dividing by group size instead of total population)
  to recur.

## Consequences

- **Positive:** groups and boundaries can be jointly swept (the recommended
  first pair from the equifinality note) with a *single* underlying
  mechanism to reason about, reducing the chance that an observed interaction
  effect is actually two different engines interacting unpredictably rather
  than a genuine finding.
- **Negative / scope:** this is a *simplified* operationalization of
  boundaries. It captures "outsiders present, unmonitored" but not the
  stronger reading of principle 1 — literal, hard exclusion (an outsider who
  cannot harvest *at all*, not just harvests unmonitored). The current
  `_allocate` feasibility scaling still gives outsiders a proportional share
  whenever total requests exceed the stock; a "closed" config exhibits true
  exclusion (outsiders are never instantiated at all), but there is no way,
  within an "open" config, to express partial/permitted access short of full
  participation. A harder-exclusion variant (config-time analogue of
  `agent.active = False`) is a real follow-up if this simplification proves
  too coarse.
- **Naming caveat for the write-up:** because this reuses `AgentSpec.group`,
  "boundaries" does not appear anywhere in the codebase as a named concept —
  only in this ADR and the experiment design that uses the pattern. Future
  readers of `config.py` alone would not discover this axis exists; the
  cross-reference in ADR-0012's docstring and this ADR are the only pointers.

## Status Notes

Implemented 2026-08-07, alongside the ADR-0012 rebuild. Demonstrated by
`tests/test_groups.py::test_boundaries_as_ungoverned_outsider_group_no_new_
mechanism_needed`. Demo: `web/commons-demo.html`'s "Boundary" dial. No
`architecture.md`/`metrics.md` update yet.

**2026-08-09:** the experiment built on this mechanism was renumbered from
E15 to E16 — population-type diversity was identified as a more foundational
axis that belongs before groups/boundaries in the complexity sequencing (see
`docs/thesis-direction-equifinality.md`), pushing both down to make room for
it as the new E14. The mechanism and this ADR are unaffected; only the
experiment numbering shifted.
