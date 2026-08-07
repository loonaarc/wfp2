# A Non-cooperative Equilibrium for Supergames

Read status: 🟢 read from the PDF.

## Citation
Friedman, J. W. (1971). A non-cooperative equilibrium for supergames. *Review
of Economic Studies*, 38(1), 1–12. https://doi.org/10.2307/2296617
(A correction was later published: *Review of Economic Studies*, 40(3), 435,
https://doi.org/10.2307/2296463 — not needed for anything cited here; the
main text and propositions used below are unaffected.)

## Research Problem
In a repeated ("super") game — the same "ordinary" game played every period,
forever, by the same players, with future payoffs discounted — the one-shot
Nash equilibrium (`sᶜ`, the "Cournot point" if players are firms) is usually
*not* Pareto optimal: players could all do better if they cooperated, but
nothing in a non-cooperative game lets them sign a binding agreement to do
so. Can a **non-cooperative** equilibrium — one where every player is
independently, unilaterally best-responding, with no enforceable promises —
still deliver a **Pareto-optimal** outcome?

## Why the Problem Is Difficult
Existing cooperative-game solution concepts (e.g. Nash's own bargaining
solution) get Pareto optimality by assuming players can make binding threats
and commitments — but in a genuinely non-cooperative repeated game, "threats"
of the cooperative-game kind make no sense: nothing forces a player to carry
one out, so a threat that would hurt the threatener too is not credible
(pp. 7–8, explicit argument). Any solution has to be **self-enforcing period
by period** using only the discount factor and the shadow of future play —
not an external enforcement mechanism.

## Proposed Method
- Defines a **supergame strategy** for player *i* as a plan mapping the
  entire observed history of past moves (by everyone) into a current-period
  move (§III) — this is what makes conditioning on others' past behaviour
  possible at all.
- The **Cournot/grim-trigger strategy** (`σᶜ`): always play the one-shot
  Nash equilibrium `sᶜ`, regardless of history. Trivially a non-cooperative
  equilibrium of the supergame (deviating only hurts yourself), but not
  Pareto optimal if `sᶜ` isn't.
- **The key construction** (§IV): pick any Pareto-improving move vector
  `s' ∈ B` (i.e. `πᵢ(s') > πᵢ(sᶜ)` for everyone). Define strategy `σᵢ'`:
  play `s'ᵢ` as long as everyone else has always played `s'ⱼ`; the instant
  anyone deviates, switch to `sᶜ` **forever** (this is what later literature
  calls "grim trigger"). This is a non-cooperative equilibrium exactly when
  the one-period temptation gain from deviating is smaller than the
  discounted infinite-horizon loss from being punished at `sᶜ` forever:
  `(αᵢ/(1−αᵢ))·[πᵢ(s')−πᵢ(sᶜ)] > πᵢ(sᵢ, tᵢ) − πᵢ(s')`, i.e. patience
  (`αᵢ` close enough to 1) beats short-run temptation.
- **The "balanced temptation" equilibrium** `s*` (Proposition 4, the paper's
  headline result): among all Pareto-optimal `s' ∈ B*`, single out the one
  where **every player's temptation ratio is equal**:
  `[πᵢ(s̄ᵢ*,tᵢ)−πᵢ(s*)] / [πᵢ(s*)−πᵢ(sᶜ)]` is the same for all `i`. Proven
  to exist via a Kakutani/Brouwer fixed-point argument (Propositions 2–3,
  §V), and to be a genuine non-cooperative equilibrium whenever every
  player's discount factor clears a threshold set by that ratio
  (Proposition 4).
- §VI relaxes the simplifying assumptions (identical stage games, constant
  discount rates, unique/non-Pareto-optimal one-shot equilibrium) and shows
  the grim-trigger construction survives essentially unchanged (Proposition
  5) — the result is not an artefact of the simplified setup.

## Experimental Setup
Not applicable — pure theory (existence proofs via fixed-point theorems),
illustrated with the oligopoly interpretation (§VII) but no simulation or
empirical data.

## Metrics
Not applicable in the empirical sense. The paper's own "metrics" are its
axioms for what a good supergame solution concept should satisfy (p. 7,
α1–α6: unique & always exists, independent of irrelevant alternatives,
Pareto optimal, symmetric, invariant to linear payoff transforms,
non-cooperative equilibrium) — used to compare the proposed solution against
the Nash cooperative bargaining solution, which the paper argues is
inapplicable here (satisfies α2–α5 but not α1/α6, since it isn't even a
non-cooperative equilibrium concept).

## Main Results
- **Existence, not uniqueness**: a Pareto-optimal, non-cooperative
  "balanced temptation" equilibrium exists whenever discount factors are
  high enough (Proposition 4) — but the paper is explicit that **many**
  non-cooperative equilibria typically coexist (any `s' ∈ B` sustainable by
  a high-enough discount factor gives rise to one), and does not claim its
  named "balanced temptation" point is special beyond satisfying α3–α6.
  This non-uniqueness is stated directly, not glossed over (p. 5: "Existence
  of non-cooperative equilibria in the supergame is no problem. Indeed the
  problem is the reverse; it is easy to show existence of a large number.").
- **The sustaining condition is a patience threshold, not a strategy-space
  fact**: whether a given cooperative move `s'` can be sustained depends
  *only* on whether `αᵢ` exceeds a computable lower bound
  `αᵢ(s')` — as `αᵢ → 1` (discount rate → 0), the bound is always eventually
  cleared, since the infinite-horizon punishment loss grows unboundedly while
  the one-period deviation gain stays finite (p. 6).
- **Oligopoly framing (§VII)**: offers grim-trigger supergame equilibrium as
  a rigorous alternative to informal "tacit collusion" — firms can sustain
  joint-profit-maximizing (Pareto-optimal) behaviour purely out of
  self-interested fear of reverting to the (worse) Cournot equilibrium,
  with no communication or binding agreement required.

## Limitations
- **No targeted punishment.** The grim-trigger response to *any* single
  deviator is *everyone* reverting to `sᶜ` — collective, permanent,
  undifferentiated retaliation. There is no mechanism for punishing only the
  deviator, and no forgiveness/return path once triggered.
- **Assumes players can perfectly observe everyone's past moves** (the
  strategy is a function of full history `s₁,...,s_{t-1}`) — no
  imperfect/noisy monitoring, no communication, no partial observability.
