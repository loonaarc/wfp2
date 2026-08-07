# The Comparative Method: Moving Beyond Qualitative and Quantitative Strategies

Read status: 🟢 read (targeted: Chapter 2 "Heterogeneity and Causal
Complexity" in full, pp. 19–33; the opening of Chapter 3 on Mill's methods,
pp. 34–43; the transition/synthesis passage closing Chapter 5, pp. 82–84;
and Chapter 6 "A Boolean Approach to Qualitative Comparison: Basic
Concepts" in full, pp. 85–98 — out of the full ~180-page book. Chapters
1, 4, 7–9 not read in full). Companion review — Miller, W. (1987). [Review
of *The Comparative Method*]. *Journal of Public Policy*, 7(4), 454–456 —
read in full (3 pages).

*Conceptual/methodological source (introduces a method, not an empirical
study) — using the alternate note shape from `_template.md`: Key Concepts
/ Main Contribution instead of Why-Hard/Method/Setup/Metrics/Results.*

## Citation
Ragin, C. C. (1987). *The comparative method: Moving beyond qualitative and
quantitative strategies*. University of California Press. ISBN
0-520-05834-8.

Miller, W. (1987). [Review of the book *The comparative method: Moving
beyond qualitative and quantitative methods*, by C. R. Ragin]. *Journal of
Public Policy*, 7(4), 454–456. (No DOI found — pre-DOI-era book review;
included here as a concise independent summary, read alongside the primary
source, not in place of it.)

## Research Problem
Comparative social science (e.g. comparing a dozen-to-hundred countries or
regions) sits in an awkward methodological gap: too many cases for
traditional **case-oriented** methods (deep, holistic comparison of a
handful of cases, as in Barrington Moore's work), but too few, and too
qualitatively rich, for standard **variable-oriented** statistical methods
(regression-style models assuming additive, linear effects across hundreds
of cases). Ragin's question: is there a method that keeps the case-oriented
tradition's core strength — treating cases as whole configurations, and
taking seriously that a single outcome can arise from *several different*
combinations of causes — while still being systematic and scalable to
moderate numbers of cases, the way statistical methods are?

## Key Concepts
- **Multiple conjunctural causation** — Ragin's central causal-complexity
  concept, introduced in Chapter 2 and used throughout: an outcome is
  **conjunctural** when it results from the *intersection* (AND) of several
  conditions together, not any one alone (following J.S. Mill's 1843
  "chemical causation" — a phenomenon emerging only when the right
  ingredients combine); it is **multiple** when *several different*
  intersections/combinations can each independently produce the *same*
  outcome. This second property — several distinct causal recipes reaching
  one outcome — is Ragin's version of equifinality, stated in explicitly
  causal-methodological terms rather than von Bertalanffy's dynamical-
  systems terms ([note](1968-bertalanffy-general-system-theory.md)).
- **Case-oriented vs. variable-oriented strategies** (Chapters 3–4): case-
  oriented work compares a small number of cases *as wholes*, generally via
  Mill's **method of agreement** (find what all instances of an outcome
  share) or **indirect method of difference** (cross-tabulate presence/
  absence of cause against presence/absence of effect) — both shown,
  explicitly and with worked examples, to break down under multiple or
  conjunctural causation (a condition can be wrongly "rejected" as a cause
  because it only matters in combination with something else). Variable-
  oriented work fits statistical models (typically additive) across many
  cases, which is well-suited to large-N generalization but structurally
  **assumes away** conjunctural causation (an additive model asserts each
  cause's effect is constant regardless of the other variables' values —
  exactly the assumption multiple conjunctural causation violates).
