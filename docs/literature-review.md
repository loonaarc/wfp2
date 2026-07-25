# Literature Review

A **living, structured** overview of the field. Papers that have been read get a
full analysed note in [paper-notes/](paper-notes/); this file is the map and the
"what it means for us" synthesis.

Read status: 🔴 not read · 🟡 skimmed · 🟢 analysed note exists in `paper-notes/`.

> **Citation status (2026-07):** foundational citations below have been verified via
> web search. The three 🟢 sources have analysed notes taken from the published
> open-access articles. Page/figure-level claims should still be checked against the
> originals before they appear in the thesis.

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
et al. 2022), and expect a concrete effect size (**GovSim: communication reduced
over-usage ~21%**). "Cheap talk" works via trust, and cooperation can persist after
communication stops.

### A well-grounded specific research question this suggests
> *Under what information conditions does cooperative intent produce sustainable
> outcomes in a decentralized CPR system — and can communication substitute for
> missing ecological knowledge?*

This builds on Schill (cooperation ≠ sustainability), uses our information axis now,
and sets up the communication phase. It is bachelor-feasible and literature-grounded.

---

## 1. Common-pool resources and the commons

- 🔴 **Hardin (1968), "The Tragedy of the Commons", *Science* 162(3859), 1243–1248.**
  https://doi.org/10.1126/science.162.3859.1243 — foundational framing; our
  `all_selfish_global` baseline instantiates it. (Read critically: later work shows
  the "tragedy" is not inevitable.)
- 🔴 **Ostrom (1990), *Governing the Commons*, Cambridge University Press (280 pp).**
  Communities *do* self-organize to sustain commons; her **eight design principles**
  (boundaries, congruence, collective choice, monitoring, graduated sanctions,
  conflict resolution, recognition of rights, nested enterprises) motivate our
  communication and sanctioning extensions.
- 🟢 **Schill, Wijermans, Schlüter & Lindahl (2016), "Cooperation Is Not Enough…",
  *PLOS ONE* 11(8), e0157796.** → [note](paper-notes/2016-schill-cooperation-not-enough.md).
  *The most direction-relevant paper we've read* (see Implications above).

## 2. Evolution and maintenance of cooperation

- 🔴 **Axelrod (1984), *The Evolution of Cooperation*, Basic Books**; **Axelrod &
  Hamilton (1981), "The Evolution of Cooperation", *Science* 211, 1390–1396.**
  Tit-for-tat, reciprocity, repeated interaction — motivates the conditional
  cooperator. *(Verify the 1981 volume number — a source returned 221; 211 is the
  commonly cited value.)*
- 🔴 **Nowak (2006), "Five Rules for the Evolution of Cooperation", *Science* 314,
  1560–1563.** https://doi.org/10.1126/science.1133755 — taxonomy of five mechanisms
  (kin selection, direct/indirect reciprocity, network reciprocity, group selection);
  a menu of mechanisms we could implement and compare.

## 3. Information, ecological knowledge, and communication in CPR/MAS

- 🟢 **Janssen, DeCaro & Lee (2022), "…Inequality, Trust, and Communication in Common
  Pool Experiments", *JASSS* 25(4), 3.** https://doi.org/10.18564/jasss.4922 →
  [note](paper-notes/2022-janssen-communication-trust-inequality.md). Communication →
  trust → restraint; heterogeneous types; Gini.
- 🟢 **Piatti et al. (2024), "Cooperate or Collapse" (GovSim), arXiv:2404.16698.** →
  [note](paper-notes/2024-piatti-govsim-cooperate-or-collapse.md). CPR benchmark;
  survival/efficiency/over-usage metrics; communication reduces over-usage ~21%.
- 🔴 **Dec-POMDP literature (Oliehoek & Amato, 2016, *A Concise Introduction to
  Decentralized POMDPs*).** Formal framing of decentralized decisions under partial
  information; useful for *defining* our information models precisely.

## 4. Resilience and robustness of collective systems

- 🔴 **Socio-ecological resilience (Folke; Walker et al.).** Definitions of
  resilience, recovery, regime shifts — informs our Phase-3 resilience metrics.
- 🔴 **Robustness of self-organizing/swarm systems.** Tolerance to agent failure and
  perturbation.

## 5. Method: agent-based modelling and reproducibility

- 🔴 **Grimm et al. (2006; 2020 update), the ODD protocol.** 2020 update:
  *"The ODD Protocol… A Second Update", JASSS* 23(2), 7
  (https://www.jasss.org/23/2/7.html). Standard for documenting ABMs reproducibly —
  **we should structure the model description in `docs/` along ODD** (Overview →
  Design concepts → Details).
- 🔴 **Mesa framework docs.** Evaluated and *not* adopted (see ADR-0001); reference
  for conventions and a possible future spatial scenario.

---

## Reading priorities (updated)

1. **Ostrom (1990)** — design principles → directly shapes the communication/
   monitoring/sanctioning roadmap. *(next to read fully)*
2. **Axelrod (1984) + Nowak (2006)** — concrete cooperation mechanisms → the
   conditional cooperator and beyond.
3. **ODD protocol (Grimm 2020)** — restructure the model description for rigour and
   comparability.
4. Resilience sources — before Phase 3.

## Open literature questions

- What is the *simplest* trust/reciprocity rule that reproduces the qualitative
  "communication helps via trust" effect in a **non-spatial** model like ours?
- Is matching the Ostrom-lineage parameterisation (max 50 / MSY 9) worth it for
  comparability, or is our K=100/MSY=10 close enough?
- Strongest non-obvious angle (RQ-A / H3–H4): **when does communication stop helping
  or start harming?** GovSim and Janssen show it helps; the boundary is open.
