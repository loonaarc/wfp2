# Mathematical Bioeconomics: The Optimal Management of Renewable Resources (Ch. 1–2)

Read status: 🟢 read (targeted: Chapter 1 §1.3 "Summary and Critique" and
Chapter 2 "Economic Models of Renewable-Resource Harvesting" in full,
pp. 21–50, covering §2.1–2.6 — out of the full ~350-page book. Chapters
3–9 not read in full.)

## Citation
Clark, C. W. (1976). *Mathematical bioeconomics: The optimal management of
renewable resources*. Wiley-Interscience. ISBN 0-471-15914-4 (Pure and
Applied Mathematics series).

## Research Problem
Gordon (1954; [note](1954-gordon-common-property-fishery.md)) established
*that* open-access fisheries dissipate economic rent, and Schaefer
(1954/1957; [note](1954-schaefer-population-dynamics-fisheries.md))
established the logistic growth model underlying the yield curve — but
neither paper answers a genuinely dynamic question: given a fish
population currently *away from* any optimum (too depleted, or too
abundant), what is the actual **time path** of harvesting that gets you
there optimally, and how does the answer depend on how much a manager
discounts future revenue relative to present revenue? Clark's book poses
and rigorously answers this as a formal **optimal control** problem, not
just a static equilibrium comparison.

## Why the Problem Is Difficult
Gordon's own model is static/equilibrium — it compares steady states but
says nothing about the trajectory connecting an arbitrary starting
population to an optimal one. Adding real dynamics forces engagement with
**time discounting**: reducing today's harvest to let a population regrow
sacrifices revenue now for revenue later, and how that tradeoff resolves
depends critically on the discount rate — a genuinely new axis Gordon and
Schaefer's papers do not model at all. Solving for the *optimal path* (not
just the optimal endpoint) requires the calculus of variations / optimal
control theory (the Euler equation, and later Pontryagin's maximum
principle), which Clark introduces at the minimum level needed rather than
assuming it.

## Proposed Method
- **The "sole owner" fiction** (§2.4): a single owner (private firm or
  public agency) with full property rights over the fishery, whose
  economically-rational choice is shown (under stated assumptions) to
  coincide with the socially optimal management choice — used to convert
  a *normative* welfare question into a tractable *optimization* problem.
- **Explicit dynamic model**: population `dx/dt = F(x) − h(t)`, harvest
  `h = Q(E,x)`, restricted here to the linear-in-effort form
  `h = G(x)·E`; net revenue rate `R(x,E) = [p − c(x)]·h`, where `c(x)` is
  the **unit harvesting cost** at population level `x` (nonincreasing in
  `x`, since higher stock density makes fish easier/cheaper to catch).
- **The objective functional** (Eq. 2.11): maximize the **present value**
  of the infinite discounted stream of net revenue,
  `PV = ∫₀^∞ e^(−δt)·R(x,h) dt`, where `δ ≥ 0` is the continuous discount
  rate — the paper's central formal device, absent from both Gordon and
  Schaefer.
- **Solving via the Euler equation** gives an implicit equation for the
  optimal *equilibrium* population level `x*` (Eq. 2.16/2.19):
  `p'(x) = δ·[p − c(x)]`, where `p(x)` is the sustainable economic rent
  function — a marginal condition: the marginal gain from harvesting one
  more unit now must equal the discounted present value of the marginal
  future rent sacrificed.
- **The "most rapid approach path" (MRAP)** (Eq. 2.17, §2.5) — the
  paper's single most important novel result for this project's purposes:
  the *dynamically* optimal harvest policy is **bang-bang**, not smooth:
  harvest at the maximum feasible rate whenever `x > x*` (driving the
  population down to `x*` as fast as possible), harvest zero whenever
  `x < x*` (letting it regrow as fast as possible), and harvest exactly the
  sustainable yield `F(x*)` once `x = x*` is reached. This is a genuinely
  new mechanism, present in neither Gordon nor Schaefer: the *dynamics* of
  reaching the optimum, not just the optimum's static location.

## Experimental Setup
Not empirical in the modern sense — a theoretical model, illustrated with
two real-world worked numerical examples using the Schaefer functional
form specifically: the Pacific halibut fishery ("Area 2," parameters from
Mohring 1973: `r=0.71/yr`, `K=80.5×10⁶ kg`, open-access reference stock
`x∞=17.5×10⁶ kg`) and the Antarctic fin whale population (`r=0.08/yr`,
`K=400,000` whales, `x∞=40,000` whales), each solved across a range of
discount rates `δ` from 0% to ∞.

