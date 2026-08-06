# An Agent-Based Model of the Interaction between Inequality, Trust, and
Communication in Common Pool Experiments

Read status: 🟢 read from the PDF (`references/papers/janssen2022.pdf`).

## Citation
Janssen, M. A., DeCaro, D. A., & Lee, A. (2022). An agent-based model of the
interaction between inequality, trust, and communication in common pool experiments.
*Journal of Artificial Societies and Social Simulation (JASSS)*, 25(4), 3.
https://doi.org/10.18564/jasss.4922

## Research Problem
*Why* does communication ("cheap talk", no enforcement power) improve cooperation in
CPR settings? The paper builds an ABM to explain — not just replicate — the dynamic,
round-by-round mechanism behind a prior lab experiment (DeCaro et al. 2021, 41
four-person groups) that measured self-reported trust before and after communication,
but never connected trust to *round-by-round* behaviour. This paper is that missing
dynamic link.

## Why the Problem Is Difficult
Communication has no direct material payoff effect ("cheap talk"), so its influence
must be mediated by something psychological. The lab data suggests *trust*, shaped by
both communication and *observed inequality* (how fairly the group is currently
sharing the resource), but disentangling that dynamic loop — trust affects harvesting
behaviour, harvesting behaviour changes inequality, inequality feeds back into trust,
repeated every round — is not observable directly from aggregate experimental data,
which is why a mechanistic, individual-level simulation is needed.

## Proposed Method
A spatially explicit ABM, calibrated (not hand-tuned) to reproduce **five specific
qualitative patterns** from the lab data via a genetic algorithm.

**Environment:** 26×26 grid, 169 cells (25%) seeded with resource tokens. An empty
cell regrows with probability `p·n_t/N` (`n_t` = number of neighbouring cells with a
token, `N=8`, `p=0.01`) — fastest regrowth in a checkerboard pattern (each token
surrounded by empty cells). 9 rounds of 4 simulated minutes; rounds 1–3 and 7–9 have
no communication, rounds 4–6 do.

**Agent decision loop**, three linked equations:
- **Harvest probability**, conditional on trust `T`: `p_h* = p_h(1 − α_h·T)` — higher
  trust *lowers* the chance of taking an available token (restraint).
- **Trust update** (once per second): `T_t,i = T_{t-1} − (τ/(N−1))·Σ_j|x_i − x_j| +
  θ(1 − T_{t-1})` — the first term is inequality aversion (`τ`: how much the agent's
  trust erodes per unit of observed harvest-inequality with the rest of the group);
  the second term is a **communication boost** (`θ`), applied *only* in rounds 4–6.
- **Movement speed**: `s_t = s_0 − α_s·T_t·s_0` — higher trust *slows* movement
  (less urgency to race for tokens), `s_0` drawn from an empirically fit normal
  distribution (mean 3 moves/s, sd 0.65).

Two further behavioural knobs, both estimated: `t_c` — the round-second at which an
agent abandons restraint and harvests everything ("going crazy," modelling the
observed last-60-seconds harvesting spike); `mn` — the minimum number of
tokens an agent leaves unharvested on neighbouring cells (approximating a
checkerboard conservation pattern), active only in rounds 4–9. Content of
communication is **not** modelled — `θ` applies a uniform trust boost to every agent
type, a deliberate, stated simplification.

**Calibration:** genetic algorithm (NetLogo `BehaviorSearch`) maximises a two-part
fitness score — `I₁` (fit on tokens harvested per round) and `I₂` (fit on resource
level sampled every 5 seconds across all 9 rounds), averaged. ~11,070 four-minute
simulated rounds per fitness evaluation (30 repetitions × 41 groups × 9 rounds), sized
so the fitness estimate's error stays ≤ 0.01 at p < 0.05.

## Experimental Setup
Calibration target: DeCaro et al. (2021), 41 four-person groups, $0.02/token, typical
earnings $10–25. Two benchmarks bracket the model: **unconditional cooperators**
(`p_h=0.4, α_h=0, α_s=0, t_c=150, τ=0, θ=1, T_0=1`) vs. **selfish agents**
(`p_h=1`, all other trust/restraint parameters at 0). Three increasingly rich
calibrations are compared: (1) selfish + unconditional-cooperator mix only; (2) add a
single conditional-cooperator type; (3) split that into two conditional-cooperator
subtypes differing in initial trust/inequality-sensitivity.

## Metrics
Resource level per round (sampled every 5 s); tokens harvested per round; **Gini
coefficient** of harvest inequality; self-reported trust (7-point scale, measured
after rounds 3 and 6); avatar-movement correlation and harvest correlation across
group members (a measure of behavioural coordination).

