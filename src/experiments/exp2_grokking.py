#!/usr/bin/env python3
"""Rung 2 — Grokking modular addition with Fourier reverse-engineering (FLAGSHIP ★).

Reproduces Nanda et al. (ICLR 2023): trains a 1-layer transformer on modular
addition (a+b mod P) and observes delayed generalization (grokking). Reverse-
engineers the learned algorithm via Fourier decomposition of the embeddings:
the model implements addition via discrete Fourier transforms and trigonometric
identities. Confirms the mechanism by ablating individual Fourier frequencies.

Usage:
    python -m src.experiments.exp2_grokking --seed 42 --modulus 113

Output:
    - figures/exp2_grokking_curve.png
    - figures/exp2_fourier_weights.png
    - figures/exp2_frequency_ablation.png
    - figures/exp2_progress_measures.png
    - Console: grokking summary with Fourier analysis results
"""

import argparse
import logging
from pathlib import Path
from typing import Optional

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
# Data: modular addition
# ---------------------------------------------------------------------------
def make_modular_addition_data(
    modulus: int,
    train_fraction: float,
    seed: int = 42,
) -> tuple[TensorDataset, TensorDataset]:
    """Generate modular addition task (a + b mod P).

    The data is split such that a fraction of all (a, b) pairs are held out
    by modulus value, following the canonical grokking setup.

    Returns:
        Tuple of (train_dataset, val_dataset). Each sample is an equation
        represented as (a, b, target) where a, b, target are in [0, P).
    """
    rng = np.random.default_rng(seed)

    # All possible pairs
    all_pairs = [(a, b) for a in range(modulus) for b in range(modulus)]
    rng.shuffle(all_pairs)

    # Split: train on a fraction of modulus values
    train_mod_values = set(
        rng.choice(modulus, size=int(modulus * train_fraction), replace=False)
    )
    train_pairs = [(a, b) for a, b in all_pairs if (a + b) % modulus in train_mod_values]
    val_pairs = [(a, b) for a, b in all_pairs if (a + b) % modulus not in train_mod_values]

    def _to_tensor(pairs: list) -> torch.Tensor:
        a = torch.tensor([p[0] for p in pairs], dtype=torch.long)
        b = torch.tensor([p[1] for p in pairs], dtype=torch.long)
        target = (a + b) % modulus
        return torch.stack([a, b], dim=1), target

    train_x, train_y = _to_tensor(train_pairs)
    val_x, val_y = _to_tensor(val_pairs)

    return (
        TensorDataset(train_x, train_y),
        TensorDataset(val_x, val_y),
    )


