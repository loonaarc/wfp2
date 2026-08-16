# ADR-0018: Grim trigger as a new strategy, and the cost of a finite horizon

- **Status:** Accepted
- **Date:** 2026-08-16
- **Deciders:** project owner (approved scope), assistant (implementing)

## Context

Item 9 in `thesis-direction-equifinality.md`'s ranking ("iterative collective
choice, conflict resolution, uncertain time horizon") bundles three loosely
related ideas under one slot. Of the three, only the time-horizon piece has
papers already *read* and directly on point: Friedman (1971), the
"grim-trigger" supergame equilibrium, and Fudenberg & Maskin (1986), the
general discounted/finite-horizon folk theorem. This ADR scopes and builds
that piece as **E21**.

**A real scoping correction, caught by reading the grounding closely, not
skimmed:** both papers' own "Possible Follow-Up Contribution" sections were
read before any design work started. Fudenberg & Maskin's is explicit:
*"None with a clean, bachelor-scoped path — the paper's machinery (minimax
strategies, discounting, incomplete-information equilibrium refinement) is
substantially heavier than this project's rule-based agent framework... Best
used as a citation for framing and caution, not as a source of a portable
mechanism."* Building a literal discounted-folk-theorem or
incomplete-information "crazy type" mechanism would mean porting apparatus
this project's engine has no analogue for (rational best-responding agents,
common-knowledge discount factors, minimax punishment) — a different, much
larger project, not a well-scoped bachelor axis.

Friedman's own follow-up section, by contrast, names something concretely
buildable: *"compute... the Friedman-style sustaining threshold for a
'everyone reverts to selfish forever after any defection' grim-trigger rule,
and check whether that threshold is easier or harder to clear than what this
project's actual `sanctioning`/`conditional_cooperator` mechanisms
achieve."* Friedman's own Relevance section independently flags this as a
real, named gap: *"This project's engine has nothing structurally like grim
trigger currently (no 'permanently punish everyone after one defection'
rule)."* Fudenberg & Maskin's own central technical point — *"finite
horizons compound the problem via backward induction... the classical
folk-theorem logic needs an open-ended future to bite at all"* — gives a
second, directly testable question once grim trigger exists: does *when* in
a finite, known-length run a defection is detected change how costly the
resulting permanent punishment is.

## Considered Options

1. **Port Fudenberg & Maskin's discounting/incomplete-information machinery
   directly** (a discount factor on future payoffs, a "crazy type"
   reputation device, minimax punishment). *(Rejected — the papers' own
   follow-up sections disclaim a clean path; this project's engine has no
   analogue for rational best-responding, common-knowledge discount
   factors, or minimax punishment, and building all of that would be a
   different project.)*
2. **A purely analytical exercise** — compute Friedman's discount-factor
   threshold formula against this project's own payoff numbers, no new
   simulation. *(Cheaper, but doesn't test anything about *this* engine's
   actual boundedly-rational, rule-based agents — the formula assumes
   fully-rational best-responding players, which none of this project's
   strategies are. Rejected as not actually informative about the model
   being studied.)*
3. **Build grim trigger as a real, registered strategy — a genuine
   strategy-space gap Friedman's own note names explicitly — and test it
   two ways: does it out- or under-perform the existing partially-forgiving
   mechanisms, and does the round at which it triggers matter given a
   fixed, finite horizon.** *(Chosen.)*

## Decision

Option 3. A new `GrimTriggerStrategy` (`src/emergent_cooperation/strategies/grim_trigger.py`,
registry key `"grim_trigger"`): cooperates exactly like `conditional_cooperator`
(same "surplus above `K/2`" harvest rule, same decline-detection trigger) with
one deliberate difference — once triggered, **it never returns to
cooperation for the rest of the run**. `conditional_cooperator`'s own
`declined` check is recomputed fresh every round (so a single bad round
resolves as soon as the stock stops falling); grim trigger adds one
persistent field, `self._triggered`, that latches `True` forever the first
time a decline is detected and is never reset. This is not a bug to avoid —
it is the literal definition of Friedman's strategy, and the harshness is
the point of comparison.

Two questions:

- **Q1 (does permanent, unforgiving punishment out-cooperate temporary,
  forgiving punishment?):** sweep free-rider count against matched
  `conditional_cooperator`- and `sanctioning`-based populations, same
  scenario Friedman's own follow-up names.
- **Q2 (does the finite horizon matter — Fudenberg & Maskin's own point):**
  force a single free-rider's defection to be detected at different rounds
  of a fixed 100-round run and measure the resulting welfare loss. Backward-
  induction intuition predicts an early trigger should cost far more than a
  late one, since permanent punishment has more of the game left to act on.

## Rationale

- **Reuses the existing decline-detection mechanism exactly** — the only
  new logic is the persistence of `_triggered`, matching this project's
  "additive, doesn't disturb what's already there" discipline (ADR-0012,
  ADR-0014, ADR-0016).
- **Directly answers a question the grounding papers themselves pose, not
  one invented to have something to build.** Both follow-up sections were
  read before scoping began; the chosen design is literally the one
  Friedman's own paper suggests as feasible, and rejects the one
  Fudenberg & Maskin's own paper says isn't.
- **Q2 is the genuine "uncertain/finite time horizon" test**, made concrete
  without porting any discounting machinery: the *finiteness* of the round
  budget is already built into every experiment this project runs; Q2 asks
  whether that finiteness matters for how costly a permanent, un-forgiving
  punishment mechanism is — the same structural point Fudenberg & Maskin
  make about backward induction, tested empirically instead of proven
  analytically.

## Consequences

- **Not added to the complexity-panel composition sweep as a 7th composable
  type (unlike reputation, E18/ADR-0014).** E21's own novel contribution is
  Q2 (round-timing), a dimension orthogonal to population composition —
  folding `grim_trigger` into the diversity sweep is a reasonable, cheap
  future extension (flagged as a follow-up) but not attempted here, so this
  axis doesn't silently become "reputation's story again" without adding
  anything new.
- **No discounting, no rationality, no common-knowledge assumptions were
  added to the engine** — `grim_trigger` is a boundedly-rational, mechanical
  rule (exactly like every other strategy here), not a calculated
  best-response. The connection to Friedman/Fudenberg-Maskin is at the level
  of the *question* (does permanent punishment sustain cooperation; does a
  finite horizon matter), not shared machinery — stated explicitly per both
  papers' own "Relevance to This Project" sections, rather than implying a
  tighter formal connection than exists.
- **A real, citable empirical answer to a question the classical literature
  only answers under much stronger rationality assumptions.**

## Status Notes

Built as **E21** (`scripts/experiment_grim_trigger.py`,
[docs/experiments/E21-grim-trigger-finite-horizon.md](../experiments/E21-grim-trigger-finite-horizon.md)).
