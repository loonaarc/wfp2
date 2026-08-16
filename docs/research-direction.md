# Research Direction

## Current direction (chosen)

> Development of a modular multi-agent simulation environment for investigating
> how information availability, communication structures, and environmental
> disruptions influence emergent cooperation, self-organization, and resilience
> in decentralized systems.

This is treated as the working direction. It may still change, but only if a
concrete problem or better evidence emerges — not through further open-ended
brainstorming.

## Why this direction

- **It targets a real, well-studied phenomenon.** Emergent cooperation in
  common-pool-resource settings is a mature research area (tragedy of the commons,
  Ostrom's work on governing the commons, evolution-of-cooperation studies). There
  is a solid literature to anchor the work and to compare against.
- **It is domain-neutral and reusable.** By modelling the shared abstraction
  (agents + a renewable common resource) rather than one application, results
  transfer across domains and the codebase stays focused.
- **It has a clear, bachelor-appropriate contribution shape.** The contribution is
  a *reproducible experimental environment plus systematic measurement*, which is
  achievable and valuable without inventing a new algorithm (see
  [contribution-opportunities.md](contribution-opportunities.md)).
- **It decomposes cleanly into independent variables.** Information, communication,
  strategies, and disturbances are separable axes, which fits a modular
  architecture and controlled experiments.
- **It scales from Wahlfachprojekt 2 to thesis** without rework: the same engine
  and metrics grow by adding models, not by rewriting.

## The three organizing axes

1. **Information availability** — how much and how good is each agent's knowledge?
   *(private / local / aggregated / global; current / outdated / partially wrong)*
2. **Communication structure** — how do agents exchange information?
   *(none / peer-to-peer / broadcast; range-, budget-, delay-, loss-limited;
   changing topology)*
3. **Disturbances** — what perturbs the system and how does cooperation cope?
   *(agent failure, resource shocks, slower regeneration, message loss, malicious
   agents, agents joining/leaving)*

Against these, we measure **emergent cooperation, self-organization, fairness, and
resilience** (see [metrics.md](metrics.md)).

## Roadmap

*This is the single, canonical roadmap; other docs link here rather than keep their
own next-steps lists.*

### Phase 0 — Foundation — ✅ done
Minimal deterministic CPR engine; `selfish` and `cooperative` strategies;
`global`/`private` information; seeds; metrics; reproducible export; CLI; tests.

### Phase 1 — Mechanisms & robustness (Wahlfachprojekt 2) — ✅ done
- Split cooperation from ecological knowledge (`knowledge_bias`; ADR-0004) after a
  literature review (Schill et al.).
- Five strategies total: added `conditional_cooperator` (reciprocity),
  `sanctioning` (enforcement; ADR-0005), and `compensating_cooperator` (restraint).
- Parameter-sweep tooling (`experiments.sweep`) and experiments **E1–E3** (the
  mechanism ladder) with figures — see [findings-summary.md](findings-summary.md).
- Robustness & sensitivity: added `decision_noise`; **E4** (robust to noise;
  sensitivity to `g` and `N`).
- Deepened documentation and ADRs 0001–0007.

### Phase 2 — Adaptation & communication (thesis, started) — 🔄 in progress
- ✅ **Voluntary monitoring (E5):** replicator dynamics (ADR-0006) — is monitoring
  evolutionarily stable? (No.)
- ✅ **Loner rescue attempt (E11, ADR-0009):** does an opt-out strategy (Hauert et
  al. 2007) rescue E5's monitoring collapse? Delays it ~4–5×, does not prevent it —
  our continuous replicator dynamics lack the finite-population fixation step the
  mechanism relies on.
- ✅ **Pool punishment (E12, ADR-0010):** does Sigmund et al. (2010)'s pre-committed
  pool + second-order fine on all non-monitors succeed where E11 didn't? Yes —
  sanctioning grows monotonically to ~100%, sustainability never drops. The first
  monitoring-stability mechanism tried that actually works.
- ✅ **Broadcast communication (E6, ADR-0007):** `broadcast_reliability` +
  `Observation.signal`; does communication substitute for information? (For fairness.)
- ✅ **Response rules (E7):** given communication, only enforcement saves the commons.
- ✅ **Binding agreement / collective choice (E13, ADR-0011):** a voted,
  jointly-funded quota — the first core-engine change since E1–E10 — unifying
  E5 + E7. Matches individually pre-committed enforcement exactly for 0–4
  free-riders (if the group votes fast: round 2, not round 10), breaks down
  at 5+ regardless of timing.
- ⏳ Next: the fuller `CommunicationModel` (per-agent messages, deception,
  delay, topology).

### Phase 3 — Disturbances & resilience (thesis) — 🔄 in progress
Implement the `Disturbance` interface (was stubbed): resource shocks, agent failure,
communication failure, malicious agents. Measure recovery time and resilience;
identify mechanisms that are efficient under normal conditions but fragile under
disruption.
- ✅ **Resource shock + resilience metrics (E8, ADR-0008):** a deterministic,
  config-scheduled pulse shock; recovery-time / recovered metrics. Result:
  **information, not enforcement, decides whether a pure population recovers** —
  observing populations self-correct and recover, blind ones collapse. The first
  genuinely non-obvious finding.
- ✅ **Mixed populations under a shock (E9):** with free-riders present, **enforcement
  is additionally required** to recover — cooperation recovers only up to ~1
  free-rider, enforcement up to 3 of 8. Resilience needs *both* information (E8) and
  enforcement (E9).
- ✅ **Agent failure (E10):** agents dropping out mid-run. **Who fails decides** —
  losing the enforcer collapses the commons, losing a cooperator is harmless, losing a
  free-rider helps. Enforcement is a **single point of failure**; distributed
  self-correction degrades gracefully.
- ⏳ Next: **communication failure** (the broadcast drops) on the same interface;
  monitor **redundancy** sweeps; a *press* (sustained) disturbance; agents that
  rejoin/are replaced.

### Phase 4 — Equifinality / complexity axes (thesis) — 🔄 in progress
*Why this reframe and the full ranked candidate list:*
[thesis-direction-equifinality.md](thesis-direction-equifinality.md). *What it's
found so far:* [complexity-synthesis.md](complexity-synthesis.md). Not yet the
formally locked-in thesis topic, but the actively developed one, with encouraging
supervisor feedback.
- ✅ **Population-type diversity (E14)** — raw diversity count is a weak,
  confounded proxy; enforcer presence explains almost all of it.
- ✅ **Groups / nested enforcement (E15, ADR-0012)** — a second core-engine change
  (after E13's collective choice); near-optimal count genuinely grows with `m`,
  fraction still falls.
- ✅ **Boundaries / open access (E16, ADR-0013)** — expressed via the same groups
  mechanism, no new engine code; opening costs a consistent ~2× fraction.
- ✅ **Reputation / indirect reciprocity (E18, ADR-0014)** — built and demo'd as a
  standalone mechanism comparison, not folded into the complexity-axis sweep
  (see ADR-0014's Status Notes for why). Partner-specific retaliation avoids the
  collapse blanket retaliation (`conditional_cooperator`, E2) causes.
- ✅ **Network reciprocity (E19, ADR-0015)** — built and demo'd as a standalone
  mechanism comparison, extending E18 with a fixed, persistent graph neighbour
  instead of a fresh random partner every round. Fixed graph position creates a
  >20× payoff gap between a free-rider's fixed neighbours and agents on the far
  side of the ring — something well-mixed reputation cannot produce. An earlier
  evolutionary-dynamics operationalization was tried first and rejected (see
  ADR-0015's Considered Options) once it became clear it couldn't produce the
  local payoff variance the mechanism actually depends on.
- ✅ **Multiple resources / specialization (E20, ADR-0016)** — unlike
  reputation/network, folded directly into the complexity-axis composition
  sweep as row 4 (see complexity-synthesis.md): exceeds the single-pool
  near-optimal set at two of five diversity levels and matches it at a
  third, once a sanctioning-quota calibration bug (a monitor enforcing the
  second pool at the first pool's sustainable yield, caught and fixed — see
  ADR-0016) was corrected. Diversifying effort across both pools still
  unlocks 44% more welfare than concentrating on one when the split is
  tuned to the asymmetry; specialist monitors are half the cost but
  consistently lower net welfare than generalists, because a specialist
  stops harvesting the pool it stops enforcing, not just enforcing it.
- ⏳ Next: see the ranked candidate list linked above (`R₀` reserved as
  **E17**).

### Phase 5 — Consolidation (thesis)
Statistical evaluation, scalability testing, automated experiment batches, and
possibly one small original strategy or measurement method compared to baselines.

## Explicitly deferred

- Reinforcement-learning agents (only with a strong, concrete justification).
- Spatial/grid environments and Mesa (see
  [decisions/0001-custom-simulation-core.md](decisions/0001-custom-simulation-core.md)).
- Rich *in-engine* visualization / GUI. *(A lightweight presentation layer now
  exists — a browser demo `web/commons-demo.html` and the `notebooks/explore.ipynb`
  dashboard — but the engine itself stays headless: it emits plain data records that
  those layers, and the static plots in `scripts/`, consume.)*
- Locking onto a single exact research question (kept open on purpose for now).