# ---------------------------------------------------------------------------
# Model: 1-layer decoder-only transformer (Nanda et al. config)
# ---------------------------------------------------------------------------
class OneLayerTransformer(nn.Module):
    """Single-layer decoder-only transformer for modular addition.

    Architecture per Nanda et al. (ICLR 2023):
    - Embedding: d_model (maps input tokens to dense vectors)
    - Positional embedding: learned per position (2 positions: a and b)
    - One attention block with n_heads
    - One MLP block with ReLU
    - LayerNorm pre each block
    - Unembedding: maps residual stream to vocabulary
    """

    def __init__(
        self,
        d_model: int,
        d_mlp: int,
        n_heads: int,
        modulus: int,
        max_positions: int = 2,
        normalize_embed: bool = True,
    ) -> None:
        super().__init__()
        assert d_model % n_heads == 0
        self.d_model = d_model
        self.d_head = d_model // n_heads
        self.n_heads = n_heads
        self.modulus = modulus
        self.normalize_embed = normalize_embed

        self.embed = nn.Embedding(modulus, d_model)
        self.pos_embed = nn.Embedding(max_positions, d_model)

        # Attention
        self.ln1 = nn.LayerNorm(d_model)
        self.W_Q = nn.Linear(d_model, d_model, bias=False)
        self.W_K = nn.Linear(d_model, d_model, bias=False)
        self.W_V = nn.Linear(d_model, d_model, bias=False)
        self.W_O = nn.Linear(d_model, d_model, bias=False)

        # MLP
        self.ln2 = nn.LayerNorm(d_model)
        self.W_in = nn.Linear(d_model, d_mlp, bias=False)
        self.W_out = nn.Linear(d_mlp, d_model, bias=False)

        # Unembed
        self.ln_final = nn.LayerNorm(d_model)
        self.unembed = nn.Linear(d_model, modulus, bias=False)

    def normalize_embeddings(self) -> None:
        if self.normalize_embed:
            with torch.no_grad():
                self.embed.weight.data = nn.functional.normalize(
                    self.embed.weight.data, dim=-1
                )
                self.unembed.weight.data = nn.functional.normalize(
                    self.unembed.weight.data, dim=-1
                )

    def forward(
        self, x: torch.Tensor, return_activations: bool = False
    ) -> tuple[torch.Tensor, Optional[dict]]:
        """Forward pass.

        Args:
            x: (B, 2) tensor with (a, b) token indices.
            return_activations: if True, return intermediate activations for analysis.

        Returns:
            Tuple of (logits, activations_dict). Logits shape: (B, modulus).
        """
        B = x.shape[0]
        positions = torch.arange(2, device=x.device).unsqueeze(0)

        h = self.embed(x) + self.pos_embed(positions)  # (B, 2, d_model)

        activations = {} if return_activations else None

        # Attention block
        h_ln = self.ln1(h)
        Q = self.W_Q(h_ln).view(B, 2, self.n_heads, self.d_head).transpose(1, 2)
        K = self.W_K(h_ln).view(B, 2, self.n_heads, self.d_head).transpose(1, 2)
        V = self.W_V(h_ln).view(B, 2, self.n_heads, self.d_head).transpose(1, 2)

        attn_scores = Q @ K.transpose(-2, -1) / (self.d_head ** 0.5)
        # No causal mask needed for 2 positions (full visibility)
        attn_probs = attn_scores.softmax(dim=-1)

        if return_activations:
            activations["attn_probs"] = attn_probs.detach().cpu()
            activations["embed"] = self.embed.weight.data.detach().cpu()

        attn_out = attn_probs @ V  # (B, n_heads, 2, d_head)
        attn_out = attn_out.transpose(1, 2).contiguous().view(B, 2, self.d_model)
        attn_out = self.W_O(attn_out)
        h = h + attn_out

        # MLP block
        h_ln = self.ln2(h)
        mlp_out = self.W_out(torch.relu(self.W_in(h_ln)))
        h = h + mlp_out

        # Final prediction from the last position
        h_final = self.ln_final(h[:, -1, :])
        logits = self.unembed(h_final)

        return logits, activations


# ---------------------------------------------------------------------------
# Training
# ---------------------------------------------------------------------------
@torch.no_grad()
def evaluate(
    model: nn.Module, loader: DataLoader
) -> tuple[float, float]:
    model.eval()
    total_loss = 0.0
    total_correct = 0
    total = 0
    criterion = nn.CrossEntropyLoss()

    for x, y in loader:
        x, y = x.to(DEVICE), y.to(DEVICE)
        logits, _ = model(x)
        loss = criterion(logits, y)
        total_loss += loss.item() * x.size(0)
        total_correct += (logits.argmax(dim=-1) == y).sum().item()
        total += y.size(0)

    return total_loss / total, total_correct / total


