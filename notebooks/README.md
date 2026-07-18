# notebooks/

Jupyter notebooks for **analysis only** — reading exported `results/` data and
producing tables/plots. Notebooks are **not** part of the application architecture:
no simulation logic lives here (that belongs in `src/`). This keeps simulation
reproducible and analysis exploratory.

Convention: a notebook loads a specific `results/<name>/metrics.csv` (and
`round_history.csv`) and cites the export directory it used, so figures trace back
to a reproducible run.
