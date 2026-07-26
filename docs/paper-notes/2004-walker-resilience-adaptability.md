Read status: 🟢 read from the PDF.

# Resilience, Adaptability and Transformability in Social–ecological Systems

## Citation

Walker, B., C. S. Holling, S. R. Carpenter, and A. Kinzig. 2004. "Resilience,
Adaptability and Transformability in Social–ecological Systems." *Ecology and
Society* 9(2): 5. [online] URL: http://www.ecologyandsociety.org/vol9/iss2/art5

Article type: "Perspective." Author affiliations: CSIRO Sustainable Ecosystems
(Walker); University of Wisconsin-Madison (Carpenter); Arizona State University
(Kinzig). Verified against the PDF masthead and abstract.

## Research Problem

The concept of *resilience* (from Holling 1973) has fragmented into many
conflicting interpretations, and this ambiguity undermines its usefulness for
sustainability science. The paper's problem is definitional and diagnostic, not
empirical: to give precise, mutually consistent definitions of three attributes
that jointly govern the trajectory of a social–ecological system (SES) —
**resilience, adaptability, transformability** — and to show how they interact.
The authors are explicit that there is "little fundamentally new theory" here;
the contribution is conceptual clarification built on existing nonlinear-stability
theory (Levin 1999, Scheffer et al. 2001, Gunderson & Holling 2002). The intended
payoff is a shift in sustainability science away from the maximum-sustainable-yield
(MSY) paradigm of seeking optimal states, toward resilience analysis, adaptive
management, and adaptive governance.

## Key Concepts

**Resilience** — "the capacity of a system to absorb disturbance and reorganize
while undergoing change so as to still retain essentially the same function,
structure, identity, and feedbacks." In the refined (basin-of-attraction)
definition: to *stay in the same basin of attraction*. The authors distinguish
this from "engineering resilience" (Holling 1996), i.e. speed of return to
equilibrium (Pimm 1991) — return time is explicitly rejected as *the* measure of
resilience, because with multiple stable states it fails to capture the ways a
system can permanently or temporarily lose essential functions.

**Adaptability** — "the capacity of actors in a system to influence resilience";
in a SES this is essentially the collective capacity of human actors to *manage*
resilience. It operates through the four aspects below: actors can move thresholds
relative to the current state (aspect 1), move the current state relative to a
threshold (aspect 3), make a threshold harder/easier to reach (aspect 2), or manage
cross-scale interactions (aspect 4).

**Transformability** — "the capacity to create a fundamentally new system when
ecological, economic, or social (including political) conditions make the existing
system untenable." It means defining/creating a *new stability landscape* by
introducing new state variables (and often a new scale). Distinct from resilience
and adaptability, which concern the dynamics of a *given* system; transformability
fundamentally alters the system's nature. Example: SE Zimbabwe's shift from cattle
ranches to collectively managed wildlife "conservancies" after a 1980s drought.

The four crucial aspects of resilience (portrayed via the stability-landscape
metaphor; the first three shown as L, R, Pr in Fig. 1a):

- **Latitude (L)** — "the maximum amount a system can be changed before losing its
  ability to recover (before crossing a threshold which, if breached, makes recovery
  difficult or impossible)." In landscape terms: *the width of the basin of
  attraction*. Wide basins → more system states reachable without crossing a
  threshold.
- **Resistance (R)** — "the ease or difficulty of changing the system; how
  'resistant' it is to being changed." In landscape terms: the *depth / steepness of
  the basin*. Deep basins (more precisely, higher **R:L ratios**) mean greater
  forces/perturbations are needed to move the state away from the attractor.
- **Precariousness (Pr)** — "how close the current state of the system is to a limit
  or 'threshold'" (refined definition adds: and the current *trajectory* of the
  system). It is a property of the *current position within the basin relative to the
  edge*, not of the landscape's shape.
- **Panarchy (Pa)** — the cross-scale aspect: "because of cross-scale interactions,
  the resilience of a system at a particular focal scale will depend on the
  influences from states and dynamics at scales above and below." External politics,
  invasions, market shifts, or climate change (coarser scales) reshape the local
  stability landscape or perturb it directly (finer scales), thereby influencing L,
  R, and Pr. Unlike the first three, panarchy is inherently *multi-scale* and cannot
  be assessed at a single scale.

Supporting machinery: **adaptive cycle** (r → K → Ω → α; a predictable "forward
loop" of growth/conservation and an unpredictable "backloop" of release/
reorganization); **state space / basin of attraction / stability landscape**
(basins are regions the system tends to remain in; the landscape is the set of
basins and the thresholds between them). A system can change basins either by the
*state crossing a threshold* or by a *threshold moving across the state* (Fig. 1b).

## Main Contribution

A coherent, internally consistent conceptual vocabulary that (1) decomposes
resilience into four assessable aspects (L, R, Pr, Pa) grounded in the stability-
landscape metaphor; (2) cleanly separates resilience/adaptability (dynamics within
a system) from transformability (creating a new system with new state variables);
and (3) reframes management as acting on these aspects — moving thresholds,
reshaping basin depth, steering the current state, or managing cross-scale effects.
The framework's headline implication is a paradigm shift from MSY/optimal-state
thinking to resilience analysis plus adaptive management and adaptive governance.
Notably, the authors argue resilience is *not always desirable*: an undesirable
basin can be too resilient, and the management goal is then to *reduce* its
resilience.

## Limitations

Stated by the authors:
- The concepts are "by their nature rather imprecise" — in the same category as
  "justice" or "wellbeing"; overly narrow definitions would be counterproductive.
