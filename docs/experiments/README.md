# Experiment Reports

One report per experiment, documenting the hypothesis, method, result (with real
numbers and a figure), interpretation, and threats to validity. Reports cite the
config/script that produced them so results are reproducible (see
[../experiment-design.md](../experiment-design.md)).

Naming: `E<n>-<short-topic>.md`.

## Index

| Report | Question | Verdict |
| ------ | -------- | ------- |
| [E1 — information and knowledge](E1-information-and-knowledge.md) | Does cooperation sustain the resource, and how does that depend on information vs. ecological knowledge? (H1, H6) | Cooperation sustains **only** with information *or* accurate knowledge |
| [E2 — reciprocity](E2-reciprocity.md) | Does conditional cooperation protect the resource against free-riders better than unconditional? (SQ-4, SQ-5) | No — reciprocity protects **fairness** (starves free-riders) but collapses the **commons** |
| [E3 — sanctioning](E3-sanctioning.md) | Can enforcement protect the resource *and* fairness where reciprocity cannot? | Yes — sanctioning protects **both**, but monitors pay a cost (second-order free-rider) |
| [E4 — robustness & sensitivity](E4-robustness-and-sensitivity.md) | Are the results robust to noise, and how sensitive to `g` and `N`? (SQ-11, SQ-12) | Robust to noise; higher `g` tolerates more free-riders; ~scale-invariant in `N` |
| [E5 — voluntary monitoring](E5-voluntary-monitoring.md) | If monitoring is a choice, does it (and the commons) survive selection? | No — monitors erode (second-order free-rider), then the commons collapses |
| [E6 — communication](E6-communication.md) | Can a broadcast substitute for missing information under private info? (SQ-6/7/8) | Yes for **fairness** (substitutes for observation) — but the resource still collapses; value depends on the *response* |
| [E7 — response rules](E7-response-rules.md) | Given communication, does the response (retaliate/restrain/enforce) save the commons? | Only **enforcement** does — peer responses fail; communication informs but does not coordinate |
| [E8 — resilience](E8-resilience.md) | Does cooperation recover from a resource shock, and does information or enforcement decide it? | **Information**, not enforcement — observing populations recover, blind ones collapse; enforcement doesn't help |
| [E9 — resilience with free-riders](E9-resilience-with-free-riders.md) | With free-riders present, does enforcement matter for shock recovery? | **Yes** — enforcement recovers across free-rider counts; cooperation recovers only up to ~1 free-rider. Resilience needs *both* information and enforcement |
| [E10 — agent failure](E10-agent-failure.md) | Does a commons tolerate losing members, and does it matter who? | **Who fails decides** — losing the enforcer collapses it, a cooperator is harmless, a free-rider helps. Enforcement is a single point of failure |
| [E11 — loner rescue](E11-loner-rescue.md) | Does an opt-out ("loner") strategy rescue voluntary monitoring (E5), per Hauert et al. (2007)? | **Delays, doesn't prevent** — cuts erosion speed ~4–5×, but continuous replicator dynamics lack the fixation step Hauert's rescue needs |
| [E12 — pool punishment](E12-pool-punishment.md) | Does pool punishment with a second-order fine stabilise monitoring (E5), per Sigmund et al. (2010)? | **Yes** — sanctioning grows monotonically to ~100%, sustainability never leaves 0.50; the first mechanism tried that actually stabilises it |
| [E13 — binding agreement](E13-binding-agreement.md) | Can a voted, jointly-funded agreement (no born monitors) match individually pre-committed enforcement (E7), per Ostrom, Walker & Gardner (1992)? | **Yes, up to a point** — matches enforcement exactly for 0–4 free-riders if the group votes fast (round 2); breaks down at 5+ regardless of timing |
| [E14 — population-type diversity](E14-population-diversity.md) | Across all 495 compositions of 8 agents over 5 strategies, does the near-optimal set grow as more distinct types coexist? | **Mostly not a diversity effect at all** — every composition with ≥1 `sanctioning` agent passes (330/330, E3 rediscovered); without one, only 1 free-rider is survivable and only paired with a non-reciprocal restrainer (E2 rediscovered) |
| [E15 — nested enforcement](E15-groups-and-boundaries.md) | Full per-group compositional sweep (56,020 configs): does nested enforcement behave differently from flat enforcement, and does the near-optimal set grow with group-count complexity? | **Yes, by count — 383 → 2,820 → 18,737 as m rises** (fraction still falls 0.774 → 0.576 → 0.370); driven almost entirely by whether any group is "unprotected" (has a free-rider, no monitor) |
| [E16 — boundaries](E16-boundaries.md) | Full governed × outsider space (Monte Carlo sampled): does closing the community to outsiders matter, on top of nested enforcement (E15)? | **Yes, consistently, but not catastrophically** — opening the boundary roughly halves the near-optimal fraction at every m (~2× cost), far less severe than the old adversarial-only reading suggested |
