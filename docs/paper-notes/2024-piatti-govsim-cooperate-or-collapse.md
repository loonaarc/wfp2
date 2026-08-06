# Cooperate or Collapse: Emergence of Sustainable Cooperation in a Society of LLM Agents

Read status: 🟢 read from the PDF (`references/papers/piatti2024.pdf`, arXiv:2404.16698v4,
NeurIPS 2024).

## Citation
Piatti, G., Jin, Z., Kleiman-Weiner, M., Schölkopf, B., Sachan, M., & Mihalcea, R.
(2024). Cooperate or Collapse: Emergence of Sustainable Cooperation in a Society of
LLM Agents. *38th Conference on Neural Information Processing Systems (NeurIPS
2024)*. arXiv:2404.16698.

## Research Problem
Can LLM-based agents, given identical rules and no priming toward cooperation or
greed, self-organize to sustainably share a common-pool resource over a long horizon
(12 rounds), the way human groups sometimes do? GOVSIM is the benchmark platform
built to answer this, plus the follow-up: *what specifically causes success or
failure* — communication, moral reasoning style, or basic reasoning capability?

## Why the Problem Is Difficult
Sustainability requires simulating the long-term, multi-agent consequences of a
short-term-tempting action ("if I take more now, is that still sustainable if
everyone reasons the same way?") — a form of hypothetical, other-agent-aware
reasoning current LLMs are not obviously built for. The paper's central diagnostic
finding is that this, not the game's raw difficulty, is the actual bottleneck:
agents largely fail not because the arithmetic is hard, but because they fail to
project the effect of a shared decision rule forward.

## Proposed Method
**GOVSIM environment**: a phase-based, partially-observable multi-agent Markov game.
Each round: (1) private harvest decisions submitted simultaneously and then
revealed; (2) free-form natural-language group discussion; (3) resource regrowth.
Three mathematically identical scenarios differing only in framing/units — fishery
(tons of fish), pasture (hectares of grass via sheep), pollution (% unpolluted water,
inverted sign) — each with capacity 100, collapse threshold `C=5`, and **regrowth by
doubling the remainder each round, capped at 100** (not a continuous logistic curve
like this project's `dR = gR(1-R/K)` — a much faster, coarser regeneration rule).
`T=12` rounds per run, 5 agents, 5 random seeds per model, temperature 0.

**Sustainability threshold** `f(t) = max({x | g(h(t)-x) ≥ h(t)})` — the largest
extraction that still leaves at least as much stock after regrowth (`g=2`, the
doubling factor) — this is this paper's exact analogue of this project's MSY, but
recomputed each round from the *current* stock rather than derived once from fixed
`g`/`K`.

**Agent architecture**: adapted from Park et al.'s "Generative Agents," restructured
into three phases (Strategy/reflect, Harvesting, Discussion) rather than open-ended
simulated life. A moderator LLM orchestrates group discussion turn-taking.
**Universalization intervention**: agents are given the explicit Kantian-style
prompt, *"Given the current situation, if everyone takes more than f(t), the shared
resources will decrease next month"* — operationalizing the "what if everybody does
that?" principle (Levine, Kleiman-Weiner, Schulz, Tenenbaum & Cushman 2020, cited as
the moral-psychology source) as a single injected sentence, not a different decision
algorithm.

## Experimental Setup
**15 LLMs**: closed-weight GPT-3.5, GPT-4, GPT-4-turbo, GPT-4o, Claude-3
Haiku/Sonnet/Opus; open-weight Llama-2 (7B/13B/70B), Llama-3 (8B/70B), Mistral
(7B/8×7B), Qwen (72B/110B). Greedy decoding (temperature 0), 5 seeds per
model/scenario, aggregated across the 3 scenarios in the headline table.
**Perturbation**: a "greedy newcomer" agent (explicitly profit-maximizing, indifferent
to others, no memory of prior group history) is inserted into an already-cooperative
4-agent group after month 3, run for 15 months total, tested on GPT-4o only (the best
performer).
**Ablations**: communication removed entirely (tested on the 4 models with survival
rate > 10%: GPT-4o, GPT-4-turbo, Claude-3 Opus, Qwen-110B); universalization prompt
added/removed (all models except Claude-3 Opus, excluded for API cost).
**Sub-skill probes**: four templated, 150-item reasoning tests isolating (a) basic
simulation-dynamics arithmetic, (b) individually-sustainable choice without any group
interaction, (c) sustainability-threshold calculation given an explicit
equal-sharing assumption, (d) the same calculation *without* that assumption
(requires the model to form its own belief about others' actions).

## Metrics
**Survival time** `m` — longest run of rounds with `h(t) > C`. **Survival rate**
`q` — fraction of the 5 seeds reaching `m=12`. **Total gain** `R_i` — cumulative
harvest per agent. **Efficiency** `u` — harvest achieved relative to the
theoretical maximum (`T·f(0)`, i.e. harvesting exactly at threshold every round from
the start). **(In)equality** `e` — Gini coefficient of total gains. **Over-usage**
`o` — fraction of agent-rounds where the harvest exceeded that round's `f(t)`.

## Main Results
**Headline benchmark (Table 1, aggregated over 3 scenarios × 5 seeds):**

| Model | Survival Rate | Survival Time | Gain | Efficiency | Equality | Over-usage |
|---|---:|---:|---:|---:|---:|---:|
| Llama-3-8B / most open-weight models | 0.0 | 1.0 | 20.0 | 16.7 | ~57–91 | 20–39 |
| Qwen-110B | 20.0 | 4.5±2.3 | 36.3±12.0 | 30.3±10.0 | 89.6±3.6 | 47.0±13.4 |
| GPT-3.5 / Claude-3 Haiku/Sonnet | 0.0 | ≤1.3 | ~20.5 | ~17 | 84–91 | 32–36 |
| GPT-4 | 6.7 | 3.9±1.5 | 31.5±5.8 | 26.2±4.8 | 91.4±2.3 | 27.1±6.1 |
| Claude-3 Opus | 46.7 | 6.9±2.9 | 58.5±22.1 | 48.8±18.4 | 91.4±4.4 | 21.0±8.5 |
| GPT-4-turbo | 40.0 | 6.6±2.6 | 62.4±22.0 | 52.0±18.3 | 93.6±2.7 | 15.7±8.6 |
| **GPT-4o (best)** | **53.3** | **9.3±2.2** | **66.0±14.6** | **55.0±12.2** | **94.4±3.1** | **10.8±8.6** |

**No model reaches sustainability in all 5 seeds.** The best is under 54% survival
rate. Most models never survive past month 1 — they overexploit immediately, before
any communication has happened (there is no discussion before the *first* harvest).

**Greedy-newcomer perturbation (GPT-4o, the best model):** inserting one selfish
agent into an established 4-agent cooperative group drops survival rate
**53.3 → 33.3**, survival time **9.3 → 6.6**, gain **66.0 → 34.8**, efficiency
**55.0 → 31.3**, equality **94.4 → 71.7**, and raises over-usage **10.8 → 15.7**. The
paper shows a qualitative example where the group *does* successfully draw the
newcomer back toward the norm through discussion — but the aggregate numbers say this
recovery is inconsistent, not the default outcome.

**Universalization reasoning (Section 3.4):** across models (excluding Claude-3 Opus),
adding the single universalization sentence significantly increases average survival
time by **4 months** (t-test, p<0.001), total gain by **29 units**, and efficiency
by **24%** (p<0.001) — a large effect from one added sentence, and the paper's
sharpest positive intervention.

**Communication ablation (Section 3.5):** on the subset of models with survival rate
>10% (GPT-4o, GPT-4-turbo, Claude-3 Opus, Qwen-110B), removing communication raises
over-usage by **22%** (p<0.001) — direct, model-agnostic evidence that talking, not
just having a good policy, matters.

**Dialogue composition (Section 3.6):** GPT-4-turbo used to classify utterances into
information / negotiation / relational sub-categories (manual-vs-model agreement
72% on 100 sampled utterances). Averaged over models: **54% negotiation, 45%
information, 1% relational**. This is *not* mostly information exchange — most talk
is agents trying to move each other's behaviour, not just reporting facts.

**Reasoning sub-skills correlate strongly with survival (Section 3.7, Figure 5):**
simulation dynamics R²=0.69, individually-sustainable-action-in-isolation R²=0.92,
threshold-under-assumption R²=0.76, **threshold-from-belief-about-others R²=0.82**
(all p<0.001). Notably: models choose the sustainable action **at most 30% of the
time** even in isolation (no group pressure at all) — most models don't reliably
know or apply their own sustainable share, which is *why* group coordination via
communication ends up doing so much of the work.

## Limitations
Stated directly: simplified dynamics (fixed regeneration multiplier, no varying
regrowth rates, single resource type, no heterogeneous stakeholders); small
population (5 agents); current LLM negotiation ability is a hard ceiling on what the
benchmark can show; no adversarial/malicious-agent robustness testing; no human
participants (LLM-only society). The authors are explicit that GOVSIM's simplicity is
a deliberate choice for systematicity, not an oversight — "our goal is to establish a
framework... flexibly extended by ourselves and others."

## Future Work
Explicitly named: larger agent populations (with fine-tuned small models as cheaper
simulators); **coordinated adaptation to sudden shocks** (the paper notes the engine
is already modular enough for this — "resource dynamics, agents... are easily
changeable for different simulation runs"); **varying regeneration rates and
multiple resource types** (listed directly as a "possible" extension, alongside
"different stakeholder interests"); handling one-off fairness exceptions to a
group norm without inviting exploitation; adversarial/malicious agents to test
norm robustness; mixed human-AI communities.

## Relevance to This Project

**This is the closest published analogue of our own engine's core loop** — a
resource with a hard collapse threshold, discrete private-harvest-then-reveal
rounds, and a communication phase — but built for evaluating LLM agents, not
hand-written strategies. Several direct, load-bearing connections:

- **Their "greedy newcomer" experiment is effectively E9/E10 run on LLM agents,
  and gets a *milder* result than ours.** One free-rider dropped GPT-4o's survival
  rate by 20 points (53.3→33.3) but did **not** collapse it to zero — comparable in
  shape to our E9 finding that cooperation degrades rather than collapses with one
  free-rider (~0.44 sustainability), while our enforcement mechanism (absent here)
  holds up better. Useful cross-validation: the qualitative pattern "one bad actor
  degrades but doesn't necessarily destroy cooperation, if there's a way to talk about
  it" reproduces across a rule-based engine and an LLM-agent engine independently.
- **Their sub-skill finding is a sharp, literature-grounded argument for our
  ADR-0004 knowledge/cooperation split.** "Models choose the sustainable action at
  most 30% of the time even alone, with no group pressure" (Fig. 5b) is exactly
  Schill et al.'s (2016) "cooperation is not enough" claim, independently
  rediscovered in a completely different agent substrate (LLMs vs. hand-written
  rules) — strong triangulation that separating *willingness to restrain* from
  *ability to compute the sustainable share* is a real, recurring failure mode, not
  an artifact of our own model's design.
- **Their universalization result is a candidate literature-grounded strategy we
  don't currently have.** A single "what if everyone did this?" prompt sentence
  produces one of the largest effect sizes in the paper (+4 months survival,
  p<0.001). Our current strategies (cooperative, conditional_cooperator,
  sanctioning, compensating_cooperator) don't include anything like an explicit
  counterfactual-universalization rule — it's a cheap, well-specified new strategy
  to prototype: an agent that computes its harvest as if reasoning "what if every
  agent harvested at my rate," which is a slightly different mechanism from both
  plain cooperation (fixed restraint) and conditional cooperation (reactive to
  others' *past* behaviour) — this one is prospective/counterfactual rather than
  reactive.
- **Directly names two of the exact complexity axes from the equifinality
  brainstorm** as its own stated future work: *"varying regeneration rates, multiple
  resource types"* (Section 5) is, verbatim, two of the axes in
  [thesis-direction-equifinality.md](../thesis-direction-equifinality.md) and the
  growth-model-variation question raised there — independent confirmation from a
  concurrently-published benchmark paper that these are recognized, open extensions
  in the field, not an idiosyncratic invention for this thesis.
- **Metric menu already adopted (ADR-0004)** — survival time, efficiency,
  over-usage — is this paper's, confirmed correct via the primary source now (the
  earlier version of this note, before the PDF was available, had these metrics
  right but was built from a less rigorous read).
- **A cautionary methodological note for our own project:** the GOVSIM regrowth
  rule (double the remainder, capped) is *not* the continuous logistic our engine
  uses — it is coarser and grows faster near collapse than a logistic curve does.
  If we ever want to argue our qualitative findings (e.g. "one free-rider degrades
  but doesn't collapse cooperation") generalize beyond our own growth-function
  choice, this paper is direct evidence the pattern also holds under a
  *structurally different* regrowth rule — relevant ammunition for the "should we
  vary the growth model" question, in the sense that at least one other regrowth
  function has already been shown compatible with similar qualitative dynamics.

## Possible Follow-Up Contribution
Implement a `UniversalizingCooperator` strategy: computes its harvest as the
sustainable share *assuming every other agent mirrors its own current decision
rule* (a one-step counterfactual, cheap to compute from information already
available to a `global`-info agent), and compare it against the existing five
strategies on sustainability, fairness, and — specifically — robustness to a single
free-rider (replicating the newcomer-perturbation comparison in a rule-based,
deterministic, reproducible setting, complementing GOVSIM's expensive, noisy LLM
runs).

## Important Terms
Survival time / survival rate; efficiency (relative to `T·f(0)`, not relative to
MSY directly); over-usage rate; sustainability threshold `f(t)` (recomputed each
round from current stock, unlike a fixed MSY); universalization reasoning (Kantian
moral psychology, Levine et al. 2020); greedy-newcomer perturbation; generative
agent architecture (Park et al. 2023).

## Questions
- The regrowth rule (doubling, capped at 100) is far more forgiving near collapse
  than logistic growth near `K/2` — does the newcomer-perturbation result (mild
  degradation, not collapse) depend on that forgiving regrowth, or would it hold
  under our slower logistic dynamics too? Directly testable with our own engine.
- A related 2025 reproducibility study (Curvo, Dragomir, Torpes & Rahimi, University
  of Amsterdam, arXiv:2505.09289) replicates this paper's two headline claims and
  adds a heterogeneous multi-model society experiment (MultiGov) where a majority of
  strong LLM agents verbally talk a weak agent down to a sustainable quota, plus an
  "inverse"/trash scenario showing framing (loss aversion) changes cooperative
  behaviour even holding the mathematics fixed. Worth a follow-up paper-note of its
  own if that PDF is obtained again — its own reported numbers differ from this
  paper's (different scope: fishery-only, 3 seeds, newer models, no Claude), so it
  should not be conflated with this citation.
- Sub-skill test (b) — sustainable action in isolation, chosen correctly ≤30% of the
  time — is worth directly comparing against our own `cooperative` strategy's
  behaviour under `private` information (H1): is our blind cooperator's collapse
  quantitatively similar to "chooses sustainably ~30% of the time," or does it fail
  in a different, more systematic way?
