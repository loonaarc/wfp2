# Terminology

Working definitions for this project. Where a term has a broad general meaning,
the definition is narrowed to how it is used *here*. Terms marked *(model term)*
name a concrete construct in the code.

## Agents and systems

- **Agent** — an autonomous decision-making entity that observes part of the world
  and chooses an action (here: how much of the resource to request each round).
  *(model term: `agents.Agent`, deciding via a `strategies.Strategy`.)*
- **Multi-agent system (MAS)** — a system of several interacting agents with no
  single controlling authority; global behaviour arises from local interactions.
- **Decentralized control** — decisions are made locally by agents, not by a
  central planner. The engine coordinates mechanics (regeneration, rationing) but
  does **not** dictate agent choices.
- **Strategy / decision rule** — the function mapping an agent's observation to an
  action. *(model term: `Strategy.decide`.)*

## Emergence and organization

- **Emergence** — system-level patterns that are not explicitly programmed into any
  single agent but arise from their interactions (e.g. resource collapse or
  sustained cooperation from purely local rules).
- **Emergent cooperation** — agents restraining individual consumption enough that
  the shared resource is sustained, without any agent being ordered to do so.
- **Self-organization** — the system settling into a structured, often stable
  regime (e.g. a steady resource level or stable division of harvest) through
  local interaction alone, without external control.

## Information

- **Private information** — an agent knows only its own state/history.
  *(model term: `information_model="private"`; the shared level is hidden.)*
- **Local / neighbourhood information** — an agent additionally knows the state of
  nearby agents. *(planned; not yet in the model.)*
- **Aggregated (group) information** — an agent knows summary statistics of the
  group (e.g. mean consumption). *(planned.)*
- **Global information** — an agent knows the full shared state.
  *(model term: `information_model="global"`; the resource level is visible.)*
- **Outdated / partially incorrect information** — information that is delayed or
  contains errors relative to the true state. *(planned.)*

## Communication

