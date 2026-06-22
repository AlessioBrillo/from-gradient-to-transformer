#!/usr/bin/env python3
"""Rung 5 — Sparse autoencoder feature dashboard.

Trains an SAE on activations from a small transformer's residual stream.
Evaluates feature interpretability via sparsity/reconstruction tradeoff,
dead feature analysis, and builds a browsable feature dashboard.

Usage:
    python -m src.experiments.exp5_sae_dashboard --seed 42

Output:
    - figures/exp5_sparsity_tradeoff.png
    - figures/exp5_feature_histogram.png
    - Console: SAE metrics (L0, loss recovered, dead feature rate)
    - (optional) Interactive feature dashboard via sae-vis
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
# Toy activation generator (simulates transformer residual stream)
# ---------------------------------------------------------------------------
class ActivationGenerator:
    """Generates synthetic residual stream activations with known feature structure.

    Simulates the output of a transformer's residual stream by mixing a sparse
    set of ground-truth features with noise. The SAE should recover these
    features.
    """

    def __init__(
        self,
        d_model: int,
        n_true_features: int,
        sparsity: float = 0.05,
        seed: int = 42,
    ) -> None:
        rng = np.random.default_rng(seed)
        self.d_model = d_model
        self.n_true_features = n_true_features

        # Generate ground-truth feature directions (approximately orthogonal)
        W = rng.standard_normal((n_true_features, d_model))
        self.feature_directions = torch.tensor(
            W / (np.linalg.norm(W, axis=1, keepdims=True) + 1e-8),
            dtype=torch.float32,
        )

        # Feature activation distribution
        self.sparsity = sparsity
        self.rng = rng

    def generate(self, n_samples: int) -> torch.Tensor:
        """Generate n_samples of residual stream activations.

        Returns:
            Tensor of shape (n_samples, d_model).
        """
        # Sparse feature activations
        mask = self.rng.binomial(1, self.sparsity, size=(n_samples, self.n_true_features))
        magnitudes = self.rng.exponential(scale=1.0, size=(n_samples, self.n_true_features))
        features = torch.tensor(mask * magnitudes, dtype=torch.float32)

        # Mix features into activations
        activations = features @ self.feature_directions

        # Add small noise
        noise = torch.randn_like(activations) * 0.1
        return activations + noise, features


# ---------------------------------------------------------------------------
# Sparse Autoencoder
# ---------------------------------------------------------------------------
class SparseAutoencoder(nn.Module):
    """Standard ReLU sparse autoencoder.

    Encodes d_model-dimensional activations into n_features-dimensional
    sparse latent space, then decodes back to d_model.
    """

    def __init__(
        self,
        d_model: int,
        n_features: int,
    ) -> None:
        super().__init__()
        self.d_model = d_model
        self.n_features = n_features

        # Encoder with bias
        self.encoder = nn.Linear(d_model, n_features, bias=True)
        # Decoder (no bias, weight tied conceptually)
        self.decoder = nn.Linear(n_features, d_model, bias=False)

        # Initialize decoder weights to unit norm (SAE convention)
        self._init_weights()

    def _init_weights(self) -> None:
        nn.init.kaiming_uniform_(self.encoder.weight, a=np.sqrt(5))
        nn.init.zeros_(self.encoder.bias)
        nn.init.kaiming_uniform_(self.decoder.weight, a=np.sqrt(5))
        self._normalize_decoder()

    def _normalize_decoder(self) -> None:
        """Normalize decoder weight columns to unit norm."""
        with torch.no_grad():
            self.decoder.weight.data = nn.functional.normalize(
                self.decoder.weight.data, dim=0
            )

    def forward(
        self, x: torch.Tensor
    ) -> tuple[torch.Tensor, torch.Tensor]:
        """Forward pass.

        Args:
            x: (batch, d_model) activations.

        Returns:
            Tuple of (reconstruction, latent_features).
        """
        latent = torch.relu(self.encoder(x))
        recon = self.decoder(latent)
        return recon, latent

    @torch.no_grad()
    def get_feature_activations(
        self, x: torch.Tensor
    ) -> torch.Tensor:
        """Get sparse feature activations without reconstruction."""
        return torch.relu(self.encoder(x))


# ---------------------------------------------------------------------------
# Training
# ---------------------------------------------------------------------------
def train_sae(
    model: SparseAutoencoder,
    loader: DataLoader,
    epochs: int,
    lr: float,
    l1_coeff: float,
    seed: int,
) -> dict:
    """Train the SAE with reconstruction + L1 sparsity loss.

    Loss = MSE(reconstruction, input) + l1_coeff * L1(latent)
    """
    set_seed(seed)
    model = model.to(DEVICE)
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    mse_loss = nn.MSELoss()

    history = {"loss": [], "mse": [], "l1": [], "l0": []}

    for epoch in tqdm(range(epochs), desc="Training SAE"):
        epoch_loss = 0.0
        epoch_mse = 0.0
        epoch_l1 = 0.0
        epoch_l0 = 0.0
        n_batches = 0

        for x, _ in loader:
            x = x.to(DEVICE)
            recon, latent = model(x)
            l2 = mse_loss(recon, x)
            l1 = latent.abs().sum(dim=-1).mean()
            loss = l2 + l1_coeff * l1

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            # Normalize decoder columns after each step
            model._normalize_decoder()

            epoch_loss += loss.item()
            epoch_mse += l2.item()
            epoch_l1 += l1.item()
            epoch_l0 += (latent > 1e-6).float().sum(dim=-1).mean().item()
            n_batches += 1

        history["loss"].append(epoch_loss / n_batches)
        history["mse"].append(epoch_mse / n_batches)
        history["l1"].append(epoch_l1 / n_batches)
        history["l0"].append(epoch_l0 / n_batches)

        if (epoch + 1) % 100 == 0:
            logger.info(
                f"Epoch {epoch+1:4d} | loss: {history['loss'][-1]:.4f} | "
                f"MSE: {history['mse'][-1]:.4f} | L1: {history['l1'][-1]:.4f} | "
                f"L0: {history['l0'][-1]:.2f}"
            )

    return history


# ---------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------
def analyze_features(
    model: SparseAutoencoder,
    dataset: TensorDataset,
    feature_activations: torch.Tensor | None = None,
) -> dict:
    """Analyze SAE feature quality.

    Metrics:
    - Dead features: features that activate on < 1/(10 * n_samples) of inputs
    - Feature sparsity (L0): average number of active features per input
    - Loss recovered: fraction of MSE explained by SAE
    """
    model.eval()

    if feature_activations is None:
        loader = DataLoader(dataset, batch_size=256, shuffle=False)
        all_latent = []
        with torch.no_grad():
            for x, _ in loader:
                x = x.to(DEVICE)
                latent = model.get_feature_activations(x)
                all_latent.append(latent.cpu())
        feature_activations = torch.cat(all_latent, dim=0)

    n_samples = feature_activations.size(0)

    # Feature frequency: how often each feature is active
    active_counts = (feature_activations > 1e-6).float().sum(dim=0)
    feature_freq = active_counts / n_samples

    # Dead features: activate on fewer than 1/(10*n_features) of inputs
    dead_threshold = 1.0 / (10 * model.n_features)
    dead_features = (feature_freq < dead_threshold).sum().item()
    total_features = model.n_features
    dead_rate = dead_features / total_features

    # L0 sparsity
    l0 = (feature_activations > 1e-6).float().sum(dim=-1).mean().item()

    # Feature magnitude distribution
    mean_activation = feature_activations.mean(dim=0)
    max_activation = feature_activations.max(dim=0).values
    median_activation = feature_activations.median(dim=0).values

    return {
        "dead_features": dead_features,
        "total_features": total_features,
        "dead_rate": dead_rate,
        "l0_sparsity": l0,
        "feature_frequency": feature_freq.numpy(),
        "mean_activation": mean_activation.numpy(),
        "max_activation": max_activation.numpy(),
        "median_activation": median_activation.numpy(),
    }


def evaluate_reconstruction(
    model: SparseAutoencoder,
    loader: DataLoader,
) -> dict:
    """Evaluate reconstruction quality.

    Metrics:
    - MSE: mean squared error between original and reconstructed
    - Fraction of variance explained (FVE)
    """
    model.eval()
    total_mse = 0.0
    total_var = 0.0
    n_samples = 0

    with torch.no_grad():
        for x, _ in loader:
            x = x.to(DEVICE)
            recon, _ = model(x)
            total_mse += ((x - recon) ** 2).sum().item()
            total_var += ((x - x.mean(dim=0, keepdim=True)) ** 2).sum().item()
            n_samples += x.size(0)

    mse = total_mse / (n_samples * model.d_model)
    fve = 1.0 - total_mse / (total_var + 1e-8)

    return {"mse": mse, "fve": float(fve)}


# ---------------------------------------------------------------------------
# Plotting
# ---------------------------------------------------------------------------
def plot_sparsity_tradeoff(
    feature_freq: np.ndarray,
    save_path: Path,
) -> None:
    """Plot feature frequency distribution.

    Good SAEs have a "heavy tail" distribution: a few features are very active,
    most are rarely active.
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Histogram of feature frequencies
    ax = axes[0]
    ax.hist(feature_freq, bins=50, alpha=0.7, color="steelblue", edgecolor="white")
    ax.set_xlabel("Feature Activation Frequency")
    ax.set_ylabel("Number of Features")
    ax.set_title("Feature Frequency Distribution", fontsize=14)
    ax.set_yscale("log")
    ax.grid(True, alpha=0.3)

    # Sorted feature frequencies (rank-frequency plot)
    ax = axes[1]
    sorted_freq = np.sort(feature_freq)[::-1]
    ax.plot(sorted_freq, linewidth=1.5, color="steelblue")
    ax.set_xlabel("Feature Rank")
    ax.set_ylabel("Activation Frequency")
    ax.set_title("Feature Rank-Frequency (Zipf plot)", fontsize=14)
    ax.set_yscale("log")
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    fig.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    logger.info(f"Saved sparsity tradeoff to {save_path}")


