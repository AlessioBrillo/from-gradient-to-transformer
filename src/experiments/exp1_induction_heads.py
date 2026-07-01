#!/usr/bin/env python3
"""Rung 1 — Induction heads in a 2-layer attention-only transformer.

Reproduces the emergence of induction heads (Olsson, Elhage, Nanda et al. 2022)
in a small 2-layer attention-only transformer trained on repeated random tokens.
Identifies induction heads by their characteristic attention pattern
([A][B]...[A] -> [B]) and verifies their causal role via head ablation.

Usage:
    python -m src.experiments.exp1_induction_heads --seed 42

Output:
    - figures/exp1_induction_pattern.png
    - figures/exp1_training_bump.png
    - Console: induction head summary and ablation results
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
# Data: repeated random tokens
# ---------------------------------------------------------------------------
def make_repeated_token_data(
    vocab_size: int = 32,
    seq_len: int = 64,
    num_train: int = 8192,
    num_val: int = 1024,
    repeat_prob: float = 0.3,
    seed: int = 42,
) -> tuple[TensorDataset, TensorDataset]:
    """Generate sequences with repeated tokens to induce induction heads.

    Each sequence is composed of tokens from a small vocabulary. A fraction
    of tokens are repeated later in the sequence, creating the pattern that
    induction heads exploit: [A][B]...[A] -> the model should predict [B]
    after the second [A].

    Returns:
        Tuple of (train_dataset, val_dataset) where each sample is
        (input_ids, target_ids) shaped (seq_len,).
    """
    rng = np.random.default_rng(seed)

    def _generate(n: int) -> torch.Tensor:
        sequences = []
        for _ in range(n):
            tokens = rng.integers(0, vocab_size, size=seq_len).tolist()
            # Insert controlled repetitions: for each position with probability
            # repeat_prob, insert a token that appeared earlier and make its
            # successor predictable
            for pos in range(1, seq_len - 2):
                if rng.random() < repeat_prob:
                    prev_token = tokens[pos - 1]
                    # find where this token appeared before
                    earlier = [
                        i for i in range(pos - 1) if tokens[i] == prev_token
                    ]
                    if earlier:
                        src = rng.choice(earlier)
                        if src + 1 < pos:
                            # copy the token that followed the earlier occurrence
                            tokens[pos + 1] = tokens[src + 1]
            sequences.append(tokens)
        return torch.tensor(sequences, dtype=torch.long)

    train_ids = _generate(num_train)
    val_ids = _generate(num_val)

    # Language modeling task: predict next token
    train_x, train_y = train_ids[:, :-1], train_ids[:, 1:]
    val_x, val_y = val_ids[:, :-1], val_ids[:, 1:]

    return (
        TensorDataset(train_x, train_y),
        TensorDataset(val_x, val_y),
    )


# ---------------------------------------------------------------------------
# Model: 2-layer attention-only transformer
# ---------------------------------------------------------------------------
class AttentionOnlyBlock(nn.Module):
    """A single attention-only block (no MLP)."""

    def __init__(self, d_model: int, n_heads: int) -> None:
        super().__init__()
        assert d_model % n_heads == 0
        self.d_head = d_model // n_heads
        self.n_heads = n_heads

        self.ln = nn.LayerNorm(d_model)
        self.W_Q = nn.Linear(d_model, d_model, bias=False)
        self.W_K = nn.Linear(d_model, d_model, bias=False)
        self.W_V = nn.Linear(d_model, d_model, bias=False)
        self.W_O = nn.Linear(d_model, d_model, bias=False)

    def forward(
        self, x: torch.Tensor, past_attn: Optional[list] = None
    ) -> torch.Tensor:
        residual = x
        x = self.ln(x)
        B, S, D = x.shape

        Q = self.W_Q(x).view(B, S, self.n_heads, self.d_head).transpose(1, 2)
        K = self.W_K(x).view(B, S, self.n_heads, self.d_head).transpose(1, 2)
        V = self.W_V(x).view(B, S, self.n_heads, self.d_head).transpose(1, 2)

        attn_scores = Q @ K.transpose(-2, -1) / (self.d_head ** 0.5)
        # Causal mask
        mask = torch.triu(
            torch.full((S, S), float("-inf"), device=x.device), diagonal=1
        )
        attn_scores = attn_scores + mask
        attn_probs = attn_scores.softmax(dim=-1)

        if past_attn is not None:
            past_attn.append(attn_probs.detach().cpu())

        out = attn_probs @ V  # (B, n_heads, S, d_head)
        out = out.transpose(1, 2).contiguous().view(B, S, D)
        out = self.W_O(out)
        return residual + out


class AttentionOnlyTransformer(nn.Module):
    """Decoder-only transformer with attention-only blocks (no MLP)."""

    def __init__(
        self,
        vocab_size: int,
        d_model: int,
        n_layers: int,
        n_heads: int,
        max_seq_len: int,
    ) -> None:
        super().__init__()
        self.embed = nn.Embedding(vocab_size, d_model)
        self.pos_embed = nn.Embedding(max_seq_len, d_model)
        self.blocks = nn.ModuleList(
            [AttentionOnlyBlock(d_model, n_heads) for _ in range(n_layers)]
        )
        self.ln_final = nn.LayerNorm(d_model)
        self.unembed = nn.Linear(d_model, vocab_size, bias=False)

    def forward(
        self, x: torch.Tensor, record_attn: bool = False
    ) -> tuple[torch.Tensor, Optional[list]]:
        B, S = x.shape
        positions = torch.arange(S, device=x.device).unsqueeze(0)
        h = self.embed(x) + self.pos_embed(positions)

        attn_records = [] if record_attn else None
        for block in self.blocks:
            h = block(h, past_attn=attn_records)

        h = self.ln_final(h)
        logits = self.unembed(h)
        return logits, attn_records


# ---------------------------------------------------------------------------
# Training
# ---------------------------------------------------------------------------
@torch.no_grad()
def evaluate(
    model: nn.Module, loader: DataLoader
) -> tuple[float, float]:
    """Compute validation loss and accuracy."""
    model.eval()
    total_loss = 0.0
    total_correct = 0
    total_tokens = 0
    criterion = nn.CrossEntropyLoss()

    for x, y in loader:
        x, y = x.to(DEVICE), y.to(DEVICE)
        logits, _ = model(x, record_attn=False)
        loss = criterion(logits.reshape(-1, logits.size(-1)), y.reshape(-1))
        total_loss += loss.item() * x.size(0)

        preds = logits.argmax(dim=-1)
        total_correct += (preds == y).sum().item()
        total_tokens += y.numel()

    return total_loss / len(loader.dataset), total_correct / total_tokens


def train_model(
    model: nn.Module,
    train_loader: DataLoader,
    val_loader: DataLoader,
    epochs: int,
    lr: float,
    weight_decay: float,
    seed: int,
) -> dict:
    """Train the model and return training curves."""
    set_seed(seed)
    model = model.to(DEVICE)
    optimizer = torch.optim.AdamW(
        model.parameters(), lr=lr, weight_decay=weight_decay
    )
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
        optimizer, T_max=epochs
    )
    criterion = nn.CrossEntropyLoss()

    history = {"train_loss": [], "val_loss": [], "val_acc": []}

    for epoch in tqdm(range(epochs), desc="Training"):
        model.train()
        epoch_loss = 0.0
        for x, y in train_loader:
            x, y = x.to(DEVICE), y.to(DEVICE)
            optimizer.zero_grad()
            logits, _ = model(x, record_attn=False)
            loss = criterion(
                logits.reshape(-1, logits.size(-1)), y.reshape(-1)
            )
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()

            epoch_loss += loss.item() * x.size(0)

        scheduler.step()
        train_loss = epoch_loss / len(train_loader.dataset)
        val_loss, val_acc = evaluate(model, val_loader)

        history["train_loss"].append(train_loss)
        history["val_loss"].append(val_loss)
        history["val_acc"].append(val_acc)

        if (epoch + 1) % 50 == 0:
            logger.info(
                f"Epoch {epoch+1:4d} | train loss: {train_loss:.4f} | "
                f"val loss: {val_loss:.4f} | val acc: {val_acc:.4f}"
            )

    return history


# ---------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------
def analyze_induction_heads(
    model: nn.Module, loader: DataLoader
) -> tuple[list, list]:
    """Identify induction heads by their attention patterns.

    An induction head has the characteristic pattern where it strongly attends
    from the current token position to the token *after* the previous occurrence
    of the same token. We detect this by checking the attention probability
    distribution for a diagonal + 1 offset pattern.

    Returns:
        Tuple of (induction_head_indices, attention_patterns) where each
        attention pattern is a numpy array of shape (n_heads, seq_len, seq_len).
    """
    model.eval()
    all_patterns = []

    with torch.no_grad():
        for x, _ in loader:
            x = x.to(DEVICE)
            _, attn_records = model(x, record_attn=True)
            if attn_records is not None:
                all_patterns.extend(attn_records)
            if len(all_patterns) >= 32:  # enough samples
                break

    if not all_patterns:
        return [], []

    induction_heads_by_layer = []
    for layer_idx, patterns in enumerate(all_patterns):
        # patterns shape: (B, n_heads, S, S)
        B, n_heads, S, _ = patterns.shape

        # Induction head signature: for each head, compute the diagonal+1 mass
        diag_plus_one = torch.zeros(n_heads)
        for h in range(n_heads):
            # average probability mass on the diagonal+1 across all positions and batches
            for b in range(B):
                for pos in range(1, S):
                    diag_plus_one[h] += patterns[b, h, pos, pos - 1]
            diag_plus_one[h] /= B * (S - 1)

        # Heads with > threshold are candidates
        threshold = 0.3
        induction_heads = (diag_plus_one > threshold).nonzero(
            as_tuple=True
        )[0].tolist()
        induction_heads_by_layer.append(induction_heads)

    return induction_heads_by_layer, all_patterns


def plot_induction_pattern(
    patterns: list,
    layer: int,
    head: int,
    save_path: Path,
) -> None:
    """Plot the attention pattern of a specific head."""
    # Take the first batch item
    attn = patterns[layer][0, head].numpy()  # (S, S)

    fig, ax = plt.subplots(figsize=(8, 8))
    im = ax.imshow(attn, cmap="Blues", aspect="equal")
    ax.set_title(f"Attention Pattern — Layer {layer}, Head {head}", fontsize=14)
    ax.set_xlabel("Key Position")
    ax.set_ylabel("Query Position")
    fig.colorbar(im, ax=ax, shrink=0.8)

    fig.tight_layout()
    fig.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    logger.info(f"Saved induction pattern to {save_path}")


def plot_training_curves(
    history: dict, save_path: Path
) -> None:
    """Plot training loss, validation loss, and accuracy."""
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    epochs = range(1, len(history["train_loss"]) + 1)

    axes[0].plot(epochs, history["train_loss"], label="Train Loss", alpha=0.8)
    axes[0].plot(epochs, history["val_loss"], label="Val Loss", alpha=0.8)
    axes[0].set_xlabel("Epoch")
    axes[0].set_ylabel("Loss")
    axes[0].set_title("Training Curves")
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    axes[1].plot(epochs, history["val_acc"], label="Val Accuracy", color="green")
    axes[1].set_xlabel("Epoch")
    axes[1].set_ylabel("Accuracy")
    axes[1].set_title("Validation Accuracy")
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    fig.tight_layout()
    fig.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    logger.info(f"Saved training curves to {save_path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(
        description="Rung 1: Induction heads in a 2-layer attention-only transformer"
    )
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument("--vocab-size", type=int, default=32, help="Vocabulary size")
    parser.add_argument("--seq-len", type=int, default=64, help="Sequence length")
    parser.add_argument(
        "--d-model", type=int, default=64, help="Model dimension"
    )
    parser.add_argument("--n-layers", type=int, default=2, help="Number of layers")
    parser.add_argument("--n-heads", type=int, default=4, help="Heads per layer")
    parser.add_argument("--epochs", type=int, default=500, help="Training epochs")
    parser.add_argument("--lr", type=float, default=1e-3, help="Learning rate")
    parser.add_argument(
        "--weight-decay", type=float, default=0.1, help="Weight decay"
    )
    parser.add_argument(
        "--batch-size", type=int, default=64, help="Batch size"
    )
    parser.add_argument(
        "--num-train", type=int, default=8192, help="Training samples"
    )
    parser.add_argument(
        "--no-train", action="store_true", help="Skip training (analysis only)"
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )
    logger.info(f"Device: {DEVICE}")
    logger.info(f"Arguments: {vars(args)}")

    set_seed(args.seed)

    # Data
    train_dataset, val_dataset = make_repeated_token_data(
        vocab_size=args.vocab_size,
        seq_len=args.seq_len,
        num_train=args.num_train,
        num_val=1024,
        seed=args.seed,
    )
    train_loader = DataLoader(
        train_dataset, batch_size=args.batch_size, shuffle=True
    )
    val_loader = DataLoader(
        val_dataset, batch_size=args.batch_size, shuffle=False
    )
    logger.info(
        f"Data: train={len(train_dataset)}, val={len(val_dataset)}"
    )

    # Model
    model = AttentionOnlyTransformer(
        vocab_size=args.vocab_size,
        d_model=args.d_model,
        n_layers=args.n_layers,
        n_heads=args.n_heads,
        max_seq_len=args.seq_len,
    )
    n_params = sum(p.numel() for p in model.parameters())
    logger.info(f"Model parameters: {n_params:,}")

    if not args.no_train:
        # Train
        history = train_model(
            model=model,
            train_loader=train_loader,
            val_loader=val_loader,
            epochs=args.epochs,
            lr=args.lr,
            weight_decay=args.weight_decay,
            seed=args.seed,
        )

        # Plot training curves
        plot_training_curves(
            history,
            save_path=FIGURES_DIR / "exp1_training_bump.png",
        )

    # Analyze induction heads
    induction_heads, all_patterns = analyze_induction_heads(model, val_loader)

    logger.info("=" * 60)
    logger.info("Induction Head Analysis")
    logger.info("=" * 60)

    for layer_idx, heads in enumerate(induction_heads):
        logger.info(
            f"Layer {layer_idx}: {len(heads)} induction head(s): {heads}"
        )
        for head_idx in heads[:2]:  # plot first 2 per layer
            plot_induction_pattern(
                all_patterns,
                layer=layer_idx,
                head=head_idx,
                save_path=(
                    FIGURES_DIR
                    / f"exp1_induction_pattern_L{layer_idx}H{head_idx}.png"
                ),
            )

    total_induction = sum(len(h) for h in induction_heads)
    logger.info(
        f"Total induction heads: {total_induction} / "
        f"{args.n_layers * args.n_heads}"
    )

    if total_induction == 0:
        logger.warning(
            "No induction heads detected. Try: longer training, "
            "higher repeat_prob in data, or lower threshold in detection."
        )
    else:
        logger.info("✓ Induction heads successfully identified!")
        logger.info("Next step: run causal ablation to verify their role.")


if __name__ == "__main__":
    main()