- **The Boolean/QCA method** (Chapters 6–7, "Qualitative Comparative
  Analysis"), offered as the synthesis: represent every case as a row in a
  **truth table** (a 1/0 score on each of `k` binary causal conditions plus
  a 1/0 outcome; `2^k` possible rows). Combine rows using **Boolean
  addition (OR)** and **Boolean multiplication (AND)** — e.g. `F = A + B +
  C` means the outcome `F` occurs if condition `A` OR `B` OR `C` is
  present, each independently sufficient; `F = AC + Bc` means `F` occurs
  from the combination of `A` AND `C`, OR from `B` combined with the
  *absence* of `C`. **Boolean minimization** then simplifies a "primitive"
  (unreduced) equation listing every observed combination into a logically
  minimal set of **prime implicants** — the smallest number of causal
  combinations needed to account for every case with the outcome — using a
  single explicit rule: two rows differing in only one condition but
  sharing the same outcome mean that one condition is irrelevant in that
  context and can be dropped (formally identical to holding all-but-one
  condition constant in an experiment). A **prime implicant chart** then
  picks the minimal set of prime implicants that together cover every
  original case.
- **Worked toy example (regime collapse, Ch. 6)**: three binary causes
  (officer conflict `A`, dictator's death `B`, CIA dissatisfaction `C`),
  each independently sufficient for regime failure — reduces cleanly to
  `F = A + B + C`. A second, less trivial example (strike success) shows
  four positive-outcome truth-table rows reducing, via two rounds of
  minimization, to `S = AC + Bc` — two logically distinct, both-sufficient
  recipes for the same outcome, each a **conjunction** of two conditions —
  the paper's clearest small-scale illustration of what multiple
  conjunctural causation looks like once formalized.

## Main Contribution
The single reusable artefact is **Qualitative Comparative Analysis (QCA)**:
a systematic, replicable, Boolean-algebra-based procedure for taking a
moderate number of cases (roughly a dozen to a few hundred), each scored on
several binary conditions plus an outcome, and deriving the **complete,
logically minimal set of condition-combinations sufficient for that
outcome** — explicitly designed to represent and preserve multiple
conjunctural causation (several independently-sufficient recipes for one
outcome) rather than average it away, which is exactly what standard
regression-style methods structurally cannot do.

## Limitations
- **Requires binary (or coarsely categorical) coding of every causal
  condition** — continuous variables must be dichotomized or bucketed,
  discarding information; Ragin acknowledges this tradeoff directly (loss
  of information "typically is not great" for genuinely qualitative
  phenomena, but is a real cost for continuous ones).
- **Truth-table rows with contradictory outcomes** (some cases with a given
  condition-combination show the outcome, others with the identical
  combination don't) are a real, common problem the basic method in
  Chapter 6 sets aside ("assume... no contradictory rows exist," explicitly
  deferred to Chapter 7) — the clean examples in this note's read portion
  are, by Ragin's own admission, unusually well-behaved.
- **The number of possible condition-combinations grows exponentially
  (`2^k`)** with the number of causal conditions `k`, while realistic data
  sets rarely contain cases realizing every combination — Ragin's own
  discussion (in the unread Chapter 7, per the Miller review and the TOC)
  addresses this "limited diversity" problem, but it is a structural
  limitation of the method, not fully resolved in the portion read here.
- **Frequency/robustness is explicitly de-emphasized**: "the number of
  instances of each combination of causal conditions does not enter
  directly into any computations" (p. 88) — a row supported by one case
  counts the same as one supported by twenty, unless the investigator
  manually imposes a frequency cutoff. This is a deliberate design choice
  (cases are types, not data points to be averaged), but it is a genuine
  tradeoff against statistical robustness that the method does not resolve
  automatically.
- **The Miller review's own criticism** (independent secondary judgment,
  read in full): Ragin does not, within the book, give a detailed head-to-
  head comparison against alternative interaction-capable statistical
  techniques (e.g. log-linear analysis), and Miller judges Ragin's claim
  that such alternatives are inherently biased toward simpler, non-
  interactive models to be flatly wrong for log-linear analysis
  specifically — a genuine limitation in the book's own argument for why
  QCA is needed at all, not just a limitation of QCA as a technique.

## Relevance to This Project
- **This is a formal, off-the-shelf method for exactly the kind of question
  this project's equifinality direction is asking**: "which combinations
  of strategy-mix conditions are *sufficient* to reach a near-`K/2`
  outcome, and how many distinct such combinations are there?" This maps
  directly onto QCA's core operation — code each experiment configuration
  (e.g. presence/absence of `sanctioning`, `conditional_cooperator`,
  communication, voluntary/collective enforcement, etc.) as a truth-table
  row, code "reached near-`K/2`" as the binary outcome, and run Boolean
  minimization to get the logically minimal set of **sufficient**
  strategy-mix recipes — a genuinely novel, precise, and directly citable
  way to state this project's central equifinality claim, rather than an
  informal "several configurations seem to work" description.
- **Distinct from, and complementary to, the other equifinality-direction
  readings**: von Bertalanffy's equifinality (fixed dynamics, varying
  initial conditions, same steady state) and Cooper & John's multiple
  Pareto-ranked equilibria (fixed game, multiple stable outcomes) are both
  about *dynamical* convergence; Ragin's multiple conjunctural causation is
  about *combinatorial/causal-structural* convergence — several different
  **configurations of causes** (not initial conditions, not equilibrium
  selection) each sufficient for the same outcome. This project's actual
  E1–E13 finding — several different strategy-mix *configurations* reach a
  comparable resource outcome — is arguably closest in *kind* to Ragin's
  sense, since it is fundamentally about which combinations of
  present/absent mechanisms (not starting conditions or discount factors)
  are sufficient.
- **A genuinely feasible, bachelor-scoped analysis technique**, not just a
  citation for framing: unlike McKenzie's turnpike theory or Fudenberg &
  Maskin's folk theorem (both requiring substantial reformulation to touch
  this project at all), QCA could be run directly on this project's
  existing experiment results with modest tooling — code each experiment's
  configuration flags as binary conditions, code its outcome, build the
  truth table, and either compute the minimization by hand (feasible for
  the current ~13-experiment, few-condition scale) or with an existing QCA
  software package.
