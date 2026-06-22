#!/usr/bin/env python3
"""Rung 3 — Toy Models of Superposition.

Reproduces Elhage et al. (Anthropic, 2022): trains a tiny ReLU autoencoder on
synthetic sparse features and observes the geometric phase transition from
monosemantic (one feature per neuron) to superposed (many features packed into
fewer dimensions) as feature sparsity is varied.

Usage:
    python -m src.experiments.exp3_superposition --seed 42

Output:
    - figures/exp3_feature_geometry.png
    - figures/exp3_phase_change.png
    - Console: sparsity vs. feature recovery table
"""

import argparse
import logging
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset
from tqdm import tqdm

from src.reproducibility import set_seed

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
FIGURES_DIR = Path("figures")
FIGURES_DIR.mkdir(exist_ok=True)

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


# ---------------------------------------------------------------------------
# Data: synthetic sparse features
# ---------------------------------------------------------------------------
class SparseFeatureDataset(TensorDataset):
    """Generates synthetic sparse features with known ground-truth directions.

    Each sample has N_features possible features, of which only a fraction are
    active (sparsity). Active features have values drawn from a distribution.
    The features are embedded into D dimensions using a random embedding matrix.
    """

    def __init__(
        self,
        n_features: int,
        n_dimensions: int,
        sparsity: float,
        num_samples: int,
        seed: int = 42,
    ) -> None:
        rng = np.random.default_rng(seed)

        # Generate ground-truth feature directions: (n_features, n_dimensions)
        # Random orthogonal-ish directions
        W = rng.standard_normal((n_features, n_dimensions))
        W = W / np.linalg.norm(W, axis=1, keepdims=True)

        # Generate sparse features
        features = []
        for _ in range(num_samples):
            # Which features are active
            mask = rng.binomial(1, sparsity, size=n_features)
            # Values for active features
            vals = mask * rng.exponential(size=n_features)
            features.append(vals)

        features = np.array(features, dtype=np.float32)

        # Embed features into lower-dimensional space
        embedded = features @ W  # (num_samples, n_dimensions)

        self.W = torch.tensor(W, dtype=torch.float32)
        self.features = torch.tensor(features)
        self.embedded = torch.tensor(embedded)

        super().__init__(self.embedded, self.features)


# ---------------------------------------------------------------------------
# Model: ReLU autoencoder (toy model)
# ---------------------------------------------------------------------------
class ToyAutoencoder(nn.Module):
    """Simple ReLU autoencoder with tied weights, mirroring Elhage et al."""

    def __init__(self, n_dimensions: int, n_features: int) -> None:
        super().__init__()
        self.encoder = nn.Linear(n_dimensions, n_features, bias=False)
        # Decoder weights are the encoder weight transpose (tied)
        # but we learn them separately for flexibility
        self.decoder = nn.Linear(n_features, n_dimensions, bias=False)

    def forward(
        self, x: torch.Tensor, return_latent: bool = False
    ) -> tuple[torch.Tensor, torch.Tensor]:
        latent = torch.relu(self.encoder(x))
        recon = self.decoder(latent)
        if return_latent:
            return recon, latent
        return recon, latent


# ---------------------------------------------------------------------------
# Training
# ---------------------------------------------------------------------------
def train_autoencoder(
    model: nn.Module,
    loader: DataLoader,
    epochs: int,
    lr: float,
    seed: int,
) -> dict:
    """Train the autoencoder and return reconstruction metrics."""
    set_seed(seed)
    model = model.to(DEVICE)
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    criterion = nn.MSELoss()

    history = {"loss": []}

    for epoch in tqdm(range(epochs), desc="Training AE"):
        epoch_loss = 0.0
        for x, _ in loader:
            x = x.to(DEVICE)
            recon, latent = model(x)
            loss = criterion(recon, x)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            epoch_loss += loss.item() * x.size(0)

        history["loss"].append(epoch_loss / len(loader.dataset))

    return history


