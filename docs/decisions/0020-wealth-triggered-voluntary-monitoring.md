# ADR-0020: Wealth-triggered voluntary monitoring, not a payoff-weighted vote

- **Status:** Accepted
- **Date:** 2026-08-16
- **Deciders:** project owner (approved scope), assistant (implementing)

## Context

Item 11 in `thesis-direction-equifinality.md`'s ranking ("wealth-weighted
collective choice") was originally sketched as making ADR-0011's
collective-choice vote *payoff-weighted* instead of one-agent-one-vote — to
test whether a small high-payoff minority could vote down enforcement a
healthy population would otherwise pass (a regulatory-capture / plutocratic-
drift story). Olson (1965), *The Logic of Collective Action*, was named as
"the obvious first check" for this item, but had not been read.

**Olson (1965) was read in full for its theoretical core (ch. I, pp. 1–43;
see `docs/paper-notes/1965-olson-logic-of-collective-action.md`), and it does
not support the originally-sketched mechanism.** Olson's book has no voting
stage and no concept of "voting weight" at all — it is entirely about the
prior question of whether a member *unilaterally contributes* to a collective
good in the first place, never how a group *decides* on one. His one
formal, load-bearing result (p. 33) is that a member has an individual
incentive to provide a collective good alone exactly when `F_i > C/V_g`
(their own share `F_i` of the group's total benefit exceeds the good's cost
relative to its total value) — and, where group members are unequal in size
(`S_i`), the member with the largest `F_i` ends up bearing a disproportionate
share of the burden, since everyone smaller free-rides on that member's own
self-interested contribution: "a systematic tendency for 'exploitation' of
the great by the small" (p. 29). This runs in the *opposite* direction from
the plutocratic-capture story originally sketched: Olson predicts the
wealthy *over*-contribute, not that they block outcomes the rest of the
group wants. Building a payoff-weighted vote would test a real, separate
political-economy question, but it would not be an application of Olson
(1965) — the same kind of honest correction ADR-0018 made after reading
Fudenberg & Maskin's own follow-up section, and ADR-0019 made after reading
Chen & Szolnoki in full.

## Considered Options

1. **Payoff-weighted collective-choice vote** (originally sketched, before
   reading Olson). *Rejected: no basis in the cited source; Olson's own
   model has no vote at all, so this would need a different citation
   (regulatory capture / plutocratic drift literature) not yet read, and
   would answer a different research question than item 11 was meant to.*
2. **A new strategy that computes its own `F_i` and decides whether to
   register as `sanctioning` at population-composition time.** Faithful to
   the *shape* of Olson's decision, but static: it collapses back to
   ordinary `AgentSpec` composition sweeps (already exhaustively tested by
   E14/E15/E16) and cannot show the self-limiting dynamic Olson's own
   footnote describes (a volunteer's wealth advantage erodes as they alone
   keep paying to provide the good). *Rejected: too close to existing
   composition sweeps to be a new test, and misses the one dynamic
   Olson's argument is actually about.*
3. **Wealth-triggered voluntary monitoring, re-evaluated every round.** An
   agent with no intrinsic sanction policy (i.e., not already a
   `sanctioning`-strategy agent) becomes an *ad-hoc* volunteer monitor for a
   given round if its own accumulated `total_payoff` exceeds a configurable
   multiple of the population's current average — directly operationalizing
   `F_i` (wealth share) clearing the `C/V_g` threshold, using `total_payoff`
   exactly as Olson's own worked example does ("an owner of vast estates...
   will have a larger `F_i`," p. 29). Only the single wealthiest eligible
   agent volunteers each round (matching this engine's existing "any one
   monitor enforces fully" simplification, and Olson's own point that once
   the largest member has provided the amount they want, no one else has
   any further incentive to contribute). *Chosen.*

## Decision

Option 3. A new `WealthMonitoringConfig` (`threshold: float`,
`monitoring_cost: float = 0.2`) and `SimulationConfig.wealth_monitoring:
WealthMonitoringConfig | None = None` (`None` by default, existing
experiments unchanged). Each round, before enforcement: compute the
population's current average `total_payoff`; among active, **non-`selfish`**
agents whose own strategy exposes no intrinsic `sanction_policy()`, find
those whose `total_payoff` exceeds `threshold × average`; if any exist, the
single *wealthiest* becomes this round's ad-hoc volunteer monitor —
enforcing the same sustainable quota a designated `sanctioning` agent would
(`_sustainable_yield`) and paying the same `monitoring_cost`, charged to its
own `total_payoff` exactly like a real sanctioner's. Re-evaluated fresh every
round (an agent can start and stop volunteering as its relative wealth
moves), scoped to the first pool only (multiple resources, ADR-0016, is out
of scope — the same deliberate limit ADR-0011/0019 already used).