## Metrics
**Optimal equilibrium population level `x*`** and its associated
**optimal sustained yield `Q* = F(x*)`**, tabulated as functions of the
discount rate `δ` (Tables 2.3, 2.4) — a direct, quantitative sensitivity
analysis of the classical Gordon-Schaefer optimum to the one parameter
(discounting) that paper never modeled.

## Main Results
- **A precise, closed-form confirmation of exactly the correction flagged
  in this project's Schaefer note**: for the Schaefer functional form,
  normalizing `z=x/K`, the zero-discount (`δ=0`) optimal population level
  is `z* = ½(1+z∞)`, where `z∞ ∈ (0,1)` is the open-access rent-dissipation
  level — this is **always strictly greater than the MSY level `z=0.5`**
  whenever fishing costs are positive (`z∞>0`). In other words: the true,
  fully-patient economic optimum (Gordon's own "maximize sustainable rent"
  objective) sits **above** `K/2`, not at it — confirming precisely, with
  an exact formula, the qualitative claim already made in this project's
  Gordon and Schaefer notes that this project's `R=K/2` target is the
  *biological* MSY benchmark, not the *economic* optimum.
- **The two limiting cases of discount rate exactly bracket Gordon's own
  two regimes**: as `δ→0`, `x*→x₀` (the rent-*maximizing* level, Gordon's
  own "optimum"); as `δ→∞`, `x*→x∞` (the open-access, rent-*dissipating*
  level) — i.e. **Gordon's open-access equilibrium is mathematically the
  infinite-discount-rate limit of the sole-owner optimization problem**, a
  clean, precise unification of Gordon's two separate models (§III vs. §IV
  in Gordon's own paper) into one continuous family indexed by `δ`.
- **A genuinely counter-intuitive edge case**: when fishing costs are
  independent of stock size (`x∞=0`), a sufficiently high discount rate
  (`δ/r > 1`, i.e. the discount rate exceeds the population's intrinsic
  growth rate) makes **deliberate extinction the formally optimal policy**
  — because a resource growing slower than money can be reinvested is,
  from a purely financial standpoint, worth "cashing out." Clark states
  this plainly, not as a rhetorical flourish, and connects it directly to
  real whaling-industry reluctance to accept conservation limits.
- **Real numbers show growth rate, not discount philosophy, drives
  sensitivity**: for the fast-growing halibut (`r=0.71`), biological
  overfishing only becomes optimal above an implausibly high `δ≈27%`; for
  the slow-growing fin whale (`r=0.08`), even a "modest" `δ=20%` cuts the
  optimal stock and yield roughly in half. This is a clean, quantified
  illustration of why slow-growing species (whales, many tree species)
  are far more vulnerable to purely economic overexploitation than
  fast-growing ones (most fish), independent of any management failure.

## Limitations
- The clean MRAP (bang-bang) result is explicitly stated to be **a
  consequence of the model's linearity in harvest rate** — Clark flags
  directly that this "extreme" policy (instant full-rate harvesting or
  complete closure) is unrealistic and specifically a product of the
  simplifying assumption that only the *amount* harvested matters, not the
  *rate*; nonlinear cost/production effects (examined in the book's later
  Chapter 5) soften this into smoother approach paths.
- The "sole owner" fiction is explicitly named as standing in for, but not
  equivalent to, genuine social-welfare optimization — Clark states this
  assumption is "generally untenable in several important ways," deferred
  to Chapter 5's treatment of true normative theory.
- The worked numerical examples explicitly acknowledge major
  oversimplifications: no age structure (flagged as a "serious omission"
  for slow-growing halibut specifically), a symmetric logistic growth
  curve assumed for the fin whale despite Clark noting the real growth
  curve is "strongly skewed," and no treatment of the fin whale's
  interaction with the (by-then depleted) blue whale population it
  ecologically succeeded.
- Deterministic throughout (no stochastic variation in growth or price) —
  named directly as a scope limitation carried over from Chapter 1.

## Future Work
Not a dedicated section at this point in the book (a textbook, not a
single paper) — but the chapter repeatedly signals what later chapters
relax: nonlinear production/cost effects and "pulse fishing" (Ch. 5), full
optimal control theory via the maximum principle for cases beyond this
chapter's elementary Euler-equation approach (Ch. 4), age structure (Ch.
8), and multispecies/spatial effects (Ch. 9).

