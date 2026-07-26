# Emergent Cooperation

A modular, reproducible multi-agent simulation environment for investigating how
**information availability, communication structures, and environmental
disturbances** influence **emergent cooperation, self-organization, and
resilience** in decentralized systems.

The environment is intentionally domain-neutral. The first concrete scenario is an
abstract **common-pool resource (CPR)** game — several agents share one renewable
resource and each round decide how much to consume — because it captures the
core cooperation-versus-sustainability tension without committing to any single
application area (traffic, energy, epidemics, etc.).

> **New here? Start with the hands-on walkthrough:
> [docs/getting-started.md](docs/getting-started.md)** — run it, change one setting,
> and watch cooperation succeed or collapse (~20 min).

## Status

**Early foundation (v0.1.0).** Working and tested:

- deterministic simulation core (regenerate → observe → harvest);
- a renewable resource with logistic/linear regeneration;
- four strategies: `selfish`, `cooperative`, `conditional_cooperator` (reciprocity),
  and `sanctioning` (monitoring + enforced harvest quota);
- two information conditions: `global` and `private`;
- controlled random seeds with independent per-agent RNG streams;
- configuration-driven experiments (YAML) with a seed sweep;
- basic metrics (performance, sustainability, collapse, fairness/Gini);
- reproducible result export (config + metrics + history + provenance);
- a CLI and 28 passing tests.

Not yet implemented (planned extension points, interfaces stubbed): explicit
**communication** models and environmental **disturbances**. See
[docs/research-direction.md](docs/research-direction.md) for the roadmap.

## Research direction

> Development of a modular multi-agent simulation environment for investigating
> how information availability, communication structures, and environmental
> disruptions influence emergent cooperation, self-organization, and resilience
> in decentralized systems.

The intended scientific contribution is **not** "I built a simulation" but a
*reproducible experimental environment* used to *systematically* study when and
why decentralized cooperation emerges, and how fragile it is. See
[docs/research-direction.md](docs/research-direction.md) and
[docs/research-questions.md](docs/research-questions.md).

## Installation

Requires Python ≥ 3.11.

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate

pip install -e ".[dev,analysis]"
```

## Quick start

```bash
# List available strategies
emergent-coop strategies

# Run a baseline experiment (writes results/<name>/)
emergent-coop run --config configs/all_cooperative_global.yaml

# Override seeds and output location
emergent-coop run --config configs/mixed_global.yaml --seeds 1 2 3 --output results/mixed

# Compare all four baselines side by side
python scripts/run_baselines.py
```

Example baseline output (mean over 5 seeds, 8 agents, 100 rounds):

| config                    | total harvest | final level | sustainability | collapsed | payoff Gini |
| ------------------------- | ------------: | ----------: | -------------: | --------: | ----------: |
| all_cooperative_global    |          1000 |          50 |           0.50 |       0.0 |       0.000 |
| all_selfish_global        |            60 |           0 |           0.00 |       1.0 |       0.000 |
| mixed_global              |            ~86 |           0 |           0.00 |       1.0 |       0.442 |
| all_cooperative_private   |          1000 |          50 |           0.50 |       0.0 |       0.000 |

Cooperators sustain the resource at the maximum-sustainable-yield stock; a fully
selfish population collapses it (tragedy of the commons); a mixed population also
collapses but with unequal payoffs (selfish agents free-ride on cooperators).

## Planned architecture

```
config (YAML) ─► ExperimentConfig ─► Simulation(seed) ─► RunResult ─► metrics ─► export
                                         │
                    ┌────────────────────┼─────────────────────┐
                    ▼                    ▼                     ▼
              ResourcePool           Agents              (future) Communication
             (regeneration)      (Strategy each)         + Disturbances
```

Each round: the resource regenerates, agents observe (subject to the information
model), agents request consumption, requests are scaled to fit the stock, harvest
is assigned, payoffs update. Full detail in [docs/architecture.md](docs/architecture.md).

## Repository structure

```
├── README.md                 This file
├── pyproject.toml            Project + tooling (pytest, ruff) configuration
├── docs/                     Documentation — see docs/README.md for the index
│   ├── project-overview.md   The problem in accessible language
│   ├── research-direction.md Chosen direction and roadmap
│   ├── research-questions.md Broad questions, testable subquestions, hypotheses
│   ├── terminology.md        Definitions of key terms
│   ├── getting-started.md    Hands-on walkthrough (run it, tweak it)
│   ├── code-walkthrough.md   Guided tour of the Python code, with diagrams
│   ├── architecture.md       Components, interfaces, data flow
│   ├── experiment-design.md  Variables, baselines, seeds, reproducibility
│   ├── metrics.md            Metric definitions, formulas, limitations
│   ├── contribution-opportunities.md
│   ├── literature-review.md  Structured overview of the field
│   ├── paper-notes/          One analysed note per paper (+ template)
│   ├── decisions/            Architecture decision records (ADRs)
│   └── meeting-notes/
├── src/emergent_cooperation/ Library (see docs/architecture.md)
├── tests/                    pytest suite
├── configs/                  Example experiment configurations (YAML)
├── scripts/                  Convenience scripts (not the reproducible pipeline)
├── notebooks/                Analysis notebooks (analysis only, not app logic)
├── results/                  Experiment outputs (bulk data git-ignored)
└── references/               Bibliography material
```

## Results so far

**➜ Read the [findings summary](docs/findings-summary.md)** — the whole story
(E1–E3) in one page, with the combined overview figure. The individual reports live
in [docs/experiments/](docs/experiments/):

- **[E1 — information & knowledge](docs/experiments/E1-information-and-knowledge.md):**
  cooperation sustains the resource *only* when agents have information (can observe
  the stock) **or** accurate ecological knowledge; blind and misinformed cooperation
  collapses it.
- **[E2 — reciprocity](docs/experiments/E2-reciprocity.md):** conditional cooperation
  protects *fairness* (starves free-riders) but not the *commons* — it can collapse
  the resource faster than unconditional restraint. Neither protects both.
- **[E3 — sanctioning](docs/experiments/E3-sanctioning.md):** enforcement (monitoring +
  a harvest quota) protects *both* the resource and fairness — the only mechanism that
  does — but the monitors bear a cost the others don't (the **second-order free-rider**
  problem).

## Next steps

1. Make monitoring **voluntary/adaptive** — does sanctioning survive its own
   second-order free-rider problem?
2. Sweep retaliation severity (`defection_greed`) and monitoring cost; add forgiveness.
3. Sensitivity/robustness sweeps over group size and regeneration rate.
4. The first **communication** model (trust/reputation) — see
   [docs/decisions/](docs/decisions/) and the Janssen et al. paper-note.
5. The first **disturbance** (sudden resource loss / agent failure) for resilience.

See [docs/research-questions.md](docs/research-questions.md) for the prioritised
question backlog.

## License

MIT — see [LICENSE](LICENSE).
