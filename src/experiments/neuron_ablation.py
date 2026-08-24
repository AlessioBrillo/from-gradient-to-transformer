#!/usr/bin/env python3
"""Neuron Ablation on Dense Grokking Checkpoints (R3).

Loads existing P=113 checkpoints and ablates MLP neurons by activation magnitude.
Compares degradation curve to Fourier ablation curve.
"""

import argparse
import logging
from pathlib import Path
from typing import List, Tuple

import matplotlib.pyplot as plt
import torch
from torch.utils.data import DataLoader

from src.experiments.exp2_grokking import (
    DEVICE,
    FIGURES_DIR,
    OneLayerTransformer,
    analyze_fourier_sparsity,
    fourier_decompose_embeddings,
    make_modular_addition_data,
)
from src.reproducibility import set_seed

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%H:%M:%S",
)

# Constants from the standard P=113 config
DEFAULT_D_MODEL = 128
DEFAULT_D_MLP = 512
DEFAULT_N_HEADS = 4
DEFAULT_MODULUS = 113
DEFAULT_BATCH_SIZE = 512


def load_checkpoint(
    checkpoint_path: Path, d_model: int, d_mlp: int, n_heads: int, modulus: int
) -> Tuple[OneLayerTransformer, dict]:
    """Load model from checkpoint."""
    model = OneLayerTransformer(
        d_model=d_model,
        d_mlp=d_mlp,
        n_heads=n_heads,
        modulus=modulus,
    )
    checkpoint = torch.load(checkpoint_path, map_location=DEVICE)
    model.load_state_dict(checkpoint["model"])
    model.eval()
    return model, checkpoint


def compute_neuron_importance(
    model: OneLayerTransformer, val_loader: DataLoader, num_samples: int = 1000
) -> torch.Tensor:
    """Compute importance of each MLP neuron by average activation magnitude using forward hooks."""
    model.eval()

    # Hook to capture MLP post-ReLU activations
    mlp_activations = []

    def hook_fn(module, input, output):
        # output is (B, 2, d_mlp) after W_in and ReLU
        mlp_activations.append(output.detach().cpu())

    # Register hook on the ReLU output (which is the input to W_out)
    # The MLP is: W_out(ReLU(W_in(h_ln)))
    # The ReLU is inside W_out? Let's check: self.W_out(torch.relu(self.W_in(h_ln)))
    # So we hook on the linear layer W_in's output after ReLU
    # Actually, we can hook on the module that computes the MLP
    handle = model.W_in.register_forward_hook(
        lambda m, i, o: mlp_activations.append(torch.relu(o).detach().cpu())
    )

    total = 0
    with torch.no_grad():
        for x, _ in val_loader:
            if total >= num_samples:
                break
            _ = model(x.to(DEVICE))
            total += x.size(0)

    handle.remove()

    if not mlp_activations:
        return torch.zeros(model.d_mlp)

    all_acts = torch.cat(mlp_activations, dim=0)[:num_samples]  # (samples, 2, d_mlp)
    # Average over batch and sequence positions -> (d_mlp,)
    importance = all_acts.abs().mean(dim=(0, 1))
    return importance


def ablate_neurons(model: OneLayerTransformer, neuron_indices: List[int]) -> OneLayerTransformer:
    """Create a copy of model with specified neurons zeroed out in MLP."""
    import copy
    ablated_model = copy.deepcopy(model)

    with torch.no_grad():
        # Zero out the output weights for these neurons (W_out[:, neuron_idx] = 0)
        ablated_model.W_out.weight[:, neuron_indices] = 0
        # Also zero the bias if it exists
        if ablated_model.W_out.bias is not None:
            ablated_model.W_out.bias[neuron_indices] = 0

    return ablated_model


def evaluate_model(model: OneLayerTransformer, val_loader: DataLoader) -> float:
    """Evaluate model accuracy on validation set."""
    model.eval()
    correct = 0
    total = 0

    with torch.no_grad():
        for x, y in val_loader:
            x, y = x.to(DEVICE), y.to(DEVICE)
            logits, _ = model(x)
            preds = logits.argmax(dim=-1)
            correct += (preds == y).sum().item()
            total += y.size(0)

    return correct / total


