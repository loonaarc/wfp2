# Via Freedom to Coercion: The Emergence of Costly Punishment

Read status: 🟢 read from the PDF.

## Citation
Hauert, C., Traulsen, A., Brandt, H., Nowak, M. A., & Sigmund, K. (2007). Via freedom
to coercion: The emergence of costly punishment. *Science*, 316(5833), 1905–1907.
https://doi.org/10.1126/science.1141588

## Research Problem
Costly (peer) punishment can sustain cooperation in public-goods interactions, and any
norm that prescribes punishing defectors is evolutionarily stable *once established* —
an entrenched punisher majority cannot be displaced by a dissident minority. The open
puzzle is **emergence, not stability**: how can costly punishing behavior *gain a
foothold* when it is initially rare? A punisher earns less than a plain cooperator who
contributes but declines to pay the punishment cost, so punishment looks like a
self-undermining altruistic act. The authors call this the **second-order social
dilemma** and quote Colman: "We seem to have replaced the problem of explaining
cooperation with that of explaining altruistic punishment."

## Why the Problem Is Difficult
Two nested free-rider problems stack. First order: non-contributing defectors out-earn
contributors, so imitation drives the population to all-defect. Punishment fixes this by
docking defectors' payoff — but punishing costs the punisher, creating the second order:
among contributors, a cooperator who does *not* punish out-earns a punisher, so
punishment erodes from within even after defectors are gone. In the standard
**compulsory** public-goods game this is fatal: with C and D only, defectors win; adding
punishers as a third strategy does not change the qualitative outcome — the system still
spends almost all its time near the all-defector state. The paper also notes that an
earlier attempt (Fowler 2005) reached the "voluntary rescues punishment" conclusion but
via an ill-founded model (single cooperators playing alone; cooperators punished even
with no defectors present), which yields structurally unstable, inconclusive dynamics in
the infinite-population limit. Hence a properly grounded **finite-population stochastic**
treatment is required.

## Proposed Method
An evolutionary public-goods game with **optional participation** and four strategies in
a well-mixed population of fixed size *M*.

Setup per interaction:
- Every individual has a safe, fixed solitary income *s* (written σ in the figures). *N*
  individuals are sampled at random and offered the joint enterprise.
- **Nonparticipants / loners** (count *z*) decline and simply keep the fixed payoff *s*,
  independent of everyone else's behavior. **Participants** are of three kinds:
  **cooperators** (*x*) contribute cost *c* but do not punish; **defectors** (*y*)
  contribute nothing but share the proceeds; **punishers** (*w*) contribute *and* fine
  defectors. *M = x + y + z + w*.
- Among the *N* sampled there are on average N_x cooperators, N_y defectors, N_z loners,
  N_w punishers. The group actually playing has size *S = N_x + N_y + N_w*. If *S > 1*
  each participant receives r(N_x + N_w)c / S from the multiplied (factor *r > 1*) common
  pool. Contributors (cooperators and punishers) additionally pay *c*; each defector's
  payoff is docked *b·N_w* (fined *b* by every punisher present); each punisher pays
  *g·N_y* (cost *g*, written γ, per defector fined). If *S = 1* the game does not happen
  and the lone volunteer just gets *s*.
- Key inequality **0 < s < (r − 1)c**: the enterprise is *risky* (all-defect pays less
  than staying a loner) but *promising* (all-cooperate pays more than a loner). This makes
  opting out a genuine, non-trivial choice rather than a dominated option.

Dynamics: **imitation with payoff-biased success** — a player copies another with
probability increasing (linearly) in that other's payoff (implemented as a Moran process,
selection strength s = 0.249), plus a small **mutation** rate *m* (μ) of switching
strategy irrespective of payoff ("blindly experimenting"). In the analytically tractable
limit *m → 0* the population is essentially always monomorphic or a two-type mix; the four
pure states are absorbing, and each mutant's fate (fixation or loss) is decided before the
next mutant arrives, so the process reduces to transition probabilities between the four
homogeneous states C, D, N, P.

