# ADR-0017: Starting resource level (R₀) as a settings-robustness sweep, not a new complexity axis

- **Status:** Accepted
- **Date:** 2026-08-16
- **Deciders:** project owner (approved scope), assistant (implementing)

## Context

`R₀` (`ResourceConfig.initial_level`) has been implicitly fixed at `K/2` by
every experiment so far, without ever being named as a choice. A number was
reserved for testing it back on 2026-08-09 (**E17** — see
`complexity-synthesis.md`'s "Numbering caveat") once population-diversity
took over the E14 slot it originally held. `thesis-direction-equifinality.md`'s
own "Should the starting condition (R₀) be varied?" section is explicit that
this is **not itself a new complexity axis** — varying `R₀` doesn't touch
decentralization, information, or institutions, which is where this
project's actual novel contribution lives — but recommends revisiting it
"once the first complexity-axis experiment's design is actually committed."
That condition is now satisfied five times over (E14–E16, E19, E20).

Three papers are already read and cited specifically for this experiment:
von Bertalanffy (1968) — the origin of the term "equifinality" itself, whose
literal definition is "different initial conditions, fixed dynamics, same
steady state" — and Beven & Binley (1992, 2014), origin of GLUE, this
project's adopted methodology for equifinality-related sweeps.

**A real precision problem, caught while reading the grounding, not
after building:** von Bertalanffy's own paper-note
(`docs/paper-notes/1968-bertalanffy-general-system-theory.md`) explicitly
flags that this project's existing literature review blends two distinct
claims that are *not* the same thing: (1) his own literal sense — fixed
strategy mix, varying initial conditions, same end state — versus (2) the
"multiple configurations" sense already tested by E14–E16/E20 — different
strategy mixes, comparable ends (closer to Cooper & John's multiple-
equilibria framing). Building E17 as a single, blended sweep would repeat
exactly the imprecision the note warns against.

## Considered Options

1. **Just the GLUE-composite sweep** — cross `R₀` with the full E14
   composition space and report near-optimal count/fraction per level,
   mirroring E14's own diversity-level table. *(The cheap version: reuses
   the most existing code, but never actually tests von Bertalanffy's own
   literal definition — the project's own founding citation for the whole
   equifinality direction goes untested. Rejected as too thin given a
   number was reserved specifically citing that definition.)*
2. **Just the literal test** — fixed population, sweep `R₀`, check
   steady-state invariance. *(Well-grounded and cheap, but skips the
   methodological anchor — GLUE / the `welfare_efficiency ≥ 0.80` threshold
   — that this project has used for every other equifinality question, and
   says nothing about whether the guarantee has limits.)*
3. **Three explicitly-labeled questions, kept separate rather than blended:
   the literal test (Q1), its limits under free-riders (Q2), and the
   GLUE-composite cross with E14's full composition space (Q3).** *(Chosen.)*

## Decision

Option 3. No engine changes — `ResourceConfig.initial_level` already exists
and is directly settable; this is purely a new analysis script
(`scripts/experiment_starting_resource.py`), reusing `run_simulation`/
`run_experiment` and the exact `welfare_efficiency ≥ 0.80` threshold already
established in E14–E16/E20.

- **Q1 (literal equifinality, von Bertalanffy 1968):** a fixed, well-behaved
  population (8 `cooperative` agents, E1's own baseline shape, no
  free-riders) swept across `R₀ ∈ {1.0, 5.0, 20.0, 50.0, 80.0, 95.0}`
  (`K=100`) — including a start right at the collapse threshold and one
  near carrying capacity. Checks whether the final resource level converges
  to the same steady state regardless of `R₀`, exactly as his Theorem 1
  predicts for any open system that reaches one.
- **Q2 (the guarantee's limits):** the identical `R₀` sweep, same rounds,
  but with free-riders present (6 `cooperative` + 2 `selfish`, no shock —
  deliberately isolating the starting-condition effect from E8/E9's own
  shock-timing question, a different axis already covered). Tests whether
  equifinality still holds once the population can actually drain the pool
  to (or near) zero from an already-fragile start — a real possibility in
  this engine's logistic regrowth (`R=0` is a genuine absorbing state,
  `dR/dt = g·0·(1-0/K) = 0`), not a hypothetical one.
- **Q3 (GLUE-style composite, Beven & Binley 1992/2014):** three
  representative `R₀` levels (`5.0` catastrophic, `50.0` the default,
  `95.0` near-capacity) crossed with the full 495-composition space E14
  already swept (5 registered non-loner strategies, `N=8`), reusing the
  identical `welfare_efficiency ≥ 0.80` threshold — a limits-of-acceptability
  bound fixed *before* the sweep runs, matching the 2014 retrospective's own
  refined recommendation over a post-hoc fitted likelihood.

## Rationale

- **Keeps the two senses of equifinality precisely separate**, per the
  literature note's own explicit warning — Q1/Q2 vary only the initial
  condition at fixed dynamics (von Bertalanffy's literal claim); Q3 varies
  the strategy mix (the "multiple configurations" sense this project's
  other axes already test), crossed with `R₀` as an *additional* dimension
  rather than conflated with it.
- **Reuses the existing threshold, not a new one.** `welfare_efficiency ≥
  0.80` is already this project's own limits-of-acceptability bound,
  declared before results are seen, applied identically across every
  complexity axis — Q3 is the same methodology, R₀ swapped in as the
  dimension being tested instead of population diversity.
- **No new engine code** — `initial_level` is a first-class `ResourceConfig`
  field every experiment already sets implicitly; this only makes the
  setting itself the thing being swept, exactly the "Bachelor-feasible,
  analysis layer only" framing both grounding papers' own follow-up
  sections recommend.
- **Q2 isn't padding — it's the scientifically honest complement to Q1.**
  Reporting only "yes, equifinality holds" (Q1) without checking whether it
  has limits would overclaim von Bertalanffy's theorem, which requires the
  system to actually *reach* a steady state — that's not guaranteed once a
  catastrophic start and active free-riders can jointly drive the pool to
  the `R=0` absorbing state before regrowth has a chance to act.

## Consequences

- **Not folded into the complexity-staircase count/fraction table as its
  own row** — per `thesis-direction-equifinality.md`'s own explicit
  scoping, this is a settings-robustness check, not a new axis varying
  decentralization/information/institutions. Q3's own table sits alongside
  E14's, not as a fourth stacking rung.
- **Q1/Q2 use a single seed (deterministic strategies, matching E1's own
  convention)**; Q3 also single-seed, matching E14's own convention for the
  same reason — zero between-seed variance for deterministic populations,
  consistent with every other composition sweep in this project.
- **A real, citable instance of von Bertalanffy's own theorem either way.**
  If Q1 confirms invariance, it's a precise, direct empirical test of the
  founding citation for this whole thesis direction — not a metaphorical
  resemblance. If it doesn't fully hold (Q2), that is *also* a genuine,
  reportable result (the 2014 retrospective's own framing: a negative
  result under a pre-declared, fixed criterion is informative, not a
  failure to explain away).

## Status Notes

Built as **E17** (`scripts/experiment_starting_resource.py`,
[docs/experiments/E17-starting-resource-level.md](../experiments/E17-starting-resource-level.md)).