- The stability landscape is only a *metaphor*. Not all systems can be adequately
  described by one, especially coupled social-ecological systems across multiple
  scales; few "lend themselves to the formal representation... required to accurately
  measure P, L, and R."
- The authors explicitly *do not advocate separate measurement* of L, R, Pr —
  because of their interdependencies (in evolved systems the three co-develop, e.g.
  body temperature: very precarious yet strongly resistant). They endorse only
  *qualitative* assessment.
- Some regime shifts are not point-attractor-to-point-attractor (e.g. stable limit
  cycles); the metaphor is stretched though "the general concepts would still apply."

Unstated / from a modeling standpoint:
- No formal operationalization, no equations, no metrics — nothing directly
  measurable is defined. This is a conceptual perspective, not a method.
- No empirical validation; examples (Everglades, lakes, Zimbabwe rangelands) are
  illustrative diagnoses, not tests.
- The resilience/transformability boundary ("closely related" vs. "fundamentally
  altered") is admitted to be "fuzzy and subject to interpretation."

## Relevance to This Project

This paper is the conceptual anchor for **Phase 3** (disturbances + resilience
measurement), which is not yet built. Our reproducible agent-based CPR simulation
already contains the structure the paper describes qualitatively — and, crucially,
it lets us do the *quantitative* operationalization the authors declined to attempt.

Mapping onto our model:
- Our resource stock is a **state variable**; under logistic growth with a collapse
  threshold, the phase line has (at least) two basins: a viable/recovering basin and
  an **absorbing basin at stock = 0** (a stock driven to 0 cannot recover). This is a
  literal, computable stability landscape — the metaphor the paper could only sketch.
- We can therefore report L, R, Pr as *numbers*, not just qualitative assessments,
  turning Walker et al.'s framework into concrete Phase-3 metrics (see mapping
  below). This is a genuine niche: the paper says formal measurement is rarely
  feasible; a controlled simulation makes it feasible.
- The paper's warning that resilience ≠ good, and that engineering resilience
  (return time) is only one aspect, tells us **not** to reduce our resilience metric
  to recovery speed alone. We should report multiple aspects (distance to threshold,
  shock size absorbed) rather than a single scalar.
- **Panarchy** is the least applicable aspect to a single-scale simulation. Honest
  scoping: if all agents draw from one shared pool at one scale, panarchy is largely
  out of range for us — unless Phase 3 introduces nested groups/sub-pools, in which
  case it becomes the natural extension.
- Transformability is likewise out of scope: our agents cannot introduce new state
  variables mid-run. Worth stating explicitly as a boundary of what we measure.

Concrete mapping of the four aspects to measurable quantities:

| Aspect | Paper's definition | Measurable proxy in our sim |
| --- | --- | --- |
| **Latitude (L)** | width of the basin; max change before recovery is lost | size of the set of stock states from which the pool still recovers — i.e. the distance from the current/operating stock down to the collapse threshold (the recoverable range) |
| **Resistance (R)** | depth/steepness of the basin; force needed to move the state | magnitude of extraction/perturbation pressure required to push the stock a given distance (basin "steepness"); operationally, how hard a sustained over-extraction rate must be to displace the stock — report as an **R:L ratio** as the paper recommends |
| **Precariousness (Pr)** | how close the current state is to the threshold (+ trajectory) | **distance from current stock to the collapse threshold**, plus the sign/slope of dStock/dt (is it trending toward the threshold?) — the single cleanest metric we can compute each round |
| **Panarchy (Pa)** | influence of scales above/below | mostly N/A at one scale; only meaningful if Phase 3 adds nested sub-pools or groups — then: how sub-pool collapses propagate to the aggregate |

A clean, defensible Phase-3 design: apply a **shock** (a one-off extraction spike or
a drop in the growth rate), then measure (a) **Pr** = distance to threshold before/
after, (b) **resistance/latitude** = the largest shock magnitude the system absorbs
without falling into the absorbing basin, and (c) **return time** as the *engineering*
resilience aspect only — kept separate and clearly labeled per the paper's caution.

## Important Terms

Candidates for `docs/terminology.md`:
- **Resilience** (ecological, basin-of-attraction sense) vs. **engineering
  resilience** (return time) — keep the distinction explicit.
- **Latitude / Resistance / Precariousness / Panarchy** — the four aspects, with our
  operational proxies.
- **Stability landscape**, **basin of attraction**, **attractor**, **state space**.
- **Threshold / regime shift** — and our **collapse threshold** as its concrete form.
- **Absorbing basin** (stock = 0, no recovery) — our term; note it as the
  degenerate/undesirable basin.
- **Adaptive cycle** (r, K, Ω, α; forward loop vs. backloop) — likely out of scope
  but worth a one-line definition.
- **Adaptability**, **transformability** — define, and mark which are in/out of scope
  for our single-scale model.

## Questions

- What growth model and collapse-threshold parameters make L and R cleanly separable
  in our sim, so the R:L ratio is meaningful rather than degenerate?
- How do we define a "shock" precisely for Phase 3 (extraction spike vs. growth-rate
  drop vs. stock haircut), and does the choice change which aspect (R vs. L) it
  probes?
- Should precariousness be a single instantaneous distance, or a trajectory-aware
  measure (distance + trend), as the refined definition suggests?
- Is panarchy worth engineering into the model (nested sub-pools) for a bachelor
  thesis, or is it cleaner to scope it out and say so?
- The paper insists L/R/Pr should *not* be measured separately due to
  interdependence. In a controlled sim we *can* separate them — is that a feature
  (our contribution) or does the interdependence reappear as a confound we must
  report? Read next: Scheffer et al. 2001 (catastrophic shifts) and Carpenter 2003
  (regime shifts in lakes) for the formal dynamics behind the metaphor.
