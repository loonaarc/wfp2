# The Economic Theory of a Common-Property Resource: The Fishery

Read status: 🟢 read from the PDF.

## Citation
Gordon, H. S. (1954). The economic theory of a common-property resource: The
fishery. *Journal of Political Economy*, 62(2), 124–142.
https://doi.org/10.1086/257497

## Research Problem
Why does the fishing industry, despite exploiting "the richest and most
indestructible" resource available to man, leave fishermen poor and yield no
economic rent? Gordon's claim: "overfishing," "depletion," and "conservation"
problems are not primarily biological — they are the predictable economic
consequence of the fishery's **common-property** nature. He sets out to build
the economic theory that fisheries biology, up to 1954, had never supplied.

## Why the Problem Is Difficult
Fisheries biology had extensively studied population dynamics but treated the
fisherman as *exogenous* — "the activities of man are themselves not regarded
as behaviorized or determined by the other elements of a system of mutual
interdependence" (p. 136). Biological "fisheries management" targeted the
**maximum sustained physical yield**, silently equating "more fish caught"
with "better," ignoring input costs entirely — Gordon calls this the
"new theory" that "comes very little closer to treating the fisheries problem
as one of human utilization of natural resources than did the older, more
primitive theories" (p. 128). Compounding this, the standard economic tool for
a stable optimum — the law of diminishing returns — does not obviously apply
to fisheries (no "cultivation" analogous to the fourth harrowing being less
useful than the third); Gordon has to argue at length (§IV) that it is
specifically **fishing's effect on the fish population itself** that supplies
the needed nonlinearity, not diminishing returns to effort.

## Proposed Method
Two linked models:

1. **Rent dissipation under open access** (§III, Figs. 1–2): defines the
   economic optimum as the effort level maximizing *net* yield (total value of
   landings minus total cost), graphically distinct from and *less than* the
   effort that maximizes *gross* physical yield. Because no fisherman owns the
   water, competitive entry continues until the *average* productivity of
   effort falls to equal *average* cost — not marginal cost — dissipating the
   entire resource rent to zero. "Everybody's property is nobody's property."
2. **The "bionomic equilibrium" of the whole fishery** (§IV): a 4-variable,
   4-equation system — population `P`, landings `L`, effort `E`, cost `C`:
   `P = P(L)`, `L = L(P,E)`, `C = C(E)`, and the closing condition `C = L`
   (open access) or "maximize `L − C`" (sole ownership / optimum). Solved in
   closed form with **linear** functional forms:
   - `P = a − bL` — population is a linear function of cumulative landings;
     `a` = "natural population" (the un-fished equilibrium), `b` = the
     "depletion coefficient."
   - `L = cEP` — landings are proportional to effort × population; `c` = the
     "production coefficient" (catchability).
   - `C = qE`, with `q` normalised to 1 (effort measured in dollars).
   - Optimum effort: `E* = (√(ca) − 1) / (cb)`. Comparative statics: `∂E*/∂a
     > 0`, `∂E*/∂b < 0`, `∂E*/∂c` ambiguous.

   **Correction to note before this project cites Gordon for its own
   formulas:** this is *not* the logistic growth model `dR = gR(1−R/K)` this
   project uses, and Gordon never derives `R*=K/2` or `MSY=gK/4` — those
   specific closed forms belong to Schaefer (1954), the companion paper (see
   [its note](1954-schaefer-population-dynamics-fisheries.md)), not to Gordon.
   Gordon's own contribution is the **economic logic** (rent dissipation under
   open access; the optimum-effort/max-yield-effort distinction), independent
   of which growth curve is plugged in. Do not attribute the logistic curve to
   this paper.

## Experimental Setup
Not empirical — a theoretical/graphical-algebraic paper, illustrated with two
real-world regulatory case studies (Pacific halibut, Canadian Atlantic
lobster) and cross-domain analogies (petroleum unitization, medieval common
pasture "stinting," anthropological land-tenure evidence).

## Metrics
**Net economic yield** = total value of landings − total cost — Gordon's
central, and central *criticism* of the biological literature's metric,
**maximum sustained physical yield**, which he argues is the wrong target
because it is blind to cost.

## Main Results
- **Open-access equilibrium dissipates the entire resource rent.** Individual
  fishermen equate *average*, not marginal, productivity across grounds (a
  fisherman choosing where to fish cares about his own expected catch, not the
  marginal product to the fleet), driving competition until average
  productivity = average cost, i.e. zero economic profit anywhere.
- **The Pacific halibut case, quantified**: a fixed-catch-limit regime
  (US–Canada, early 1930s) produced measured stock recovery, but the season
  length collapsed from **more than 6 months in 1933** to **26 days in 1952**
  (60 days in the Alaska region) as fishermen raced to catch the quota with
  ever more, larger, faster boats — "a rise in the average cost of fishing
  effort, allowing no gap between average production and average cost to
  appear, and hence no rent" (p. 133). The regulation raised the gross catch
  ceiling but did **not** make fishermen better off, because it never touched
  open access to *entry*.
