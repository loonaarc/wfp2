# ADR-0021: Agent turnover as a new disturbance kind, resetting strategy state only

- **Status:** Accepted
- **Date:** 2026-08-17
- **Deciders:** project owner (approved scope), assistant (implementing)

## Context

Item 10 in `thesis-direction-equifinality.md`'s ranking ("agent entry/exit,
turnover") was flagged from the start of this session's 5-axis undertaking
as the weakest-grounded candidate — initial searches during planning found
no clean, direct match, and the plan explicitly named it the one item that
might end up deferred rather than built. A second, targeted literature
search (this axis's own required first step, per the approved plan) found
Duffy & Lafky (2015), *"Birth, death and public good provision"*
(`docs/paper-notes/2015-duffy-lafky-birth-death-public-good.md`) — a lab
experiment showing that replacing a fixed cohort with staggered
overlapping-generations turnover (new subjects entering as old ones exit)
significantly flattens the well-documented decay of public-goods
contributions over time, for both fresh entrants and existing members. This
is a genuine, on-point citation, not a stretch.

**What this project's engine actually has that could "decay":** this
project's strategies are fixed, deterministic rules, not learning agents —
there is no experience-driven contribution decay to arrest. But one
strategy has a structurally exact analogue: `grim_trigger` (E21, ADR-0018),
whose `_triggered` flag latches permanently once tripped — E21's own
headline finding is that a permanent trigger has "no return path."
`conditional_cooperator`/`compensating_cooperator` recompute their own
decline-check fresh every round (no sticky flag, confirmed by reading
`conditional.py`/`compensating.py` directly), so they never get "stuck" in
the first place — leaving `grim_trigger` as the one strategy with a genuine,
literature-relevant "can turnover recover it" question.

## Considered Options

1. **A literal overlapping-generations port** (staggered individual
   lifetimes, age-tracking per agent, new agents drawn with different
   dispositions). *Rejected: this project's agents don't have individual
   "dispositions" that vary by experience — every agent of a given strategy
   behaves identically to every other. Porting age-tracking machinery with
   nothing for it to differentiate would be complexity with no payoff.*
2. **A new, standalone population-management subsystem** (agents literally
   removed and new `Agent` objects inserted, with their own fresh
   `total_payoff`). *Rejected as more machinery than the actual question
   needs: this project's per-slot `total_payoff` accounting (already used by
   E20/E22/E23) tracks a position across the run, not a specific
   individual's lifetime earnings — introducing per-individual sub-accounts
   would complicate every existing metric (Gini, welfare_efficiency) that
   currently assumes one payoff stream per slot, for a distinction the
   research question doesn't need.*
3. **A new disturbance kind, `agent_turnover`, that resets a fraction of
   agents' own strategy *state* (not identity, not accumulated payoff) at
   scheduled rounds — reusing `DisturbanceConfig`'s existing schedule/
   magnitude fields exactly like `agent_failure` already does.** *Chosen.*

## Decision

Option 3. Two small additions, both reusing existing machinery:

- `Strategy.reset_state(self) -> None` (base class default: no-op).
  Overridden by `ConditionalCooperatorStrategy`, `CompensatingCooperatorStrategy`
  (reset `_last_level = None`), and `GrimTriggerStrategy` (reset
  `_last_level = None` **and** `_triggered = False`) — the three strategies
  with per-round decline-tracking state. Every other strategy's inherited
  no-op means turnover is a genuine, verified no-op wherever there is
  nothing to reset (confirmed directly, see Rationale).
- A new `DISTURBANCE_KINDS` entry, `"agent_turnover"`. At its scheduled
  round, the fraction (`magnitude`, same `(0, 1]` semantics as
  `agent_failure`) of *active* agents starting at a deterministic rotation
  offset (`round_index % num_agents`, so successive turnover events at
  different rounds naturally touch different agents without needing shared
  mutable state across disturbance instances) each get `strategy.reset_state()`
  called, plus `agent.reputation = 0` (the one piece of turnover-relevant
  state that lives on `Agent`, not `Strategy`, per ADR-0014). `total_payoff`
  is deliberately **not** reset — it is a per-slot running total, the same
  convention `agent_failure` and `wealth_floor_fraction` already use, not a
  per-individual lifetime earnings record (see Option 2's rejection).
  Multiple `DisturbanceConfig(kind="agent_turnover", round=r, ...)` entries
  in the existing tuple give periodic turnover with zero new config surface.

**Verified directly before the experiment script was written:** turnover is
confirmed to be a byte-for-byte no-op against an all-`cooperative` or
all-`selfish` population (neither strategy has any state to reset), and
non-trivial only where `conditional_cooperator`, `compensating_cooperator`,
or `grim_trigger` are present — exactly as the state-based design predicts,
not assumed.

## Rationale

- **Directly operationalizes Duffy & Lafky's own finding** — a fresh
  "individual" (reset state) replacing an experienced one, without porting
  their staggered-age or belief-formation machinery this project's fixed
  strategies have no use for.
- **Reuses the disturbance architecture (ADR-0008) exactly as designed**: a
  tuple of scheduled events, no core round-loop changes beyond the new
  `Disturbance` implementation, following `AgentFailure`'s own established
  pattern in `disturbances/shocks.py` line for line.
- **Deterministic rotation from `round_index % n`, not a shared cursor**,
  keeps every disturbance instance stateless and independently
  constructible (matching every other `Disturbance` implementation), at the
  cost of not guaranteeing perfectly even coverage across a short run — an
  explicitly accepted simplification, not a hidden one.
- **Connects directly to a real, previously-open question this project's
  own prior work raised**: E21's report and ADR-0018 both note that a
  permanent `grim_trigger` lock has "no return path" within the engine as
  it existed then — E24 is the first test of whether an *external*
  intervention (turnover), rather than the forgiveness E21 deliberately
  excluded by construction, can recover one.

## Consequences

- **A genuine no-op for the majority of this project's existing
  regimes/experiments** — turnover only matters wherever `conditional_
  cooperator`, `compensating_cooperator`, `grim_trigger`, or
  `reputation_cooperator` (via the reputation reset) are present. This is
  expected and stated plainly, not a limitation to apologize for: it is the
  direct, correct consequence of "this project's agents don't decay from
  experience," not a sign the mechanism was built wrong.
- **Not folded into the complexity-panel composition sweep** — the same
  scope call as E17/E21/E22/E23: this tests a mechanism question (can
  turnover recover a locked population), not a composition-space question.
- **Item 10 is resolved, and the disclosed risk did not materialize** — the
  original plan's own caveat ("may end up deferred") does not apply; a
  second, targeted search (as promised) found a genuine, on-point citation.

## Status Notes

Built as **E24** (`scripts/experiment_agent_turnover.py`,
[docs/experiments/E24-agent-turnover.md](../experiments/E24-agent-turnover.md)).
