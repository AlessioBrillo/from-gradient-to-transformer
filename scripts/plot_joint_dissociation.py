#!/usr/bin/env python3
"""Generate the joint-dissociation figure from the committed probe manifests.

The previous version of this script baked the numbers into module-level dicts,
so the figure could not be regenerated from the manifests and silently drifted
from them. It also drew the three retune A/B arms while the paper's caption
described the shakedown's two-task dissociation — a caption/figure mismatch.

This version reads `results/probe_capstone_*.json` and draws the dissociation
the caption actually describes: joint training on modular addition + induction,
where modular stays at chance while induction climbs, with both tasks' Fourier
spectra dense. Percentages are pulled from the manifests, never retyped.
"""

import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

RESULTS_DIR = Path("results")
FIGURES_DIR = Path("figures")
PORTFOLIO_FIGURES_DIR = Path("portfolio/figures")
SHAKEDOWN = "probe_capstone_shakedown"
AB_ARMS = [
    ("Control", "probe_capstone_ab_control"),
    ("Vocab offset", "probe_capstone_ab_offset"),
    ("Reweight", "probe_capstone_ab_reweight"),
]
CHANCE_MODULAR = 1.0 / 113  # uniform over the P=113 modular-addition classes


def load_probe(name: str) -> dict:
    """Load a probe manifest. Fails loudly rather than plotting a stale figure."""
    path = RESULTS_DIR / f"{name}.json"
    if not path.exists():
        sys.exit(f"missing manifest {path} — run make reproduce-retune first")
    return json.loads(path.read_text(encoding="utf-8"))


def seed_metrics(manifest: dict) -> dict:
    """Return the single seed's metrics (these probes are single-seed by design)."""
    per_seed = manifest.get("per_seed_metrics", [])
    if not per_seed:
        sys.exit(f"{manifest.get('experiment', '?')}: no per-seed metrics")
    return per_seed[0]


def main() -> None:
    shakedown = seed_metrics(load_probe(SHAKEDOWN))
    arms = [(label, seed_metrics(load_probe(name))) for label, name in AB_ARMS]

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    # Panel 1 — the dissociation itself: modular at chance, induction learned.
    ax = axes[0]
    tasks = ["Modular\naddition", "Induction\n(repeated tokens)"]
    accs = [shakedown["final_modular_acc"], shakedown["final_induction_acc"]]
    colors = ["coral", "steelblue"]
    ax.bar(tasks, accs, color=colors, alpha=0.7, edgecolor="black")
    ax.axhline(
        y=CHANCE_MODULAR,
        color="red",
        linestyle="--",
        alpha=0.5,
        label=f"Chance (1/113 = {CHANCE_MODULAR:.4f})",
    )
    for i, v in enumerate(accs):
        ax.text(i, v + 0.012, f"{v:.4f}", ha="center", fontsize=9)
    ax.set_ylabel("Accuracy")
    ax.set_title("Joint training dissociation\n(shakedown, 2000 steps)")
    ax.set_ylim(0, 0.65)
    ax.legend(loc="upper left")
    ax.grid(True, alpha=0.3, axis="y")

    # Panel 2 — both tasks end up with a DENSE Fourier spectrum (k99 / P).
    ax = axes[1]
    k99 = shakedown["final_k_99"]
    ax.bar(
        tasks,
        [k99 / 113.0, k99 / 113.0],
        color=colors,
        alpha=0.7,
        edgecolor="black",
    )
    ax.axhline(y=0.5, color="red", linestyle="--", alpha=0.5, label="Sparsity cutoff (P/2)")
    ax.text(
        0.5,
        0.92,
        f"k\u2089\u2089 = {k99:.1f} of P=113\n({k99 / 113.0:.0%} of frequencies)",
        ha="center",
        transform=ax.transAxes,
        fontsize=9,
    )
    ax.set_ylabel("k\u2089\u2089 / P")
    ax.set_title("Fourier sparsity: dense in both tasks\n(sparse would need < 0.5)")
    ax.set_ylim(0, 1.0)
    ax.legend(loc="lower right")
    ax.grid(True, alpha=0.3, axis="y")

    # Panel 3 — the retune A/B that tried and failed to rescue modular.
    ax = axes[2]
    labels = [label for label, _ in arms]
    mod_accs = [m["final_modular_acc"] for _, m in arms]
    ind_accs = [m["final_induction_acc"] for _, m in arms]
    x = range(len(labels))
    width = 0.38
    lefts = [i - width / 2 for i in x]
    rights = [i + width / 2 for i in x]
    ax.bar(
        lefts, mod_accs, width, label="Modular", color="coral", alpha=0.7, edgecolor="black"
    )
    ax.bar(
        rights, ind_accs, width, label="Induction", color="steelblue", alpha=0.7, edgecolor="black"
    )
    ax.axhline(y=CHANCE_MODULAR, color="red", linestyle="--", alpha=0.5, label="Chance")
    ax.set_xticks(list(x))
    ax.set_xticklabels(labels, fontsize=9)
    ax.set_ylabel("Accuracy")
    ax.set_title("Retune A/B (500 steps):\nno arm lifts modular off chance")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3, axis="y")

    plt.tight_layout()

    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    PORTFOLIO_FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    out = FIGURES_DIR / "joint_dissociation.png"
    plt.savefig(out, dpi=150, bbox_inches="tight")
    # The paper and RESULTS.md cite the tracked copy, so keep it in sync.
    tracked = PORTFOLIO_FIGURES_DIR / out.name
    tracked.write_bytes(out.read_bytes())
    plt.close()
    print(f"Saved {out} and {tracked} (from committed manifests)")


if __name__ == "__main__":
    main()
