# Social Learning Promotes Institutions for Governing the Commons

Read status: 🟢 read from the PDF.

## Citation
Sigmund, K., De Silva, H., Traulsen, A., & Hauert, C. (2010). Social learning promotes
institutions for governing the commons. *Nature*, 466(7308), 861–863.
https://doi.org/10.1038/nature09203 (received 12 March 2010, accepted 24 May 2010,
published online 14 July 2010; print 12 August 2010).

## Research Problem
Costly punishment can sustain cooperation in public-goods games (PGGs), but two things
about it are unexplained: **emergence** (how can punishers invade a population of
defectors by social learning?) and **stability against second-order free-riders** —
players who contribute to the joint effort but *not* to the sanctions. Among
self-interested agents second-order free-riding should spread (punishers are effectively
altruists whose enforcement everyone enjoys for free), erode the sanctioning system, and
let defectors return. The paper asks whether a *different* sanctioning architecture can
close this second-order hole, and which architecture social learning actually selects
when both compete. Its answer contrasts the standard **peer-punishment** with
**pool-punishment** (a pre-committed, institution-like fund) and shows that rudimentary
sanctioning institutions can emerge among purely self-interested imitators — no
other-regarding preferences, group selection, or top-down authority required.

## Proposed Method
An optional PGG played in a **finite population of fixed size M** with **five strategies**,
evolving under **social learning (payoff-biased imitation)**.

**The public-goods game.** *N ≥ 2* individuals are sampled at random. Each participant may
contribute a fixed amount *c > 0*; the pool is multiplied by *r > 1* and divided among the
*other N − 1* players (a contributor does not benefit from its own contribution). If all
contribute, each nets *(r − 1)c*; if none do, payoff is 0 — the social dilemma.
Participation is **optional**: a non-participant opts out and earns a fixed solitary payoff
*σ*, independent of everyone else. A lone would-be participant (nobody else joins) also gets
*σ*. The enabling inequality is `0 < σ < (r − 1)c` (pool case: `0 < σ < (r − 1)c − G`): the
venture is *risky* (all-defect pays less than opting out) yet *promising* (all-contribute
beats opting out).

**The five strategies** (counts sum to *M*):
- **X — cooperators**: participate and contribute, do not punish.
- **Y — defectors**: participate but contribute neither to the PGG nor to sanctions.
- **Z — non-participants / loners**: opt out for the fixed payoff *σ*.
- **V — pool-punishers**: contribute *c* to the PGG **and**, *beforehand*, an amount *G* to a
  punishment pool.
- **W — peer-punishers**: contribute *c* to the PGG and, *after* the game, fine each free-rider.

**PEER punishment vs POOL punishment — the core distinction.**
- **Peer-punishment (W)** is *reactive and decentralised*: after seeing the outcome, each
  peer-punisher imposes a fine *β* on every free-rider present, at a private cost *γ* to
  itself. With *N_w* peer-punishers in a group, each defector pays a total fine *βN_w*. The
  punisher pays only when defectors are actually there — "taking law enforcement into their
  own hands." Cost scales with the number of defectors punished, and is **zero when everyone
  contributes**.
- **Pool-punishment (V)** is *pre-committed and institution-like*: the pool-punisher pays *G*
  into a sanctioning fund **before** the collaborative effort, and free-riders are then fined
  *BN_v* (proportional to the number *N_v* of pool-punishers). This is "like paying towards a
  police force." The cost *G* is **paid up front regardless of whether any exploiter shows
  up**, so pool-punishment looks *more* socially expensive than peer-punishment.

