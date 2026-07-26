Read status: 🟢 read from the PDF.

# 1998 — Nowak & Sigmund, "Evolution of indirect reciprocity by image scoring"

## Citation

Martin A. Nowak & Karl Sigmund, "Evolution of indirect reciprocity by image scoring", *Nature*, Vol. 393, pp. 573–577, 11 June 1998. DOI: 10.1038/31225. (Received 11 November 1997; accepted 31 March 1998.) Affiliations: M. A. Nowak, Department of Zoology, University of Oxford (present address at time of publication: Institute for Advanced Study, Princeton); K. Sigmund, Institut für Mathematik, Universität Wien. Article type: *Nature* letter. Volume/year verified against the PDF header ("NATURE | VOL 393 | 11 JUNE 1998").

## Research Problem

Darwinian evolution must explain costly cooperation. The established mechanisms at the time were kin selection (needs genetic relatedness), group selection, and reciprocal altruism — but reciprocal altruism was almost always studied as *direct* reciprocity, which needs repeated encounters between the **same** two individuals so the recipient can later return the favour ("help someone who may later help you"). Direct reciprocity cannot explain human cooperation, where helping is frequently channelled toward "valuable" community members one may never interact with again ("give, and you shall be given"; the "I won't scratch your back if you won't scratch their backs" principle). The paper asks: can individual selection favour cooperation when the same pair essentially never meets again, and what exact condition is required? It builds a formal model of Alexander's verbal notion of *indirect reciprocity* — cooperation driven by reputation and status, "everyone in the group continually being assessed and reassessed".

## Proposed Method

**Image scoring — the donor/recipient game.** A population of `n` individuals. In each interaction a random pair is drawn: one is the potential **donor**, the other the **recipient**. The donor may **help** (cooperate), paying a cost `c` so the recipient gains a benefit `b`, with `b > c`; or **refuse**, in which case both get zero. Only the donor has a decision; the recipient is passive.

**Reputation / image score.** Every player carries an integer **image score** `s`. When a player acts as donor and cooperates, their image score rises by one; if they refuse, it falls by one. Being a recipient does **not** change one's own image score — reputation tracks only what you do *as a donor*, i.e. how you treat others. In the basic model, `s` is public: every other player knows it. In simulations the score is bounded (Fig. 1 uses −5…+5) and reset to 0 for everyone at the start of each generation (offspring do not inherit a parent's image).

