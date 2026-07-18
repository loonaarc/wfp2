# Literature Review

A **living, structured** overview of the field. This is a map and a reading
backlog, not a finished survey. Every paper that is actually read gets a full,
analysed note in [paper-notes/](paper-notes/) following the workflow (problem →
difficulty → contribution → evaluation → limitations → future work → relevance).
**Do not collect papers without analysis.**

> ⚠️ **Citation status.** Entries below are *candidate* sources with commonly-cited
> bibliographic details. Before any of these are cited in a report or thesis, the
> exact reference (authors, venue, year, pages, DOI) MUST be verified against the
> original, and the paper actually read. Treat unread entries as leads only.
> Read status: 🔴 not read · 🟡 skimmed · 🟢 fully noted in `paper-notes/`.

## How this maps to the project

| Theme | Why it matters here | Project axis |
| ----- | ------------------- | ------------ |
| Common-pool resources & the commons | the core scenario | environment/strategies |
| Evolution & maintenance of cooperation | why/when cooperation is stable | strategies |
| Information & partial observability in MAS | the information axis | information models |
| Communication in MAS | the communication axis | communication (Phase 2) |
| Resilience / robustness of collective systems | the disturbance axis | disturbances (Phase 3) |
| Reproducibility & agent-based modelling method | how to do it credibly | experiment method |

## 1. Common-pool resources and the commons

- 🔴 **Hardin (1968), "The Tragedy of the Commons", *Science*.** Foundational
  framing: individually rational over-use degrades a shared resource. Our
  `all_selfish_global` baseline is a direct instantiation. *(Verify citation; read
  critically — later work argues the "tragedy" is not inevitable.)*
- 🔴 **Ostrom (1990), *Governing the Commons*, Cambridge University Press.** Shows,
  empirically and theoretically, that communities *do* self-organize to sustain
  commons under certain design principles (monitoring, communication, sanctioning).
  Directly motivates our communication and sanctioning extensions.
- 🔴 **Ostrom et al. — CPR experiments (various).** Laboratory CPR games; sources of
  concrete rules, payoffs, and the role of communication. Relevant to metric and
  scenario design.

## 2. Evolution and maintenance of cooperation

- 🔴 **Axelrod & Hamilton (1981), "The Evolution of Cooperation", *Science*; Axelrod
  (1984), *The Evolution of Cooperation*.** Tit-for-tat, reciprocity, the role of
  repeated interaction. Motivates the planned `conditional-cooperator` strategy.
- 🔴 **Nowak (2006), "Five Rules for the Evolution of Cooperation", *Science*.**
  Taxonomy of cooperation mechanisms (kin, direct/indirect reciprocity, network,
  group). A checklist of mechanisms we could implement and compare.
- 🔴 **Reputation / indirect reciprocity (e.g. Nowak & Sigmund).** Basis for a
  reputation-based strategy (deferred).

## 3. Information and partial observability in multi-agent systems

- 🔴 **Dec-POMDP literature (e.g. Oliehoek & Amato, *A Concise Introduction to
  Decentralized POMDPs*, 2016).** Formal framing of decentralized decision-making
  under partial information. Useful for *precisely defining* our information models,
  even though we use rule-based (not optimal) agents.
- 🔴 **Partial-observability effects on coordination (various MAS papers).** Evidence
  on how information scarcity degrades or changes collective behaviour.

## 4. Communication in multi-agent systems

- 🔴 **Emergent communication / learning-to-communicate (e.g. Foerster et al., 2016,
  and follow-ups).** Mostly RL-based; relevant as context for *why* communication
  helps and when it is redundant, even though we start rule-based.
- 🔴 **Communication constraints (bandwidth, delay, loss) in distributed systems.**
  Sources for realistic constraint models for Phase 2.

## 5. Resilience and robustness of collective/decentralized systems

- 🔴 **Resilience in complex adaptive systems / socio-ecological systems (e.g.
  Folke, Walker et al.).** Definitions of resilience, recovery, and regime shifts;
  informs our resilience metrics (recovery time, post-shock sustainability).
- 🔴 **Robustness of self-organizing / swarm systems (various).** How decentralized
  systems tolerate agent failure and perturbation.

## 6. Method: agent-based modelling and reproducibility

- 🔴 **ODD protocol (Grimm et al., 2006/2010/2020), "Overview, Design concepts, and
  Details" for describing ABMs.** A standard for documenting agent-based models
  reproducibly; we should align `docs/` with ODD where sensible.
- 🔴 **Mesa framework documentation (Python ABM).** Evaluated and *not* adopted for
  now (see ADR-0001); still a reference for conventions and for a possible future
  spatial scenario.
- 🔴 **Reproducibility in computational science (general).** Justifies the provenance
  and seed discipline already implemented.

## Reading priorities

1. **Ostrom (1990)** — most directly shapes the whole direction (why commons need
   not be tragic; role of communication/monitoring). → informs Phase 2.
2. **Axelrod (1984)** + **Nowak (2006)** — concrete mechanisms → next strategies.
3. **ODD protocol** — align documentation and make the model description rigorous.
4. **Dec-POMDP intro** — sharpen definitions of the information axis.
5. Resilience sources — before Phase 3.

## Gaps / open literature questions

- What are standard, comparable **metrics** for cooperation and resilience in CPR
  simulations? (Feeds [metrics.md](metrics.md).)
- Which **CPR game parameterizations** are conventional, so our scenario is
  comparable to prior work rather than idiosyncratic?
- What is the evidence on **when communication stops helping or harms** (RQ-A / H3,
  H4)? This is the most promising "non-obvious" angle.
