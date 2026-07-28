# ADR-0008: Model disturbances as deterministic, config-scheduled events

- **Status:** Accepted *(2026-07-27)*
- **Date:** 2026-07-27
- **Deciders:** project owner (assistant implementing)

## Context

Phase 3 of the roadmap studies **resilience**: how emergent cooperation copes with
environmental *disturbances* (resource shocks, agent failure, communication failure,
misleading information). Until now the environment was static — all stochasticity
lived in agent decisions, none in the world. To measure recovery we need to perturb
the world at a known point and watch what happens.

The design tension is with the project's first principle: a run must stay a **pure
function of `(config, seed)`** (determinism / reproducibility). A disturbance that
fires at a *random* round or with a *random* magnitude would inject a second,
hard-to-audit source of randomness and make "recovery time" depend on hidden draws.

The `disturbances` package already shipped a stub `Disturbance` Protocol (a callback
invoked at a round boundary that mutates the world). This ADR records how that stub
becomes real.

## Considered Options

1. **Random disturbances** — each round, a shock fires with some probability / random
   size, drawn from the run RNG. Realistic, but it entangles the disturbance with the
   seed and makes the "when/how big" of a shock non-obvious from the config; recovery
   metrics become noisy for reasons unrelated to the mechanism under test.
2. **Deterministic, config-scheduled disturbances.** A disturbance carries an explicit
   schedule (which round) and size (magnitude) in the `SimulationConfig`. The engine
   applies it in place at that round. The shock is part of the configuration, not a
   random event. *(Chosen.)*
3. **Disturbance as a wrapper around the engine** (like the E5 replicator loop) rather
   than inside `step`. Keeps `core` untouched, but a mid-run shock genuinely needs to
   act *between* a round's regeneration and its harvest — that is inside the round, so
   an external wrapper cannot express it cleanly.

## Decision

Adopt **Option 2**. Disturbances are declared in the config as
`DisturbanceConfig(kind, round, magnitude)` and built into concrete objects
(`disturbances.shocks.ResourceShock`) that the engine invokes once per round via a
`_disturb` step. The first kind is `resource_shock` — a single-round "pulse" that
multiplies the standing stock by `(1 − magnitude)`.

**Placement in the round order:** `regenerate → disturb → observe → decide → allocate
→ enforce → harvest`. The shock lands on the regrown stock and *before* observation,
so agents on the `global` model see and react to the depleted level the same round,
while `private` agents do not — which is exactly the comparison E8 exploits.

Each disturbance's `apply` returns whether it fired; the engine records `disturbed`
on the `RoundRecord`, and the resilience metrics (`recovery_time`, `recovered`,
`pre_shock_level`, `post_shock_min_level`) are computed from that mark, so no metric
needs to be told out-of-band when the shock happened.

## Rationale

- **Determinism is preserved.** A shock is configuration, not a random event; two runs
  with the same `(config, seed)` are still bit-for-bit identical. Recovery time varies
  across seeds *only* through `decision_noise`, which is the intended source.
- **Interpretability.** "70% shock at round 60" is legible in the resolved config and
  reproducible by anyone. The resilience story is about the *mechanism's* response,
  not about which rounds happened to be unlucky.
- **Minimal, additive core change.** Empty `disturbances` (the default) leaves every
  prior experiment byte-for-byte unchanged; the new step is a no-op without a schedule.
- **The Protocol generalises.** `resource_shock` is the first kind; agent failure,
  communication failure, and misleading information slot in behind the same interface
  and the same `disturbed` bookkeeping.

## Consequences

- **Positive.** Phase 3 is unblocked with a reproducible, auditable disturbance model;
  E8 already yields a non-obvious result (information, not enforcement, decides
  recovery from a shock).
- **Negative / limits.** Only deterministic *pulse* shocks exist today; *press*
  disturbances (a sustained regime change, e.g. a permanently lower `g`) and
  stochastic disturbance timing are not modelled. A genuinely random disturbance
  regime, if ever needed, should draw from a **separate, explicitly seeded** stream
  rather than the per-agent streams, to keep provenance clean.
- **Follow-ups.** `AgentDropout` (agent failure) and a `communication_failure` kind;
  a *press* shock; recovery metrics beyond time-to-90% (e.g. cumulative shortfall).