def train_model(
    model: nn.Module,
    train_loader: DataLoader,
    val_loader: DataLoader,
    epochs: int,
    lr: float,
    weight_decay: float,
    seed: int,
    use_wandb: bool = False,
) -> dict:
    """Train and return history with progress measures.

    If use_wandb is True, logs metrics to Weights & Biases.
    Falls back gracefully if wandb is not installed or not logged in.
    """
    set_seed(seed)
    model = model.to(DEVICE)

    _wandb = None
    if use_wandb:
        try:
            import wandb as _wandb
            _wandb.init(
                project="from-gradient-to-transformer",
                config={
                    "modulus": model.modulus,
                    "d_model": model.d_model,
                    "n_heads": model.n_heads,
                    "lr": lr,
                    "weight_decay": weight_decay,
                    "epochs": epochs,
                    "seed": seed,
                },
            )
        except Exception as e:
            logger.warning(f"W&B init failed, continuing without: {e}")
            _wandb = None

    decay_params = []
    no_decay_params = []
    for name, param in model.named_parameters():
        if "embed" in name or "ln" in name or "pos_embed" in name:
            no_decay_params.append(param)
        else:
            decay_params.append(param)
    optimizer = torch.optim.AdamW(
        [
            {"params": decay_params, "weight_decay": weight_decay},
            {"params": no_decay_params, "weight_decay": 0.0},
        ],
        lr=lr,
    )
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs)
    criterion = nn.CrossEntropyLoss()

    history = {
        "train_loss": [],
        "val_loss": [],
        "train_acc": [],
        "val_acc": [],
        "embed_norm": [],
        "embed_norm_max": [],
        "embed_norm_min": [],
        "unembed_norm": [],
        "attn_entropy": [],
        "weight_decay_norm": [],
    }

    for epoch in tqdm(range(epochs), desc="Training"):
        model.train()
        epoch_loss = 0.0
        epoch_correct = 0
        epoch_total = 0

        for x, y in train_loader:
            x, y = x.to(DEVICE), y.to(DEVICE)
            optimizer.zero_grad()
            logits, _ = model(x)
            loss = criterion(logits, y)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()
            model.normalize_embeddings()

            epoch_loss += loss.item() * x.size(0)
            epoch_correct += (logits.argmax(dim=-1) == y).sum().item()
            epoch_total += y.size(0)

        train_loss = epoch_loss / epoch_total
        train_acc = epoch_correct / epoch_total
        val_loss, val_acc = evaluate(model, val_loader)

        scheduler.step()

        embed_norm = model.embed.weight.norm(dim=-1)
        embed_norm_mean = embed_norm.mean().item()
        embed_norm_max = embed_norm.max().item()
        embed_norm_min = embed_norm.min().item()
        unembed_norm = model.unembed.weight.norm(dim=-1)
        unembed_norm_mean = unembed_norm.mean().item()
        wd_norm = sum(
            p.norm().item() for n, p in model.named_parameters()
            if "weight" in n and "ln" not in n and "embed" not in n
        )

        # Attention entropy: measure of how diffused attention is
        with torch.no_grad():
            sample_x = next(iter(train_loader))[0].to(DEVICE)[:8]
            _, activations = model(sample_x, return_activations=True)
            if activations and "attn_probs" in activations:
                attn = activations["attn_probs"]
                entropy = -(attn * (attn + 1e-8).log()).sum(-1).mean(-1).mean().item()
            else:
                entropy = 0.0

        history["train_loss"].append(train_loss)
        history["val_loss"].append(val_loss)
        history["train_acc"].append(train_acc)
        history["val_acc"].append(val_acc)
        history["embed_norm"].append(embed_norm_mean)
        history["embed_norm_max"].append(embed_norm_max)
        history["embed_norm_min"].append(embed_norm_min)
        history["unembed_norm"].append(unembed_norm_mean)
        history["attn_entropy"].append(entropy)
        history["weight_decay_norm"].append(wd_norm)

        if _wandb is not None:
            _wandb.log({
                "train/loss": train_loss,
                "val/loss": val_loss,
                "train/acc": train_acc,
                "val/acc": val_acc,
                "metrics/embed_norm_mean": embed_norm_mean,
                "metrics/embed_norm_max": embed_norm_max,
                "metrics/embed_norm_min": embed_norm_min,
                "metrics/unembed_norm": unembed_norm_mean,
                "metrics/attn_entropy": entropy,
                "metrics/weight_decay_norm": wd_norm,
                "lr": scheduler.get_last_lr()[0],
            }, step=epoch)

        current_lr = scheduler.get_last_lr()[0]
        if (epoch + 1) % 50 == 0 or epoch == 0:
            logger.info(
                f"Epoch {epoch+1:4d} | train loss: {train_loss:.4f} | "
                f"val loss: {val_loss:.4f} | val acc: {val_acc:.4f} | "
                f"embed norm: {embed_norm_mean:.2f} ({embed_norm_min:.2f}-{embed_norm_max:.2f}) | "
                f"unembed norm: {unembed_norm_mean:.2f} | "
                f"lr: {current_lr:.2e}"
            )

    if _wandb is not None:
        _wandb.finish()

    return history


