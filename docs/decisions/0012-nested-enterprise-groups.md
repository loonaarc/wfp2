# ADR-0012: Group-scoped ("nested enterprise") enforcement

- **Status:** Accepted *(2026-08-07)*
- **Date:** 2026-08-07
- **Deciders:** project owner (approved scope), assistant (implementing)

## Context

This is the first structural axis for the equifinality thesis direction (see
[`docs/thesis-direction-equifinality.md`](../thesis-direction-equifinality.md)):
a genuinely new mechanism, not a new value for an existing config field. Ostrom
(1990)'s eighth design principle, **nested enterprises**, says durable commons
institutions organize "appropriation, provision, monitoring, enforcement,
conflict resolution, and governance activities... in multiple layers of nested
enterprises" — small groups govern themselves, rather than one central
authority governing everyone. This project's own existing paper note on Ostrom
(1990) already flagged this as an unrepresented gap, and separately criticised
the current enforcement mechanism as "closer to the Leviathan Ostrom argues
against": today, if **any** agent anywhere is configured with the `sanctioning`
strategy, the engine's `_enforce` computes **one** population-wide quota and
applies it to **every** agent, regardless of where they are. A single monitor
that has never seen agent 47 nevertheless fully protects agent 47. Nested
enterprises predicts this shouldn't work in general — a subgroup a monitor
cannot observe shouldn't be protected by that monitor.

A second, independent citation strengthens this axis further, found on a later
pass through already-read literature: Nowak (2006), "Five Rules for the
Evolution of Cooperation" ([note](../paper-notes/2006-nowak-five-rules.md)),
gives an *exact* formula for group-structured cooperation — cooperation is
favoured under weak selection when `b/c > 1 + n/m` (`n` = maximum group size,
`m` = number of groups). This means groups doesn't have to stay a binary
"sanctioner present in this group or not" test — sweeping `n` and `m` against
this precise, independently-derived prediction turns it into a properly
parameterized experiment, not a narrow on/off mechanism check.

## Considered Options

1. **Multiple separate resource pools, one per group.** Rejected: this is a
   different candidate axis ("multiple resources"), already named separately
   in the brainstorming note. Conflating the two would make it unclear which
   effect (nested governance vs. resource separation) produces any observed
   result.
2. **Group-scoped monitoring, one shared pool.** Partition agents into groups
   (`AgentSpec.group`); a `sanctioning` agent's quota is computed from, and
   applied only to, its own group's members. The pool stays single and shared,
   so a group's individual protection can still be undermined by another,
   unprotected group drawing from the same pool — which is itself an
   interesting, literature-relevant finding (real nested enterprises usually
   pair local monitoring with local *boundaries*, principle 1, not
   monitoring alone; see ADR-0013). *(Chosen.)*

## Decision

Add `group: int = 0` to `AgentSpec` (validated non-negative), threaded through
to `Agent`. Rewrite `Simulation._enforce` to partition agents by `group` before
computing individual-sanctioner quotas:

- For each group, if it has at least one active sanctioning member, compute
  `quota_per_capita = min(quota_total among that group's own sanctioners) /
  N_total` — **`N_total` is the whole population, not the group's own size**,
  so a group's fair share stays anchored to the shared pool's true sustainable
  yield; two independently-monitored groups therefore don't each claim a full
  per-capita share and jointly over-draw the pool.
- That quota caps only that group's own members' harvests; a group with no
  sanctioner of its own is left uncapped by individual enforcement, even if
  another group has one.
- **Collective-choice enforcement (ADR-0011) is untouched and stays
  population-wide** regardless of grouping — it is a different Ostrom
  principle (3, collective choice) from this one (8, nested enterprises), and
  conflating them was avoided.
- `group` defaults to `0` on every `AgentSpec`, so with no group configured
  every agent lands in one group and `_enforce` reduces to exactly the
  original formula (verified in `tests/test_groups.py`, including an exact
  reproduction of `test_sanctioning.py`'s `105.0` net-payoff figure).
- `RunResult` gained a parallel `agent_groups: tuple[int, ...]` field (empty
  by default) so experiment scripts can break results out by group, and so
  `n`/`m` can be recovered from a config for the Nowak-formula analysis above.

## Rationale

- Additive and backward-compatible by construction (a new field with a
  no-op default), matching every prior engine-changing ADR (0007–0011) in
  this project.
- Keeps the pool single and shared rather than also splitting it, which
  isolates the effect under test to *who enforces*, not *what resource is
  shared* — that's the other candidate axis, deliberately deferred.
- Reuses the existing `SanctionPolicy`/quota machinery rather than inventing
  a second enforcement code path, same discipline as ADR-0011.
- Using total population `N`, not group size, in the per-capita denominator
  is the one non-obvious design choice: it's what keeps a covered group's
  quota meaning "this group's fair share of the *whole* pool's sustainable
  yield," rather than silently doubling the claimed sustainable total once
  more than one group monitors itself.
- No changes were needed to support sweeping `n` and `m` for the Nowak
  formula: both are already fully expressible by how an experiment script
  populates `AgentSpec.group` values — a config/experiment-design concern,
  not an engine one.

## Consequences

- **Positive:** for the first time this project can compare *flat,
  population-wide* enforcement (every prior E3/E5/E7/E13 result) against
  *nested, group-scoped* enforcement under otherwise identical conditions —
  directly testable, e.g. `tests/test_groups.py`'s
  `test_sanctioner_does_not_protect_a_different_group`, where the exact same
  4-sanctioner + 4-selfish composition that stays healthy when flat
  (`final_resource_level > 10.0`, matching `test_sanctioning.py`) drops
  below the sustainable-yield level once the selfish agents are moved to a
  separate, unmonitored group.
- **Negative / scope:** groups are a static partition fixed at config time —
  agents cannot switch groups, groups cannot merge or split, and there is no
  notion of group-level collective choice (principle 3) nested *within* a
  group; only principle 8 (nested monitoring) is modelled, not the fuller
  "multiple layers" picture.
- **Shared-pool caveat, discovered rather than designed in:** because the
  pool stays single, a well-monitored group is not fully insulated from a
  neighbouring group's over-harvest — the shared resource can still be
  driven down by the unprotected group even though the protected group's own
  members stay within quota. This matches Ostrom's real cases, where nested
  monitoring is normally paired with clearly defined boundaries (principle
  1) rather than deployed alone — directly addressed by ADR-0013, which
  reuses this same mechanism for a boundaries experiment rather than
  building a second one.
- **Follow-ups:** the E14 experiment sweeping `n`/`m` (via group composition)
  against Nowak's `b/c > 1+n/m` prediction, jointly with the boundaries axis
  (ADR-0013), against the near-optimal-set-size question from the
  equifinality note.

## Status Notes

Implemented 2026-08-07 (rebuilt after an earlier revert of the first pass at
this same design): `config.py`, `agent.py`, `simulation.py`, `state.py`
changed; `tests/test_groups.py` added (8 tests, including a boundaries-reuse
demonstration for ADR-0013). Full existing suite (102 tests total) re-run and
green, `group=0` on every prior config confirmed to reproduce prior results
exactly. No experiment script, demo update, or docs (`architecture.md`,
`metrics.md`) update yet — this ADR covers the engine mechanism only.
