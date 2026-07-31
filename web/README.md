# web/ — standalone browser demo

[`commons-demo.html`](commons-demo.html) — a self-contained, interactive
common-pool-resource simulator that doubles as a one-page explainer of the whole
project. **Double-click it** (or open it in any browser) — no install, no server, no
internet. Pick a *regime* or drag the dials, and it runs and animates the run: a
central pool being drawn down, agents around it coloured by strategy, a stock
sparkline, and the headline metrics. Below the stage it summarises **what the nine
experiments found** and links into the rest of the repository.

It covers all three research axes: **who is in the group** (strategy mix), **what they
can see** (information/communication), and **whether it survives a disturbance**. The
`Resource shock` dial and the four `💥 Shock` regimes reproduce E8–E9 (observing
populations recover, blind ones collapse, and with free-riders you also need
enforcement); the `Agent failure` dial and the `🔌/🧩` regimes reproduce E10 (losing
the enforcer collapses the commons, losing a self-correcting member does not —
enforcement is a single point of failure).

## Status: presentation layer, not the science

This is a **faithful JavaScript port** of the Python engine, kept as a *communication
tool* — the Python code in [`../src/`](../src/) remains the canonical, tested,
reproducible source of all results.

- The port is **validated** against Python, including both disturbances: the
  deterministic presets reproduce the Python `sustainability / collapsed / Gini /
  harvest` values exactly; the shock regimes reproduce E8/E9 (cooperative+global
  recovers to K/2, cooperative+private collapses to 0, sanctioning+free-riders
  recovers, cooperative+free-riders does not); the agent-failure regimes reproduce
  E10 (enforcer-fails collapses to 0, member-fails holds at K/2).
- Deterministic configs match Python exactly. With **decision noise** or **partial
  communication** the browser's RNG differs from NumPy's, so those runs are
  representative, not identical (the presets are all deterministic, so they match).
- The ring layout is **decorative** — the model is non-spatial (agents have no
  positions; the resource is one shared scalar). It illustrates the dynamics; it is
  not a spatial simulation.

The **"Explore the repository"** links in the page point to the rendered files on
GitHub (`github.com/loonaarc/wfp2`), so they open the same way wherever the demo is
viewed — served raw, hosted, or published as an artifact. (They are absolute URLs, so
they require the repo to be public and do not resolve when browsing the file fully
offline.)
