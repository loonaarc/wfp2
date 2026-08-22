# Birth, Death and Public Good Provision

Read status: 🟢 read in full (open-access working-paper PDF hosted on the
author's own page, `sites.socsci.uci.edu/~duffy/papers/EE.pdf`, no paywall).

## 1. Citation
Duffy, J., & Lafky, J. (2015). Birth, death and public good provision.
*Experimental Economics*, 19, 317–341. https://doi.org/10.1007/s10683-015-9439-y

## 2. Research Problem
A robust finding across public-goods-game experiments is "over-contribution
and decay": subjects start generous and steadily reduce contributions toward
zero as a fixed, known-length repeated game nears its end. Real groups,
though, rarely have every member start and end together — residents move
into and out of neighbourhoods, donors join and lapse, voters enter and exit
districts. Does replacing a fixed cohort with realistic, staggered turnover
(new members entering as old ones leave, no common end date shared by
everyone) change how contributions decay?

## 3. Why the Problem Is Difficult
Existing theory gives no clean prediction. A learning/adaptation account of
decay would predict *higher* contributions under turnover (fresh,
optimistic entrants keep re-injecting generosity into the group). A
strategic account (Fischbacher et al. 2001's conditional cooperation) is
ambiguous: new entrants might anticipate free-riding by their older,
experienced group-mates and immediately behave more selfishly, or they might
not yet have learned the local norm and contribute at the population's
overall naive baseline regardless. Because both directions are theoretically
defensible, the question can only be settled empirically — and doing so
requires solving a genuine logistical problem experimental economics had
mostly avoided: staggering when different human subjects physically enter
and leave the lab mid-session, while keeping every group at a constant size
throughout.

## 4. Proposed Method
A finitely-repeated, linear voluntary contribution mechanism (VCM), the
"N-person Prisoner's Dilemma" workhorse of the public-goods literature.
**Fixed treatment** (baseline): 4 subjects, fixed for all 12 periods, a
common known end date shared by everyone — the standard design. **Dynamic
treatment**: 4 "positions" (desks) always occupied by someone, but every 3
periods one occupant is replaced by a brand-new subject; each individual
still plays exactly 12 periods (or a shortened 3/6/9-period life for those
staggered in at the start/end of the session), but different positions are
at different "ages" at any given moment — an overlapping-generations
structure with four generations coexisting simultaneously. New entrants are
told nothing about the group's prior contribution history.

## 5. Experimental Setup
z-Tree lab experiment, Pittsburgh Experimental Economics Laboratory. Fixed
treatment: 8 sessions × 4 subjects × 12 periods. Dynamic treatment: 4
sessions × 30 subjects (two staggered 4-position groups per session) × 36
total periods, each individual subject living for 3, 6, 9, or 12 periods
depending on their staggered entry slot. MPCR = 0.4 (marginal per-capita
return on the public good), matching Fehr & Gächter (2000)'s own
parameterization — already this project's own E3 grounding citation.
Dominant-strategy prediction (zero contribution every period) is identical
in both treatments, so any behavioral difference is attributable purely to
the matching structure.

## 6. Metrics
Proportion of each period's 100-token endowment contributed to the public
account, at the group and individual level; contribution by calendar
*period* vs. by subject *age* (periods since that subject's own entry);
random-effects Tobit regressions with `period`, `age`, a `dynamic` treatment
dummy, and their interactions.

## 7. Main Results
- **Finding 1 (no difference at the start):** initial beliefs, first-period
  contributions, and contributions averaged over the whole session are not
  significantly different between treatments.
- **Finding 2:** contributions decrease significantly less *per period* in
  the dynamic (turnover) treatment than in the fixed treatment — the classic
  decay curve is markedly flatter.
- **Finding 3:** contributions decrease significantly less *per subject-age*
  too — not just because fresh, generous entrants pull the calendar-time
  average up, but because **existing, older subjects also decay less** once
  turnover is present.
- **Not a simple "restart effect":** a subject's own contribution does not
  spike in the specific period a new entrant joins their group (the
  `turnover` dummy is never significant) — the effect is more diffuse than a
  one-off jolt.
- **The likely mechanism is reciprocity, reinjected.** New entrants
  contribute generously regardless of when in the session they arrive (no
  decline in entrants' own first-period contributions over calendar time);
  this steadily re-injects generosity that existing, conditionally-
  cooperative members reciprocate — contributions in period *t−2*, not just
  *t−1*, still predict a subject's own contribution in the dynamic
  treatment but not in the fixed treatment, i.e. behavior has more long-term
  inertia once turnover exists.

## 8. Limitations
- Fixed and dynamic treatments differ in total session length (12 vs. 36
  periods) — addressed by the paper's own "age," not calendar period,
  analysis and by an excluded-short-lived-subjects robustness check, but the
  two treatments are still not a perfectly matched pair.
- Only one turnover rate tested (one replacement every 3 periods, of one
  member out of four) — no sweep over how *fast* turnover needs to be to
  matter.
- Human-subject learning/beliefs are the entire mechanism under study; the
  paper has no formal agent-based or evolutionary-game model of *why*
  reciprocity reinjection works, only the experimental behavioral evidence
  for it.

## 9. Future Work
Not stated as a dedicated section; the conclusion suggests overlapping-
generations matching protocols be added to the experimentalist's toolkit
for arresting cooperation decay generally, without naming a specific next
study.

## 10. Relevance to This Project
- **This project's agents don't "decay from experience" the way human
  subjects do** — strategies are fixed, deterministic rules, not learning
  processes. But one strategy has an exact structural analogue of decay:
  `grim_trigger` (E21, ADR-0018), whose `_triggered` flag latches permanently
  once tripped — E21's own headline finding is that a permanent trigger has
  "no return path." `conditional_cooperator`/`compensating_cooperator`
  recompute their own decline-check fresh every round (no sticky flag), so
  they self-terminate any "decay" already — leaving `grim_trigger` as the
  one strategy with a genuine, literature-relevant "does it recover" question
  to ask.
- **Turnover is a natural fit for this project's existing disturbance
  architecture (ADR-0008)**, not a new subsystem: `DisturbanceConfig`
  already supports scheduling multiple events (a tuple), each firing at its
  own round — a periodic turnover schedule needs no new config surface
  beyond one more `kind` value.
- **A direct, buildable operationalization:** at a scheduled round, replace
  a fraction of agents' own internal strategy *state* (not their identity or
  accumulated payoff) with a fresh, untriggered instance — the same
  strategy, same parameters, but with no memory of a prior decline/trigger,
  exactly Duffy & Lafky's "new individual, same role, no history" entrant.

## 11. Possible Follow-Up Contribution
Add a `Strategy.reset_state()` hook (default no-op, overridden by
`conditional_cooperator`/`compensating_cooperator`/`grim_trigger`, the three
strategies with per-round decline-tracking state) and a new disturbance kind,
`agent_turnover`, reusing `DisturbanceConfig`'s existing schedule/magnitude
fields exactly like `agent_failure` does. Test whether periodic turnover
after a shock can rescue an all-`grim_trigger` population from the
permanent, no-forgiveness lock-in E21 found — a genuine, literature-motivated
answer to E21's own open question of whether *anything* recovers a triggered
population, tested against turnover rather than the forgiveness E21 already
ruled out by construction.

## 12. Important Terms
- **Overlapping generations (OLG) matching** — a population structure where
  members enter and exit at staggered times, so multiple "ages"/experience
  levels coexist simultaneously, rather than every member starting and
  ending together.
- **Decay (in VCM experiments)** — the well-documented tendency for public-
  goods contributions to fall from an initially generous level toward the
  dominant-strategy prediction (often near zero) as a fixed-cohort repeated
  game proceeds.
- **Restart effect (Andreoni 1988)** — a jump in contributions when a group
  is unexpectedly given a fresh round/restart; Duffy & Lafky explicitly test
  for, and rule out, this as the explanation for their own result.

## 13. Questions
- Does the "reciprocity reinjection" mechanism the authors favor (existing
  members respond to a fresh entrant's generosity, not just the entrant's
  own contribution) have any analogue for a strategy with *no* observational
  memory at all (e.g. `cooperative`, which always targets the same fixed
  surplus regardless of history)? If not, turnover should be a genuine no-op
  for this project's non-adaptive strategies — worth confirming directly
  rather than assuming, the same "verify before reporting" discipline as
  every other axis this session.
