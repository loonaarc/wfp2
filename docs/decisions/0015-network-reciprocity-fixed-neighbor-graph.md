# ADR-0015: Network reciprocity as a fixed neighbour graph on reputation's partner selection

- **Status:** Accepted
- **Date:** 2026-08-15
- **Deciders:** project owner (approved scope after the first attempt was rejected), assistant (implementing)

## Context

Nowak (2006), "Five Rules for the Evolution of Cooperation," rule 4 (network
reciprocity): relax the well-mixed assumption -- individuals occupy the
vertices of a graph and interact only with their `k` graph neighbours, not
the whole population. Plain cooperators can then survive by forming clusters
that mutually protect each other, favoured when `b/c > k`.

This is distinct from rule 5 (group selection, already built as groups/E15,
ADR-0012 -- Nowak's own formula `b/c > 1 + n/m`) and from rule 3 (indirect
reciprocity, already built as reputation/E18, ADR-0014 -- `q > c/b`). The
project owner's explicit brief for this axis: build the version that "makes
the most sense," is "not just more of the same," and is "not just redundant
to other parameters" -- not the least-effort option.

## Considered Options

1. **Graph-structured evolutionary dynamics on top of E5/E11/E12.** *(First
   attempt; built, tested, and rejected.)* Keep the single shared pool
   completely unchanged; replace E5/E11/E12's population-wide replicator
   step with per-node imitation restricted to a fixed ring-lattice neighbour
   (a standard Fermi/pairwise-comparison update). Implemented as
   `scripts/experiment_network_reciprocity.py` (evolutionary version) and
   run across `k in {2, 4, 8, N-1}`: monitoring collapsed at every degree
   tested, with no visible effect from `k` at all.

   **Why it was rejected, not just re-tuned:** fitness was still computed as
   the *population-wide mean payoff per strategy* (exactly E5/E11/E12's own
   `_measure()`), because every agent of the same strategy sees the same
   aggregate stock and requests the same amount -- there is no per-agent
   payoff variance to begin with. Making only the *imitation* step local
   while every node's *fitness* stayed a single population-wide number could
   never reproduce Nowak's actual mechanism, which depends on a monitor
   surrounded by monitors genuinely earning more than one surrounded by
   defectors. In this project's single shared pool, any protective action
   (any monitor capping any free-rider) benefits the *whole population*
   equally -- a monitor's protection is a public good, not a pairwise
   donor-recipient transfer the way Nowak's toy model assumes. Local
   imitation on top of structurally-global fitness was mechanically
   guaranteed to make `k` matter little to not at all; the null result would
   have been an artifact of the operationalization, not a real finding, and
   is exactly the kind of "invented mechanism that doesn't test the real
   thing" this project has been trying to catch before it ships (see
   ADR-0014's own rejected Option 2, and `complexity-synthesis.md`'s
   methodological lessons).
2. **A genuinely local sub-pool per neighbourhood.** Give each neighbourhood
   its own slice of the resource, so protection is inherently local. Rejected
   as out of scope for this axis: it would either collide with the
   explicitly-deferred spatial/grid environment
   (`decisions/0001-custom-simulation-core.md`) or duplicate the "multiple
   resources" candidate axis, which is its own, differently-motivated future
   direction (dividing effort across distinct resources, not restricting who
   competes for one).
3. **A fixed neighbour graph on reputation's (E18) partner selection.**
   *(Chosen.)* E18 already has a genuinely individual, position-*capable*
   interaction: a reputation cooperator's harvest decision depends on one
   specific partner, not a population aggregate. E18's own partner is
   redrawn fresh and uniformly at random every round, though, so no agent
   has a persistent graph position -- structurally closer to Nowak's rule 3
   (indirect reciprocity, "who happens to have heard about whom") than rule
   4. Building a ring lattice that fixes *which* agents can ever be drawn as
   a partner, persistent across the whole run, is the one change that turns
   E18's already-individual mechanic into a genuinely graph-structured one --
   and it is a small, surgical change (`NetworkConfig` + one branch in
   `Simulation._observe`), not a new strategy or a second core-engine
   overhaul.

## Decision

