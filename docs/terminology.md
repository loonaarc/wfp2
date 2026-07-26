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

- **Communication topology** — the graph of who can send messages to whom
  (e.g. none, peer-to-peer, broadcast, range-limited, changing over time).
- **Message budget / range / delay / loss** — constraints on communication:
  how many messages, how far, how late, how reliably they arrive.
  *(planned; `communication.CommunicationModel` interface is stubbed.)*

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

## Cooperation mechanisms

- **Ecological knowledge** — an agent's (possibly wrong) estimate of the sustainable
  yield. Distinct from *cooperation* (the willingness to restrain): sustainability
  needs both. *(model term: `knowledge_bias` on the cooperative/sanctioning
  strategies; see [research-questions.md](research-questions.md) H6.)*
- **Cooperative restraint** — harvesting only the regeneration surplus above a healthy
  reference stock (`K/2`), so the resource is maintained. *(model term:
  `cooperative`.)*
- **Reciprocity / conditional cooperation** — cooperate as long as others do; respond
  to over-extraction by defecting (grabbing a selfish share). Protects the individual
  from exploitation, but can accelerate collapse. *(model term:
  `conditional_cooperator`.)*
- **Sanctioning** — cooperating *and* enforcing a rule: over-extraction is confiscated
  and the enforcer bears a monitoring cost. Here it caps every agent's harvest at a
  sustainable quota. *(model term: `sanctioning`, via `SanctionPolicy` + the engine's
  enforcement step.)*
- **Monitoring / enforcement** — observing others' behaviour and applying a
  consequence (here, capping extraction). Ostrom identifies monitoring and graduated
  sanctions as conditions for enduring commons.
- **Second-order free-rider problem** — because monitoring is costly, agents who
  benefit from enforcement without paying to monitor out-earn those who do, so
  monitoring is itself under-provided — a collective-action problem one level up.

## Evaluation concepts

- **Cooperation rate** — the degree to which agents restrain consumption relative
  to a selfish benchmark (operationalised in [metrics.md](metrics.md)).
- **Fairness** — how equally payoffs (accumulated harvest) are distributed;
  measured by the **Gini coefficient** (0 = perfectly equal, →1 = maximally
  unequal).
- **Resilience** — the system's ability to maintain or recover cooperative,
  sustainable behaviour after a disturbance. Proxies: recovery time, post-shock
  sustainability. *(disturbances planned.)*
- **Robustness** — insensitivity of outcomes to nuisance factors such as random
  seed or small parameter changes. Contrast with resilience (recovery from shocks).
- **Reproducibility** — the property that a run can be exactly re-executed from its
  recorded configuration, seed, and software version, yielding identical results.
  Enforced here via deterministic RNG and provenance capture.

## Software / method terms

- **Seed** — the integer that determines all randomness in a run; identical seed +
  config ⇒ identical result. *(model term: `SimulationConfig.seed`, swept by
  `ExperimentConfig.seeds`.)*
- **Provenance** — the metadata recorded with each experiment (software version,
  git commit, platform, timestamp, seeds, status) that makes it reproducible.
  *(model term: `experiments.Provenance`.)*
- **Experiment** — a base configuration run once per seed in a sweep, producing
  comparable metric rows. *(model term: `ExperimentConfig` + `run_experiment`.)*
