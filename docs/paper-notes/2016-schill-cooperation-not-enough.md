# Cooperation Is Not Enough — Exploring Social-Ecological Micro-Foundations for
Sustainable Common-Pool Resource Use

Read status: 🟢 read from the PDF (`references/papers/schill2016.pdf`).

## Citation
Schill, C., Wijermans, N., Schlüter, M., & Lindahl, T. (2016). Cooperation is not
enough — Exploring social-ecological micro-foundations for sustainable common-pool
resource use. *PLOS ONE*, 11(8), e0157796. https://doi.org/10.1371/journal.pone.0157796

## Research Problem
Does cooperation among CPR users guarantee sustainable resource use? Prior lab
experiments by two of the authors (Schill, Lindahl & Crépin 2015; Lindahl, Crépin &
Schill, forthcoming) already show the answer is no: cooperative groups (equal-sharing
agreements, followed by all members) sometimes still over- or under-exploit the
resource. This paper asks *why* — what social-ecological micro-foundations turn
cooperative *intent* into a sustainable *outcome*.

## Why the Problem Is Difficult
Sustainability requires not just restraint but *identifying* a sustainable extraction
level under ecological complexity — a "moving target" ecosystem. That identification
is a **group** cognitive process: individuals hold different, possibly wrong beliefs
about the sustainable yield, differ in how confident they are in those beliefs, and
differ in whether they speak up. Untangling how these three individual-level
attributes combine into a *group* decision — and why the *same* average level of
knowledge can produce optimal exploitation in one group composition and collapse in
another — is not observable directly in a 4-person lab experiment, which is why the
authors build an ABM (`AgentEx`) to make the underlying mechanism explicit and
testable.

## Proposed Method
**AgentEx**, a NetLogo ABM (documented with the ODD+D protocol) directly modelling the
lab experiment's structure: groups of 4 agents, 14 rounds, one resource stock.

**Three key individual attributes** (plus trust and a binary social-preference trait):
- **Individual ecological knowledge** — the agent's belief about the optimal stock
  size, range 5–50.
- **Confidence in knowledge** — 0.0–1.0; interpreted as *perceived environmental
  uncertainty* (max confidence = the agent perceives no uncertainty at all).
- **Social skills** — 0.0–1.0 probability the agent speaks up and shares its
  knowledge; fixed per agent for the whole run.