**Why the pre-commitment matters for second-order free-riders.** This is the paper's pivot.
If everyone happens to contribute to the public good, a **peer-punisher is behaviourally
indistinguishable from a plain non-punishing cooperator (a second-order free-rider)** —
there is no defector to reveal who *would have* paid to punish. Second-order free-riders can
therefore accumulate by neutral drift undetected, and once punishers are diluted, defectors
invade with impunity. A **pool-punisher, by contrast, has already declared itself** by paying
*G* into the fund. Second-order free-riders (who contribute to the PGG but not to the pool)
are thus **exposed even when everyone contributes**, which makes **second-order punishment**
(fining second-order free-riders the same *BN_v*) actually enforceable. Peer-punishment is
"ill-suited for second-order punishment" (as also found empirically); pool-punishment is
"conducive" to it. A sanctioning institution treats anyone not paying its upkeep as a
defector.

**Social-learning / imitation dynamics.** Random samples of *N* face the joint enterprise;
payoffs are computed per strategy. A player copies another with probability increasing in the
payoff difference, tuned by an **imitation strength *s* ≥ 0** (small *s* ≈ random updating;
*s → ∞* = "strong imitation," always copy the higher payoff). A small **exploration /
mutation rate *μ* ≥ 0** lets players switch strategy at random. This defines a stochastic
process on the frequencies (X, Y, Z, V, W); the authors compute stationary distributions
numerically, obtain closed-form long-run frequencies in a limiting case (Supplementary
Information), and confirm both with individual-based simulations.

## Main Results
Long-run (stationary) frequencies, rare-mutation limit:

- **Pool-punishment alone, no second-order punishment** → (X, Y, Z, V) = **(2, 2, 2, 1)/7**:
  little cooperation, pool-punishers do not take hold.
- **Pool-punishment alone, with second-order punishment** → **(0, 0, 0, 1)**: the population
  is dominated by pool-punishers **enforcing cooperation**. Pool-punishment *requires*
  second-order punishment to work.
- **Peer-punishment alone** → (X, Y, Z, W) = **(2, 2, 2, M+2)/(M+8)**: punishers prevail
  **with or without** second-order punishment — peer-punishment is "little affected by it,"
  and emerges more easily because inequality (2) is weaker than (1).
- **Peer vs pool, no second-order punishment** → (X, Y, Z, V, W) = **(6, 6, 4, 1, 3M+6)/(3M+23)**:
  **peer-punishers win** (they are the cheaper, more *efficient* enforcer).
- **Peer vs pool, WITH second-order punishment** → **(0, 0, 0, 1, 0)**: **pool-punishers take
  over**, displacing peer-punishers — "although the average income is thereby reduced."
- **Compulsory game (remove the loner option, Z = 0)** → in every variant, **only free-riders
  survive**. Optional participation is necessary for *any* punishment to emerge.

**Which architecture social learning favours:** it **depends entirely on second-order
punishment.** Without it, imitation dynamics settle on the efficient **peer-punishers**. With
it, imitation dynamics settle on the pre-committed **pool-punishers** — the more stable but
more expensive institution. The headline trade-off: **"Efficiency is traded for stability."**

**Individual-based picture (Figs. 1–3).** Without second-order punishment (Fig. 1a, 3a),
peer-punishers dominate *most* of the time but cooperation **keeps breaking down**: second-order
free-riders occasionally drift in, defectors then non-participants take over, and peer-punishment
must be re-established — a recurring boom-bust. With second-order punishment (Fig. 1b, 3b),
pool-punishers "eventually establish a very stable regime." In the voluntary game the
**cycle X → Y → Z → X** (cooperators → defectors → loners → cooperators) provides the escape
route from the all-defector state, repeatedly re-opening windows in which a sanctioning system
with second-order punishment can be founded (Fig. 2b); the compulsory game has no such escape and
collapses to defectors for large imitation strength (Fig. 2a).

## Limitations
- **Opt-out is mandatory for the mechanism.** Both punishment types emerge *only* if players
  can decline the joint enterprise. This restricts applicability — the authors explicitly flag
  settings where opting out is impossible (e.g. climate), predicting obligatory participation
  and widespread defection there.
