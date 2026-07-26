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

### Communication (RQ-A)
- **SQ-6** 🔵 Does broadcasting intended consumption before acting reduce collapse
  probability in mixed populations, compared to no communication?
- **SQ-7** 🔵 At what message-loss rate or delay does communication stop helping?
- **SQ-8** 🔵 Is there a communication regime where *more* messaging worsens
  outcomes (e.g. agents over-reacting to noisy signals)?

### Resilience (RQ-C)
- **SQ-9** 🔵 After a sudden resource shock (e.g. −50% stock), how long do
  cooperative vs. conditional-cooperative populations take to recover, if at all?
- **SQ-10** 🔵 How does resilience scale with group size and with regeneration rate?

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
  *(Deferred: requires a spatial environment; see ADR-0001.)*
- Reputation- and sanctioning-based mechanisms. *(Deferred to after communication.)*
- Endogenous, evolving strategy populations. *(Deferred.)*

## How questions map to the code

| Subquestion | Needs | Current support |
| ----------- | ----- | --------------- |
| SQ-1,2,11,12 | seeds, param sweeps | ✅ runner + configs |
| SQ-4 | strategy-mix configs | ✅ `mixed_global.yaml` pattern |
| SQ-3 | outdated-info model | ➕ small `Observation` extension |
| SQ-5 | conditional cooperator | ➕ new strategy |
| SQ-6–8 | communication module | 🔲 `communication` (stubbed) |
| SQ-9,10 | disturbance module | 🔲 `disturbances` (stubbed) |
