# ADR-0009: Add a loner (opt-out) strategy and scale monitoring cost by the defector share

- **Status:** Accepted *(2026-08-06)*
- **Date:** 2026-08-06
- **Deciders:** project owner (assistant implementing)

## Context

E5 found that voluntary monitoring is **not evolutionarily stable**: sanctioners pay
a flat `monitoring_cost` every round, free-riding cooperators out-earn them without
paying it, monitors erode to zero, and the commons then collapses (see
[E5](../experiments/E5-voluntary-monitoring.md) and
[ADR-0006](0006-evolutionary-dynamics-at-experiment-level.md)). E5's own "Follow-ups"
section named the direct fix: Hauert, Traulsen, Brandt, Nowak & Sigmund (2007) show
that adding an **optional-participation ("loner")** strategy can rescue costly
punishment from exactly this second-order free-rider problem (see the paper note at
[`docs/paper-notes/2007-hauert-via-freedom-to-coercion.md`](../paper-notes/2007-hauert-via-freedom-to-coercion.md)).

Two things had to be added together for the mechanism to have any chance of working,
not just the loner on its own:

1. A **loner strategy** — opts out of the shared resource for a fixed, guaranteed
   payoff `σ` (sigma), independent of what's happening to the pool.
2. **Monitoring cost that scales with how many defectors are actually present.** In
   Hauert's model, a punisher's cost is proportional to the number of defectors it
   fines. E5's flat `monitoring_cost = 0.2` has no such dependence, so a loner
   shrinking the population does nothing on its own to make monitoring cheaper.

## Considered Options

1. **Loner only, keep monitoring cost flat.** Simplest, but does not touch the actual
   mechanism (cheap monitoring when defectors are rare) that Hauert identifies as the
   cause of the rescue — expected to do nothing.
2. **Loner + defector-scaled monitoring cost, computed inside the core engine.** Would
   require the `SanctionPolicy`/enforcement step to know the current population
   composition and adjust cost per round — a core-engine change, which ADR-0006
   deliberately avoided for this whole line of work.
3. **Loner + defector-scaled monitoring cost, computed at the experiment/script
   level.** Before each generation's simulation is run, compute
   `monitoring_cost = BASE_MONITORING_COST * (selfish_count / n_active)` from the
   *current* replicator shares, and pass that as the `SanctioningStrategy`'s
   `monitoring_cost` parameter for that generation only. The loner itself never
   enters the simulation — it earns a fixed payoff `σ` applied directly in the
   replicator bookkeeping. *(Chosen.)*

## Decision

Adopt **Option 3**, exactly mirroring ADR-0006's own precedent (replicator dynamics
live in the experiment layer; the core engine is untouched). Implemented as:

- `LonerStrategy` (`src/emergent_cooperation/strategies/loner.py`) — requests `0.0`
  every round; registered in the strategy registry so it can be referenced by name
  like any other strategy, but it is deliberately *excluded* from the actual
  `run_simulation` call in the new experiment script (a loner touches nothing, so
  running it through the engine would be pure overhead).
- A new script, `scripts/experiment_voluntary_monitoring_loner.py` (Experiment E11),
  which reuses E5's replicator-dynamics loop but with four strategies
  (`sanctioning`, `cooperative`, `selfish`, `loner`) instead of three, and computes
  `monitoring_cost` freshly each generation from the current selfish share among the
  *active* (non-loner) population.

**Calibrating `σ` (the loner's fixed payoff).** Hauert's enabling inequality is
`0 < σ < (r−1)c`: opting out must beat a fully-collapsed commons but lose to a
thriving one. A diagnostic run at E5's exact population scale (`N=40`, 60 rounds,
`K=100`, `g=0.4`) gave reference payoffs: an all-cooperative healthy commons nets
**≈15.0** per agent; an all-selfish collapsed commons nets **≈1.5**. `σ = 6.0` was
chosen as a value clearly inside `(1.5, 15.0)` — a real refuge from collapse, not a
strategy that can out-earn a healthy commons.

## Rationale

- Keeps the "no core-engine change" discipline established in ADR-0006 — the new
  mechanism lives entirely in the experiment script.
- `σ` is grounded in numbers actually measured from this project's own simulation,
  not copied from Hauert's abstract payoff units, which don't correspond to anything
  in our engine.
- Excluding the loner from `run_simulation` avoids inventing fake harvest/payoff
  bookkeeping inside the engine for an agent that, by construction, never touches the
  resource.

## Consequences

- **Positive:** directly tests the Hauert mechanism against E5's negative result with
  a minimal, explainable change; reuses all of E5's existing tooling and conventions.
- **Result (see [E11](../experiments/E11-loner-rescue.md) for the full write-up):**
  the mechanism **delays** monitoring's collapse substantially (erosion completes
  around generation ~60–65, vs. ~13–14 in E5 — roughly a 4–5× delay) but does
  **not prevent** it in this engine. The reason is structural, not a tuning failure:
  Hauert's actual rescue relies on a **finite-population, rare-mutation** regime
  where punishers can reach full fixation and then resist invasion permanently; our
  replicator dynamics are continuous and deterministic with no fixation step, so
  sanctioning's cost is always strictly positive (however small) while cooperation's
  is always exactly zero, and in the long run a strictly-positive cost always loses.
  This sharpens, rather than closes, the open question already flagged in the Hauert
  paper note: the *finite-population stochastic* setting, not just an opt-out option,
  is likely the load-bearing ingredient.
- **Follow-ups:** Sigmund, De Silva, Traulsen & Hauert (2010) offer a *different*
  fix for the same underlying second-order problem — **pool-punishment with
  second-order sanctioning** (see
  [`docs/paper-notes/2010-sigmund-social-learning-institutions.md`](../paper-notes/2010-sigmund-social-learning-institutions.md)) —
  which does not depend on reaching fixation the way Hauert's loner mechanism does,
  and is a more promising next attempt at actually stabilising E5's monitoring
  result. A finite-population/stochastic (Moran-process) version of the replicator
  loop is a second, more involved follow-up that would let Hauert's mechanism be
  tested as originally specified.

## Status Notes

Implemented 2026-08-06 as Experiment E11 (loner rescue attempt). Engine untouched;
`LonerStrategy` added to the registry for reuse in future experiments.