- **Minimalistic "proof of principle."** Deliberately omits quorum-sensing, signalling,
  reputation, opportunism, repeated interactions, and graduated punishment, and **does not
  specify how a pool is actually set up** — the origin of the institution is asserted to be
  spontaneous, not mechanistically modelled.
- **Antisocial punishment excluded.** The claim that peer-punishment becomes "cost-free" in
  long-enough games rests on assuming players avoid antisocial punishment of contributors — a
  feature left out of the model but empirically real.
- **Pure self-interest, no preferences.** Reciprocity/equity preferences are deliberately not
  assumed; the authors concede such preferences exist and may themselves be a *product* of long
  histories of sanctioning institutions (so the model is about origins, not present-day motives).
- **Higher-order regress acknowledged but bounded.** Second-order punishment could invite
  third-order free-riders ad infinitum; the paper argues pre-commitment stops the regress at
  order two, but this is a modelling choice, not a proof that higher orders never matter.
- Results are long-run *evolutionary/imitation* statistics in a well-mixed, unstructured
  population — no spatial or network structure; clean analytics live in the rare-mutation limit.

## Relevance to This Project
This paper is the **direct next step after our Experiment E5**. E5 ran replicator dynamics on
`sanctioning` (cooperate + pay to monitor) vs `cooperative` (cooperate, free-ride on monitoring)
vs `selfish`, and found **voluntary monitoring is not evolutionarily stable**: monitors erode
because non-monitoring cooperators enjoy enforcement without paying for it (the classic
**second-order free-rider**), and once monitors hit zero the resource cliff-drops from 0.50 to
0 and selfish agents fixate. Our `sanctioning` strategy is **peer-punishment-like**: it is
reactive and self-financed, and — exactly as Sigmund et al. explain — a monitor who cooperates
is *indistinguishable from a second-order free-rider whenever the commons looks healthy*, which
is precisely why our E5 monitors drift/erode away silently before the collapse.

Sigmund et al. 2010 supplies two ingredients our E5 lacks and tells us what each buys:
1. **A "pool" / pre-committed institutional variant of sanctioning.** Because pool-punishers
   *declare themselves up front*, second-order free-riders are exposed *even while the commons is
   healthy* — the exact blind spot that kills E5's monitors during their quiet erosion phase.
   This makes **second-order sanctioning enforceable**, which is the paper's mechanism for
   stability. It maps onto E5's own listed follow-up ("let sanctioners also penalise
   non-monitoring cooperators").
2. **The efficiency-vs-stability trade-off.** Their result predicts a pool/institutional
   sanctioner would be *more expensive* than our peer-like `sanctioning` (a standing monitoring
   cost paid every round regardless of defector presence) but *evolutionarily robust* where our
   peer-like monitor is not. That is a concrete, testable contrast to run against E5's collapse.

Note one gap to bridge: their rescue also relies on **optional participation** (the loner *σ*
and the X→Y→Z→X cycle), which is the Hauert et al. (2007) mechanism our E5 also omits. Sigmund
et al. is best read as: *even with* an opt-out, plain peer-punishment only boom-busts; genuine
stability needs the **pool + second-order** combination. So for E5, "add a loner" and "add a
pre-committed pool with second-order sanctioning" are complementary, not alternative, fixes.

## Possible Follow-Up Contribution
A bachelor-feasible, reproducible extension of E5 — **add a `pool_sanctioning` strategy** and
compare it head-to-head with the existing peer-like `sanctioning`:

1. **Mechanism.** Give `pool_sanctioning` a *fixed per-round upkeep* `G` paid **before** the
   round (charged whether or not defectors appear), funding enforcement whose strength scales
   with the pool-punisher share `N_v`. Defectors are docked `B·N_v`. Keep the existing
   `sanctioning` as the peer baseline (cost paid only when it enforces).
