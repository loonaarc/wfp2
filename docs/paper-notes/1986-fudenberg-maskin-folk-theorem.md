# The Folk Theorem in Repeated Games with Discounting or with Incomplete Information

Read status: 🟢 read from the PDF.

## Citation
Fudenberg, D., & Maskin, E. (1986). The folk theorem in repeated games with
discounting or with incomplete information. *Econometrica*, 54(3), 533–554.
https://doi.org/10.2307/1911307

## Research Problem
The classical Folk Theorem says any "individually rational" payoff vector
(one that Pareto-dominates the minimax point) can arise as a Nash equilibrium
of an infinitely repeated game if players barely discount the future — and
the sharper Aumann–Shapley/Rubinstein version gets the same result for
*perfect* (subgame-perfect, i.e. credible) equilibrium, but only with
literally **zero** discounting. Real agents discount the future. Does the
Folk Theorem's full power survive once **positive discounting** is
reintroduced — and separately, can something like it be recovered in
**finite**, not infinite, games via incomplete information about whether
opponents are "rational"?

## Why the Problem Is Difficult
- **Perfection is the crux.** A punishment ("if you deviate, we all switch to
  minimaxing you") only deters if it is *credible* — i.e. it must itself be
  a best response for the punishers, or *they* need a reason to carry it out.
  Reasons need reasons: enforcing a punishment may itself be costly to the
  punisher, requiring a second-order punishment for *not* punishing, and so
  on — an infinite regress of nested threats (explicit in the introduction,
  and central to Example 2's failure case).
- Without discounting, this regress can be resolved by making punishments
  *at each level* arbitrarily severe the further out they lie (Rubinstein's
  construction) — but **with discounting, arbitrarily long punishments are
  no longer arbitrarily severe**, because far-future payoffs are worth less.
  The paper shows explicitly (Example 2) a case where this regress simply
  fails to terminate for any discount factor `δ < 1`: the "punisher" is
  hurt more by punishing than the deviator is by being punished, so ever
  more severe counter-punishments are needed, and the required `δ` threshold
  converges to 1 without ever being reachable.
- **Finite horizons compound the problem via backward induction**: in a
  finitely repeated Prisoner's Dilemma, the unique equilibrium is defection
  every round, by unraveling from the last period — the classical
  folk-theorem logic needs an *open-ended* future to bite at all.

## Proposed Method
Two largely independent results, unified by the same underlying technique
("simple," history-independent punishments, building on Abreu 1983):

1. **Discounted folk theorem (§3, Theorems 1–2)**: for **two-player** games,
   *any* individually rational payoff vector is achievable in a perfect
   equilibrium once players are patient enough — proved constructively via
   **mutual minimaxing**: after any deviation, both players punish each
   other by playing minimax strategies against one another for a *fixed,
   finite* number of periods, then return to the cooperative path (no
   infinite regress needed, because the punishment length, not its per-period
   severity, does the work). For **three-plus players**, mutual minimaxing
   can fail entirely (`n≥3` allows configurations with no valid "everyone
   else minimaxes player *j*" triple), so Theorem 2 instead requires a
   **"full dimensionality"** condition (the feasible-payoff set has an
   interior in `n`-dimensional space) — this lets punishers who carry out a
   costly punishment be *rewarded* afterward with a small permanent bonus
   funded by the extra dimension, restoring their incentive to punish.
   **Example 3 proves full dimensionality is not just a proof convenience**:
   a genuinely degenerate 3-player game is constructed where no equilibrium
   can sustain average payoffs below the *one-shot mixed-strategy* payoff,
   for *any* `δ < 1` — the discounted folk theorem provably fails without it.
2. **Finite-horizon folk theorem via incomplete information (§4–5,
   Theorems 3–4)**: embeds the finite repeated game in a game where each
   player is, with small fixed probability `ε`, a "crazy" type who
   *mechanically* plays a fixed conditional-cooperation/punishment strategy
   rather than best-responding — reviving Kreps–Wilson/Milgrom–Roberts
   reputation-game logic. Because a rational opponent cannot rule out facing
   a crazy type, and crazy types *do* retaliate against defection even near
   the end of the game, backward-induction unraveling from the final period
   is blocked. Splits the finite game into three phases: cooperate-and-punish
   (Phase I, mirrors the infinite-horizon strategy), a transitional buffer
   (Phase II), and a "reputation-building" endgame (Phase III) sized so the
   whole construction doesn't unravel — and shows the needed lengths of
   Phases II/III are **independent of total game length**, so for long
   enough games nearly the whole game is spent cooperating.

## Experimental Setup
Not applicable — pure theory (existence proofs via explicit constructive
strategies plus two small counterexample games, Examples 1–3, used to
demonstrate where naive extensions fail).

## Metrics
Not applicable empirically. The paper's organizing concept is the
**individually rational payoff set `V*`** (payoffs Pareto-dominating the
minimax point) and whether the **perfect-equilibrium payoff correspondence
`V(δ)`** converges to it as `δ → 1` (technically: whether `V(·)` is *lower
hemicontinuous* at `δ = 1` — the paper's central technical question).

## Main Results
- **Two-player discounted folk theorem holds without qualification**
  (Theorem 1): any individually rational payoff pair is sustainable in
  perfect equilibrium for `δ` close enough to 1, via simple mutual
  minimaxing — no full-dimensionality condition needed for `n=2`.
- **`n≥3` needs full dimensionality, and this is a real restriction, not a
  technicality** (Theorem 2, Example 3): in Example 3's degenerate 3-player
  game, the discounted folk theorem's conclusion *provably fails* — no
  perfect equilibrium can push average payoffs below the static
  mixed-equilibrium payoff (1/4), for any discount factor at all. This is a
  clean demonstration that discounting introduces genuine, non-vanishing
  limits on what "many strategies reach the same optimum" can mean, contrary
  to the frictionless intuition of the classical (undiscounted) Folk
  Theorem.
- **The finite-horizon result (Theorem 4) needs only two players in general**
  (full generality for `n≥3` is deferred, footnote 19, to future work) —
  and requires the existence of a one-shot Nash equilibrium giving *both*
  players strictly more than their minimax value, a real restriction stated
  explicitly, not glossed over.
- **Both the discounting and incomplete-information routes converge on the
  same qualitative conclusion**: with enough patience (discounting) or
  enough of a *shadow of doubt* about rationality (incomplete information),
  cooperation sustainable at the individually-rational level is recoverable
  — but *how much* patience/doubt is needed, and whether it is achievable
  at all, depends on structural properties of the game (dimensionality,
  the shape of `V*`) that the classical undiscounted Folk Theorem simply
  never has to confront.

## Limitations
- Requires **common knowledge of the discount factor / payoff structure**;
  no bounded rationality, no learning — deviations are always correctly
  attributed and punished with perfect calculation.
- The 3+-player discounted result depends on **full dimensionality**, which
  the paper itself shows (Example 3) can fail in economically simple games —
  this is a genuine gap, not fully closed in this paper (mixed-strategy
  observability issues addressed in §6, but the dimensionality condition
  itself is left as a hard requirement).
- The finite-horizon incomplete-information construction (Theorem 4) is only
  fully proved for **two players** under an added Nash-equilibrium condition;
  the `n≥3` case is explicitly deferred.
- **Monitoring is assumed perfect** (§2–5) or, after relaxation in §6, at
  least *action-level* observable — no noisy/private signals of others'
  play, no communication, no partial observability, which is a substantially
  stronger assumption than most CPR/commons settings can make.
- The "crazy type" device is a modelling convenience whose specific form
  (which strategy the crazy type mechanically follows, what off-path beliefs
  are assumed) is chosen *by the theorist* to make the proof work (explicit
  in the Remark after Theorem 3) — it is not derived from any independent
  account of what real bounded-rational or norm-following agents actually do.

## Future Work
Explicitly named as open: extending the finite-horizon incomplete-information
folk theorem (Theorem 4) to three-or-more players under a full-dimensionality
condition (footnote 19); the stability (in the Kohlberg–Mertens sense) of the
constructed equilibria, addressed only partially via a "trembling" crazy-type
modification (§5, response to a referee/Kreps's critique).

## Relevance to This Project
- **This paper is the correct, general anchor for "many strategies sustain
  the same near-optimal outcome" — more so than Friedman (1971;
  [note](1971-friedman-noncooperative-supergames.md))**, which only shows
  Pareto-*improving* points above the one-shot Nash equilibrium are
  sustainable, not the *entire* individually-rational set. Fudenberg &
  Maskin's `V*` is the maximal such set — worth citing this paper, not
  Friedman, if the thesis wants the strongest formal equifinality claim
  ("almost anything reasonable is achievable given enough patience").
- **The dimensionality/degeneracy caveat is the single most useful, most
  citable finding for this project's actual argument.** This project's
  claim is implicitly the *opposite* direction from the classical Folk
  Theorem: not "with enough patience, anything is achievable," but "with a
  fixed, finite number of rounds, no discounting, and boundedly-rational
  rule-based agents (not fully-rational best-responders), *only some*
  qualitative strategy combinations reach near-`K/2`." Fudenberg & Maskin's
  Example 3 is valuable precisely because it shows that **even the idealized,
  fully-rational, infinitely-patient benchmark has structural cases where
  the "anything is sustainable" folk-theorem promise breaks down** — i.e.
  frictionless equifinality is not automatic even in the classical
  framework, which strengthens (rather than undercuts) the interest of
  characterizing *which* configurations in this project's engine actually
  reach the good outcome and which don't.
- **This project's engine has none of the paper's core machinery**: no
  discounting of future rounds, no minimax punishment, no incomplete
  information about opponent "type" in the crazy/sane sense, no
  fully-rational best-responding. This is worth stating plainly in the
  thesis rather than implying a tighter connection than exists — the
  connection is at the level of the *question* (many paths to one outcome)
  and the *cautionary finding* (this need not hold universally, structural
  conditions matter), not at the level of shared mechanism.
- **A genuinely useful terminological borrowing for the thesis**:
  "individually rational set" (`V*`) is a clean, standard name for "the set
  of outcomes at least as good as everyone acting purely selfishly" — a
  natural lower bound this project could reference when describing what
  counts as a "successful" cooperative outcome in the CPR game (better than
  the all-`selfish` collapse baseline), distinct from the resource-based
  `K/2` sustainability benchmark it currently uses.

## Possible Follow-Up Contribution
None with a clean, bachelor-scoped path — the paper's machinery (minimax
strategies, discounting, incomplete-information equilibrium refinement) is
substantially heavier than this project's rule-based agent framework, and
porting it in would be a different (much larger) project. Best used as a
**citation for framing and caution**, not as a source of a portable
mechanism or metric.

## Important Terms
- **Individually rational payoff set (`V*`)** — payoffs that Pareto-dominate
  the minimax point; the maximal target set for folk-theorem results.
- **Minimax strategy / reservation value (`v*ⱼ`)** — the strategy the other
  players use to hold player `j` down to the lowest payoff they can force;
  `v*ⱼ` is that floor.
- **Full dimensionality** — the feasible payoff set `V` has a nonempty
  interior in `n`-dimensional space; needed for `n≥3` discounted folk
  theorems to reward punishers without running out of "room."
- **Simple (history-independent) punishment / Abreu's "stick-and-carrot"**
  — punishments that depend only on *whether* a deviation occurred, not on
  the full history of play; the technical device that avoids the infinite
  punishment-regress problem under discounting.
- **Crazy type / reputation equilibrium** — a small-probability player type
  that mechanically follows a fixed (non-best-responding) strategy, used to
  block backward-induction unraveling in finite games.

## Questions
- Given the "individually rational set" concept, is it worth re-describing
  this project's own outcome metric (net welfare relative to all-`selfish`
  baseline) explicitly in those terms in a terminology/glossary pass?
- Is Example 3's degeneracy condition (a game where the individually
  rational set is one-dimensional) analogous to *any* identifiable
  configuration in this project's strategy-mix space — e.g. all-selfish plus
  a single conditional cooperator — or is the analogy too loose to be worth
  drawing out formally?
- Should the thesis cite Fudenberg & Maskin *and* Friedman together as
  "the folk-theorem family," with Friedman flagged as the earlier, weaker,
  more mechanistically-relevant (grim-trigger, closer to a strategy this
  project could implement) special case, and Fudenberg & Maskin flagged as
  the general/strongest formal result but the least mechanistically
  relevant?