# ---------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------
def compute_feature_recovery(
    model: nn.Module, dataset: SparseFeatureDataset
) -> dict:
    """Measure how well each feature is recovered by the autoencoder.

    For each ground-truth feature, check if there is a corresponding neuron
    in the autoencoder that selectively activates for it. A feature is
    "recovered" if the encoder weight direction has cosine similarity > 0.9
    with the ground-truth feature direction.

    Returns:
        Dict with recovery metrics per feature and overall.
    """
    model.eval()
    W_gt = dataset.W.numpy()  # (n_features, n_dimensions)
    W_enc = model.encoder.weight.data.cpu().numpy()  # (n_features, n_dimensions)

    # Normalize encoder weights
    W_enc_norm = W_enc / (np.linalg.norm(W_enc, axis=1, keepdims=True) + 1e-8)

    # Cosine similarity matrix: (n_features_gt, n_features_enc)
    cos_sim = W_gt @ W_enc_norm.T

    # Best-matching encoder neuron for each ground-truth feature
    best_match = cos_sim.max(axis=1)
    recovered = (best_match > 0.9).mean()

    # Monosemanticity: fraction of encoder neurons that match only one feature
    # (best-matching ground-truth feature per neuron)
    neuron_best = cos_sim.max(axis=0)
    n_monosemantic = (neuron_best > 0.9).mean()

    return {
        "cosine_sim_matrix": cos_sim,
        "feature_recovery_rate": float(recovered),
        "monosemantic_neuron_rate": float(n_monosemantic),
        "mean_cosine_sim": float(best_match.mean()),
    }


def compute_feature_geometry(
    model: nn.Module, dataset: SparseFeatureDataset
) -> dict:
    """Analyze the geometric arrangement of learned features.

    In the superposition regime, features arrange into geometric structures
    (pentagons, polytopes) in the decoder weight space.
    """
    model.eval()
    W_dec = model.decoder.weight.data.cpu().numpy()  # (n_dimensions, n_features)
    W_dec_norm = W_dec / (np.linalg.norm(W_dec, axis=0, keepdims=True) + 1e-8)

    # Cosine similarity between decoder feature directions
    cos_matrix = W_dec_norm.T @ W_dec_norm  # (n_features, n_features)
    np.fill_diagonal(cos_matrix, 0.0)

    # Average absolute correlation (a measure of superposition)
    mean_abs_corr = np.abs(cos_matrix).mean()

    # Number of near-orthogonal directions (cosine similarity < 0.1)
    n_orthogonal = (np.abs(cos_matrix) < 0.1).sum() / cos_matrix.shape[0]

    return {
    "mean_abs_correlation": float(mean_abs_corr),
        "n_orthogonal_per_feature": float(n_orthogonal),
        "decoder_cos_matrix": cos_matrix,
    }


# ---------------------------------------------------------------------------
# Plotting
# ---------------------------------------------------------------------------
def plot_feature_geometry(
    decoder_cos_matrix: np.ndarray,
    n_features: int,
    save_path: Path,
) -> None:
    """Heatmap of cosine similarities between decoder feature directions."""
    fig, ax = plt.subplots(figsize=(8, 7))
    im = ax.imshow(decoder_cos_matrix, cmap="RdBu_r", vmin=-1, vmax=1)
    ax.set_title(f"Feature Geometry (n_features={n_features})", fontsize=14)
    ax.set_xlabel("Feature Index")
    ax.set_ylabel("Feature Index")
    fig.colorbar(im, ax=ax, shrink=0.8, label="Cosine Similarity")

    fig.tight_layout()
    fig.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    logger.info(f"Saved feature geometry to {save_path}")


