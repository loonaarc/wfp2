# ADR-0011: A collective-choice (voted, jointly-funded) enforcement mechanism

- **Status:** Accepted *(2026-08-06)*
- **Date:** 2026-08-06
- **Deciders:** project owner (approved scope), assistant (implementing)

## Context

E7 found that of the responses to communication tried so far — retaliate,
restrain, enforce — only enforcement protects both the resource and fairness,
but "enforcement" there means some agents are individually, permanently
pre-committed to the `sanctioning` strategy from round 0. Ostrom, Walker &
Gardner (1992) (see
[`docs/paper-notes/1992-ostrom-walker-gardner-covenants.md`](../paper-notes/1992-ostrom-walker-gardner-covenants.md))
show something structurally different in their lab CPR game: groups that
**communicate, then vote whether to adopt a sanctioning mechanism**, and
whose vote passes, reach ~93% of optimal yield with ~4% defection —
approaching a fully cooperative game. Groups that communicate but reject the
sword do far worse (56%, 42% defection). The interesting variable is not "is
someone enforcing" but **whether the group itself chose to be enforced, and
funds it jointly** — this is Ostrom's design principle 3, collective-choice
arrangements, and it is not represented anywhere in this engine: enforcement
currently only exists if an agent happens to be individually configured with
the `sanctioning` strategy, and only that agent pays for it.

Unlike E11/E12 (replicator-dynamics tricks layered on an unmodified engine),
this needs to change behaviour **within a single run** — the group's decision
made at round *k* has to affect every subsequent round of that same run — so
it cannot be done as a post-hoc fitness adjustment the way E11/E12 were. This
is accepted as the first genuine core-engine change of this project's E11–E13
work, scoped as tightly as possible.

## Considered Options

1. **Cost-sharing only, no real vote.** Approximate "collective choice" by
   simply splitting the existing monitoring cost evenly across the group,
   without modelling any decision. Cheap, stays script-level, but does not
   capture OWG-1992's actual finding — that *whether* the vote passes is the
   interesting, consequential event (2 of 4 groups voted yes; the split
   mattered enormously). Rejected: too weak a reproduction to be worth doing.
2. **A real, scheduled group vote inside the engine.** Add an optional
   `CollectiveChoiceConfig`: at a configured round, the engine tallies whether
   the group has been over-using the commons (total harvest exceeding the
   sustainable yield) more than some threshold fraction of rounds so far, and
   if so, adopts a binding quota funded by *every* agent from then on — not
   only whichever agents happen to carry the `sanctioning` strategy. *(Chosen.)*

## Decision

Adopt Option 2, added additively to `SimulationConfig` as an optional field
(`collective_choice: CollectiveChoiceConfig | None = None`; `None` reproduces
every existing config's behaviour exactly unchanged):

- **`CollectiveChoiceConfig(vote_round, overuse_threshold, cost_share)`** —
  new frozen dataclass in `core/config.py`, validated like `DisturbanceConfig`.
- **The vote rule is deterministic and reuses information already in the
  model**, rather than inventing agent preferences or utility functions this
  project doesn't otherwise have: at `vote_round`, look back over all rounds
  simulated so far and compute what fraction had total harvest exceeding the
  sustainable yield (`g·K/4`). If that fraction exceeds `overuse_threshold`,
  the vote passes. This ties the vote to something the group could plausibly
  observe (its own over-use pattern), the same way the broadcast signal
  (ADR-0007) already lets agents see the group's total harvest — a natural
  companion to E6/E7's communication axis, without requiring agents to hold
  explicit beliefs or run any game-theoretic reasoning.
- **If adopted, the engine enforces the same per-capita quota mechanism E5's
  `sanctioning` strategy already uses** (`_enforce`, unchanged), but funded
  by **every active agent without its own individual sanction policy** —
  paying `cost_share` per round — rather than requiring any agent to be
  pre-committed to `sanctioning`. A population of entirely `cooperative` /
  `conditional_cooperator` / `selfish` agents can end up enforced, which is
  the whole point: enforcement becomes something the *group* can choose,
  not a trait some agents are born with.
- If individual `sanctioning` agents are *also* present, they keep paying
  their own cost as before and are not additionally charged the collective
  share (avoids double-charging the same mechanism twice).

## Rationale

- Minimal, additive, and backward-compatible: every existing config has
  `collective_choice=None` implicitly, so E1–E12 are provably unaffected
  (verified by the full existing test suite still passing unchanged).
- Reuses the existing `_enforce` quota mechanism rather than inventing a
  second enforcement code path — the *only* new things are (a) deciding
  *whether* enforcement turns on, and (b) *who* pays for it.
- The deterministic, observation-based vote rule keeps agents simple and
  rule-based, consistent with every other strategy in this project — no new
  agent-level reasoning capability is introduced, only a new *group-level*
  decision computed once, centrally, from data the engine already has.

## Consequences

- **Positive:** for the first time, this project can compare *individually
  pre-committed* enforcement (E3/E5/E7's `sanctioning` strategy) against
  *collectively chosen and funded* enforcement (this mechanism) under
  otherwise identical conditions — a genuinely new axis, not a variant of an
  existing one. See [E13](../experiments/E13-binding-agreement.md) for the
  experiment and result.
- **Negative / scope:** the vote rule is a simplification. Real groups vote
  based on more than a mechanical over-use tally (trust, personalities,
  prior institutional history — OWG-1992's own "hysteresis" finding, where a
  group's *history* with a bad sanctioning design made it vote against a
  better one later). This model has no memory across configurations and no
  agent-level vote (every agent gets the same collective outcome; there is
  no "2 of 4 groups vote yes" — a *config* either crosses the threshold or
  it doesn't, deterministically, for a given seed's history). A stochastic
  or per-agent vote is a real follow-up, not attempted here.
- **Cost-collection realism caveat**, same as ADR-0010: the fine/share is
  collected costlessly and with perfect knowledge of who already sanctions —
  real institutions pay overhead to collect dues that this model doesn't
  charge.
- **A structural fact discovered while testing, not designed in:** if even one
  individually-`sanctioning` agent is present from round 0, the per-capita
  quota already caps total harvest at the sustainable yield every round, so
  over-use (the vote's only trigger) can never be observed and the collective
  vote deterministically fails, *even at `overuse_threshold = 0.0`* — see
  `tests/test_collective_choice.py::test_individual_sanctioner_presence_prevents_the_vote_from_ever_passing`.
  Individual and collective enforcement therefore cannot combine via the
  normal vote pathway; they are mutually exclusive founding mechanisms in
  this model, not layers. Worth stating explicitly in the thesis write-up.
- **Follow-ups:** sweep `vote_round` and `overuse_threshold` to map when the
  vote passes vs. fails, and whether early votes (little evidence) behave
  differently from late ones; a stochastic/probabilistic vote (pass with a
  probability rather than a hard threshold) would let a single config produce
  OWG-1992's "some groups vote yes, some don't" split across seeds.

## Status Notes

Implemented 2026-08-06 as Experiment E13 (binding agreement). Full existing
test suite re-run and green after the change (`collective_choice=None` by
default on every prior config).
