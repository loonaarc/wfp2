# ADR-0014: Reputation (indirect reciprocity) as a partner-targeted, not population-wide, mechanism

- **Status:** Accepted
- **Date:** 2026-08-14
- **Deciders:** project owner (approved scope), assistant (implementing)

## Context

Nowak & Sigmund (1998), "Evolution of Indirect Reciprocity by Image Scoring":
cooperation can be sustained via a public reputation score, without repeated
interaction between the same two individuals — you help someone not because
of what they did *to you*, but because of what others have observed them
doing to *anyone*. Their model is a pairwise donor-recipient game, which this
project's shared-pool commons is not: nobody has a "recipient" to individually
help or refuse each round.

Two design questions had to be resolved before this was buildable at all:
whose behaviour should the *response* be conditioned on, and what should the
response actually *do*.

## Considered Options

1. **Reputation feeds enforcement, not a strategy.** Any agent whose
   accumulated reputation drops below a threshold gets capped at the
   per-capita quota, the same mechanical cap `sanctioning` already applies —
   but with no dedicated monitor and no `monitoring_cost`, since the
   information is a byproduct of everyone observing everyone's harvest, not a
   paid role. Rejected for the pairwise-literature-fidelity goal, though it
   remains a legitimate, undiscarded alternative for a future axis (see
   Status Notes) — it directly answers E3/E5's second-order free-rider cost
   problem, which this option does not.
2. **Reputation feeds a strategy's own request, keyed to the population
   aggregate.** A rejected first draft: "detect how many free-riders exist,
   then also take a selfish share." This is `conditional_cooperator` again —
   E2 already found blanket retaliation collapses the resource with even one
   free-rider, and better detection of the same trigger only makes that
   collapse more reliable, not less. Discarded once traced through concretely.
3. **Reputation feeds a strategy's own request, keyed to one randomly
   assigned partner each round.** *(Chosen.)* Each agent is paired with one
   random *other* agent every round and, with probability `visibility` (`q`),
   observes that specific partner's current score. Cooperate unless the
   partner is known and below `trust_threshold`; an unobserved partner
   defaults to trusted. Only whoever happens to be paired with a bad-reputation
   agent on a given round defects — not the whole population synchronising at
   once, the way aggregate-triggered retaliation does.

## Decision

Option 3: a new `ReputationCooperatorStrategy` (`strategies/reputation.py`),
config-gated by `SimulationConfig.reputation: ReputationConfig | None`
(`visibility` in `[0,1]`, structurally the same kind of parameter as
`broadcast_reliability`). Every agent's own reputation score is tracked and
updated by the engine every round (`Simulation._update_reputation`) —
`+1` for a round at/below the governed community's fair share, `-1` above it
— regardless of that agent's own strategy, so it is real bookkeeping, not a
fiction specific to the one strategy that reads it. Partner selection and the
`visibility` observation roll happen in `Simulation._observe`, populating a
new `Observation.partner_reputation` field that every other strategy simply
ignores, the same way an unread broadcast `signal` already works.

## Rationale

Fidelity to the actual theoretical claim (reputation substitutes for
repeated personal interaction, not "know your enemies better and punish them
harder") mattered more than fidelity to the literal donor-recipient
book-keeping structure, which does not exist in a shared-pool commons at all
and would have required inventing a parallel transfer mechanic disconnected
from harvesting. Conditioning on one random partner instead of the
population aggregate is what keeps this a genuinely different mechanism from
`conditional_cooperator` rather than the same trigger with better detection —
confirmed empirically, not just argued: see Consequences.

## Consequences

- **A real, non-obvious empirical result, not a rediscovery.** At 1
  free-rider in an 8-agent population: `conditional_cooperator` already
  collapses (sustainability 0.0, `welfare_efficiency` 0.07 — E2's own
  finding); `compensating_cooperator` survives well (0.47, 0.99);
  `reputation_cooperator` survives but worse than passive restraint (0.11,
  0.65) — a genuine third point on that spectrum, not identical to either
  known extreme. `tests/test_reputation.py::
  test_reputation_reciprocity_is_not_disguised_conditional_cooperator`
  encodes the load-bearing half of this (does not collapse where
  `conditional_cooperator` does).
- **Reputation scoring is intentionally orthogonal to groups/boundaries
  (ADR-0012/0013).** Partner selection is population-wide, not scoped to
  `AgentSpec.group`, and the fair-share reference always uses
  `_n_governed`. Combining reputation with groups/boundaries is possible
  (nothing prevents it) but untested — a real follow-up, not assumed to
  compose cleanly.
- **Reputation is scored from the raw *request* (intent), not the realised
  post-rationing/enforcement harvest** — an agent that gets scaled down by
  scarcity, or capped by an unrelated sanctioner, is scored on what it
  *asked for*, which is the only thing under its own control.
- **Option 1 (reputation-as-enforcement) is not implemented, but not
  disproven either** — it is a real candidate for directly testing whether
  reputation can replace `sanctioning`'s cost (E3/E5's second-order
  free-rider problem) without a paid monitor, which this strategy-level
  version does not attempt to answer.

## Status Notes

Given its own experiment number, **E18** (`scripts/experiment_reputation.py`,
[docs/experiments/E18-reputation.md](../experiments/E18-reputation.md)) — a
standalone 3-way strategy comparison (`reputation_cooperator` vs.
`conditional_cooperator` vs. `compensating_cooperator`) plus a `visibility`
sweep, not a composition sweep.

Still **not folded into the complexity-axis sweep** (E14–E16's
composition-sweep machinery) — that remains deliberate, per the discussion
that led here: whether reputation belongs in the complexity/equifinality
story *at all* was an open question, not a foregone conclusion, and forcing
it into the composition-sweep machinery before it earned its place would
have repeated the mistake groups/boundaries' own renumbering history already
taught (see `docs/complexity-synthesis.md`'s lesson 5). Getting its own
experiment number now is not the same decision as folding it into that
sweep — E18 stands on its own validated result (see Consequences above), and
composition-sweep integration is logged as a follow-up in E18's own doc, not
assumed.
