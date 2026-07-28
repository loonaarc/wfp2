# web/ — standalone browser demo

[`commons-demo.html`](commons-demo.html) — a self-contained, interactive
common-pool-resource simulator that doubles as a one-page explainer of the whole
project. **Double-click it** (or open it in any browser) — no install, no server, no
internet. Pick a *regime* or drag the dials, and it runs and animates the run: a
central pool being drawn down, agents around it coloured by strategy, a stock
sparkline, and the headline metrics. Below the stage it summarises **what the nine
experiments found** and links into the rest of the repository.

It covers all three research axes: **who is in the group** (strategy mix), **what they
can see** (information/communication), and **whether it survives a shock** (the
`Resource shock` dial and the four `💥 Shock` regimes reproduce the resilience results
E8–E9 — observing populations recover, blind ones collapse, and with free-riders you
also need enforcement).

## Status: presentation layer, not the science

This is a **faithful JavaScript port** of the Python engine, kept as a *communication
tool* — the Python code in [`../src/`](../src/) remains the canonical, tested,
reproducible source of all results.

- The port is **validated** against Python, including the resource shock: the
  deterministic presets reproduce the Python `sustainability / collapsed / Gini /
  harvest` values exactly, and the shock regimes reproduce E8/E9 (cooperative+global
  recovers to K/2, cooperative+private collapses to 0, sanctioning+free-riders
  recovers, cooperative+free-riders does not).
- Deterministic configs match Python exactly. With **decision noise** or **partial
  communication** the browser's RNG differs from NumPy's, so those runs are
  representative, not identical (the presets are all deterministic, so they match).
- The ring layout is **decorative** — the model is non-spatial (agents have no
  positions; the resource is one shared scalar). It illustrates the dynamics; it is
  not a spatial simulation.

The **"Explore the repository"** links in the page are repo-relative, so they resolve
when the file is opened inside the repo (locally or on the code host). A hosted copy
(shareable URL) can also be published via Claude Code's artifact tool from the same
content — there the repo-relative links do not resolve (it is served off-repo), so the
page still works as a standalone explainer but the navigation links are inert.