- **A precise vocabulary upgrade for the thesis**: this project's writing
  can distinguish, using Ragin's own terms, between conditions that are
  merely **associated with** a good outcome (correlational) and conditions
  that are part of a **logically minimal sufficient combination** (QCA's
  actual deliverable) — a sharper, more defensible standard of evidence
  than "this strategy mix tends to work well."

## Possible Follow-Up Contribution
A concrete, well-scoped, genuinely novel thesis contribution: **run a small
QCA analysis over this project's existing E1–E13 experiment configurations**
— code each configuration's key binary features (sanctioning present/absent,
communication present/absent, voluntary vs. imposed enforcement, imperfect
vs. perfect monitoring, etc.) as causal conditions, code "resource
sustained near `K/2`" as the outcome, and derive the minimal sufficient
combination(s). This is small enough in scope for a bachelor's thesis
(the method's computational core, per this chapter, is simple enough to
apply by hand or with a short script at this project's scale), and would be
a genuinely new, precisely-stated deliverable distinct from anything else
proposed in this literature review so far.

## Important Terms
- **Multiple conjunctural causation** — Ragin's term for causation that is
  both conjunctural (an outcome requires the intersection/AND of several
  conditions) and multiple (several different such intersections can each
  independently/sufficiently produce the outcome); the paper's central
  concept and this project's closest match for its own "several strategy
  mixes reach a good outcome" claim.
  - Note: **not the same claim as von Bertalanffy's equifinality** ([note](1968-bertalanffy-general-system-theory.md))
    — Ragin's multiplicity is over *causal condition-combinations*,
    von Bertalanffy's is over *initial conditions under fixed dynamics*;
    worth keeping these two precisely distinct if both are cited.
- **Case-oriented vs. variable-oriented strategy** — Ragin's own dichotomy
  for the two dominant pre-existing methodological traditions in
  comparative social science, both shown to handle multiple conjunctural
  causation poorly for different reasons.
- **Truth table** — a table with `2^k` rows (one per logically possible
  combination of `k` binary conditions), each assigned an outcome value;
  the QCA method's basic data structure.
- **Boolean minimization / prime implicant** — the procedure and its
  output: the logically simplest set of condition-combinations ("prime
  implicants") that together account for every case with the outcome of
  interest, derived by repeatedly dropping conditions shown irrelevant by
  a pairwise, one-condition-at-a-time comparison (explicitly analogous to
  holding all-but-one condition constant in an experiment).
- **INUS condition** (not covered in the read portion but standard QCA
  vocabulary from later chapters/literature building on this book) — an
  **I**nsufficient but **N**ecessary part of a condition that is itself
  **U**nnecessary but **S**ufficient for the outcome; worth confirming
  against Chapter 7 if this project pursues the QCA follow-up above.

## Questions
- Is it worth reading Chapter 7 ("Extensions of Boolean Methods") before
  attempting the QCA follow-up above, specifically for its treatment of
  contradictory rows and "limited diversity" (both flagged as unresolved
  in the portion read here) — likely yes, given both problems are close to
  certain to arise with this project's own, still-modest number of
  experiment configurations?
- Should this project's equifinality claim be reframed, in QCA vocabulary,
  as "multiple conjunctural causation" rather than (or alongside) "many
  paths to the optimum" — given the former is a more precise, established,
  citable term with a matching formal method attached?
- Is Miller's specific criticism (that Ragin overstates log-linear
  analysis's inability to handle interaction) load-bearing for anything
  this project would claim, or is it a dispute internal to 1980s
  methodology debates that doesn't affect QCA's usefulness here?