## Main Results

**Benchmark (Fig. 8):** unconditional cooperators collect **421.5 tokens** on average
per round-equivalent and keep the resource high throughout; selfish agents deplete the
resource within **~60 seconds** and collect only **201.2 tokens** — restraint
increases *total* yield, not just sustainability, because the pool stays productive.

**Calibration (Table 3 — verified against the PDF; note this corrects a detail from an
earlier, non-PDF-sourced pass at this note):**

| Model | Population | Fitness | Key parameters (conditional-cooperator type) |
| --- | --- | --- | --- |
| Selfish + unconditional only | 76% selfish, 24% unconditional cooperator | **0.507** | — |
| **Model 1** (1 conditional-cooperator type) | 16% selfish, 9% unconditional, **75% conditional cooperator** | **0.842** | `p_h=0.38` (low — conserves), `α_h=0.97` (harvest rate strongly trust-sensitive), `α_s=0.30`, `t_c=176s`, `τ=0.00009`, `θ=0.93`, `T_0=0.35` (starts distrustful), `mn=3` |
| Model 2 (2 conditional-cooperator types) | 6% selfish, 5% unconditional, 52% type A + 37% type B | **0.857** | Type A (low-trust/inequity-averse): `T_0=0.08`, `p_h=0.82`. Type B (high-trust/inequity-tolerant): `T_0=0.85`, `p_h=0.86` |

The two-type model (0.857) barely beats the one-type model (0.842) at the cost of
several extra parameters — the authors judge the **extra type is not needed**;
**Model 1 is the one to cite**. (This corrects an earlier draft of this note, which
had misattributed Model 2's `p_h≈0.82–0.86` to Model 1; Model 1's actual harvest
probability is the conservative **0.38**.)

**Trust regression (Table 1, multi-level, 41 groups × up to 164 individuals):**
before any communication, only **relative harvest in round 1** predicts trust after
round 3 (`β=3.708, p<0.01`) — group-level inequality (Gini) is *not* significant here.
After communication, trust after round 6 is predicted by **total group harvest**
(`β=0.026, p<0.01`) and **inequality** (`β=−6.033 on Gini, p<0.01`) — a low-Gini,
high-harvest round-6 strongly predicts high subsequent trust. Communication changes
*which* factor drives trust: individual unfairness dominates before talking is
possible; collective performance and equality dominate after.

**Behavioural correlation (Table 4):** movement is essentially uncorrelated across
group members in rounds 1–3 (`r≈−0.04` to `0.08` — everyone acts independently) and
becomes strongly correlated from round 4 onward (`r≈0.57–0.72` for movement, rising to
`r=0.85` for harvested tokens by round 9) — direct behavioural evidence that
communication produces *coordination*, not just individual restraint.

**Sensitivity (Table 6, appendix):** as long as **≥70% of the population is
conditional-cooperator**, fitness stays ≥0.70 — the qualitative finding (majority
conditional cooperators explain the data) is robust to exact population share, not a
knife-edge fit.