- **Broadcast signal** — the one communication channel currently implemented: each
  round every agent hears an aggregate (the group's total harvest last round) with a
  per-round reliability probability; message loss = silence. *(model terms:
  `SimulationConfig.broadcast_reliability`, `Observation.signal`; ADR-0007; used in
  E6/E7.)*
- **Communication topology** — the graph of who can send messages to whom
  (e.g. none, peer-to-peer, broadcast, range-limited, changing over time).
- **Message budget / range / delay / loss** — constraints on *per-agent* messaging:
  how many messages, how far, how late, how reliably they arrive.
  *(planned; the reserved `communication.CommunicationModel` interface — the current
  broadcast is a single aggregate signal, not per-agent messages.)*

## Resource dynamics

- **Common-pool resource (CPR)** — a shared resource that is *rivalrous* (one
  agent's consumption reduces what remains for others) but from which excluding
  users is hard. The central object of the first scenario.
  *(model term: `environment.ResourcePool`.)*
- **Carrying capacity (K)** — the maximum stock the resource can reach.
- **Regeneration rule** — how the stock regrows each round. *Logistic:*
  `dR = g·R·(1 − R/K)` (self-limiting, peaks at `R = K/2`). *Linear:* `dR = g·R`.
- **Maximum sustainable yield (MSY)** — the largest harvest that can be taken
  indefinitely. For logistic growth, `MSY = g·K/4`, achieved at stock `R = K/2`.
- **Collapse** — the stock falling to/below the collapse threshold. Under logistic
  growth a stock driven to 0 cannot recover, so collapse is effectively absorbing.
- **Tragedy of the commons** — the outcome where individually rational
  over-consumption destroys a shared resource that restrained use would sustain.

## Cooperation mechanisms (the strategies)

This is the **canonical list of strategies**; the code is ground truth
(`src/emergent_cooperation/strategies/`, `emergent-coop strategies`). Other docs
should link here rather than re-enumerate.

- **Selfish** — grab a large share of whatever is currently visible; ignores the
  future. An all-selfish population collapses the resource (tragedy of the commons).
  *(model term: `selfish`.)*
- **Cooperative restraint** — harvest only the regeneration surplus above a healthy
  reference stock (`K/2`), so the resource is maintained; self-correcting under
  observation. *(model term: `cooperative`.)*
- **Reciprocity / conditional cooperation** — cooperate as long as others do; respond
  to *detected* over-extraction by **retaliating** (grabbing a selfish share).
  Protects the individual from exploitation, but can accelerate collapse. *(model
  term: `conditional_cooperator`.)*
- **Compensating cooperation** — the restraint counterpart to reciprocity: on detected
  over-extraction, **withhold** (harvest nothing) to let the pool recover. Tends to be
  the *most* exploited response. *(model term: `compensating_cooperator`.)*
- **Sanctioning** — cooperate *and* enforce a rule: over-extraction is confiscated and
  the enforcer bears a monitoring cost. Caps every agent's harvest at a sustainable
  quota. *(model term: `sanctioning`, via `SanctionPolicy` + the engine's enforcement
  step.)*

Related concepts:

- **Ecological knowledge** — an agent's (possibly wrong) estimate of the sustainable
  yield. Distinct from *cooperation* (the willingness to restrain): sustainability
  needs both. *(model term: `knowledge_bias`; see [research-questions.md](research-questions.md) H6.)*
- **Monitoring / enforcement** — observing others' behaviour and applying a
  consequence (here, capping extraction). Ostrom identifies monitoring and graduated
  sanctions as conditions for enduring commons.
- **Second-order free-rider problem** — because monitoring is costly, agents who
  benefit from enforcement without paying to monitor out-earn those who do, so
  monitoring is itself under-provided — a collective-action problem one level up.
- **Replicator dynamics** — a rule by which above-average-payoff strategies grow their
  share of the population over "generations"; used (at the experiment level) to ask
  whether a costly strategy like monitoring is evolutionarily stable (E5, ADR-0006).

## Evaluation concepts

- **Cooperation rate** — the degree to which agents restrain consumption relative
  to a selfish benchmark (operationalised in [metrics.md](metrics.md)).
- **Fairness** — how equally payoffs (accumulated harvest) are distributed;
  measured by the **Gini coefficient** (0 = perfectly equal, →1 = maximally
  unequal).
- **Resilience** — the system's ability to maintain or recover cooperative,
  sustainable behaviour after a disturbance. Proxies: recovery time, post-shock
  sustainability. *(model terms: `DisturbanceConfig`, the `recovery_time`/`recovered`
  metrics; the first disturbance — a resource shock — is implemented, see E8/ADR-0008.)*
- **Robustness** — insensitivity of outcomes to nuisance factors such as random
  seed or small parameter changes. Contrast with resilience (recovery from shocks).
- **Disturbance** — an external perturbation applied to the world at a scheduled
  round (not a random event, so runs stay reproducible). *(model terms:
  `DisturbanceConfig`, the `disturbances` package; ADR-0008.)*
- **Resource shock** — a *pulse* disturbance that removes a fraction of the stock in
  one round (`magnitude = 0.7` → lose 70%). The first implemented disturbance kind.
  *(model term: `disturbances.ResourceShock`.)*
- **Agent failure** — a disturbance that deactivates a fraction of the agents at a
  scheduled round: they stop requesting, harvesting, and (if a sanctioner) enforcing.
  Tests tolerance to agent loss (E10). *(model term: `disturbances.AgentFailure`;
  `Agent.active`.)*
- **Recovery time** — rounds after a shock until the stock returns to ≥ 90% of its
  pre-shock level; undefined (right-censored) if it never does. *(model term: the
  `recovery_time` metric.)*
- **Reproducibility** — the property that a run can be exactly re-executed from its
  recorded configuration, seed, and software version, yielding identical results.
  Enforced here via deterministic RNG and provenance capture.

## Software / method terms

- **Seed** — the integer that determines all randomness in a run; identical seed +
  config ⇒ identical result. *(model term: `SimulationConfig.seed`, swept by
  `ExperimentConfig.seeds`.)*
- **Decision noise** — an optional stochastic perturbation of each agent's request
  (factor in `[1−d, 1+d]`), which is what makes the seed consequential and
  between-seed variance meaningful. *(model term: `SimulationConfig.decision_noise`.)*
- **Broadcast communication** — a channel by which each agent hears an aggregate
  signal (the group's total harvest last round) with a per-round *reliability*
  probability; message loss = silence. *(model terms:
  `SimulationConfig.broadcast_reliability`, `Observation.signal`; ADR-0007.)*
- **Provenance** — the metadata recorded with each experiment (software version,
  git commit, platform, timestamp, seeds, status) that makes it reproducible.
  *(model term: `experiments.Provenance`.)*
- **Experiment** — a base configuration run once per seed in a sweep, producing
  comparable metric rows. *(model term: `ExperimentConfig` + `run_experiment`.)*