- **The Canadian lobster case**: similarly, seasonal closure alone produced
  "a steady growth in the number of lobster traps set by each fisherman,"
  such that (Gordon's conservative estimate) "the same quantity of lobsters
  could be caught with half the present number of traps" (p. 134) — pure
  effort-cost inflation, no rent gain, *unless* fishermen locally banded into
  an entry-restricting monopoly, which measurably worked.
- **Cross-domain corroboration**: petroleum common-pool drilling races,
  medieval manorial "stinting" of common pasture, and — notably —
  anthropological evidence that unrestricted common tenure was **historically
  rare even in hunting-gathering societies**; where it appears, it is
  specifically where the resource is too migratory to be "husbandable" at all
  (p. 134) — property/coordination institutions are the norm precisely
  *because* unmanaged common exploitation is destructive.

## Limitations
- Assumes linear cost and landings functions; explicitly discards the law of
  diminishing returns as the source of model stability (relies on
  population-reduction instead) — a considered, argued choice, but a
  simplification nonetheless.
- Single, non-migratory ("demersal") fishing ground; Gordon explicitly flags
  that migratory species are not formally covered by the method, only
  qualitatively.
- Aggregate, representative-fisherman treatment — no individual strategic
  behavior, no heterogeneity, no game theory of entry/exit.
- **Only two remedies are ever considered: private property, or public
  (government) control, "in either case subject to a unified directing
  power"** (p. 135). Gordon does not consider, or even gesture at, a
  self-governing/decentralized third option.

## Future Work
Not stated as a dedicated section (not the era's convention); the paper closes
on the algebraic derivation without an explicit research agenda.

## Relevance to This Project
- **This is the founding paper of bioeconomics**, and it does what the
  thesis-direction-equifinality note hoped: the "did economists already solve
  the single-planner case" question is answered concretely — yes, and the
  answer is rent dissipation under open access vs. an optimum that falls
  strictly below the biologically-maximal yield.
- **But the specific formulas this project already uses (`R*=K/2`,
  `MSY=gK/4`) are not from here** — see the correction above. Read Schaefer
  (1954) to confirm and properly attribute the logistic-growth half of the
  "Gordon–Schaefer model."
- **The sharpest, most useful finding for the "is this novel" question**:
  Gordon's own remedy set — private property *or* centralized government
  control — is exactly the false dichotomy Ostrom's *Governing the Commons*
  (1990; [note](1990-ostrom-governing-the-commons.md)) spends a book refuting.
  Gordon, writing in 1954, does not anticipate self-governance at all. That
  gap between Gordon's sole-owner optimum and a decentralized, heterogeneous,
  boundedly-rational multi-agent population (this project's actual subject)
  is precisely where the novelty has to live — stated in Gordon's own words,
  not asserted from outside.
- **A real-world empirical echo of this project's own E3 finding.** E3 shows
  sanctioning protects the resource but costs the sanctioner (the
  second-order free-rider gap, 105 vs. 125 net payoff). Gordon's halibut case
  is the same phenomenon in the field: a regulation that raises gross physical
  yield can still fail to raise *net* welfare, because the cost of achieving
  or complying with it eats the gain. Worth citing as real-world, non-lab
  corroboration of "gross ≠ net" mattering.
- **Gordon pre-dates and cleanly out-classes Hardin (1968).** The same
  tragedy-of-the-commons mechanism, derived 14 years earlier, purely from
  price theory, with none of Hardin's population/eugenics baggage
  ([note](1968-hardin-tragedy-of-the-commons.md)). Worth citing Gordon as the
  economically rigorous originator and Hardin as the (later, more famous, more
  contested) popularizer, if the thesis wants to distance the resource-economics
  argument from Hardin's other claims.

## Possible Follow-Up Contribution
None beyond what the project already is: Gordon's own 1954 remedy set stops at
"private property or centralized control." A systematic study of *which*
decentralized, heterogeneous strategy combinations recover Gordon's optimum
without either — this project's actual mechanism ladder (E1–E13) — is a
direct, literal extension of the gap this paper leaves open.

## Important Terms
- **Common-property resource** — Gordon's own term (distinct from, and
  earlier than, Hardin's "commons"): a resource not legally ownable by
  individuals, hence yielding no rent under free competitive access.
- **Economic rent** (here, resource/scarcity rent) — the surplus a resource
  could yield if its access were controlled; dissipated to zero under open
  access.
- **Bionomic equilibrium** — Gordon's term (building on Baranoff's
  "bio-economics") for the joint economic–biological steady state of a
  fishery.
- **Intensive margin vs. extensive margin** — effort allocated within one
  ground (intensive) vs. across grounds of differing quality (extensive); the
  mechanism by which competition dissipates rent even on the *best* grounds.
- **Natural population (`a`), depletion coefficient (`b`), production
  coefficient (`c`)** — Gordon's own parameters; do not conflate with this
  project's `K`, `g`, or with Schaefer's logistic terms.
- **Maximum sustained physical yield** vs. **optimum economic yield** — the
  paper's central distinction; the former (biologists' target) is always
  larger than the latter (the true, cost-aware optimum).

## Questions
- ~~Confirm with Schaefer (1954): is the logistic growth curve, and the
  `R=K/2`/`MSY=gK/4` closed form, actually first stated there~~ — **Resolved.**
  Confirmed via Schaefer (1954) directly, and given an exact closed form via
  Clark (1976; [note](1976-clark-mathematical-bioeconomics.md)): the true,
  fully-patient (zero-discount) economic optimum under the Schaefer
  functional form is `z*=½(1+z∞)`, where `z∞∈(0,1)` is the open-access
  rent-dissipation level — **strictly above** the MSY level `z=0.5` whenever
  fishing costs are positive. This project's `R=K/2` benchmark is the
  biological MSY point, not the true economic optimum; the gap between them
  is exactly `½·z∞`, governed by the cost/price ratio this project's engine
  does not model.
- Does this project's `selfish` baseline reproduce Gordon's specific
  open-access mechanism (average productivity = average cost) numerically, or
  only the qualitative collapse? Worth a direct check.
- Is it worth citing Gordon's halibut/lobster field evidence in the thesis as
  a real-world analog to E3's second-order free-rider cost gap, alongside the
  existing lab-experiment citations (Fehr & Gächter, Ostrom/Walker/Gardner)?