# ---------------------------------------------------------------------------
# Fourier analysis
# ---------------------------------------------------------------------------
def fourier_decompose_embeddings(
    embed_weight: torch.Tensor, modulus: int
) -> dict:
    """Decompose the learned embeddings into Fourier frequencies.

    The model learns a discrete Fourier transform basis. The embedding for
    each number n in [0, P) should decompose into sparse Fourier frequencies,
    revealing that the model represents numbers via their frequency components.

    Args:
        embed_weight: (modulus, d_model) embedding matrix.
        modulus: The modulus P.

    Returns:
        Dict with:
        - frequencies: (modulus,) array of frequency magnitudes per embedding dim.
        - top_frequencies: indices of the top-k frequencies by magnitude.
        - fourier_basis: (modulus, modulus) DFT matrix.
    """
    # Construct the Fourier basis matrix: (modulus, modulus)
    # F_{k, n} = exp(-2πi * k * n / P) / sqrt(P)
    k = torch.arange(modulus, device=embed_weight.device).float()
    n = torch.arange(modulus, device=embed_weight.device).float()
    fourier_basis = torch.exp(-2j * np.pi * k[:, None] * n[None, :] / modulus)
    fourier_basis = fourier_basis / (modulus ** 0.5)

    # Project each embedding dimension onto the Fourier basis
    # embed_weight: (P, d_model) -> fourier_coeffs: (P, d_model)
    embed_complex = embed_weight.to(fourier_basis.dtype)
    fourier_coeffs = fourier_basis.conj().T @ embed_complex
    fourier_magnitudes = fourier_coeffs.abs()

    # Per-frequency magnitude: sum across embedding dimensions
    freq_magnitudes = fourier_magnitudes.sum(dim=1)

    return {
        "frequencies": freq_magnitudes.cpu(),
        "fourier_basis": fourier_basis.cpu(),
        "fourier_coeffs": fourier_coeffs.cpu(),
        "top_frequencies": freq_magnitudes.argsort(descending=True),
    }


def analyze_fourier_sparsity(fourier_result: dict, top_k: int = 10) -> dict:
    """Analyze how sparse the Fourier representation is.

    The key signature of the grokking Fourier algorithm: the model uses a
    small set of frequencies (O(sqrt(P))) and the rest carry negligible weight.

    Returns:
        Dict with sparsity metrics.
    """
    magnitudes = fourier_result["frequencies"].numpy()
    total_mass = magnitudes.sum()
    sorted_mags = np.sort(magnitudes)[::-1]
    cumulative = np.cumsum(sorted_mags) / total_mass

    # Number of frequencies needed to reach 90% / 99% of mass
    k_90 = int(np.searchsorted(cumulative, 0.9) + 1)
    k_99 = int(np.searchsorted(cumulative, 0.99) + 1)

    top_freqs = fourier_result["top_frequencies"][:top_k].numpy()

    return {
        "k_90_percent": k_90,
        "k_99_percent": k_99,
        "top_frequencies": top_freqs.tolist(),
        "total_mass_top_k": cumulative[top_k - 1] if top_k <= len(cumulative) else 1.0,
    }


# ---------------------------------------------------------------------------
# Causal ablation: remove Fourier frequencies
# ---------------------------------------------------------------------------
def ablate_frequencies(
    model: nn.Module,
    loader: DataLoader,
    frequencies_to_keep: list[int],
) -> float:
    """Ablate all but the specified Fourier frequencies from the embeddings.

    Projects the embedding matrix onto the subspace spanned by the specified
    Fourier basis vectors, effectively removing all other frequency content.
    Measures the accuracy after this intervention.

    Args:
        model: The trained model.
        loader: DataLoader with validation data.
        frequencies_to_keep: Indices of Fourier frequencies to preserve.

    Returns:
        Accuracy after frequency ablation.
    """
    model.eval()
    modulus = model.modulus

    # Construct Fourier basis
    k = torch.arange(modulus).float()
    n = torch.arange(modulus).float()
    fourier_basis = torch.exp(-2j * np.pi * k[:, None] * n[None, :] / modulus)
    fourier_basis = fourier_basis / (modulus ** 0.5)

    # Build the projection matrix onto the kept frequencies
    proj_matrix = torch.zeros(modulus, modulus, dtype=torch.complex64)
    for f in frequencies_to_keep:
        proj_matrix = proj_matrix + fourier_basis[:, f:f+1] @ fourier_basis[:, f:f+1].conj().T

    # Apply to embeddings (real part)
    with torch.no_grad():
        original_embed = model.embed.weight.data.clone()
        # Project each embedding vector (cast to complex for multiplication)
        embed_complex = original_embed.to(proj_matrix.dtype)
        projected = (proj_matrix @ embed_complex).real.to(original_embed.dtype)
        model.embed.weight.data = projected

    # Evaluate
    correct = 0
    total = 0
    for x, y in loader:
        x, y = x.to(DEVICE), y.to(DEVICE)
        logits, _ = model(x)
        correct += (logits.argmax(dim=-1) == y).sum().item()
        total += y.size(0)

    # Restore
    with torch.no_grad():
        model.embed.weight.data = original_embed.to(model.embed.weight.device)

    return correct / total


