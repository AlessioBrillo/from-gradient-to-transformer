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
    prefix_ratio: float = 0.5,
    seed: int = 42,
) -> tuple[TensorDataset, TensorDataset]:
    """Generate sequences with repeated prefix to induce induction heads.

    Canonical setup (Olsson et al., 2022):
    Each sequence is [A_0, A_1, ..., A_k, A_0, A_1, ..., A_k, ...] where the
    first half (prefix) is a random sequence and the second half repeats it.
    This creates the pattern: [A][B]...[A] -> the model should predict [B]
    after the second [A], which is the induction head signature.

    For next-token prediction, at position k (where A_0 reappears), the correct
    next token is A_1 (what followed A_0 the first time). An induction head
    solves this by attending from position k to position 0 (matching A_0 with A_0)
    and copying A_1 from position 1.

    Args:
        vocab_size: Size of vocabulary.
        seq_len: Total sequence length.
        num_train: Number of training samples.
        num_val: Number of validation samples.
        prefix_ratio: Fraction of sequence that is the unique prefix.
        seed: Random seed.

    Returns:
        Tuple of (train_dataset, val_dataset) where each sample is
        (input_ids, target_ids) shaped (seq_len-1,).
    """
    rng = np.random.default_rng(seed)

    def _generate(n: int) -> torch.Tensor:
        sequences = []
        for _ in range(n):
            prefix_len = max(2, int(seq_len * prefix_ratio))
            # Random prefix: the unique tokens
            prefix = rng.integers(0, vocab_size, size=prefix_len).tolist()
            # Repeat the prefix to fill the rest of the sequence
            tokens = prefix.copy()
            while len(tokens) < seq_len:
                tokens.append(tokens[len(tokens) % prefix_len])
            sequences.append(tokens[:seq_len])
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


