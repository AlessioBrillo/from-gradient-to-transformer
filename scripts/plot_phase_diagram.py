#!/usr/bin/env python3
"""Generate phase diagram heatmap and boundary analysis figures.

Usage:
    python scripts/plot_phase_diagram.py --manifest results/phase_diagram.pt
"""

import argparse
import logging
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import torch

logger = logging.getLogger(__name__)

FIGURES_DIR = Path("figures")
FIGURES_DIR.mkdir(exist_ok=True)


def load_manifest(manifest_path: Path) -> dict:
    """Load phase diagram manifest."""
    data = torch.load(manifest_path, map_location="cpu", weights_only=False)
    return data["cells"]


def classify_sparse(cell: dict) -> bool:
    """Classify cell as sparse (k_99/P < 0.5) or dense."""
    return cell["k_99_percent"]["mean"] < cell["modulus"] * 0.5


def plot_phase_diagram_heatmap(cells: dict, save_path: Path) -> None:
    """Plot phase diagram heatmap: P × WD for solo and joint modes."""
    
    solo_cells = {k: v for k, v in cells.items() if v["mode"] == "solo"}
    joint_cells = {k: v for k, v in cells.items() if v["mode"] == "joint"}
    
    if not solo_cells and not joint_cells:
        logger.warning("No cells to plot")
        return
    
    # Collect unique values
    moduli = sorted(set(v["modulus"] for v in solo_cells.values()))
    wds = sorted(set(v["weight_decay"] for v in solo_cells.values()))
    
    fig, axes = plt.subplots(1, 2 if joint_cells else 1, figsize=(14, 6))
    if not joint_cells:
        axes = [axes]
    
    # Solo mode heatmap
    ax = axes[0]
    heatmap = np.full((len(moduli), len(wds)), np.nan)
    annotations = np.full((len(moduli), len(wds)), "", dtype=object)
    
    for cell in solo_cells.values():
        p_idx = moduli.index(cell["modulus"])
        wd_idx = wds.index(cell["weight_decay"])
        k99_ratio = cell["k_99_percent"]["mean"] / cell["modulus"]
        heatmap[p_idx, wd_idx] = k99_ratio
        sparse = classify_sparse(cell)
        annotations[p_idx, wd_idx] = f"{k99_ratio:.2f}\n{'S' if sparse else 'D'}"
    
    im = ax.imshow(heatmap, aspect='auto', cmap='RdYlGn_r', vmin=0, vmax=1, origin='lower')
    ax.set_xticks(range(len(wds)))
    ax.set_xticklabels([f"{wd:.1f}" for wd in wds])
    ax.set_yticks(range(len(moduli)))
    ax.set_yticklabels([str(p) for p in moduli])
    ax.set_xlabel("Weight Decay")
    ax.set_ylabel("Modulus P")
    ax.set_title("Solo Modular Addition: k₉₉/P Ratio (Red=Dense, Green=Sparse)")
    
    # Add annotations
    for i in range(len(moduli)):
        for j in range(len(wds)):
            if annotations[i, j]:
                color = 'white' if heatmap[i, j] > 0.5 else 'black'
                ax.text(j, i, annotations[i, j], ha='center', va='center', color=color, fontsize=8)
    
    plt.colorbar(im, ax=ax, label="k₉₉ / P")
    
    # Joint mode heatmap
    if joint_cells:
        ax = axes[1]
        joint_moduli = sorted(set(v["modulus"] for v in joint_cells.values()))
        joint_wds = sorted(set(v["weight_decay"] for v in joint_cells.values()))
        
        heatmap = np.full((len(joint_moduli), len(joint_wds)), np.nan)
        annotations = np.full((len(joint_moduli), len(joint_wds)), "", dtype=object)
        
        for cell in joint_cells.values():
            p_idx = joint_moduli.index(cell["modulus"])
            wd_idx = joint_wds.index(cell["weight_decay"])
            k99_ratio = cell["k_99_percent"]["mean"] / cell["modulus"]
            heatmap[p_idx, wd_idx] = k99_ratio
            sparse = classify_sparse(cell)
            annotations[p_idx, wd_idx] = f"{k99_ratio:.2f}\n{'S' if sparse else 'D'}"
        
        im = ax.imshow(heatmap, aspect='auto', cmap='RdYlGn_r', vmin=0, vmax=1, origin='lower')
        ax.set_xticks(range(len(joint_wds)))
        ax.set_xticklabels([f"{wd:.1f}" for wd in joint_wds])
        ax.set_yticks(range(len(joint_moduli)))
        ax.set_yticklabels([str(p) for p in joint_moduli])
        ax.set_xlabel("Weight Decay")
        ax.set_ylabel("Modulus P")
        ax.set_title("Joint Modular+Induction: k₉₉/P Ratio")
        
        for i in range(len(joint_moduli)):
            for j in range(len(joint_wds)):
                if annotations[i, j]:
                    color = 'white' if heatmap[i, j] > 0.5 else 'black'
                    ax.text(j, i, annotations[i, j], ha='center', va='center', color=color, fontsize=8)
        
        plt.colorbar(im, ax=ax, label="k₉₉ / P")
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close()
    logger.info(f"Saved phase diagram heatmap to {save_path}")


