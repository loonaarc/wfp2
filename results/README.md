# results/

Experiment outputs land here, one subdirectory per experiment run. Each contains
`resolved_config.yaml`, `metrics.csv`, `round_history.csv`, and `provenance.json`.

Bulk output files are git-ignored (see `.gitignore`) because every result is
reproducible from its config and seeds. Commit a result directory deliberately
only when it backs a figure or claim in the documentation or thesis.
