# Thesis Direction — Equifinality: how many approaches reach the optimum?

**Status:** brainstorming note for the bachelor thesis (BA). Not yet a
committed direction. Wahlfachprojekt 2 (E1–E10) is treated as complete; this
note is about where the *thesis* could go and does not change any WP2 result.

## The reframe

One way to reframe the research question, from *"does the commons collapse?"*
to an **optimization / comparison** question:

**What is the maximum sustainable harvest achievable, under different
approaches, in different settings, over a fixed number of rounds — and how many
*different* approaches reach it?**

Two conjectures follow from that reframing:

1. **(Equifinality)** Informed cooperation is probably always (near-)optimal, but
   there may be settings where **many other approaches are *equally* optimal** —
   i.e. the best outcome has *many paths*, not one.
2. **(Complexity as the lever)** The problem gets richer if you **drop "global
   information"**, and richer still if you **add** dimensions: multiple resources,
   group-wise information exchange / cooperation, specialization, …

The link between them is the actual hypothesis: **adding complexity (2) is what
creates the "many optimal solutions" situations (1).** In the simple, fully-informed
model there is essentially one obvious best behaviour (hold `R` at `K/2`); the bet
is that a harder, less-informed world opens up *more* routes to a good outcome.

## What "equifinality" does and does not mean here

- It is **not** "remove the best approach and see what wins second." You keep the
  benchmark in.
- It **is**: define the optimum, then **count how many *different* approaches land
  in the same near-optimal region.** One → the optimum is unique. Several →
  equifinality.

Note this is **already ≥ 1 path even in the current model.** Under global
information, *informed cooperation* and *informed enforcement* both park `R` at
`K/2` and harvest ≈ MSY every round — the same gross harvest. Enforcement just pays
a small monitoring cost, so it is a hair lower on *net* payoff. So the interesting
measurement is **"how big is the near-optimal set, and what pushes an approach out
of it?"** — not "which single approach wins."

## An experiment is three explicit choices

The methodology reduces to a clean template. **An experiment = a fixed setting, a
set of approaches varied within it, and a stated objective:**

1. **The setting `S` (held fixed).** Resource parameters (`g`, `K`), group size,
   information regime, *whether free-riders are present*, disturbance schedule, …
   — everything not under test is held constant, so differences are attributable.
2. **The approaches `A` (varied).** The strategy / institution mixes being compared.
3. **The objective (how "optimum" is scored).** Stated explicitly — see below.

**Within** an experiment: `S` fixed, `A` varied → find the near-optimal set.
**Across** experiments: change `S` → watch the near-optimal set grow, shrink, or
flip. That "watch the winning set change as the setting changes" **is** the
equifinality study. It is also exactly how E1–E10 are already built (each fixes a
setting and varies one axis), so it reuses the existing engine rather than
requiring a rewrite.

This resolves a natural confusion: *"is a free-rider part of the setting or part of
the strategy under test?"* Either — it is a **design choice per experiment.** Fix
"1 free-rider present" as part of `S` in one experiment; fix "0 free-riders" in
another; comparing across the two is what reveals the winner flipping.

## The optimum is not unique — it depends on the objective

"Which approaches are optimal" depends on **what you optimize**, and this itself can
manufacture multiple optima or a trade-off frontier:

| Objective | Who wins (global info, ≥1 free-rider present) |
| --- | --- |
| Gross sustainable harvest | cooperation and enforcement **tie** (both hold `R=K/2`) |
| Net welfare (harvest − costs) | cooperation alone (enforcement pays monitoring cost) |
| Fairness (e.g. Gini) | enforcement (it equalizes) |

So the objective is a **first-class design decision**, and a multi-objective
framing (harvest vs. net welfare vs. fairness as a Pareto frontier) is one concrete
way to make "many paths to the optimum" rigorous: *under objective X these
approaches tie; under objective Y a different one wins.*

## Context-dependence is already visible in the current model

The "best approach depends on who else is in the game" effect does not need new
code — it is in the E9 numbers:

- **0 free-riders:** plain informed cooperation is best (sustains **and** pays no
  monitoring cost).
- **≥1 free-rider:** enforcement overtakes it. Cooperation degrades to ≈ 0.44
  sustainability with one free-rider (suboptimal, not collapsed), while enforcement
  holds ≈ 0.51.

So there is **no single always-best approach even now** — the winner already flips
with population composition. The thesis hypothesis is that *complexity widens this*:
more settings in which several approaches tie.

## Economic / literature anchors

The instinct that economists must already have studied this — that it smells
like macroeconomics — is correct, and it directly answers the "is this novel
or arbitrary" worry — the anchors aren't fringe, they're central to the story.

