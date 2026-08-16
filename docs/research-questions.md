# Research Questions

Questions are separated by maturity: broad framing questions, concrete testable
subquestions, candidate hypotheses, and questions deliberately postponed. The
immediate goal is **not** to lock onto one exact question but to keep a
prioritised, testable backlog.

Status legend: 🟢 answerable with the current v0.1.0 code · 🟡 needs a small
extension (Phase 1) · 🔵 needs communication/disturbance modules (Phase 2–3).

## Primary candidate question (literature-grounded, added 2026-07-25)

Emerging from the literature review (esp. Schill et al. 2016, *"Cooperation Is Not
Enough"*):

> **Under what information conditions does cooperative *intent* produce sustainable
> *outcomes* in a decentralized CPR system — and (later) can communication substitute
> for missing ecological knowledge?**

This separates *cooperation* (a social preference to restrain/share) from *ecological
knowledge* (knowing the sustainable yield), which our current model conflates (see
[decisions/0004](decisions/0004-separate-cooperation-from-knowledge.md)). It uses the
information axis we can already study and sets up the communication phase. It is the
current front-runner for the project's specific focus — not yet locked.

## Broad research questions

- **RQ-A.** How does communication influence emergent cooperation, and under which
  conditions does it help, become inefficient, or become harmful?
- **RQ-B.** How much information do agents need for stable self-organization, and
  how do local vs. neighbourhood vs. global information differ in effect?
- **RQ-C.** How resilient is emergent cooperation when agents, resources, or
  communication channels fail? Which cooperation mechanisms are efficient under
  normal conditions but fragile under disruption?
- **RQ-D.** How can cooperation, self-organization, fairness, resilience, and
  emergence be measured quantitatively, reproducibly, and comparably?
- **RQ-E** *(added once Phase 4 started; see
  [thesis-direction-equifinality.md](thesis-direction-equifinality.md)).* As the
  population and its governance structure get richer, does the **set of distinct
  configurations that reach a near-optimal outcome** grow, and what actually drives
  that — not "does cooperation work" but "in how many different ways"?

## Testable subquestions

### Information (RQ-B, RQ-D)
- **SQ-1** 🟢 Does withholding the shared resource level (`private` vs `global`)
  change whether an all-cooperative population sustains the resource, holding all
  else fixed? *(Baseline finding: at initial stock = K/2 the two coincide; the
  interesting question is how this depends on initial stock — see SQ-2.)*
- **SQ-2** 🟢 How does the `private`-information outcome depend on the initial
  stock relative to K/2? *(Hypothesis H1.)*
- **SQ-3** 🟡 With outdated information (level from `d` rounds ago), at what delay
  `d` does cooperation start to fail?

### Strategy mixes & free-riding (RQ-A, RQ-D)
- **SQ-4** 🟢 As the fraction of selfish agents in a mixed population rises from 0
  to 1, how do total harvest, collapse probability, and payoff inequality (Gini)
  change? Is there a threshold fraction at which the resource collapses?
- **SQ-5** 🟢 Does a `conditional_cooperator` (harvest cooperatively unless others
  over-consume) protect the resource against a minority of selfish agents better
  than unconditional cooperators do? **→ Answered (E2): No.** Reciprocity protects
  *fairness* (starves free-riders) but collapses the *resource* faster; unconditional
  restraint protects the resource but is heavily exploited. Neither protects both —
  motivating sanctioning. Caveat: depends on retaliation severity (`defection_greed`).
- **SQ-5b** 🟢 Does conditioning retaliation on one randomly-assigned partner's
  reputation (indirect reciprocity, Nowak & Sigmund 1998) avoid the collapse
  blanket, population-aggregate retaliation causes (SQ-5/E2)? **→ Answered (E18):
  yes** — `reputation_cooperator` survives at 1 free-rider where
  `conditional_cooperator` collapses (though worse than pure restraint); raising
  `visibility` (how often a partner's score is actually seen) protects fairness but
  costs the resource, the same trade-off E2 found, rediscovered inside one
  mechanism's own information parameter.
- **SQ-5c** 🟢 Does fixing that partner to a persistent graph neighbour instead of
  a fresh random draw every round (network reciprocity, Nowak 2006 rule 4) make
  an agent's outcome depend on its graph *position*? **→ Answered (E19): yes,
  dramatically** — at a sparse ring, a free-rider's fixed neighbours earn ~117 on
  average (20 seeds) vs. ~5 for agents on the far side, a >20× gap well-mixed
  reputation (SQ-5b) cannot produce; population-level sustainability barely
  moves, so the effect is distributional, not aggregate.

### Communication (RQ-A)
- **SQ-6** 🟢 Does broadcasting reduce exploitation / improve outcomes in mixed
  populations vs. no communication? **→ Answered (E6): partly.** Under private info a
  broadcast of group extraction lets conditional cooperators detect free-riders,
  cutting payoff inequality from 0.52 toward the global value — but it does **not**
  save the resource (the response is retaliatory).
- **SQ-7** 🟢 At what message-loss rate does communication stop helping? **→ Answered
  (E6): graded, not a threshold** — the fairness benefit falls smoothly as reliability
  drops from 1.0 to 0.0.
- **SQ-8** 🟢 Is there a regime where communication fails to help / harms? **→ Answered
  (E6): yes** — communication improves *fairness* but is neutral-to-harmful for the
  *resource*; its value depends on the response rule, not communication itself. A
  restraint-based responder is the open follow-up.

### Resilience (RQ-C)
- **SQ-9** 🟢 After a sudden resource shock, how long do populations take to recover,
  if at all? *Answered by [E8](experiments/E8-resilience.md) (pure populations:
  information decides recovery, not enforcement) and
  [E9](experiments/E9-resilience-with-free-riders.md) (with free-riders, enforcement is
  also required). Resilience needs both.*
- **SQ-9b** 🟢 When agents *fail* (drop out mid-run), does the commons survive, and
  does it matter who? *Answered by [E10](experiments/E10-agent-failure.md): who fails
  decides — losing the enforcer collapses it, a cooperator is harmless, a free-rider
  helps. Enforcement is a single point of failure.*
- **SQ-10** 🟡 How does resilience scale with group size and with regeneration rate?
  *(A sweep of the E8 shock over `N` and `g` — small addition.)*

### Equifinality / complexity (RQ-E)
- **SQ-13** 🟢 Does raw population-type diversity (how many distinct strategies
  coexist) predict near-optimal success, or is a specific composition feature doing
  the real work? **→ Answered (E14): the latter** — diversity count is a weak,
  confounded proxy; whether any `sanctioning` agent is present explains almost all
  of it.
- **SQ-14** 🟢 Does splitting the population into independently-enforced groups
  (nested enforcement, Ostrom principle 8) change the near-optimal-set size vs. flat
  enforcement? **→ Answered (E15): yes** — count grows genuinely with `m` (383 →
  2,820 → 18,737), fraction still falls (0.774 → 0.576 → 0.370).
- **SQ-15** 🟢 Does excluding vs. including a fixed batch of unmonitored outsiders
  (boundaries, Ostrom principle 1) change the near-optimal-set size? **→ Answered
  (E16): yes, consistently but not catastrophically** — opening costs a ~2× fraction
  at every group count tested.
- **SQ-16** 🟢 Does adding a second, asymmetric resource (a fixed per-agent
  `allocation_split` across two pools with different growth rates) change the
  near-optimal-set size? **→ Answered (E20): yes — grows it at several
  diversity levels**, exceeding the single-pool count/fraction at diversity 3
  (153/210 → 160/210) and 4 (140/175 → 145/175), matching it at 5 (35/35).
  Only diversity 1–2 lag, fully explained by a doubled-monitoring-cost tax
  (finding 3), not a general mismatch. A first pass found the opposite —
  shrinkage at every level — traced to a sanctioning-quota bug (a monitor
  enforcing the second, slower pool at the first pool's sustainable yield);
  caught and fixed, see ADR-0016.
- **SQ-17** 🟢 Does a fixed population's final outcome actually not depend on
  the starting resource level `R₀` (von Bertalanffy 1968's own literal
  definition of equifinality), and does that hold once free-riders can drain
  the pool from an already-fragile start? **→ Answered (E17): yes, exactly,
  for a well-behaved population** (`50.0` final level regardless of `R₀`
  from 1 to 95) **and yes, asymptotically, with free-riders present** (all
  starting levels converge to the identical `16.667` given enough rounds) —
  but with a sharp exception found along the way: any `R₀ > K/2` makes an
  all-`conditional_cooperator` population collapse the pool permanently
  within two rounds, since its decline-detection can't tell the
  population's own legitimate first harvest from real over-extraction.

### Reproducibility & sensitivity (RQ-D)
- **SQ-11** 🟢 How much do outcome metrics vary across random seeds for a fixed
  config (variance between runs)? Which metrics are stable, which noisy?
  **→ Answered (E4): very stable.** With `decision_noise=0.1`, between-seed s.d. of
  sustainability ≤ 0.008 — the mechanism results are robust, not seed-luck.
- **SQ-12** 🟢 How sensitive are outcomes to group size and regeneration rate?
  **→ Answered (E4):** higher regeneration rate `g` tolerates more free-riders
  (collapse threshold ∝ `g`); outcomes depend on the selfish *fraction*, not group
  size `N` (approximately scale-invariant).

## Candidate hypotheses

- **H1.** Under `private` information, cooperators sustain the resource only when
  the initial stock is close to the maximum-sustainable-yield stock (K/2); away
  from it, blind cooperation drifts and can collapse. *(Motivated by the v0.1.0
  finding that `private` and `global` coincide exactly at initial stock = K/2.)*
- **H2.** In mixed populations, collapse probability rises sharply above a critical
  fraction of selfish agents rather than gradually. *(Threshold effect.)*
- **H3.** Communication helps most when information is scarce and agents are
  heterogeneous, and helps little when agents already have global information.
- **H4.** Mechanisms that rely on fast, reliable communication are efficient under
  normal conditions but disproportionately fragile under message loss/delay.
- **H5.** Fairness (low Gini) and sustainability are positively associated across
  strategy mixes, but not perfectly — some regimes sustain the resource while
  distributing payoffs unequally.
- **H6** *(from Schill et al. 2016).* Cooperative *intent* alone does not guarantee
  sustainability: with biased or absent ecological knowledge, cooperators over- or
  under-exploit. Sustainability requires cooperation **plus** sufficiently accurate
  knowledge (or information that supplies it). *(Our `private` cooperator collapse is
  the "absent knowledge" corner of this; see H1.)*

## Postponed questions

- Do learning/adaptive (RL) agents discover cooperative equilibria the hand-written
  rules miss? *(Deferred: adds large complexity and reproducibility burden.)*
- How do spatial structure and locality of the resource change results?
  *(Still deferred: requires a spatial environment for the resource itself
  (a grid/local sub-pools); see ADR-0001. Not the same question as E19's
  graph — that fixes who a reputation-conditioned agent's partner can be,
  not where the shared resource physically lives; the pool stays one
  scalar, well-mixed for harvesting, exactly as before.)*
- ~~Reputation-based mechanisms (indirect reciprocity).~~ *(Built — see SQ-5b,
  E18, ADR-0014.)*
- ~~Network reciprocity (fixed-neighbour interaction structure).~~ *(Built —
  see SQ-5c, E19, ADR-0015.)*
- Reinforcement-learning agents. *(Deferred; but rule-based evolutionary/replicator
  dynamics are used — E5, ADR-0006.)*

## How questions map to the code

| Subquestion | Needs | Current support |
| ----------- | ----- | --------------- |
| SQ-1,2,11,12 | seeds, param sweeps, `decision_noise` | ✅ runner + sweep + E1/E4 |
| SQ-4 | strategy-mix configs | ✅ E2/E3/E7 |
| SQ-5 | conditional + sanctioning strategies | ✅ E2/E3 |
| SQ-6–8 | broadcast communication | ✅ `broadcast_reliability` + E6/E7 |
| SQ-3 | outdated-info model | ➕ small `Observation` extension |
| SQ-9 | resource shock + recovery metrics | ✅ `disturbances.ResourceShock` + E8/E9 |
| SQ-9b | agent failure | ✅ `disturbances.AgentFailure` + E10 |
| SQ-10 | resilience vs. `N` and `g` | ➕ sweep the E8 shock over `N`, `g` |
| SQ-13 | full compositional sweep | ✅ `AgentSpec` composition sweep + E14 |
| SQ-14 | group-scoped enforcement | ✅ `AgentSpec.group`, ADR-0012 + E15 |
| SQ-15 | ungoverned outsider batch | ✅ `AgentSpec.governed=False`, ADR-0013 + E16 |
| SQ-16 | second resource pool + per-agent split | ✅ `SimulationConfig.second_resource`, `AgentSpec.allocation_split`, ADR-0016 + E20 |
| SQ-17 | starting resource level `R₀` sweep | ✅ `ResourceConfig.initial_level`, ADR-0017 + E17 |
| SQ-5b | partner-specific reputation | ✅ `ReputationConfig`, ADR-0014 + E18 |
| SQ-5c | fixed neighbour graph on partner selection | ✅ `NetworkConfig`, ADR-0015 + E19 |
