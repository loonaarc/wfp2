# Altruistic Punishment in Humans

Read status: 🟢 read from the PDF.

## Citation
Fehr, E., & Gächter, S. (2002). Altruistic punishment in humans. *Nature*, 415(6868),
137–140. https://doi.org/10.1038/415137a

## Research Problem
Human cooperation among genetically unrelated strangers, in large groups, in
non-repeated interactions, and where reputation gains are small or absent, is an
evolutionary puzzle that kin selection, direct/indirect reciprocity, and costly
signalling do not readily explain. The paper tests experimentally whether *altruistic
punishment* — costly punishing of defectors that yields the punisher no material gain —
is a key mechanism that establishes and sustains cooperation.

## Why the Problem Is Difficult
Punishing free riders is itself a second-order public good. Everyone benefits if free
riding is deterred, but punishing is costly and returns nothing to the punisher, so a
purely self-interested individual should never punish (and should free-ride on others'
punishment). The design deliberately removes every selfish escape route: groups are
re-randomised each period so no pair ever meets twice, and no reputation can form
(Methods). Under these rules a purely selfish subject should neither cooperate nor
punish. So observed punishment cannot be explained by reciprocity, reputation, or
signalling — it must be genuinely altruistic.

## Experimental Setup
- **Subjects:** 240 undergraduates (31% female) from University of Zürich and ETH,
  recruited across many disciplines to minimise prior acquaintance. Ten sessions of 24
  subjects each. Software: z-Tree; subjects in separate booths, fully anonymous.
- **Game:** linear public-goods game in groups of 4. Endowment 20 money units (MUs) per
  member per period; contribute 0–20 to a project. Marginal per-capita return = 0.4 MU
  per MU invested (private return 0.4 < cost 1, so free-riding is the dominant selfish
  strategy), group return = 1.6 MU. Full defection yields 20 MU each; full cooperation
  yields 0.4 × 80 = 32 MU each.
- **Two conditions:** *punishment* vs *no punishment*. In the punishment condition,
  after seeing others' contributions each member could assign 0–10 punishment points to
  each other member; each point cost the punished 3 MU and the punisher 1 MU (3:1
  ratio). All decisions simultaneous.
- **Repetition / matching:** each condition run for 6 periods. Groups re-formed every
  period ("perfect stranger" / stranger matching — no subject meets another more than
  once within a treatment; undisclosed history) to rule out direct reciprocity and
  reputation.
- **Order control:** each subject played both a 6-period no-punishment game and a
  6-period punishment game. In 5 sessions punishment came first; in 5 sessions it came
  second. Subjects did not know a second game would follow until after period 6.
