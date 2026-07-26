# ADR-0006: Model strategy adaptation as replicator dynamics at the experiment level

- **Status:** Accepted *(2026-07-26)*
- **Date:** 2026-07-26
- **Deciders:** project owner (assistant implementing)

## Context
Experiment E3 left an open question (and the Hauert et al. 2007 note sharpens it):
sanctioning protects the commons but monitors pay a cost the others don't, so *if
monitoring is voluntary, does it survive?* Answering this needs agents whose choice
of strategy can **change over time** in response to payoff — adaptation the current
fixed-strategy agents do not have.

The project brief defers reinforcement learning ("begin with simple rule-based
agents; avoid RL unless strongly justified") but explicitly lists "adaptive
strategies" and "mixed populations of different strategies" as in-scope. Evolutionary
/ imitation dynamics are rule-based (no value functions, no gradient learning), so
they fit.

## Considered Options
1. **Mid-run strategy switching in the engine.** Agents imitate more successful peers
   during a run. Powerful but a significant core-engine change (mutable strategies,
   in-run selection), and it entangles the deterministic per-round engine with
   population dynamics.
2. **Individual adaptive monitor choice.** Each agent carries an adjustable
   probability of paying to monitor, updated by win-stay-lose-shift. Requires new
   per-round observation of others' payoffs and a stochastic per-round enforcement
   contribution.
3. **Replicator dynamics at the *experiment* level.** Keep the engine unchanged; over
   "generations", instantiate a population at the current strategy frequencies, run
   one simulation, measure each strategy's mean payoff, and update the frequencies by
   a replicator/imitation rule. *(Chosen.)*

## Decision
Adopt **Option 3**. Implement voluntary-monitoring dynamics as a loop *on top of* the
existing simulator (in `scripts/experiment_voluntary_monitoring.py`), with no change
to `core`. Each generation measures per-strategy fitness from a full simulation and
updates strategy shares by a discrete replicator step.

## Rationale
- **No core-engine change** — the deterministic, reproducible per-round engine stays
  exactly as validated; the new dynamics live in the experiment layer and reuse the
  library's public API (`run_simulation`, `total_payoffs`).
- **Standard and legible** — replicator dynamics is the canonical way to study whether
  a costly strategy (monitoring) is evolutionarily stable, and directly parallels
  Hauert et al.
- **Reproducible** — the update is deterministic given the measured payoffs; the whole
  trajectory is a pure function of the initial composition and parameters.
- Keeps RL genuinely deferred.

## Consequences
- **Positive:** answers the voluntary-monitoring question with minimal new machinery;
  composes with everything (noise, mechanisms, metrics).
- **Simplifications:** fitness is measured from one simulation per generation at
  discretised integer counts (finite-population rounding); no explicit mutation, so
  extinct strategies do not re-enter (a strategy that hits zero share is gone). Both
  are documented in the E5 report.
- **Follow-ups:** add mutation (re-invasion), the "loner"/optional-participation
  rescue (Hauert et al.), or promote to in-engine imitation if a within-run treatment
  is needed later.

## Status Notes
Implemented 2026-07-26 as Experiment E5 (voluntary monitoring). Engine untouched.