- Multiplicity is left completely open — the paper picks out "balanced
  temptation" as *a* natural equilibrium with nice symmetry properties, not
  as *the* uniquely correct prediction; which equilibrium real players would
  actually reach is explicitly left unresolved (§VII, closing paragraphs).
- Homogeneous, common knowledge of payoffs and discount factors; no
  bounded rationality, no learning, no heterogeneous player types.

## Future Work
States its own next step directly: "the implications of the supergame
equilibrium for oligopoly will be explored in more detail in a subsequent
paper" (p. 12) — i.e. Friedman himself flags this 1971 paper as a
first, general-existence result, with applied oligopoly modelling deferred.

## Relevance to This Project
- **This is the formal ancestor of "many strategies sustain the same
  cooperative outcome"** — but the paper's own notion of *many* is about
  **many possible target points `s'` and many discount-factor thresholds**,
  not about many *different agent strategy types* (selfish/conditional/
  sanctioning/etc., this project's actual axis) converging on one outcome.
  Mapping this project's E1–E13 finding — several different strategy-mix
  configurations all reaching near-`K/2` — onto Friedman's equifinality
  requires care: Friedman's multiplicity lives in *which Pareto-optimal
  point* is targeted and *how patient* players must be, not in *which
  qualitative behavioural rule* an agent follows. Worth stating this
  distinction explicitly if citing Friedman for the equifinality direction,
  rather than implying a closer match than exists.
- **Grim trigger is close to, but not the same as, this project's
  `sanctioning` strategy.** Sanctioning imposes a real-time, targeted,
  *costly* penalty on defectors it observes each round; grim trigger imposes
  an *un-targeted*, permanent, self-fulfilling collapse to the one-shot
  equilibrium triggered by *any* deviation, with no ongoing monitoring cost
  and no way back. This project's engine has nothing structurally like
  grim trigger currently (no "permanently punish everyone after one
  defection" rule) — worth naming as a genuine strategy-space gap if the
  thesis discusses folk-theorem-style mechanisms as one axis of comparison.
- **The discount-factor threshold (`αᵢ(s')`) is a clean, quantifiable
  "patience dial"** — a good formal anchor if the equifinality direction
  wants a parametrised axis (à la "how many periods of future interaction
  are needed before cooperation becomes self-sustaining") distinct from this
  project's existing axes (information, free-rider count, enforcement
  mechanism). This project currently has no explicit discounting of future
  rounds at all — worth flagging as a structural difference from the
  folk-theorem framing, not an oversight to fix.

## Possible Follow-Up Contribution
A cheap, well-scoped addition: since this project's simulation already runs
many rounds with a known horizon, one could compute — for the `selfish`
baseline's one-shot payoff structure at each round — the Friedman-style
sustaining threshold for a "everyone reverts to selfish forever after any
defection" grim-trigger rule, and check whether that threshold is easier or
harder to clear than what this project's actual `sanctioning`/`conditional_cooperator`
mechanisms achieve. Would give a concrete, literature-grounded answer to "is
our finite-horizon, imperfect-monitoring setting more or less permissive
than the classical infinite-horizon folk-theorem baseline" — a genuinely
novel, bounded comparison.

## Important Terms
- **Supergame** — Friedman's own term for a repeated/infinitely-iterated
  game; today usually called a "repeated game."
- **Ordinary game (stage game)** — the one-shot game played each period.
- **Cournot/grim-trigger strategy** — permanent reversion to the one-shot
  Nash equilibrium after any observed deviation; the paper's own name is
  "Cournot strategy" (`σᶜ`), "grim trigger" is later literature's term.
- **Balanced temptation equilibrium** — the specific Pareto-optimal
  non-cooperative equilibrium Friedman singles out, where every player's
  ratio of one-period deviation gain to discounted punishment loss is equal.
- **Temptation** (Friedman's substitute for "threat" in non-cooperative
  settings) — the short-run gain from deviating against others' expected
  continued cooperation, weighed against the discounted future loss from
  triggering reversion to `sᶜ`.

## Questions
- Is Friedman's paper better cited for the *folk-theorem/equifinality*
  angle (many sustainable equilibria) or kept separate from it and cited
  instead as a contrast case (no targeted punishment, unlike this project's
  `sanctioning`) — worth deciding once Fudenberg & Maskin (1986, the more
  general/modern folk theorem) is read, since it may subsume this point.
- Does grim trigger's "collective, permanent, untargeted" punishment
  actually correspond to *any* existing or planned mechanism in this
  project (e.g. a hypothetical "market collapse" or "trust breakdown" event
  after repeated large-scale defection), or is it worth explicitly ruling
  out as out of scope?
- Is the "possible follow-up contribution" above (computing a
  grim-trigger sustaining threshold against this project's actual payoff
  structure) worth doing, or is it a tangent from the thesis's actual
  research question?
