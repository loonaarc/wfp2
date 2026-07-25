# ADR-0004: Separate "cooperation" (social preference) from "ecological knowledge"

- **Status:** Accepted  *(2026-07-25 — approved by project owner)*
- **Date:** 2026-07-25
- **Deciders:** project owner (assistant proposing, based on literature review)

## Context
The literature review surfaced a direct challenge to our model. Schill et al.
(2016), *"Cooperation Is Not Enough"* (PLOS ONE), show empirically and in an ABM that
**cooperation is necessary but not sufficient for sustainable CPR use** — sustainable
outcomes also require *ecological knowledge* (knowing the sustainable yield) and
confidence in it. See [paper-note](../paper-notes/2016-schill-cooperation-not-enough.md).

Our current `CooperativeStrategy` **fuses two things**: a *social preference*
(restraint / take only a share of the surplus) and *ecological knowledge* (it is
given `g` and `K` and computes the sustainable yield exactly). As a result, in our
model "cooperation" implies "sustainability" by construction — exactly the conflation
Schill et al. warn against. It also means our model cannot express a *well-meaning
but misinformed* cooperator.

Notably, our existing `private`/blind cooperator already gestures at the split: it
restrains (social preference) but lacks current stock information, and consequently
collapses the resource when it starts depleted (hypothesis H1). That is precisely
"cooperation without adequate ecological knowledge fails."

## Considered Options
1. **Do nothing.** Keep the fused strategy. Simple, but carries a hidden,
   literature-contradicted assumption and limits the questions we can ask.
2. **Split the cooperative decision into two explicit factors:** a *social
   preference* (how much of the perceived surplus to claim / willingness to restrain)
   and an *ecological knowledge model* (an estimate of the sustainable yield, with an
   error/confidence level). The realised behaviour is restraint *applied to* the
   agent's possibly-wrong estimate.
3. **Only add a metric** (over-usage rate) to *measure* the gap between cooperation
   and sustainability, without changing the strategy. Cheaper; less expressive.

## Decision (proposed)
Adopt **Option 2**, phased and additively, *if the owner agrees*:
- Introduce an explicit **knowledge parameter** on the cooperative strategy: its
  estimate of the sustainable share, derived from an assumed `g`/`K` that may be
  biased or noisy (perfect knowledge = today's behaviour, so it is a strict
  generalisation and backward-compatible).
- Adopt **Option 3 as well**: add the **over-usage** and **survival-time** and
  **efficiency** metrics (all standard; see GovSim note) so the cooperation-vs-
  sustainability gap is measurable.

## Rationale
- Removes a hidden assumption the literature explicitly rejects, making the model
  more defensible and more interesting.
- Turns our information axis into a sharper question — *does cooperative intent yield
  sustainable outcomes, and how much does that depend on ecological knowledge /
  information?* — which is well-grounded (Schill) and bachelor-feasible.
- Backward-compatible: perfect knowledge reproduces current baselines, so existing
  results and tests still hold.
- Sets up the communication phase cleanly: *can communication substitute for missing
  ecological knowledge?* (RQ-A).

## Consequences
- **Positive:** a more honest, literature-aligned model; a crisper research question;
  new comparable metrics; no loss of existing behaviour.
- **Negative / cost:** more parameters to document and sweep; must be careful the
  "knowledge" and "social preference" knobs are clearly defined and not entangled.
- **Follow-ups if accepted:** implement the knowledge parameter on
  `CooperativeStrategy`; add metrics; add a `conditional-cooperator` (reciprocity)
  strategy (Janssen et al.); update `docs/metrics.md`, `research-questions.md`, and
  the ODD-style model description.

## Status Notes
Proposed and **accepted** on 2026-07-25. First implementation: a `knowledge_bias`
parameter on `CooperativeStrategy` (multiplier on the agent's estimate of the
sustainable yield used when it cannot observe the stock), plus `survival_time`,
`efficiency`, and `over_usage_rate` metrics. Backward-compatible: `knowledge_bias =
1.0` reproduces the previous behaviour and all prior baselines/tests.

Design note on where knowledge bites: with **global** information the agent observes
the stock and self-corrects (harvest only the surplus above the healthy level), so
`knowledge_bias` has little effect — *observation substitutes for ecological
knowledge*. With **private** information the agent is blind and must rely on its
(possibly biased) yield estimate, so `knowledge_bias` drives over-/under-exploitation.
This is exactly the cooperation-needs-knowledge effect (H6), and the substitutability
of information for knowledge is the sharpened research question.