2. **Second-order sanctioning (the decisive knob).** Let the pool also penalise **second-order
   free-riders** — `cooperative` agents that do not pay into the pool — by the same `B·N_v`.
   Sigmund et al. predict this flips the outcome: *without* it the pool erodes like E5's monitors;
   *with* it the pool becomes the stable long-run attractor. Running the replicator with the
   second-order term off vs on is a clean, single-variable reproduction of the paper's central
   claim inside our own CPR model.
3. **Predictions to test.** (a) Peer `sanctioning` reproduces E5's erosion-then-collapse.
   (b) `pool_sanctioning` *without* second-order punishment also erodes (pre-commitment alone is
   not enough). (c) `pool_sanctioning` *with* second-order punishment stabilises monitoring and
   keeps sustainability up — at a **lower mean payoff** than the peer case would transiently
   achieve (efficiency traded for stability). (d) In a three-way peer-vs-pool-vs-cooperator
   contest, second-order punishment is what decides whether peer or pool wins — matching their
   (6,6,4,1,3M+6)/(3M+23) vs (0,0,0,1,0) result.
4. **Combine with the loner follow-up** already on E5's list (optional participation + mutation)
   to see whether the X→Y→Z→X escape cycle plus a pool institution together yield a *persistently*
   monitored commons rather than E5's one-way collapse.

This turns E5's negative result into a positive, mechanistic contribution and directly tests a
named prediction of a Nature paper in our own minimal simulator.

## Important Terms
- **Peer-punishment** — decentralised, reactive sanctioning: a contributor fines each defector
  *β* at private cost *γ*, only when defectors are present; cost is zero if all contribute.
- **Pool-punishment** — pre-committed, institution-like sanctioning: pay *G* into a fund
  *before* the game; free-riders (and, under second-order punishment, second-order free-riders)
  are fined *B·N_v* proportional to the number of pool-punishers.
- **Second-order free-rider** — a player who contributes to the joint effort but not to the
  sanctions; enjoys enforcement for free and erodes it. *Invisible under peer-punishment when
  everyone contributes; visible under pool-punishment because commitment is declared up front.*
- **Second-order punishment** — sanctioning the second-order free-riders themselves; enforceable
  under pool-punishment, ill-suited to peer-punishment; the switch that makes pool-punishment win.
- **Sanctioning institution / punishment fund** — a rudimentary self-governing enforcement body
  ("hiring an enforcer," "paying towards a police force") that pool-punishment approximates.
- **Optional participation / loner** — the opt-out strategy earning fixed payoff *σ*; necessary
  for any punishment to emerge, and the source of the X→Y→Z→X rescue cycle.
- **Imitation strength *s* / exploration rate *μ*** — social-learning parameters: how strongly
  players copy higher payoffs, and how often they switch strategy at random.
- **Efficiency traded for stability** — the paper's core trade-off: peer-punishment is cheaper
  (efficient) but boom-busts; pool-punishment is dearer but evolutionarily stable.

## Questions
- Our simulator's enforcement is "any one monitor enforces fully" (ADR-0005). To port
  pool-punishment faithfully we need enforcement **proportional to the pool-punisher share
  `N_v`**; does adopting that also change the *peer* baseline's behaviour, confounding the
  peer-vs-pool comparison? (Probably need the proportional-enforcement follow-up first.)
- The paper's second-order punishment presupposes the pool can *observe* who paid in. In our
  model, does "monitoring who monitors" require a second monitoring layer with its own cost, or
  is pool membership free to observe by construction (the pre-commitment being public)?
- Does the pool rescue survive our **deterministic replicator** setting, or does it — like the
  Hauert loner rescue — really need finite-population stochasticity (drift + exploration *μ*) to
  seed the institution? E5 is deterministic and has no mutation term.
- Their stability result is stated in the rare-mutation limit; at the mutation/selection regime
  we would actually simulate, how large is the stable pool basin — a wide region or a narrow
  window in (`G`, `B`, `σ`) space?
- Is the "average income is reduced" cost of pool-punishment large enough in our CPR payoffs to
  matter for the sustainability metric, or does the resource-health gain dominate net welfare?
