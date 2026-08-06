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
│   ├── config.py       ResourceConfig, AgentSpec, SimulationConfig, ExperimentConfig,
│   │                     CollectiveChoiceConfig (ADR-0011); YAML loading
│   ├── rng.py          make_rng, spawn_streams (independent per-agent streams)
│   ├── state.py        RoundRecord, RunResult (plain data, no behaviour)
│   └── simulation.py   Simulation engine + run_simulation()
├── environment/
│   └── resource.py     ResourcePool (stock + regeneration)
├── agents/
│   ├── observation.py  Observation (the information boundary)
│   └── agent.py        Agent (identity + payoff state; delegates to a Strategy)
├── strategies/
│   ├── base.py         Strategy (ABC) + SanctionPolicy
│   ├── selfish.py      SelfishStrategy
│   ├── cooperative.py  CooperativeStrategy (+ knowledge_bias)
│   ├── conditional.py  ConditionalCooperatorStrategy (reciprocity / retaliate)
│   ├── compensating.py CompensatingCooperatorStrategy (restraint / withhold)
│   ├── sanctioning.py  SanctioningStrategy (enforced quota + monitoring cost)
│   └── registry.py     name → class registry (extension point)
├── communication/      per-agent CommunicationModel protocol (reserved); broadcast lives in core
├── disturbances/       Disturbance protocol + ResourceShock / AgentFailure (config-scheduled; ADR-0008)
├── metrics/
│   └── metrics.py      compute_metrics, gini
├── experiments/
│   ├── runner.py       run_experiment, export_outcome, history_frame
│   ├── sweep.py        run_grid, with_resource (parameter sweeps)
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
`None`, which is what makes information models meaningful and testable. It also
carries an optional `signal` — a communicated aggregate (the group's total harvest
last round) delivered by the broadcast communication channel when
`broadcast_reliability > 0` (ADR-0007); this is how communication can supply
information the direct observation withholds.

### `agents.Agent` and `strategies.Strategy`
`Agent` owns identity and mutable per-run state (payoff, last harvest) and
delegates decisions to a `Strategy`. `Strategy.decide(observation, rng) -> float`
must be pure w.r.t. hidden state: any randomness comes from the passed `rng`
(strategies *may* hold per-run state, e.g. the conditional cooperator's memory of
the last stock — that is reset per run). A strategy may also expose
`sanction_policy() -> SanctionPolicy | None`; a non-`None` policy makes the engine
enforce a harvest quota (ADR-0005). New decision rules are added by subclassing
`Strategy` and registering the class.

### `core.Simulation` (the engine)
Owns one run. Builds the pool and agents from the config, spawns one RNG stream
per agent, and advances rounds. **Round order:** `regenerate → disturb → observe →
decide → ration → vote → enforce → harvest`; the `disturb` step is a no-op unless a
disturbance is scheduled for the round (ADR-0008), `vote` is a no-op unless
`collective_choice` is configured and this is its scheduled round (ADR-0011), and
`enforce` is a no-op unless a sanctioning agent is present *or* the collective-choice
vote has passed.

### `metrics`
Pure functions from a `RunResult` to a flat metric dict. No dependency on the
engine beyond the data records.

### `experiments`
`run_experiment` executes one `Simulation` per seed and collects metric rows into
a DataFrame; `export_outcome` writes a self-contained, reproducible output
directory; `Provenance` captures the software/environment context.

### `disturbances`
The `Disturbance` protocol plus two config-scheduled kinds (ADR-0008): `ResourceShock`
(cuts the stock at a set round) and `AgentFailure` (deactivates a fraction of the
agents — they stop requesting, harvesting, and enforcing). The engine applies scheduled
disturbances in the `disturb` step and marks the affected `RoundRecord`. Communication
failure is the next kind behind the same interface.

### `communication` (partly stubbed)
The per-agent `CommunicationModel` protocol fixes the intended interface for a fuller
channel; the *broadcast* model already lives in `core` (ADR-0007). See the module
docstrings and
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
   per round:  regenerate ─► disturb ─► observe (Observation) ─► decide (Strategy) ─►
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
2. **Regenerate:** `pool.regenerate()`.
3. **Disturb:** apply any disturbance scheduled for round `t` — a resource shock cuts
   the stock, or an agent failure deactivates some agents; the round is flagged
   `disturbed`. No-op when nothing is scheduled (ADR-0008).
4. **Observe:** build each agent's `Observation` of the (regrown, possibly shocked)
   stock, respecting the information model.
5. **Decide:** each agent returns a non-negative requested consumption.
6. **Allocate:** if `Σ requests > stock`, scale every request by the same factor
   `stock / Σ requests` (strategy-neutral rationing); otherwise grant requests.
7. **Vote (collective choice):** if `collective_choice` is configured and this is its
   scheduled round, tally whether the group has over-used the commons (harvest >
   sustainable yield) in more than a threshold share of rounds so far; if so, adopt
   collective enforcement starting this round. No-op otherwise (ADR-0011).
8. **Enforce (sanctioning):** if any agent exposes a `SanctionPolicy`, *or* the
   collective-choice vote has passed, cap every agent's harvest at the per-capita
   quota (excess stays in the pool) and charge monitoring costs — each individual
   sanctioner its own `monitoring_cost`, and (if collectively enforced) every other
   active agent the collective `cost_share`. No-op when neither applies (ADR-0005;
   ADR-0011).
9. **Harvest:** update per-agent payoffs (net of penalties), withdraw the total,
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
| an enforcement/institutional rule | expose a `SanctionPolicy` via `sanction_policy()` |
| a regeneration rule | extend `ResourcePool.regenerate` + `ResourceConfig` validation |
| a metric | add a key in `compute_metrics` (or a new pure function in `metrics`) |
| an information model | extend `Observation` + `Simulation._observe` |
| a parameter sweep / study | use `experiments.sweep.run_grid` |
| communication | implement `CommunicationModel`; add an exchange step in `step` |
| a disturbance | add a kind to `DISTURBANCE_KINDS`, a class in `disturbances.shocks`, and a `build_disturbances` branch (ADR-0008) |

## Known simplifications (current)

- Single scalar resource; no spatial structure.
- Utility = cumulative harvest (linear; no diminishing returns or discounting), net
  of sanction penalties.
- Enforcement is frictionless and "any one monitor enforces fully" (see ADR-0005).
- Communication is a single true aggregate broadcast (no per-agent messages,
  deception, delay, or topology yet — ADR-0007); the full `CommunicationModel`
  protocol remains stubbed.
- Disturbances cover a deterministic *pulse* resource shock and *agent failure*
  (ADR-0008); communication failure, *press* (sustained) disturbances, and agents that
  rejoin/are replaced are not yet implemented.
- Stochasticity is available (`decision_noise`, broadcast message loss), but the
  strategies themselves are deterministic; a stochastic *strategy* is future work.
- Collective-choice enforcement (ADR-0011) is a single deterministic threshold vote
  at one scheduled round, decided from a mechanically observed over-use tally — no
  per-agent vote, no stochasticity, no institutional memory across configs. It also
  cannot combine with an individually-`sanctioning` agent: any such agent already
  caps harvest at the sustainable yield, so over-use (the vote's only trigger) is
  never observed and the vote deterministically fails.
