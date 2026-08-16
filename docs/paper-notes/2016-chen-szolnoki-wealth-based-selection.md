# Individual Wealth-Based Selection Supports Cooperation in Spatial Public Goods Games

Read status: 🟢 read (open-access article, `nature.com/articles/srep32802`, no PDF
needed — Scientific Reports publishes under CC BY 4.0).

## Citation
Chen, X., & Szolnoki, A. (2016). Individual wealth-based selection supports
cooperation in spatial public goods games. *Scientific Reports*, 6, 32802.
https://doi.org/10.1038/srep32802

## Research Problem
In spatial public goods games, letting agents *choose* whether to participate
each round (rather than being forced to play) is already known to help
cooperation (voluntary participation, "optional public goods game"). Does
making that participation decision depend on an agent's own **accumulated
wealth** (past payoffs), rather than being a free, uniform-probability choice,
change — and specifically improve — cooperation further?

## Why the Problem Is Difficult
Prior optional-participation models treat the decision to join a public goods
round as free and independent of history — every agent, rich or poor in
accumulated payoff, has the same odds of participating. This ignores that in
real cooperative institutions, participation often *does* depend on
accumulated standing (credit, reputation capital, resources needed to buy in)
— but naively adding a wealth requirement risks simply excluding the poor
(who are disproportionately likely to be exploited cooperators, not just
lazy defectors), which could make things worse, not better. The paper needs
to show the wealth-gating mechanism actually tracks *behavior* (who is
extractive vs. who reinvests) rather than just re-partitioning the population
by initial luck.

## Proposed Method
A spatial (lattice) public goods game where each agent additionally tracks
cumulative wealth `w` from past payoffs. Participation in a given round's
group public-goods game requires **both**: (1) wealth above a threshold
`W_T`, and (2) succeeding at a per-round participation probability `p` (a
cost `g` is paid to attempt participation). Cooperators contribute to the
group pool (multiplied by synergy factor `r`, split among participants);
defectors free-ride on the pool without contributing. Strategy imitation
follows standard payoff-proportional copying from spatial neighbours (Fermi
rule). The wealth threshold is the paper's one new mechanism layered on top
of the existing optional-participation baseline.

## Experimental Setup
Monte Carlo simulation on a square lattice (spatial, not well-mixed), varying
synergy factor `r`, participation cost `g`, participation probability `p`,
and the wealth threshold `W_T`; standard evolutionary-game convergence
metrics (fraction of cooperators at steady state) across the parameter space.

## Metrics
Steady-state cooperator fraction across the `(r, W_T)` and related parameter
planes; phase diagrams showing where cooperation dominates, coexists with
defection, or collapses.

## Main Results
- **Wealth-based exclusion disproportionately locks out defectors, not
  cooperators — the mechanism is genuinely self-correcting, not just a
  second lottery.** Because defection is destructive to a defector's own
  future income (it erodes the neighbouring cooperator pool it free-rides
  on), sustained defection drives a defector's own wealth down over time;
  cooperators, by contrast, sustain each other's wealth through the
  multiplied pool payout and so remain qualified to keep participating.
- **This expands the parameter region where cooperation survives**, beyond
  what probabilistic participation alone achieves — the wealth filter adds a
  second, behavior-tracking layer on top of the existing participation-cost
  mechanism, rather than substituting for it.
- **The effect specifically depends on spatial structure**: the mechanism
  works because a defector's wealth erosion comes from exhausting its own
  *local* cooperator neighbours — in a well-mixed population, this
  spatial-depletion channel wouldn't operate the same way.

## Limitations
- **Lattice/spatial only** — the mechanism's dependence on local
  neighbourhoods is central to the result, not incidental; the paper doesn't
  test a well-mixed (fully-connected) population as a contrast case.
- Wealth is a pure derived quantity (cumulative past payoff) — no
  independent "starting wealth"/inequality dimension is varied; the paper is
  about wealth as a *behavioral signal*, not about pre-existing inequality
  or redistribution.
- No monitoring, sanctioning, or costly enforcement of any kind — the wealth
  threshold is a passive participation gate, not an active punishment
  mechanism.

## Future Work
Not stated as a dedicated section; the mechanism is presented as
extensible to other network structures and other participation-cost
functions, without a specific named next step.

## Relevance to This Project
- **Directly buildable, but not the mechanism originally scoped for item 12
  in `thesis-direction-equifinality.md`.** That item's original framing
  ("inequality-adaptive monitoring investment," a Gini-sensitive fitness
  function in the E5/E11/E12 evolutionary-dynamics machinery) has no precise
  match here — this paper is about wealth-gated *participation*, not
  monitoring-investment decisions scaling with population-level inequality.
  Read in full specifically to check the fit before building, per this
  project's own practice — see E23/ADR-0019 for the resulting scope pivot.
- **`Observation.own_total_payoff` already exists and is currently unused by
  every registered strategy** — a wealth-participation gate is a small,
  additive engine change (a floor on `own_total_payoff` for eligibility to
  request that round), not a new field.
- **The paper's own headline mechanism explicitly depends on spatial
  structure** — this project already has exactly that structure available
  and optional (`NetworkConfig`, E19/ADR-0015, a fixed neighbour graph). A
  faithful test of this paper's finding should compare the well-mixed
  default against the E19 network structure, not assume the effect
  transfers to a well-mixed population.

## Possible Follow-Up Contribution
Add a wealth-participation threshold to `AgentSpec`/the engine's per-round
eligibility check (an agent whose `own_total_payoff` falls below a
configured floor cannot request that round), and test it two ways: does it
protect the shared pool against free-riders in this project's default
well-mixed setting, and does the effect depend on combining it with E19's
fixed-neighbour-graph structure, matching this paper's own spatial
dependency claim.

## Important Terms
- **Wealth-based participation gate** — a threshold `W_T` on accumulated
  payoff below which an agent cannot participate in the current round.
- **Optional / voluntary public goods game** — participation is a choice,
  not mandatory, the pre-existing baseline this paper's wealth gate is
  layered on top of.
- **Spatial reciprocity** — cooperation sustained via local clustering on a
  lattice/network, distinct from well-mixed population dynamics.

## Questions
- Does this project's single shared pool (not a per-neighbour local public
  good) preserve the "defection erodes the defector's own future income"
  channel this paper's mechanism depends on, or does well-mixed sharing
  dilute it enough that the effect disappears without network structure?
  This is exactly what E23's own Q2 (wealth gate × network structure) tests
  directly rather than assuming.