**Discriminating strategies.** A strategy is a single threshold integer `k`: the donor helps **if and only if** the recipient's image score `s_j ≥ k`. Interpretation of `k`:
- `k = −5` (Fig. 1's lowest): an **unconditional cooperator** — helps everyone regardless of reputation.
- `k = +6` (Fig. 1's highest): an effective **defector** — the threshold is above the maximum attainable score, so it never helps.
- `k ≤ 0`: called **cooperative** strategies, because they cooperate with a fresh player who has image 0 (no history yet).
- `k = 0`: the **most discriminating cooperative** strategy — help everyone with image ≥ 0 (i.e. everyone who did not just defect), refuse the rest.

Crucially, discrimination uses the *experience of others*, not one's own past encounters with this partner. That is what makes it *indirect*.

**Fitness and evolution.** A generation is `m` donor–recipient rounds during which strategies (the `k` values) are fixed; a player's fitness is the total payoff accumulated over the rounds in which it was involved. Between generations, players reproduce in proportion to fitness (replicator dynamics); optionally a small mutation probability (0.001) lets an offspring adopt a random strategy.

**Extensions built on the same core.**
1. *Incomplete information (Fig. 3):* an interaction is seen only by the recipient plus a random subset of "onlookers" (≈10 players). Only observers update their private perception of the donor's score, so reputation becomes a matrix `s_ij` = image of `i` as seen by `j`; if `j` has no information on `i`, then `s_ij = 0`.
2. *Own-image strategies (Fig. 4):* strategies conditioning on both the recipient's score and the donor's own score, via "AND" (help if recipient ≥ k **and** own image < h) or "OR" (recipient ≥ k **or** own image < h) rules.
3. *Analytical two-image model:* image collapses to 0 (bad — defected last round) or 1 (good — cooperated last round), so image depends only on the last donor move. Two player types — **defectors** (never help) and **discriminators** (help image-1, refuse image-0). A discriminator knows a recipient's image with probability `q`; lacking information, it assumes image 1 with probability `p`. Higher `p` always wins, so the analysis takes `p = 1`. This model yields the closed-form condition below.

## Main Results

- **Cooperation wins (Fig. 1).** Starting from random strategies (`b = 1`, `c = 0.1`, `n = 100`, only ~2.5 interactions per player per generation), the population converges to `k = 0` — the sternest cooperative discriminator — fixed by generation 166. Because the chance of re-meeting the same partner (or of a favour chain looping back) is negligible, **direct reciprocity is ruled out by construction**; the result is purely indirect.
- **The central condition: `q > c/b`.** From the analytical model, discriminators are evolutionarily stable only if the probability of knowing a co-player's image exceeds the cost-to-benefit ratio of the altruistic act. This is "remarkably similar to Hamilton's rule" (`r > c/b`) for kin selection, with **relatedness replaced by acquaintanceship**. A second requirement is a minimum interaction frequency: the average number of rounds `1/(1−w)` must exceed `(bq+c)/(bq−c)` (for the Fig. 1/2 numbers with `q = 1`, only ≈1.2 rounds per generation suffice). A minimum frequency `x_min` of discriminators is also needed to get cooperation started.
- **Information about partners' past behaviour is the load-bearing input.** Cooperation "depends crucially on the ability of a player to estimate the image score of the opponent." Under incomplete information (Fig. 3), only observers learn a donor's move, so reputation spreads imperfectly and there is a strong **group-size effect**: the time-averaged frequency of cooperative strategies is 90% at `n = 20`, ~47% at `n = 50`, and only 18% at `n = 100`. Larger groups need proportionally more interactions because any single act is seen by a smaller fraction of the population — i.e. lower effective `q` kills cooperation.
- **Discriminating on the recipient is essential.** Strategies that condition on the *recipient's* image sustain cooperation (Fig. 4: 55–80% cooperative interactions across AND/OR and information variants), whereas strategies that condition only on the *donor's own* image produce essentially no cooperation (<0.1%).
- **Unconditional cooperators are corrosive (Fig. 2).** With mutation, the population never settles: defectors are beaten by discriminators, discriminators are eroded by drift toward over-generous strategies (unconditional cooperators, against whom there is no selection once defectors are gone), and that indiscriminate generosity then lets defectors re-invade — "endless cycles of cooperation and defection." Populations without unconditional cooperators stay cooperative far longer.
- **Discriminators ≠ tit-for-tat.** TFT bases its move on the player's *own* prior experience with this partner; a discriminator uses *others'* experience of the partner. This is the decisive advantage when an agent meets many partners but each only rarely. (At `p = 1` with two image levels the discriminator does reduce to a TFT variant that opens with defection against anyone seen defecting.)
- Authors' broader claim: indirect reciprocity, resting on reputation transmitted by observation and language, "was a decisive step for the evolution of human societies."

## Limitations

- **Idealised public reputation.** The basic model assumes every player's image is perfectly known to all — explicitly "only an idealized scenario." The Fig. 3 extension relaxes this, but still assumes honest, noise-free observation: no misperception, no deception, no lying about others' scores (the authors note real indirect reciprocity invites "anticipation, planning, deception and manipulation," but do not model it).
- **First-order assessment only.** Image score judges the *act* (helped vs. refused), not the *context*. A discriminator who justly refuses a bad player is itself penalised with a lower score — the model flags this but does not resolve it; the later "standing"/higher-order-assessment literature exists precisely to fix it, and this paper sets it aside.
- **No convergence under mutation.** With realistic mutation the dynamics cycle indefinitely rather than reaching a stable cooperative equilibrium; cooperation is a recurrent phase, not an endpoint.
- **Strong group-size sensitivity.** Under incomplete information cooperation is already rare at `n = 100`; scaling to large populations needs interaction counts that grow with `n`.
- **Passive recipients, binary act, single scalar reputation.** No partial cooperation, no recipient agency, and reputation is one integer — a deliberately "drastically simplified" model.
- The two-image analytical result assumes `p = 1` (optimistic priors on strangers) and weak-selection-style replicator dynamics.

## Relevance to This Project

Our Nowak-2006 note singled out **indirect reciprocity (reputation)** as the most promising *unexplored* mechanism for this CPR simulation, precisely because its key parameter `q` (probability of knowing a partner's reputation) maps onto our **information axis (E1)** and our **communication axis (E6/E7)**. This 1998 paper is the foundational model, and it hands us three directly usable things: (a) a concrete reputation object — the **image score**, an integer that goes up when you restrain and down when you over-extract; (b) a concrete decision rule — the **threshold `k`** discriminator; and (c) a concrete, testable design target — cooperation should appear once **`q > c/b`** and vanish below it, mirroring the group-size collapse in the paper's Fig. 3.

**What our current `conditional_cooperator` does, and how it differs.** Our `conditional_cooperator` (see `src/emergent_cooperation/strategies/conditional.py`) reacts to **aggregate** over-extraction, not to individual reputations. Under the `global` model it watches the *shared stock* and defects (grabs a selfish share `defection_greed · level / n`) whenever the stock *declined* since last round; under the `private` model with a broadcast signal it defects whenever the *group's total harvest* exceeds MSY (`sustainable_total`). In both cases:
- It cannot tell *who* over-extracted — the `Observation` it receives (`src/emergent_cooperation/agents/observation.py`) exposes only a scalar `resource_level` and a scalar `signal` (group total harvest). There are no per-agent identities or histories.
- Its retaliation is therefore **collective punishment**: one free-rider makes it grab from *everyone*, including restrained agents. It is closer to Nowak's *trigger/defector* dynamics than to a discriminator.
- It has memory of exactly one aggregate number (`_last_level`), not a per-partner reputation matrix.

Indirect reciprocity is exactly the missing capability: **targeted** cooperation conditioned on an *individual* partner's track record, which the current aggregate monitoring cannot express.

**How to add a reputation-based strategy to our CPR model (concretely).**
1. *Define the CPR image score.* Reuse our existing over-extraction test. Each agent `j` accrues a per-agent image score for every other agent `i`: `s_ij` increases when `i`'s realised harvest last round was at/below its sustainable per-capita share (`sustainable_total / n`, i.e. restraint = "cooperate as donor"), and decreases when `i` over-extracted ("defect as donor"). This is the CPR analogue of "+1 for helping, −1 for refusing." Unknown agents default to `s_ij = 0` (Nowak's newcomer convention).
2. *Supply reputation through the observation.* Extend `Observation` with an optional `peer_scores: dict[int, float] | None` (per-partner image as seen by this agent), populated either by **direct observation** (analogue of Fig. 3 onlookers — you only update scores for agents whose harvest you actually saw) or by the **broadcast channel** (ADR-0007): a broadcast of *per-agent* harvests, not just the group total, lets receivers update `s_ij` for everyone reported. This directly wires `q` = fraction of the population whose reputation an agent knows.
3. *Define the discriminator.* A `ReputationCooperatorStrategy` with threshold `k`: when paired with / harvesting alongside a specific partner `i`, restrain (cooperate) if `s_ij ≥ k`, otherwise take a selfish share. In the CPR many-agent round (no explicit pairing), a natural aggregate form is: **restrain fully if the fraction of known over-extractors is below a tolerance, and scale one's own grab up in proportion to how many partners are currently below threshold** — i.e. punish only when *reputation* (not just the stock) says the group is defecting.
4. *Experiment.* Sweep `q` (via information completeness E1, or broadcast reach/lossiness E6/E7) and the payoff ratio `c/b` (via `defection_greed`/harvest economics) and test the paper's prediction that cooperation survives iff `q > c/b`, and that it collapses with group size at fixed observation reach (our analogue of Fig. 3's `n = 20 / 50 / 100`).

The sharp contrast to log against `conditional_cooperator`: a reputation strategy should **spare restrained agents and target over-extractors specifically**, and should sustain cooperation at intermediate information levels where aggregate monitoring (which needs to *see the whole stock*) already fails.

## Possible Follow-Up Contribution

A bachelor-feasible contribution is realistic and well-scoped: implement one `reputation_cooperator` strategy plus a minimal per-agent image-score bookkeeping layer, and run a single focused study reproducing the paper's two signature results **inside a CPR (not donation-game) setting**:
1. **The `q > c/b` threshold** — show cooperation (sustained stock, low over-extraction) emerges above the threshold and collapses below it, by sweeping information completeness `q` against the CPR cost/benefit ratio.
2. **The group-size / information-reach effect** — reproduce Fig. 3's finding that fixed observation reach sustains cooperation in small groups but fails in large ones.

Novelty over the original: Nowak & Sigmund use an abstract pairwise donation game; recasting image scoring as *restraint vs. over-extraction in a shared regenerating stock*, and comparing it head-to-head against our aggregate `conditional_cooperator` under identical information budgets, is a genuine (small) empirical increment. It also connects two of our axes (information E1 and communication E6/E7) through a single mechanistic parameter, `q`. Keep it deterministic and seed-controlled per the project's reproducibility rule; a stretch goal is adding mutation to check for the paper's cooperation/defection cycles.

## Important Terms

- **Indirect reciprocity**: cooperation returned not by the recipient but by third parties, based on reputation; no repeated pairing required. Contrast **direct reciprocity** (same two players meet again).
- **Image score (`s`)**: an integer reputation that rises when a player helps as donor and falls when it refuses; unchanged by being a recipient. In CPR terms: rises with restraint, falls with over-extraction.
- **Donor / recipient**: the two roles per interaction; only the donor decides (help at cost `c` → recipient gains `b`, `b > c`; or refuse → both get 0).
- **Discriminating strategy / threshold `k`**: help iff the recipient's image ≥ `k`. `k ≤ 0` = cooperative (helps newcomers); `k = 0` = sternest cooperative discriminator; very low `k` = unconditional cooperator; unreachable-high `k` = defector.
- **`q` (acquaintanceship / knowledge probability)**: probability a would-be donor knows the recipient's image score. The paper's key control variable; maps to our information (E1) and communication (E6/E7) axes.
- **`c/b` (cost-to-benefit ratio)** and the condition **`q > c/b`**: the evolutionary-stability threshold for indirect reciprocity; the acquaintanceship analogue of Hamilton's rule `r > c/b`.
- **Onlookers / observation matrix `s_ij`**: under incomplete information, image of `i` as seen by `j`; unknown ⇒ `s_ij = 0`. Model of reputation spread by observation/gossip.
- **"AND" / "OR" own-image strategies**: strategies that also condition on the donor's own image score.
- **Standing / higher-order assessment**: judging the *justification* of a refusal, not just the act — a known weakness of first-order image scoring, set aside here.
- **Unconditional cooperator**: helps regardless of reputation; shown to erode discrimination and reopen the door to defectors.

## Questions

- Our CPR round has no explicit donor/recipient pairing — every agent harvests simultaneously. What is the cleanest CPR translation of "image score changes only for the donor role"? (Proposal: score each agent by its own last-round harvest vs. its sustainable share, independent of pairing.)
- What is the operational `b` and `c` in our appropriation payoff, so that `q > c/b` becomes a concrete, measurable prediction rather than a metaphor? (Ties to the same open question raised in the Nowak-2006 note.)
- Does reputation add anything over aggregate stock monitoring when information is *complete*? The interesting regime is presumably **partial** information (small `q`), where `conditional_cooperator`'s whole-stock view is unavailable but per-partner gossip still flows — is that where a reputation strategy strictly dominates?
- Should the broadcast channel (ADR-0007) carry **per-agent** harvests (enabling reputation) or only the group total (as now)? Per-agent broadcast is the minimal change that makes indirect reciprocity expressible — is the added state/bandwidth justified by the experiments it unlocks?
- Do we want first-order image scoring (simple, but punishes justified refusal) or a "standing"-style rule? First-order is the faithful reproduction of this paper; standing is the acknowledged fix. Reproduce first, extend second.
- With mutation added, do we see the paper's endless cooperation/defection cycles in a CPR setting, or does the resource dynamics (stock collapse as a hard floor) damp them?
