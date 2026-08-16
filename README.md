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
>
> **Just want to play?** Open [`web/commons-demo.html`](web/commons-demo.html) in any
> browser (no install) — an interactive, animated simulator (a validated JS port of
> the engine).

## Status

**Working and tested:**

- deterministic simulation core (regenerate → observe → decide → ration → enforce →
  harvest), with an optional `decision_noise` stochastic knob;
- a renewable resource with logistic/linear regeneration;
- **eight strategies** (`selfish`, `cooperative`, `conditional_cooperator`,
  `sanctioning`, `compensating_cooperator`, `loner`, `reputation_cooperator`,
  `grim_trigger`) —
  defined in [docs/terminology.md](docs/terminology.md#cooperation-mechanisms);
- two information conditions (`global` / `private`) plus a **broadcast communication**
  channel (`broadcast_reliability`);
- controlled random seeds with independent per-agent RNG streams;
- configuration-driven experiments (YAML) with seed sweeps and a grid runner;
- metrics: performance, efficiency, sustainability, collapse, survival time,
  over-usage, and fairness (Gini);
- reproducible result export (config + metrics + history + provenance);
- environmental **disturbances** (a resource shock) with resilience metrics (E8);
- a CLI and twenty-three experiments (E1–E23) — current experiment and
  test counts live in [docs/findings-summary.md](docs/findings-summary.md)'s
  Status line, the one place they're kept up to date.

Partly implemented: disturbances so far cover a single resource shock (agent /
communication failure are next), and the full per-agent `CommunicationModel` (a first
broadcast model is implemented). See
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

## Architecture

```
config (YAML) ─► ExperimentConfig ─► Simulation(seed) ─► RunResult ─► metrics ─► export
                                         │
                    ┌────────────────────┼─────────────────────┐
                    ▼                    ▼                     ▼
              ResourcePool           Agents              Communication (broadcast)
             (regeneration)      (Strategy each)         + Disturbances (resource shock)
```

Each round: the resource regenerates, any scheduled disturbance perturbs it, agents
observe (subject to the information model and any communicated signal), agents request
consumption, requests are scaled to fit the stock, sanctioners enforce a quota,
harvest is assigned, payoffs update.
Full detail in [docs/architecture.md](docs/architecture.md).

## Repository structure

```
├── README.md                 This file
├── pyproject.toml            Project + tooling (pytest, ruff) configuration
├── docs/                     Documentation — see docs/README.md for the index
│   ├── README.md             Documentation index + recommended reading path
│   ├── getting-started.md    Hands-on walkthrough (run it, tweak it)
│   ├── findings-summary.md   The E1–E23 results in one page (the writeup spine)
│   ├── project-overview.md   The problem in accessible language
│   ├── research-direction.md Chosen direction and roadmap (canonical)
│   ├── research-questions.md Broad questions, testable subquestions, hypotheses
│   ├── terminology.md        Definitions of key terms (incl. the strategies)
│   ├── code-walkthrough.md   Guided tour of the Python code, with diagrams
│   ├── architecture.md       Components, interfaces, data flow
│   ├── experiment-design.md  Variables, baselines, seeds, reproducibility
│   ├── metrics.md            Metric definitions, formulas, limitations
│   ├── experiments/          One report per experiment E1–E23 (+ index)
│   ├── contribution-opportunities.md
│   ├── literature-review.md  Structured overview of the field
│   ├── paper-notes/          One analysed note per paper (+ template)
│   ├── decisions/            Architecture decision records (ADRs 0001–0020)
│   └── meeting-notes/
├── src/emergent_cooperation/ Library (see docs/architecture.md)
├── tests/                    pytest suite
├── configs/                  Example experiment configurations (YAML)
├── scripts/                  Convenience scripts (not the reproducible pipeline)
├── notebooks/                Analysis notebooks (analysis only, not app logic)
├── results/                  Experiment outputs (bulk data git-ignored)
├── references/               Bibliography material (+ git-ignored papers/)
└── web/                      Standalone interactive browser demo (validated JS port)
```

## Results so far

**➜ Read the [findings summary](docs/findings-summary.md)** — the whole story
(experiments **E1–E23**) in one page, with the overview figure. The
per-experiment reports and a one-line index live in
[docs/experiments/](docs/experiments/).

The throughline: cooperation needs *information* (E1, E6); its outcome is decided by
the *mechanism/response* (E2, E3, E7); **communication informs but does not
coordinate — only a binding rule (enforcement) protects both the resource and
fairness** (E7); enforcement is itself fragile when voluntary (E5); and the results
are robust to noise (E4).

## Next steps

The roadmap lives in [docs/research-direction.md](docs/research-direction.md). The
standout open thread is a **binding agreement / collective-choice** mechanism (can
communication produce a consented quota and fund the monitoring to uphold it?), plus
the **disturbance** axis (resource shocks / agent failure) for resilience.

See [docs/research-questions.md](docs/research-questions.md) for the prioritised
question backlog.

## License

MIT — see [LICENSE](LICENSE).