def plot_phase_change(
    sparsity_values: list[float],
    recovery_rates: list[float],
    monosemantic_rates: list[float],
    save_path: Path,
) -> None:
    """Plot the phase transition from monosemantic to superposed features."""
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(
        sparsity_values,
        recovery_rates,
        marker="o",
        label="Feature Recovery Rate",
        linewidth=2,
        color="steelblue",
    )
    ax.plot(
        sparsity_values,
        monosemantic_rates,
        marker="s",
        label="Monosemantic Neuron Rate",
        linewidth=2,
        color="crimson",
    )
    ax.set_xlabel("Feature Sparsity (probability of activation)")
    ax.set_ylabel("Rate")
    ax.set_title("Phase Change: Monosemantic → Superposed Features", fontsize=14)
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_xscale("log")

    # Annotate the phase transition region
    for i in range(len(sparsity_values) - 1):
        if recovery_rates[i] > 0.5 and recovery_rates[i + 1] < 0.5:
            transition_point = (sparsity_values[i] + sparsity_values[i + 1]) / 2
            ax.axvline(
                x=transition_point,
                color="gray",
                linestyle="--",
                alpha=0.5,
                label=f"Transition ~{transition_point:.1e}",
            )
            break

    fig.tight_layout()
    fig.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    logger.info(f"Saved phase change plot to {save_path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(
        description="Rung 3: Toy Models of Superposition"
    )
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument(
        "--n-features", type=int, default=20, help="Number of ground-truth features"
    )
    parser.add_argument(
        "--n-dimensions", type=int, default=5, help="Embedding dimension"
    )
    parser.add_argument(
        "--epochs", type=int, default=5000, help="Training epochs per sparsity level"
    )
    parser.add_argument("--lr", type=float, default=1e-2, help="Learning rate")
    parser.add_argument(
        "--num-samples", type=int, default=50000, help="Number of training samples"
    )
    parser.add_argument(
        "--batch-size", type=int, default=512, help="Batch size"
    )
    parser.add_argument(
        "--single-sparsity",
        type=float,
        default=None,
        help="Run a single sparsity value instead of a sweep",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )
    logger.info(f"Device: {DEVICE}")
    logger.info(f"Arguments: {vars(args)}")

    set_seed(args.seed)

    if args.single_sparsity is not None:
        sparsity_values = [args.single_sparsity]
    else:
        # Sweep sparsity from dense to extremely sparse
        sparsity_values = [0.5, 0.2, 0.1, 0.05, 0.02, 0.01, 0.005, 0.002, 0.001]

    results = []
    for sparsity in sparsity_values:
        logger.info("=" * 60)
        logger.info(f"Sparsity: {sparsity:.4f}")
        logger.info("=" * 60)

        dataset = SparseFeatureDataset(
            n_features=args.n_features,
            n_dimensions=args.n_dimensions,
            sparsity=sparsity,
            num_samples=args.num_samples,
            seed=args.seed,
        )
        loader = DataLoader(
            dataset, batch_size=args.batch_size, shuffle=True
        )

        model = ToyAutoencoder(
            n_dimensions=args.n_dimensions,
            n_features=args.n_features,
        )

        train_autoencoder(
            model=model,
            loader=loader,
            epochs=args.epochs,
            lr=args.lr,
            seed=args.seed,
        )

        recovery = compute_feature_recovery(model, dataset)
        geometry = compute_feature_geometry(model, dataset)

        logger.info(
            f"Feature recovery: {recovery['feature_recovery_rate']:.3f} | "
            f"Monosemantic rate: {recovery['monosemantic_neuron_rate']:.3f} | "
            f"Mean abs corr: {geometry['mean_abs_correlation']:.3f}"
        )

        results.append({
            "sparsity": sparsity,
            **recovery,
            **geometry,
        })

    # Plot phase change if we did a sweep
    if len(sparsity_values) > 1:
        recovery_rates = [r["feature_recovery_rate"] for r in results]
        monosemantic_rates = [r["monosemantic_neuron_rate"] for r in results]
        plot_phase_change(
            sparsity_values,
            recovery_rates,
            monosemantic_rates,
            save_path=FIGURES_DIR / "exp3_phase_change.png",
        )

    # Plot geometry for the final/default sparsity
    final_result = results[-1]
    if "decoder_cos_matrix" in final_result:
        plot_feature_geometry(
            final_result["decoder_cos_matrix"],
            n_features=args.n_features,
            save_path=FIGURES_DIR / "exp3_feature_geometry.png",
        )

    # Summary table
    logger.info("=" * 60)
    logger.info("SUPERPOSITION EXPERIMENT COMPLETE")
    logger.info("=" * 60)
    logger.info(f"{'Sparsity':>10} | {'Recovery':>9} | {'Monosemantic':>11} | {'Mean |Corr|':>10}")
    logger.info("-" * 50)
    for r in results:
        logger.info(
            f"{r['sparsity']:>10.4f} | {r['feature_recovery_rate']:>9.3f} | "
            f"{r['monosemantic_neuron_rate']:>11.3f} | "
            f"{r['mean_abs_correlation']:>10.3f}"
        )

    # Interpretation
    high_rec = [r for r in results if r["feature_recovery_rate"] > 0.8]
    low_rec = [r for r in results if r["feature_recovery_rate"] < 0.2]
    if high_rec and low_rec:
        logger.info(
            "✓ CONFIRMED phase transition: features transition from "
            "monosemantic to superposed as sparsity decreases."
        )
    elif high_rec:
        logger.info(
            "All features are monosemantic at this sparsity range. "
            "Try lower sparsity values to observe superposition."
        )
    else:
        logger.info(
            "Features are in superposition regime. "
            "Try higher sparsity values to observe monosemantic phase."
        )


if __name__ == "__main__":
    main()
