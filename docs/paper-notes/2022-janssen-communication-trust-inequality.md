# An Agent-Based Model of the Interaction Between Inequality, Trust, and Communication in Common Pool Experiments

Read status: 🟢 noted from the published article (JASSS, open access). Full-text
re-read recommended before citing specific tables/figures.

## Citation
Janssen, M. A., DeCaro, D. A., & Lee, A. (2022). An agent-based model of the
interaction between inequality, trust, and communication in common pool experiments.
*Journal of Artificial Societies and Social Simulation (JASSS)*, 25(4), 3.
https://doi.org/10.18564/jasss.4922

## Research Problem
*Why* does communication improve cooperation in CPR settings, given that it is
"cheap talk" with no enforcement? The paper models the mechanism as communication →
trust → restraint, and tests it against experimental data.

## Why the Problem Is Difficult
Communication has no direct material effect; its influence is mediated by
psychological state (trust) and perceived fairness (inequality of harvest), which
interact dynamically over rounds. Capturing that requires heterogeneous agents and
fitting to real experimental trajectories.

## Proposed Method
A spatial ABM (26×26 grid, mobile agents harvesting tokens) fit to lab experiments.
Trust modulates behaviour: harvesting probability `p_h·(1 − α_h·T)` and movement
speed both *decrease* with trust `T`. Communication (allowed only before certain
rounds) is modelled as a *trust boost*. A genetic algorithm fits agent-type mix and
parameters to experimental data.

## Experimental Setup
Probabilistic logistic-style regrowth (empty cell regrows with probability
proportional to green neighbours). Communication before rounds 4–6 only. Fit measured
on both tokens-harvested-per-round and resource-level trajectories.

## Metrics
Resource pool size per round; tokens harvested; harvest rate; **Gini coefficient**
for income inequality; relative harvest share; self-reported trust (7-point scale).

## Main Results
- Best fit (fitness 0.842) requires a **heterogeneous population: ~75% conditional
  cooperators, ~16% selfish, ~9% altruistic.**
- Conditional cooperators have a *low* baseline harvest probability (0.38) and high
  trust-sensitivity (α_h = 0.93) — they conserve and respond strongly to others.
- Communication raised trust and produced sustained cooperation that *persisted even
  after communication stopped* (rounds 7–9).
- Low relative earnings (unfair share) lowered trust; high group harvest + low
  inequality raised it.

## Limitations
The model does not mechanistically explain *how* communication changes trust (it is
imposed as a boost); assumes identical communication sensitivity across types;
representative-agent-type simplification.

## Future Work
Model heterogeneous communication effects across agent types; richer behavioural and
institutional foundations of self-governance.

## Relevance to This Project
- **Validates our fairness metric:** Gini is the standard inequality measure in this
  exact setting — good, keep it.
- **Validates adding a conditional cooperator:** it is the *dominant* realistic agent
  type (≈75%), not a niche add-on. Strong support for our planned third strategy.
- **Gives a concrete communication design for Phase 2:** model communication as a
  *trust/reputation* state that raises restraint, rather than as literal message
  passing of numbers. This is simpler and evidence-based.
- Heterogeneous populations (mixes of types) are the norm — our `mixed_*` configs are
  on the right track; we should sweep the mix ratio.

## Possible Follow-Up Contribution
A minimal, non-spatial version of the trust-mediated conditional cooperator: an agent
that restrains more when it recently received a fair share and others restrained.
Compare cooperation/collapse/Gini against our baselines, then add a communication
"trust boost" and measure the effect — directly addressing RQ-A.

## Important Terms
Conditional cooperator; cheap talk; trust; reciprocity; relative harvest; genetic-
algorithm model fitting; heterogeneous agent population.

## Questions
- Is a non-spatial trust update enough to reproduce the qualitative effect, or does
  space matter? (We are non-spatial by design — worth checking the dependence.)
- How is trust initialised and decayed between rounds?
