#!/usr/bin/env python3
"""
Neuron Ablation on Dense Grokking (ADR-0024 Row 3)

On existing P=113 checkpoints (seed 0,1,2), ablate MLP neurons by
activation magnitude; compare degradation to Fourier ablation curve.

Output: figures/exp2_neuron_ablation.png, manifest entry in exp2_grokking.json
"""

import argparse
import json
from pathlib import Path

import torch
import matplotlib.pyplot as plt

from src.models.decoder_only_transformer import DecoderOnlyTransformer
from src.experiments.exp2_grokking import (
    make_modular_addition_data,
    analyze_fourier_sparsity,
    fourier_ablation,
)


def load_checkpoint(ckpt_path: Path, model: DecoderOnlyTransformer) -> dict:
    """Load checkpoint and return state dict."""
    ckpt = torch.load(ckpt_path, map_location="cpu")
    model.load_state_dict(ckpt["model"])
    return ckpt


def get_mlp_neuron_activations(model: DecoderOnlyTransformer, data_loader, device: str = "cpu"):
    """Collect MLP neuron activations across the dataset."""
    model.eval()
    model.to(device)

    # Hook to capture MLP output activations
    activations = {}

    def hook_fn(module, input, output, layer_idx):
        if layer_idx not in activations:
            activations[layer_idx] = []
        activations[layer_idx].append(output.detach().cpu())

    handles = []
    for i, block in enumerate(model.blocks):
        handles.append(block.mlp.register_forward_hook(
            lambda m, inp, out, idx=i: hook_fn(m, inp, out, idx)
        ))

    with torch.no_grad():
        for batch in data_loader:
            x, y = batch
            x = x.to(device)
            _ = model(x)

    for h in handles:
        h.remove()

    # Concatenate activations
    for layer_idx in activations:
        activations[layer_idx] = torch.cat(activations[layer_idx], dim=0)

    return activations


def compute_neuron_importance(activations: dict) -> dict:
    """Compute importance score for each neuron (mean activation magnitude)."""
    importance = {}
    for layer_idx, acts in activations.items():
        # acts shape: [num_samples, seq_len, d_mlp]
        # Mean over samples and sequence positions
        importance[layer_idx] = acts.abs().mean(dim=(0, 1))  # [d_mlp]
    return importance


def ablate_neurons(model: DecoderOnlyTransformer, layer_idx: int, neuron_indices: list, device: str = "cpu"):
    """Zero out specific neurons in the MLP of a given layer."""
    model.eval()
    model.to(device)

    mlp = model.blocks[layer_idx].mlp
    with torch.no_grad():
        # Zero out output weights for specified neurons (W_out)
        mlp.W_out.weight[neuron_indices] = 0
        # Zero out input weights for specified neurons (W_in)
        mlp.W_in.weight[:, neuron_indices] = 0


def evaluate_model(model: DecoderOnlyTransformer, data_loader, device: str = "cpu") -> float:
    """Evaluate model accuracy on validation set."""
    model.eval()
    model.to(device)

    correct = 0
    total = 0
    with torch.no_grad():
        for x, y in data_loader:
            x, y = x.to(device), y.to(device)
            logits = model(x)
            preds = logits.argmax(dim=-1)
            correct += (preds == y).sum().item()
            total += y.numel()

    return correct / total


def run_neuron_ablation_sweep(
    checkpoint_path: Path,
    data_loader,
    max_neurons_to_ablate: int = 100,
    device: str = "cpu",
) -> dict:
    """Run neuron ablation sweep: ablate top-k neurons by importance."""
    # Load model
    model = DecoderOnlyTransformer(
        vocab_size=113,
        d_model=128,
        n_layers=2,
        n_heads=4,
        d_mlp=512,
    )

    ckpt = load_checkpoint(checkpoint_path, model)

    # Get baseline accuracy
    baseline_acc = evaluate_model(model, data_loader, device)
    print(f"Baseline accuracy: {baseline_acc:.4f}")

    # Get neuron importance
    activations = get_mlp_neuron_activations(model, data_loader, device)
    importance = compute_neuron_importance(activations)

    # For each layer, sort neurons by importance and ablate progressively
    results = {"baseline_acc": baseline_acc, "layers": {}}

    for layer_idx in importance:
        imp = importance[layer_idx]
        sorted_indices = torch.argsort(imp, descending=True).tolist()

        layer_results = {"neuron_importance": imp.tolist(), "ablation_curve": []}

        # Reload model for each ablation step
        for k in range(0, min(max_neurons_to_ablate, len(sorted_indices)) + 1, 5):
            if k == 0:
                acc = baseline_acc
            else:
                model = DecoderOnlyTransformer(
                    vocab_size=113, d_model=128, n_layers=2, n_heads=4, d_mlp=512
                )
                load_checkpoint(checkpoint_path, model)
                ablate_neurons(model, layer_idx, sorted_indices[:k], device)
                acc = evaluate_model(model, data_loader, device)

            layer_results["ablation_curve"].append({"k_ablated": k, "accuracy": acc})
            print(f"  Layer {layer_idx}, k={k}: acc={acc:.4f}")

        results["layers"][layer_idx] = layer_results

    return results


