# Cooperate or Collapse: Emergence of Sustainability in a Society of LLM Agents (GovSim)

Read status: 🟢 noted from the arXiv HTML. Uses LLM agents (not our approach), but
the *environment, metrics, and framing* are highly relevant. Re-read method section
before citing numbers.

## Citation
Piatti, G., Jin, Z., Kleiman-Weiner, M., Schölkopf, B., Sachan, M., & Mihalcea, R.
(2024). Cooperate or Collapse: Emergence of Sustainability in a Society of LLM
Agents. arXiv:2404.16698. https://arxiv.org/abs/2404.16698

## Research Problem
Can LLM-based agents sustain a shared renewable resource — i.e. develop and honour
cooperative norms — or do they over-extract and collapse it? Introduces **GovSim**, a
CPR governance benchmark.

## Why the Problem Is Difficult
Sustainability requires foresight, restraint, belief about others' actions, and
norm negotiation under a strong temptation to defect — a hard multi-agent social
dilemma.

## Proposed Method
Three mathematically equivalent CPR scenarios (fishery / pasture / pollution),
capacity 100, resource **regenerates by doubling the remainder** up to capacity;
collapse if stock < 5. Agents act in phases: plan → simultaneously harvest (hidden,
then revealed) → free-form natural-language discussion (negotiation).

## Experimental Setup
45 LLM-×-scenario combinations. Interventions tested: *universalization* reasoning
("what if everyone did that?") and communication/negotiation.

## Metrics (the useful part for us)
- **Survival time** — months/rounds the resource stayed above the collapse threshold.
- **Total gain** — cumulative harvest per agent.
- **Efficiency** — harvest relative to the *optimal sustainable* extraction.
- **Equality** — Gini coefficient of gains.
- **Over-usage** — % of actions exceeding the sustainability threshold.

## Main Results
- Only **2 of 45** combinations achieved sustainability — collapse is the default.
- **Universalization** reasoning improved survival by ~44 months.
- **Communication reduced over-usage by ~21%** (62% of dialogue was negotiation).
- Ability to form beliefs about others' actions correlated strongly with survival
  (Pearson r ≈ 0.83).

## Limitations
Simplified dynamics (single resource, fixed regeneration); LLM-specific; the doubling
regeneration is coarser than an ecological logistic model.

## Relevance to This Project
- **Metric menu to adopt:** *survival time*, *efficiency vs optimal*, and *over-usage
  rate* are standard, cheap to compute from our `RunResult`, and complement our
  current total-harvest / sustainability / collapse / Gini set. Recommend adding
  them.
- **Framing:** "cooperate or collapse" and default-to-collapse matches our
  all-selfish baseline; their sustainability threshold `f(t)` is our MSY share.
- **Communication result** (over-usage −21%) gives a concrete, quantitative
  expectation for our Phase-2 communication experiments (RQ-A).
- Their "belief about others' actions → survival" echoes the *information* axis: what
  agents know about *each other* matters, not just about the resource.

## Possible Follow-Up Contribution
Reuse GovSim's metric definitions (survival time, efficiency, over-usage) in our
rule-based, reproducible setting to produce clean, deterministic baselines — a
complementary, cheaper-to-run counterpart to their LLM study.

## Important Terms
Survival time; efficiency; over-usage; sustainability threshold; universalization;
social dilemma; norm negotiation.

## Questions
- Their regeneration doubles the remainder (fast); ours is logistic (slower near
  capacity). Does the qualitative story change with regeneration speed? (A sweep we
  can run.)
- Can a simple rule-based "universalizing" agent (assume everyone harvests what I do)
  reproduce the survival benefit without an LLM?