Option 3. A new `NetworkConfig` (`core/config.py`), referenced by
`SimulationConfig.network: NetworkConfig | None`, holding one field:
`degree` (`k`, must be even, checked `< num_agents`). `Simulation.__init__`
builds a fixed ring-lattice adjacency list once from agent order
(`_ring_lattice`, a module-level pure function) when `network` is
configured. `_observe` draws the reputation partner from that agent's fixed
neighbour list instead of the whole population when `self._neighbors` is
set; when `network` is `None` the code path -- and its RNG call sequence --
is byte-for-byte what ADR-0014 already does, so every existing reputation
config and test is unaffected (confirmed: all 115 pre-existing tests still
pass unchanged).

`NetworkConfig` has no effect without `SimulationConfig.reputation` also
configured, the same relationship `ReputationConfig` already has with
`reputation_cooperator` -- a config that changes nothing unless something
downstream actually reads it.

## Rationale

- **Persistence is the one ingredient neither existing mechanism has.**
  Groups (E15) are a hard, disjoint, *permanent* partition. Reputation (E18)
  is the opposite extreme: a fresh random partner *every single round*, so
  no relationship persists and no clustering can ever form. A fixed graph
  sits between them -- the same two agents interact repeatedly, so a
  cluster of cooperators can genuinely protect each other over time, and an
  agent's outcome can depend on *where it sits*, not just the population's
  aggregate composition. That is a structurally new capability, not a
  relabelling of an existing one.
- **It required admitting the first attempt didn't work**, rather than
  reporting a flat "k doesn't matter" result as if it were a finding.
  Catching that the evolutionary-dynamics version couldn't produce local
  payoff variance *before* writing it up avoided shipping a null result that
  was actually a modelling artifact.
- **Minimal, surgical engine change** -- one new frozen dataclass, one field
  on `SimulationConfig`, one branch in one method, reusing every other piece
  of ADR-0014's already-validated bookkeeping (the reputation score itself,
  the strategy's `decide()` logic, the visibility roll) unchanged.

## Consequences

- **A real, non-obvious empirical result exists, and it does not test
  `b/c > k` literally** (see Context above for why that formula does not
  transfer to a public-good enforcement benefit). What it *does* show
  (E19): at a sparse ring (`k=2`), the free-rider's two fixed neighbours
  earn a mean payoff of ~117 across 20 seeds, while agents on the far side
  of the ring earn ~5 -- a large, mechanistically clear inequality driven
  purely by graph position. Under well-mixed reputation (E18's own setup,
  `network=None`), the same agent-index labels earn statistically similar
  amounts (~37 vs. ~41) -- there is no "position" for a well-mixed
  mechanism to depend on. This is something neither E18 nor any other
  mechanism in this project can produce, even in principle.
- **Population-level sustainability is roughly flat across degree**
  (0.12-0.14 across `k in {2, 4, 6}` and well-mixed) -- the free-rider's own
  behaviour doesn't depend on the network at all, so its damage to the one
  shared pool is largely unaffected by who else is nearby. The interesting
  effect this experiment surfaces is distributional (who bears the cost),
  not aggregate (whether the pool survives) -- a genuinely different kind of
  claim than E14-E16's near-optimal-*set-size* framing, see
  `complexity-synthesis.md`'s own scoping note for this axis.
- **Orthogonal to groups/boundaries**, the same way reputation already is
  (ADR-0014's own Consequences): the neighbour graph is built from raw agent
  order, not `AgentSpec.group`; combining them is possible but untested.
- **Option 1's evolutionary-dynamics script is not published** as an
  experiment (no results directory, no report) -- it is documented here, in
  this ADR, as the considered-and-rejected path, per this project's own
  standing practice of keeping a record of what was tried and why it failed
  (see ADR-0009, ADR-0010, ADR-0014's own Option 2).

## Status Notes

Built as **E19** (`scripts/experiment_network_reciprocity.py`,
[docs/experiments/E19-network-reciprocity.md](../experiments/E19-network-reciprocity.md)).
Ported to the browser demo (`web/commons-demo.html`) as a network-topology
toggle + degree slider on the existing reputation panel, with a persistent
faint ring-lattice overlay distinguishing it from the per-round highlighted
pairing arrows.
