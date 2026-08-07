# Some Aspects of the Dynamics of Populations Important to the Management of the Commercial Marine Fisheries

Read status: 🟢 read from the PDF.

## Citation
Schaefer, M. B. (1954). Some aspects of the dynamics of populations important
to the management of the commercial marine fisheries. *Bulletin of the
Inter-American Tropical Tuna Commission*, 1(2), 27–56. (No DOI — pre-DOI era;
PDF hosted directly by IATTC.)

## Research Problem
Given that a fish population's own biology limits how the size of a fishery
can be managed, what is the *quantitative* relationship between fishing
intensity, population size, and sustainable catch — and can it be estimated
from ordinary commercial catch statistics (total catch, catch-per-unit-effort)
rather than requiring dedicated population surveys? Written explicitly as
groundwork for managing the tropical tuna fishery, where adequate stock data
did not yet exist.

## Why the Problem Is Difficult
Oceanic ecosystems are complex, and man's predation is only one of many
influences on a fish population — but it is the only one that can be
controlled. Existing biological "models" of fisheries were not, in Schaefer's
view, adequate for translating routine commercial statistics (catch,
catch-per-effort) into an estimate of *where a population sits relative to its
maximum sustainable catch*, which is the actionable question for management.
Getting this from data alone requires a *specified* mathematical form of
population growth, an estimate of the "catchability" relating effort to
mortality, and separating fishing-driven change from environmental noise — all
three are non-trivial.

## Proposed Method
Two linked models, building directly on Gordon's economic framing but adding
an explicit biological growth law:

1. **Logistic population growth** (p. 29): `dP/dt = f(P)`, specialised to the
   **Verhulst–Pearl logistic**: `dP/dt = k₁P(L − P)`, where `L` is the maximum
   population the environment can support (**this project's `K`**) and `k₁` a
   constant (**this project's `g`**, up to a scale factor). `f(P)` is a
   parabola in `P`, symmetric about `P = L/2` — **this is the actual source of
   the "growth peaks at half of carrying capacity" fact this project's
   regeneration rule encodes**; Gordon's 1954 paper (read first;
   [note](1954-gordon-common-property-fishery.md)) does **not** use this curve
   at all.
2. **Effects of fishing**: `dP/dt = f(P) − Pφ(F)`, with catch rate assumed
   proportional to effort × population, `φ(F) = k₂F`. At equilibrium
   (`dP/dt=0`), the **equilibrium catch** = `f(P)` — the sustainable harvest at
   that population. Because `f(P)` is a parabola, there is exactly one
   population level maximising it: Schaefer names this the **maximum
   equilibrium catch** (his preferred term over "optimum catch," which he
   flags as ambiguous — see Limitations) — for the pure logistic this occurs
   at `P = L/2`, giving `MSY = k₁L²/4` (**this project's `MSY = gK/4`**).
3. **The joint bio-*economic* system** (§"Stabilization of an unregulated
   fishery," pp. 38–42): couples the logistic with a *second* differential
   equation for fishing effort growth, `dF/dt = k₃F(P − b)`, where `b` is the
   "economically critical population level" (effort grows when `P > b`, i.e.
   when fishing is still profitable, shrinks when `P < b`) — structurally
   identical to a Lotka–Volterra predator–prey pair, and Schaefer cites Lotka
   (1925) and Volterra & D'Ancona (1935) directly for the stability analysis.

## Experimental Setup
Not a designed experiment — a method paper, validated by fitting the model to
two real, extended commercial-fishery datasets: Pacific halibut off the
Canada/US coast (catch and catch-per-skate, 1916–1947, with independent
mortality-rate estimates from 1926 tagging studies) and California
sardine/Pacific pilchard (catch and catch-per-boat-month, 1934–1950, with
mortality estimated from 1936–1943 tagging).

## Metrics
**Maximum equilibrium catch** — Schaefer's preferred term (over "optimum
catch") for the largest *sustainable* harvest, i.e. the peak of `f(P)`.
Estimated from data via `f̄(P) = k₂F̄t·P̄` (mean population from
catch-per-effort, calibrated by an independently-estimated catchability
constant `1/k₂` from tagging-derived mortality rates) — a method for turning
ordinary catch/effort statistics into population estimates without a direct
stock survey.

## Main Results
- **Pacific halibut**: fitting the logistic to 1916–1947 data (using a
  47%-annual-mortality tagging estimate from 1926) gives maximum equilibrium
  catch **28.25 million lb** at a catch rate of **78.05 lb/skate**,
  corresponding to a population of roughly **62 million lb** — with the
  explicit caveat that since no data exist above this population level, the
  *true* maximum could be higher. An alternative fit anchoring the un-fished
  population to early-1900s catch rates (275 lb/skate) instead gives **36.9
  million lb** at population ~137.5 lb/skate — Schaefer is explicit that the
  two answers diverge because of missing high-population data, not because
  the method is unreliable low-population.
- **California sardine**: `f̄(P) = 1.253·U·(1385 − U)`, giving a maximum
  equilibrium catch of **~601,000 tons/year** at a population of **~1.52
  million tons** (692 tons/boat-month) — with an acknowledged mid-series
  anomaly (1938–1942) attributable to unusually strong recruitment year
  classes plus wartime disruption, not fishing alone — an explicit, honest
  case where the clean model does not fit and *environmental* variance is
  invoked rather than forced into the fishing-effort explanation.
- **The joint bio-economic system generically produces damped oscillations,
  not smooth convergence.** Using Lotka's stability discriminant, Schaefer
  shows the system's characteristic roots are complex whenever `(L−b)` and
  `(L−P)` are positive (i.e. essentially always, in the realistic region) —
  so a developing fishery is *predicted* to overshoot: catch rises well above
  both its eventual stable level and the maximum equilibrium catch, then
  fluctuates with shrinking amplitude toward the stable point `P = b` (Figs.
  3–7). Real halibut and sardine data are checked against this qualitative
  prediction and judged consistent (data points fall to the expected side of
  the "line of equilibrium conditions" during observed population
  increase/decrease phases).
- **Explicit policy warning**: "During the development of a fishery, it is to
  be expected that... the catch will rise for a short time well above the
  level at which it will reach natural stable equilibrium, and also well
  above the maximum equilibrium catch. The task which conservationists have
  sometimes set themselves of restoring a fishery to the highest historical
  levels of production is, in this event, unobtainable on a permanent basis"
  (p. 47).

## Limitations
- Explicitly flags "optimum catch" as an ambiguous, contested term and
  deliberately avoids it in favour of the more precise "maximum equilibrium
  catch" — but this is a *biological/physical* optimum, not an *economic*
  one; Schaefer does not himself re-derive Gordon's cost-aware optimum here
  (see Relevance, below).
- Acknowledges the logistic curve is likely **not exactly symmetric** for
  real fish populations (peak growth may occur below `L/2`), citing
  contemporary yeast-population evidence for asymmetric analogues — flagged
  as a modelling simplification, not asserted as biological fact.
- The joint bio-economic model assumes a **constant** economically-critical
  level `b` — explicitly noted as valid only "over a relatively limited time,"
  since `b` depends on technology and the business cycle, both of which
  drift.
- Both worked examples are hampered by absent data at high population levels
  (near-virgin stock), which Schaefer repeatedly flags as the single biggest
  limitation on the precision of the fitted maximum.
- Environmental variation is treated as an independent random variable, not
  modelled — acknowledged directly as "a bold attempt" in the sardine case,
  where 1938–1942 data visibly breaks the fishing-only story.

## Future Work
Calls explicitly for: longer catch/effort time series starting earlier in a
fishery's development (to pin down the near-virgin population and hence the
true maximum); mortality-rate ("`k₂`") estimates at more than one population
level to check the model's adequacy directly; and — the paper's own stated
next step — applying the same method to the tropical tuna fishery once
comparable catch/effort/mortality data exist.

## Relevance to This Project
- **This is the actual source of this project's regeneration rule and its
  `K/2`, `MSY=gK/4` reference points** — not Gordon (1954). Read together, the
  "Gordon–Schaefer model" is genuinely a *synthesis* of two independent 1954
  papers: Schaefer supplies the logistic growth curve and the *maximum
  equilibrium catch* concept (a biological/physical optimum); Gordon supplies
  the economic argument for why *actually achieving* that catch under open
  access is impossible, and why the true cost-aware economic optimum sits
  *above* `K/2` (fewer fish taken, more left standing), not at it.
- **A precise, useful correction for this project's own model documentation**:
  this project's `cooperative`/`sanctioning` strategies target `R=K/2` exactly
  — i.e. **Schaefer's biological MSY benchmark**, not Gordon's economic
  optimum. That's a defensible simplification (there is no explicit "cost of
  harvesting effort" parameter in this project's agents, only `monitoring_cost`
  for sanctioning specifically), but it should be named as such rather than
  implied to be "the" economically optimal target — the classical bioeconomic
  literature's actual optimum is more conservative than what this project
  currently calls "sustainable."
- **The damped-oscillation / overshoot result is a genuinely new, borrowable
  idea for the disturbance/resilience phase (E8–E10) or a future experiment**:
  Schaefer's own model *predicts* that even a well-behaved, unregulated
  fishery should overshoot and oscillate before settling — the "any one
  monitor enforces fully" and other idealisations in this project's engine
  currently produce clean, non-oscillatory convergence to `K/2` wherever
  sustained. Whether that's a meaningful difference (a simplification worth
  flagging) or irrelevant to the questions this project asks is worth a
  one-line note in `architecture.md`'s "known simplifications."