def plot_phase_boundary_analysis(cells: dict, save_path: Path) -> None:
    """Plot theoretical boundary vs empirical cells."""
    
    solo_cells = {k: v for k, v in cells.items() if v["mode"] == "solo"}
    
    if not solo_cells:
        logger.warning("No solo cells for boundary analysis")
        return
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # 1. k₉₉/P vs WD at different P
    ax = axes[0, 0]
    moduli = sorted(set(v["modulus"] for v in solo_cells.values()))
    for p in moduli:
        p_cells = [v for v in solo_cells.values() if v["modulus"] == p]
        wds = sorted(set(v["weight_decay"] for v in p_cells))
        k99_ratios = []
        for wd in wds:
            cell = next((v for v in p_cells if v["weight_decay"] == wd), None)
            if cell:
                k99_ratios.append(cell["k_99_percent"]["mean"] / cell["modulus"])
            else:
                k99_ratios.append(np.nan)
        ax.plot(wds, k99_ratios, 'o-', label=f"P={p}", markersize=6)
    
    ax.axhline(y=0.5, color='red', linestyle='--', alpha=0.5, label="Sparse threshold (0.5)")
    ax.set_xlabel("Weight Decay")
    ax.set_ylabel("k₉₉ / P")
    ax.set_title("Sparsity vs Weight Decay (per P)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_ylim(0, 1.05)
    
    # 2. k₉₉/P vs P at different WD
    ax = axes[0, 1]
    wds = sorted(set(v["weight_decay"] for v in solo_cells.values()))
    for wd in wds:
        wd_cells = [v for v in solo_cells.values() if v["weight_decay"] == wd]
        moduli_sorted = sorted(set(v["modulus"] for v in wd_cells))
        k99_ratios = []
        for p in moduli_sorted:
            cell = next((v for v in wd_cells if v["modulus"] == p), None)
            if cell:
                k99_ratios.append(cell["k_99_percent"]["mean"] / cell["modulus"])
            else:
                k99_ratios.append(np.nan)
        ax.plot(moduli_sorted, k99_ratios, 's-', label=f"WD={wd}", markersize=6)
    
    ax.axhline(y=0.5, color='red', linestyle='--', alpha=0.5)
    ax.set_xlabel("Modulus P")
    ax.set_ylabel("k₉₉ / P")
    ax.set_title("Sparsity vs Modulus (per WD)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_ylim(0, 1.05)
    
    # 3. Theoretical boundary: WD_crit ≈ C * (d_model * n_layers) / (P * train_frac)
    ax = axes[1, 0]
    # For fixed model (d_model=128, n_layers=1, train_frac=0.3)
    # WD_crit ≈ k / P
    C = 60  # fitted constant
    P_range = np.linspace(10, 120, 100)
    WD_crit = C / P_range
    
    ax.plot(P_range, WD_crit, 'k--', label=f"Theoretical: WD_crit ≈ {C}/P", linewidth=2)
    
    # Empirical cells
    for cell in solo_cells.values():
        p = cell["modulus"]
        wd = cell["weight_decay"]
        k99_ratio = cell["k_99_percent"]["mean"] / cell["modulus"]
        color = 'green' if k99_ratio < 0.5 else 'red'
        ax.scatter(p, wd, c=color, s=100, alpha=0.7, edgecolors='black', 
                  label='Sparse' if k99_ratio < 0.5 else 'Dense')
    
    # Avoid duplicate labels
    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys())
    
    ax.set_xlabel("Modulus P")
    ax.set_ylabel("Weight Decay")
    ax.set_title("Phase Boundary: Theory vs Empirical")
    ax.grid(True, alpha=0.3)
    ax.set_ylim(0, max(v["weight_decay"] for v in solo_cells.values()) * 1.2)
    
    # 4. Generalization epoch vs k₉₉/P
    ax = axes[1, 1]
    for cell in solo_cells.values():
        k99_ratio = cell["k_99_percent"]["mean"] / cell["modulus"]
        gen_epoch = cell["generalization_epoch"]["mean"]
        if gen_epoch > 0:
            color = 'green' if k99_ratio < 0.5 else 'red'
            ax.scatter(k99_ratio, gen_epoch, c=color, s=80, alpha=0.7, edgecolors='black')
    
    ax.set_xlabel("k₉₉ / P")
    ax.set_ylabel("Generalization Epoch")
    ax.set_title("Generalization Speed vs Sparsity")
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 1.05)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close()
    logger.info(f"Saved phase boundary analysis to {save_path}")