def run_fourier_ablation_curve(
    checkpoint_path: Path,
    data_loader,
    device: str = "cpu",
) -> list:
    """Run Fourier ablation curve for comparison."""
    model = DecoderOnlyTransformer(
        vocab_size=113, d_model=128, n_layers=2, n_heads=4, d_mlp=512
    )
    load_checkpoint(checkpoint_path, model)

    model.eval()
    model.to(device)

    # Get embeddings
    embeddings = model.embed.weight.data.cpu()

    # Fourier analysis
    fourier = analyze_fourier_sparsity(embeddings)
    freq_magnitudes = fourier["magnitudes"]  # [P]
    sorted_freqs = torch.argsort(freq_magnitudes, descending=True).tolist()

    # Ablate frequencies progressively
    curve = []
    for k in range(0, 113, 5):
        if k == 0:
            acc = evaluate_model(model, data_loader, device)
        else:
            model = DecoderOnlyTransformer(
                vocab_size=113, d_model=128, n_layers=2, n_heads=4, d_mlp=512
            )
            load_checkpoint(checkpoint_path, model)
            fourier_ablation(model, sorted_freqs[:k])
            acc = evaluate_model(model, data_loader, device)

        curve.append({"k_ablated": k, "accuracy": acc})
        print(f"  Fourier k={k}: acc={acc:.4f}")

    return curve


def plot_comparison(neuron_results: dict, fourier_curves: dict, output_path: Path):
    """Plot neuron ablation vs Fourier ablation curves."""
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Neuron ablation (per layer)
    ax = axes[0]
    for layer_idx, data in neuron_results["layers"].items():
        ks = [p["k_ablated"] for p in data["ablation_curve"]]
        accs = [p["accuracy"] for p in data["ablation_curve"]]
        ax.plot(ks, accs, label=f"Layer {layer_idx} neurons", marker="o", markersize=3)

    ax.axhline(y=neuron_results["baseline_acc"], color="black", linestyle="--", alpha=0.5, label="Baseline")
    ax.axhline(y=1/113, color="red", linestyle=":", alpha=0.5, label="Chance (1/113)")
    ax.set_xlabel("Neurons Ablated (top-k by importance)")
    ax.set_ylabel("Validation Accuracy")
    ax.set_title("Neuron Ablation on Dense Grokking")
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Fourier ablation
    ax = axes[1]
    for seed, curve in fourier_curves.items():
        ks = [p["k_ablated"] for p in curve]
        accs = [p["accuracy"] for p in curve]
        ax.plot(ks, accs, label=f"Seed {seed}", marker="o", markersize=3)

    ax.axhline(y=1/113, color="red", linestyle=":", alpha=0.5, label="Chance (1/113)")
    ax.set_xlabel("Frequencies Ablated (top-k by magnitude)")
    ax.set_ylabel("Validation Accuracy")
    ax.set_title("Fourier Ablation on Dense Grokking")
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()
    print(f"Saved plot to {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Neuron Ablation on Dense Grokking")
    parser.add_argument("--checkpoints-dir", type=Path, default=Path("checkpoints"),
                        help="Directory containing P=113 checkpoints")
    parser.add_argument("--output-dir", type=Path, default=Path("figures"),
                        help="Output directory for figures")
    parser.add_argument("--manifest-path", type=Path, default=Path("results/exp2_grokking.json"),
                        help="Path to manifest to update")
    parser.add_argument("--max-neurons", type=int, default=100,
                        help="Max neurons to ablate per layer")
    parser.add_argument("--device", default="cpu", help="Device to run on")
    parser.add_argument("--seeds", nargs="+", type=int, default=[0, 1, 2],
                        help="Seeds to process")
    args = parser.parse_args()

    # Create data loader (same as exp2_grokking)
    _, val_loader = make_modular_addition_data(
        P=113,
        train_frac=0.3,
        batch_size=512,
        seed=42,
    )

    all_neuron_results = {}
    all_fourier_curves = {}

    for seed in args.seeds:
        ckpt_path = args.checkpoints_dir / f"exp2_seed{seed}_epoch5000.pt"
        if not ckpt_path.exists():
            print(f"Checkpoint not found: {ckpt_path}")
            continue

        print(f"\n=== Seed {seed} ===")

        # Neuron ablation
        print("Running neuron ablation sweep...")
        neuron_results = run_neuron_ablation_sweep(
            ckpt_path, val_loader, max_neurons_to_ablate=args.max_neurons, device=args.device
        )
        all_neuron_results[seed] = neuron_results

        # Fourier ablation (for comparison)
        print("Running Fourier ablation sweep...")
        fourier_curve = run_fourier_ablation_curve(ckpt_path, val_loader, args.device)
        all_fourier_curves[seed] = fourier_curve

    # Plot
    output_path = args.output_dir / "exp2_neuron_ablation.png"
    plot_comparison(all_neuron_results, all_fourier_curves, output_path)

    # Update manifest
    if args.manifest_path.exists():
        with open(args.manifest_path) as f:
            manifest = json.load(f)
    else:
        manifest = {}

    if "neuron_ablation" not in manifest:
        manifest["neuron_ablation"] = {}

    manifest["neuron_ablation"]["results"] = all_neuron_results
    manifest["neuron_ablation"]["fourier_comparison"] = all_fourier_curves

    with open(args.manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)
    print(f"Updated manifest: {args.manifest_path}")


if __name__ == "__main__":
    main()