def run_ablation_sweep(
    model: nn.Module,
    loader: DataLoader,
    fourier_result: dict,
    modulus: int,
) -> dict:
    """Sweep ablation: keep increasing number of frequencies and measure accuracy.

    The expected result: keeping only the sparse set of key frequencies (top ~20)
    preserves performance. Keeping all but the key frequencies (i.e., ablating
    only the critical few) destroys performance.

    Returns:
        Dict with ablation curve data.
    """
    sorted_freqs = fourier_result["frequencies"].argsort(descending=True).numpy()

    n_freqs_to_test = [0, 1, 2, 3, 5, 10, 20, 50, 100, modulus]
    accuracies = []

    for n in n_freqs_to_test:
        if n == 0:
            # Random baseline: shuffle labels
            model.eval()
            correct = 0
            total = 0
            for x, y in loader:
                x = x.to(DEVICE)
                logits, _ = model(x)
                # Random prediction
                preds = torch.randint(0, modulus, y.shape, device=DEVICE)
                correct += (preds == y.to(DEVICE)).sum().item()
                total += y.size(0)
            accuracies.append(correct / total)
            acc_str = f"{accuracies[-1]:.4f}"
            logger.info(f"Ablation: keep {n:4d} freqs → accuracy: {acc_str} (random baseline)")
        else:
            freqs_to_keep = sorted_freqs[:n].tolist()
            acc = ablate_frequencies(model, loader, freqs_to_keep)
            accuracies.append(acc)
            logger.info(f"Ablation: keep {n:4d} freqs → accuracy: {acc:.4f}")

    # Also test: keep ALL frequencies EXCEPT the top few
    keep_all_except = []
    n_freqs_to_remove = [1, 2, 3, 5, 10, 20]
    for n in n_freqs_to_remove:
        freqs_to_remove = sorted_freqs[:n].tolist()
        freqs_to_keep = [f for f in range(modulus) if f not in freqs_to_remove]
        acc = ablate_frequencies(model, loader, freqs_to_keep)
        keep_all_except.append(acc)
        logger.info(
            f"Ablation: remove top {n:4d} freqs → accuracy: {acc:.4f} "
            f"(drop: {accuracies[-1] - acc:+.4f})"
        )

    return {
        "n_freqs": n_freqs_to_test,
        "accuracies": accuracies,
        "n_removed": n_freqs_to_remove,
        "keep_all_except": keep_all_except,
    }


# ---------------------------------------------------------------------------
# Progress measures
# ---------------------------------------------------------------------------
def compute_progress_measures(
    history: dict, fourier_result: dict, modulus: int
) -> dict:
    """Analyze the three phases of grokking.

    Phase 1 - Memorization: train loss drops, val loss stays high.
    Phase 2 - Circuit formation: Fourier weight grows, generalization begins.
    Phase 3 - Cleanup: unnecessary frequencies are pruned, val accuracy peaks.

    Returns:
        Dict with phase boundaries and metrics.
    """
    val_acc = np.array(history["val_acc"])
    embed_norm = np.array(history["embed_norm"])

    # Phase 1 → Phase 2: when val accuracy first exceeds 1/P (random chance)
    random_baseline = 1.0 / modulus
    phase1_end = np.where(val_acc > random_baseline * 2)[0]
    phase1_end = int(phase1_end[0]) if len(phase1_end) > 0 else len(val_acc) // 3

    # Phase 2 → Phase 3: when Fourier sparsity stops increasing rapidly
    # (embedding norm plateau indicates circuit consolidation)
    norm_diff = np.abs(np.diff(embed_norm))
    if len(norm_diff) > 0 and norm_diff.mean() > 0:
        plateau_indices = np.where(norm_diff < norm_diff.mean() * 0.1)[0]
        if len(plateau_indices) > 0:
            phase2_end = int(plateau_indices[0])
        else:
            phase2_end = len(embed_norm) - 1
    else:
        phase2_end = len(embed_norm) - 1
    if phase2_end < phase1_end or phase2_end >= len(embed_norm) - 1:
        phase2_end = len(embed_norm) - 1

    return {
        "phase1_end": int(phase1_end),
        "phase2_end": int(phase2_end),
        "memorization_epochs": int(phase1_end),
        "circuit_formation_epochs": int(phase2_end - phase1_end),
        "cleanup_epochs": int(len(val_acc) - phase2_end),
    }


