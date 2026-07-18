# ADR-0001: Custom lightweight simulation core instead of Mesa

- **Status:** Accepted
- **Date:** 2026-07-18
- **Deciders:** project owner (with assistant review)

## Context
The project needs a simulation engine for an abstract common-pool-resource game:
turn-based rounds, a handful of simple rule-based agents, one shared scalar
resource, and — above all — **strict determinism and reproducibility**. The brief
explicitly asks whether [Mesa](https://mesa.readthedocs.io/) (a Python agent-based
modelling framework) helps here or whether a small custom core gives better
control and clarity, and warns against unnecessary dependence on Mesa.

## Considered Options
1. **Mesa framework.** Batteries-included ABM: schedulers, spatial grids,
   `DataCollector`, batch runner, browser visualization.
2. **Custom lightweight core.** A ~few-hundred-line engine purpose-built for this
   scenario, with explicit seeded RNG and plain data records.
3. **Other frameworks (AgentPy, NetLogo, MASON).** Similar trade-offs to Mesa,
   with less Python-native fit or extra language dependencies.

## Decision
Build a **custom lightweight core** (Option 2). Keep Mesa as a documented option to
revisit *if and when* a spatial scenario is introduced.

## Rationale
- **Determinism is the top requirement.** Mesa's schedulers and internal state add
  indirection between us and the exact order of random draws. A custom core lets us
  guarantee that a run is a pure function of `(config, seed)` and route *all*
  randomness through explicit `SeedSequence`-derived streams — the project's
  central methodological commitment.
- **The current scenario doesn't use Mesa's strengths.** There is no spatial grid,
  no complex scheduling, and (by design) no GUI. Mesa's main value would go unused.
- **Clarity and control.** A small, readable engine is easier to reason about,
  test, and extend along our specific axes (information, communication,
  disturbances) than adapting a general framework's abstractions.
- **Low cost to build, low lock-in.** The core is small; not depending on a
  framework avoids inheriting its release cycle and conventions.

## Consequences
- **Positive:** full control over determinism; minimal dependencies (numpy, pandas,
  pyyaml); an architecture shaped exactly to the research axes; easy testing.
- **Negative:** we re-implement conveniences Mesa provides (data collection, batch
  running) — but these are small and already partly built (`experiments.runner`).
- **Commitment:** we must maintain our own experiment/batch tooling.
- **Revisit trigger:** introducing a **spatial** environment, or needing
  interactive visualization, is a concrete reason to re-evaluate Mesa (or AgentPy).

## Status Notes
Validated so far: the custom core reproduces runs bit-for-bit across seeds
(`tests/test_simulation.py`) and the whole v0.1.0 pipeline is ~700 lines.
