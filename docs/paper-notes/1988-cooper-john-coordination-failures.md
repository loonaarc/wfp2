# Coordinating Coordination Failures in Keynesian Models

Read status: 🟢 read from the PDF.

## Citation
Cooper, R., & John, A. (1988). Coordinating coordination failures in
Keynesian models. *Quarterly Journal of Economics*, 103(3), 441–463.
https://doi.org/10.2307/1885539

## Research Problem
By the mid-1980s several independent papers (Diamond 1982's search model,
Bryant 1983's imperfect-information model, Weitzman 1982's increasing-returns
model, Hart 1982's imperfect-competition model) had each constructed an
economy with multiple, Pareto-ranked equilibria — some with low output/
"underemployment" — without relying on the traditional Keynesian assumptions
(nonrational expectations, sticky wages/prices). These models looked
superficially unrelated (different micro-foundations: search frictions,
information, returns to scale, imperfect competition). Cooper & John ask:
**is there a single, common structural feature driving all of them**, and can
it be isolated and studied in one abstract framework?

## Why the Problem Is Difficult
Each source model buries its coordination-failure mechanism inside
domain-specific machinery (search-and-matching probabilities, information
structures, production technologies, monopolistic-competition demand
systems), making the shared structure hard to see. Showing that multiple
equilibria and inefficiency can occur is not, by itself, informative about
*why*; a genuinely useful contribution needs to strip the mechanism to its
essential game-theoretic core and show it is both **necessary** (not just
sufficient in these particular examples) for the "Keynesian" features
observed (multiple equilibria, a multiplier process, Pareto-rankable
inefficiency).

## Proposed Method
- **An abstract symmetric game** (§II): `I` agents each choose a
  one-dimensional action `eᵢ ∈ [0,E]`; payoff `σ(eᵢ, e₋ᵢ; θᵢ)`. Defines a
  **symmetric Nash equilibrium (SNE)** as an action `e` where, if everyone
  else plays `e`, playing `e` is also each individual's best response
  (`V₁(e,e)=0`), and a **symmetric cooperative equilibrium (SCE)** as the
  locally welfare-maximizing common action for a representative agent
  (`V₁(e,e)+V₂(e,e)=0`).
- Two structural properties are defined and shown to be doing all the work:
  - **Spillovers**: `V₂(eᵢ,ē) ≠ 0` — one agent's action directly affects
    others' *payoffs* (positive spillover if `>0`).
  - **Strategic complementarity**: `V₁₂(eᵢ,ē) > 0` — an increase in others'
    actions raises the *marginal return* to my own action, so my best
    response is increasing in theirs (reaction function slopes upward,
    `ρ = -V₁₂/V₁₁ > 0`).
- **Six propositions** (proved directly from these definitions, not from any
  specific economic model): (1) strategic complementarity is *necessary* for
  multiple SNE (an upward-sloping reaction function is required to cross the
  45° line more than once); (2) any equilibrium with spillovers present is
  inefficient (not an SCE); (3) with positive spillovers there is always a
  *better* symmetric action above any given SNE; (4) with multiple SNE and
  globally positive spillovers, **the equilibria can be Pareto-ranked by
  their action level** — higher-action equilibria are preferred by everyone;
  (5) a continuum of equilibria (when the reaction function coincides with
  the 45° line over an interval) is welfare-increasing along that interval;
  (6) strategic complementarity is **necessary and sufficient** for a
  Keynesian-style multiplier (aggregate response to a shock exceeds any
  individual's own first-round response), quantified as `1/(1-ρ)`.
- **Three worked economic examples** (§III) show strategic complementarity
  arising from genuinely different sources: (A) **input/production
  complementarities** — effort levels in a shared production process, with
  two sub-cases (increasing-returns aggregate production; Bryant's
  `min(eᵢ,ē)` "weakest-link" technology, which produces a literal
  *continuum* of Pareto-ranked equilibria); (B) **trading externalities** —
  Diamond's search model recast in the same framework, where the probability
  of finding a trading partner rises with how many others are also trying to
  trade; (C) **demand externalities** — a multisector, monopolistically
  competitive economy (à la Hart/Heller) where higher output in other
  sectors raises income and hence demand for your sector's output, worked
  through in full with Cobb-Douglas preferences, closed-form prices/
  quantities, and an explicit multiplier calculation (= 2 in the numerical
  example) — plus a fix-price/quantity-rationing variant showing the same
  mechanism survives without any price flexibility at all.

## Experimental Setup
Not applicable — pure theory (an abstract game with propositions proved from
its definitions, illustrated by three worked analytical examples with closed-
form solutions, not simulation or empirical data).

## Metrics
Not applicable empirically. The paper's own organizing device is whether a
given SNE is Pareto-dominated by another SNE or by the (efficient) SCE — i.e.
**equilibrium ranking by welfare**, established purely from the sign of
spillovers and complementarity, not from any numerical simulation.

## Main Results
- **Strategic complementarity is the single, common, necessary structural
  ingredient across all the disparate "underemployment equilibrium"
  models the paper surveys** — this is the headline unifying claim, and it
  is proved in general (Proposition 1), not merely observed to hold in each
  example.
- **Spillovers, not complementarity, drive the inefficiency**; complementarity
  drives the *multiplicity and multiplier*. The two properties are logically
  independent and play distinct roles — a clean conceptual separation the
  paper is explicit about.
- **When multiple equilibria exist under positive spillovers, they are
  Pareto-ranked purely by their action level** — there is no case of two
  incomparable-welfare equilibria in this framework; "better" and "worse"
  equilibria form a strict, unambiguous order.
- **A coordination failure is precisely the situation where a Pareto-superior
  symmetric equilibrium exists but no individual agent has a unilateral
  incentive to move toward it** (explicit definition, p. 445) — a compact,
  reusable definition distinct from mere multiplicity of equilibria.
- The demand-externality example gets a full closed-form multiplier (`=2`
  in the numerical Cobb-Douglas case) and shows the identical qualitative
  result survives under fix-price/quantity-rationing, strengthening the
  claim that the mechanism (complementarity + spillovers), not any specific
  price-adjustment story, is what matters.

## Limitations
- Entirely a **real** (non-monetary) framework — the paper is explicit that
  it says nothing about money non-neutrality, menu costs, or nominal
  rigidities (§IV, conclusion).
- Only addresses **underemployment**, not unemployment in the strict sense —
  agents always choose some positive action level; there is no labor-market
  matching/search unemployment margin in the core abstract game.
- **Static/timeless** — no dynamics, no stochastic shocks over time, no role
  for expectations formation; explicitly named by the authors as the first
  planned extension (§IV).
- The multiplicity/ranking results (Propositions 1–5) are proved for
  **symmetric** equilibria only — asymmetric equilibria (different agents
  choosing different actions) are outside the scope of the formal results.
- The abstract game assumes continuously differentiable payoffs; Bryant's
  `min()` technology example is explicitly flagged as violating this
  (discontinuous marginal products) and analyzed separately, informally.

## Future Work
Explicitly named (§IV, Conclusion): (1) dynamic, stochastic versions of the
same examples, to study intertemporal coordination failures and the role of
expectations; (2) given that coordination failures are established, study
the role of **government intervention** in coordinating economic activity,
particularly in an intertemporal setting.

## Relevance to This Project
- **This is a clean, general, well-suited anchor for "many equilibria, some
  of them good" — the actual macro/coordination-failure framing this
  project's literature review already gestures at**, and unlike Friedman
  (1971; [note](1971-friedman-noncooperative-supergames.md)) or Fudenberg &
  Maskin (1986; [note](1986-fudenberg-maskin-folk-theorem.md)), it needs no
  repeated-game/discounting machinery at all — it is a **one-shot**
  simultaneous-move game, much closer in spirit to a single round of this
  project's CPR game than the repeated-game folk-theorem papers are.
- **The strategic-complementarity/spillover distinction maps cleanly onto
  a testable question about this project's own engine**: does increasing
  the *number* of cooperative-type agents (`conditional_cooperator`,
  `sanctioning`) raise the *marginal* payoff to being cooperative for a
  remaining agent (complementarity), or does it only raise everyone's
  payoff *levels* uniformly (a pure spillover, no complementarity)? If this
  project's agents display genuine strategic complementarity in this precise
  sense, Cooper & John's Proposition 4 gives an off-the-shelf argument for
  *why* multiple stable, Pareto-ranked configurations (all-selfish collapse
  vs. near-`K/2` sustained states) should coexist — and predicts they must
  be rankable purely by "how much cooperation," which is a checkable claim
  against existing E1–E13 data.
- **The paper's own definition of "coordination failure" (a Pareto-superior
  symmetric state exists, but no individual agent benefits from unilaterally
  moving toward it) is a precise, borrowable description of exactly what
  this project's baseline `selfish`-only collapse *is***: every agent
  playing `selfish` is a stable SNE, the near-`K/2` sustained outcome is a
  Pareto-superior SCE, and no individual `selfish` agent gains by
  unilaterally switching. Worth stating this project's central baseline
  finding in exactly Cooper & John's vocabulary — it is a more precise,
  more standard term than "tragedy of the commons" for the specific
  multiple-equilibrium structure (as opposed to Hardin's open-access
  depletion framing, which is about a single degrading equilibrium, not a
  *choice* between a bad and a good one).
- **Complements rather than duplicates Gresov & Drazin (1997;
  [note](1997-gresov-drazin-equifinality.md))**: Cooper & John's multiple
  Pareto-ranked SNE, reachable from the *same* underlying game merely by
  different coordination outcomes, is closest to what Gresov & Drazin would
  call *configurational* equifinality (low conflict, wide latitude) rather
  than a demand-driven *tradeoff* — worth cross-referencing when classifying
  this project's own results per Gresov & Drazin's typology.

## Possible Follow-Up Contribution
A concrete, bounded, genuinely interesting analysis: **check whether this
project's CPR game exhibits strategic complementarity in Cooper & John's
precise sense** — does an agent's expected marginal payoff from playing
cooperatively increase as more of the *other* agents play cooperatively
(holding the resource state fixed, or empirically across configurations)?
If so, this project's near-`K/2` vs. collapse bimodality could be reframed,
citably, as a Cooper & John-style coordination failure with a formally
Pareto-ranked equilibrium set — a small, precise piece of theoretical framing
rather than a new mechanism to build.

## Important Terms
- **Strategic complementarity** — `V₁₂ > 0`: my optimal action increases in
  others' actions (upward-sloping reaction/best-response function).
- **Spillover** (positive/negative) — `V₂ ≠ 0`: others' actions directly
  affect my *payoff*, independent of whether I change my own action.
- **Symmetric Nash equilibrium (SNE) vs. symmetric cooperative equilibrium
  (SCE)** — the individually-best-responding common action vs. the
  jointly-welfare-maximizing common action; the gap between them is the
  paper's measure of inefficiency.
- **Coordination failure** — the specific situation where a Pareto-superior
  symmetric outcome exists but no individual has a unilateral incentive to
  move toward it (distinct from mere equilibrium multiplicity).
- **Multiplier** (Cooper & John's game-theoretic sense) — the ratio of the
  aggregate equilibrium response to a shock over one agent's initial/partial
  response, `= 1/(1-ρ)`; strictly greater than 1 exactly when strategic
  complementarity is present.

## Questions
- Is it feasible to check, empirically from existing simulation runs, whether
  this project's engine displays strategic complementarity in Cooper &
  John's exact sense (marginal payoff to cooperating rising in others'
  cooperation), or is that better established analytically from the payoff/
  regeneration functions directly?
- Should this project's central "all-selfish collapse vs. sustained near-
  K/2" finding be re-described in the thesis using Cooper & John's
  "coordination failure" vocabulary, replacing or supplementing the current
  Hardin-derived "tragedy of the commons" framing?
- Given Cooper & John needs no discounting/repeated-game structure, is this
  the *cleanest* of the three "many equilibria" papers (this one, Friedman,
  Fudenberg & Maskin) to cite as the primary formal anchor, with the other
  two demoted to "related repeated-game results with heavier machinery"?