# ---------------------------------------------------------------------------
# Plotting
# ---------------------------------------------------------------------------
def plot_progress_measures(
    history: dict,
    save_path: Path,
) -> None:
    """Plot embedding/unembed norms and attention entropy over training."""
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    epochs = range(1, len(history["embed_norm"]) + 1)

    ax = axes[0]
    ax.plot(epochs, history["embed_norm"], label="Embed norm (mean)", linewidth=1)
    ax.plot(epochs, history["embed_norm_max"], label="Embed norm (max)", linewidth=0.8, alpha=0.5)
    ax.plot(epochs, history["embed_norm_min"], label="Embed norm (min)", linewidth=0.8, alpha=0.5)
    ax.set_xlabel("Epoch")
    ax.set_ylabel("Row-wise L2 norm")
    ax.set_title("Embedding Row Norms (should converge to 1.0)", fontsize=12)
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)
    ax.axhline(y=1.0, color="gray", linestyle="--", alpha=0.3)

    ax = axes[1]
    ax.plot(epochs, history["unembed_norm"], label="Unembed norm (mean)", color="orange", lw=1)
    ax.set_xlabel("Epoch")
    ax.set_ylabel("Row-wise L2 norm")
    ax.set_title("Unembedding Row Norms", fontsize=12)
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)
    ax.axhline(y=1.0, color="gray", linestyle="--", alpha=0.3)

    ax = axes[2]
    ax.plot(epochs, history["attn_entropy"], label="Attention entropy", color="green", linewidth=1)
    ax.set_xlabel("Epoch")
    ax.set_ylabel("Entropy (nats)")
    ax.set_title("Attention Entropy (lower = more focused)", fontsize=12)
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    fig.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    logger.info(f"Saved progress measures to {save_path}")


