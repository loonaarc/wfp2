# Documentation Index

Start here. This project's docs fall into four groups: **orientation** (what it is
and how to run it), **results** (what we found), **reference** (how it works), and
**research process** (decisions, literature, questions).

## ▶ Recommended reading path

1. [getting-started.md](getting-started.md) — hands-on: run it, tweak a config, see
   cooperation succeed or collapse (~20 min).
2. [findings-summary.md](findings-summary.md) — the actual results (experiments
   E1–E13) in one page, with the overview figure.
3. [project-overview.md](project-overview.md) — the problem in plain language.
4. [code-walkthrough.md](code-walkthrough.md) — a guided tour of the Python code,
   with diagrams.
5. Then dip into the reference and research docs below as needed.

**Prefer to see it move?** Open [`../web/commons-demo.html`](../web/commons-demo.html)
in a browser (no install; pick a regime and watch a run unfold round by round), or
run [`../notebooks/explore.ipynb`](../notebooks/explore.ipynb) for the same regimes
backed by the real engine. Both are presentation layers over the same mechanics —
see [getting-started.md](getting-started.md) for setup.

## Orientation

| Doc | What it's for |
| --- | ------------- |
| [getting-started.md](getting-started.md) | Hands-on first run; change one setting and watch the effect. |
| [project-overview.md](project-overview.md) | The problem, in accessible language. |
| [research-direction.md](research-direction.md) | The chosen direction, why, and the phased roadmap. |
| [terminology.md](terminology.md) | Definitions — keep open while reading/writing. |

## Results

| Doc | What it's for |
| --- | ------------- |
| [findings-summary.md](findings-summary.md) | The whole E1–E13 story + overview figure (the writeup spine). |
| [complexity-synthesis.md](complexity-synthesis.md) | Living cross-experiment synthesis of the equifinality/complexity question — grows every time a new axis is tested. |
| [experiments/](experiments/) | One detailed report per experiment (E1–E13); see its index for the one-line summaries. |

## Reference (how it works)

| Doc | What it's for |
| --- | ------------- |
| [code-walkthrough.md](code-walkthrough.md) | Guided, diagram-rich tour of every module. |
| [architecture.md](architecture.md) | Concise reference: components, interfaces, data flow, extension points. |
| [metrics.md](metrics.md) | Metric definitions, formulas, assumptions, limitations. |
| [experiment-design.md](experiment-design.md) | Variables, baselines, seeds, reproducibility rules. |

## Research process

| Doc | What it's for |
| --- | ------------- |
| [thesis-direction-equifinality.md](thesis-direction-equifinality.md) | Brainstorming note for the BA thesis direction — the equifinality reframe, candidate complexity axes, open methodology questions. |
| [research-questions.md](research-questions.md) | Broad questions → testable subquestions → hypotheses (with status). |
| [contribution-opportunities.md](contribution-opportunities.md) | Candidate contributions, assessed for feasibility/risk. |
| [literature-review.md](literature-review.md) | Structured field overview + implications for the model. |
| [paper-notes/](paper-notes/) | One analysed note per paper read. |
| [decisions/](decisions/) | Architecture decision records (ADRs 0001–0011). |
| [meeting-notes/](meeting-notes/) | One file per meeting. |

## Conventions

- **Every significant decision** gets an ADR in [decisions/](decisions/) before or as
  it is made.
- **Every experiment** gets a report in [experiments/](experiments/) that cites the
  script and config that produced it (reproducibility).
- **Every paper read** gets an analysed note in [paper-notes/](paper-notes/) before it
  is marked "read" in the literature review.
- Citations are verified before use; unread sources are flagged as leads only.