## Main Results
- **Voluntary game: punishers dominate.** In the rare-mutation limit the system spends
  most of its time in the homogeneous **punisher** state, *irrespective of the initial
  composition* and robustly across *s* and *r* (Figs. 1A, 2A: P ≈ 72%, C ≈ 14%, N ≈ 9%,
  D ≈ 5%). Punishers can invade and predominate.
- **Compulsory game: defectors dominate.** Remove the loner option and the system sits in
  the all-defector state, even when *initialized* with punishers, with almost no economic
  benefit from the interaction (Figs. 1B, 2B). "Joint enterprises that are compulsory
  rather than voluntary are less likely to lead to cooperation."
- **How the loner rescues costly punishment (the crux).** Optional participation is what
  makes punishing *cheap enough to invade*. When loners are common, few people join, so
  the realized group size *S* is small; small groups contain few defectors, so a punisher
  pays little total punishment cost (its dock g·N_y is small when N_y is small). The payoff
  gap between a punisher and a non-punishing cooperator — the engine of the second-order
  dilemma — therefore shrinks toward zero, and punishers can drift/invade into a foothold.
  Because the loner payoff also undercuts defectors (all-defect earns less than opting
  out), defection is no longer a stable absorbing outcome; the population keeps being
  pushed back to the small-group, few-defector regime where punishment is nearly free.
  Once punishers reach their monomorphic state, that state is evolutionarily stable and
  they persist. Freedom to abstain thus paves the way to enforcement — "via freedom to
  coercion."
- **Cyclic (rock-paper-scissors) dynamics.** With optional participation but *no*
  punishment (only C, D, N), cooperation never fixates; instead the three strategies chase
  each other in an RPS cycle: many defectors → joining doesn't pay → loners rise → group
  size shrinks → the social dilemma vanishes (cooperators now out-earn defectors *and*
  loners) → cooperators spread → group size grows → dilemma returns → defectors rise again
  (Fig. 3A). With punishers added, the same oscillatory mechanism (a transient
  rock-paper-scissors succession of C, D, N) repeatedly regenerates the small-group windows
  in which punishers can climb, and the punisher regime, once reached, absorbs the dynamics
  — occasionally broken by cooperators invading via neutral drift, after which oscillations
  resume and punishers re-emerge (Fig. 1A).
- **Targeting matters; more coercion is not better.** Second-order punishment (punishers
  also fining non-punishing cooperators, strength α) barely changes anything, because at
  small *m* punishers, cooperators and defectors rarely coexist, so non-punishers are
  seldom observed and held accountable (and empirical evidence for punishing non-punishers
  is lacking). Punishing *nonparticipants/loners* (strength δ) stabilizes punishment once
  established but *hinders its emergence* and can even be counterproductive (Fig. 3B):
  "The system responds to an increase in compulsion with a decrease in cooperation."
  Punishment is best aimed at defectors only.

## Limitations
- Stylized, well-mixed (no spatial/network structure), constant population size, fixed
  payoff parameters; results are about long-run evolutionary/imitation dynamics, not
  individual rational deliberation.
- The clean analytic result lives in the **rare-mutation limit (m → 0)**; substantial
  mutation rates require numerical simulation, and outcomes there can shift (e.g. in the
  compulsory game, large mutation rates supplying defectors can keep punishers active).
- "Opting out" is idealized as a single fixed, safe payoff *s* — an abstraction of
  heterogeneous outside options; and the whole loner rescue presupposes that opting out is
  actually *possible*. The authors flag cases where it is not (e.g. climate), predicting
  obligatory participation and widespread defection there.
- Emergence is shown; the transition from opting-out to full institutions (ostracism →
  sanctioning institutions) is argued verbally, not modeled.

