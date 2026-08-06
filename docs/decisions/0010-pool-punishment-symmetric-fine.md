# ADR-0010: Pool punishment with a symmetric fine on all non-monitors

- **Status:** Accepted *(2026-08-06)*
- **Date:** 2026-08-06
- **Deciders:** project owner (assistant implementing)

## Context

[E11](../experiments/E11-loner-rescue.md) showed Hauert et al. (2007)'s opt-out
rescue only delays E5's monitoring collapse, not prevents it, and pointed at
Sigmund, De Silva, Traulsen & Hauert (2010)'s *pool punishment* as a different
fix worth trying (see
[`docs/paper-notes/2010-sigmund-social-learning-institutions.md`](../paper-notes/2010-sigmund-social-learning-institutions.md)).
Pool punishment differs from peer punishment (E11's/E5's `sanctioning`) in two
ways: the cost is paid unconditionally every round (not scaled down when
defectors are rare), and — because paying into the pool is a declared,
observable act — the pool can additionally fine **second-order free-riders**:
plain cooperators who benefit from enforcement without paying for it.

## Considered Options

1. **Fine only `cooperative` agents, funding `sanctioning`.** The direct,
   literal reading of "second-order sanctioning": tax the free-riding
   cooperators, pay it to the monitors. *(Tried first; reverted — see below.)*
2. **Fine both `cooperative` and `selfish` agents, funding `sanctioning`.**
   *(Chosen.)*

## Why Option 1 failed

Implemented and run first (`SECOND_ORDER_FINE_PER_ROUND` applied to
`cooperative` only). Result: **cooperative agents collapsed faster than in
plain E5** (down to 16% by generation 4, vs. taking ~13 generations for
sanctioning to erode in E5), and the whole population still ended up
all-selfish by generation ~24 — a *worse*, faster collapse, not a rescue.

The reason is a property of this project's engine, not of Sigmund's model: a
diagnostic run (`AgentSpec` counts `{sanctioning: 16, cooperative: 16,
selfish: 8}`, `N=40`, 60 rounds, `K=100`, `g=0.4`) shows that whenever
enforcement holds, **`selfish` and `cooperative` earn identically** (~15.0
each) — the harvest-cap confiscates a selfish agent's *attempted*
over-extraction but does not reduce its payoff *below* what a complying
cooperator gets. In Sigmund's own model, ordinary defectors are **already**
fined below cooperators' payoff before any second-order addition is even
considered. Taxing only `cooperative` here reproduced the second-order half of
his mechanism while skipping the ordinary first-order half his baseline
already assumes — so the fine simply made `cooperative` worse off than
*untaxed* `selfish`, accelerating drift toward selfish rather than toward
sanctioning. Worse, because the fine's revenue source (`cooperative`) was
exactly the population being driven to extinction, `sanctioning`'s subsidy
evaporated just as it was needed most — a self-consuming funding source.

## Decision

Adopt **Option 2**: `POOL_FINE_PER_ROUND` (0.2, matching the existing
monitoring cost's magnitude) is charged to **every** non-sanctioning agent —
`cooperative` and `selfish` alike — each round enforcement exists, and the
total collected is redistributed evenly across `sanctioning` agents. This
correctly reproduces both halves of Sigmund's mechanism: the ordinary fine on
defectors his baseline model already has, plus the second-order fine on
free-riding cooperators that his paper adds on top.

Implemented, like E11, purely at the replicator/fitness level in
`scripts/experiment_pool_punishment.py` (Experiment E12) — no core-engine
change, no new `Strategy` subclass; `sanctioning`/`cooperative`/`selfish`
behave exactly as they already do during the simulated round, and the fine is
applied to the *measured* generational fitness before the replicator update,
matching ADR-0006's and ADR-0009's precedent.

## Consequences

- **Positive — this one actually works.** With the corrected symmetric fine,
  `sanctioning` grows **monotonically** from 40% to ~100% of the population
  over 60 generations, and sustainability never leaves 0.50 — no collapse, no
  delay-then-collapse. This is a genuine reproduction of Sigmund et al.'s
  qualitative finding (pool punishment + second-order sanctioning stabilises
  monitoring), in contrast to E5 (collapses) and E11 (delays but does not
  prevent collapse). See [E12](../experiments/E12-pool-punishment.md) for the
  full write-up.
- **The failed first attempt is kept, not deleted**, in the script's docstring
  and this ADR, because the *reason* it failed is itself informative: it
  exposes that this engine's enforcement is cap-only (confiscates upside, does
  not fine below baseline), which is a real, load-bearing property of the
  model worth knowing about for any future sanctioning-design work, not just
  an implementation slip.
- **Cost realism caveat.** As in real institutions, this "works" partly
  because the fine is collected costlessly and with perfect information about
  who is and isn't monitoring — real pool/tax enforcement has its own
  overhead, which this model doesn't charge. Ostrom (1990)'s point that real
  monitoring is cheap only when *engineered* to be a low-cost by-product
  applies here too: this fine is asserted, not derived from any underlying
  mechanism that makes it cheap to collect.
- **Follow-ups:** sweep `POOL_FINE_PER_ROUND` to find the minimum fine that
  still stabilises monitoring (0.2 was chosen for symmetry with the existing
  monitoring cost, not tuned); test whether combining this with E11's loner
  option changes the speed of convergence; a genuinely adaptive/finite-
  population version, as flagged in ADR-0009, remains a separate, larger
  follow-up.

## Status Notes

Implemented 2026-08-06 as Experiment E12 (pool punishment). Engine untouched;
first (cooperative-only) attempt reverted in favour of the symmetric fine
before this ADR was written up.