def plot_model_size_sweep(cells: dict, save_path: Path) -> None:
    """Plot model size sweep at fixed P=59."""
    
    solo_cells = {k: v for k, v in cells.items() if v["mode"] == "solo" and v["modulus"] == 59}
    
    if not solo_cells:
        return
    
    # Group by model size
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    # d_model sweep
    ax = axes[0]
    for cell in solo_cells.values():
        if cell["n_layers"] == 1 and cell["weight_decay"] == 1.0:
            k99_ratio = cell["k_99_percent"]["mean"] / cell["modulus"]
            gen_epoch = cell["generalization_epoch"]["mean"]
            ax.scatter(cell["d_model"], k99_ratio, s=100, alpha=0.7, edgecolors='black',
                      c='green' if k99_ratio < 0.5 else 'red')
    
    ax.set_xlabel("d_model")
    ax.set_ylabel("k₉₉ / P")
    ax.set_title("Model Width Sweep (P=59, WD=1.0, 1L)")
    ax.grid(True, alpha=0.3)
    ax.set_ylim(0, 1.05)
    
    # n_layers sweep
    ax = axes[1]
    for cell in solo_cells.values():
        if cell["d_model"] == 128 and cell["weight_decay"] == 1.0:
            k99_ratio = cell["k_99_percent"]["mean"] / cell["modulus"]
            ax.scatter(cell["n_layers"], k99_ratio, s=100, alpha=0.7, edgecolors='black',
                      c='green' if k99_ratio < 0.5 else 'red')
    
    ax.set_xlabel("n_layers")
    ax.set_ylabel("k₉₉ / P")
    ax.set_title("Depth Sweep (P=59, WD=1.0, d_model=128)")
    ax.grid(True, alpha=0.3)
    ax.set_ylim(0, 1.05)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close()
    logger.info(f"Saved model size sweep to {save_path}")


def plot_joint_dissociation(cells: dict, save_path: Path) -> None:
    """Plot joint training dissociation: modular vs induction."""
    
    joint_cells = {k: v for k, v in cells.items() if v["mode"] == "joint"}
    
    if not joint_cells:
        return
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    # Modular accuracy vs WD
    ax = axes[0]
    for cell in joint_cells.values():
        mod_acc = cell["final_val_acc"]["mean"]
        wd = cell["weight_decay"]
        ax.scatter(wd, mod_acc, s=100, alpha=0.7, edgecolors='black', label=f"WD={wd}")
    ax.set_xlabel("Weight Decay")
    ax.set_ylabel("Modular Accuracy")
    ax.set_title("Joint: Modular Accuracy vs WD")
    ax.grid(True, alpha=0.3)
    
    # Induction accuracy vs WD
    ax = axes[1]
    for cell in joint_cells.values():
        ind_acc = cell["final_induction_acc"]["mean"]
        wd = cell["weight_decay"]
        ax.scatter(wd, ind_acc, s=100, alpha=0.7, edgecolors='black')
    ax.set_xlabel("Weight Decay")
    ax.set_ylabel("Induction Accuracy")
    ax.set_title("Joint: Induction Accuracy vs WD")
    ax.grid(True, alpha=0.3)
    
    # K-comp vs WD
    ax = axes[2]
    for cell in joint_cells.values():
        kcomp = cell["final_kcomp"]["mean"]
        wd = cell["weight_decay"]
        ax.scatter(wd, kcomp, s=100, alpha=0.7, edgecolors='black')
    ax.set_xlabel("Weight Decay")
    ax.set_ylabel("Max K-comp")
    ax.set_title("Joint: K-composition vs WD")
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close()
    logger.info(f"Saved joint dissociation plot to {save_path}")


def main():
    parser = argparse.ArgumentParser(description="Generate phase diagram figures")
    parser.add_argument("--manifest", type=Path, default=Path("results/phase_diagram.pt"))
    parser.add_argument("--output-dir", type=Path, default=Path("figures"))
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )

    args.output_dir.mkdir(exist_ok=True)

    cells = load_manifest(args.manifest)
    logger.info(f"Loaded {len(cells)} cells from manifest")

    # Generate all figures
    plot_phase_diagram_heatmap(cells, args.output_dir / "phase_diagram_heatmap.png")
    plot_phase_boundary_analysis(cells, args.output_dir / "phase_boundary_analysis.png")
    plot_model_size_sweep(cells, args.output_dir / "model_size_sweep.png")
    plot_joint_dissociation(cells, args.output_dir / "joint_dissociation.png")

    logger.info("All figures generated successfully")


if __name__ == "__main__":
    main()