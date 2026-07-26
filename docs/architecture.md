# Architecture

## Goals

1. **Determinism / reproducibility first.** A run is a pure function of
   `(config, seed)`. No hidden global state; all randomness flows through
   explicit, seeded generators.
2. **Modularity along the research axes.** Information, strategies, communication,
   and disturbances are separable so experiments can vary one at a time.
3. **Separation of simulation from analysis.** The engine produces plain data
   records; metrics, export, and notebooks consume them without reaching into
   engine internals.
4. **Small and readable.** A custom lightweight core is preferred over a framework
   for the current abstract scenario (see
   [decisions/0001-custom-simulation-core.md](decisions/0001-custom-simulation-core.md)).

## Package map

```
src/emergent_cooperation/
├── core/
│   ├── config.py       ResourceConfig, AgentSpec, SimulationConfig, ExperimentConfig; YAML loading
│   ├── rng.py          make_rng, spawn_streams (independent per-agent streams)
│   ├── state.py        RoundRecord, RunResult (plain data, no behaviour)
│   └── simulation.py   Simulation engine + run_simulation()
├── environment/
│   └── resource.py     ResourcePool (stock + regeneration)
├── agents/
│   ├── observation.py  Observation (the information boundary)
│   └── agent.py        Agent (identity + payoff state; delegates to a Strategy)
├── strategies/
│   ├── base.py         Strategy (ABC)
│   ├── selfish.py      SelfishStrategy
│   ├── cooperative.py  CooperativeStrategy
│   └── registry.py     name → class registry (extension point)
├── communication/      CommunicationModel protocol (stubbed; Phase 2)
├── disturbances/       Disturbance protocol (stubbed; Phase 3)
├── metrics/
│   └── metrics.py      compute_metrics, gini
├── experiments/
│   ├── runner.py       run_experiment, export_outcome, history_frame
│   └── provenance.py   Provenance (reproducibility metadata)
└── cli/
    └── main.py         emergent-coop entry point
```

## Responsibilities and interfaces

### `core.config`
Immutable dataclasses describing a run/experiment, built from nested dicts
(`from_dict`) so the YAML format is decoupled from the in-memory types.
Validation happens in `__post_init__` (fail fast on bad configs).

### `core.rng`
- `make_rng(seed) -> Generator`
- `spawn_streams(seed, n) -> list[Generator]` — independent streams via
  `SeedSequence.spawn`, so per-agent randomness is stable under changes to other
  agents. **The only sanctioned source of randomness in the project.**

### `environment.ResourcePool`
Holds the scalar stock and knows how it regrows (`regenerate`) and how withdrawals
are clipped to available stock (`withdraw`). It does **not** decide how a round's
harvest is split among agents — that needs per-agent info it has no reason to hold.

### `agents.Observation`
The **information boundary**: the only channel through which a strategy learns
about the world. Under `private` information the shared `resource_level` is set to
`None`, which is what makes information models meaningful and testable.

### `agents.Agent` and `strategies.Strategy`
`Agent` owns identity and mutable per-run state (payoff, last harvest) and
delegates decisions to a `Strategy`. `Strategy.decide(observation, rng) -> float`
must be pure w.r.t. hidden state: any randomness comes from the passed `rng`.
New decision rules are added by subclassing `Strategy` and registering the class.

### `core.Simulation` (the engine)
Owns one run. Builds the pool and agents from the config, spawns one RNG stream
per agent, and advances rounds. **Round order:** `regenerate → observe → harvest`.

### `metrics`
Pure functions from a `RunResult` to a flat metric dict. No dependency on the
engine beyond the data records.

### `experiments`
`run_experiment` executes one `Simulation` per seed and collects metric rows into
a DataFrame; `export_outcome` writes a self-contained, reproducible output
directory; `Provenance` captures the software/environment context.

### `communication`, `disturbances` (stubbed)
Protocols fixing the intended interfaces so the engine can adopt them later without
redesign. See the module docstrings and
[decisions/0003-information-models-before-communication.md](decisions/0003-information-models-before-communication.md).

## Data flow

```
YAML ──load_experiment──► ExperimentConfig
                               │  for each seed
                               ▼
                          Simulation(config, seed)
                               │  build ResourcePool + Agents
                               │  spawn per-agent RNG streams
                               ▼
   per round:  regenerate ─► observe (Observation) ─► decide (Strategy) ─►
               allocate (proportional rationing) ─► harvest ─► record RoundRecord
                               │
                               ▼
                          RunResult ──compute_metrics──► metric row
                               │                              │
                               └──────────► ExperimentOutcome ◄┘
                                                 │ export_outcome
                                                 ▼
        results/<name>/  resolved_config.yaml · metrics.csv · round_history.csv · provenance.json
```

## The round in detail

For round `t` (in `Simulation.step`):

1. **Snapshot** `resource_start = pool.level` (stock carried from `t−1`).
2. **Regenerate:** `pool.regenerate()` → `resource_after_regen`.
3. **Observe:** build each agent's `Observation` of the regrown stock (respecting
   the information model).
4. **Decide:** each agent returns a non-negative requested consumption.
5. **Allocate:** if `Σ requests > stock`, scale every request by the same factor
   `stock / Σ requests` (strategy-neutral rationing); otherwise grant requests.
6. **Enforce (sanctioning):** if any agent exposes a `SanctionPolicy`, cap every
   agent's harvest at the per-capita quota (excess stays in the pool) and charge each
   sanctioner its monitoring cost. No-op when no sanctioner is present (ADR-0005).
7. **Harvest:** update per-agent payoffs (net of penalties), withdraw the total,
   record `resource_after_harvest` (carried into `t+1`), and flag `collapsed`.

Regenerating **before** harvest makes the all-cooperative equilibrium exactly
stable (agents harvest exactly the regrowth), which gives clean, interpretable
baselines. See [decisions/0002-round-order-and-cooperative-rule.md](decisions/0002-round-order-and-cooperative-rule.md).

## Determinism guarantees

- No use of the global `numpy.random` state anywhere.
- Each agent gets an independent stream from `SeedSequence(seed).spawn(n)`.
- Agents are built and iterated in a fixed order (by spec order, then index).
- Given identical `(config, seed)`, `RunResult` is bit-for-bit identical.
  *(Verified by `tests/test_simulation.py::test_run_is_deterministic_for_same_seed`.)*

## Extension points (how to add things)

| To add… | Do this |
| ------- | ------- |
| a strategy | subclass `Strategy`, set `name`, `register_strategy(...)` |
| a regeneration rule | extend `ResourcePool.regenerate` + `ResourceConfig` validation |
| a metric | add a key in `compute_metrics` (or a new pure function in `metrics`) |
| an information model | extend `Observation` + `Simulation._observe` |
| communication | implement `CommunicationModel`; add an exchange step in `step` |
| a disturbance | implement `Disturbance`; invoke at a round boundary in `step` |

## Known simplifications (current)

- Single scalar resource; no spatial structure.
- Utility = cumulative harvest (linear; no diminishing returns or discounting).
- Communication and disturbances are interfaces only, not yet implemented.
- Metrics are basic; richer cooperation/resilience measures are future work.