## Relevance to This Project
This is the direct theoretical counterpart to our **Experiment E5**. In E5 we ran
replicator dynamics on a monitoring/sanctioning strategy and found voluntary monitoring is
**not evolutionarily stable**: monitors bear a private cost, get out-competed by
non-monitoring cooperators (the classic second-order free-rider), monitoring erodes, and
the commons then collapses. That is exactly the compulsory-game result here (Fig. 1B/2B):
punishers cannot hold, defectors win. Hauert et al. supply the missing ingredient our E5
model lacks — an **exit option**. Their loner is a fixed-payoff opt-out that (i) caps how
large the participating group gets, so monitoring/punishment stays cheap when defectors are
scarce, closing the second-order payoff gap, and (ii) denies defectors a stable
absorbing state, forcing the RPS cycle that repeatedly re-opens invasion windows for
enforcers. Our E5 replicator setup has no such opt-out and no mutation term, so it flows
straight to the monitor-free, then cooperator-free, collapse — with no mechanism to
regenerate enforcement. The paper predicts that adding either an opt-out strategy or a
small mutation/experimentation rate should qualitatively change our E5 outcome.

## Possible Follow-Up Contribution
Extend the E5 replicator experiment minimally and reproducibly:
1. **Add a loner strategy** with a fixed payoff *s* satisfying 0 < s < (r − 1)c, and make
   the effective group size depend on how many agents opt in (so monitoring cost scales
   with the number of defectors actually present). Test whether monitors/sanctioners stop
   eroding and whether an RPS-style cycle (cooperators ⇄ defectors ⇄ loners) appears, with
   the sanctioner state becoming the long-run attractor.
2. **Add a small mutation/experimentation term** to the replicator (or move to a
   finite-population Moran process) and check the rare-mutation prediction that the system
   spends most time near the sanctioner state regardless of initial mix.
3. **Sweep the loner payoff *s* and the monitoring cost *g*** to map the boundary between
   "monitoring survives" and "commons collapses," and confirm the paper's counter-intuitive
   corollary that *punishing the opt-out itself* (δ > 0) hurts rather than helps emergence.
This turns E5's negative result into a positive, mechanistic one and stays squarely
bachelor-feasible.

## Important Terms
- **Second-order free-rider / second-order social dilemma** — non-punishing cooperators
  out-earn punishers, so punishment is itself vulnerable to free-riding.
- **Optional participation / loner (nonparticipant)** — strategy of abstaining for a fixed,
  safe payoff *s* independent of others; the paper's central mechanism.
- **Costly / peer punishment** — a contributor fines each defector *b* at private cost *g*.
- **Rock-paper-scissors (cyclic) dynamics** — C beats no one stably; the C→D→N→C cycle
  driven by group-size feedback under optional participation.
- **Rare-mutation limit (m → 0)** — regime where the population is near-monomorphic and
  dynamics reduce to transitions between pure states (analyzed via a Moran process).
- **Evolutionary stability of an established norm** — a punisher majority resists invasion,
  even though it could not have arisen by that same logic (the emergence puzzle).
- **Compulsory vs. voluntary joint enterprise** — the paper's key contrast; compulsion
  → defection, freedom to exit → enforcement.

## Questions
- Our E5 uses deterministic replicator dynamics; does the loner rescue need the
  *finite-population stochastic* setting (drift-assisted invasion of near-neutral
  punishers), or does an opt-out alone flip a deterministic replicator model too?
- How sensitive is the rescue to the loner payoff *s* and the punishment cost *g* in our
  parameterization — is there a usable stable region, or only a narrow window?
- The paper's group-size feedback is essential (small groups make punishment cheap). Does
  our E5 payoff structure actually encode monitoring cost as scaling with the number of
  defectors present? If not, that coupling must be added for the mechanism to transfer.
- Does the "punishing the opt-out backfires" (δ > 0) result also hold in a rule-based /
  replicator analogue, and would it caution against modeling ostracism as cheap in our
  commons?
