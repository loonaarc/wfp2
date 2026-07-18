# ADR-0002: Round order (regenerate→harvest) and a target-based cooperative rule

- **Status:** Accepted
- **Date:** 2026-07-18
- **Deciders:** project owner (with assistant review)

## Context
The minimal CPR model needs (a) an order for the per-round operations
regeneration and harvest, and (b) a rule for what a "cooperative" agent does.
Both choices determine whether the intended baselines behave cleanly.

An initial implementation used **harvest → regenerate** with a cooperative rule
that harvested the *current inflow* `g·R·(1−R/K)` split across agents. Testing
revealed this bleeds the stock down every round even for an all-cooperative
population: harvesting before regeneration means the pool always regrows from a
*reduced* stock, so net stock declines and eventually collapses. The
"all-cooperative sustains the resource" baseline failed.

## Considered Options
1. **Keep harvest→regenerate; make cooperators solve the implicit sustainable
   harvest** `h = g·(R−h)·(1−(R−h)/K)`. Correct but opaque and hard to explain.
2. **Switch to regenerate→harvest; cooperators harvest the current inflow.**
   Cleaner, but convergence to a stable stock is not obvious and depends on the
   observed post-regen level.
3. **Switch to regenerate→harvest; cooperators harvest the *surplus above a
   reference stock* `K/2`** (`request = max(0, R − K/2)/N`). Self-correcting and
   easy to explain; equilibrium is exactly the maximum-sustainable-yield stock.

## Decision
Adopt **regenerate → observe → harvest** (Option 3's ordering) **and** a
**target-based cooperative rule**: harvest an equal share of the surplus above the
reference stock `target_fraction·K` (default `K/2`). Blind (`private`) cooperators
fall back to claiming a share of the maximum sustainable yield `g·K/4`.

## Rationale
- **Clean, interpretable baselines.** All-cooperative populations hold the stock at
  `K/2` and harvest exactly the regrowth (MSY) indefinitely; all-selfish collapse.
  This makes the core contrast unambiguous and easy to teach and verify.
- **Self-correcting cooperation.** Harvesting only the *surplus above a reference*
  means cooperators automatically stop harvesting when the stock is low and let it
  recover. This is exactly the behaviour we want for future **resilience**
  experiments (Phase 3) — a strong forward-looking reason.
- **Standard framing.** "The resource regrows, then agents exploit it" is a
  conventional and defensible ordering (e.g. seasonal fisheries).

## Consequences
- **Positive:** stable, explainable equilibria; a cooperative rule that is robust
  by construction; verified baseline dynamics (harvest 1000 & steady stock 50 for
  all-cooperative; collapse for all-selfish).
- **Trade-off:** the initial stock regenerates once *before* the first harvest,
  which is a minor modelling quirk to document.
- **Note (fragility, kept intentionally):** blind (`private`) cooperators harvest a
  *constant* MSY regardless of the true stock, so they are sustainable only near
  `R = K/2` and drift otherwise. This is a feature to study (hypothesis H1), not a
  bug — it makes the information axis consequential.
- **Data-model impact:** `RoundRecord` fields renamed to
  `resource_start`, `resource_after_regen`, `resource_after_harvest`.

## Status Notes
Verified by `tests/test_simulation.py` (all-cooperative sustains, all-selfish
collapses, harvest never exceeds available stock) and `scripts/run_baselines.py`.