### The classical baseline: this project's numbers *are* textbook bioeconomics

`dR = gR(1-R/K)`, `R* = K/2`, `MSY = gK/4` is not an arbitrary modelling choice —
it **is** the **Gordon–Schaefer model** (Gordon 1954; Schaefer 1954), the founding
model of fisheries/renewable-resource economics, formalized in Colin Clark's
*Mathematical Bioeconomics* (1976/1990), still the standard reference. Gordon–Schaefer
already derives the fully-informed, single-decision-maker optimal harvest —
exactly the benchmark this project's "informed cooperation" reproduces.

This is good news for "do the numbers feel arbitrary" (they don't — they're the
standard benchmark) and a sharp constraint on the novelty claim: **the single-planner,
fully-informed case is 70-year-old economics, not new.** See "Is this actually a
contribution?" below for where the novelty has to live instead.

### The "many paths to the same outcome" literature

Four distinct, citable anchors for the equifinality claim, roughly best-fit first:

- **Folk theorem (repeated games)** — Friedman (1971); Fudenberg & Maskin (1986).
  In an infinitely/indefinitely repeated game, a whole *set* of outcomes can be
  sustained as equilibria by many different strategies (grim trigger, tit-for-tat,
  various punishment schemes). This is the closest match: the CPR game here *is* a
  repeated game, and "many strategies sustain the same good outcome" is the folk
  theorem's exact content.
- **Turnpike theory (optimal growth theory)** — Dorfman, Samuelson & Solow (1958);
  McKenzie (1976). Optimal paths starting from very different initial conditions
  converge to and spend almost all their time near the same "turnpike," regardless
  of the starting point. A precise economic version of *many paths, one optimal
  corridor* — and it's a resource/growth model, structurally close to this one.
- **Multiple equilibria / coordination failure (macro)** — Cooper & John (1988).
  Many equilibria, several of them good, driven by strategic complementarities —
  the macro literature's version of "no single right answer."
- **Equifinality itself** — the term originates in general systems theory (von
  Bertalanffy, 1968) and was imported into organization theory by Gresov & Drazin
  ("Equifinality: Functional Equivalence in Organization Design," *Academy of
  Management Review*, 1997): different organizational designs can be equally
  effective under the same conditions. This is the exact term for that idea,
  and it comes from *management theory* — it ties directly to the idea that
  this challenges how firms and politics approach strategy (see below).

### Where linear programming actually fits

The intuition that this could be approached with repeated linear programming
isn't wrong, just misplaced. The growth dynamics stay nonlinear (logistic
growth ⇒ nonlinear optimal harvest rule; the sustainable optimum is MSY, so
there is nothing left for an LP to discover in the single-resource case). But
once **multiple resources** are added (one of the proposed complexity axes),
"how to split limited effort/harvest across several pools under
constraints" is a genuine allocation problem, and that sub-problem can legitimately
be linear or integer-linear. So: **LP has a natural home as a multi-resource
allocation layer on top of the nonlinear per-resource dynamics — not as the core
model.**

### Is this actually a contribution, or has it "already been done"?

