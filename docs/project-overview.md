# Project Overview

## The problem, in plain terms

Many important systems have no central controller. Drivers on a road network, fish
harvesters sharing a stock, servers balancing load, people sharing a budget of
antibiotics — in each case many independent actors make **local** decisions, and
the **collective** outcome emerges from those decisions. Sometimes this produces
good, cooperative, self-sustaining behaviour. Sometimes it produces collapse:
everyone acts reasonably from their own point of view, yet the shared system is
ruined. This is the classic *tragedy of the commons*.

Two things strongly shape which outcome occurs — **what each actor knows** (its
own situation only, or the whole system's state, and how current that knowledge
is) and **how actors communicate** (not at all, or by some channel with its own
limits). A third thing shapes how *robust* a good outcome is: **disturbances** —
actors fail, resources crash, messages get dropped. See
[research-direction.md](research-direction.md#the-three-organizing-axes) for the
precise breakdown of all three.

## What this project does

We build a small, clean, **abstract** simulation where these factors can be varied
one at a time and their effects measured. "Abstract" is deliberate: instead of
modelling one domain in detail, we model the *shared structure* common to many —
a renewable **common-pool resource** that several agents draw from each round.
That keeps the findings transferable and keeps the engineering focused on the
science rather than domain minutiae.

The concrete starting scenario:

- several agents share one renewable resource;
- each round the resource regenerates, then each agent chooses how much to take;
- if agents collectively take too much, the resource collapses and cannot recover;
- agents may receive different information and (later) may communicate;
- agents follow simple, transparent decision rules (e.g. *selfish* vs *cooperative*).

## Why it matters

If we can measure **when** cooperation emerges, **how much** information agents
actually need, and **how fragile** cooperation is under disturbance, we learn
something reusable about designing and understanding decentralized systems — and
we get a reproducible testbed others can extend and compare against.

## What this project is *not*

- Not a visualization or GUI project. Output is metrics, tables, and plots.
- Not tied to one application domain.
- Not (initially) a machine-learning project. Agents use hand-written rules;
  reinforcement learning is deferred unless a concrete need justifies it.

## Scope

**Wahlfachprojekt 2 (submitted):** the engine, five strategies, the
information/knowledge conditions, a broadcast communication channel, seeds +
`decision_noise`, metrics, reproducible export, and ten documented experiments
(E1–E10; see the [findings summary](findings-summary.md)) — done and graded.

**Since then (thesis-track work, ongoing):** a sixth strategy (`loner`) and three
more experiments probing whether monitoring can be made evolutionarily stable
(E11, E12) and whether a voted, jointly-funded agreement can substitute for
individually pre-committed enforcement (E13) — the latter required the project's
first core-engine change since WFP2 (`CollectiveChoiceConfig`, ADR-0011). Since
then, two further core-engine changes — group-scoped ("nested enterprise")
enforcement (ADR-0012) and boundaries/open-access via the same mechanism
(ADR-0013) — backed three more experiments testing whether the equifinality
framing itself holds up: population-type diversity (E14), groups (E15), and
boundaries (E16), with a starting-resource-level experiment reserved as E17. The
bachelor thesis direction is not yet formally locked in, but in practice this
equifinality/complexity-axis line is what's actively being developed and has
had encouraging supervisor feedback; see
[thesis-direction-equifinality.md](thesis-direction-equifinality.md) for the
brainstorming and [complexity-synthesis.md](complexity-synthesis.md) for the
living synthesis of what's been found so far.

**Still open, regardless of thesis framing:** richer communication (per-agent
messages, deception, delay, topology), further disturbance kinds (communication
failure, a sustained "press" disturbance, agents rejoining), statistical evaluation
at scale, and possibly one small original strategy or measurement method.

See [research-direction.md](research-direction.md) for the reasoning behind this
direction and [research-questions.md](research-questions.md) for the questions we
aim to answer.