- **Directly strengthens the "is this arbitrary" answer already built into
  thesis-direction-equifinality.md**: not only are `K`, `g`, `MSY` standard,
  the *specific* choice to treat `K/2` as "the" sustainable target (rather
  than a more conservative, cost-aware level) is now traceable to a specific,
  known simplification relative to the 70-year-old literature, not an
  arbitrary round number.

## Possible Follow-Up Contribution
A small, cheap addition: report, for any experiment, whether the achieved
trajectory shows Schaefer-style overshoot-then-damp behaviour (it currently
should not, given the engine's mechanics) — useful as a one-paragraph
"how our idealised model differs from the classical bioeconomic prediction"
note for the thesis's model-limitations section.

## Important Terms
- **Verhulst–Pearl logistic** — `dP/dt = k₁P(L−P)`; this project's
  `dR = g·R·(1−R/K)` is this equation under a different symbol convention.
- **Maximum equilibrium catch** — Schaefer's preferred term for the peak of
  the sustainable-catch curve (the biological/physical optimum); deliberately
  distinguished from the ambiguous "optimum catch."
- **Economically critical population level (`b`)** — the population at which
  further fishing investment stops being profitable (Schaefer's own version
  of Gordon's open-access equilibrium condition), the attractor of the joint
  bio-economic system.
- **Catch per unit effort (`U`)** — the standard fisheries-science proxy for
  population size, `U = k₂·P̄`; the whole empirical method rests on
  estimating `k₂` (catchability) independently, usually from tagging data.
- **Damped vs. undamped oscillation (Lotka's discriminant)** — whether the
  joint population/effort system spirals into stable equilibrium or cycles
  forever; determined by the sign of a discriminant built from `k₁, k₂, k₃,
  b, L`.

## Questions
- Is it worth citing *both* Gordon and Schaefer together whenever this
  project references `K/2`/`MSY=gK/4`, rather than either alone, given the
  synthesis is genuinely a two-paper result?
- ~~Would it strengthen the thesis to explicitly state, once, that this
  project's "sustainable" target is Schaefer's biological MSY, not Gordon's
  economic optimum — and that the gap between them is itself a (currently
  unmodelled) cost-of-effort question?~~ — **Resolved via Clark (1976;
  [note](1976-clark-mathematical-bioeconomics.md))**: the exact gap is
  `z*−z_MSY = ½·z∞` (zero-discount case), where `z∞` is the open-access
  rent-dissipation level — worth stating this precise formula, not just the
  qualitative gap, in the thesis.
- Is the damped-oscillation prediction worth testing as a cheap diagnostic
  on existing E1–E13 trajectories, or is it out of scope given this project's
  agents don't have the effort-entry dynamics (`dF/dt`) that produce it in
  Schaefer's model?