Directly addressing the recurring worry ("either this was done before, or what I
do is very random"): the anchors above draw the line precisely.

- **Already done, and fine to lean on rather than reinvent:** the fully-informed,
  centrally-optimal single-resource harvest problem. That's Gordon–Schaefer. Citing
  it *strengthens* the thesis — it shows the benchmark is principled, not invented.
- **Not already done (this is where the contribution lives):** classical
  bioeconomics assumes a social planner or a single rational decision-maker. This
  project instead has **decentralized, heterogeneous agents** (cooperative /
  selfish / sanctioning), **imperfect and unevenly distributed information**, and
  **evolving institutions** (voluntary monitoring, population dynamics across
  generations) — nobody is choosing the harvest rule top-down. That combination is
  the territory of Ostrom's empirical commons work and evolutionary game theory /
  multi-agent systems (MAS) research, not classical optimization.
- **The actual novel synthesis:** use the classical planner optimum (Gordon–Schaefer)
  as the fixed benchmark, then ask — as complexity/decentralization increases —
  *how large is the set of decentralized, boundedly-rational strategies that still
  reach (near) that benchmark?* That specific question — near-optimal-set size of
  decentralized strategies, measured against a classical planner benchmark, as a
  function of complexity — is not a standard textbook result. It's a small but real
  synthesis of three literatures (bioeconomics for the benchmark, Ostrom/MAS for the
  agent behaviors, folk theorem/turnpike/equifinality for the "many paths" framing),
  which is an appropriate scope for a BA.

## Keeping the configuration space principled (not arbitrary)

Concern: how do we decide which settings/approaches to allow without it being random?

- Configurations are **motivated by meaningful axes**, not enumerated randomly. The
  axes (information, communication, enforcement, disturbances, and the proposed new
  ones — multiple resources, groups, specialization) are the dimensions the commons
  literature (Ostrom, evolution-of-cooperation) says matter.
- A concrete real-world scenario is **not required** — the abstraction is
  legitimate — but grounding each axis in a **real referent** ("information = do the
  harvesters know the stock; specialization = different boat types; multiple
  resources = fish + water") is cheap and reduces the "these numbers feel arbitrary"
  feeling.
- The discipline: **vary the 1–2 axes the research question names; fix the rest.**

## Enlarging the setting space: what counts as a complexity axis

The original four candidates (drop global information; add multiple
resources; let subgroups coordinate rather than one flat population; add
specialization) have since been superseded by the fuller, literature-checked
list in "Ranking the axes" below — see that section for the current,
maintained roster rather than repeating it here. Two general distinctions
from the early brainstorming are still load-bearing for any *future* axis,
though:

### Telling "complexity" apart from "difficulty"

Not everything that makes a run harder is a complexity axis. Working test: does it
change the *structure* of the problem (how much state exists, how much of it is
observable, how many distinct entities/roles/subgroups must be coordinated) — or
does it just make a *specific realization* of an unchanged structure go worse?

- **Complexity** (structural): information regime, multiple resources, groups,
  specialization, and the additional candidates below — the problem itself has more
  to track or reason about.
- **Not complexity** (harshness/robustness, same structure): free-rider count
  (E9), disturbance magnitude (E8–E10). These already have their own name in this
  project — *resilience* — and stay a separate category, not folded into the
  complexity dial.

### Telling "just a different value" apart from "needs new code"

Also not the same axis of difficulty: whether a candidate is cheap to test.
`information_model` already has both `"global"` and `"private"` implemented in
`config.py`, and population-composition, groups, and boundaries are now
built too (E14/E15/E16, ADR-0012/0013) — testing any of these is picking a
value or running an existing sweep script. Multiple resources, network
reciprocity, reputation, and specialization have no implemented code path
yet (there is no `num_resources` field, no interaction graph, no
`peer_scores`, no agent-role concept) — testing any of them means writing
new mechanism first, not just choosing a value. See "Ranking the axes"
below for which is which.

### Additional candidate axes (surfaced later, checked against already-read literature)

Beyond the four named directly above, a look through what's already been
read for this project turns up more candidates — most of them free of a new
literature detour, because they map onto **gaps this project's own paper notes
already flagged as unrepresented**, not newly invented ideas:

**From Ostrom (1990)'s eight design principles — already read; her own note's
"What it cannot yet represent" section already lists these as gaps
([note](paper-notes/1990-ostrom-governing-the-commons.md)):**
- **Boundaries** (principle 1) — right now every configured agent has full
  harvesting rights unconditionally; this axis would add "outsiders" who aren't
  part of the governed group and aren't bound by its rules — a literal test of
  Gordon's (1954) open-access framing vs. Ostrom's closed-community framing.
- **Collective choice, iterative** (principle 3) — E13's vote is a one-time,
  permanent yes/no. A richer version would let the group keep renegotiating the
  rule over time, closer to what Ostrom actually describes.
- **Conflict resolution** (principle 6) — a cheap, local way for a sanctioned agent
  to dispute a fine, vs. none. Thinner to turn into numbers than the others, but a
  real, already-named gap.
- **Nested enterprises** (principle 8) — the groups/subgroups axis already
  discussed above.

**From the folk theorem literature — already read (Friedman 1971; Fudenberg &
Maskin 1986):**
- **Unknown/uncertain time horizon** — every run currently has a fixed, known
  `rounds`. Folk-theorem results depend heavily on whether players know when the
  game ends; this is the literal "discount factor" dial this note's own
  "Operationalizing" section already names as a candidate lever, just never built.
  Possibly cheaper than the others to test — worth checking whether any existing
  strategy's `decide()` logic actually uses knowledge of `rounds`/the horizon
  before assuming it needs new mechanism, not just a config change.

**From Nowak (2006)'s "Five Rules for the Evolution of Cooperation" — already
read ([note](paper-notes/2006-nowak-five-rules.md)); two of the five mechanisms
map directly onto axes here, one of them with an exact formula for an axis
already built:**
- **Network reciprocity — corrects an earlier mis-classification.** Previously
  logged below as "communication network structure, not yet grounded" — wrong;
  this is Nowak's own rule 4. Instead of the well-mixed interaction this project
  already has (one shared pool, one broadcast channel reaching everyone equally),
  agents sit on a graph and interact only with neighbours. Nowak gives an exact
  condition: cooperation is favoured when `b/c > k` (`k` = average number of
  neighbours) — a precise, citable target to test against, not a vague "add a
  network" idea.
- **Group selection formula — sharpens the axis already built (ADR-0012), not a
  new axis.** Nowak's rule 5 gives an exact condition for when cooperation wins
  under group structure: `b/c > 1 + n/m` (`n` = max group size, `m` = number of
  groups). This directly answers the concern that groups alone might be a
  narrow, near-binary axis (protected/unprotected) once built: sweeping `n` and
  `m` and checking the simulation's actual behaviour against this precise
  prediction turns it into a properly parameterized, theory-grounded sweep
  rather than an on/off test.

**From Nowak & Sigmund (1998), "Evolution of Indirect Reciprocity by Image
Scoring" — already read ([note](paper-notes/1998-nowak-sigmund-indirect-reciprocity.md)).
Really an extension/refinement of the *information* axis (E1), not a fully
separate one — its own paper note already has a near-complete implementation
sketch:**
- **Reputation-based (indirect) reciprocity.** Instead of the binary
  global/private information split, agents track a per-partner **image score**
  (rises with restraint, falls with over-extraction) and cooperate conditionally
  on a specific partner's score, not just the aggregate stock. Exact condition:
  cooperation is evolutionarily stable when `q > c/b` (`q` = probability of
  knowing a partner's reputation). The paper note already sketches how to wire
  this in: extend `Observation` with per-agent `peer_scores`, add a
  `ReputationCooperatorStrategy` with a threshold `k`. More implementation-ready
  than most other candidates here, since the design work is already written up.

**From GovSim (Piatti et al., 2024) — already read
([note](paper-notes/2024-piatti-govsim-cooperate-or-collapse.md)). Upgrades two
axes from "an early hunch" to "a named gap in an already-read paper," though
without a worked formula the way the Nowak citations have:**
- **Multiple resources** — GovSim's own stated limitations name "varying
  regeneration rates and multiple resource types" directly as future work, not
  just this project's own early LP intuition.
- **Specialization / heterogeneous agents** — GovSim also names "different
  stakeholder interests" as an unaddressed extension — a real, if thinner,
  anchor for a specialization axis.

**Still not grounded in anything read — would need a literature check first:**
- Agent entry/exit — population turnover over a run, not just failure (E10).
- **Wealth-weighted collective choice.** ADR-0011's collective-choice vote is
  currently one-agent-one-vote. A variant where voting weight scales with
  accumulated payoff would test whether a small high-payoff minority can
  vote down enforcement that would otherwise pass, even while the broader
  population's own production stays healthy — a real-referent test of
  regulatory capture / plutocratic drift, in the same spirit as grounding
  "specialization" in different boat types (see "Keeping the configuration
  space principled" above). Would need its own citation (political economy
  of capture — Olson-style collective-action literature is the obvious
  first check) before it's as defensible as the Ostrom/Nowak-sourced axes.
- **Inequality-adaptive monitoring investment.** The evolutionary-dynamics
  machinery already built for E5/E11/E12 currently selects strategies on
  raw fitness/payoff alone. Making that fitness function sensitive to
  `payoff_gini` (already computed, see `docs/metrics.md`) rather than mean
  payoff alone would test whether a population under-invests in monitoring
  as inequality rises, and whether that erosion is self-reinforcing — less
  monitoring widening the very inequality that suppressed it. Reuses
  existing evolutionary machinery rather than inventing a new mechanism
  (cheaper than it sounds), but — same caveat — not yet anchored to a
  specific paper; would need a literature check (inequality/wealth-
  concentration dynamics) first.

## Should the growth model itself be varied?

So far every experiment assumes logistic growth, `dR = gR(1-R/K)`. Worth asking
explicitly, since it's a silent fixed assumption, not a derived result.

- **Keep logistic as the base case.** It's not an arbitrary pick — it's the
  Gordon–Schaefer standard (see literature anchors above), it has a clean closed-form
  optimum (`R=K/2`, `MSY=gK/4`) to benchmark against, and E4's threshold results are
  already expressed in its terms. Changing the base case would orphan that work.
- **Treat alternate growth models as a *robustness/secondary* axis, not the primary
  complexity lever.** The complexity axes named above (information,
  multiple resources, groups, specialization) are about the *agents and
  institutions*, which is where the novel contribution lives (see above) — the
  growth function is a property of the *resource*, a different kind of axis.
  Mixing both into the primary sweep dilutes the story; keep it as an optional
  extension if time allows.
- **If pursued, the Allee-effect / critical-depensation variant is the interesting
  one**, not Ricker/Gompertz (which mostly just reshape the same single-hump curve).
  An Allee effect adds a genuine **lower tipping point** — below some `R_min` the
  population can't recover even with zero harvest — i.e. real bistability, not just
  a different growth rate. That connects naturally to the existing E4 "how many
  free-riders before collapse" threshold experiments and would let the thesis show
  whether equifinality (many paths to the optimum) *survives* the presence of an
  irreversible collapse zone, or narrows sharply near it. That's a stronger test of
  the "many paths, if you're not too foolish" claim than logistic alone provides.
- **Recommendation:** logistic stays the spine of the thesis; Allee-effect as one
  robustness check is a good stretch goal if time allows post-Porto, not a
  requirement.

## Should the starting condition (R₀) be varied?

A side-thought from the equifinality brainstorming, not (yet) a dedicated
experiment: every experiment so far implicitly fixes the starting resource
level `R₀` (as part of the setting `S`) without ever naming that choice —
the same kind of silent fixed assumption as the logistic-growth question
above.

- **This is the single most literal test of this project's own founding
  citation for the term.** Von Bertalanffy's (1968) original definition of
  equifinality is exactly "open system + steady state ⇒ final state
  provably independent of initial conditions" (see
  [note](paper-notes/1968-bertalanffy-general-system-theory.md)). Sweeping
  `R₀` — including catastrophic starting levels — at a fixed strategy mix
  and checking whether the long-run outcome actually converges is a direct,
  named test of that claim, not a metaphorical one like the folk theorem or
  turnpike anchors.
- **It is not itself a new complexity axis.** Unlike dropping information,
  adding resources, groups, or specialization, varying `R₀` doesn't touch
  decentralization, information, or institutions — which is where this
  project's actual novel contribution lives (see "Is this actually a
  contribution?" above). It sits in the same category as the Allee-effect
  question: a useful robustness/setting check, secondary to the core
  complexity-axis work.
- **Where it earns its place:** fold `R₀` in as one more swept *setting*
  parameter within whichever complexity-axis experiment it gets tested
  alongside, rather than treating it as a full complexity axis in its own
  right. That reuses the engine and turns "does the near-optimal set /
  winning approach change with a catastrophic start?" into a side-output of
  the main sweep, not a separate research thread competing for BA scope. A
  number is already reserved for it regardless (**E17**, per the numbering
  note in "Ranking the axes" below) — this bullet is about scope, not
  naming.
- **Methodological fit:** now that GLUE (Beven & Binley, 1992/2014; see
  below) is the adopted method for scoring near-optimal-set membership,
  `R₀` is a natural extra dimension to classify with the same
  behavioural/non-behavioural + limits-of-acceptability procedure, at
  effectively no extra methodological cost.
- **Recommendation:** don't build a dedicated experiment for this now; note
  it here as a candidate extra sweep dimension and revisit once the first
  complexity-axis experiment's design is actually committed.

## Operationalizing "sufficient complexity" and "always"

Two things flag the hard part in the early brainstorming: "sufficient
complexity" needs an operational definition, not just a phrase; and "always...
many paths" needs its "always" softened, since no domain is exempt from
counterexamples. Two things to fix before this is BA-shaped:

- **Drop "always."** A thesis can't prove a universal law by simulation over a
  finite set of configurations. Reframe to something demonstrable: **the size of
  the near-optimal set grows (or doesn't) as complexity increases along axis X.** A
  measured trend across swept settings, not a theorem.
- **Define a complexity dial and a set-size metric — this *is* the research
  contribution, not a detail:**
  - **Complexity dial:** an ordered or scored combination of the axes above (e.g.
    number of resources; information regime, from global → private → none; number
    of distinct agent/institution types present; whether disturbances are present).
  - **Near-optimal-set-size metric:** given a chosen objective (harvest / net
    welfare / fairness — see the objective table above) and a tolerance band (e.g.
    ≥ 95% of the Gordon–Schaefer benchmark), count how many distinct approaches
    land inside it, for each setting.
  - **The thesis result is then a curve or table:** near-optimal-set-size vs.
    complexity level. A rising curve supports the hypothesis in this model; a flat
    or falling one is still a legitimate, honest finding — and worth reporting
    either way.

### Ready-made metrics to borrow instead of inventing one

Don't design the complexity dial / set-size metric from scratch — the "many paths"
literature above already has candidate machinery. **Citations verified 2026-08-06
(see [literature-review.md §6](literature-review.md) and the corresponding
paper-notes stubs) — still unread, so the concepts below are confirmed-citable
leads, not yet confirmed-relevant ones:**

- **The folk theorem's own dial-and-set relationship.** It's typically stated in
  terms of the discount factor `δ` (agent patience/far-sightedness): as `δ → 1`,
  the set of payoffs sustainable in equilibrium *grows*. That's a ready-made
  template for "turn a dial, watch a set grow" — map one of the complexity axes
  (e.g. information quality) onto something `δ`-like.
- ~~**Qualitative Comparative Analysis (QCA)**~~ — Ragin's method (*The
  Comparative Method*, 1987), considered and **not adopted**: QCA is built
  for a small, fixed set of historical cases and forces continuous
  configurations into crisp yes/no conditions — a poor fit for a project
  with a simulator that can generate unlimited data with native continuous
  parameters and outcomes. Superseded by GLUE below.
- **GLUE (Generalized Likelihood Uncertainty Estimation)** — Beven & Binley
  (1992, [note](paper-notes/1992-beven-binley-glue.md); 2014 retrospective,
  [note](paper-notes/2014-beven-binley-glue-20-years-on.md)), the adopted
  replacement for QCA. Monte Carlo sample configurations, score each with
  an explicit, pre-declared acceptance criterion ("limits of acceptability,"
  from the 2014 paper), classify behavioural vs. non-behavioural, and
  describe the behavioural *set* directly — matches this project's
  continuous-parameter, unlimited-realization simulator far better than
  QCA's crisp-set/fixed-case machinery. Note the disanalogy flagged in both
  paper notes: GLUE was built to handle uncertainty about an *external*
  reality the model approximates, whereas here the simulation *is* its own
  ground truth — so only the behavioural-classification/limits-of-
  acceptability part transfers, not GLUE's full likelihood-weighted
  uncertainty-bounds machinery (see literature-review.md §6).
- **The hypervolume indicator (multi-objective optimization)** — Zitzler & Thiele,
  used to score the size/quality of a Pareto-optimal set with a single scalar.
  Fits directly if the objective is framed as multi-objective (harvest vs. net
  welfare vs. fairness) rather than a single tolerance band.

## The management/politics framing — motivation, not an experiment

The idea that you can argue endlessly about strategy and still arrive at the
same result is the **significance narrative** — why anyone outside CPR
research should care — not something to build experiments around directly:

- **Use it in the intro/discussion**, not the methods: in sufficiently complex
  systems, no single strategy may be uniquely correct, which reframes (not
  dissolves) the "one correct strategy" debates common in management and policy
  discourse — a legitimate, if provocative, framing.
- **This is exactly why "equifinality" is the right term to lead with** — it's
  literally an organization-theory concept (Gresov & Drazin, above), so the
  management framing isn't a stretch; it's the origin of the vocabulary. This
  also mirrors the analytic-vs-simulation split already in this project:
  derive what can be derived in closed form (MSY, thresholds), simulate the
  rest.
- **A concrete version of this narrative, for the intro rather than the
  methods**: political-economy debates about unchecked inequality (does a
  population keep tolerating a widening Gini as long as aggregate output
  stays healthy; does that tolerance itself let a small high-payoff minority
  capture the institution meant to constrain it) are a real-world instance
  of exactly this "many strategies, no single correct one, until you name
  the objective" framing — motivation for why the wealth-weighted-choice and
  inequality-adaptive-monitoring candidates in "Additional candidate axes"
  above are interesting, even before either is literature-grounded enough
  to build.

## Questions this note originally left open — now resolved by the build

Kept for context on how the direction firmed up, not as live open questions:

- **"Define the optimum operationally"** → resolved: `welfare_efficiency`
  (net payoff / (MSY × rounds)), a single scalar, not a Pareto frontier —
  see `docs/metrics.md`.
- **"Define 'reaches the optimum'"** → resolved: a tolerance band,
  `welfare_efficiency ≥ 0.80` (provisional — see each experiment's own
  threats-to-validity section), not an exact match to the theoretical max.
- **"Which complexity axis first?"** → resolved differently than the
  original guess here (dropping information): **population-type diversity**
  (E14), promoted to first once building groups/boundaries surfaced that
  they were already varying composition implicitly without ever isolating
  it — see "Ranking the axes" below for the reasoning and the current order.
- **"Define the complexity dial and near-optimal-set metric concretely"** →
  resolved: count *and* fraction of compositions clearing the threshold,
  reported separately (see `complexity-synthesis.md`'s methodological
  lessons for why never just one).
- **Scope for a BA** — still the live judgment call, not resolved by a
  build: include every axis grounded in already-read literature as it
  becomes practical, but see the top of this note (and the discussion this
  file doesn't itself record) for the more recent steer toward picking a
  small number of axes that connect to a specific realistic scenario,
  rather than exhausting the full roster for its own sake.

## Ranking the axes (by fit, not by build cost)

Earlier drafts of this note ranked axes partly by implementation cost —
corrected here: **cost is not the ranking criterion; how directly and richly
an axis tests the hypothesis is.** The original framing already implies an
order, and it's a better source than anything invented here: the problem gets
richer if you drop global information, and richer still if you add
dimensions — multiple resources, group-wise information exchange/cooperation,
specialization. Information-dropping is explicitly the *mild* step; the other
three are meant to stack **on top of it**, not sit as separate alternatives.

Ranked by grounding + directness (not cost), across the original four named
axes and every candidate surfaced later (see "Additional candidate axes"
above). **Updated after a full pass through already-read literature (Nowak
2006, Nowak & Sigmund 1998, GovSim 2024) upgraded several entries, and again
after building E14 surfaced a sequencing gap — this is the third revision of
this ranking:**

1. **Population-type diversity** (built, [E14](experiments/E14-population-diversity.md))
   — promoted to 1st on this revision: E15's own `k`-sweep and E16's
   outsider-type sweep both vary population composition without ever
   isolating "how many distinct types coexist" as its own question first,
   the way a clean axis sequence requires. Built as a full 495-composition
   sweep (5 strategies, `N=8`); the finding reframes the axis itself —
   raw type-count turned out to be a weak, confounded proxy for two
   already-known effects (enforcer presence, E3; reciprocal-vs-compensating
   response to a free-rider, E2), so the *recommended* version of this axis
   going forward is two named booleans, not a scalar count (see E14's own
   follow-ups).
2. **Groups / nested enterprises** (built, ADR-0012, now
   [E15](experiments/E15-groups.md)) — grounded in Ostrom,
   and now also in Nowak (2006)'s exact group-selection formula
   `b/c > 1 + n/m`. Sweeping `n` (max group size) and `m` (number of groups)
   against that precise prediction is a properly parameterized test, not an
   on/off mechanism check.
3. **Boundaries** (Ostrom principle 1, now
   [E16](experiments/E16-boundaries.md)) — doubly grounded (Ostrom +
   Gordon), and directly repairs the shared-pool gap ADR-0012's own
   "Consequences" section exposed. Natural pairing with groups (both
   Ostrom-grounded, directly complementary).
4. **Network reciprocity** (Nowak 2006, rule 4) — newly corrected from "not
   grounded" (was mis-filed as "communication topology"). Exact condition
   `b/c > k`; a real, citable mechanism, not a vague structural idea.
5. **Multiple resources** — upgraded from "an early hunch" to
   citation-grounded: GovSim (2024) names "multiple resource types" and
   "varying regeneration rates" directly as its own future work. Likely the
   richest strategy space (diversify, specialise, switch) of any axis here.
6. **Reputation / indirect reciprocity** (Nowak & Sigmund 1998) — grounded,
   exact condition `q > c/b`, and its own paper note already has a
   near-complete implementation sketch (extend `Observation` with
   `peer_scores`, add a `ReputationCooperatorStrategy`). Really an extension
   of the information axis (E1), not a fully independent one. Also the
   cheapest bridge toward the wealth-weighted-choice/capture candidates
   below, if that direction gets picked up later — per-partner reputation
   tracking is close to the machinery a "does the population let itself be
   fooled" study would need anyway.
7. **Specialization** — upgraded from "no grounding" to a named GovSim gap
   ("different stakeholder interests"), though still without a worked
   formula the way the Nowak-sourced axes above have.
8. **Information regime** (built, E1) — the original first example, but only
   two levels exist in the code (`global`/`private`) — cheap to report, too
   narrow on its own to show a trend by itself.
9. **Iterative collective choice, conflict resolution, uncertain time
   horizon** — grounded (Ostrom principles 3/6; folk theorem) but thinner or
   narrower in scope than the axes above; logged as follow-ups, not core.
10. **Agent entry/exit (turnover)** — still not grounded in anything read;
    would need a literature check before being as defensible as the others.
11. **Wealth-weighted collective choice** — reuses existing machinery
    (ADR-0011's vote), but the capture/plutocracy motivation isn't grounded
    in a specific already-read paper yet.
12. **Inequality-adaptive monitoring investment** — reuses existing
    machinery (E5/E11/E12's evolutionary dynamics, `payoff_gini`), same
    grounding gap as 11.

**Numbering note, resolved 2026-08-09:** `docs/literature-review.md` and two
Beven & Binley paper notes independently referenced a *different*,
still-unbuilt "E14" (a GLUE-methodology experiment varying the starting
resource level `R₀`), planned before population-diversity claimed the E14
slot. Renumbered to **E17**.

## Sweep design: staircase vs. full factorial

A one-axis-at-a-time design (test information alone, then groups alone,
then resources alone, each against the same flat baseline) can only show
that a single axis, in isolation, moved the near-optimal set. It cannot show
**interaction** — whether dropping information matters more or less once
resources are also multiple, which is exactly what "does *complexity*
(not any one feature) grow the set" is actually asking about.

**Full factorial** — every combination of every chosen axis — catches
interactions but requires every included axis to already be built, and the
combination count grows fast (even 2 axes at 2 levels each is 4 cells to
run the full strategy roster through; 4 axes at 2–3 levels each is
16–81 cells). Not affordable across every axis in the ranking above.

**Staircase (cumulative)** — matches the original "richer, richer
still" framing directly: start at the baseline, then add one richness
dimension at a time, keeping every previous one turned on (e.g. baseline →
+ private info → + multiple resources → + groups). This gives a genuine
multi-point curve cheaply (one path through the space, not the whole grid)
— but it visits only *one* path through the space, so if the set changes at
some stage you can't tell whether that specific axis would have done the
same thing starting from a different combination of the others; interaction
effects are invisible.

**The resolution: these aren't two designs to choose between, or to run
separately.** A full factorial already *contains* the staircase as one
diagonal path through the same grid — running one factorial gives both the
cumulative trend *and* the interaction effects from a single dataset, no
need to run both designs independently.

**Scope correction (implementation cost is explicitly not the limiting
factor here — see the corresponding discussion this note doesn't otherwise
record): the sweep should include every axis grounded in already-read
literature, not an artificially small subset picked to save build time.**
The earlier "2–3 axes" framing conflated two different constraints that
don't actually require the same answer:
- **How many axes to *build and sweep*** — no reason to cap this for cost
  reasons if cost isn't the deciding factor; include the full grounded set
  (groups, boundaries, network reciprocity, multiple resources, reputation,
  specialization, and the thinner-but-still-grounded ones) as it becomes
  practical to build each.
- **How many axes one heatmap can show at once** — capped at 2 (maybe 3
  with small-multiple facets) **by what a heatmap *is***, not by cost. A
  heatmap is an (x, y, color) picture; it cannot represent a 9-axis
  factorial in one image regardless of how much is built.

**Reporting plan for a large factorial, resolving that second constraint
properly instead of shrinking the sweep to fit a single picture:**
- **Headline: a marginal-effects chart** — one bar per axis, the average
  change in near-optimal-set-size attributable to that axis alone,
  averaged over every other axis's settings. The standard way full-factorial
  designs get reported once there are more than 2–3 factors; not a
  workaround.
- **Supporting detail: pairwise heatmaps only for axis-pairs with a
  detected strong interaction** (found statistically, not guessed) — e.g.
  if groups and boundaries turn out to interact heavily, that pair earns
  its own heatmap; not every pair does.
- **The staircase/cumulative curve stays the headline "does complexity grow
  the set" story**, built from the same dataset.

**A build-order economy worth recording: boundaries may not need new engine
code at all.** Re-examining what Ostrom's principle 1 actually contrasts
with principle 8: "closed community" vs. "open access" is a question of
whether a *fixed, unmonitored batch of outsiders is present in the config
at all* — which the groups mechanism (ADR-0012) already expresses exactly,
by comparing a config with vs. without an extra, ungoverned outsider group.
No new field, no new engine logic — a documented *experimental-design
pattern* reusing groups, not a second mechanism. Network reciprocity,
multiple resources, reputation, and specialization still need real new
code; boundaries likely doesn't.

## Relationship to existing docs

- [research-direction.md](research-direction.md) — the committed WP2 direction and
  the three organizing axes this builds on.
- [experiment-design.md](experiment-design.md) — the experiment template and
  conventions this reuses.
- [experiments/E9-resilience-with-free-riders.md](experiments/E9-resilience-with-free-riders.md)
  — source of the "winner flips with free-riders present" numbers.
- [experiments/E13-binding-agreement.md](experiments/E13-binding-agreement.md) — a
  first concrete, if small, worked example of the near-optimal-set idea: under
  global information, the near-optimal set has **2** members (enforcement, voted
  agreement) for 0–4 free-riders and shrinks to **1** (enforcement only) at 5+ —
  the same "count how many approaches land near-optimal, watch it change as the
  setting gets harder" pattern this note proposes, found before it was deliberately
  gone looking for.
- [experiments/E5-voluntary-monitoring.md](experiments/E5-voluntary-monitoring.md)
  — the replicator machinery a "which approaches survive" study would extend.
