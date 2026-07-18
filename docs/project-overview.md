# Project Overview

## The problem, in plain terms

Many important systems have no central controller. Drivers on a road network, fish
harvesters sharing a stock, servers balancing load, people sharing a budget of
antibiotics — in each case many independent actors make **local** decisions, and
the **collective** outcome emerges from those decisions. Sometimes this produces
good, cooperative, self-sustaining behaviour. Sometimes it produces collapse:
everyone acts reasonably from their own point of view, yet the shared system is
ruined. This is the classic *tragedy of the commons*.

Two things strongly shape which outcome occurs:

1. **What each actor knows** — only its own situation, its neighbours', or the
   whole system's state; and whether that knowledge is current, delayed, or wrong.
2. **How actors communicate** — not at all, with neighbours, by broadcast; with
   limited range, budget, or reliability.

And a third thing shapes how *robust* a good outcome is:

3. **Disturbances** — actors fail, resources crash, messages get dropped, or some
   actors behave selfishly or deceptively.

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

**Wahlfachprojekt 2:** the minimal engine, two strategies, two information
conditions, seeds, metrics, and reproducible export — done (v0.1.0). Remaining
first-scope work is analysis, sensitivity sweeps, and documentation depth.

**Bachelor's thesis (later):** communication models, disturbance scenarios, more
strategies, statistical evaluation, scalability, and possibly one small original
strategy or measurement method.

See [research-direction.md](research-direction.md) for the reasoning behind this
direction and [research-questions.md](research-questions.md) for the questions we
aim to answer.