def run_neuron_ablation_sweep(
    model: OneLayerTransformer,
    val_loader: DataLoader,
    num_steps: int = 20,
) -> Tuple[List[int], List[float]]:
    """Run neuron ablation sweep from 0 to all neurons."""
    logger.info("Computing neuron importance...")
    importance = compute_neuron_importance(model, val_loader)

    # Sort neurons by importance (descending)
    sorted_indices = importance.argsort(descending=True).tolist()

    logger.info("Running ablation sweep...")
    accuracies = []

    # Baseline (no ablation)
    base_acc = evaluate_model(model, val_loader)
    accuracies.append(base_acc)
    logger.info(f"Baseline accuracy: {base_acc:.4f}")

    # Ablate progressively more neurons
    for i in range(1, num_steps + 1):
        k = int(len(sorted_indices) * i / num_steps)
        neurons_to_ablate = sorted_indices[:k]

        ablated = ablate_neurons(model, neurons_to_ablate)
        acc = evaluate_model(ablated, val_loader)
        accuracies.append(acc)

        if i % 5 == 0:
            logger.info(f"Ablated {k}/{len(sorted_indices)} neurons: accuracy = {acc:.4f}")

    # Return evenly spaced steps from 0 to num_components
    steps = [int(len(sorted_indices) * i / num_steps) for i in range(num_steps + 1)]
    return steps, accuracies


def run_fourier_ablation_for_comparison(
    model: OneLayerTransformer,
    val_loader: DataLoader,
    modulus: int,
    d_mlp: int,
    num_steps: int = 20,
) -> Tuple[List[int], List[float]]:
    """Run Fourier frequency ablation for comparison."""
    logger.info("Running Fourier ablation for comparison...")

    embed = model.embed.weight.data.detach().cpu()
    fourier_result = fourier_decompose_embeddings(embed, modulus)
    sparsity = analyze_fourier_sparsity(fourier_result, top_k=modulus)
    freq_order = sparsity["top_frequencies"]  # Already a list

    accuracies = []
    base_acc = evaluate_model(model, val_loader)
    accuracies.append(base_acc)

    for i in range(1, num_steps + 1):
        k = int(len(freq_order) * i / num_steps)
        freqs_to_ablate = freq_order[:k]

        # Ablate by zeroing the corresponding embedding dimensions
        # (This is a simplified version - full implementation in exp2_grokking.py)
        ablated_model = type(model)(
            d_model=model.d_model,
            d_mlp=d_mlp,
            n_heads=model.n_heads,
            modulus=model.modulus,
        )
        ablated_model.load_state_dict(model.state_dict())

        with torch.no_grad():
            # Zero out the embedding rows for ablated frequencies
            for freq in freqs_to_ablate:
                if freq < modulus:
                    ablated_model.embed.weight[freq] = 0
                    ablated_model.unembed.weight[freq] = 0

        acc = evaluate_model(ablated_model, val_loader)
        accuracies.append(acc)

        if i % 5 == 0:
            logger.info(f"Ablated {k}/{len(freq_order)} frequencies: accuracy = {acc:.4f}")

    # Return evenly spaced steps from 0 to num_components
    steps = [int(len(freq_order) * i / num_steps) for i in range(num_steps + 1)]
    return steps, accuracies


