# Getting Started — a hands-on walkthrough

This is a guided tour. You'll run a few commands, read their output, and change
one setting to see the system respond — with the concepts explained inline as they
come up. Budget ~20–30 minutes. By the end you'll understand what this repo does
and be able to explain it.

You don't need to read any other doc first. Pointers to deeper docs appear as you
go.

> **Just want to watch it first?** Open [`../web/commons-demo.html`](../web/commons-demo.html)
> in any browser — no install needed. Pick a regime (tragedy, sustainable,
> enforcement, …) and step through a run round by round. It's a faithful port of the
> engine below; this walkthrough explains *why* those runs behave as they do.

---

## 0. One-time setup

If you haven't installed the project yet (see [../README.md](../README.md)):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1        # activate the environment (Windows PowerShell)
pip install -e ".[dev,analysis]"
```

Once activated, your prompt shows `(.venv)` and the `emergent-coop` command is
available. Every command below assumes the environment is active. *(If you don't
want to activate it, prefix commands with `.venv\Scripts\`, e.g.
`.venv\Scripts\emergent-coop run ...`.)*

---

## 1. What can the agents do?

```powershell
emergent-coop strategies
```

```
Available strategies:
  - compensating_cooperator
  - conditional_cooperator
  - cooperative
  - sanctioning
  - selfish
