# GLUE: 20 Years On

## Citation
Beven, K., & Binley, A. (2014). GLUE: 20 years on. *Hydrological
Processes*, 28(24), 5897–5918. (Received 19 April 2013; published online 5
November 2013; journal volume/issue dated 2014.) DOI: 10.1002/hyp.10082

## Research Problem
Twenty years after Beven & Binley (1992) introduced GLUE
([note](1992-beven-binley-glue.md)), was its central diagnosis — that
physically-based hydrological models routinely exhibit *equifinality*
because real-world error is not well captured by classical statistical
assumptions — actually right? Has the resulting "GLUE controversy" (GLUE
vs. formal Bayesian statistical inference) been resolved, and, revisiting
the original Gwy catchment case study with twenty years of extra compute
power and hindsight, does the original conclusion still hold up?

## Why the Problem Is Difficult
The paper's central technical argument is a distinction between **aleatory
error** (random, stationary variability that formal statistical likelihood
functions are built to handle) and **epistemic error** (error from a lack
of knowledge — non-random, transitory, non-stationary, arising from model
structural simplification, poorly known input fields, and observation
data that are themselves virtual/uncertain rather than "true" ground
truth). Real hydrological modelling errors are argued to be predominantly
epistemic, yet almost all formal Bayesian/statistical likelihood
approaches must assume an aleatory error structure to remain analytically
tractable. Treating epistemic error as if it were aleatory **overestimates
the information content of the data** and "overstretches" the likelihood
surface: because a formal likelihood multiplies contributions across
every time step (`L ∝ (σ²ε)^(−Nt/2)`), even tiny differences in residual
variance between two similarly-good models can translate into likelihoods
differing by many orders of magnitude, producing an illusion of sharp,
confident parameter identification that the underlying data quality does
not actually support (severe **overconditioning**). Compounding this,
there is no way to independently separate the four entangled error
sources (model structure, parameters, input data, observations) without
extra information that is essentially never available — for genuinely
epistemic reasons, not just present carelessness.

