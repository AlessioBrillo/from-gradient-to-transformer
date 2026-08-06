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
from typing import Callable, Optional

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

# A duplicate token inside the prefix makes "attend to the position after
# the *first* occurrence of the current token" genuinely ambiguous (several
# prior occurrences, possibly different correct next tokens) — an ill-posed
# instance of the task, not a scale limit on the model. Warn above this
# collision probability; see prefix_duplicate_probability() and
# 06_production_ai/exercises/ex-03-induction-task-design.md.
PREFIX_AMBIGUITY_WARN_THRESHOLD = 0.3


def prefix_duplicate_probability(vocab_size: int, prefix_len: int) -> float:
    """Birthday-problem approximation: probability that a length-`prefix_len`
    prefix drawn uniformly at random from `vocab_size` tokens contains at
    least one repeated token.

    P(no collision) ~= exp(-k(k-1) / (2n)) for k draws from n items
    (the standard birthday-paradox approximation), so
    P(collision) ~= 1 - exp(-k(k-1) / (2n)).
    """
    if prefix_len < 2:
        return 0.0
    k, n = prefix_len, vocab_size
    exponent = -(k * (k - 1)) / (2.0 * n)
    return float(1.0 - np.exp(exponent))


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

    This requires the prefix to have no repeated tokens — a duplicate inside
    the prefix means "the previous occurrence of the current token" is not
    unique, so there may be several candidate positions to attend to with
    different correct next tokens. `PREFIX_AMBIGUITY_WARN_THRESHOLD` and
    `prefix_duplicate_probability()` make this checkable instead of silently
    assumed; the pre-2026-08-02 defaults (vocab_size=32, prefix_len=32; or
    vocab_size=16, prefix_len=12 in `--quick`) both landed at ~98-100%
    collision probability — the task was ill-posed at nearly every position,
    independent of model scale or training budget.

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
    prefix_len = max(2, int(seq_len * prefix_ratio))
    collision_p = prefix_duplicate_probability(vocab_size, prefix_len)
    if collision_p > PREFIX_AMBIGUITY_WARN_THRESHOLD:
        logger.warning(
            f"Prefix ambiguity: a {prefix_len}-token prefix drawn from a "
            f"{vocab_size}-token vocabulary has a {collision_p:.1%} chance "
            "of containing a repeated token, making the induction task "
            "ill-posed at those positions (multiple valid 'previous "
            "occurrences' with different correct next tokens). Increase "
            "vocab_size or shorten the prefix to bring this below "
            f"{PREFIX_AMBIGUITY_WARN_THRESHOLD:.0%}."
        )

    rng = np.random.default_rng(seed)

    def _generate(n: int) -> torch.Tensor:
        sequences = []
        for _ in range(n):
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

        # Optional per-head ablation mask: shape (n_heads,), 1.0 = keep,
        # 0.0 = ablate. Applied to each head's output *before* W_O mixes the
        # heads together, so a zeroed head is actually a zeroed head — not an
        # arbitrary post-mixing subspace. See causal_ablation().
        self.head_mask: Optional[torch.Tensor] = None

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
        if self.head_mask is not None:
            head_mask = self.head_mask.view(1, self.n_heads, 1, 1).to(out.device, out.dtype)
            out = out * head_mask
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
    """Compute per-layer attention entropy and diagonal+1 mass.

    `diag1_mass` reports, per layer, the **max over heads** of the diagonal+1
    attention mass — the strength of the single most induction-like head in
    that layer. This is on the same [0, 1] scale as the per-head 0.3 detection
    threshold used in `analyze_induction_heads`, so the two are directly
    comparable (e.g. on the training-curve plot's threshold line).

    Earlier versions summed diag1 mass across heads instead of taking the max,
    which put this metric on a [0, n_heads] scale. That made the training
    curve look like induction heads were forming (aggregate approaching 1.0)
    even when no individual head crossed the 0.3 per-head threshold — the
    2026-07-26 audit's "diag+1 mass ~1.0 but 0 heads detected" discrepancy.
    """
    model.eval()
    n_layers = len(model.blocks)

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
                diag1 = probs[:, :, 1:, :-1].diagonal(dim1=-2, dim2=-1)
                # Per-head mass, then the strongest head wins — not a sum.
                total_diag1[l] += diag1.mean(dim=(0, -1)).max().item()
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
    fresh_batches_fn: Optional[Callable[[int], DataLoader]] = None,
) -> dict:
    """Train the model and return training curves.

    `fresh_batches_fn`, if given, is called once per epoch with the epoch
    index and must return a fresh `DataLoader` sampled from a new set of
    sequences — used to test whether a fixed, epoch-reused dataset lets the
    model memorize specific sequences rather than learn the general
    prefix-matching-and-copying rule (Olsson et al. resample continuously;
    the pre-2026-08-02 version reused one fixed dataset, reshuffled, for the
    entire run). When `None`, `train_loader` is reused every epoch as
    before.
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
        epoch_loader = fresh_batches_fn(epoch) if fresh_batches_fn is not None else train_loader

        model.train()
        epoch_loss = 0.0
        for x, y in epoch_loader:
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
        train_loss = epoch_loss / len(epoch_loader.dataset)
        val_loss, val_acc = evaluate(model, val_loader)

        # Attention metrics every 50 epochs
        if (epoch + 1) % 50 == 0:
            attn_metrics = compute_attention_entropy(model, val_loader)
            attn_entropy = sum(attn_metrics["entropy"])
            # Max over layers too, so this stays comparable to the single
            # per-head 0.3 detection threshold plotted alongside it.
            diag1_mass = max(attn_metrics["diag1_mass"])
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


def k_composition_scores(p0: torch.Tensor, p1: torch.Tensor) -> np.ndarray:
    """K-composition scores between a layer-0 head set and a layer-1 head set.

    Nanda & Jacobsen (2023), "Attention as a Step Towards the Emergence of
    the Induction Head", Step 2: in K-composition, the layer-1 head attends
    from query position q to `prev(q) + 1`, where `prev(q)` is the position
    the layer-0 duplicate-token head attended to at q (the previous
    occurrence of the current token) and +1 is the position holding the
    token to copy. The induction head is the composition of Step 1 (L0
    duplicate head) and Step 2 (L1 K-composition).

    Returns a (n_heads_0, n_heads_1) matrix: row h0's `prev` combined with
    column h1's attention.

    Self-attention guard: queries where `prev(q) + 1 == q` are excluded —
    a head attending to itself would trivially score 1.0 on a shift-by-one
    prev pattern without being an induction head at all. This makes the
    detector falsifiable (see TestKComposition).
    """
    B, H0, S, _ = p0.shape
    H1 = p1.shape[1]
    if B == 0 or S == 0:
        return np.zeros((H0, H1))

    prev = p0.argmax(dim=-1)  # (B, H0, S): position L0 head h0 attended to at q
    target = prev + 1  # (B, H0, S): position one token after it
    qs = torch.arange(S, device=p0.device)
    # Gate: in-bounds, and the L0 head must actually point at a *different*
    # position than q — a head attending to itself is not a previous-
    # occurrence signal, and a head attending to q-1 (prev+1 == q) is plain
    # self-attention, not induction.
    valid = (target < S) & (prev != qs) & (target != qs)

    scores = np.zeros((H0, H1))
    for h0 in range(H0):
        idx = target[:, h0].clamp(max=S - 1)  # (B, S); OOB entries masked below
        idx_gather = idx.unsqueeze(1).unsqueeze(-1).expand(B, H1, S, S)
        vals = torch.gather(p1, -1, idx_gather)  # (B, H1, S, S)
        diag = vals.diagonal(dim1=-2, dim2=-1)  # (B, H1, S): vals[b, h1, q, q]
        mask = valid[:, h0]  # (B, S)
        n_valid = int(mask.sum())
        if n_valid:
            masked = diag * mask[:, None, :].to(diag.dtype)  # (B, H1, S)
            scores[h0] = masked.sum(dim=(0, 2)).numpy() / max(n_valid, 1)
    return scores


def diagnose_induction_formation(all_patterns: list) -> dict:
    """The "how far did the model get" instrument for the two-step path
    (Nanda & Jacobsen 2023). Given collected per-layer attention patterns
    (list of (B, n_heads, S, S) tensors, one per layer), reports:

    - Step 1: per-head diag+1 mass in layer 0 (duplicate-token head);
    - Step 2: the K-composition matrix between layer-0 and layer-1 heads
      and its best (h0, h1) pair;
    - peakedness of the L0 argmax: whether `prev` is a real, focused choice
      (a diffuse L0 head would make any K-composition number uninterpretable).

    A confirmed induction head needs both steps high; a high Step 2 with a
    low Step 1 is not "almost an induction head", it is a misread.
    """
    if len(all_patterns) < 2:
        return {
            "step1_l0_duplicate_mass": [],
            "l0_peakedness": 0.0,
            "step2_k_composition": 0.0,
            "best_l0_head": -1,
            "best_l1_head": -1,
        }
    p0 = all_patterns[0]
    p1 = all_patterns[1]

    diag0 = p0[:, :, 1:, :-1].diagonal(dim1=-2, dim2=-1).mean(dim=(0, -1))
    peakedness = p0.max(dim=-1).values.mean(dim=(0, 2))

    comp = k_composition_scores(p0, p1)
    if comp.size == 0:
        best = 0.0
        best_pair = (-1, -1)
    else:
        flat_idx = int(np.argmax(comp))
        best = float(comp.flat[flat_idx])
        best_pair = (flat_idx // comp.shape[1], flat_idx % comp.shape[1])

    return {
        "step1_l0_duplicate_mass": diag0.tolist(),
        "l0_peakedness": float(peakedness.max()),
        "step2_k_composition": best,
        "best_l0_head": best_pair[0],
        "best_l1_head": best_pair[1],
    }


def plot_composition_diagnostic(
    all_patterns: list, diagnosis: dict, save_path: Path
) -> None:
    """Two-panel figure: the best L0 duplicate head's attention (Step 1) and
    the best L1 head's attention with the K-composition `prev(q)+1` curve
    overlaid (Step 2) — the visual "how far" answer."""
    if len(all_patterns) < 2 or diagnosis["best_l0_head"] < 0:
        return
    h0, h1 = diagnosis["best_l0_head"], diagnosis["best_l1_head"]
    p0 = all_patterns[0][0, h0].numpy()
    p1 = all_patterns[1][0, h1].numpy()
    S = p0.shape[-1]
    prev_curve = np.argmax(p0, axis=-1) + 1
    prev_curve[prev_curve >= S] = S - 1

    fig, axes = plt.subplots(1, 2, figsize=(14, 7))
    for ax, pat, title in (
        (axes[0], p0, f"L0 head {h0} — duplicate-token head (Step 1)"),
        (axes[1], p1, f"L1 head {h1} — attention vs prev+1 curve (Step 2)"),
    ):
        im = ax.imshow(pat, cmap="Blues", aspect="equal")
        ax.set_title(title, fontsize=12)
        ax.set_xlabel("Key Position")
        ax.set_ylabel("Query Position")
        fig.colorbar(im, ax=ax, shrink=0.8)
    axes[1].plot(prev_curve, np.arange(S), color="red", ls="--", lw=1.2,
                 label="prev(q) + 1 (K-composition target)")
    axes[1].legend(fontsize=9)
    axes[0].set_title(
        f"L0 head {h0} — duplicate-token head (Step 1)\n"
        f"diag+1 mass: {diagnosis['step1_l0_duplicate_mass'][h0]:.3f}",
        fontsize=12,
    )
    axes[1].set_title(
        f"L1 head {h1} — K-composition (Step 2)\n"
        f"score: {diagnosis['step2_k_composition']:.3f}",
        fontsize=12,
    )
    fig.tight_layout()
    fig.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    logger.info(f"Saved composition diagnostic to {save_path}")


def _make_fresh_batches_fn(
    args: argparse.Namespace, seed: int
) -> Callable[[int], DataLoader]:
    """Build a per-epoch DataLoader factory: a fresh set of sequences every
    epoch instead of one fixed set reshuffled — see train_model()'s
    fresh_batches_fn docstring."""

    def fn(epoch: int) -> DataLoader:
        dataset, _ = make_repeated_token_data(
            vocab_size=args.vocab_size,
            seq_len=args.seq_len,
            num_train=args.num_train,
            num_val=1,
            seed=seed * 1_000_003 + epoch + 1,
        )
        return DataLoader(dataset, batch_size=args.batch_size, shuffle=True)

    return fn


def causal_ablation(
    model: nn.Module, loader: DataLoader, layer: int, head: int
) -> float:
    """Ablate a specific attention head by zeroing its contribution.

    Measures the accuracy drop when a head's contribution is removed,
    which causally confirms its role in the circuit.

    Uses `AttentionOnlyBlock.head_mask`, which zeroes the head's output
    *before* W_O mixes all heads together (see forward()). The previous
    version hooked `W_O`'s output and sliced it into `n_heads` chunks — but
    W_O's output is a d_model vector that has already mixed every head, so
    that zeroed an arbitrary residual-stream subspace, not a specific head.
    This mirrors the (correct) approach in exp4_circuit_patching.py.

    Returns:
        Accuracy after head ablation.
    """
    model.eval()
    block = model.blocks[layer]
    mask = torch.ones(block.n_heads)
    mask[head] = 0.0
    block.head_mask = mask

    correct = 0
    total = 0
    with torch.no_grad():
        for x, y in loader:
            x, y = x.to(DEVICE), y.to(DEVICE)
            logits, _ = model(x, record_attn=False)
            preds = logits.argmax(dim=-1)
            correct += (preds == y).sum().item()
            total += y.numel()

    block.head_mask = None
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
# Multi-seed headline run
# ---------------------------------------------------------------------------
def run_single_seed(seed: int, args: argparse.Namespace) -> dict[str, float]:
    """Train one induction-heads run end-to-end and return headline metrics
    for one seed. Mirrors main()'s single-seed data/model/train/analysis
    steps, minus plotting and model-saving — used by `--seeds` to aggregate
    across seeds via `src.experiments.runner.run_seeds`.
    """
    train_dataset, val_dataset = make_repeated_token_data(
        vocab_size=args.vocab_size,
        seq_len=args.seq_len,
        num_train=args.num_train,
        num_val=1024,
        seed=seed,
    )
    train_loader = DataLoader(train_dataset, batch_size=args.batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=args.batch_size, shuffle=False)

    model = AttentionOnlyTransformer(
        vocab_size=args.vocab_size,
        d_model=args.d_model,
        n_layers=args.n_layers,
        n_heads=args.n_heads,
        max_seq_len=args.seq_len,
    )

    fresh_batches_fn = _make_fresh_batches_fn(args, seed) if args.fresh_batches else None

    history = train_model(
        model=model,
        train_loader=train_loader,
        val_loader=val_loader,
        epochs=args.epochs,
        lr=args.lr,
        weight_decay=args.weight_decay,
        seed=seed,
        use_wandb=False,
        fresh_batches_fn=fresh_batches_fn,
    )

    induction_heads, all_patterns = analyze_induction_heads(model, val_loader)
    total_induction = sum(len(h) for h in induction_heads)
    peak_diag1 = float(np.max(history["diag1_mass"])) if history["diag1_mass"] else 0.0
    diagnosis = diagnose_induction_formation(all_patterns)

    drops = []
    for layer_idx, heads in enumerate(induction_heads):
        for head_idx in heads:
            ablated_acc = causal_ablation(model, val_loader, layer_idx, head_idx)
            drops.append(history["val_acc"][-1] - ablated_acc)
    mean_ablation_drop = float(np.mean(drops)) if drops else 0.0

    return {
        "final_val_acc": float(history["val_acc"][-1]),
        "total_induction_heads": float(total_induction),
        "peak_diag1_mass": peak_diag1,
        "mean_ablation_drop": mean_ablation_drop,
        "k_composition_score": float(diagnosis["step2_k_composition"]),
        "l0_duplicate_head_mass": float(
            max(diagnosis["step1_l0_duplicate_mass"] or [0.0])
        ),
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    FIGURES_DIR.mkdir(exist_ok=True)
    parser = argparse.ArgumentParser(
        description="Rung 1: Induction heads in a 2-layer attention-only transformer"
    )
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument(
        "--vocab-size",
        type=int,
        default=2048,
        help=(
            "Vocabulary size. Default raised from 32 (2026-08-02): with the "
            "default seq-len/prefix-ratio (prefix_len=32), vocab_size=32 gave "
            "a ~100%% chance of a repeated token inside the prefix, making "
            "the induction task ill-posed at most positions independent of "
            "model scale. See prefix_duplicate_probability()."
        ),
    )
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
        "--standard",
        action="store_true",
        help=(
            "Canonical standard-scale config (Micro-Phase 10 pinning): "
            "vocab_size=2048, seq_len=64, d_model=64, 2 layers, 4 heads, "
            "fresh-batches on, epochs=3000, num_train=8192. The single "
            "config Rungs 1/4/5 must share so the cascade measures one "
            "model, not three similar ones."
        ),
    )
    parser.add_argument(
        "--wandb", action="store_true", help="Log metrics to Weights & Biases"
    )
    parser.add_argument(
        "--save-model", action="store_true", help="Save trained model"
    )
    parser.add_argument(
        "--fresh-batches",
        action="store_true",
        help=(
            "Resample a fresh set of training sequences every epoch instead "
            "of reusing one fixed set (reshuffled). Tests whether the fixed "
            "dataset lets the model memorize specific sequences rather than "
            "learn prefix-matching-and-copying (Olsson et al. resample "
            "continuously)."
        ),
    )
    parser.add_argument(
        "--seeds",
        type=str,
        default=None,
        help=(
            "Comma-separated seeds (e.g. '0,1,2'). If set, runs the full "
            "train+analysis pipeline once per seed, saves a "
            "results/exp1_induction_heads.json manifest, and skips "
            "plotting/model-saving."
        ),
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )

    if args.quick:
        args.vocab_size = 256
        args.seq_len = 24
        args.d_model = 32
        args.n_layers = 2
        args.n_heads = 4
        args.epochs = 500
        args.num_train = 1024
        args.batch_size = 32
        logger.info("QUICK MODE: reduced config for fast iteration")

    if args.standard:
        args.vocab_size = 2048
        args.seq_len = 64
        args.d_model = 64
        args.n_layers = 2
        args.n_heads = 4
        args.epochs = 3000
        args.num_train = 8192
        args.batch_size = 64
        args.fresh_batches = True
        logger.info(
            "STANDARD MODE: canonical standard-scale config "
            "(vocab=2048, seq=64, d_model=64, fresh-batches, epochs=3000)"
        )

    logger.info(f"Device: {DEVICE}")
    logger.info(f"Arguments: {vars(args)}")

    set_seed(args.seed)

    if args.seeds:
        seeds = parse_seeds(args.seeds)
        logger.info(
            f"MULTI-SEED MODE: {len(seeds)} seeds {seeds} "
            f"(fresh_batches={args.fresh_batches}, skipping plots/model-save)"
        )
        result = run_seeds(lambda s: run_single_seed(s, args), seeds)
        probe_model = AttentionOnlyTransformer(
            vocab_size=args.vocab_size,
            d_model=args.d_model,
            n_layers=args.n_layers,
            n_heads=args.n_heads,
            max_seq_len=args.seq_len,
        )
        manifest = ResultsManifest.from_run(
            experiment="exp1_induction_heads",
            seeds=seeds,
            args={k: v for k, v in vars(args).items() if k != "seeds"},
            per_seed_metrics=result.per_seed,
            aggregate=result.aggregate,
            wall_clock_seconds=result.wall_clock_seconds,
            device=str(DEVICE),
            n_parameters=count_parameters(probe_model),
        )
        manifest_path = Path("results") / "exp1_induction_heads.json"
        manifest.save(manifest_path)
        logger.info(f"Saved multi-seed manifest to {manifest_path}")
        for key in result.aggregate:
            logger.info(f"  {key}: {result.summary_line(key)}")
        return

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
        fresh_batches_fn = (
            _make_fresh_batches_fn(args, args.seed) if args.fresh_batches else None
        )

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
            fresh_batches_fn=fresh_batches_fn,
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
                f"Peak smoothed val acc: {val_smooth[max_smooth_idx]:.4f} "
                f"at epoch ~{max_smooth_idx * 10}"
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

    # K-composition diagnostic (Nanda & Jacobsen): the "how far did the model
    # get" instrument — Step 1 (L0 duplicate-token head) and Step 2
    # (K-composition) are reported independently so a missing induction head
    # is measured, not just counted.
    diagnosis = diagnose_induction_formation(all_patterns)
    if diagnosis["best_l0_head"] >= 0:
        step1 = max(diagnosis["step1_l0_duplicate_mass"])
        logger.info("-" * 60)
        logger.info("How far did the model get? (Nanda & Jacobsen two-step path)")
        logger.info(
            f"Step 1 — L0 duplicate-token head: max diag+1 mass {step1:.3f} "
            f"(peakedness {diagnosis['l0_peakedness']:.3f})"
        )
        logger.info(
            f"Step 2 — K-composition: best score {diagnosis['step2_k_composition']:.3f} "
            f"(L0 head {diagnosis['best_l0_head']}, L1 head {diagnosis['best_l1_head']})"
        )
        plot_composition_diagnostic(
            all_patterns, diagnosis, FIGURES_DIR / "exp1_k_composition.png"
        )

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
