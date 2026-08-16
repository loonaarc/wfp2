# ADR-0019: Wealth-based participation floor, and why it backfires here

- **Status:** Accepted
- **Date:** 2026-08-16
- **Deciders:** project owner (approved scope), assistant (implementing)

## Context

Item 12 in `thesis-direction-equifinality.md`'s ranking ("inequality-adaptive
monitoring investment") was originally scoped as making the E5/E11/E12
evolutionary-dynamics fitness function sensitive to `payoff_gini`. That item
was explicitly flagged as *not yet grounded in anything read* — a real
literature search was needed before any design work, not a search for a
citation to retrofit onto an idea already decided.

**Two open-access candidates were read in full before any code was
written.** Johnson & Smirnov (2018, wealth-homophily partner selection) has
no punishment/monitoring/enforcement element at all — not a fit. Chen &
Szolnoki (2016, `docs/paper-notes/2016-chen-szolnoki-wealth-based-selection.md`)
is a genuine, different, buildable mechanism: gating participation in a
public-goods round on accumulated wealth (past payoff), which in their
spatial-lattice model self-corrects — sustained defection erodes a
defector's *own* future income (it exhausts the local cooperators it
free-rides on), so the gate disproportionately excludes defectors, not
cooperators. Neither candidate is the originally-scoped "Gini-sensitive
evolutionary fitness" idea. This ADR documents the resulting scope pivot
honestly, the same way ADR-0018 pivoted after reading Fudenberg & Maskin's
own follow-up section.

**A second correction, caught empirically, not from reading:** the original
plan (recorded in the paper-note's own "Questions" section) was to test the
wealth gate combined with this project's existing network structure
(`NetworkConfig`, E19/ADR-0015), reasoning that Chen & Szolnoki's own
mechanism depends on spatial/local structure. Checking the engine directly
before building around this: `network` only restricts *reputation's partner
selection* (ADR-0015) — the resource pool itself is always one single,
globally shared stock, regardless of `network`. Combining `wealth_floor_
fraction` with `network` would not actually test what Chen & Szolnoki's
result depends on, since it doesn't touch how the pool is shared at all.
Dropped before building; replaced with a sharper, more direct test (below).

## Considered Options

1. **Combine the wealth gate with `network` (E19)**, as originally sketched
   in the paper-note. *(Rejected once checked against the engine: `network`
   doesn't touch resource-sharing structure at all, only reputation pairing
   — this would not test the paper's own local-exhaustion mechanism.)*
2. **Test the wealth gate alone against a growing free-rider count, and
   separately against a growing free-rider count with `sanctioning`
   present** — both directly answerable with the existing engine, no new
   axis needed beyond the gate itself. *(Chosen.)*

## Decision

Option 2. A new `SimulationConfig.wealth_floor_fraction: float | None`
(`None` by default, existing experiments unchanged): when set, an agent
whose own `total_payoff` falls below `wealth_floor_fraction` times the
population's *own current average* `total_payoff` is excluded from
requesting (not enforcing) that round — recomputed fresh every round, so an
agent can drop out and rejoin as its relative wealth moves. Relative to the
population's own average, not a fixed absolute number, so it scales with
however much wealth has actually accumulated and never excludes anyone at
round 0 (everyone starts at exactly the average: zero).

Two questions, run directly against the built engine before writing the
experiment script, to check what the mechanism actually does here rather
than assume it transfers:

- **Q1 (wealth gate alone):** cooperative + selfish agents, no monitor. A
  quick check first: **the gate excludes the cooperative majority, not the
  free-rider.** In a well-mixed shared pool, a selfish agent's request
  scales with the *current, global* level, not a local neighbourhood it
  personally exhausts — so free-riders consistently out-earn cooperators
  (the standard tragedy-of-the-commons pattern this project has shown since
  E2), and a wealth floor built on "below average" therefore targets the
  exploited, not the exploiter.
- **Q2 (wealth gate + sanctioning):** adding a monitor changes *who* ends up
  poorest. Checked directly: with `sanctioning` present, the quota already
  equalizes harvest across all non-monitor agents — the wealth gap that
  remains is between monitors (who pay `monitoring_cost` and can end up with
  *negative* net payoff) and everyone else. The gate then excludes the
  monitors themselves, removing enforcement precisely because enforcing it
  was costly.

## Rationale

- **Both questions were checked directly against the running engine before
  the experiment script was written**, exactly like the stateful-strategy
  and quota-miscalibration bugs caught in ADR-0016 and the R₀ threshold
  found in ADR-0017 — this is the same "verify before reporting" discipline
  applied one step earlier, at the design stage rather than after results
  were already written up.
- **The mechanism doesn't transfer, and the reason is precise and citable,
  not a shrug.** Chen & Szolnoki's self-correction depends on defection
  eroding a defector's *own* local resource base — a channel that requires
  spatial/local structure their model has and this project's single shared
  pool does not. Recording *why* it doesn't transfer is exactly the kind of
  negative, mechanistically-explained result this project already treats as
  a genuine finding (ADR-0015's `b/c > k` non-transfer is the direct
  precedent), not a failed experiment to discard.
- **Reuses `Observation`/`Agent.total_payoff`, already tracked and
  previously unused by any strategy** — no new per-agent state, only a
  per-round eligibility check in `Simulation.step()`, mirroring
  `agent.active`'s existing pattern without conflating the two (a wealth
  exclusion is re-evaluated every round; `active` is permanent).

## Consequences

- **The wealth gate is a genuinely harmful default in this project's
  well-mixed setting, not a neutral or beneficial one** — this needs to be
  stated plainly wherever the mechanism is discussed, since "wealth-gate
  participation" sounds protective by name.
- **Enforcement (`sanctioning`) reach follows a monitor's own eligibility**:
  a wealth-gated-out monitor stops requesting but keeps enforcing this
  round (enforcement is not gated) — a deliberate scope decision, not an
  oversight, to avoid re-touching `_enforce()`'s `agent.active`-based
  filtering for a temporary, per-round condition.
- **Not folded into the complexity-panel composition sweep** — the same
  scope call as E21/E23's sibling axes: this tests a mechanism question
  (does wealth-gating help or hurt), not a composition-space question.

## Status Notes

Built as **E23** (`scripts/experiment_wealth_participation.py`,
[docs/experiments/E23-wealth-based-participation.md](../experiments/E23-wealth-based-participation.md)).
