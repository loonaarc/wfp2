# ADR-0005: An enforcement phase in the engine for sanctioning

- **Status:** Accepted  *(2026-07-26 — approved by project owner)*
- **Date:** 2026-07-26
- **Deciders:** project owner (assistant implementing)

## Context
Experiment E2 showed that reciprocity (the conditional cooperator) protects
*fairness* but not the *commons*. Ostrom's design principles point to **monitoring
and graduated sanctions** as the mechanism that sustains commons. We want a
`sanctioning` strategy to test whether it can protect the resource *and* fairness
where reciprocity cannot.

The obstacle: our `selfish` agent is a *fixed automaton* — it ignores punishment, so
docking its payoff would not change its extraction and the resource would still
collapse. For sanctioning to protect the *resource* against non-adaptive defectors,
it must reduce their realised *extraction*, not just their payoff. That requires the
engine to act on harvests after agents decide — a new **enforcement phase**.

## Considered Options
1. **Enforcement (cap over-extraction).** After agents decide, if any sanctioner is
   present, cap every agent's harvest at a per-capita quota; the confiscated excess
   stays in the pool. Sanctioners pay a monitoring cost. *(Chosen.)*
2. **Costly payoff punishment.** Sanctioners pay to dock defectors' payoffs. Faithful
   to the literature but ineffective against fixed selfish agents (redistributes,
   doesn't protect the resource).
3. **Punishment + adaptive defectors.** Add payoff punishment and make selfish agents
   reduce greed when punished. Most realistic but the largest change (introduces
   agent adaptivity, which the project otherwise defers).

## Decision
Adopt **Option 1**. Add an enforcement phase to `Simulation.step`, driven by an agent
*capability* rather than a hard-coded strategy check:

- `Strategy` gains `sanction_policy() -> SanctionPolicy | None` (default `None`).
- `SanctionPolicy(quota_total, monitoring_cost)` describes the enforced rule.
- In `step`, after harvest allocation: if any agent exposes a policy, cap each agent's
  harvest at `min(quota_total) / n`; the excess is *not* withdrawn (it stays in the
  pool); each sanctioner's payoff is reduced by its `monitoring_cost`.

## Rationale
- **Protects the resource against fixed defectors** — enforcement reduces their
  extraction directly, so no agent adaptivity is needed (keeps RL/learning deferred).
- **Minimal, decoupled engine change** — the engine queries a capability
  (`sanction_policy()`), so it does not depend on any concrete strategy class; the
  default `None` means non-sanctioners and all existing runs are unaffected.
- **Directly answers E2's open question** ("can a mechanism protect both resource and
  fairness?") and surfaces the classic **second-order free-rider** trade-off
  (monitoring is costly, so monitors earn less than cooperators who don't monitor).

## Consequences
- **Positive:** backward-compatible (no policy ⇒ old behaviour, verified by existing
  tests); a clean capability hook reusable by future institutional mechanisms; enables
  E3.
- **Negative / simplifications:** "any one sanctioner enforces fully" is a strong
  simplification (monitoring as a step public good); the quota and monitoring cost are
  free parameters whose values shape results; enforcement is frictionless (no evasion,
  no false positives). All to be documented in the E3 report and `docs/architecture.md`.
- **Follow-ups:** graduated (proportional) enforcement; enforcement strength scaling
  with the number of sanctioners; evasion/imperfect monitoring; the second-order
  free-rider experiment (mix sanctioners with plain cooperators).

## Status Notes
Accepted and implemented 2026-07-26 as the `sanctioning` strategy + engine
enforcement phase, backing Experiment E3.
