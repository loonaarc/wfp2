Read status: 🟢 read from the PDF.

# 2006 — Nowak, "Five Rules for the Evolution of Cooperation"

## Citation

Martin A. Nowak, "Five Rules for the Evolution of Cooperation", *Science*, Vol. 314, No. 5805, pp. 1560–1563, 8 December 2006. DOI: 10.1126/science.1133755. Program for Evolutionary Dynamics, Department of Organismic and Evolutionary Biology, and Department of Mathematics, Harvard University. (Article type: Review.)

## Research Problem

How can natural selection lead to cooperation? A cooperator pays a cost `c` so that another individual receives a benefit `b` (both measured in fitness); a defector pays no cost and gives no benefit. Cooperation is nonetheless the organizing principle behind every major transition in biological organization (genes in genomes, chromosomes in cells, cells in multicellular organisms, animal societies, human society). The paper asks under what condition selection can favor such costly helping, and organizes the answer into five distinct mechanisms, each yielding one simple rule.

## Why the Problem Is Difficult

In any mixed, well-mixed population, defectors have a higher average fitness than cooperators, so selection continuously increases the relative abundance of defectors until cooperators go extinct (Fig. 1). Paradoxically, a population of only cooperators has the highest average fitness and a population of only defectors the lowest, so natural selection here *reduces* average fitness over time. Fisher's fundamental theorem (average fitness increases under constant selection) does not apply, because selection is frequency-dependent: an individual's fitness depends on the current frequency of cooperators. The paper gives the explicit payoffs for `i` cooperators in a population of size `N`: `f_C = [b(i-1)/(N-1)] - c` and `f_D = bi/(N-1)`, with average fitness `f̄ = (b-c)i/N`. Thus well-mixed selection "needs help" — a specific mechanism — to establish cooperation.

## The Five Rules (each with its condition)

