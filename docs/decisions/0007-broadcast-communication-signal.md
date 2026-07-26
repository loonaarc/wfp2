# ADR-0007: A minimal broadcast communication signal via the observation

- **Status:** Accepted *(2026-07-26)*
- **Date:** 2026-07-26
- **Deciders:** project owner (assistant implementing)

## Context
Communication is the project's stated second axis (ADR-0003 deferred it in favour of
information models first). Experiments E1–E5 exhausted the information/mechanism axis;
the natural next step is a first communication model. The literature points the way:
communication works through *shared information / trust* (Janssen et al. 2022;
GovSim's communication cut over-usage ~21%).

We want the smallest change that (a) implements a real communication channel, (b) lets
us ask the project's communication questions (SQ-6 does it help, SQ-7 message loss,
SQ-8 can it harm), and (c) does not require the full message-passing subsystem
(topology, budgets, delays) up front.

## Considered Options
1. **Full `CommunicationModel` subsystem** (the stubbed protocol): per-agent messages,
   topology, budget, delay, loss. Faithful but large; premature.
2. **Pairwise/neighbour messaging.** Needs a topology and per-pair routing.
3. **Broadcast of an aggregate signal via the observation.** Each round the engine
   computes one aggregate — the group's total extraction last round — and delivers it
   into each agent's `Observation` with a per-agent *reliability* probability
   (dropped = not received). *(Chosen.)*

## Decision
Adopt **Option 3**. Add:
- `SimulationConfig.broadcast_reliability ∈ [0, 1]` (`0` = no communication, the
  default; `p` = each agent receives the broadcast with probability `p`, drawn from
  its own RNG);
- `Observation.signal: float | None` — the communicated aggregate (total harvest last
  round), or `None` when no message was received;
- engine support: track last-round total harvest and populate `signal` in `_observe`.

A strategy may use `signal` (e.g. the conditional cooperator, under private
information, treats `signal > MSY` as detected over-extraction). Backward compatible:
`broadcast_reliability = 0` ⇒ `signal` is always `None` ⇒ unchanged behaviour.

## Rationale
- **Minimal, reusable, honest.** One config knob + one observation field + a few engine
  lines give a genuine communication channel with a **reliability/message-loss** knob
  (SQ-7) — without committing to topology/budget yet.
- **Directly answers the communication questions** and ties back to E1: communication
  is a way to *acquire information* the private model withholds.
- **Reproducible:** the per-agent receive draw uses the agent's seeded RNG, so a run
  stays a pure function of `(config, seed)`.
- Leaves room to grow into the full `CommunicationModel` protocol later (broadcast is
  the p2p/limited-range special case with everyone connected).

## Consequences
- **Positive:** a first communication model; SQ-6/7/8 become answerable (E6);
  backward compatible.
- **Simplifications:** a single scalar *aggregate* signal (not per-agent messages), no
  delay, no deception model (agents broadcast the true aggregate); "reliability" is
  i.i.d. per agent per round. All documented in the E6 report.
- **Follow-ups:** per-agent messages, intentions/pledges (and lying), delay, topology,
  budget; a trust/reputation state (Janssen et al.).

## Status Notes
Implemented 2026-07-26. The conditional cooperator uses `signal` under private
information; Experiment E6 sweeps `broadcast_reliability`.
