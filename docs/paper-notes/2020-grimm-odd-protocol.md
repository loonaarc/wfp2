# The ODD Protocol: A Second Update (Grimm et al. 2020)

Read status: 🟢 read from the open-access article (JASSS, https://www.jasss.org/23/2/7.html).

## Citation
Grimm, V., Railsback, S. F., Vincenot, C. E., Berger, U., Gallagher, C., DeAngelis,
D. L., … Ayllón, D. (2020). The ODD Protocol for Describing Agent-Based and Other
Simulation Models: A Second Update to Improve Clarity, Replication, and Structural
Realism. *Journal of Artificial Societies and Social Simulation*, 23(2), 7.
https://doi.org/10.18564/jasss.4259

## Research Problem
Agent-based models are often described incompletely and inconsistently, which
undermines **replication** and comparison. ODD ("Overview, Design concepts, Details")
is a standardized document structure for describing ABMs completely enough to
re-implement *without the code*.

## The Seven Elements (in order)
**Overview** — (1) *Purpose and patterns*; (2) *Entities, state variables and scales*;
(3) *Process overview and scheduling*. **Design concepts** — (4) the 11 *design
concepts* (emergence, adaptation, objectives, learning, prediction, sensing,
interaction, stochasticity, collectives, observation, …). **Details** — (5)
*Initialization*; (6) *Input data*; (7) *Submodels*.

## What the 2020 update changed
Added **patterns** to element 1 (integrating pattern-oriented modelling); optional
per-element **Rationale** subsections; checklists and a **summary-ODD template** for
journal articles; guidance for **nested ODDs**, **delta-ODD** (model reuse), and
**linking ODD text to code**; and a broader "any simulation model" applicability claim.

## Relevance to This Project
ODD is the natural standard to structure our model description for the thesis and to
make the simulation **replicable and comparable** to the CPR/ABM literature. Mapping
our repo onto ODD:

- **Purpose & patterns** → [project-overview.md](../project-overview.md); the
  "patterns" are our qualitative baselines (tragedy-of-the-commons collapse; sustained
  cooperation at MSY) that the model must reproduce.
- **Entities, state variables, scales** → agents (strategy, payoff), the scalar
  `ResourcePool`, discrete rounds — see [architecture.md](../architecture.md).
- **Process overview & scheduling** → the fixed round order (regenerate → observe →
  decide → ration → enforce → harvest).
- **Design concepts** → *emergence* (cooperation/collapse), *adaptation* (E5
  replicator), *sensing* (information models + communication signal), *stochasticity*
  (`decision_noise`, message loss), *interaction* (shared pool, enforcement),
  *observation* (metrics).
- **Initialization / input data / submodels** → config (`SimulationConfig`), the
  regeneration rule, and the strategy `decide` methods.

**Action:** add a compact **ODD-structured model description** (a new `docs/` section
or a summary block in `architecture.md`) so the write-up aligns with the field
standard. Much of the material already exists across our docs; ODD would organise it.

## Possible Follow-Up Contribution
A one-page summary-ODD of the model in the thesis, with the full ODD in an appendix —
low effort, high credibility, and exactly what reviewers of ABM work expect.

## Important Terms
ODD; pattern-oriented modelling; design concepts; submodel; replication; summary-ODD;
delta-ODD.

## Questions
- Which of the 11 design concepts genuinely apply to us vs. can be marked "not
  applicable" (e.g. *learning*, *prediction* — we have neither yet)?
- Do we structure the ODD as its own `docs/model-odd.md`, or fold it into
  `architecture.md`?