def plot_grokking_curve(
    history: dict,
    save_path: Path,
    phase_boundaries: Optional[dict] = None,
) -> None:
    """Plot train/val loss and accuracy with phase annotations."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    epochs = range(1, len(history["train_loss"]) + 1)
    train_loss = history["train_loss"]
    val_loss = history["val_loss"]

    # Loss plot
    ax = axes[0]
    ax.plot(epochs, train_loss, label="Train Loss", alpha=0.7, linewidth=1)
    ax.plot(epochs, val_loss, label="Val Loss", alpha=0.7, linewidth=1)
    ax.set_xlabel("Epoch")
    ax.set_ylabel("Loss")
    ax.set_title("Grokking: Train/Val Loss", fontsize=14)
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Accuracy plot
    ax = axes[1]
    ax.plot(epochs, history["val_acc"], label="Val Accuracy", color="green", linewidth=1.5)
    ax.plot(epochs, history["train_acc"], label="Train Accuracy", color="blue", alpha=0.5)
    ax.set_xlabel("Epoch")
    ax.set_ylabel("Accuracy")
    ax.set_title("Grokking: Train/Val Accuracy", fontsize=14)
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Phase boundaries
    if phase_boundaries is not None:
        colors = ["red", "orange", "green"]
        labels = ["Memorization", "Circuit Formation", "Cleanup"]
        boundaries = [
            phase_boundaries["phase1_end"],
            phase_boundaries["phase2_end"],
        ]
        for ax_i in axes:
            for b_idx, (b, c, lb) in enumerate(zip(boundaries, colors, labels)):
                if b < len(epochs):
                    label_text = lb if ax_i == axes[0] else ""
                    ax_i.axvline(x=b, color=c, linestyle="--", alpha=0.5, label=label_text)
            if ax_i == axes[0]:
                ax_i.legend()

    fig.tight_layout()
    fig.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    logger.info(f"Saved grokking curve to {save_path}")


def plot_fourier_weights(
    fourier_result: dict,
    modulus: int,
    save_path: Path,
) -> None:
    """Plot Fourier frequency magnitudes.

    The canonical result: only a sparse set of frequencies have significant
    weight, forming a distinctive pattern.
    """
    frequencies = fourier_result["frequencies"].numpy()

    fig, ax = plt.subplots(figsize=(12, 4))
    freqs = np.arange(modulus)
    ax.bar(freqs, frequencies, width=0.8, alpha=0.7, color="steelblue")
    ax.set_xlabel("Fourier Frequency k")
    ax.set_ylabel("Magnitude (sum across embedding dims)")
    ax.set_title("Fourier Decomposition of Learned Embeddings", fontsize=14)
    ax.grid(True, alpha=0.3, axis="y")

    # Highlight top frequencies
    top_k = min(10, modulus)
    top_freqs = frequencies.argsort()[::-1][:top_k]
    ax.scatter(
        top_freqs,
        frequencies[top_freqs],
        color="red",
        s=30,
        zorder=5,
        label=f"Top {top_k} frequencies",
    )
    ax.legend()

    fig.tight_layout()
    fig.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    logger.info(f"Saved Fourier weights to {save_path}")


def plot_ablation_curve(
    ablation_result: dict,
    modulus: int,
    save_path: Path,
) -> None:
    """Plot ablation results: keep N frequencies → accuracy."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Left: accuracy as function of kept frequencies
    ax = axes[0]
    ax.plot(
        ablation_result["n_freqs"],
        ablation_result["accuracies"],
        marker="o",
        color="steelblue",
        linewidth=1.5,
    )
    ax.axhline(
        y=1.0 / modulus,
        color="red",
        linestyle="--",
        alpha=0.5,
        label=f"Random chance (1/{modulus})",
    )
    ax.set_xlabel("Number of Fourier Frequencies Kept")
    ax.set_ylabel("Accuracy")
    ax.set_title("Causal Ablation: Frequency Removal", fontsize=14)
    ax.set_xscale("symlog")
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Right: accuracy when removing top frequencies
    ax = axes[1]
    ax.plot(
        ablation_result["n_removed"],
        ablation_result["keep_all_except"],
        marker="s",
        color="crimson",
        linewidth=1.5,
    )
    ax.axhline(
        y=1.0 / modulus,
        color="red",
        linestyle="--",
        alpha=0.5,
        label=f"Random chance (1/{modulus})",
    )
    ax.set_xlabel("Number of Top Frequencies Removed")
    ax.set_ylabel("Accuracy")
    ax.set_title("Ablation: Remove Top Frequencies", fontsize=14)
    ax.legend()
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    fig.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    logger.info(f"Saved ablation curve to {save_path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(
        description="Rung 2: Grokking modular addition with Fourier reverse-engineering"
    )
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument(
        "--modulus", type=int, default=113, help="Modulus P for a+b mod P"
    )
    parser.add_argument(
        "--train-fraction", type=float, default=0.3, help="Fraction of data for training"
    )
    parser.add_argument("--d-model", type=int, default=128, help="Model dimension")
    parser.add_argument("--d-mlp", type=int, default=512, help="MLP hidden dimension")
    parser.add_argument("--n-heads", type=int, default=4, help="Attention heads")
    parser.add_argument("--epochs", type=int, default=5000, help="Training epochs")
    parser.add_argument("--lr", type=float, default=1e-3, help="Learning rate")
    parser.add_argument(
        "--weight-decay", type=float, default=1.0, help="Weight decay (critical for grokking)"
    )
    parser.add_argument("--batch-size", type=int, default=512, help="Batch size")
    parser.add_argument(
        "--quick", action="store_true", help="Quick test with smaller modulus and fewer epochs"
    )
    parser.add_argument(
        "--micro", action="store_true", help="Micro test: tiny modulus, fast CPU iteration"
    )
    parser.add_argument(
        "--wandb", action="store_true", help="Log metrics to Weights & Biases"
    )
    parser.add_argument(
        "--diagnose", action="store_true", help="Print per-row norms and Fourier details each epoch"
    )
    parser.add_argument(
        "--save-model", action="store_true", help="Save trained model to figures/ dir"
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )

    if args.micro:
        args.modulus = 11
        args.d_model = 64
        args.d_mlp = 256
        args.n_heads = 2
        args.epochs = 5000
        args.weight_decay = 1.0
        args.train_fraction = 0.5
        args.batch_size = 64
        logger.info("MICRO MODE: modulus=11, d_model=64, d_mlp=256, epochs=5000, train=50%")

    if args.quick:
        args.modulus = 29
        args.epochs = 2000
        logger.info("QUICK MODE: modulus=29, epochs=2000")

    logger.info(f"Device: {DEVICE}")
    logger.info(f"Arguments: {vars(args)}")

    set_seed(args.seed)
    modulus = args.modulus

    # Data
    train_dataset, val_dataset = make_modular_addition_data(
        modulus=modulus,
        train_fraction=args.train_fraction,
        seed=args.seed,
    )
    train_loader = DataLoader(
        train_dataset, batch_size=args.batch_size, shuffle=True
    )
    val_loader = DataLoader(
        val_dataset, batch_size=args.batch_size, shuffle=False
    )
    logger.info(
        f"Data: train={len(train_dataset)} ({args.train_fraction:.0%}), "
        f"val={len(val_dataset)} ({1-args.train_fraction:.0%})"
    )

    # Model
    model = OneLayerTransformer(
        d_model=args.d_model,
        d_mlp=args.d_mlp,
        n_heads=args.n_heads,
        modulus=modulus,
    )
    n_params = sum(p.numel() for p in model.parameters())
    logger.info(f"Model parameters: {n_params:,}")

    # Train
    history = train_model(
        model=model,
        train_loader=train_loader,
        val_loader=val_loader,
        epochs=args.epochs,
        lr=args.lr,
        weight_decay=args.weight_decay,
        seed=args.seed,
        use_wandb=args.wandb,
    )

    # Fourier analysis
    logger.info("=" * 60)
    logger.info("Fourier Decomposition Analysis")
    logger.info("=" * 60)

    _, activations = model(
        torch.zeros((1, 2), dtype=torch.long, device=DEVICE),
        return_activations=True,
    )
    fourier_result = fourier_decompose_embeddings(
        model.embed.weight.data.detach().cpu(), modulus
    )
    sparsity = analyze_fourier_sparsity(fourier_result, top_k=20)
    logger.info(f"Top 10 frequencies: {sparsity['top_frequencies'][:10]}")
    logger.info(f"Frequencies for 90% mass: {sparsity['k_90_percent']} / {modulus}")
    logger.info(f"Frequencies for 99% mass: {sparsity['k_99_percent']} / {modulus}")
    logger.info(f"Mass in top 20 freqs: {sparsity['total_mass_top_k']:.3f}")

    # Progress measures
    phases = compute_progress_measures(history, fourier_result, modulus)
    logger.info(f"Phase boundaries: {phases}")

    # Ablation sweep
    logger.info("=" * 60)
    logger.info("Causal Ablation in Fourier Space")
    logger.info("=" * 60)
    ablation_result = run_ablation_sweep(model, val_loader, fourier_result, modulus)

    # Plot everything
    plot_grokking_curve(
        history,
        save_path=FIGURES_DIR / "exp2_grokking_curve.png",
        phase_boundaries=phases,
    )
    plot_fourier_weights(
        fourier_result,
        modulus=modulus,
        save_path=FIGURES_DIR / "exp2_fourier_weights.png",
    )
    plot_ablation_curve(
        ablation_result,
        modulus=modulus,
        save_path=FIGURES_DIR / "exp2_frequency_ablation.png",
    )

    plot_progress_measures(
        history,
        save_path=FIGURES_DIR / "exp2_progress_measures.png",
    )

    if args.save_model:
        model_path = FIGURES_DIR / "exp2_trained_model.pt"
        torch.save(model.state_dict(), model_path)
        logger.info(f"Saved trained model to {model_path}")

    # Summary
    logger.info("=" * 60)
    logger.info("GROKKING EXPERIMENT COMPLETE")
    logger.info("=" * 60)
    final_val_acc = history["val_acc"][-1]
    grokking_step = next(
        (i for i, acc in enumerate(history["val_acc"]) if acc > 0.9), -1
    )
    logger.info(f"Final validation accuracy: {final_val_acc:.4f}")
    logger.info(f"Generalization achieved at epoch: {grokking_step}")
    logger.info(
        f"Fourier frequencies used: {sparsity['k_99_percent']} / {modulus} "
        f"({sparsity['k_99_percent']/modulus:.1%})"
    )
    if sparsity["k_99_percent"] < modulus * 0.5:
        logger.info("✓ CONFIRMED: Model uses sparse Fourier representation")
    else:
        logger.warning(
            "Fourier representation is dense. "
            "Try increasing weight decay or training longer."
        )


if __name__ == "__main__":
    main()