**The `selfish` exclusion was added during implementation, not planned up
front — caught by asking what a wealthy free-rider would actually do if
swept up by the rule as originally drafted.** Enforcement caps *every*
member's harvest at the sustainable quota, including the volunteer's own —
for a fixed-greed extractor this would cap its own over-extraction, a strict
loss with no offsetting benefit (unlike a sustainability-valuing strategy,
which already wants that outcome). A rule that mechanically promoted
whichever agent is wealthiest, regardless of what it actually wants from the
good, would not be testing Olson's `F_i > C/V_g` at all — `F_i` presumes the
volunteer values the good the threshold is being cleared for. Excluding
`selfish` keeps the mechanism honestly scoped to agents Olson's own logic
actually applies to.

Two questions, checked directly against the engine (via `tests/
test_wealth_monitoring.py`) before writing the experiment script — the same
"verify before reporting" discipline as ADR-0016/0017/0019:

- **Q1 (does it emerge and protect the commons with zero designated
  monitors?):** cooperative + selfish agents only, no `sanctioning` agent in
  the composition at all. **Checked directly: it never engages at all.** A
  free-rider consistently out-earns cooperators here (E2's own standing
  finding), which inflates the *population average* so far above any single
  cooperator's own wealth that no cooperator ever clears even a
  barely-above-average threshold — the mechanism is structurally inert in
  precisely the population it would need to protect. A sharper, more
  complete non-engagement than E23's own free-rider-dominance problem (there
  the wealth *floor* engaged but targeted the wrong agents; here the wealth
  *trigger* never fires at all) — see the report for the free-rider-count
  sweep this motivates.
- **Q2 (exploitation of the great by the small, traced over time, without a
  free-rider present):** an all-cooperative population, where `decision_
  noise` is the only source of wealth divergence (deterministic strategies
  never organically diverge on their own). **Checked directly: it does
  engage here**, and the agent who was wealthiest in an otherwise-identical
  ungated run visibly loses payoff relative to its ungated self once
  wealth-triggered volunteering is switched on — the predicted
  disproportionate, self-limiting burden, made directly observable via
  existing `total_payoff` machinery. The report quantifies this across
  seeds and threshold values.

## Rationale

- **Directly operationalizes Olson's one formal result** (`F_i > C/V_g`,
  p. 33) rather than a vote-weighting mechanism his book never describes —
  the citation now actually supports the mechanism built, unlike the
  originally-sketched option.
- **Reuses `Agent.total_payoff` and `_sustainable_yield`, both already
  present and already reused for E23's wealth gate** — no new per-agent
  state, and the same "relative to the population's own current average, not
  a fixed absolute number" framing E23 established, for consistency and to
  avoid inventing a second wealth-normalization convention.
- **The single-wealthiest-volunteer rule matches an existing, already-
  documented engine simplification** ("any one monitor enforces fully,"
  `findings-summary.md`'s Threats to validity) rather than adding a new one —
  and is independently the more Olson-faithful choice (his own small-group
  argument is about the single largest `F_i`, not simultaneous multi-member
  provision).
- **Symmetric with, and a deliberate narrative pair to, E23**: E23 is a
  wealth *floor* that *excludes* low-wealth agents from requesting; E22 is a
  wealth *trigger* that *recruits* high-wealth agents into paying to
  enforce. Both reuse the same `total_payoff`-relative-to-average pattern in
  opposite directions, and both test whether a wealth-based rule protects or
  harms the commons — a natural point of comparison in the eventual report.

## Consequences

- **Mechanically inert whenever a free-rider is present** — the exact
  population this mechanism would most need to protect. This needs to be
  stated plainly wherever the mechanism is discussed, the same way E23's own
  "sounds protective, isn't" caveat is stated for the wealth floor.
- **Any non-sanctioning, non-`selfish` strategy can become the ad-hoc
  monitor** (cooperative, compensating cooperator, conditional cooperator,
  grim trigger, reputation cooperator) — not specific to one strategy
  identity, only to whether it structurally values the good.
- **Enforcement gains a second source of `SanctionPolicy`, layered on top of
  `_enforce()`'s existing group/collective-choice logic without changing
  it** — the volunteer's policy flows through the same per-group
  quota/penalty code every other sanctioner already uses, so no new
  enforcement math is introduced, only a new way a policy can appear.
- **Not folded into the complexity-panel composition sweep** — the same
  scope call as E17/E21/E23: this tests a mechanism question (does
  wealth-triggered volunteering emerge and protect the commons), not a
  composition-space question.
- **The plutocratic-capture question item 11 originally asked is still
  open** and now explicitly logged as a *different*, not-yet-grounded
  candidate (needs its own citation from the regulatory-capture / political-
  economy-of-capture literature), not silently folded into this result.

## Status Notes

Built as **E22** (`scripts/experiment_wealth_monitoring.py`,
[docs/experiments/E22-wealth-triggered-monitoring.md](../experiments/E22-wealth-triggered-monitoring.md)).