def plot_feature_histogram(
    feature_analysis: dict,
    save_path: Path,
) -> None:
    """Plot mean and max activation per feature."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Mean activation
    ax = axes[0]
    ax.hist(
        feature_analysis["mean_activation"],
        bins=50,
        alpha=0.7,
        color="crimson",
        edgecolor="white",
    )
    ax.set_xlabel("Mean Feature Activation")
    ax.set_ylabel("Number of Features")
    ax.set_title("Mean Activation Distribution", fontsize=14)
    ax.set_yscale("log")
    ax.grid(True, alpha=0.3)

    # Max activation
    ax = axes[1]
    ax.hist(
        feature_analysis["max_activation"],
        bins=50,
        alpha=0.7,
        color="darkgreen",
        edgecolor="white",
    )
    ax.set_xlabel("Max Feature Activation")
    ax.set_ylabel("Number of Features")
    ax.set_title("Max Activation Distribution", fontsize=14)
    ax.set_yscale("log")
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    fig.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    logger.info(f"Saved feature histogram to {save_path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(
        description="Rung 5: Sparse autoencoder feature dashboard"
    )
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument(
        "--d-model", type=int, default=64, help="Activation dimension"
    )
    parser.add_argument(
        "--n-features",
        type=int,
        default=512,
        help="SAE dictionary size (4-8x d_model recommended)",
    )
    parser.add_argument(
        "--n-true-features",
        type=int,
        default=20,
        help="Number of ground-truth features in synthetic data",
    )
    parser.add_argument(
        "--feature-sparsity",
        type=float,
        default=0.05,
        help="True feature sparsity (lower = sparser)",
    )
    parser.add_argument(
        "--epochs", type=int, default=1000, help="SAE training epochs"
    )
    parser.add_argument(
        "--lr", type=float, default=1e-3, help="Learning rate"
    )
    parser.add_argument(
        "--l1-coeff",
        type=float,
        default=1e-3,
        help="L1 sparsity coefficient",
    )
    parser.add_argument(
        "--num-samples",
        type=int,
        default=50000,
        help="Number of activation samples",
    )
    parser.add_argument(
        "--batch-size", type=int, default=256, help="Batch size"
    )
    parser.add_argument(
        "--quick", action="store_true", help="Quick test with fewer samples and epochs"
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )

    if args.quick:
        args.num_samples = 5000
        args.epochs = 200
        logger.info("QUICK MODE: samples=5000, epochs=200")

    logger.info(f"Device: {DEVICE}")
    logger.info(f"Arguments: {vars(args)}")

    set_seed(args.seed)

    # Generate synthetic activations with hidden features
    generator = ActivationGenerator(
        d_model=args.d_model,
        n_true_features=args.n_true_features,
        sparsity=args.feature_sparsity,
        seed=args.seed,
    )
    activations, true_features = generator.generate(args.num_samples)

    dataset = TensorDataset(activations, true_features)
    loader = DataLoader(dataset, batch_size=args.batch_size, shuffle=True)
    logger.info(
        f"Generated {args.num_samples} activation samples with "
        f"{args.n_true_features} ground-truth features "
        f"(sparsity={args.feature_sparsity})"
    )

    # Train SAE
    sae = SparseAutoencoder(
        d_model=args.d_model,
        n_features=args.n_features,
    )
    n_params = sum(p.numel() for p in sae.parameters())
    mult = f"{args.n_features / args.d_model:.1f}x"
    logger.info(f"SAE parameters: {n_params:,} (dict multiplier: {mult})")

    train_sae(
        model=sae,
        loader=loader,
        epochs=args.epochs,
        lr=args.lr,
        l1_coeff=args.l1_coeff,
        seed=args.seed,
    )

    # Evaluate
    reconstruction = evaluate_reconstruction(sae, loader)
    feature_analysis = analyze_features(sae, dataset)

    logger.info("=" * 60)
    logger.info("SAE Evaluation")
    logger.info("=" * 60)
    logger.info(f"Reconstruction MSE: {reconstruction['mse']:.6f}")
    logger.info(f"Fraction of variance explained: {reconstruction['fve']:.4f}")
    logger.info(f"L0 sparsity: {feature_analysis['l0_sparsity']:.2f} / {args.n_features}")
    logger.info(
        f"Dead features: {feature_analysis['dead_features']} / "
        f"{feature_analysis['total_features']} "
        f"({feature_analysis['dead_rate']:.1%})"
    )

    # Plot
    plot_sparsity_tradeoff(
        feature_analysis["feature_frequency"],
        save_path=FIGURES_DIR / "exp5_sparsity_tradeoff.png",
    )
    plot_feature_histogram(
        feature_analysis,
        save_path=FIGURES_DIR / "exp5_feature_histogram.png",
    )

    # Interpret results
    if feature_analysis["dead_rate"] > 0.5:
        logger.warning(
            f"High dead feature rate ({feature_analysis['dead_rate']:.1%}). "
            "Try: lower l1_coeff, larger batch size, or BatchTopK variant."
        )
    elif reconstruction["fve"] > 0.9:
        logger.info("✓ SAE captures >90% of activation variance.")
    else:
        logger.info(
            f"SAE captures {reconstruction['fve']:.1%} of variance. "
            "Try increasing n_features or training longer."
        )

    if feature_analysis["l0_sparsity"] < args.n_features * 0.1:
        logger.info("✓ SAE achieves good sparsity (L0 < 10% of dict size).")

    logger.info("")
    logger.info("Next steps for a production-quality feature dashboard:")
    logger.info("  1. Use SAELens for integrated training + visualization")
    logger.info("  2. Train on real transformer activations (not synthetic)")
    logger.info("  3. Generate top-activating examples per feature")
    logger.info("  4. Deploy interactive dashboard via sae-vis + HF Spaces")


if __name__ == "__main__":
    main()