def main():
    parser = argparse.ArgumentParser(description="Neuron ablation on dense grokking checkpoints")
    parser.add_argument("--seeds", type=str, default="0,1,2", help="Comma-separated seeds")
    parser.add_argument(
        "--checkpoint-epoch", type=int, default=5000, help="Checkpoint epoch to load"
    )
    parser.add_argument(
        "--checkpoint-dir", type=str, default="checkpoints", help="Checkpoint directory"
    )
    parser.add_argument(
        "--modulus", type=int, default=DEFAULT_MODULUS, help="Modulus P"
    )
    parser.add_argument(
        "--d-model", type=int, default=DEFAULT_D_MODEL, help="Model dimension"
    )
    parser.add_argument(
        "--d-mlp", type=int, default=DEFAULT_D_MLP, help="MLP hidden dimension"
    )
    parser.add_argument(
        "--n-heads", type=int, default=DEFAULT_N_HEADS, help="Attention heads"
    )
    parser.add_argument(
        "--num-steps", type=int, default=20, help="Number of ablation steps"
    )
    parser.add_argument(
        "--num-samples", type=int, default=1000, help="Samples for importance computation"
    )

    args = parser.parse_args()

    FIGURES_DIR.mkdir(exist_ok=True)

    seeds = [int(s.strip()) for s in args.seeds.split(",")]

    all_neuron_results = {}
    all_fourier_results = {}

    for seed in seeds:
        logger.info(f"\n{'='*60}")
        logger.info(f"Processing seed {seed}")
        logger.info(f"{'='*60}")

        ckpt_path = Path(args.checkpoint_dir) / f"exp2_checkpoint_seed{seed}.pt"
        if not ckpt_path.exists():
            logger.warning(f"Checkpoint not found: {ckpt_path}")
            continue

        # Load model and data
        model, checkpoint = load_checkpoint(
            ckpt_path, args.d_model, args.d_mlp, args.n_heads, args.modulus
        )
        logger.info(f"Loaded checkpoint from epoch {checkpoint.get('epoch', 'unknown')}")

        set_seed(seed)
        train_dataset, val_dataset = make_modular_addition_data(
            modulus=args.modulus,
            train_fraction=0.3,
            seed=seed,
        )
        val_loader = DataLoader(val_dataset, batch_size=DEFAULT_BATCH_SIZE, shuffle=False)

        # Run neuron ablation
        neuron_steps, neuron_accs = run_neuron_ablation_sweep(model, val_loader, args.num_steps)
        all_neuron_results[seed] = (neuron_steps, neuron_accs)

        # Run Fourier ablation for comparison
        fourier_steps, fourier_accs = run_fourier_ablation_for_comparison(
            model, val_loader, args.modulus, args.d_mlp, args.num_steps
        )
        all_fourier_results[seed] = (fourier_steps, fourier_accs)

    # Plot comparison
    fig, axes = plt.subplots(1, len(seeds), figsize=(6 * len(seeds), 5), squeeze=False)

    for idx, seed in enumerate(seeds):
        if seed not in all_neuron_results:
            continue

        ax = axes[0, idx]
        neuron_steps, neuron_accs = all_neuron_results[seed]
        fourier_steps, fourier_accs = all_fourier_results[seed]

        ax.plot(
            neuron_steps,
            neuron_accs,
            "b-o",
            label="Neuron Ablation",
            linewidth=2,
            markersize=4,
        )
        ax.plot(
            fourier_steps,
            fourier_accs,
            "r-s",
            label="Fourier Ablation",
            linewidth=2,
            markersize=4,
        )

        ax.set_xlabel('Components Ablated')
        ax.set_ylabel('Validation Accuracy')
        ax.set_title(f'Seed {seed}: Neuron vs Fourier Ablation')
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.set_ylim([0, 1.05])

    plt.tight_layout()
    save_path = FIGURES_DIR / "exp2_neuron_ablation.png"
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()
    logger.info(f"Saved figure to {save_path}")

    # Save results for manifest
    import json

    neuron_dict = {
        str(s): {"steps": steps, "accuracies": accs}
        for s, (steps, accs) in all_neuron_results.items()
    }
    fourier_dict = {
        str(s): {"steps": steps, "accuracies": accs}
        for s, (steps, accs) in all_fourier_results.items()
    }
    results = {
        "neuron_ablation": neuron_dict,
        "fourier_ablation": fourier_dict,
    }
    results_path = FIGURES_DIR / "exp2_neuron_ablation_results.json"
    with open(results_path, 'w') as f:
        json.dump(results, f, indent=2)
    logger.info(f"Saved results to {results_path}")


if __name__ == "__main__":
    main()
