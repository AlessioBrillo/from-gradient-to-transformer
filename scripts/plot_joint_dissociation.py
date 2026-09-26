#!/usr/bin/env python3
"""Generate joint dissociation figure from capstone shakedown and retune A/B."""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

FIGURES_DIR = Path("figures")
FIGURES_DIR.mkdir(exist_ok=True)

# Data from manifests
# Shakedown (2000 steps, d_model=256, 4L, 8H, P=113, joint)
shakedown = {
    "modular_acc": 0.0047,
    "induction_acc": 0.5041,
    "modular_k99": 98.1,
    "induction_kcomp": 0.394,
}

# Retune A/B (500 steps from shakedown checkpoint)
control = {"modular": 0.00615, "induction": 0.00049, "k99": 98.18, "kcomp": 0.369}
offset = {"modular": 0.00604, "induction": 0.00050, "k99": 98.61, "kcomp": 0.173}
reweight = {"modular": 0.00649, "induction": 0.00052, "k99": 98.11, "kcomp": 0.305}

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# Modular accuracy vs WD (we only have one WD point, so show as bar chart)
ax = axes[0]
arms = ["Control\n(500 steps)", "Vocab\nOffset", "Reweight"]
modular_accs = [control["modular"], offset["modular"], reweight["modular"]]
chance = 1/113

bars = ax.bar(arms, modular_accs, color=["steelblue", "coral", "gold"], alpha=0.7, edgecolor="black")
ax.axhline(y=chance, color="red", linestyle="--", alpha=0.5, label=f"Chance (1/113={chance:.4f})")
ax.set_ylabel("Modular Accuracy")
ax.set_title("Retune A/B: Modular Accuracy\n(500 steps from shakedown)")
ax.legend()
ax.grid(True, alpha=0.3, axis="y")

# Induction accuracy
ax = axes[1]
induction_accs = [control["induction"], offset["induction"], reweight["induction"]]
bars = ax.bar(arms, induction_accs, color=["steelblue", "coral", "gold"], alpha=0.7, edgecolor="black")
ax.set_ylabel("Induction Accuracy")
ax.set_title("Retune A/B: Induction Accuracy")
ax.grid(True, alpha=0.3, axis="y")

# K-composition
ax = axes[2]
kcomps = [control["kcomp"], offset["kcomp"], reweight["kcomp"]]
bars = ax.bar(arms, kcomps, color=["steelblue", "coral", "gold"], alpha=0.7, edgecolor="black")
ax.set_ylabel("Max K-composition")
ax.set_title("Retune A/B: Max K-composition\n(_vacuous - no induction batches in val)")
ax.grid(True, alpha=0.3, axis="y")

plt.tight_layout()
plt.savefig(FIGURES_DIR / "joint_dissociation.png", dpi=150, bbox_inches="tight")
plt.close()

# Also copy to portfolio
import shutil
shutil.copy(FIGURES_DIR / "joint_dissociation.png", Path("portfolio/figures/joint_dissociation.png"))

print("Saved joint_dissociation.png")