- **Emotion elicitation:** after the final period, hypothetical free-rider scenarios
  measured anger/annoyance toward a free rider (and free riders' expected anger) on a
  1–7 scale; also run on 33 non-participants as a control.
- Average earnings 39.7 Swiss francs (~US$23.95) per ~60-min session.

## Metrics
- Mean contribution (investment) to the public good per period, by condition.
- Frequency, targeting, and magnitude of punishment (MUs spent) as a function of a
  member's deviation from the others' mean contribution.
- Behavioural response to being punished (change in next-period investment).
- Self-reported anger intensity (1–7) toward free riders, actual and expected.
- Nonparametric tests (Wilcoxon signed-rank, Mann–Whitney) on session-level matched
  observations; Tobit regressions for punishment vs deviation.

## Main Results
- **Punishment occurred frequently and was targeted.** Across the 10 sessions subjects
  punished 1,270 times. 84.3% of subjects punished at least once, 34.3% more than five
  times, 9.3% more than ten times. 74.2% of punishment acts were by above-average
  contributors against below-average contributors.
- **Punishment scales with defection.** Tobit regression: coefficient on *negative*
  deviation = 0.622 (z = 18.1, P < 0.0005); on *positive* deviation = −0.149 (z = −2.86,
  P < 0.004). A 10-MU larger negative deviation raised others' punishment spending by
  6.22 MU, implying a ~18.66 MU payoff reduction on the defector. Punishment strength
  was stable over time (periods 1–4 vs 5–6: z = −1.07, P = 0.285).
- **Cooperation flourishes with punishment, collapses without it.** Pooling all 10
  sessions, mean investment was significantly higher with punishment (Wilcoxon, 10
  matched obs, z = 2.803, P = 0.005). Punishment-first sessions: 94.2% of subjects
  invested more under punishment; no-punishment-first sessions: 91.4% did.
- **Divergent time trends.** With punishment, cooperation rises over the 6 periods;
  without it, it decays. In the **final** period of the *punishment* condition, 38.9% of
  subjects contributed their **entire** 20-MU endowment and 77.8% contributed ≥15 MU. In
  the final period of the *no-punishment* condition, 58.9% contributed **nothing** and
  75.6% contributed ≤5 MU.
- **Threat is immediately effective and order-independent.** When punishment was turned
  on there was an immediate upward jump in investment (and a drop when removed);
  treatment sequence had no effect (Mann–Whitney, punishment condition z = 0.104,
  P = 0.918).
- **Actual punishment changes behaviour.** A subject punished before period 6 raised
  investment the next period by 1.62 MU on average — a benefit that accrues to future
  (different) group members, not to the punisher, hence "altruistic."
- **Negative emotion is the proximate driver.** In the high-contribution scenario, 47%
  of subjects reported anger 6–7 and 37% reported 5 toward a free rider; anger fell
  significantly when the free rider deviated less (z = 9.636, P < 0.0005). Expected anger
  was even higher: 74.5% of hypothetical free riders expected others' anger at 6–7. The
  same patterns held in the 33-person non-participant control.

## Limitations
- Lab setting, modest monetary stakes, WEIRD student sample; only 6 periods per
  condition.
- Punishment is frictionless, perfectly targeted, and available to everyone at a fixed
  3:1 cost ratio; no error, collusion, or anti-social/retaliatory punishment modelled.
- The study *demonstrates* altruistic punishment but does not resolve **how** such
  costly punishing dispositions are evolutionarily sustained (who bears the cost in
  equilibrium — the second-order problem it names but does not solve).
- Emotions are inferred from *hypothetical* post-hoc scenarios, not measured during play.
- Stranger matching only; no test of whether the effect persists in fixed groups or at
  larger scale.

## Relevance to This Project
This is the empirical backbone for **Experiment E3**: enforcement/sanctioning sustains
cooperation where unstructured cooperation decays. Our CPR simulation reproduces the
*direction* of this finding. Two differences are load-bearing and must be stated
explicitly:
- **Mechanism of the effect.** Fehr & Gächter's punishment works through *deterrence*:
  it lowers a defector's payoff, and because humans **adapt** (a punished subject raised
  investment by 1.62 MU next period; contributions climb over periods), the mere threat
  changes behaviour. Our selfish agents are **FIXED / non-adaptive**, so payoff-based
  deterrence cannot operate. Our sanctioning instead **caps extraction directly** (ADR-
  0005) to obtain the same protective effect on the resource — confiscation, not
  deterrence. When reporting E3 we should not claim to reproduce their behavioural
  adaptation, only the system-level outcome.
- **Second-order free-rider problem.** Their framing that punishing is costly and
  unrewarded is exactly our E3 finding that **monitors earn less**. The paper names this
  as a second-order public good but leaves it unsolved — so our result inherits the same
  open question rather than answering it.

## Possible Follow-Up Contribution
Add an **adaptive** selfish agent that reduces greed/extraction in response to being
sanctioned. This would let us reproduce Fehr & Gächter-style *deterrence* (behavioural
adaptation to the punishment threat) rather than mechanical extraction-capping, and
directly compare the two enforcement designs — confiscation vs deterrence — in one
reproducible harness. A natural extension is *optional/voluntary* monitoring to probe
whether the second-order free-rider problem (monitors earning less) erodes enforcement
over time, which the paper raises but does not test.

## Important Terms
- **Altruistic punishment** — punishing a defector at a personal cost with no material
  return to the punisher.
- **Public-goods game** — contribute-to-common-project game where marginal private
  return (0.4) < cost (1) but group return (1.6) > 1, so defection is individually
  rational but collectively harmful.
- **Second-order public good / second-order free-rider problem** — punishment benefits
  all but is costly only to the punisher, so who punishes is itself an under-provided
  public good.
- **Stranger ("perfect stranger") matching** — groups re-randomised each period so no
  pair meets twice, ruling out direct reciprocity and reputation.
- **Marginal per-capita return (MPCR)** — here 0.4 MU per MU contributed.
- **Deterrence vs confiscation** — payoff-reducing threat that changes future behaviour
  (Fehr & Gächter) vs directly capping extraction (this project's fixed-agent analogue).

## Questions
- Does the punishment effect persist beyond 6 periods, or does punishment fatigue set in
  as the second-order cost accumulates?
- Their design uses stranger matching only — how much of the cooperation gain would
  survive in fixed (partner) groups where reciprocity is also available?
- In our simulation, is capping extraction genuinely equivalent to their payoff
  deterrence at the *system* level, or does the absence of agent adaptation change the
  equilibrium contribution path (their rising trend vs our flat cap)?
- Could an adaptive-agent variant reproduce the immediate upward *jump* in cooperation
  they observe when punishment is switched on?