1. **Kin selection** — Selection can favor cooperation when donor and recipient are genetic relatives, because helping kin propagates shared genes ("inclusive fitness", the "extended phenotype" of "selfish genes"). Mechanism: relatedness `r` = probability that two individuals share a gene by descent (1/2 for brothers, 1/8 for cousins). **Condition (Hamilton's rule): `r > c/b`.** In the paper's unified framework this same rule is the decisive criterion for all three success measures (ESS, RD, AD).

2. **Direct reciprocity** — Repeated encounters between the *same* two individuals in a repeated Prisoner's Dilemma; "if I cooperate now, you may cooperate later." Axelrod's tournaments found tit-for-tat winning, but it cannot correct errors (an accidental defection triggers long retaliation); generous-tit-for-tat [cooperating after a defection with probability `1 - (c/b)`] and then win-stay, lose-shift are more robust. Mechanism parameter: `w` = probability of another encounter between the same two individuals; expected number of rounds is `1/(1-w)`. **Condition: `w > c/b`** (this is the ESS condition; slightly more stringent conditions hold for RD/AD).

3. **Indirect reciprocity** — Reputation-based: pairwise encounters where the two individuals need not meet again; a donor's choice to help is observed and can be reported, so helpers build a good reputation and are more likely to receive help later ("indirect reciprocity resembles the invention of money; the currency is reputation"). Has high cognitive demands (memory, monitoring the social network, language/gossip); linked to the evolution of morality, social norms, and human intelligence. Mechanism parameter: `q` = probability of knowing someone's reputation (social acquaintanceship). **Condition: `q > c/b`** (ESS condition; RD/AD slightly more stringent).

4. **Network reciprocity** — Relaxes the well-mixed assumption: individuals occupy the vertices of a graph and interact only with graph neighbors (evolutionary graph theory; a generalization of spatial reciprocity). Plain cooperators (no strategic complexity) can survive by forming clusters in which they help each other. Mechanism parameter: `k` = average number of neighbors per individual. **Condition: `b/c > k`** (holds for all three success measures — when it holds, cooperators dominate defectors).

5. **Group selection ("multilevel selection")** — The population is subdivided into groups; cooperators help others in their own group, defectors do not. Individuals reproduce in proportion to payoff and offspring join the same group; when a group reaches a size it can split in two (another group going extinct to hold total population constant). Selection acts on two levels: within groups defectors win, but between groups pure-cooperator groups grow/split faster ("group fecundity selection"; a "group viability selection" variant is also noted). Mechanism parameters: `n` = maximum group size, `m` = number of groups. **Condition (weak selection, rare splitting): `b/c > 1 + (n/m)`** (holds for all three success measures).

## Main Results

- All five mechanisms, despite very different underlying formalisms, reduce to a single common form: each can be written as a 2×2 payoff matrix between cooperators C and defectors D (Table 1), and every resulting rule is of the form **benefit-to-cost ratio exceeds a critical value**.
- The paper defines three measures of evolutionary success from the payoff matrix (entries α, β for C's row; γ, δ for D's row). Cooperation is: **ESS** if α > γ (cannot be invaded by defectors); **risk-dominant (RD)** if α + β > γ + δ (larger basin of attraction; defectors' basin < 1/2); **advantageous (AD)** if α + 2β > γ + 2δ (fixation probability of a single cooperator exceeds 1/N; equivalent to the "1/3 rule" — invader fitness at frequency 1/3 exceeds resident's — in the weak-selection limit).
- For kin selection, network reciprocity, and group selection, the *same* condition (`r > c/b`, `b/c > k`, `b/c > 1 + n/m`) governs all three success measures, because when it holds cooperators actually dominate defectors. For direct and indirect reciprocity, the ESS conditions are `w > c/b` and `q > c/b`; RD and AD require slightly more stringent conditions.
- Broader claim: cooperation drives the construction of new levels of biological organization and open-ended evolution; Nowak proposes adding "natural cooperation" as a third fundamental principle of evolution alongside mutation and natural selection.

## Limitations

- Fig. 1 / the core defection argument assumes a **well-mixed population**; network reciprocity exists precisely because real populations are structured.
- Conditions are derived under simplifying assumptions: **weak selection** (and, for group selection, **rare group splitting**); the 1/3 rule and AD fixation results hold "in the limit of weak selection."
- Games on graphs (network reciprocity) are "difficult to analyze mathematically because of the enormous number of possible configurations"; results rely on approximations/simulation, and the general rule `b/c > k` is a derived approximation.
- Indirect reciprocity's calculations are "complicated and only a tiny fraction of this universe has been uncovered."
- The mechanisms are presented as the ways cooperation can evolve, but the author explicitly says not all potential mechanisms are discussed (e.g. "green beard" tag-based recognition; voluntary rather than obligatory games producing oscillating cooperation).
- **Punishment is explicitly *not* a mechanism for the evolution of cooperation** — all evolutionary models of punishment rest on an underlying mechanism (indirect reciprocity, group selection, or network reciprocity); punishment can only *enhance* the cooperation level achieved within such a model.
- Detailed derivations and their limitations are deferred to the Supporting Online Material (reference 53), not the main text.

## Relevance to This Project

This project is a reproducible agent-based common-pool-resource (CPR) simulation of emergent cooperation, with strategies: selfish, cooperative, conditional_cooperator (direct reciprocity / retaliate), compensating_cooperator (restraint), and sanctioning (enforcement), across experiments E1–E7 (information/knowledge, reciprocity, sanctioning, robustness, voluntary monitoring via replicator dynamics, communication). Mapping Nowak's five mechanisms:

- **Direct reciprocity (`w > c/b`)** — Already modelled: the `conditional_cooperator` (retaliate) strategy is the tit-for-tat analogue. Nowak's `w` (probability of re-encounter) maps onto repeated-interaction / horizon assumptions; his note that tit-for-tat is fragile to errors while win-stay-lose-shift is more robust is directly relevant to robustness experiment E4.
- **Indirect reciprocity (`q > c/b`)** — Candidate future strategy. Maps naturally onto the project's information/knowledge (E1) and communication (E7) axes: `q` is the probability of knowing a partner's reputation, so a reputation-tracking strategy is the obvious extension. This is arguably the mechanism closest to the project's existing "information" framing but not yet instantiated as a strategy.
- **Group selection (`b/c > 1 + n/m`)** — Partially reachable: the voluntary-monitoring / replicator-dynamics experiment (E5) already uses the multilevel/evolutionary-dynamics machinery Nowak invokes; a subdivided-population variant would be the direct instantiation.
- **Network reciprocity (`b/c > k`)** — Candidate future direction requiring a spatial/graph interaction structure rather than well-mixed CPR play; not modelled if the current simulation is well-mixed.
- **Kin selection (`r > c/b`)** — Least aligned: requires genetic relatedness / shared-gene semantics that do not map cleanly onto CPR appropriation agents; likely out of scope.

Two conceptual anchors are directly usable: (a) every rule reduces to a **benefit-to-cost ratio threshold**, which gives a principled way to parameterize when cooperation should win in the CPR payoff structure; and (b) Nowak's explicit position that **punishment is not itself an evolutionary mechanism** but only enhances cooperation on top of one — a sharp, testable framing for the project's `sanctioning` strategy and sanctioning experiment (E3): sanctioning should be analyzed as an *enhancer* riding on an underlying reciprocity/group mechanism, not as a standalone driver.

## Important Terms

- **Cooperator / Defector**: cooperator pays cost `c` to give benefit `b` (fitness units); defector pays nothing, gives nothing.
- **`c`, `b`**: cost to donor, benefit to recipient; the **benefit-to-cost ratio `b/c`** is the recurring quantity in every rule.
- **Hamilton's rule**: `r > c/b`; `r` = coefficient of relatedness = probability of sharing a gene by descent.
- **Inclusive fitness / kin selection / extended phenotype / selfish gene**: framing where a gene's effect on kin carrying the same gene counts toward fitness.
- **Repeated Prisoner's Dilemma**: the game underlying direct reciprocity.
- **Tit-for-tat / generous-tit-for-tat / win-stay, lose-shift**: reciprocity strategies; win-stay-lose-shift is more robust to errors.
- **`w`**: probability of another encounter between the same two individuals; expected rounds `1/(1-w)`.
- **Reputation / `q`**: `q` = probability of knowing someone's reputation (social acquaintanceship), the driver of indirect reciprocity.
- **Evolutionary graph theory / network (spatial) reciprocity / `k`**: interaction on a graph; `k` = average number of neighbors.
- **Group / multilevel selection; `n`, `m`**: `n` = maximum group size, `m` = number of groups; "group fecundity" vs "group viability" selection.
- **ESS (evolutionarily stable strategy)**: α > γ — resists invasion by defectors.
- **RD (risk-dominant)**: α + β > γ + δ — larger basin of attraction (defector basin < 1/2).
- **AD (advantageous)**: α + 2β > γ + 2δ — fixation probability > 1/N; equivalent to the **1/3 rule** under weak selection.
- **Weak selection**: limit in which several of the results are derived.
- **Natural cooperation**: Nowak's proposed third fundamental principle of evolution alongside mutation and natural selection.

## Questions

- The rules are ESS-level thresholds; for the project's finite-population, stochastic CPR agents, is the AD / 1/3-rule (fixation probability > 1/N) the more appropriate success criterion than ESS?
- All conditions assume a fitness-defined `b` and `c`. What are the operational `b` and `c` in the CPR appropriation payoff, and can each experiment be reframed as measuring an effective `b/c` against a mechanism-specific threshold?
- Nowak treats the five mechanisms as separable, each with one payoff matrix. The project mixes strategies (e.g. conditional_cooperator + sanctioning) in one population — how do combined mechanisms interact, given that the paper only analyzes them in isolation?
- Given the claim that punishment merely enhances an underlying mechanism, which underlying mechanism does the project's `sanctioning` strategy actually ride on (indirect reciprocity, group selection, or network reciprocity), and is that mechanism present in the model?
- The core results assume weak selection and (for group selection) rare splitting. How sensitive are the project's outcomes to strong-selection regimes where these approximations break down (robustness experiment E4)?
- Is the current CPR simulation well-mixed? If so, network reciprocity (`b/c > k`) is untapped — would adding a spatial/graph interaction topology be a tractable extension?