**Out-of-sample robustness test:** Model 1, unmodified, is applied to a *different*
experimental condition (Janssen et al. 2014: limited 5-cell visibility radius, so
players rarely observe others' behaviour) and correctly reproduces the qualitative
finding that limited visibility *increases* early-round harvesting (agents can't see —
and thus can't be deterred by — others' greed) while leaving post-communication
cooperation largely unaffected. This is a genuine out-of-sample generalisation check,
not a re-fit.

## Limitations
Explicitly stated: (1) communication *content* is not modelled — `θ` is a uniform
trust boost applied identically to every agent type, "a major simplification... needed
since we do not model the communication content itself"; (2) the model "does not
capture how communication had an impact on trust among the participants of the
original experiment" — trust-building is imposed, not derived, so the paper "cannot
provide a full understanding as to how communication has a direct impact on
cooperation"; (3) representative-agent-type simplification — individuals within a type
still vary due to local opportunity and observed inequality, but the type-level
parameters are fixed; (4) only trust and inequality-aversion are modelled among
possibly many relevant perceptions (e.g. procedural justice, self-determination —
named in HRCT but not implemented).

## Future Work
Explore heterogeneous communication-sensitivity across agent types (currently
uniform `θ`); build a mechanistic (not imposed) model of *how* communication content
raises trust; extend to more diverse commons-dilemma institutional settings.

## Relevance to This Project

- **Validates our fairness metric and our conditional-cooperator strategy with
  verified numbers**, not just a qualitative nod: the best-fit population is **75%
  conditional cooperator, 16% selfish, 9% unconditional cooperator** (Model 1, fitness
  0.842) — close to Fischbacher, Gächter & Fehr's (2001) independently-cited figure —
  and this dominance is *robust* (Table 6: fitness stays ≥0.70 whenever the
  conditional-cooperator share is ≥70%). This is strong, quantified support for
  `conditional_cooperator` being a first-class strategy rather than a minor variant
  (already reflected in our five-strategy set).
- **A concrete, evidence-based design for a richer communication mechanism than our
  current `broadcast_reliability`.** Our E6/ADR-0007 communication is a single
  reliability parameter on a broadcast signal. Janssen's trust equation —
  `T_t,i = T_{t-1} − (τ/(N−1))Σ|x_i−x_j| + θ(1−T_{t-1})` — is a fully specified,
  *fitted* dynamic trust model: inequality erodes trust every round, communication
  gives a bounded boost toward 1, and *harvest probability itself* is a direct
  function of current trust (`p_h(1−α_h T)`), not a fixed rate. This is a
  drop-in-shape candidate mechanism for the "Next: full `CommunicationModel`" item
  already queued in research-direction.md Phase 2 — closer to what we'd actually
  implement than a re-derivation from scratch, since the functional forms and fitted
  parameter ranges are already published.
- **Empirical grounding for a claim E6 currently makes qualitatively.** Our
  E6/E7 finding is "communication informs but does not coordinate" (peer response
  fails, only enforcement saves the resource). Janssen's Table 4 shows communication
  produces measurable behavioural *coordination* (movement correlation jumps from
  ≈0 to 0.57–0.72 after round 4) — i.e. in the human data, communication *does*
  coordinate, via the trust/restraint channel. This sharpens, rather than
  contradicts, our finding: it suggests our E6 broadcast (a bare aggregate number,
  no trust state, no restraint-linked response) is missing the *mechanism* by which
  human communication coordinates, not that coordination via communication is
  impossible in principle — consistent with the Ostrom/Walker/Gardner (1992) note's
  same conclusion via a different channel (agreement + endogenous sanction rather
  than trust + restraint).
- **A quantitative sustainability/yield benchmark consistent with our own baselines.**
  Unconditional cooperators out-yield selfish agents on *total* tokens (421.5 vs.
  201.2) as well as on sustainability — matching the direction of our
  `all_cooperative_global` vs. `all_selfish_global` negative control, from an
  independent spatial model with different mechanics. Useful corroboration to cite
  when justifying that baseline pair.
- **A caution about trusting unverified extractions.** An earlier version of this
  note, built from a web-fetched summary rather than the PDF, mis-transcribed which
  model variant Model 1's `p_h=0.38` belonged to. The corrected numbers above are
  read directly from Table 3 of the PDF. Worth remembering when using any
  AI-summarised source for a number that will appear in the thesis.

## Possible Follow-Up Contribution
Implement a minimal version of Janssen's trust-restraint loop on top of our existing
`broadcast_reliability` channel: agents track a scalar trust state updated by observed
inequality (Gini-like, computable from the same `RunResult` data we already log) and a
communication boost, with harvest restraint scaling with trust. Compare against the
current static-signal E6 broadcast on both sustainability *and* the movement/behaviour
correlation Janssen uses as a coordination metric — directly testing whether adding a
trust state (not just a louder signal) is what E6 was missing.

## Important Terms
Conditional cooperator (vs. unconditional cooperator, vs. altruist, vs. selfish);
cheap talk; trust (dynamic, equation-defined here, vs. our currently static
information/communication parameters); inequality aversion (`τ`); genetic-algorithm
model calibration / `BehaviorSearch`; Humanistic Rational Choice Theory (DeCaro 2019,
extending Ostrom 1998); pattern-oriented fitting (`I₁`/`I₂` fitness indices).

## Questions
- Is a non-spatial trust update (dropping the grid/movement machinery entirely, which
  our engine doesn't have) enough to reproduce the qualitative effect, or does spatial
  visibility (who can observe whose inequality) matter for the trust dynamics
  specifically? The Janssen et al. (2014) limited-visibility robustness test (radius
  sweep, Fig. 11) is directly relevant and already shows visibility changes *early*
  cooperation but not post-communication cooperation — worth re-reading in full if we
  build the follow-up.
- The paper's `θ ≥ 0.9` finding (communication must produce a near-maximal trust
  boost to fit the data) — is that specific to the token-race game mechanics, or would
  a smaller, tunable boost make more sense in our discrete-round CPR setting?