def compute_attention_entropy(
    model: nn.Module, loader: DataLoader
) -> dict:
    """Compute per-layer attention entropy and diagonal+1 mass."""
    model.eval()
    n_layers = len(model.blocks)
    n_heads = model.blocks[0].n_heads

    total_entropy = [0.0 for _ in range(n_layers)]
    total_diag1 = [0.0 for _ in range(n_layers)]
    total_batches = 0
    sample_size = 0

    with torch.no_grad():
        for x, _ in loader:
            x = x.to(DEVICE)
            _, attn_records = model(x, record_attn=True)
            if attn_records is None:
                break
            for l, probs in enumerate(attn_records):
                ent = -(probs * (probs + 1e-8).log()).sum(-1)
                total_entropy[l] += ent.mean(dim=(0, 2)).sum().item()
                S = probs.shape[-1]
                diag1 = probs[:, :, 1:, :-1].diagonal(dim1=-2, dim2=-1)
                total_diag1[l] += diag1.mean(dim=(0, -1)).sum().item()
            total_batches += 1
            sample_size += 1
            if sample_size >= 4:
                break

    if total_batches == 0:
        return {"entropy": [0.0], "diag1_mass": [0.0]}
    return {
        "entropy": [e / total_batches for e in total_entropy],
        "diag1_mass": [d / total_batches for d in total_diag1],
    }


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
    """Train the model and return training curves."""
    set_seed(seed)
    model = model.to(DEVICE)

    _wandb = None
    if use_wandb:
        try:
            import wandb as _wandb
            _wandb.init(
                project="from-gradient-to-transformer",
                config={
                    "model": "AttentionOnlyTransformer",
                    "vocab_size": model.embed.num_embeddings,
                    "d_model": model.embed.embedding_dim,
                    "n_layers": len(model.blocks),
                    "n_heads": model.blocks[0].n_heads,
                    "lr": lr,
                    "weight_decay": weight_decay,
                    "epochs": epochs,
                    "seed": seed,
                },
            )
        except Exception as e:
            logger.warning(f"W&B init failed: {e}")
            _wandb = None

    optimizer = torch.optim.AdamW(
        model.parameters(), lr=lr, weight_decay=weight_decay
    )
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
        optimizer, T_max=epochs
    )
    criterion = nn.CrossEntropyLoss()

    history = {
        "train_loss": [], "val_loss": [], "val_acc": [],
        "attn_entropy": [], "diag1_mass": [],
    }

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

        # Attention metrics every 50 epochs
        if (epoch + 1) % 50 == 0:
            attn_metrics = compute_attention_entropy(model, val_loader)
            attn_entropy = sum(attn_metrics["entropy"])
            diag1_mass = sum(attn_metrics["diag1_mass"])
        else:
            attn_entropy = history["attn_entropy"][-1] if history["attn_entropy"] else 0.0
            diag1_mass = history["diag1_mass"][-1] if history["diag1_mass"] else 0.0

        history["train_loss"].append(train_loss)
        history["val_loss"].append(val_loss)
        history["val_acc"].append(val_acc)
        history["attn_entropy"].append(attn_entropy)
        history["diag1_mass"].append(diag1_mass)

        if _wandb is not None:
            _wandb.log({
                "train/loss": train_loss,
                "val/loss": val_loss,
                "val/acc": val_acc,
                "metrics/attn_entropy": attn_entropy,
                "metrics/diag1_mass": diag1_mass,
                "lr": scheduler.get_last_lr()[0],
            }, step=epoch)

        if (epoch + 1) % 50 == 0:
            logger.info(
                f"Epoch {epoch+1:4d} | train loss: {train_loss:.4f} | "
                f"val loss: {val_loss:.4f} | val acc: {val_acc:.4f} | "
                f"attn entropy: {attn_entropy:.2f} | diag+1: {diag1_mass:.3f}"
            )

    if _wandb is not None:
        _wandb.finish()
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
        attention pattern is a list of numpy arrays per layer.
    """
    model.eval()
    n_layers = len(model.blocks)
    per_layer_patterns: list[list] = [[] for _ in range(n_layers)]

    with torch.no_grad():
        for x, _ in loader:
            x = x.to(DEVICE)
            _, attn_records = model(x, record_attn=True)
            if attn_records is not None:
                for layer_idx, pattern in enumerate(attn_records):
                    per_layer_patterns[layer_idx].append(pattern.cpu())
            if sum(len(p) for p in per_layer_patterns) >= 32 * n_layers:
                break

    induction_heads_by_layer = []
    all_patterns = []
    for layer_idx, patterns in enumerate(per_layer_patterns):
        if not patterns:
            induction_heads_by_layer.append([])
            all_patterns.append([])
            continue

        # Concatenate all batches for this layer: (B_total, n_heads, S, S)
        cat = torch.cat(patterns, dim=0)
        all_patterns.append(cat)
        B, n_heads, S, _ = cat.shape

        # Diagonal+1 mass: average over all positions and batches
        diag = cat[:, :, 1:, :-1].diagonal(dim1=-2, dim2=-1).mean(dim=(0, -1))

        threshold = 0.3
        induction_heads = (diag > threshold).nonzero(as_tuple=True)[0].tolist()
        induction_heads_by_layer.append(induction_heads)

    return induction_heads_by_layer, all_patterns


def causal_ablation(
    model: nn.Module, loader: DataLoader, layer: int, head: int
) -> float:
    """Ablate a specific attention head by zeroing its output.

    Measures the accuracy drop when a head's contribution is removed,
    which causally confirms its role in the circuit.

    Returns:
        Accuracy after head ablation.
    """
    model.eval()

    def _zero_head_hook(
        module: nn.Module, input: torch.Tensor, output: torch.Tensor
    ) -> torch.Tensor:
        B, S, D = output.shape
        d_head = D // model.blocks[layer].n_heads
        output_view = output.view(B, S, model.blocks[layer].n_heads, d_head)
        output_view[:, :, head, :] = 0.0
        return output_view.view(B, S, D)

    block = model.blocks[layer]
    hook = block.W_O.register_forward_hook(_zero_head_hook)

    correct = 0
    total = 0
    with torch.no_grad():
        for x, y in loader:
            x, y = x.to(DEVICE), y.to(DEVICE)
            logits, _ = model(x, record_attn=False)
            preds = logits.argmax(dim=-1)
            correct += (preds == y).sum().item()
            total += y.numel()

    hook.remove()
    return correct / total


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
    """Plot training + attention metrics."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    epochs = range(1, len(history["train_loss"]) + 1)

    axes[0, 0].plot(epochs, history["train_loss"], label="Train Loss", alpha=0.8)
    axes[0, 0].plot(epochs, history["val_loss"], label="Val Loss", alpha=0.8)
    axes[0, 0].set_xlabel("Epoch")
    axes[0, 0].set_ylabel("Loss")
    axes[0, 0].set_title("Loss Curves", fontsize=13)
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)

    axes[0, 1].plot(epochs, history["val_acc"], label="Val Accuracy", color="green")
    axes[0, 1].set_xlabel("Epoch")
    axes[0, 1].set_ylabel("Accuracy")
    axes[0, 1].set_title("Validation Accuracy", fontsize=13)
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)

    axes[1, 0].plot(epochs, history["attn_entropy"], label="Attn Entropy", color="purple")
    axes[1, 0].set_xlabel("Epoch")
    axes[1, 0].set_ylabel("Entropy (nats)")
    axes[1, 0].set_title("Attention Entropy (lower = more focused)", fontsize=13)
    axes[1, 0].grid(True, alpha=0.3)

    axes[1, 1].plot(epochs, history["diag1_mass"], label="Diag+1 Mass", color="orange")
    axes[1, 1].set_xlabel("Epoch")
    axes[1, 1].set_ylabel("Diagonal+1 mass")
    axes[1, 1].set_title("Induction Head Signal (diag+1)", fontsize=13)
    axes[1, 1].axhline(y=0.3, color="red", linestyle="--", alpha=0.3, label="Detection threshold")
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)

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
    parser.add_argument("--epochs", type=int, default=5000, help="Training epochs")
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
    parser.add_argument(
        "--quick", action="store_true", help="Quick test (reduced config)"
    )
    parser.add_argument(
        "--wandb", action="store_true", help="Log metrics to Weights & Biases"
    )
    parser.add_argument(
        "--save-model", action="store_true", help="Save trained model"
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )

    if args.quick:
        args.vocab_size = 16
        args.seq_len = 24
        args.d_model = 32
        args.n_layers = 2
        args.n_heads = 4
        args.epochs = 500
        args.num_train = 1024
        args.batch_size = 32
        logger.info("QUICK MODE: reduced config for fast iteration")

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
            use_wandb=args.wandb,
        )

        # Plot training curves
        plot_training_curves(
            history,
            save_path=FIGURES_DIR / "exp1_training_bump.png",
        )

        if args.save_model:
            model_path = FIGURES_DIR / "exp1_trained_model.pt"
            torch.save(model.state_dict(), model_path)
            logger.info(f"Saved model to {model_path}")

        # Loss bump detection
        val_accs = np.array(history["val_acc"])
        diag1_mass = np.array(history["diag1_mass"])
        if len(val_accs) > 100:
            val_smooth = np.convolve(val_accs, np.ones(10)/10, mode='valid')
            max_smooth_idx = np.argmax(val_smooth)
            loss_bump_idx = np.argmax(np.abs(np.diff(history["val_loss"])))
            logger.info(
                f"Loss bump at epoch ~{loss_bump_idx} | "
                f"Peak smoothed val acc: {val_smooth[max_smooth_idx]:.4f} at epoch ~{max_smooth_idx*10}"
            )
        if len(diag1_mass) > 100:
            peak_diag1 = np.argmax(diag1_mass)
            diag1_at_end = diag1_mass[-1]
            logger.info(
                f"Peak diag+1 mass at epoch {peak_diag1} (value: {diag1_mass[peak_diag1]:.3f}) | "
                f"Final diag+1 mass: {diag1_at_end:.3f}"
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
            "or lower threshold in detection."
        )
    else:
        logger.info("✓ Induction heads successfully identified!")
        logger.info("Running causal ablation to verify...")

        # Ablate each detected induction head and measure accuracy drop
        for layer_idx, heads in enumerate(induction_heads):
            for head_idx in heads:
                full_acc = history["val_acc"][-1] if not args.no_train else 0.0
                ablated_acc = causal_ablation(
                    model, val_loader, layer_idx, head_idx
                )
                logger.info(
                    f"Ablation L{layer_idx}H{head_idx}: "
                    f"accuracy {full_acc:.4f} → {ablated_acc:.4f} "
                    f"(drop: {full_acc - ablated_acc:+.4f})"
                )


if __name__ == "__main__":
    main()
