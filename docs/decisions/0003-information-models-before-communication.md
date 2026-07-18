# ADR-0003: Start with information models; defer explicit communication

- **Status:** Accepted
- **Date:** 2026-07-18
- **Deciders:** project owner (with assistant review)

## Context
The brief asks the first prototype to compare "at least two information **or**
communication conditions". Both are core research axes. We must choose what the
*minimal* first version varies, without foreclosing the other.

## Considered Options
1. **Information models first** (`global` vs `private`): control what each agent may
   observe, with no messaging machinery yet.
2. **Communication first** (e.g. no-comms vs broadcast-of-intentions): build a
   message-passing layer immediately.
3. **Both at once.**

## Decision
Implement **information models first** (Option 1). Provide a stubbed
`CommunicationModel` protocol so communication can be added later without redesign.

## Rationale
- **Information availability is the more fundamental, cheaper variable.** It is a
  property of the observation an agent receives — a single, well-contained boundary
  (`agents.Observation`) — and needs no new subsystem, message types, scheduling,
  or reliability model.
- **It isolates a clean question first.** "How much does *seeing the shared state*
  matter?" is answerable now and already produces a non-trivial result (blind
  cooperation is sustainable only near `K/2`; hypothesis H1).
- **Communication is a strictly larger design space** (topology, range, budget,
  delay, loss) better tackled once the engine, metrics, and baselines are solid.
- **No lock-in.** The `CommunicationModel` protocol reserves the interface; adding
  an exchange step to `Simulation.step` later is additive.

## Consequences
- **Positive:** a smaller, testable first prototype; a clean information-only
  finding; the communication axis kept explicitly on the roadmap (Phase 2).
- **Negative:** communication-specific questions (RQ-A / SQ-6–8) wait for Phase 2.
- **Commitment:** keep `Observation` and the information model as the single locus
  of "what an agent knows", so information and (future) communication compose
  cleanly rather than overlapping.

## Status Notes
`information_model ∈ {global, private}` implemented and tested; local/aggregated/
outdated/partially-incorrect models are the natural next information extensions.
