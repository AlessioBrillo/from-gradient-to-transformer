#!/usr/bin/env python3
"""Rung 3 — Toy Models of Superposition.

Reproduces Elhage et al. (Anthropic, 2022): trains a tiny linear-encode /
ReLU-decode autoencoder on synthetic sparse features and observes the
geometric phase transition from monosemantic (one feature per dimension) to
superposed (many features packed into fewer dimensions) as feature sparsity
is varied.

Rewritten 2026-08-02 (Micro-Phase 8, the Evidence Pass) after root-causing
why the 2026-07-26/2026-08-01 sweeps showed flat, near-zero "recovery" at
every sparsity level. The answer was architectural, not a parameter bug:
the previous `SparseFeatureDataset` pre-embedded the sparse features into
`n_dimensions` space with a random ground-truth matrix *before* the model
ever saw them, so `ToyAutoencoder` was expanding an already-compressed
vector back out — not compressing anything. MSE could (and did) reach
exactly 0.000000 regardless of sparsity, because there was no bottleneck to
create the interference superposition exists to resolve. See
05_llm_engineering/proofs/superposition-setup-validity.md for the full
reconstruction, including the side-by-side run that found this.

This version puts the sparse features directly in the standard basis of
R^n_features (no invented ground-truth directions to "recover") and forces
a real bottleneck: encode n_features -> n_dimensions (n_dimensions <
n_features), decode back with a learned bias. That bias is the second
missing ingredient — it is what lets the model suppress interference between
non-orthogonal feature directions by pushing near-zero activations below
the ReLU floor, which is *how* superposition pays for itself.

Usage:
    python -m src.experiments.exp3_superposition --seed 42

Output:
    - figures/exp3_feature_geometry.png
    - figures/exp3_phase_change.png
    - Console: sparsity vs. feature-representation table
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

from src.experiments.runner import parse_seeds, run_seeds
from src.reproducibility import set_seed
from src.results import ResultsManifest, count_parameters

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
FIGURES_DIR = Path("figures")

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


# ---------------------------------------------------------------------------
# Data: synthetic sparse features in the standard basis
# ---------------------------------------------------------------------------
class SparseFeatureDataset(TensorDataset):
    """Sparse feature vectors directly in R^n_features (Elhage et al. setup).

    Each of `n_features` ground-truth features is active independently with
    probability `sparsity`; an active feature's magnitude is drawn from
    Uniform(0, 1). There is no embedding step and no ground-truth direction
    matrix — the features themselves are the standard basis vectors of
    R^n_features, and it is the *model's* encoder that must learn a direction
    for each one under the R^n_dimensions bottleneck. `importance_decay`
    implements Elhage et al.'s per-feature importance weighting
    `I_i = decay^i`, used to weight the reconstruction loss so some features
    matter more than others (decay=1.0 recovers uniform importance).
    """

    def __init__(
        self,
        n_features: int,
        sparsity: float,
        num_samples: int,
        importance_decay: float = 1.0,
        seed: int = 42,
    ) -> None:
        rng = np.random.default_rng(seed)

        mask = rng.binomial(1, sparsity, size=(num_samples, n_features))
        magnitude = rng.uniform(0.0, 1.0, size=(num_samples, n_features))
        features = (mask * magnitude).astype(np.float32)

        importance = importance_decay ** np.arange(n_features)
        self.importance = torch.from_numpy(importance.astype(np.float32))
        self.features = torch.from_numpy(features)

        # Autoencoder: input and target are the same tensor.
        super().__init__(self.features, self.features)


# ---------------------------------------------------------------------------
# Model: linear-encode, ReLU-decode toy autoencoder (Elhage et al.)
# ---------------------------------------------------------------------------
class ToyAutoencoder(nn.Module):
    """Canonical Toy Models of Superposition architecture.

        h  = W x                (compress: n_features -> n_dimensions, linear)
        x' = ReLU(W^T h + b)     (decompress: n_dimensions -> n_features)

    `W` is a single tied parameter (`encoder.weight`, shape
    `(n_dimensions, n_features)`); the decoder reuses `W^T`, not a second
    independently-learned matrix. `n_dimensions < n_features` is enforced —
    without an actual bottleneck there is nothing for superposition to
    trade off against, which was exactly the defect in the pre-2026-08-02
    version (see module docstring).

    The decoder bias `b` is what makes packing non-orthogonal feature
    directions into a shared dimension worthwhile: it lets the model shift
    small cross-feature interference below zero so ReLU clips it, instead of
    that interference always corrupting the reconstruction.
    """

    def __init__(self, n_features: int, n_dimensions: int) -> None:
        super().__init__()
        if not n_dimensions < n_features:
            raise ValueError(
                f"n_dimensions ({n_dimensions}) must be < n_features ({n_features}) "
                "— without a real bottleneck there is nothing for superposition "
                "to trade off against."
            )
        self.n_features = n_features
        self.n_dimensions = n_dimensions
        self.encoder = nn.Linear(n_features, n_dimensions, bias=False)
        self.decoder_bias = nn.Parameter(torch.zeros(n_features))

    def forward(self, x: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        h = self.encoder(x)  # (B, n_dimensions)
        recon = torch.relu(
            nn.functional.linear(h, self.encoder.weight.t()) + self.decoder_bias
        )  # (B, n_features)
        return recon, h


# ---------------------------------------------------------------------------
# Training
# ---------------------------------------------------------------------------
def train_autoencoder(
    model: nn.Module,
    loader: DataLoader,
    importance: torch.Tensor,
    epochs: int,
    lr: float,
    seed: int,
) -> dict:
    """Train the autoencoder with importance-weighted reconstruction loss."""
    set_seed(seed)
    model = model.to(DEVICE)
    importance = importance.to(DEVICE)
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)

    history = {"loss": []}

    for _epoch in tqdm(range(epochs), desc="Training AE"):
        epoch_loss = 0.0
        for x, _ in loader:
            x = x.to(DEVICE)
            recon, _latent = model(x)
            loss = (importance * (recon - x) ** 2).mean()
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            epoch_loss += loss.item() * x.size(0)

        history["loss"].append(epoch_loss / len(loader.dataset))

    return history


# ---------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------
def compute_feature_geometry(model: nn.Module, threshold: float = 0.5) -> dict:
    """Analyze how the model's encoder represents each ground-truth feature.

    There is no external ground truth to compare against here — features are
    the standard basis of R^n_features, so the encoder's own weight columns
    (one per feature) *are* the learned feature directions. What changes with
    sparsity is (1) whether a feature gets a nonzero direction at all
    (`n_represented`, `feature_norms`) and (2) how many dimensions each
    represented feature effectively gets to itself
    (`dimensionality`, Elhage et al.'s `D_i = ||W_i||^2 / sum_j (Ŵ_i·W_j)^2`).

    Returns:
        Dict with per-feature arrays and summary scalars.
    """
    model.eval()
    W = model.encoder.weight.data.cpu().numpy()  # (n_dimensions, n_features)

    feature_norms = np.linalg.norm(W, axis=0)  # (n_features,)
    n_represented = int((feature_norms > threshold).sum())

    W_hat = W / (feature_norms[np.newaxis, :] + 1e-8)  # unit-norm columns
    # dots[i, j] = Ŵ_i . W_j  (row i is feature i's normalized direction dotted
    # against every feature's raw direction, including itself)
    dots = W_hat.T @ W  # (n_features, n_features)
    denom = (dots**2).sum(axis=1)
    dimensionality = (feature_norms**2) / (denom + 1e-8)

    gram_normalized = W_hat.T @ W_hat  # (n_features, n_features), cosine similarities
    off_diagonal = gram_normalized.copy()
    np.fill_diagonal(off_diagonal, 0.0)
    mean_abs_correlation = float(np.abs(off_diagonal).mean())

    return {
        "feature_norms": feature_norms,
        "n_represented": n_represented,
        "dimensionality": dimensionality,
        "mean_dimensionality": float(dimensionality.mean()),
        "gram_normalized": gram_normalized,
        "mean_abs_correlation": mean_abs_correlation,
    }


def compute_feature_angles(weight: np.ndarray) -> list[float]:
    """Angles in degrees of each encoder direction in R^2 (n_dimensions=2).

    Elhage et al.'s canonical small case: 5 features into 2 dimensions must
    land on the vertices of an approximate pentagon — directions evenly
    spaced around the circle at ~72° apart. This function extracts the
    unordered set of absolute angles so `angular_gap_metrics()` can check
    that spacing claim against the learned encoder.
    """
    if weight.shape[0] != 2:
        raise ValueError(
            f"compute_feature_angles requires n_dimensions=2, got {weight.shape[0]}"
        )
    angles = np.degrees(np.arctan2(weight[1], weight[0])) % 360.0
    return sorted(angles.tolist())


def angular_gap_metrics(angles: list[float]) -> dict:
    """Gaps between consecutive angles (circularly), the pentagon check.

    For n features evenly spaced on a circle the consecutive gaps are all
    ~360/n. Report the gap list plus min/max/std so the reader can judge
    "pentagon-like" quantitatively instead of by eye. A clean pentagon
    (n=5, evenly spaced) gives gaps of 72.0, 72.0, 72.0, 72.0, 72.0.
    """
    sorted_angles = sorted(angles)
    n = len(sorted_angles)
    gaps = [
        (sorted_angles[(i + 1) % n] - sorted_angles[i]) % 360.0 for i in range(n)
    ]
    return {
        "n_directions": n,
        "gap_degrees": gaps,
        "gap_min": float(min(gaps)),
        "gap_max": float(max(gaps)),
        "gap_std": float(np.std(gaps, ddof=0)),
        "expected_gap": 360.0 / n if n else 0.0,
    }


def is_pentagon_like(gap_metrics: dict, min_gap: float = 45.0) -> bool:
    """True if the direction spacing is roughly equiangular (the pentagon
    arrangement). Heuristic: every consecutive gap exceeds `min_gap` and the
    spread (std) is small relative to the expected gap."""
    if gap_metrics["n_directions"] < 3:
        return False
    expected = gap_metrics["expected_gap"]
    return gap_metrics["gap_min"] >= min_gap and gap_metrics["gap_std"] < 0.35 * expected


def plot_feature_directions(
    angles: list[float],
    save_path: Path,
    sparsity: float,
    n_features: int,
) -> None:
    """Polar plot of the learned feature directions — the pentagon check
    rendered as geometry instead of numbers."""
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw={"projection": "polar"})
    theta = np.radians(angles)
    ax.scatter(theta, np.ones(len(theta)), s=120, color="steelblue", zorder=3)
    for t, angle in zip(theta, angles):
        ax.annotate(f"{angle:.0f}°", (t, 1.05), ha="center", fontsize=9)
    expected_gap = 360.0 / n_features
    ideal = np.radians(np.arange(n_features) * expected_gap)
    ax.scatter(ideal, np.ones(n_features), marker="x", s=80, color="crimson", zorder=4)
    ax.set_title(
        f"Learned Feature Directions (sparsity={sparsity}, {n_features} features, "
        f"2 dims) — x: ideal {expected_gap:.0f}° spacing",
        fontsize=10,
        pad=20,
    )
    ax.set_ylim(0, 1.25)
    fig.tight_layout()
    fig.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    logger.info(f"Saved feature direction geometry to {save_path}")


# ---------------------------------------------------------------------------
# Plotting
# ---------------------------------------------------------------------------
def plot_feature_geometry(
    gram_normalized: np.ndarray,
    n_features: int,
    save_path: Path,
) -> None:
    """Heatmap of cosine similarities between learned feature directions."""
    fig, ax = plt.subplots(figsize=(8, 7))
    im = ax.imshow(gram_normalized, cmap="RdBu_r", vmin=-1, vmax=1)
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
    represented_fractions: list[float],
    mean_dimensionalities: list[float],
    save_path: Path,
) -> None:
    """Plot the phase transition: fraction of features represented and mean
    dimensionality per feature, both vs. sparsity."""
    fig, ax1 = plt.subplots(figsize=(10, 6))

    color1 = "steelblue"
    ax1.plot(
        sparsity_values,
        represented_fractions,
        marker="o",
        linewidth=2,
        color=color1,
        label="Fraction of Features Represented (‖W_i‖ > τ)",
    )
    ax1.set_xlabel("Feature Sparsity (probability of activation)")
    ax1.set_ylabel("Fraction of Features Represented", color=color1)
    ax1.tick_params(axis="y", labelcolor=color1)
    ax1.set_xscale("log")
    ax1.set_ylim(-0.05, 1.05)
    ax1.grid(True, alpha=0.3)

    color2 = "crimson"
    ax2 = ax1.twinx()
    ax2.plot(
        sparsity_values,
        mean_dimensionalities,
        marker="s",
        linewidth=2,
        color=color2,
        label="Mean Dimensionality per Feature",
    )
    ax2.set_ylabel("Mean Dimensionality (D_i)", color=color2)
    ax2.tick_params(axis="y", labelcolor=color2)

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="center left")

    fig.suptitle("Phase Change: Feature Representation vs. Sparsity", fontsize=14)
    fig.tight_layout()
    fig.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    logger.info(f"Saved phase change plot to {save_path}")


# ---------------------------------------------------------------------------
# Multi-seed headline run
# ---------------------------------------------------------------------------
def run_single_seed(seed: int, args: argparse.Namespace) -> dict[str, float]:
    """Train one autoencoder at a single representative sparsity and return
    the headline geometry metrics for one seed.

    Used by `--seeds` to aggregate across seeds (see
    `src.experiments.runner.run_seeds`) instead of running the full,
    plot-producing sparsity sweep once per seed — the sweep is for the
    figures; this is for a defensible number with a spread attached to it.
    """
    sparsity = args.single_sparsity if args.single_sparsity is not None else 0.01
    dataset = SparseFeatureDataset(
        n_features=args.n_features,
        sparsity=sparsity,
        num_samples=args.num_samples,
        importance_decay=args.importance_decay,
        seed=seed,
    )
    loader = DataLoader(dataset, batch_size=args.batch_size, shuffle=True)
    model = ToyAutoencoder(n_features=args.n_features, n_dimensions=args.n_dimensions)
    train_autoencoder(
        model=model,
        loader=loader,
        importance=dataset.importance,
        epochs=args.epochs,
        lr=args.lr,
        seed=seed,
    )
    geometry = compute_feature_geometry(model, threshold=args.threshold)
    return {
        "n_represented": float(geometry["n_represented"]),
        "mean_dimensionality": geometry["mean_dimensionality"],
        "mean_abs_correlation": geometry["mean_abs_correlation"],
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    FIGURES_DIR.mkdir(exist_ok=True)
    parser = argparse.ArgumentParser(
        description="Rung 3: Toy Models of Superposition"
    )
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument(
        "--n-features", type=int, default=20, help="Number of ground-truth features"
    )
    parser.add_argument(
        "--n-dimensions", type=int, default=5, help="Bottleneck dimension (< n-features)"
    )
    parser.add_argument(
        "--importance-decay",
        type=float,
        default=1.0,
        help="Per-feature importance decay (I_i = decay^i); 1.0 = uniform importance",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.5,
        help="Encoder-norm threshold for counting a feature as 'represented'",
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
    parser.add_argument("--quick", action="store_true", help="Quick test (reduced config)")
    parser.add_argument(
        "--geometry-check",
        action="store_true",
        help=(
            "Run the known small case — 5 features into 2 dimensions — and "
            "check that represented features land on an approximate pentagon "
            "(equiangular ~72 degree spacing in the Gram matrix). Trains at "
            "several sparsities and reports angular-gap metrics per level."
        ),
    )
    parser.add_argument(
        "--seeds",
        type=str,
        default=None,
        help=(
            "Comma-separated seeds (e.g. '0,1,2'). If set, runs the "
            "headline single-sparsity config across all seeds, saves a "
            "results/exp3_superposition.json manifest, and skips the "
            "plot-producing sweep."
        ),
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )

    if args.quick:
        args.epochs = 2000
        args.num_samples = 10000
        logger.info("QUICK MODE: reduced config for fast iteration")

    logger.info(f"Device: {DEVICE}")
    logger.info(f"Arguments: {vars(args)}")

    set_seed(args.seed)

    if args.seeds:
        seeds = parse_seeds(args.seeds)
        sparsity = args.single_sparsity if args.single_sparsity is not None else 0.01
        logger.info(
            f"MULTI-SEED MODE: {len(seeds)} seeds {seeds} at sparsity={sparsity} "
            "(skipping the plot-producing sweep)"
        )
        result = run_seeds(lambda s: run_single_seed(s, args), seeds)
        probe_model = ToyAutoencoder(
            n_features=args.n_features, n_dimensions=args.n_dimensions
        )
        manifest = ResultsManifest.from_run(
            experiment="exp3_superposition",
            seeds=seeds,
            args={k: v for k, v in vars(args).items() if k != "seeds"},
            per_seed_metrics=result.per_seed,
            aggregate=result.aggregate,
            wall_clock_seconds=result.wall_clock_seconds,
            device=str(DEVICE),
            n_parameters=count_parameters(probe_model),
        )
        manifest_path = Path("results") / "exp3_superposition.json"
        manifest.save(manifest_path)
        logger.info(f"Saved multi-seed manifest to {manifest_path}")
        for key in result.aggregate:
            logger.info(f"  {key}: {result.summary_line(key)}")
        return

    if args.geometry_check:
        logger.info("=" * 60)
        logger.info("PENTAGON GEOMETRY CHECK (5 features -> 2 dimensions)")
        logger.info("=" * 60)
        sparsity_values = [0.5, 0.2, 0.1, 0.05, 0.02, 0.01]
        logger.info(
            f"{'Sparsity':>10} | {'Represented':>10} | {'Gap min':>8} | "
            f"{'Gap max':>8} | {'Gap std':>8} | {'Pentagon-like':>14}"
        )
        logger.info("-" * 68)
        final_gaps = None
        for sparsity in sparsity_values:
            dataset = SparseFeatureDataset(
                n_features=5,
                sparsity=sparsity,
                num_samples=args.num_samples,
                importance_decay=args.importance_decay,
                seed=args.seed,
            )
            loader = DataLoader(dataset, batch_size=args.batch_size, shuffle=True)
            model = ToyAutoencoder(n_features=5, n_dimensions=2)
            train_autoencoder(
                model=model,
                loader=loader,
                importance=dataset.importance,
                epochs=args.epochs,
                lr=args.lr,
                seed=args.seed,
            )
            geometry = compute_feature_geometry(model, threshold=args.threshold)
            W = model.encoder.weight.data.cpu().numpy()
            angles = compute_feature_angles(W)
            gaps = angular_gap_metrics(angles)
            pentagon = is_pentagon_like(gaps)
            logger.info(
                f"{sparsity:>10.4f} | {geometry['n_represented']:>6d}/5 | "
                f"{gaps['gap_min']:>8.1f} | {gaps['gap_max']:>8.1f} | "
                f"{gaps['gap_std']:>8.1f} | {str(pentagon):>14}"
            )
            final_gaps = (gaps, sparsity, angles)
        if final_gaps is not None:
            gaps, sparsity, angles = final_gaps
            plot_feature_directions(
                angles,
                save_path=FIGURES_DIR / "exp3_pentagon_geometry.png",
                sparsity=sparsity,
                n_features=5,
            )
            if is_pentagon_like(gaps):
                logger.info(
                    "✓ CONFIRMED: learned directions are approximately "
                    f"equiangular (gaps {gaps['gap_min']:.1f}-{gaps['gap_max']:.1f}°, "
                    f"std {gaps['gap_std']:.1f}° vs ideal {gaps['expected_gap']:.1f}°)"
                )
            else:
                logger.warning(
                    "Directions are not pentagon-like at the sparsest level — "
                    "the geometric claim needs a closer look (see figure)."
                )
        return

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
            sparsity=sparsity,
            num_samples=args.num_samples,
            importance_decay=args.importance_decay,
            seed=args.seed,
        )
        loader = DataLoader(
            dataset, batch_size=args.batch_size, shuffle=True
        )

        model = ToyAutoencoder(
            n_features=args.n_features,
            n_dimensions=args.n_dimensions,
        )

        train_autoencoder(
            model=model,
            loader=loader,
            importance=dataset.importance,
            epochs=args.epochs,
            lr=args.lr,
            seed=args.seed,
        )

        geometry = compute_feature_geometry(model, threshold=args.threshold)

        logger.info(
            f"Represented: {geometry['n_represented']}/{args.n_features} | "
            f"Mean dimensionality: {geometry['mean_dimensionality']:.3f} | "
            f"Mean abs corr: {geometry['mean_abs_correlation']:.3f}"
        )

        results.append({
            "sparsity": sparsity,
            "n_features": args.n_features,
            **geometry,
        })

    # Plot phase change if we did a sweep
    if len(sparsity_values) > 1:
        represented_fractions = [
            r["n_represented"] / r["n_features"] for r in results
        ]
        mean_dimensionalities = [r["mean_dimensionality"] for r in results]
        plot_phase_change(
            sparsity_values,
            represented_fractions,
            mean_dimensionalities,
            save_path=FIGURES_DIR / "exp3_phase_change.png",
        )

    # Plot geometry for the final/default sparsity
    final_result = results[-1]
    plot_feature_geometry(
        final_result["gram_normalized"],
        n_features=args.n_features,
        save_path=FIGURES_DIR / "exp3_feature_geometry.png",
    )

    # Summary table
    logger.info("=" * 60)
    logger.info("SUPERPOSITION EXPERIMENT COMPLETE")
    logger.info("=" * 60)
    logger.info(
        f"{'Sparsity':>10} | {'Represented':>11} | {'Mean Dim':>9} | {'Mean |Corr|':>10}"
    )
    logger.info("-" * 55)
    for r in results:
        logger.info(
            f"{r['sparsity']:>10.4f} | {r['n_represented']:>6d}/{r['n_features']:<4d} | "
            f"{r['mean_dimensionality']:>9.3f} | "
            f"{r['mean_abs_correlation']:>10.3f}"
        )

    # Interpretation
    dense = results[0]
    sparse = results[-1]
    if dense["n_represented"] < sparse["n_represented"]:
        logger.info(
            "✓ CONFIRMED phase transition: more features get represented "
            "at all as sparsity increases (fewer active at once -> less "
            "interference pressure -> the bottleneck can host more of them)."
        )
    else:
        logger.info(
            "No monotonic increase in represented features from dense to "
            "sparse in this sweep — inspect the full table above."
        )


if __name__ == "__main__":
    main()
