# web/ — standalone browser demo

[`commons-demo.html`](commons-demo.html) — a self-contained, interactive
common-pool-resource simulator. **Double-click it** (or open it in any browser) — no
install, no server, no internet. Pick a *regime* or drag the dials, and it runs and
animates the run: a central pool being drawn down, agents around it coloured by
strategy, a stock sparkline, and the headline metrics.

## Status: presentation layer, not the science

This is a **faithful JavaScript port** of the Python engine, kept as a *communication
tool* — the Python code in [`../src/`](../src/) remains the canonical, tested,
reproducible source of all results.

- The port is **validated** against Python: all seven presets reproduce the Python
  `sustainability / collapsed / Gini / harvest` values exactly.
- Deterministic configs match Python exactly. With **decision noise** or **partial
  communication** the browser's RNG differs from NumPy's, so those runs are
  representative, not identical (the presets are all deterministic, so they match).
- The ring layout is **decorative** — the model is non-spatial (agents have no
  positions; the resource is one shared scalar). It illustrates the dynamics; it is
  not a spatial simulation.

A hosted copy (shareable URL) can also be published via Claude Code's artifact tool
from the same content.