## Proposed Method
Rather than a single new method, the paper (a) formalizes the
aleatory/epistemic distinction as the theoretical core of the GLUE
controversy, (b) reviews and responds to the criticism that GLUE's
informal likelihoods are merely "a poor approximation to formal Bayesian
methods" (Mantovan & Todini, 2006; Beven et al., 2008 respond that formal
Bayesian methods fare no better once real, non-ideal error structures are
considered), and (c) foregrounds a refinement developed since 1992: the
**limits-of-acceptability approach** (from Beven's 2006 "Manifesto for the
Equifinality Thesis"). Instead of deriving "behavioural" status from a
post-hoc, residual-based likelihood statistic fitted after the fact, this
approach sets **per-observation acceptance bounds *before* running any
model**, based on independent hydrological reasoning about observational,
input, and commensurability error (e.g. "discharge is only known to
within ±X%") — behavioural models are then simply those whose simulated
output falls within these pre-declared bounds for every observation. The
paper argues this is more objective than either an informal residual
likelihood or a formal statistical likelihood, because the acceptance
criterion is fixed independently of the model output distribution itself.
To test all this, the paper **revisits the original 1992 Gwy/IHDM4 case
study** with (i) 500,000 Monte Carlo realizations instead of 500, (ii)
three side-by-side likelihood measures (BB92-style inverse variance,
formal Gaussian likelihood, weighted least squares assuming 20%
measurement error; exact forms in their Table III), and (iii) a new
limits-of-acceptability evaluation using ±10% and ±20% bounds around each
observed discharge.

## Experimental Setup
Same catchment, model, and parameters as BB92: IHDM4 on the Gwy catchment,
Plynlimon; the same four parameters and prior ranges (`Ks`, `θs`, `ψin`,
`f`; Table II); four of the original storms, now given with their exact
characteristics (Table I: total rainfall 80.5–121.8 mm, peak flows
6.1–16.8 m³/s). The key change is scale: 500,000 realizations (vs. the
original 500), letting them properly resolve dotty plots and 3D likelihood
isosurfaces in the 4-parameter space (Figures 3 and 4) that were
uninterpretable at the 1992 sample size.

## Metrics
The same family of likelihood measures as BB92, now formally tabulated
side by side (Table III); a normalized misfit statistic against the new
limits-of-acceptability bounds (Figure 6); posterior parameter cumulative
distributions before/after each storm is added (Figure 5); the fraction of
time steps within a storm for which the best available model satisfies
the acceptance limits.

## Main Results
- **Sample size matters for structure, not for bounds**: going from 500 to
  500,000 realizations barely changes the estimated 5%/95% uncertainty
  bounds, but it is essential for resolving actual structure in parameter
  space — the 500-realization dotty plot shows no discernible pattern,
  while the 500,000-realization version reveals clear structure (Figure
  3), meaning the original 1992 sample was too sparse to properly support
  its own resampling/interpolation step.
- **Formal likelihood overconditions, visibly**: comparing posterior
  parameter distributions after just one storm (Figure 5), the formal
  Gaussian likelihood collapses onto a narrow parameter range almost
  immediately, while the informal BB92-style measure stays comparatively
  broad — direct empirical evidence for the paper's central theoretical
  claim that formal likelihoods overstretch given real, epistemic-error-
  dominated hydrological data.
- **Under the stricter, independently-set limits-of-acceptability
  criterion (±10%/±20% of observed discharge), the model is rejected
  outright**: none of the 500,000 realizations satisfy the limits of
  acceptability for *any* of the four storms, even though the same model
  looked reasonable under the older global efficiency-based GLUE
  evaluation. The single best realization achieves only 82% time-step
  compliance with the limits for storm 1.
- This rejection is explicitly framed as a **positive research outcome**:
  it demonstrates that global, residual-averaging likelihood measures can
  mask detailed, time-step-level model inadequacy that a more demanding,
  independently-specified criterion exposes — informative because it
  points toward what needs improving (model structure, or the input/
  observation data), rather than being hidden inside an artificially
  reassuring uncertainty band.
- An explicit **ethical caveat**: in a practical (non-research) decision-
  making context, discovering that all tried models should be rejected is
  not actionable in the same way — a practitioner may lack the time or
  data to improve the model, raising a genuine question about how far a
  rejected model should still be used for decisions.

## Limitations
- Twenty years on, the central subjectivity question is explicitly
  unresolved: there is still no principled answer to which likelihood
  measure — or which combination rule across observations — is "correct"
  under real epistemic uncertainty; the paper states this is inherent
  ("for good epistemic reasons"), not a gap still to be closed.
  Separating the four error sources independently remains acknowledged as
  essentially impossible without external information that is rarely
  available.
- The ±10%/±20% limits of acceptability used in the revisited case study
  are themselves somewhat provisional — the authors admit they lacked
  adequate independent knowledge of the actual input error for this
  catchment and chose "generous" round-number bounds rather than
  bounds derived from a rigorous independent error assessment.
- Rejecting all models tried is scientifically useful but is explicitly
  flagged as **not** a practically useful result when a real-world
  decision still has to be made on a deadline.
- The paper is honest that the GLUE-vs-formal-Bayesian debate is not
  resolved and, in the authors' own view, may have no resolution as long
  as epistemic uncertainty is present — GLUE's claimed advantage is being
  more transparent about that irreducibility, not eliminating it.

## Future Work
The closing "Next 20 Years" section names four concrete priorities: (1)
better methods to evaluate the real information content of hydrological
data series and reduce epistemic error in input/evaluation data —
treated as requiring as much domain (hydrological) reasoning as
statistical theory; (2) designing model-evaluation strategies and
likelihood measures that genuinely allow for model *rejection* when a
model is not fit-for-purpose, instead of silently compensating via an
aleatory error model; (3) resolving how likelihoods from different
observations/events should be combined — multiplicative/Bayes-style
(strong conditioning, but risks rejecting useful models over minor
discrepancies) vs. weighted addition (softer, but the paper does not
say which is right, only that the choice should reflect how much genuine
new information a period of data actually adds); (4) evaluating the
information content of calibration data independently of any particular
model being tested.

## Relevance to This Project
This retrospective sharpens, rather than simply reconfirms, the choice of
GLUE ([note](1992-beven-binley-glue.md)) as the methodological anchor for
this project's own equifinality question. Two refinements matter directly:

1. **The aleatory/epistemic distinction has an important disanalogy for
   this project that should be stated explicitly, not glossed over.** In
   hydrology, the "true" catchment behaviour is unobserved and all error
   sources (model, input, observation) are genuinely uncertain relative to
   an unknown ground truth. In this project, the simulation model itself
   *is* the ground truth — there is no separate "real world" the model is
   being fit to. What plays the role of epistemic uncertainty here is
   narrower: stochastic elements internal to the model (e.g. loner-strategy
   noise, defector-scaled monitoring cost) and the arbitrariness of initial
   seeds/starting conditions, not unknown measurement error. Any use of
   GLUE-style language in the thesis should make this substitution
   explicit rather than borrowing the hydrology framing wholesale.
2. **The limits-of-acceptability refinement is a better fit than raw
   BB92-style informal-likelihood GLUE for this project's still-unbuilt
   E17 experiment.** Defining a fixed, independently justified acceptance
   criterion *before* running the sweep (e.g. "final resource must stay
   ≥ 50% of `K`", "no permanent collapse within `T` rounds") and then
   classifying strategy/starting-condition combinations as behavioural or
   not against that fixed bar is more defensible than fitting a likelihood
   post hoc and picking a threshold afterward — and it mirrors exactly the
   kind of pushback that led away from QCA's post-hoc crisp thresholds in
   this project's own methodological discussion. It also legitimizes
   reporting a **negative** E17 result (e.g. "no strategy mix recovers from
   a sufficiently catastrophic start") as a genuine, positive finding
   rather than something to explain away, directly following this paper's
   own framing of model rejection as informative.

## Possible Follow-Up Contribution
Implement E17 using the limits-of-acceptability refinement specifically:
fix acceptance thresholds for "recovery" independently and in advance
(e.g. final resource ≥ some fraction of `K` within a fixed round budget,
combined with a no-permanent-collapse condition), then run a full-
factorial or Monte Carlo sweep over starting resource levels (including
catastrophic lows) and strategy mixes, classify each run as
behavioural/non-behavioural against the fixed thresholds, and report which
combinations are behavioural — a direct analogue of this paper's Figure 6
per-storm compliance analysis, applied to CPR recovery instead of
discharge prediction. Bachelor-feasible: this is purely an analysis layer
over the existing engine, and, unlike BB92's 30–60-hour storm runs, the
simulation here is cheap enough to run the full sweep many times over.

## Important Terms
- **Aleatory vs. epistemic error/uncertainty** — random/stationary
  variability vs. error from lack of knowledge (non-random, non-
  stationary, structural); the paper's central theoretical distinction,
  underlying why formal statistical likelihoods overcondition real
  hydrological data.
- **Limits of acceptability** — an a priori, per-observation acceptance
  bound set independently of any model run, used to classify behavioural
  models; introduced in Beven's (2006) "Manifesto for the Equifinality
  Thesis," discussed and applied here.
- **Overconditioning / stretching of the likelihood surface** — the effect
  by which a formal (aleatory-assuming) likelihood function makes
  near-equally-good models look enormously different in likelihood,
  producing artificially narrow, overconfident uncertainty bounds.
- **Type I / Type II / Type III error (Beven's usage)** — Type I: failing
  to reject a model that is not actually fit for purpose (because
  epistemic error in the data masked its unfitness); Type II: rejecting a
  model that would actually have been useful (because it was evaluated
  against epistemically flawed forcing/observation data); Type III:
  errors arising specifically from uncertain model inputs interacting with
  the identification of "behavioural" status.
- **GLUE controversy** — the ongoing (unresolved, per this paper) debate
  over whether GLUE's informal, subjective likelihood measures are a
  legitimate alternative to formal Bayesian statistical inference, or
  merely a poorly justified approximation to it.

## Questions
- Should Beven's (2006) "A manifesto for the equifinality thesis" — the
  primary source for the limits-of-acceptability refinement repeatedly
  cited here — be read directly before implementing E17, rather than
  relying on this paper's secondary description of it?
- Given this project's simulation is cheap to run at scale (unlike 1980s/
  2010s hydrological models), should E17 use a full-factorial sweep rather
  than Monte Carlo sampling, sidestepping the sample-size-adequacy problem
  this paper found in the original 500-realization BB92 study?
- How should the project set its own "limits of acceptability" thresholds
  in a way that is genuinely independent and defensible, rather than
  picked to produce a convenient result — analogous to this paper's own
  admission that its ±10%/±20% bounds were "generous" rather than derived
  from rigorous independent error estimation?
- Does the aleatory/epistemic distinction, reframed for a model that *is*
  its own ground truth (see Relevance section above), still add
  explanatory value to the thesis, or is it better left out in favour of
  a simpler framing specific to simulation stochasticity and initial
  conditions?