## Relevance to This Project
- **This closes the loop this project's Gordon and Schaefer notes both
  left open**, with an exact formula rather than a qualitative gesture:
  `z*=½(1+z∞) > 0.5 = z_MSY` for the true economic optimum under full
  patience. Both of those notes' "Questions" sections should be updated to
  cite this precise result rather than leaving it as an open question —
  **this project's `R=K/2` benchmark is confirmed, with an exact
  closed-form gap, to be the biological MSY point, strictly below the true
  economic optimum**, and the size of that gap is governed by exactly the
  open-access cost/price ratio (`z∞`) this project's engine does not
  currently model as an explicit "cost of effort" for any agent type.
- **The most-rapid-approach-path (MRAP) result is a genuinely new,
  citable idea for this project's disturbance/recovery experiments
  (E8–E10 territory)**: it gives a rigorous, formally-optimal benchmark
  for "how fast should harvesting be cut, and by how much, after a
  disturbance" — bang-bang, not gradual — that this project's own agents
  (which harvest via fixed behavioural rules, not dynamic optimization)
  do not implement and are not designed to approximate. Worth a one-line
  note in a disturbance-experiment write-up: this project's recovery
  dynamics are driven by fixed agent rules, not by an MRAP-optimal
  controller, and are not expected to match this benchmark's speed.
- **The discount-rate framing supplies a clean, well-defined "patience
  dial"** distinct from, but comparable to, Friedman's and Fudenberg &
  Maskin's discount factors in the folk-theorem literature
  ([note](1971-friedman-noncooperative-supergames.md),
  [note](1986-fudenberg-maskin-folk-theorem.md)) — worth noting explicitly
  that bioeconomics and repeated-game theory arrive at *structurally
  similar* "how much do you weight the future" dials from completely
  independent traditions, which is itself a small, interesting point about
  convergent formal structure across literatures, worth a sentence in the
  thesis if the equifinality direction discusses cross-disciplinary
  parallels.
- **A concrete, checkable prediction this project's engine could be tested
  against**: since none of this project's existing agent strategies
  discount future rounds or optimize a present-value objective, none of
  them should be expected to reproduce MRAP-style bang-bang harvesting —
  worth verifying (or explicitly noting as an assumption) that no existing
  strategy accidentally approximates this behaviour.

## Possible Follow-Up Contribution
A precise, bounded addition to this project's model-limitations
discussion: compute, for this project's actual `K`, `g` (mapping onto
Clark's `K`, `r`) and a plausible open-access reference level `x∞` (e.g.
this project's `selfish`-only collapse equilibrium), the exact `z*=½(1+z∞)`
value this project's economically-optimal (but currently unmodelled)
target *would* be — and report it alongside the existing `R=K/2` benchmark
as a labeled, honest comparison ("MSY reference" vs. "true economic
optimum reference") in the docs or web demo, rather than only using `K/2`.

## Important Terms
- **Sole owner** — the fiction of a single rights-holder over a resource,
  used to align private optimization with a normative welfare benchmark.
- **Present value (`PV`) / discount rate (`δ`)** — the objective functional
  and its key parameter; `δ=0` recovers Gordon's "maximize sustainable
  rent," `δ=∞` recovers Gordon's open-access equilibrium.
- **Most rapid approach path (MRAP)** — the bang-bang optimal harvesting
  policy: maximum harvest above the target stock, zero harvest below it,
  sustainable-yield harvest at the target.
- **Bionomic growth ratio (`y = δ/r`)** — Clark's own dimensionless
  parameter (this project should not confuse with `g`, this project's own
  regeneration-rate parameter) expressing the discount rate relative to
  the population's intrinsic growth rate; governs how close the optimum
  sits to the MSY point vs. the open-access point.
- **Unit harvesting cost `c(x)`** — cost per unit harvested at stock level
  `x`, nonincreasing in `x`; the mechanism by which stock scarcity
  self-limits exploitation even under pure profit-seeking.

## Questions
- Should the "Questions" sections of this project's Gordon and Schaefer
  paper notes now be edited to reference this exact `z*=½(1+z∞)` closing
  result, rather than left as open?
- Is it worth computing this project's own implied `z∞` (e.g. from the
  `selfish`-only collapse experiment's steady state, if one is reported)
  to get a concrete number for the "possible follow-up contribution"
  above, or is that a level of quantitative precision beyond what the
  thesis needs?
- Given the MRAP result's dependence on linearity (flagged directly by
  Clark as a simplifying artifact), is a bang-bang benchmark still a fair
  comparison point for this project's smoother, rule-based agent
  dynamics, or would that comparison be misleading without also reading
  Clark's nonlinear extensions (Ch. 5)?
