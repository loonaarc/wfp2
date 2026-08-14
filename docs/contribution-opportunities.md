# Contribution Opportunities

Possible contribution types, each assessed by scientific value, technical
difficulty, bachelor-level feasibility, risks, dependencies, and evaluation
requirements. The aim is a realistic, achievable contribution — **a new algorithm
is not required**; a careful reproducible comparison or measurement is acceptable
and often more appropriate at this level.

Scoring is coarse (Low / Medium / High) and reflects *current* judgement.

---

## C1. Modular experiment architecture *(primary, in progress)*
A reusable, documented environment with interchangeable information, strategy,
communication, and disturbance models, and reproducible experiment tooling.

- **Scientific value:** Medium — enabling infrastructure rather than a finding, but
  the backbone that makes everything else credible.
- **Difficulty:** Medium. **Feasibility:** High (foundation already built).
- **Risks:** over-engineering; scope creep into a "framework". Mitigate by growing
  from concrete experiments.
- **Dependencies:** none. **Evaluation:** tests + demonstrated experiments.
- **Verdict:** ✅ The safe backbone contribution; **built** (engine, 6 strategies,
  broadcast communication, sweep + replicator tooling, reproducible export, two
  disturbance kinds (E8–E10), a collective-choice enforcement mechanism (E13,
  ADR-0011), and two further core-engine changes since — group-scoped enforcement
  (ADR-0012) and boundaries via the same mechanism (ADR-0013), backing E14–E16's
  population-diversity/groups/boundaries sweeps). Only the full per-agent
  communication protocol (deception, delay, topology) and the remaining ranked
  complexity axes (network reciprocity, multiple resources, reputation,
  specialization — see
  [thesis-direction-equifinality.md](thesis-direction-equifinality.md#ranking-the-axes-by-fit-not-by-build-cost))
  remain.

## C2. Systematic comparison of known strategies under controlled conditions *(primary target)*
Compare selfish / cooperative / conditional-cooperative (and mixes) across
information conditions and group sizes, with proper seed statistics.

- **Scientific value:** Medium–High — a clean, reproducible comparison is publishable
  as a solid empirical study.
- **Difficulty:** Low–Medium. **Feasibility:** High.
- **Risks:** results may be "expected" (e.g. cooperation sustains, selfishness
  collapses) — value then comes from *quantifying* thresholds and variability, not
  novelty. Manage expectations accordingly.
- **Dependencies:** one more strategy (conditional cooperator); sweep tooling.
- **Evaluation:** distributions across ≥20 seeds; effect sizes; sensitivity sweeps.
- **Verdict:** ✅ Strongest bachelor-appropriate target — **realized** across
  experiments E1–E10 ([findings-summary.md](findings-summary.md)), including robustness
  and sensitivity (E4), extended by E11–E13's comparison of monitoring-stability
  and enforcement mechanisms, and further extended by E14–E16's shift from
  point comparisons to full-space sweeps (does the *count* of near-optimal
  configurations grow as the population/governance structure gets richer).
  Remaining: larger seed sets once a genuinely *stochastic strategy* exists.

## C3. Benchmark / collection of reproducible cooperation scenarios
A curated, documented set of scenarios + expected outcomes others can reproduce
and compare against.

- **Scientific value:** Medium — useful if adopted; risk of being ignored.
- **Difficulty:** Low–Medium. **Feasibility:** High (extends the config set).
- **Risks:** "benchmark" implies community uptake we can't guarantee; frame as a
  *reproducible scenario suite* instead.
- **Dependencies:** C1. **Evaluation:** reproducibility across machines.
- **Verdict:** 🟡 Good secondary deliverable, weak as the sole contribution.

## C4. Disturbance-testing module for resilience experiments
A pluggable set of perturbations (resource shocks, agent/communication failure,
malicious agents) + resilience metrics.

- **Scientific value:** High — resilience of emergent cooperation is genuinely
  interesting and less "obvious" than the static case.
- **Difficulty:** Medium. **Feasibility:** Medium (thesis-phase).
- **Risks:** many design choices (what/when/how much to perturb) can balloon.
  Constrain to a few canonical disturbances.
- **Dependencies:** `disturbances` module + recovery-time metric — **both built**
  (ADR-0008; `ResourceShock`, `recovery_time`/`recovered`).
- **Evaluation:** recovery time and post-shock sustainability vs. baselines.
- **Verdict:** 🔄 Strong thesis extension, **now under way** — the resource shock and
  agent-failure disturbances + resilience metrics ship, with three results: E8
  (information, not enforcement, decides a pure population's recovery), E9 (with
  free-riders, enforcement is also required), and E10 (enforcement is a single point of
  failure). Remaining: communication failure; monitor-redundancy sweeps; a *press*
  disturbance.

## C5. Measurement framework for cooperation, self-organization, fairness, resilience
Carefully defined, validated metrics with stated assumptions and limitations, plus
robustness/sensitivity reporting.

- **Scientific value:** Medium–High — good measurement is a real contribution and
  is often under-done.
- **Difficulty:** Medium (definitions and validation are the hard part).
- **Feasibility:** High. **Dependencies:** partly done ([metrics.md](metrics.md)).
- **Evaluation:** metric behaviour on known-outcome scenarios; seed robustness.
- **Verdict:** ✅ Excellent companion to C2; low risk, high rigour payoff.

## C6. A small original local rule or communication strategy
Design one new strategy or communication scheme and compare it to baselines.

- **Scientific value:** High if it shows a non-trivial, explained effect.
- **Difficulty:** Medium–High. **Feasibility:** Medium.
- **Risks:** "original" invites the question "is it actually better/interesting?";
  a weak novelty is worse than a strong comparison. Only pursue if a concrete idea
  with a testable advantage appears.
- **Dependencies:** C1, C2, ideally C4 (to show it matters under disturbance).
- **Evaluation:** head-to-head vs. baselines across conditions and seeds.
- **Verdict:** 🟡 Optional "reach"; not required. Decide late, backed by evidence.

## C7. Automated parameter & seed experiment runner
A batch runner for sweeps over parameters and seeds, with aggregation.

- **Scientific value:** Low directly (tooling), High as an enabler.
- **Difficulty:** Low. **Feasibility:** High.
- **Dependencies:** C1. **Evaluation:** reproducible batch outputs.
- **Verdict:** 🟢 Cheap, high-leverage; build early in Phase 1.

## C8. Structured analysis of unexpected emergent behaviour
Investigate and explain surprising phenomena the experiments surface.

- **Scientific value:** High *if* something genuinely surprising appears.
- **Difficulty:** Medium. **Feasibility:** opportunistic (can't be planned).
- **Verdict:** 🟡 Keep a running log of anomalies; promote to a contribution only
  if a real one appears.

---

## Recommended plan

- **Core (Wahlfachprojekt 2 → thesis):** **C1 + C2 + C5** — a reproducible
  environment, a systematic strategy comparison, and a validated measurement
  framework. Highest value-to-risk ratio, fully bachelor-feasible.
- **Thesis extension:** add **C4** (resilience) and **C7** (batch runner).
- **Optional reach:** **C6**, only if a concrete idea with a testable advantage
  emerges from the C2/C4 work.

Avoid framing the project as "I built a simulation." Frame it as: *a reproducible
environment was built and used to systematically measure when and why decentralized
cooperation emerges and how fragile it is.*
