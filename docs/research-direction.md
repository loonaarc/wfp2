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

### Phase 0 — Foundation (done, v0.1.0)
Minimal deterministic CPR engine; `selfish` and `cooperative` strategies;
`global`/`private` information; seeds; metrics; reproducible export; CLI; tests.

### Phase 1 — First-scope completion (Wahlfachprojekt 2) — largely done
- ✅ Split cooperation from ecological knowledge (`knowledge_bias`; ADR-0004) after a
  literature review (Schill et al.).
- ✅ Two more strategies: `conditional_cooperator` (reciprocity) and `sanctioning`
  (enforcement; ADR-0005).
- ✅ Parameter-sweep tooling (`experiments.sweep`) and three documented experiments
  (E1–E3) with figures — see [findings-summary.md](findings-summary.md).
- ✅ Deepened documentation and ADRs 0001–0005.
- ⏳ Remaining: sensitivity sweeps over group size / regeneration rate; stochastic
  strategies (so between-seed variance becomes meaningful).

### Phase 2 — Communication (thesis)
Implement the `CommunicationModel` interface (already stubbed): start with
broadcast-of-intentions, then range/budget/delay/loss variants. Study when
communication improves outcomes and when it becomes inefficient or harmful.

### Phase 3 — Disturbances & resilience (thesis)
Implement the `Disturbance` interface (already stubbed): resource shocks, agent
failure, communication failure, malicious agents. Measure recovery time and
resilience; identify mechanisms that are efficient under normal conditions but
fragile under disruption.

### Phase 4 — Consolidation (thesis)
Statistical evaluation, scalability testing, automated experiment batches, and
possibly one small original strategy or measurement method compared to baselines.

## Explicitly deferred

- Reinforcement-learning agents (only with a strong, concrete justification).
- Spatial/grid environments and Mesa (see
  [decisions/0001-custom-simulation-core.md](decisions/0001-custom-simulation-core.md)).
- Rich visualization / GUI.
- Locking onto a single exact research question (kept open on purpose for now).