**Five-step round cycle** (formalised in the paper's Table B / S1 Appendix):
1. **Communicate & form group knowledge** — speaking agents share their individual
   knowledge; group knowledge = the **confidence-weighted average** of all shared
   values (a more confident speaker's number counts for more).
2. **Update individual knowledge** — an agent may move its own belief toward the
   group knowledge, with probability that *increases* as its own confidence
   *decreases* (Assumption 2b: low confidence → more open to influence).
3. **Calculate extraction levels** — individual extraction = units needed to reach
   the agent's own perceived optimal stock (share equally if it has social
   preferences, more if not); group extraction (the "agreement") = the surplus above
   the group-knowledge stock level, shared equally.
4. **Choose & extract** — an agent takes the *higher* of the group or individual
   extraction level unless it has social preferences and (low) trust makes it defect
   to its own; the group level is chosen whenever it exceeds the agent's individual
   level.
5. **Feedback & update confidence/trust** — comparing actual vs. expected new stock:
   no deviation → confidence and trust *rise*; a deviation in either direction →
   confidence *falls* (Assumption 3); a deviation specifically *below* expectation
   also lowers *trust* (Assumption 6), since the agent cannot tell whether the gap is
   its own misunderstanding or someone else over-harvesting.

This is a genuinely dynamic knowledge/trust system — closer to a small social-learning
model than a fixed decision rule.

## Experimental Setup
**Resource dynamics** (from the 2015/2016 lab experiments this model reproduces): a
discretised logistic-shaped growth function, **max stock 50, min stock 5** (needed to
allow regeneration), regeneration rate stepping in units of 5 up to a peak of **9
units/round (the MSY) at a stock of 25–29** — i.e. the sustainable optimum sits at
roughly the same *relative* point (≈ half of max stock) as this project's `K/2`, even
though the shape is a stepped empirical histogram rather than a continuous `gR(1-R/K)`
curve (see Fig 1 of the paper).

**Lab data base:** 19 four-person groups, 14 rounds each (undisclosed length),
face-to-face communication allowed at any point. **9/19 (≈47%) cooperated** (reached
and followed an equal-sharing group agreement); **10/19 did not.** Critically: **no
single group — cooperative or not — held the optimal exploitation path for the entire
game**, and cooperative groups still over- or under-exploited in various rounds (Fig
2).

**Model validation:** a systematic sweep of **6,480 unique agent-attribute
configurations**, each repeated **5,000 times** for stochasticity, checked against
three qualitative patterns from the lab data (cooperative/non-cooperative outcomes;
over/under/optimal exploitation; both occurring *within* cooperative groups). This is
pattern-oriented modelling — validating structure, not fitting point estimates.

**Scenario experiment** (the part relevant to group-composition claims): starting from
configurations classified as cooperative, 7 hand-designed scenarios in two sets (Fig
5), manipulating only individual knowledge, confidence, and who speaks:
- **Set I** (does a confident, informed agent help an otherwise-uninformed,
  low-confidence group?): scenario 1 = 4 uninformed/low-confidence; scenario 2 = swap
  one to informed/high-confidence; scenario 3 = two informed/high-confidence.
- **Set II** (does an opposing confident-but-wrong speaker cancel the effect?):
  3 uninformed + 1 informed throughout; varies whether 1 or 2 agents speak and their
  confidence levels.
- A final robustness pass re-runs all 7 scenarios with a **lower trust ceiling**
  (0.66–0.94 → capped at 0.8) to test sensitivity to social (not just environmental)
  uncertainty.

## Metrics
Resource-stock trajectory over 14 rounds; **over-/under-/optimal-exploitation
classification** (deviation from the MSY band, Fig 2/6 style plots); cooperative vs.
non-cooperative classification (whether the group agreement is equal sharing, followed
by all).

## Main Results
- **Model validated**: the 6,480-configuration sweep reproduces all the qualitative
  patterns from the lab data (cooperative/non-cooperative; over/under/optimal;
  learning trends within some cooperative groups) — Fig 6 shows the model's
  cooperative-run trajectories are qualitatively indistinguishable from the lab
  groups'.
- **Scenario set I — one confident informed agent is enough to move the whole group**:
  scenario 1 (all uninformed/low-confidence) drifts to a stock around **14** (deep
  overexploitation, well below the 25–29 MSY band); adding just **one**
  informed/confident agent (scenario 2) lifts the group to **~20–23**; a **second**
  informed/confident agent (scenario 3) reaches **~24–25**, inside the MSY band —
  "even if this results in lower payoffs for each agent." The lever is *confidence*,
  not raw average knowledge: scenario 2's average knowledge is barely higher than
  scenario 1's, but the confident agent's opinion dominates the weighted group
  average, and the *uninformed* agents' low confidence makes them keep updating
  toward it.
- **Scenario set II — a confident opposing (wrong) speaker cancels the effect**: one
  confident informed speaker alone (scenario 4) tracks close to optimal; adding a
  second, uninformed but *low-confidence* speaker only weakens this slightly
  (scenario 5); adding a second, uninformed but **high-confidence** speaker
  (scenario 6) "cancels out the change towards optimal behaviour" (~20); flipping
  which side is confident — informed-but-unconfident vs. uninformed-but-confident
  (scenario 7) — produces the *worst* outcome of all seven scenarios (~15–17,
  climbing only slowly). **Confidence, not correctness, drives influence** in this
  model.
- **Robustness to social uncertainty (lower trust ceiling)**: exploitation patterns
  barely move, but **2 of 7 scenarios (4 and 5) lose their cooperative
  classification** entirely — some groups stop reaching an agreement at all under
  higher social uncertainty, even though the *exploitation path itself* (when
  cooperative) doesn't change much. Scenarios that stay cooperative share one of
  three properties: (i) uninformed speakers are ≥ as confident as informed ones, (ii)
  ≥2 confident informed speakers, or (iii) everyone speaks with ≥3 uninformed agents
  present (dilutes any one agent's pull). **Two confident informed speakers (scenario
  3) is the standout case: robust *and* close to optimal.**
- **Central conclusion — multiple group constellations reach (close to) optimal
  exploitation.** It is not the group's *average* knowledge that matters but the
  *distribution* of knowledge, confidence, and social skill across members — several
  different combinations (1 confident leader + silent followers; 2 confident leaders;
  a fully-informed-but-quiet majority) land in the same near-optimal band, while
  superficially similar compositions (informed but unconfident, opposed by a
  confident amateur) land far from it.

## Limitations
Explicitly stated by the authors: (1) no ecological uncertainty about `g`/`K` is
modelled — agents (like lab participants) are given the true dynamics, so this is a
*social*, not *ecological*, uncertainty study; (2) social preferences are modelled as
a fixed binary trait, not context-dependent, though evidence suggests they should be;
(3) group-knowledge formation is *one* plausible weighting rule (confidence-weighted
average) among several possible social-learning mechanisms — untested alternatives;
(4) trust is only updated by outcome deviation, not directly by communication content,
even though the literature says communication itself builds trust; (5) results are a
*possible* mechanism-based explanation, not the only one, for a complex
social-ecological system.

## Future Work
Named directly: test alternative group-knowledge-formation mechanisms; add a
trust-communication feedback (so trust could start low and still recover via
communication, which the current model cannot show); make social preferences
context-dependent (environmental-psychology literature); add ecological *regime
shifts* / external uncertainty (not just smooth logistic dynamics) — with the
prediction that confident, knowledgeable leaders become *more* critical under abrupt
ecological change; validate `AgentEx` against further lab/field data.

## Relevance to This Project

**This directly challenges a hidden assumption in our model — and we already have the
seed of the fix (ADR-0004).** Our `CooperativeStrategy` is sustainable *by
construction*: it is handed `g`/`K` and computes the exact sustainable share. Schill's
finding that "cooperation ⇒ sustainability" does not hold *even when every agent wants
to cooperate* is exactly what motivated splitting social preference from ecological
knowledge (`knowledge_bias`, ADR-0004). Our `private`-information blind cooperator,
which collapses the resource when it lacks current stock information, is a direct,
simpler instance of the paper's central claim.

**Where our model is deliberately simpler than AgentEx — and what that costs us:**
Schill's group-knowledge mechanism is a genuine multi-agent social-learning process —
confidence-weighted averaging, per-round belief updates, endogenous confidence and
trust dynamics driven by prediction error. Our `knowledge_bias` is a single static
multiplier per agent (ADR-0004's Status Notes), with no updating, no weighting by
confidence, and no group-knowledge-formation step at all — agents don't influence each
other's beliefs. This is a legitimate simplification for a bachelor-scope engine, but
it means we currently **cannot reproduce AgentEx's central finding** (that *one*
confident, correctly-informed agent can pull an entire uninformed group toward
optimal) — our agents have no channel through which one agent's knowledge propagates
to another's. That mechanism (belief propagation weighted by a confidence-like signal)
is a concrete, literature-grounded candidate for the "Next: binding agreement /
collective-choice mechanism" item already queued in research-direction.md Phase 2 —
it is a different, complementary idea to the Ostrom/Walker/Gardner (1992) binding
quota, closer to a *belief*-coordination mechanism than a *rule*-coordination one.

**Direct precedent for the equifinality/complexity-dial thesis direction.** Schill's
own headline conclusion — *"there are multiple group constellations that can lead to
(close to) optimal exploitation"* — is, in miniature, exactly the equifinality claim
in [thesis-direction-equifinality.md](../thesis-direction-equifinality.md): several
different distributions of a few individual-level attributes (who's informed, who's
confident, who speaks) converge on the same near-optimal band, while other,
superficially similar distributions (their scenario 7) land far from it. This is a
second, independent literature anchor for the "many paths to the optimum" framing —
alongside the folk theorem/turnpike/equifinality citations already in that document —
and it is **CPR-specific and mechanism-level**, closer to what we'd actually build,
rather than the abstract-game-theory anchors. Worth citing there.

**A concrete, cheap methodological lesson:** Schill's validation runs 6,480
configurations × 5,000 repetitions specifically to separate "our finding" from
"stochastic noise" *before* running the scenario comparisons. Our own project already
does the analogous thing at a smaller scale (E4's seed-robustness check, `[1,2,3,4,5]`
seeds by default) — this paper is evidence that seed/configuration robustness checks
of this kind are standard practice in the field we're citing, not over-engineering.

## Possible Follow-Up Contribution
A minimal belief-propagation extension to `CooperativeStrategy`: agents with
`knowledge_bias` communicate their perceived optimal stock (weighted by something
confidence-like, e.g. inversely by their own historical prediction error), and update
their belief toward the resulting group value. Compare against the current static
`knowledge_bias` baseline on whether a single well-informed agent can now rescue an
otherwise-biased population — directly testing whether Schill's "one confident leader
saves the group" result reproduces in our simpler engine, and feeding straight into
the equifinality question (how many *distributions* of leader-informedness reach
near-optimal?).

## Important Terms
Social-ecological system (SES); individual ecological knowledge vs. group knowledge;
confidence in knowledge (≈ perceived environmental uncertainty); social skills; social
preferences (conditional cooperator, per Fischbacher, Gächter & Fehr 2001); social
uncertainty (trust) vs. environmental uncertainty (confidence); pattern-oriented
modelling; ODD+D protocol; maximum sustainable yield (MSY); over-/under-/optimal
exploitation.

## Questions
- Is the confidence-weighted-average group-knowledge rule itself well supported, or
  just the simplest workable choice? The paper flags this as one of several plausible
  mechanisms — worth checking Table B / S1 Appendix (not fetched here) for the exact
  formalisation before reusing it.
- The paper finds *higher* perceived environmental uncertainty (lower confidence)
  among the uninformed can *help* (they update more readily) — this is a genuinely
  counter-intuitive result worth stress-testing if we build a belief-propagation
  strategy: does the same "low confidence helps convergence" effect appear in our
  simpler setting?
- Is matching the Ostrom/Schill-lineage parameterisation (max 50 / MSY 9) worth doing
  for direct comparability, given our `K=100, g=0.4` gives the same *shape* (peak
  productivity at half of max stock) but different absolute numbers?
