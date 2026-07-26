"""Build the combined overview figure that tells the E1-E3 story in one image.

Loads the committed experiment CSVs (no re-simulation needed) and composes a
three-panel summary:

1. E1 - information/knowledge: cooperation sustains only with information or knowledge.
2. E3 - resource: which mechanism keeps the resource alive under free-riders.
3. E3 - fairness: which mechanism keeps payoffs equal under free-riders.

Output: ``results/synthesis/overview.png``. Run with::

    python scripts/make_synthesis_figure.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"
OUT_DIR = RESULTS / "synthesis"
TYPE_LABELS = {
    "cooperative": "unconditional",
    "conditional_cooperator": "conditional",
    "sanctioning": "sanctioning",
}


def main() -> None:
    """Compose and save the three-panel overview figure."""
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    e1 = pd.read_csv(RESULTS / "E1_information_knowledge" / "sweep_information.csv")
    e1_mean = (
        e1.groupby(["information_model", "initial_level"])["sustainability_ratio"]
        .mean()
        .reset_index()
    )
    e3 = pd.read_csv(RESULTS / "E3_sanctioning" / "sweep.csv")

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 4.4))

    # Panel 1 - E1: information / knowledge.
    for model in ["global", "private"]:
        sub = e1_mean[e1_mean["information_model"] == model].sort_values("initial_level")
        ax1.plot(sub["initial_level"], sub["sustainability_ratio"], marker="o", label=model)
    ax1.axvline(50, color="grey", ls=":", lw=1)
    ax1.set_xlabel("initial stock")
    ax1.set_ylabel("sustainability ratio")
    ax1.set_title("1. Cooperation needs information\nOR knowledge (E1)")
    ax1.set_ylim(-0.02, 1.0)
    ax1.legend(title="information")

    # Panel 2 - E3: resource survival by mechanism.
    for ctype, label in TYPE_LABELS.items():
        sub = e3[e3["cooperator_type"] == ctype].sort_values("n_selfish")
        ax2.plot(sub["n_selfish"], sub["sustainability_ratio"], marker="o", label=label)
    ax2.set_xlabel("number of selfish agents (of 8)")
    ax2.set_ylabel("sustainability ratio")
    ax2.set_title("2. Only sanctioning saves\nthe resource (E2/E3)")
    ax2.set_ylim(-0.02, 0.6)
    ax2.legend(title="mechanism")

    # Panel 3 - E3: fairness by mechanism.
    for ctype, label in TYPE_LABELS.items():
        sub = e3[e3["cooperator_type"] == ctype].sort_values("n_selfish")
        ax3.plot(sub["n_selfish"], sub["payoff_gini"], marker="s", label=label)
    ax3.set_xlabel("number of selfish agents (of 8)")
    ax3.set_ylabel("payoff Gini (0 = equal)")
    ax3.set_title("3. ...and keeps payoffs\nfair (E2/E3)")
    ax3.set_ylim(-0.02, 0.8)
    ax3.legend(title="mechanism")

    fig.suptitle(
        "Emergent cooperation in a common-pool resource: information, and the mechanism ladder",
        fontsize=13,
    )
    fig.tight_layout()
    fig.savefig(OUT_DIR / "overview.png", dpi=130)
    plt.close(fig)
    print(f"Wrote {OUT_DIR / 'overview.png'}")


if __name__ == "__main__":
    main()
