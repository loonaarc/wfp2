# Literature Review

A **living, structured** overview of the field. Papers that have been read get a
full analysed note in [paper-notes/](paper-notes/); this file is the map and the
"what it means for us" synthesis.

Read status: 🔴 not read · 🟡 skimmed · 🟢 analysed note exists in `paper-notes/` ·
⚪ reference only (not a reading lead).

> **Status (2026-08-06):** all core sources have now been read from the primary PDFs
> (obtained via library access, in `references/papers/`, git-ignored) and have full
> analysed notes (🟢). This includes Schill (2016), Janssen et al. (2022), and Piatti
> et al. (2024), whose notes were originally written from web sources rather than
> PDFs and have since been rewritten against the actual PDFs, correcting one
> transcription error in the Janssen note (Model 1's harvest-probability parameter).
> The one textbook, Oliehoek & Amato, is analysed for the framework/model/complexity
> chapters we use; its solver chapters (4–8) are out of scope. Citations verified
> from the PDFs. A few thematic leads (below) remain 🔴 as candidates.

## How this maps to the project

| Theme | Why it matters here | Project axis |
| ----- | ------------------- | ------------ |
| Common-pool resources & the commons | the core scenario | environment/strategies |
| Evolution & maintenance of cooperation | why/when cooperation is stable | strategies |
| Information / ecological knowledge | the information axis | information models |
| Communication in MAS/CPR | the communication axis | communication (Phase 2) |
| Resilience / robustness | the disturbance axis | disturbances (Phase 3) |
| ABM method & reproducibility | doing it credibly | experiment method |

---

## Implications for our project *(the important part)*

What the read literature says about our design decisions:

### ✅ Where our model is standard (good — we are comparable, not idiosyncratic)
- **Logistic renewable resource + discrete extraction rounds** is the conventional
  abstract CPR formulation (Schill et al. 2016; the Ostrom experimental lineage uses
  discrete logistic with max stock 50, MSY ≈ 9/round — our K=100, g=0.4 gives MSY=10,
  the same shape).
- **Selfish vs. cooperative extraction rules** and **default-to-collapse** match the
  literature (GovSim: only 2/45 runs sustainable; tragedy-of-the-commons framing).
- **Gini for fairness** is the standard inequality metric in this exact setting
  (Janssen et al. 2022; GovSim "equality"). Keep it.
- **Collapse / sustainability / total-harvest** metrics are all standard.

### ⚠️ The one assumption to fix: we conflate cooperation with sustainability
Schill et al. (2016), *"Cooperation Is Not Enough"*, show **cooperation is necessary
but not sufficient** for sustainability — you also need *ecological knowledge*. Our
`cooperative` agent is sustainable *by construction* because we hand it `g` and `K`.
So our model currently cannot tell "cooperation" apart from "having the right
knowledge".

**But we already have the seed of the fix:** our `private`/blind cooperator collapses
the resource precisely because it lacks current ecological information — a direct
instance of Schill's thesis. This lets us reframe the information axis as *"does
cooperative intent translate into sustainable outcomes, and how much does that depend
on ecological knowledge/information?"* See
[decisions/0004-separate-cooperation-from-knowledge.md](decisions/0004-separate-cooperation-from-knowledge.md).

### ➕ Metrics worth adding (all standard, cheap from our `RunResult`)
- **Survival time** — rounds before collapse (GovSim).
- **Efficiency** — harvest relative to the optimal sustainable yield (GovSim).
- **Over-usage rate** — fraction of agent-rounds exceeding the sustainable share
  (GovSim). Directly measures "cooperation vs. over-extraction".

### ➕ Strategy worth adding: the conditional cooperator
Janssen et al. (2022) find the *dominant* realistic agent type is the **conditional
cooperator** (~75% of their best-fit population). This strongly backs our planned
third strategy and suggests a **trust/reciprocity** formulation.

### ➕ Communication design for Phase 2 (evidence-based)
Model communication as a **trust/reputation** state that raises restraint (Janssen
et al. 2022), and expect a concrete effect size (**GovSim: removing communication
raises over-usage 22%**, p<0.001, on the subset of models with survival rate >10%).
"Cheap talk" works via trust, and cooperation can persist after communication stops.

### A well-grounded specific research question this suggests
> *Under what information conditions does cooperative intent produce sustainable
> outcomes in a decentralized CPR system — and can communication substitute for
> missing ecological knowledge?*

This builds on Schill (cooperation ≠ sustainability), uses our information axis now,
and sets up the communication phase. It is bachelor-feasible and literature-grounded.

---

## 1. Common-pool resources and the commons

- 🟢 **Hardin (1968), "The Tragedy of the Commons", *Science* 162(3859), 1243–1248.**
  → [note](paper-notes/1968-hardin-tragedy-of-the-commons.md). Our `all_selfish_global`
  baseline instantiates it. (Read critically: the essay's driving purpose is a
  coercive anti-overpopulation argument, and "commons" means an *unmanaged, open-access*
  resource — exactly the case Ostrom shows is not inevitable.)
- 🟢 **Ostrom (1990), *Governing the Commons*, Cambridge University Press (280 pp).**
  → [note](paper-notes/1990-ostrom-governing-the-commons.md) *(read ch. 1 + the
  design-principles portion of ch. 3, incl. Table 3.1)*. Her **eight design
  principles** underpin our sanctioning experiment (E3). **Key reframe:** the
  second-order free-rider problem our model hits (E5) is one real commons *routinely
  solve* via accountable monitoring, graduated sanctions, and collective choice — so
  E7's "only external enforcement works" reflects our *impoverished* institutions, not
  a general truth.
- 🟢 **Schill, Wijermans, Schlüter & Lindahl (2016), "Cooperation Is Not Enough…",
  *PLOS ONE* 11(8), e0157796.** → [note](paper-notes/2016-schill-cooperation-not-enough.md).
  *The most direction-relevant paper we've read* (see Implications above).

## 2. Evolution and maintenance of cooperation

*(chronological)*

- 🟢 **Axelrod & Hamilton (1981), "The Evolution of Cooperation", *Science* 211(4489),
  1390–1396.** → [note](paper-notes/1981-axelrod-hamilton-evolution-of-cooperation.md)
  *(volume 211 verified from the PDF)*. Tit-for-tat / reciprocity motivates our
  `conditional_cooperator`; **caveat:** TFT's stability needs *targeted* retaliation,
  absent in an N-player commons (why E2's reciprocity punishes the resource, not a
  culprit). (Axelrod's 1984 book expands this; not separately noted.)
- 🟢 **Nowak & Sigmund (1998), "Evolution of indirect reciprocity by image scoring",
  *Nature* 393, 573–577.** →
  [note](paper-notes/1998-nowak-sigmund-indirect-reciprocity.md). Founding model of
  **indirect reciprocity** (reputation / image score); cooperation is stable when
  `q > c/b` (probability of knowing a partner's reputation) and collapses as group size
  grows. Basis for a **reputation-based strategy** that targets individual
  over-extractors, unlike our collective-punishment conditional cooperator.
- 🟢 **Fehr & Gächter (2002), "Altruistic Punishment in Humans", *Nature* 415,
  137–140.** → [note](paper-notes/2002-fehr-gaechter-altruistic-punishment.md).
  Empirical backbone for E3: punishment sustains cooperation, its removal collapses it.
  Their punishment works via *deterrence* (humans adapt); our fixed agents force
  *confiscation* instead — a load-bearing distinction.
- 🟢 **Nowak (2006), "Five Rules for the Evolution of Cooperation", *Science* 314,
  1560–1563.** → [note](paper-notes/2006-nowak-five-rules.md). Five mechanisms with
  their conditions (kin `r>c/b`, direct reciprocity `w>c/b`, indirect reciprocity
  `q>c/b`, network `b/c>k`, group). Direct reciprocity = our conditional cooperator;
  **indirect reciprocity (reputation, `q`) is the most promising unexplored strategy**
  and maps onto our information/communication axes.
- 🟢 **Hauert, Traulsen, Brandt, Nowak & Sigmund (2007), "Via Freedom to Coercion",
  *Science* 316, 1905–1907.** →
  [note](paper-notes/2007-hauert-via-freedom-to-coercion.md). A **loner** opt-out
  rescues costly punishment from the second-order free-rider problem via cyclic
  dynamics — a concrete recipe to turn E5's negative result positive (add a loner +
  make monitoring cost scale with group size).
- 🟢 **Sigmund, De Silva, Traulsen & Hauert (2010), "Social learning promotes
  institutions for governing the commons", *Nature* 466, 861–863.** →
  [note](paper-notes/2010-sigmund-social-learning-institutions.md). **Pool**
  (pre-committed) vs **peer** punishment: pool punishment is stable *only* if it also
  punishes second-order free-riders. A direct one-variable follow-up to flip E5
  (efficiency-for-stability trade-off).

## 3. Information, ecological knowledge, and communication in CPR/MAS

- 🟢 **Janssen, DeCaro & Lee (2022), "…Inequality, Trust, and Communication in Common
  Pool Experiments", *JASSS* 25(4), 3.** https://doi.org/10.18564/jasss.4922 →
  [note](paper-notes/2022-janssen-communication-trust-inequality.md). Communication →
  trust → restraint; heterogeneous types; Gini.
- 🟢 **Piatti et al. (2024), "Cooperate or Collapse" (GovSim), arXiv:2404.16698.** →
  [note](paper-notes/2024-piatti-govsim-cooperate-or-collapse.md). CPR benchmark, 15
  LLMs; survival/efficiency/over-usage metrics; best model (GPT-4o) survival rate
  only 53.3%; removing communication raises over-usage 22%; universalization
  reasoning (+4 months survival) is the strongest single intervention.
- 🟢 **Ostrom, Walker & Gardner (1992), "Covenants With and Without a Sword: Self-
  Governance Is Possible", *American Political Science Review* 86(2), 404–417.** →
  [note](paper-notes/1992-ostrom-walker-gardner-covenants.md). *The* CPR lab
  experiment on communication vs. sanctioning. **Communication alone** works (it
  bundles *agreement*); **sanctioning alone** is inefficient (~9% net after fines/
  errors); **communication + an endogenously chosen sword** is best (~90% net) —
  empirical backing for our binding-agreement follow-up, and it explains why E6 (a bare
  signal with no agreement) understates communication's power.
- 🟢 **Balliet (2010), "Communication and Cooperation in Social Dilemmas: A
  Meta-Analysis", *J. Conflict Resolution* 54(1), 39–57.** →
  [note](paper-notes/2010-balliet-communication-meta-analysis.md). Large effect of
  communication on cooperation (*d* ≈ 1.01), strongest face-to-face. Measures
  *cooperation*, never *resource survival* — so E6's fairness-vs-resource distinction
  is a genuine contribution angle.
- 🟢 **Oliehoek & Amato (2016), *A Concise Introduction to Decentralized POMDPs*.** →
  [note](paper-notes/2016-oliehoek-amato-dec-pomdps.md) *(framework/model/complexity
  chapters analysed; solver chapters 4–8 out of scope)*. Formal tuple for decentralized
  decisions under partial observability;
  useful to *precisely define* our `global`/`private` information models and to justify
  rule-based agents (finite-horizon Dec-POMDPs are NEXP-complete). We do **not** solve
  Dec-POMDPs — borrow the vocabulary, not the machinery.

## 4. Resilience and robustness of collective systems

- 🟢 **Folke (2006), "Resilience: the emergence of a perspective…", *Global Env.
  Change* 16(3), 253–267.** → [note](paper-notes/2006-folke-resilience.md).
  Engineering vs. ecological resilience; collapse as a basin shift. Gives Phase-3
  metrics: return time, absorbed-disturbance magnitude, rising-variance early warning.
- 🟢 **Walker, Holling, Carpenter & Kinzig (2004), "Resilience, Adaptability and
  Transformability…", *Ecology & Society* 9(2), 5.** →
  [note](paper-notes/2004-walker-resilience-adaptability.md). Four aspects of
  resilience (latitude, resistance, precariousness, panarchy) → measurable in our model
  (precariousness = distance to the collapse threshold).

## 5. Method: agent-based modelling and reproducibility

- 🟢 **Grimm et al. (2020), "The ODD Protocol… A Second Update", *JASSS* 23(2), 7.** →
  [note](paper-notes/2020-grimm-odd-protocol.md). The standard for documenting ABMs
  reproducibly — **action: add an ODD-structured model description** so the write-up
  matches the field standard (much of the material already exists across our docs).
- ⚪ **Mesa framework docs.** *Evaluated and deliberately not adopted* (ADR-0001) —
  not a reading lead; kept here as a reference for conventions and a possible future
  spatial scenario.

---

## Reading priorities (updated)

The foundational set is now read (Hardin, Ostrom, Axelrod & Hamilton, Nowak, Fehr &
Gächter, Hauert, Schill, Janssen, Piatti, Folke, Walker, ODD). Next actions from the
reading:

1. ✅ **Act on Hauert (2007)** — added a *loner* opt-out to the E5 replicator
   ([E11](experiments/E11-loner-rescue.md), [ADR-0009](decisions/0009-loner-and-defector-scaled-monitoring-cost.md)).
   Result: delays E5's collapse ~4–5× but does not prevent it — points to Sigmund et
   al. (2010)'s pool-punishment mechanism as the more promising next attempt.
2. **Act on ODD (2020)** — write an ODD-structured model description for the thesis.
3. **Candidate new strategy from Nowak** — an *indirect-reciprocity / reputation*
   agent (ties to the information and communication axes).
4. **Before Phase 3** — operationalise the Folke/Walker resilience metrics
   (precariousness = distance to collapse; absorbed-disturbance magnitude).

## Open literature questions

- What is the *simplest* trust/reciprocity rule that reproduces the qualitative
  "communication helps via trust" effect in a **non-spatial** model like ours?
- Is matching the Ostrom-lineage parameterisation (max 50 / MSY 9) worth it for
  comparability, or is our K=100/MSY=10 close enough?
- Strongest non-obvious angle (RQ-A / H3–H4): **when does communication stop helping
  or start harming?** GovSim and Janssen show it helps; the boundary is open.