```

A **strategy** is an agent's decision rule — given what the agent sees, how much
of the shared resource does it try to take this round? There are five (defined in
[terminology.md](terminology.md#cooperation-mechanisms-the-strategies)):

- **`selfish`** — grab a large share of whatever is currently available.
- **`cooperative`** — take only your fair share of what *regrew*, leaving the pool
  healthy.
- **`conditional_cooperator`** — cooperate *until* others over-extract, then
  retaliate (reciprocity).
- **`compensating_cooperator`** — on over-extraction, *withhold* to let the pool
  recover (restraint).
- **`sanctioning`** — cooperate *and* enforce a sustainable quota on everyone, at a
  monitoring cost.

The first two are the core contrast (and where this walkthrough focuses); the rest
are studied in experiments E2–E7 — see the [findings summary](findings-summary.md).

---

## 2. The scenario in one paragraph

Several agents share **one renewable resource** (think of a fish stock or a shared
budget). Each round: the resource **regenerates** a bit, then every agent decides
how much to **harvest**. If they collectively take too much, the resource
**collapses** and can't recover. Agents follow simple local rules and may see
different information. We run this many times with controlled randomness and
**measure** what happens.

The resource regrows by a *logistic* rule: growth is fastest when the stock is at
half its maximum and stops at zero (a depleted pool stays dead). With our default
numbers (capacity `K=100`, growth rate `g=0.4`), the most that can be harvested
forever — the **maximum sustainable yield** — is `10` per round.

---

## 3. Run the cooperative baseline

An **experiment** is one scenario described by a config file, run once per random
**seed** so we can see how consistent the result is. Let's run the all-cooperative
scenario:

```powershell
emergent-coop run --config configs/all_cooperative_global.yaml
```

You'll see a summary and a line like `Results written to: results\all_cooperative_global`.
Open that folder — four files were written:

| file | what it is |
| ---- | ---------- |
| `resolved_config.yaml` | the exact settings that were run |
| `metrics.csv` | one row of results per seed |
| `round_history.csv` | the full round-by-round trajectory |
| `provenance.json` | reproducibility record (code version, timestamp, seeds) |

Open `results/all_cooperative_global/round_history.csv`. The first rounds look like:

```
seed,round,resource_start,resource_after_regen,total_requested,total_harvested,resource_after_harvest,collapsed
1,0,50.0,60.0,10.0,10.0,50.0,False
1,1,50.0,60.0,10.0,10.0,50.0,False
```

Read one row left to right: stock starts at **50** → regenerates to **60** → the 8
agents together take exactly the **10** that regrew → stock is back to **50**.
Forever. Total harvested over 100 rounds = **1000**, and the pool is never
harmed. **This is emergent cooperation:** nobody is *told* to hold back, but the
simple local rule sustains the shared resource.

---

## 4. Run the selfish baseline — watch it collapse

```powershell
emergent-coop run --config configs/all_selfish_global.yaml
```

Open `results/all_selfish_global/round_history.csv`:

```
seed,round,resource_start,resource_after_regen,total_requested,total_harvested,resource_after_harvest,collapsed
1,0,50.0,60.0,60.0,60.0,0.0,True
1,1,0.0,0.0,0.0,0.0,0.0,True
```

Round 0: stock regenerates to 60, the agents collectively demand **all 60**,
harvest it, and the stock crashes to **0** — `collapsed=True`. From then on there's
nothing left to regrow. Total harvest over 100 rounds is a measly **60**.

This is the **tragedy of the commons**: each agent taking a "fair share of what's
visible" is individually reasonable, but collectively it destroys the resource that
restraint would have sustained indefinitely (compare: 60 vs 1000).

---

## 5. Mix them — free-riding and fairness

```powershell
emergent-coop run --config configs/mixed_global.yaml
```

Look at the printed summary: `collapsed` is 1.0 (it still collapses) and
`payoff_gini` is about **0.44**. The **Gini coefficient** measures inequality of
earnings: 0 = everyone earns the same, higher = more unequal. Here it's high
because the 4 selfish agents **free-ride** — they grab more while the 4 cooperators
try (and fail) to protect the pool. A minority of selfish agents is enough to sink
everyone *and* walk away with the larger share.

> This is subquestion **SQ-4** in [research-questions.md](research-questions.md):
> how many selfish agents does it take to tip a population into collapse?

---

## 6. Your turn (1): find the selfish tipping point

`greed` controls how much a selfish agent grabs. Let's find where "selfish" stops
being fatal.

1. Open [../configs/all_selfish_global.yaml](../configs/all_selfish_global.yaml).
2. Find `greed: 1.0` and change it to `greed: 0.2`. Save.
3. Run it:
   ```powershell
   emergent-coop run --config configs/all_selfish_global.yaml
   ```
   **Expected:** no collapse, total harvest ≈ **957**, final stock ≈ 37. Even
   "selfish" agents sustain the resource if each takes little enough.
4. Now change it to `greed: 0.3`, save, and run again.
   **Expected:** collapse returns, total harvest ≈ **271**.

Somewhere between `0.2` and `0.3` the system flips from *sustainable* to *doomed* —
a **threshold effect** (hypothesis **H2**). You just did a miniature experiment.

**Change `greed` back to `1.0` and save** before moving on.

---

## 7. Your turn (2): why information matters *(the payoff)*

The two configs `all_cooperative_global` and `all_cooperative_private` are
**identical except one line**: whether agents can *see the current stock*.

- `global` — agents observe the stock and take only the surplus above a healthy
  level (so if the stock is low, they take nothing and let it recover).
- `private` — agents are **blind** to the stock and just take a fixed "sustainable"
  amount, hoping the pool is healthy.

At the default starting stock (50) these behave identically. But watch what happens
when the resource starts **depleted**:

1. In [../configs/all_cooperative_private.yaml](../configs/all_cooperative_private.yaml),
   change `initial_level: 50.0` to `initial_level: 20.0`. Save. Run it:
   ```powershell
   emergent-coop run --config configs/all_cooperative_private.yaml
   ```
   **Expected:** it **collapses** (total harvest ≈ 38). The blind agents keep taking
   their fixed amount even though the depleted pool can't regrow that fast, and they
   grind it to zero.
2. Now do the same edit in
   [../configs/all_cooperative_global.yaml](../configs/all_cooperative_global.yaml)
   (`initial_level: 20.0`), save, and run it.
   **Expected:** it **fully recovers** to 50 (total harvest ≈ 963, no collapse). The
   agents *see* the stock is low, back off, and let it heal.

**Same agents, same cooperative rule — the only difference is what they can see, and
it decides survival vs. collapse.** This is the core of the whole project: *how much
information do agents need for stable cooperation?* (Hypothesis **H1**.)

**Reset both `initial_level` values back to `50.0`** when you're done.

---

## 8. What just happened, in terms of the code

Everything you ran flows through the same small pipeline
(full detail in [architecture.md](architecture.md)):

```
config (YAML) → Simulation(seed) → per-round: regenerate → observe → harvest → RunResult → metrics → files
```

- **What agents can see** is controlled by the *observation* (`information_model`).
- **What agents do** is the *strategy* (`selfish` / `cooperative`).
- **How the resource behaves** is the *environment* (regeneration rule).
- **Randomness** is fixed by the *seed*, so results are reproducible.

The pieces are deliberately separable so you can vary **one thing at a time** — the
essence of a controlled experiment ([experiment-design.md](experiment-design.md)).

---

## 9. Reproducibility (why the extra files exist)

Run any experiment twice with the same seeds and you get **identical** results —
guaranteed, because all randomness comes from the seed. The `provenance.json` file
records the code version, git commit, platform, and timestamp, so any result can be
traced back and re-run months later. That "anyone can reproduce this" property is a
real part of the project's contribution, not bookkeeping
([terminology.md → reproducibility](terminology.md)).

---

## 10. Where to go next

You've seen the whole system. Good follow-ups, in order:

0. **[findings-summary.md](findings-summary.md)** — the actual results (experiments
   E1–E7) in one page, with the overview figure. Read this to see what the tool has
   *found*, not just how it works.
1. **[project-overview.md](project-overview.md)** — the problem in plain language,
   now that you've seen it in action.
2. **[research-questions.md](research-questions.md)** — the backlog of questions we
   can investigate. Your project's specific contribution comes from here. The 🟢
   ones are answerable with today's code.
3. **[research-direction.md](research-direction.md)** — the phased roadmap and your
   "elevator pitch" for what this project is.
4. **[terminology.md](terminology.md)** — keep it open while reading/writing; it's
   the vocabulary for your report.
5. **[contribution-opportunities.md](contribution-opportunities.md)** — what a
   defensible bachelor-level contribution looks like here.

Prefer to explore interactively rather than read? Two presentation layers over the
same mechanics: the browser demo
[`../web/commons-demo.html`](../web/commons-demo.html) (no install) and the notebook
[`../notebooks/explore.ipynb`](../notebooks/explore.ipynb) (regime presets + sliders,
backed by the real engine).

When you want to *add* something (a new strategy, a metric), see the extension-point
table in [architecture.md](architecture.md).
