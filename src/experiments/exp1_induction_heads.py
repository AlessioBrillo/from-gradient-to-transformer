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
import time
from pathlib import Path
from typing import Callable, Optional

import matplotlib.pyplot as plt
import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset
from tqdm import tqdm

from src.experiments.checkpointing import (
    architecture_metadata,
    checkpoint_path_for_seed,
    load_training_checkpoint,
    save_training_checkpoint,
)
from src.experiments.copy_circuit import (
    candidate_heads,
    classify_mechanism,
    content_triples,
    content_vs_position_attribution,
    mass_covering_heads,
    mass_summary,
)
from src.experiments.induction_detection import (
    COMPOSITION_THRESHOLD,
    INDUCTION_MASS_THRESHOLD,
    attention_patterns_for_inputs,
    collect_patterns_and_tokens,
    detect_from_loader,
    head_masses,
    layer_entropy,
    prefix_length_for,
    run_content_vs_offset_probe,
    run_dissociation_probe,
)

# `k_composition_scores` is re-exported explicitly (the `as` form) because
# exp6 imports it from this module, and mypy's implicit-reexport rule would
# otherwise report it as "not explicitly exported".
from src.experiments.induction_detection import k_composition_scores as k_composition_scores
from src.experiments.induction_tasks import (
    TASK_PERIODIC,
    TASK_VARIABLE,
    TaskSpec,
    copy_mask_for_pairs,
    copy_queries,
    fixed_offset_baseline,
    task_datasets,
)
from src.experiments.runner import parse_seeds, run_seeds
from src.reproducibility import set_seed
from src.results import ResultsManifest, count_parameters, resolve_manifest_path

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

    # The generator itself lives in `src.experiments/induction_tasks`, so the
    # periodic task and the variable-distance task are produced by the same
    # code path and the periodic data stays bit-for-bit what every manifest
    # in this repository was written against.
    spec = TaskSpec.periodic(
        vocab_size=vocab_size, seq_len=seq_len, prefix_ratio=prefix_ratio
    )
    return task_datasets(spec, num_train, num_val, seed)


def default_variable_geometry(seq_len: int) -> tuple[int, int, int]:
    """The variable task's ``(key_len, copy_blocks, copy_block_len)``.

    The standard geometry (seq_len 64) is the one
    [[07_capstone/notes/variable-distance-induction-preregistration]]
    froze: a key of 36 distinct tokens and four blocks of five. Any other
    sequence length gets a geometry that fits, with one filler token per
    gap, so the layout stays well posed.
    """
    if seq_len >= 48:
        return 36, 4, 5
    block_len = 3
    blocks = 2
    key_len = seq_len - blocks * block_len - (blocks + 1)
    return key_len, blocks, block_len


def task_spec_from_args(args: argparse.Namespace) -> TaskSpec:
    """The task a run is about, from its CLI arguments.

    ``--task periodic`` (the default) is the historical ``prefix + prefix``
    layout. ``--task variable`` is the content-based task of ADR-0033, whose
    repeats sit at varying distances and therefore cannot be copied by a
    fixed offset.
    """
    if getattr(args, "task", TASK_PERIODIC) == TASK_VARIABLE:
        key_len, blocks, block_len = default_variable_geometry(args.seq_len)
        return TaskSpec.variable(
            vocab_size=args.vocab_size,
            seq_len=args.seq_len,
            key_len=getattr(args, "key_len", None) or key_len,
            copy_blocks=getattr(args, "copy_blocks", None) or blocks,
            copy_block_len=getattr(args, "copy_block_len", None) or block_len,
        )
    return TaskSpec.periodic(
        vocab_size=args.vocab_size,
        seq_len=args.seq_len,
        prefix_ratio=getattr(args, "prefix_ratio", 0.5),
    )


def make_task_data(
    args: argparse.Namespace,
    num_train: int,
    num_val: int,
    seed: int,
) -> tuple[TensorDataset, TensorDataset]:
    """The training and validation data of the run's task."""
    return task_datasets(task_spec_from_args(args), num_train, num_val, seed)


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
        self,
        x: torch.Tensor,
        past_attn: Optional[list] = None,
        cache: Optional[dict] = None,
        cache_prefix: str = "",
    ) -> torch.Tensor:
        """One attention-only block.

        `cache` records the same tensors the `DecoderOnlyTransformer` records
        (`resid_pre`, `attn.attn_probs`, `attn.V`, `attn.attn_out`,
        `resid_mid`, `resid_post`), so the circuit-patching interventions
        (exp4) can be written once against the cache protocol instead of
        twice against two model families. `resid_mid == resid_post` here
        because there is no MLP branch.
        """
        residual = x
        x = self.ln(x)
        B, S, D = x.shape

        Q = self.W_Q(x).view(B, S, self.n_heads, self.d_head).transpose(1, 2)
        K = self.W_K(x).view(B, S, self.n_heads, self.d_head).transpose(1, 2)
        V = self.W_V(x).view(B, S, self.n_heads, self.d_head).transpose(1, 2)

        attn_scores = Q @ K.transpose(-2, -1) / (self.d_head**0.5)
        # Causal mask
        mask = torch.triu(torch.full((S, S), float("-inf"), device=x.device), diagonal=1)
        attn_scores = attn_scores + mask
        attn_probs = attn_scores.softmax(dim=-1)

        if past_attn is not None:
            past_attn.append(attn_probs.detach().cpu())

        out = attn_probs @ V  # (B, n_heads, S, d_head)
        if self.head_mask is not None:
            head_mask = self.head_mask.view(1, self.n_heads, 1, 1).to(out.device, out.dtype)
            out = out * head_mask
        out = out.transpose(1, 2).contiguous().view(B, S, D)
        attn_out = self.W_O(out)
        block_out = residual + attn_out

        if cache is not None:
            cache[f"{cache_prefix}.resid_pre"] = residual.detach().cpu()
            cache[f"{cache_prefix}.attn.attn_probs"] = attn_probs.detach().cpu()
            cache[f"{cache_prefix}.attn.V"] = V.detach().cpu()
            cache[f"{cache_prefix}.attn.attn_out"] = attn_out.detach().cpu()
            cache[f"{cache_prefix}.resid_mid"] = block_out.detach().cpu()
            cache[f"{cache_prefix}.resid_post"] = block_out.detach().cpu()

        return block_out


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
        self.blocks = nn.ModuleList([AttentionOnlyBlock(d_model, n_heads) for _ in range(n_layers)])
        self.ln_final = nn.LayerNorm(d_model)
        self.unembed = nn.Linear(d_model, vocab_size, bias=False)

    def forward(
        self,
        x: torch.Tensor,
        record_attn: bool = False,
        cache: Optional[dict] = None,
    ) -> tuple[torch.Tensor, Optional[list]]:
        B, S = x.shape
        positions = torch.arange(S, device=x.device).unsqueeze(0)
        h = self.embed(x) + self.pos_embed(positions)

        attn_records = [] if record_attn else None
        for i, block in enumerate(self.blocks):
            h = block(h, past_attn=attn_records, cache=cache, cache_prefix=f"blocks.{i}")

        h = self.ln_final(h)
        logits = self.unembed(h)
        return logits, attn_records


# ---------------------------------------------------------------------------
# Training
# ---------------------------------------------------------------------------
@torch.no_grad()
def evaluate(model: nn.Module, loader: DataLoader) -> tuple[float, float]:
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


# ---------------------------------------------------------------------------
# Copy metrics: the behavioural half of the induction claim
# ---------------------------------------------------------------------------
def analyze_copy_metrics(
    model: nn.Module,
    loader: DataLoader,
    max_batches: Optional[int] = None,
) -> dict[str, float]:
    """How well the model copies, and whether it copies by content.

    Three numbers, all measured on the **copy queries** — the positions
    where "copy what followed the previous occurrence" is the right thing
    to do (see `src/experiments/induction_tasks.copy_queries`):

    * ``copy_accuracy`` — the accuracy on those positions. On the variable
      task this is the headline: only a quarter of the positions are
      learnable, so the overall accuracy is not comparable across tasks.
    * ``copy_accuracy_nonmodal`` — the accuracy on the copy queries whose
      distance is *not* the most frequent one. A fixed-offset head is right
      on the queries that share its offset and wrong everywhere else, so its
      non-modal accuracy is ~0; a content head is right on all of them.
    * ``fixed_offset_baseline`` — the accuracy of the *best single fixed
      offset* on the same queries. It is the ceiling of the positional
      explanation, measured on the data rather than assumed.

    The overall accuracy is reported next to them, never instead of them.
    """
    model.eval()
    per_distance_total: dict[int, int] = {}
    per_distance_correct: dict[int, int] = {}
    token_chunks: list[np.ndarray] = []
    mask_chunks: list[np.ndarray] = []
    overall_correct = 0
    overall_total = 0

    with torch.no_grad():
        for i, (x, y) in enumerate(loader):
            if max_batches is not None and i >= max_batches:
                break
            full = torch.cat([x, y[:, -1:]], dim=1)
            geom = copy_queries(full.numpy())
            mask = geom["mask"][:, :-1]
            dist = geom["distance"][:, :-1]
            logits, _ = model(x.to(DEVICE), record_attn=False)
            preds = logits.argmax(dim=-1).cpu().numpy()
            answers = y.numpy()
            ok = preds == answers
            overall_correct += int(ok.sum())
            overall_total += int(answers.size)
            for d in np.unique(dist[mask]):
                sel = mask & (dist == d)
                key = int(d)
                per_distance_total[key] = per_distance_total.get(key, 0) + int(sel.sum())
                per_distance_correct[key] = per_distance_correct.get(key, 0) + int(
                    ok[sel].sum()
                )
            token_chunks.append(full.numpy())
            mask_chunks.append(geom["mask"])

    total = sum(per_distance_total.values())
    correct = sum(per_distance_correct.values())
    modal = (
        max(per_distance_total, key=lambda k: per_distance_total[k])
        if per_distance_total
        else -1
    )
    modal_total = per_distance_total.get(modal, 0)
    modal_correct = per_distance_correct.get(modal, 0)
    nonmodal_total = total - modal_total
    nonmodal_correct = correct - modal_correct

    baseline = {"best_offset": -1, "best_accuracy": 0.0}
    if token_chunks:
        baseline = fixed_offset_baseline(
            np.concatenate(token_chunks), np.concatenate(mask_chunks)
        )

    return {
        "copy_accuracy": float(correct / total) if total else 0.0,
        "copy_accuracy_nonmodal": (
            float(nonmodal_correct / nonmodal_total) if nonmodal_total else 0.0
        ),
        "fixed_offset_baseline": float(baseline["best_accuracy"]),
        "fixed_offset_best_d": float(baseline["best_offset"]),
        "n_copy_queries": float(total),
        "n_distances": float(len(per_distance_total)),
        "modal_distance": float(modal),
        "overall_accuracy": (
            float(overall_correct / overall_total) if overall_total else 0.0
        ),
    }


# ---------------------------------------------------------------------------
# Checkpoint / resume (Micro-Phase 12)
# ---------------------------------------------------------------------------
# save/load/path helpers live in src/experiments/checkpointing.py (shared
# with exp2); see its docstring for the RNG continuity contract.


def _attention_patterns(model: nn.Module, x: torch.Tensor) -> Optional[list[torch.Tensor]]:
    """Per-layer attention probabilities, for either model protocol in this repo.

    Delegates to `src.experiments.induction_detection.attention_patterns_for_inputs`,
    which owns the protocol dispatch (cache > record_attn > return_cache) and
    the reason for that order: `AttentionOnlyTransformer` has *both* a
    `blocks` attribute and a `record_attn` keyword, so an attribute check
    alone picks the wrong branch for it — which silently returns no patterns
    at all and then crashes `diagnose_induction_formation` on an empty list.
    """
    patterns = attention_patterns_for_inputs(model, x)
    return patterns or None


def compute_attention_entropy(
    model: nn.Module,
    loader: DataLoader,
    prefix_len: Optional[int] = None,
    max_batches: int = 4,
    task: str = TASK_PERIODIC,
) -> dict:
    """Per-layer attention entropy and the four offset masses.

    The masses are the *head-level* signals this repository measures, one
    per hypothesis (see `src/experiments/induction_detection` for the offset
    conventions):

    * `induction_mass`  — mass on `q -> q-L+1`, the copy offset. This is the
      detection signal, on the same [0, 1] scale as the 0.3 threshold.
    * `duplicate_mass`  — mass on `q -> q-L`, the duplicate-token offset
      (Nanda's Step 1).
    * `content_mass`    — mass on `prev(q)+1`, the previous *occurrence* of
      the same token plus one.
    * `prev_token_mass` — mass on `q -> q-1`. This is the offset the old
      detector measured and called "diag+1"; it is kept, explicitly
      labelled, because it is the useful negative control: a head that only
      does this is a previous-token head, not an induction head.

    Each entry is the **max over heads** of that layer, so it stays on the
    same [0, 1] scale as the per-head detection threshold. (The 2026-08-01
    bug summed across heads instead, which put the number on a [0, n_heads]
    scale and made the training curve claim heads were forming while the
    detector found none.)
    """
    model.eval()
    n_layers = len(getattr(model, "blocks", []))
    patterns, tokens = collect_patterns_and_tokens(model, loader, max_batches=max_batches)
    if not patterns:
        zeros = [0.0 for _ in range(n_layers)]
        return {
            "entropy": list(zeros),
            "induction_mass": list(zeros),
            "duplicate_mass": list(zeros),
            "content_mass": list(zeros),
            "prev_token_mass": list(zeros),
        }

    if prefix_len is None:
        seq_len = tokens.shape[1] + 1 if tokens.numel() else 0
        prefix_len = prefix_length_for(seq_len)

    entropy = layer_entropy(patterns)
    masses = head_masses(patterns, tokens, prefix_len, task=task)
    out = {"entropy": entropy}
    for name in ("induction", "duplicate", "content", "prev_token"):
        out[f"{name}_mass"] = [
            float(layer.max()) if len(layer) else 0.0 for layer in masses[name]
        ]
    return out


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
    checkpoint_dir: Optional[str] = None,
    checkpoint_every: int = 0,
    resume_from: Optional[str] = None,
    schedule_epochs: Optional[int] = None,
    detect_every: int = 50,
    stop_on_confirmed: bool = False,
    stop_rule: str = "mechanism",
    detect_patience: int = 2,
    prefix_len: Optional[int] = None,
    composition_threshold: float = COMPOSITION_THRESHOLD,
    task: str = TASK_PERIODIC,
) -> dict:
    """Train the model and return training curves.

    `fresh_batches_fn`, if given, is called once per epoch with the epoch
    index and must return a fresh `DataLoader` sampled from a new set of
    sequences — used to test whether a fixed, epoch-reused dataset lets the
    model memorize specific sequences rather than learn the general
    prefix-matching-and-copying rule (Olsson et al. resample continuously;
    the pre-2026-08-02 version reused one fixed dataset, reshuffled, for the
    entire run). When `None`, `train_loader` is reused every epoch as before.

    Checkpoint/resume (Micro-Phase 12): when `checkpoint_dir` and
    `checkpoint_every > 0` are given, a resume checkpoint is written every
    `checkpoint_every` epochs. The checkpoint captures the model, optimizer,
    and scheduler state *plus the PyTorch RNG state at the exact continuity
    point* — after one epoch's data draws and before the next epoch's. Data
    sampling is driven by that RNG, so a resumed run draws exactly the same
    batches it would have drawn had it never stopped. A killed long run is
    therefore a *pause*, not a loss: relaunch with `resume_from` (or the
    `--resume` CLI flag) and continue.

    The LR schedule (CosineAnnealing, `T_max=schedule_epochs` defaulting to
    `epochs`) spans the *full run horizon*, not the epochs of this call. A
    partial call that will be resumed must pass the same horizon the final
    run will use — e.g. the tests interrupt a run at epoch 3 while planning
    9, so the partial call passes `schedule_epochs=<full horizon>`; treating
    the partial call's own `epochs` as T_max anneals LR to the wrong peak and
    makes no resumed run equal to an uninterrupted one. Falsified by
    TestCheckpointResume (resume must reproduce an uninterrupted run
    bit-for-bit).

    Detection cadence and early stop: every `detect_every` epochs the
    detector runs on the validation set and the result is recorded in the
    history (`induction_mass`, `prev_token_mass`, `composition_score`,
    `confirmed`). With `stop_on_confirmed` the run stops as soon as the stop
    rule fires at `detect_patience` consecutive checks — the positive case
    is bounded by the mechanism rather than by the wall clock, while the
    negative case still runs the *full* pre-registered budget (a shorter
    budget would reproduce exactly the under-trained false negatives this
    repository's audit history keeps finding).

    The stop rule is `stop_rule`:

    * `"mechanism"` (default) — stop only when a head in a layer **above
      the first** is confirmed, i.e. when the two-step circuit (Nanda's
      duplicate head + K-composition) is actually there. A copy head in the
      first layer has no earlier layer to compose with, so it is confirmed
      on the mass alone; on this periodic task the model forms exactly that
      (a fixed-offset copy) within 50 epochs, and stopping there would
      answer a different question than the rung asks.
    * `"any"` — stop on any confirmed head, first layer included.
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
                    "n_layers": len(getattr(model, "blocks", [])),
                    "n_heads": getattr(getattr(model, "blocks", [])[0], "n_heads", 0),
                    "lr": lr,
                    "weight_decay": weight_decay,
                    "epochs": epochs,
                    "seed": seed,
                },
            )
        except Exception as e:
            logger.warning(f"W&B init failed: {e}")
            _wandb = None

    optimizer = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=weight_decay)
    T_max = schedule_epochs if schedule_epochs is not None else epochs
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=T_max)
    criterion = nn.CrossEntropyLoss()

    history = {
        "train_loss": [],
        "val_loss": [],
        "val_acc": [],
        "attn_entropy": [],
        "induction_mass": [],
        "prev_token_mass": [],
        "composition_score": [],
        "confirmed": [],
        "mechanism_confirmed": [],
        "detect_checked": [],
    }
    # A scalar, not a list: the epoch at which the mechanism was confirmed
    # (-1 = never). It lives in the history so it survives a checkpoint.
    history["confirmed_epoch"] = -1.0

    start_epoch = 0
    resume_ckpt = (
        load_training_checkpoint(Path(resume_from), map_location=DEVICE) if resume_from else None
    )
    if resume_ckpt is not None:
        model.load_state_dict(resume_ckpt["model"])
        optimizer.load_state_dict(resume_ckpt["optimizer"])
        scheduler.load_state_dict(resume_ckpt["scheduler"])
        # The stored T_max came from the plan that saved the checkpoint; the
        # continuation's own horizon (`schedule_epochs`/`epochs`) is the same
        # plan, so keep it authoritative for the LR curve.
        scheduler.T_max = T_max
        torch.random.set_rng_state(resume_ckpt["rng_state"])
        history = resume_ckpt["history"]
        start_epoch = resume_ckpt["epoch"] + 1
        logger.info(
            f"RESUME: loaded {resume_from} (saved after epoch "
            f"{resume_ckpt['epoch']}) — continuing from epoch {start_epoch}"
        )
    elif resume_from:
        logger.warning(f"RESUME: checkpoint {resume_from} not found — starting fresh")

    ckpt_path: Optional[Path] = None
    if checkpoint_dir and checkpoint_every > 0:
        ckpt_path = checkpoint_path_for_seed(checkpoint_dir, "exp1", seed)

    consecutive_confirmations = 0

    for epoch in tqdm(range(start_epoch, epochs), desc="Training"):
        epoch_loader = fresh_batches_fn(epoch) if fresh_batches_fn is not None else train_loader

        model.train()
        epoch_loss = 0.0
        for x, y in epoch_loader:
            x, y = x.to(DEVICE), y.to(DEVICE)
            optimizer.zero_grad()
            logits, _ = model(x, record_attn=False)
            loss = criterion(logits.reshape(-1, logits.size(-1)), y.reshape(-1))
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()

            epoch_loss += loss.item() * x.size(0)

        scheduler.step()
        train_loss = epoch_loss / len(epoch_loader.dataset)
        val_loss, val_acc = evaluate(model, val_loader)

        # Attention metrics and head detection, on the same cadence.
        checked = bool(detect_every > 0 and (epoch + 1) % detect_every == 0)
        confirmed = False
        mechanism_confirmed = False
        composition = 0.0
        if checked:
            report, _patterns, _tokens = detect_from_loader(
                model,
                val_loader,
                prefix_len=prefix_len,
                composition_threshold=composition_threshold,
                task=task,
            )
            attn_entropy = float(sum(report.entropy))
            induction_mass = report.peak("induction")
            prev_token_mass = report.peak("prev_token")
            composition = report.best_composition
            confirmed = report.confirmed_count > 0
            # "the circuit is there": a confirmed head above the first layer
            # (which is the only kind that needed the composition to be
            # confirmed in the first place).
            mechanism_confirmed = any(len(h) > 0 for h in report.confirmed[1:])
        elif (epoch + 1) % 50 == 0:
            # Detection off (`--detect-every 0`): the cheap metric-only
            # cadence, kept so the training curves still show the signal.
            attn_metrics = compute_attention_entropy(
                model, val_loader, prefix_len=prefix_len, task=task
            )
            attn_entropy = sum(attn_metrics["entropy"])
            induction_mass = max(attn_metrics["induction_mass"])
            prev_token_mass = max(attn_metrics["prev_token_mass"])
        else:
            attn_entropy = history["attn_entropy"][-1] if history["attn_entropy"] else 0.0
            induction_mass = history["induction_mass"][-1] if history["induction_mass"] else 0.0
            prev_token_mass = history["prev_token_mass"][-1] if history["prev_token_mass"] else 0.0
            confirmed = bool(history["confirmed"][-1]) if history["confirmed"] else False
            mechanism_confirmed = (
                bool(history["mechanism_confirmed"][-1])
                if history["mechanism_confirmed"]
                else False
            )

        history["train_loss"].append(train_loss)
        history["val_loss"].append(val_loss)
        history["val_acc"].append(val_acc)
        history["attn_entropy"].append(attn_entropy)
        history["induction_mass"].append(induction_mass)
        history["prev_token_mass"].append(prev_token_mass)
        history["composition_score"].append(composition)
        history["confirmed"].append(1.0 if confirmed else 0.0)
        history["mechanism_confirmed"].append(1.0 if mechanism_confirmed else 0.0)
        history["detect_checked"].append(1.0 if checked else 0.0)

        if _wandb is not None:
            _wandb.log(
                {
                    "train/loss": train_loss,
                    "val/loss": val_loss,
                    "val/acc": val_acc,
                    "metrics/attn_entropy": attn_entropy,
                    "metrics/induction_mass": induction_mass,
                    "metrics/prev_token_mass": prev_token_mass,
                    "metrics/composition_score": composition,
                    "lr": scheduler.get_last_lr()[0],
                },
                step=epoch,
            )

        if checked:
            logger.info(
                f"Epoch {epoch + 1:4d} | train loss: {train_loss:.4f} | "
                f"val loss: {val_loss:.4f} | val acc: {val_acc:.4f} | "
                f"induction mass: {induction_mass:.3f} | "
                f"prev-token mass (control): {prev_token_mass:.3f} | "
                f"composition: {composition:.3f} | "
                f"confirmed head: {'yes' if confirmed else 'no'}"
            )

        if ckpt_path is not None and (epoch + 1) % checkpoint_every == 0:
            save_training_checkpoint(
                ckpt_path,
                epoch,
                model,
                optimizer,
                scheduler,
                history,
                torch.random.get_rng_state(),
                arch=architecture_metadata(model),
            )
            logger.info(f"Checkpoint saved: {ckpt_path} (epoch {epoch + 1})")

        if stop_on_confirmed and checked:
            stop_fired = confirmed if stop_rule == "any" else mechanism_confirmed
            consecutive_confirmations = consecutive_confirmations + 1 if stop_fired else 0
            if consecutive_confirmations >= detect_patience:
                history["confirmed_epoch"] = float(epoch + 1)
                # The rolling checkpoint may not exist yet: the confirmation
                # can land *before* the first `checkpoint_every` boundary (the
                # standard run confirmed a head at epoch 100 with a 250-epoch
                # checkpoint interval). Writing it here is what makes the
                # cascade runnable — Rung 4 analyses the checkpoint of the
                # model that was confirmed, not a stale one.
                if ckpt_path is not None:
                    save_training_checkpoint(
                        ckpt_path,
                        epoch,
                        model,
                        optimizer,
                        scheduler,
                        history,
                        torch.random.get_rng_state(),
                        arch=architecture_metadata(model),
                    )
                    logger.info(f"Checkpoint saved at the confirmation point: {ckpt_path}")
                logger.info(
                    f"Early stop: an induction head was confirmed at "
                    f"{consecutive_confirmations} consecutive checks "
                    f"(epoch {epoch + 1})."
                )
                break

    if _wandb is not None:
        _wandb.finish()
    return history


# ---------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------
def analyze_induction_heads(
    model: nn.Module,
    loader: DataLoader,
    prefix_len: Optional[int] = None,
    threshold: float = INDUCTION_MASS_THRESHOLD,
    composition_threshold: float = COMPOSITION_THRESHOLD,
    task: str = TASK_PERIODIC,
) -> tuple[list, list]:
    """Identify induction heads by their attention patterns.

    An induction head attends from the current query position `q` to the
    token *after the previous occurrence of the current token*, which on this
    task's `prefix + prefix` layout is the key `q - L + 1` (`L` = prefix
    length). The detection is two-stage:

    * **screen** — the head's induction mass (`q -> q-L+1`) is above
      `threshold` (0.3, the per-head threshold this repository has used
      since 2026-08-01);
    * **confirmation** — the head's layer is composed with an earlier layer
      at a K-composition score of at least `composition_threshold`.

    The offset convention is the part that was wrong before 2026-10-19: the
    old detector measured `q -> q-1` (a *previous-token* head) and called it
    "diag+1", so every "0 / N heads" number this repository published was a
    statement about the detector. See
    `src/experiments/induction_detection` for the full derivation.

    Returns:
        Tuple of (confirmed_head_indices_per_layer, attention_patterns).
    """
    report, patterns, _tokens = detect_from_loader(
        model,
        loader,
        prefix_len=prefix_len,
        mass_threshold=threshold,
        composition_threshold=composition_threshold,
        task=task,
    )
    return report.confirmed, patterns


def analyze_induction_heads_full(
    model: nn.Module,
    loader: DataLoader,
    prefix_len: Optional[int] = None,
    threshold: float = INDUCTION_MASS_THRESHOLD,
    composition_threshold: float = COMPOSITION_THRESHOLD,
    task: str = TASK_PERIODIC,
):
    """The full detection report (masses, screen, confirmation, composition).

    `analyze_induction_heads` is the two-value convenience wrapper; this one
    carries the numbers the manifests report, so a caller never has to
    recompute a metric the detector already measured.
    """
    return detect_from_loader(
        model,
        loader,
        prefix_len=prefix_len,
        mass_threshold=threshold,
        composition_threshold=composition_threshold,
        task=task,
    )


# `k_composition_scores` used to live here; it now lives in
# `src.experiments/induction_detection` (the single source of truth shared
# by Rungs 1, 4 and 6) and is re-exported by this import so that
# `from src.experiments.exp1_induction_heads import k_composition_scores`
# — the import exp6 and the tests use — keeps working.
def diagnose_induction_formation(
    all_patterns: list,
    tokens: Optional[torch.Tensor] = None,
    prefix_len: Optional[int] = None,
    task: str = TASK_PERIODIC,
) -> dict:
    """The "how far did the model get" instrument for the two-step path
    (Nanda & Jacobsen 2023). Given collected per-layer attention patterns
    (list of (B, n_heads, S, S) tensors, one per layer), reports:

    - Step 1: per-head **duplicate-token** mass in the source layer — the
      mass on `q -> q-L`, the key holding the previous occurrence of the
      current token. (Before 2026-10-19 this was the `q -> q-1`
      previous-token mass, which is a different head entirely.)
    - Step 2: the K-composition matrix between any layer pair (l_src, l_dest)
      with l_src < l_dest and its best pair;
    - peakedness of the source layer argmax: whether `prev` is a real, focused choice.

    A confirmed induction head needs both steps high. Supports arbitrary
    number of layers >= 2.

    `tokens` (the input ids the patterns were collected on) is optional: with
    it, Step 1 is the correct duplicate-offset mass; without it the
    previous-token mass is reported instead and `step1_metric` says which
    one it is. That fallback exists because exp6's K-composition helper
    historically collected patterns without keeping the tokens — callers must
    be able to tell the two apart instead of reading one as the other.
    """
    empty = {
        "step1_l0_duplicate_mass": [],
        "step1_metric": "none",
        "l0_peakedness": 0.0,
        "step2_k_composition": 0.0,
        "best_l0_head": -1,
        "best_l1_head": -1,
        "best_l_src": 0,
        "best_l_dest": 1,
    }
    if len(all_patterns) < 2:
        return empty

    # A layer with no attention patterns at all arrives as an empty list, not a
    # tensor. Indexing that with [:, :, 1:, :-1] raises
    # "list indices must be integers or slices, not tuple" — which is what the
    # --seeds path hit whenever a layer produced no records.
    if any(not hasattr(p, "ndim") for p in all_patterns):
        return empty

    step1_metric = "prev_token"
    if tokens is not None and tokens.numel():
        if prefix_len is None and task != TASK_VARIABLE:
            seq_len = tokens.shape[1] + 1
            prefix_len = prefix_length_for(seq_len)
        step1_masses = head_masses(
            list(all_patterns), tokens, prefix_len if prefix_len is not None else 0, task=task
        )["duplicate"]
        step1_metric = "duplicate"
    else:
        step1_masses = [
            p[:, :, 1:, :-1].diagonal(dim1=-2, dim2=-1).mean(dim=(0, -1)).cpu().numpy()
            for p in all_patterns
        ]

    best_comp = -1.0
    best_pair = (0, 1, -1, -1)
    best_l0_duplicate_mass = []
    best_peakedness = 0.0

    for l_src in range(len(all_patterns) - 1):
        p_src = all_patterns[l_src]
        diag0 = step1_masses[l_src]
        peakedness = p_src.max(dim=-1).values.mean(dim=(0, 2))

        for l_dest in range(l_src + 1, len(all_patterns)):
            p_dest = all_patterns[l_dest]
            comp = k_composition_scores(p_src, p_dest)
            if comp.size > 0:
                flat_idx = int(np.argmax(comp))
                max_val = float(comp.flat[flat_idx])
                if max_val > best_comp:
                    best_comp = max_val
                    h0 = flat_idx // comp.shape[1]
                    h1 = flat_idx % comp.shape[1]
                    best_pair = (l_src, l_dest, h0, h1)
                    best_l0_duplicate_mass = diag0.tolist()
                    best_peakedness = float(peakedness.max())

    if best_comp < 0:
        p0 = all_patterns[0]
        diag0 = step1_masses[0]
        peakedness = p0.max(dim=-1).values.mean(dim=(0, 2))
        comp = k_composition_scores(all_patterns[0], all_patterns[1])
        if comp.size > 0:
            flat_idx = int(np.argmax(comp))
            best_comp = float(comp.flat[flat_idx])
            best_pair = (0, 1, flat_idx // comp.shape[1], flat_idx % comp.shape[1])
        else:
            best_pair = (0, 1, -1, -1)
            best_comp = 0.0
        best_l0_duplicate_mass = diag0.tolist()
        best_peakedness = float(peakedness.max())

    l_src, l_dest, h0, h1 = best_pair
    return {
        "step1_l0_duplicate_mass": best_l0_duplicate_mass,
        "step1_metric": step1_metric,
        "l0_peakedness": best_peakedness,
        "step2_k_composition": best_comp,
        "best_l0_head": h0,
        "best_l1_head": h1,
        "best_l_src": l_src,
        "best_l_dest": l_dest,
    }


def plot_composition_diagnostic(all_patterns: list, diagnosis: dict, save_path: Path) -> None:
    """Two-panel figure: the best duplicate head's attention (Step 1, from best_l_src)
    and the best induction head's attention (Step 2, from best_l_dest) with the
    K-composition `prev(q)+1` curve overlaid."""
    l_src = diagnosis.get("best_l_src", 0)
    l_dest = diagnosis.get("best_l_dest", 1)
    h0 = diagnosis.get("best_l0_head", -1)
    h1 = diagnosis.get("best_l1_head", -1)
    if len(all_patterns) <= max(l_src, l_dest) or h0 < 0 or h1 < 0:
        return
    p0 = all_patterns[l_src][0, h0].numpy()
    p1 = all_patterns[l_dest][0, h1].numpy()
    S = p0.shape[-1]
    prev_curve = np.argmax(p0, axis=-1) + 1
    prev_curve[prev_curve >= S] = S - 1
    fig, axes = plt.subplots(1, 2, figsize=(14, 7))
    for ax, pat, title in (
        (axes[0], p0, f"L{l_src} head {h0} — duplicate-token head (Step 1)"),
        (axes[1], p1, f"L{l_dest} head {h1} — attention vs prev+1 curve (Step 2)"),
    ):
        im = ax.imshow(pat, cmap="Blues", aspect="equal")
        ax.set_title(title, fontsize=12)
        ax.set_xlabel("Key Position")
        ax.set_ylabel("Query Position")
        fig.colorbar(im, ax=ax, shrink=0.8)
    axes[1].plot(
        prev_curve,
        np.arange(S),
        color="red",
        ls="--",
        lw=1.2,
        label="prev(q) + 1 (K-composition target)",
    )
    axes[1].legend(fontsize=9)
    # Use the layer the detector actually found, not a hardcoded "L0".
    # diagnose_induction_formation() explicitly supports best_l_src >= 1 for
    # deeper models, but the old title overwrote the correct one with "L0",
    # mislabelling every multi-layer diagnosis.
    axes[0].set_title(
        f"L{l_src} head {h0} — duplicate-token head (Step 1)\n"
        f"diag+1 mass: {diagnosis['step1_l0_duplicate_mass'][h0]:.3f}",
        fontsize=12,
    )
    axes[1].set_title(
        f"L1 head {h1} — K-composition (Step 2)\nscore: {diagnosis['step2_k_composition']:.3f}",
        fontsize=12,
    )
    fig.tight_layout()
    fig.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    logger.info(f"Saved composition diagnostic to {save_path}")


def _make_fresh_batches_fn(args: argparse.Namespace, seed: int) -> Callable[[int], DataLoader]:
    """Build a per-epoch DataLoader factory: a fresh set of sequences every
    epoch instead of one fixed set reshuffled — see train_model()'s
    fresh_batches_fn docstring."""

    def fn(epoch: int) -> DataLoader:
        dataset, _ = make_task_data(
            args,
            num_train=args.num_train,
            num_val=1,
            seed=seed * 1_000_003 + epoch + 1,
        )
        return DataLoader(dataset, batch_size=args.batch_size, shuffle=True)

    return fn


def causal_ablation(
    model: nn.Module,
    loader: DataLoader,
    layer: int,
    head: int,
    restrict_to_copy: bool = False,
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

    `restrict_to_copy` measures the accuracy on the **copy queries** only.
    On the variable-distance task that is the meaningful number: the
    filler positions are unpredictable, so an overall accuracy is mostly a
    measure of how much of the sequence is noise.

    Returns:
        Accuracy after head ablation.
    """
    model.eval()
    block = model.blocks[layer]
    mask = torch.ones(block.n_heads)
    mask[head] = 0.0
    block.head_mask = mask
    try:
        return _accuracy_under_mask(model, loader, restrict_to_copy)
    finally:
        # The mask must never survive an exception: a leaked mask would
        # silently ablate that head for the rest of the run.
        block.head_mask = None


def _accuracy_under_mask(
    model: nn.Module,
    loader: DataLoader,
    restrict_to_copy: bool,
) -> float:
    """The accuracy the model gets with the heads that are currently masked.

    With ``restrict_to_copy`` the accuracy is measured on the **copy
    queries** only: on the variable-distance task the filler positions are
    unpredictable, so an overall accuracy is mostly a measure of how much of
    the sequence is noise.
    """
    correct = 0
    total = 0
    with torch.no_grad():
        for x, y in loader:
            copy_mask = None
            if restrict_to_copy:
                copy_mask = copy_mask_for_pairs(x, y)
            x, y = x.to(DEVICE), y.to(DEVICE)
            logits, _ = model(x, record_attn=False)
            preds = logits.argmax(dim=-1)
            ok = preds == y
            if copy_mask is not None:
                mask_device = copy_mask.to(ok.device)
                ok = ok & mask_device
                total += int(mask_device.sum().item())
            else:
                total += y.numel()
            correct += int(ok.sum().item())
    return correct / total if total else 0.0


def causal_ablation_group(
    model: nn.Module,
    loader: DataLoader,
    heads: list[tuple[int, int]],
    restrict_to_copy: bool = False,
) -> float:
    """Ablate a *set* of heads at once, and return the accuracy.

    The single-head ablation answers "does this head matter?". The group
    ablation answers the question a distributed circuit raises: "does the
    *group* matter, and does any single member of it?". A large drop when
    the whole group is removed, next to a small drop when any one of its
    members is removed, is the signature of a copy that is carried by the
    group rather than by one head.

    The group is the *candidate* set of
    `src.experiments.copy_circuit.candidate_heads` — fixed by the rule
    "content mass at least three times the chance level", which reads the
    data and the attention masses, never the outcome.
    """
    if not heads:
        return _accuracy_under_mask(model, loader, restrict_to_copy)
    model.eval()
    per_layer: dict[int, list[int]] = {}
    for layer, head in heads:
        per_layer.setdefault(layer, []).append(head)
    saved: dict[int, Optional[torch.Tensor]] = {}
    try:
        for layer, head_list in per_layer.items():
            block = model.blocks[layer]
            saved[layer] = block.head_mask
            mask = torch.ones(block.n_heads)
            for head in head_list:
                mask[head] = 0.0
            block.head_mask = mask
        return _accuracy_under_mask(model, loader, restrict_to_copy)
    finally:
        for layer, previous in saved.items():
            model.blocks[layer].head_mask = previous


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


def plot_training_curves(history: dict, save_path: Path) -> None:
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

    axes[1, 1].plot(
        epochs, history["induction_mass"], label="Induction mass (q - L + 1)", color="orange"
    )
    axes[1, 1].plot(
        epochs,
        history["prev_token_mass"],
        label="Prev-token mass (q - 1, control)",
        color="gray",
        alpha=0.7,
    )
    axes[1, 1].set_xlabel("Epoch")
    axes[1, 1].set_ylabel("Attention mass")
    axes[1, 1].set_title("Induction Head Signal (copy offset)", fontsize=13)
    axes[1, 1].axhline(y=0.3, color="red", linestyle="--", alpha=0.3, label="Detection threshold")
    axes[1, 1].legend(fontsize=9)
    axes[1, 1].grid(True, alpha=0.3)

    fig.tight_layout()
    fig.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    logger.info(f"Saved training curves to {save_path}")


# ---------------------------------------------------------------------------
# Multi-seed headline run
# ---------------------------------------------------------------------------
def _run_task_probe(
    model: nn.Module,
    args: argparse.Namespace,
    val_loader: DataLoader,
    seed: int,
) -> dict:
    """The naming test of the run's task.

    On the **periodic** task the content target and the fixed offset are
    the same key, so the probe needs an off-distribution batch to tell the
    two mechanisms apart (ADR-0032). On the **variable-distance** task the
    dissociation is native: the repeats sit at different distances, so the
    training distribution itself separates the mechanisms and no
    off-distribution batch is needed.
    """
    if getattr(args, "task", TASK_PERIODIC) == TASK_VARIABLE:
        tokens = next(iter(val_loader))[0]
        return run_content_vs_offset_probe(model, tokens)
    return run_dissociation_probe(
        model,
        vocab_size=args.vocab_size,
        seq_len=args.seq_len,
        num_samples=min(64, max(16, args.num_train // 16)),
        seed=seed,
    )


def _headline_metrics(
    history: dict,
    induction_heads: list,
    diagnosis: dict,
    report=None,
    probe: Optional[dict] = None,
    copy_stats: Optional[dict] = None,
) -> dict[str, float]:
    """The headline numbers both the multi-seed manifest and the single-seed
    `--standard` manifest report, derived from one analysis pass — shared so
    the two reporting paths cannot drift apart. Ablation drops are filled in
    by the caller (they need the model).

    The metric names changed with the detector (2026-10-19):
    `peak_diag1_mass` — the previous-token mass, which the old detector
    called the induction signal — is now reported as
    `peak_prev_token_mass` (a control), and the induction signal itself is
    `peak_induction_mass`, measured on the copy offset `q - L + 1`.

    With the variable-distance task (2026-10-20) three more numbers travel
    with them, because on that task the overall accuracy is mostly a
    measure of how much of the sequence is noise: the accuracy on the copy
    queries, the accuracy on the *non-modal* distance group (the
    behavioural separator between copying by content and copying by a fixed
    offset) and the best fixed-offset baseline they have to beat.
    """
    total_induction = sum(len(h) for h in induction_heads)
    peak_induction = (
        float(np.max(history["induction_mass"])) if history.get("induction_mass") else 0.0
    )
    peak_prev_token = (
        float(np.max(history["prev_token_mass"])) if history.get("prev_token_mass") else 0.0
    )
    epochs_run = float(len(history["val_acc"]))
    steps_per_epoch = float(history.get("steps_per_epoch", 0.0))
    # Where the confirmed heads live. The split matters: a copy head in the
    # *first* layer has no earlier layer to compose with (so it is confirmed
    # on the mass alone), while a head in a later layer is confirmed only
    # when the K-composition mechanism agrees — so "how many in layer 0" and
    # "how many above it" are two different claims.
    first_layer = len(induction_heads[0]) if induction_heads else 0
    later_layers = total_induction - first_layer
    stats = copy_stats or {}
    metrics = {
        "final_val_acc": float(history["val_acc"][-1]),
        "total_induction_heads": float(total_induction),
        "total_mass_heads": float(report.screen_count if report is not None else total_induction),
        "confirmed_heads_first_layer": float(first_layer),
        "confirmed_heads_later_layers": float(later_layers),
        "mechanism_confirmed": float(
            bool(report is not None and any(len(h) > 0 for h in report.confirmed[1:]))
        ),
        "peak_induction_mass": peak_induction,
        "peak_prev_token_mass": peak_prev_token,
        "peak_content_mass": float(report.peak("content") if report is not None else 0.0),
        "peak_offset_mass": float(
            report.peak_offset_mass if report is not None else 0.0
        ),
        "k_composition_score": float(diagnosis["step2_k_composition"]),
        "l0_duplicate_head_mass": float(max(diagnosis["step1_l0_duplicate_mass"] or [0.0])),
        "confirmed_epoch": float(history.get("confirmed_epoch", -1.0)),
        "epochs_run": epochs_run,
        "steps_run": epochs_run * steps_per_epoch,
        "probe_content_mass": float((probe or {}).get("peak_content_mass", 0.0)),
        "probe_period_mass": float((probe or {}).get("peak_period_mass", 0.0)),
        "probe_offset_mass": float(
            (probe or {}).get("peak_offset_mass", (probe or {}).get("peak_period_mass", 0.0))
        ),
        "probe_content_wins": float(bool((probe or {}).get("content_wins", False))),
        "copy_accuracy": float(stats.get("copy_accuracy", 0.0)),
        "copy_accuracy_nonmodal": float(stats.get("copy_accuracy_nonmodal", 0.0)),
        "fixed_offset_baseline": float(stats.get("fixed_offset_baseline", 0.0)),
        "copy_gap": float(
            stats.get("copy_accuracy", 0.0) - stats.get("fixed_offset_baseline", 0.0)
        ),
        "n_copy_queries": float(stats.get("n_copy_queries", 0.0)),
        "n_copy_distances": float(stats.get("n_distances", 0.0)),
    }
    return metrics


# How many sequences of the detected batch the logit attribution runs on.
# The attribution needs a forward pass with a cache, and the cache holds the
# attention probabilities of every sequence it sees: 256 sequences of length
# 64 is already thousands of queries, far more than the attribution needs.
ATTRIBUTION_SEQUENCES = 256


def _circuit_report(
    model: nn.Module,
    val_loader: DataLoader,
    report,
    tokens: torch.Tensor,
    task: str,
    copy_stats: dict,
) -> dict[str, float]:
    """The secondary, circuit-level measurement of the copy mechanism.

    This is the measurement the per-head screen cannot make. The screen
    asks "how much attention mass does *this* head put on the content key?",
    and a copy distributed over several heads falls below it in every one of
    them while the circuit as a whole is strong. So the report measures:

    * the **aggregate** content mass and how concentrated it is;
    * the **group ablation**: the drop in copy accuracy when the whole
      candidate group is removed at once;
    * the **single-head** drops of the same candidates, next to it — a large
      group drop with small single drops is a distributed circuit;
    * the **first-order logit attribution** of every head to the
      content-vs-position contrast.

    The candidate group is fixed by a rule that reads the data and the
    attention masses, never the outcome (see
    `src.experiments.copy_circuit.candidate_heads`).

    Only the variable-distance task has a content-vs-position contrast to
    measure — on the periodic task the two coincide — so the report is
    empty elsewhere.
    """
    if task != TASK_VARIABLE:
        return {}

    triples = content_triples(tokens)
    metrics: dict[str, float] = mass_summary(report, triples)
    candidates = candidate_heads(report, triples)
    metrics["n_candidate_heads"] = float(len(candidates))

    # Exploratory group: the smallest set of heads covering 80% of the
    # content mass. Not the pre-registered candidate rule, not used for the
    # verdict — it exists so the mechanism report can describe a distributed
    # circuit even when the 3x chance screen selects few or no heads.
    exploratory = mass_covering_heads(report, triples)
    metrics["exploratory_group_size"] = float(len(exploratory))

    base_copy = float(copy_stats.get("copy_accuracy", 0.0))
    single_drops: list[float] = []
    for layer, head in candidates:
        ablated = causal_ablation(model, val_loader, layer, head, restrict_to_copy=True)
        single_drops.append(base_copy - ablated)
    group_accuracy = causal_ablation_group(
        model, val_loader, candidates, restrict_to_copy=True
    )
    metrics["group_ablation_drop"] = float(base_copy - group_accuracy)
    metrics["max_single_ablation_drop"] = (
        float(max(single_drops)) if single_drops else 0.0
    )
    metrics["mean_single_ablation_drop"] = (
        float(sum(single_drops) / len(single_drops)) if single_drops else 0.0
    )

    # Exploratory group ablation: same intervention, wider group.
    group_accuracy_exploratory = causal_ablation_group(
        model, val_loader, exploratory, restrict_to_copy=True
    )
    metrics["exploratory_group_ablation_drop"] = float(
        base_copy - group_accuracy_exploratory
    )

    subset = min(int(tokens.shape[0]), ATTRIBUTION_SEQUENCES)
    triples_subset = triples[triples[:, 0] < subset]
    best_offset = int(copy_stats.get("fixed_offset_best_d", -1))
    if best_offset <= 0:
        best_offset = int(report.best_offset)
    attribution = content_vs_position_attribution(
        model, tokens[:subset], triples_subset, best_offset
    )
    metrics["dla_content_minus_offset"] = float(attribution["dla_total"])
    metrics["dla_top_head_share"] = float(attribution["dla_top_head_share"])
    metrics["dla_positive_share"] = float(attribution["dla_positive_share"])
    metrics["dla_observed_logit_diff"] = float(attribution["dla_observed_logit_diff"])
    metrics["dla_n_queries"] = float(attribution["dla_n_queries"])

    code, label = classify_mechanism(metrics)
    metrics["mechanism_kind"] = float(code)
    logger.info(
        "Circuit report - content mass total %.4f (chance %.4f, excess %.4f, "
        "ratio %.2f) | top head %.0f%%, %d heads cover 80%% | "
        "n_candidates=%d | group ablation drop %.4f | max single drop %.4f | "
        "exploratory group=%d, exploratory drop %.4f | attribution %.4f -> %s",
        metrics["content_mass_total"],
        metrics["content_chance_mass"],
        metrics["content_mass_excess"],
        metrics["content_mass_ratio"],
        100.0 * metrics["content_mass_top_share"],
        int(metrics["content_mass_heads_for_80pct"]),
        int(metrics["n_candidate_heads"]),
        metrics["group_ablation_drop"],
        metrics["max_single_ablation_drop"],
        int(metrics["exploratory_group_size"]),
        metrics["exploratory_group_ablation_drop"],
        metrics["dla_content_minus_offset"],
        label,
    )
    return metrics


def _seed_metrics(
    model: nn.Module,
    val_loader: DataLoader,
    history: dict,
    induction_heads: list,
    diagnosis: dict,
    report,
    probe: Optional[dict],
    copy_stats: dict,
    tokens: torch.Tensor,
    task: str,
) -> dict[str, float]:
    """The metrics of one seed: the headline numbers, the ablation drops and
    the circuit-level report.

    One function, so the single-seed (`--standard`) reporting path and the
    multi-seed (`--seeds`) reporting path cannot drift apart — the two used
    to duplicate the ablation loop, and a change to one of them was a
    change the other never saw.
    """
    metrics = _headline_metrics(
        history,
        induction_heads,
        diagnosis,
        report=report,
        probe=probe,
        copy_stats=copy_stats,
    )
    drop_sum = 0.0
    n_drops = 0
    copy_drop_sum = 0.0
    for layer_idx, heads in enumerate(induction_heads):
        for head_idx in heads:
            ablated_acc = causal_ablation(model, val_loader, layer_idx, head_idx)
            drop_sum += history["val_acc"][-1] - ablated_acc
            copy_ablated = causal_ablation(
                model, val_loader, layer_idx, head_idx, restrict_to_copy=True
            )
            copy_drop_sum += copy_stats["copy_accuracy"] - copy_ablated
            n_drops += 1
    # With no confirmed head there is nothing to ablate: the mean is undefined,
    # not zero. Writing 0.0 would look like a causal measurement and would fail
    # criterion 6 by fabrication — the same bug fixed in exp4 for path patching.
    if n_drops:
        metrics["mean_ablation_drop"] = float(drop_sum / n_drops)
        metrics["mean_copy_ablation_drop"] = float(copy_drop_sum / n_drops)
    metrics.update(
        _circuit_report(model, val_loader, report, tokens, task, copy_stats)
    )
    return metrics


def _write_single_manifest(
    args: argparse.Namespace,
    metrics: dict[str, float],
    wall_clock_seconds: float,
) -> None:
    """Provenance for a single-seed run: `--standard` (and `--save-manifest`)
    write a results/exp1_induction_heads.json manifest so the headline is
    traceable to a commit + config even when only one seed has run (the
    multi-seed manifest is the same file, written by `--seeds`)."""
    manifest = ResultsManifest.from_run(
        experiment="exp1_induction_heads",
        seeds=[args.seed],
        args={k: v for k, v in vars(args).items() if k != "seeds"},
        per_seed_metrics=[metrics],
        aggregate={
            k: {"mean": v, "std": 0.0, "min": v, "max": v, "n": 1.0} for k, v in metrics.items()
        },
        wall_clock_seconds=wall_clock_seconds,
        device=str(DEVICE),
        n_parameters=count_parameters(
            AttentionOnlyTransformer(
                vocab_size=args.vocab_size,
                d_model=args.d_model,
                n_layers=args.n_layers,
                n_heads=args.n_heads,
                max_seq_len=args.seq_len,
            )
        ),
        notes="Single-seed standard-scale run (Micro-Phase 12 'landed domino').",
    )
    # `--quick` is a smoke config and must not overwrite the flagship record;
    # an explicit --manifest-path always wins.
    manifest_path = resolve_manifest_path(
        "exp1_induction_heads",
        Path("results") / "exp1_induction_heads.json",
        getattr(args, "manifest_path", None),
        getattr(args, "quick", False),
    )
    manifest.save(manifest_path)
    logger.info(f"Saved single-seed manifest to {manifest_path}")


def run_single_seed(seed: int, args: argparse.Namespace) -> dict[str, float]:
    """Train one induction-heads run end-to-end and return headline metrics
    for one seed. Mirrors main()'s single-seed data/model/train/analysis
    steps, minus plotting and model-saving — used by `--seeds` to aggregate
    across seeds via `src.experiments.runner.run_seeds`.
    """
    train_dataset, val_dataset = make_task_data(
        args,
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

    resume_from = None
    if args.resume and args.checkpoint_every > 0:
        resume_from = str(checkpoint_path_for_seed(args.checkpoint_dir, "exp1", seed))
    elif getattr(args, "resume_from", None):
        resume_from = args.resume_from

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
        checkpoint_dir=args.checkpoint_dir if args.checkpoint_every > 0 else None,
        checkpoint_every=args.checkpoint_every,
        resume_from=resume_from,
        detect_every=getattr(args, "detect_every", 50),
        stop_on_confirmed=getattr(args, "stop_on_confirmed", False),
        stop_rule=getattr(args, "stop_rule", "mechanism"),
        detect_patience=getattr(args, "detect_patience", 2),
        prefix_len=prefix_length_for(args.seq_len),
        task=getattr(args, "task", TASK_PERIODIC),
    )
    history["steps_per_epoch"] = float(len(train_loader))

    prefix_len = prefix_length_for(args.seq_len)
    task = getattr(args, "task", TASK_PERIODIC)
    report, all_patterns, tokens = analyze_induction_heads_full(
        model, val_loader, prefix_len=prefix_len, task=task
    )
    induction_heads = report.confirmed
    diagnosis = diagnose_induction_formation(
        all_patterns, tokens=tokens, prefix_len=prefix_len, task=task
    )

    probe = None
    if getattr(args, "probe_dissociation", True):
        probe = _run_task_probe(model, args, val_loader, seed=seed)

    copy_stats = analyze_copy_metrics(model, val_loader)

    metrics = _seed_metrics(
        model,
        val_loader,
        history,
        induction_heads,
        diagnosis,
        report,
        probe,
        copy_stats,
        tokens,
        task,
    )
    # Record which batch regime produced these numbers. The fixed-vs-fresh
    # comparison is the one solid Rung 1 finding, and without this field a
    # manifest does not say which arm of the comparison it is.
    metrics["batch_mode"] = 0.0 if not args.fresh_batches else 1.0
    return metrics


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
class _FreshBatchesAction(argparse.Action):
    """`--fresh-batches` is the historical spelling of `--batches fresh`.

    It has to write through to `batch_mode` as well as `fresh_batches`, or the
    two fields disagree and every downstream consumer has to pick one.
    """

    def __init__(self, option_strings, dest, **kwargs):  # type: ignore[no-untyped-def]
        kwargs["nargs"] = 0
        super().__init__(option_strings, dest, **kwargs)

    def __call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        values: object,
        option_string: str | None = None,
    ) -> None:
        setattr(namespace, self.dest, True)
        setattr(namespace, "batch_mode", "fresh")


class _BatchesAction(argparse.Action):
    """`--batches {fixed,fresh}` writes through to `fresh_batches`.

    Normalising at parse time rather than in main() means the flag is correct
    for anything that parses arguments without running an experiment — which is
    how tests exercise it, and how the matched fixed-vs-fresh comparison gets
    built. When both spellings are given, the last one wins, which is standard
    argparse semantics and more predictable than an error.
    """

    def __call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        values: object,
        option_string: str | None = None,
    ) -> None:
        assert isinstance(values, str)
        if values not in ("fixed", "fresh"):
            parser.error(f"--batches must be 'fixed' or 'fresh', got {values!r}")
        setattr(namespace, "fresh_batches", values == "fresh")
        setattr(namespace, "batch_mode", values)


def build_parser() -> argparse.ArgumentParser:
    """The exp1 CLI. Extracted from main() so tests can parse arguments without
    running an experiment, matching exp2/exp6's structure."""
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
        "--content-standard",
        action="store_true",
        help=(
            "The content task's standard-scale config, as amended on "
            "2026-10-22 before the GPU run (see the pre-registration's "
            "addendum). It is the standard config with one change: the "
            "vocabulary is 256 instead of 2048. The 2048 of the periodic "
            "task answered a constraint the content task does not have — "
            "the periodic prefix is sampled *with replacement*, so a large "
            "vocabulary is what keeps the prefix collision-free, while the "
            "content task samples its key *without* replacement. The "
            "standard-geometry CPU probe of 2026-10-22 was still at the "
            "uniform prediction after 400 epochs at 2048, and the amended "
            "geometry is the one the run has to answer the question."
        ),
    )
    parser.add_argument(
        "--task",
        choices=[TASK_PERIODIC, TASK_VARIABLE],
        default=TASK_PERIODIC,
        help=(
            "Which induction task to train on. 'periodic' is the historical "
            "prefix+prefix layout, where the previous occurrence of a token "
            "is always at q-L and a fixed-offset copy is the same function as "
            "a content-based one (ADR-0032). 'variable' is the content-based "
            "task of ADR-0033: the repeats sit at distances that change from "
            "block to block, so the fixed-offset shortcut does not exist and "
            "the induction claim becomes testable."
        ),
    )
    parser.add_argument(
        "--key-len",
        type=int,
        default=None,
        help=(
            "Variable task only: the length of the source segment (the "
            "distinct 'key' tokens at the start of the sequence). Default: "
            "the pre-registered geometry for the sequence length."
        ),
    )
    parser.add_argument(
        "--copy-blocks",
        type=int,
        default=None,
        help=(
            "Variable task only: how many verbatim copies of the key each "
            "sequence carries. Default: the pre-registered geometry."
        ),
    )
    parser.add_argument(
        "--copy-block-len",
        type=int,
        default=None,
        help=(
            "Variable task only: the length of each copy block. Default: the "
            "pre-registered geometry."
        ),
    )
    parser.add_argument("--d-model", type=int, default=64, help="Model dimension")
    parser.add_argument("--n-layers", type=int, default=2, help="Number of layers")
    parser.add_argument("--n-heads", type=int, default=4, help="Heads per layer")
    parser.add_argument("--epochs", type=int, default=5000, help="Training epochs")
    parser.add_argument("--lr", type=float, default=1e-3, help="Learning rate")
    parser.add_argument("--weight-decay", type=float, default=0.1, help="Weight decay")
    parser.add_argument("--batch-size", type=int, default=64, help="Batch size")
    parser.add_argument("--num-train", type=int, default=8192, help="Training samples")
    parser.add_argument("--no-train", action="store_true", help="Skip training (analysis only)")
    parser.add_argument("--quick", action="store_true", help="Quick test (reduced config)")
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
    parser.add_argument("--wandb", action="store_true", help="Log metrics to Weights & Biases")
    parser.add_argument(
        "--scale",
        type=str,
        choices=["standard", "large"],
        default=None,
        help=(
            "Named config preset. 'standard' is the Micro-Phase 10 canonical "
            "config (identical to --standard). 'large' is the scaled GPU "
            "config: vocab_size=2048, seq_len=128, d_model=256, 4 layers, "
            "8 heads, epochs=1500, num_train=16384, fresh-batches on — the "
            "scale the standard-scale run is meant to de-risk. This replaces "
            "the closed PR #164 'exp7' wrapper: exp1 already had every knob "
            "exp7 hardcoded, so the preset lives here instead of in a second "
            "module that could drift."
        ),
    )
    parser.add_argument("--save-model", action="store_true", help="Save trained model")
    parser.add_argument(
        "--fresh-batches",
        action=_FreshBatchesAction,
        help=(
            "Resample a fresh set of training sequences every epoch instead "
            "of reusing one fixed set (reshuffled). Tests whether the fixed "
            "dataset lets the model memorize specific sequences rather than "
            "learn prefix-matching-and-copying (Olsson et al. resample "
            "continuously). Historical spelling of --batches fresh."
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
    parser.add_argument(
        "--checkpoint-dir",
        type=str,
        default="checkpoints",
        help="Directory for rolling resume checkpoints (Micro-Phase 12 stateful runs).",
    )
    parser.add_argument(
        "--checkpoint-every",
        type=int,
        default=0,
        help="Write a resume checkpoint every N epochs (0 = off).",
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help=(
            "Resume the seed's latest checkpoint in --checkpoint-dir if "
            "present — a killed run is a pause, not a loss."
        ),
    )
    parser.add_argument(
        "--resume-from",
        type=str,
        default=None,
        help="Explicit checkpoint file to resume from (overrides --resume).",
    )
    parser.add_argument(
        "--detect-every",
        type=int,
        default=50,
        help=(
            "Run the head detector every N epochs (0 = never). The detector "
            "measures the induction mass on the copy offset q-(L-1) and the "
            "K-composition score; both land in the manifest and in the "
            "training curves."
        ),
    )
    parser.add_argument(
        "--stop-on-confirmed",
        action="store_true",
        help=(
            "Stop training as soon as the stop rule fires at "
            "--detect-patience consecutive checks. The positive case is then "
            "bounded by the mechanism; the negative case still runs the full "
            "pre-registered budget."
        ),
    )
    parser.add_argument(
        "--stop-rule",
        choices=["mechanism", "any"],
        default="mechanism",
        help=(
            "What counts as 'confirmed' for the early stop. 'mechanism' (the "
            "default) requires a confirmed head above the first layer, i.e. "
            "the two-step circuit; 'any' also stops on a first-layer copy "
            "head, which on this periodic task the model forms within 50 "
            "epochs and which is not the circuit the rung is about."
        ),
    )
    parser.add_argument(
        "--detect-patience",
        type=int,
        default=2,
        help=(
            "Consecutive detector checks that must confirm a head before "
            "--stop-on-confirmed fires (default 2: one check is noise)."
        ),
    )
    parser.add_argument(
        "--no-probe-dissociation",
        dest="probe_dissociation",
        action="store_false",
        help=(
            "Skip the content-vs-position dissociation probe. It is on by "
            "default because, on this periodic task, an on-distribution "
            "measurement cannot tell a content-matching copy circuit from a "
            "positional one."
        ),
    )
    parser.set_defaults(probe_dissociation=True)
    parser.add_argument(
        "--save-manifest",
        action="store_true",
        help=(
            "Write a single-seed results/exp1_induction_heads.json manifest "
            "after the run (implied by --standard)."
        ),
    )
    parser.add_argument(
        "--manifest-path",
        type=str,
        default=None,
        help=(
            "Explicit results/*.json path for the manifest. Defaults to "
            "results/exp1_induction_heads.json. The matched fixed-vs-fresh "
            "comparison needs two manifests, so both arms must pass this."
        ),
    )
    parser.add_argument(
        "--batches",
        choices=["fixed", "fresh"],
        default=None,
        action=_BatchesAction,
        help=(
            "Which training-batch regime to use. `fixed` reuses one dataset for "
            "every epoch (the ill-posed regime); `fresh` draws a new one each "
            "epoch. The matched fixed-vs-fresh comparison is the one solid Rung 1 "
            "finding, so both arms must be runnable with the SAME seeds — pass "
            "--batches to each of the two runs rather than switching globally."
        ),
    )
    parser.set_defaults(fresh_batches=False, batch_mode="fixed")
    return parser


def apply_config_presets(args: argparse.Namespace) -> None:
    """Resolve the named config presets (--quick / --standard / --scale).

    Extracted from main() so the preset matrix is directly testable: every
    preset is a pinned config, and a silent preset regression would otherwise
    only appear as a mysterious run with the wrong shape. `--scale` resolves
    first — `--scale standard` must select the same config `--standard`
    does, not set a flag the `--standard` check has already passed.
    """
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

    if args.scale == "standard":
        args.standard = True
    elif args.scale == "large" and args.standard:
        raise SystemExit(
            "--standard and --scale large select different configs; "
            "pass only --scale large (or only --standard)."
        )

    if args.content_standard and (args.standard or args.quick or args.scale):
        raise SystemExit(
            "--content-standard is its own config: it cannot be combined with "
            "--standard, --quick or --scale. The content task's standard "
            "config differs from the periodic one in the vocabulary, and a "
            "preset that silently overrode another would be a run whose "
            "config nobody chose."
        )

    if args.content_standard:
        # The content task's standard config (the 2026-10-22 amendment).
        # Everything is the standard config except the vocabulary: 256
        # instead of 2048, because the periodic task's 2048 answered a
        # constraint this task does not have (the periodic prefix is sampled
        # with replacement, the content key is not).
        args.vocab_size = 256
        args.seq_len = 64
        args.d_model = 64
        args.n_layers = 2
        args.n_heads = 4
        args.epochs = 3000
        args.num_train = 8192
        args.batch_size = 64
        args.fresh_batches = True
        args.task = TASK_VARIABLE
        if args.checkpoint_every == 0:
            args.checkpoint_every = 250
        args.save_model = True
        args.save_manifest = True
        logger.info(
            "CONTENT STANDARD MODE: the content task's standard config "
            "(vocab=256, seq=64, d_model=64, fresh-batches, epochs=3000) "
            f"// stateful: checkpointing every {args.checkpoint_every} epochs, "
            "model + manifest saved"
        )

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
        # Micro-Phase 12: standard-scale runs are stateful by default — a
        # 3000-epoch run is ~17h on this CPU and must never again vanish
        # without on-disk state (checkpoint, model, manifest).
        if args.checkpoint_every == 0:
            args.checkpoint_every = 250
        args.save_model = True
        args.save_manifest = True
        logger.info(
            "STANDARD MODE: canonical standard-scale config "
            "(vocab=2048, seq=64, d_model=64, fresh-batches, epochs=3000) "
            f"// stateful: checkpointing every {args.checkpoint_every} epochs, "
            "model + manifest saved"
        )

    if args.scale == "large":
        # The scaled GPU config. PR #164 shipped this as a separate exp7
        # module with a hardcoded args namespace; the repo's rule that
        # Rungs 1/4/5 share ONE config made that a drift risk, so the preset
        # lives here and everything else (resume, manifest routing, seeds)
        # is inherited.
        args.vocab_size = 2048
        args.seq_len = 128
        args.d_model = 256
        args.n_layers = 4
        args.n_heads = 8
        args.epochs = 1500
        args.num_train = 16384
        args.batch_size = 128
        args.fresh_batches = True
        if args.checkpoint_every == 0:
            args.checkpoint_every = 500
        args.save_model = True
        args.save_manifest = True
        logger.info(
            "SCALE=large: vocab=2048, seq=128, d_model=256, 4 layers, 8 heads, "
            "fresh-batches, epochs=1500 "
            f"// stateful: checkpointing every {args.checkpoint_every} epochs, "
            "model + manifest saved"
        )


def main() -> None:
    FIGURES_DIR.mkdir(exist_ok=True)
    parser = build_parser()
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )

    apply_config_presets(args)

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
        manifest_path = resolve_manifest_path(
            "exp1_induction_heads",
            Path("results") / "exp1_induction_heads.json",
            args.manifest_path,
            args.quick,
        )
        manifest.save(manifest_path)
        logger.info(f"Saved multi-seed manifest to {manifest_path}")
        for key in result.aggregate:
            logger.info(f"  {key}: {result.summary_line(key)}")
        return

    # Data
    task = getattr(args, "task", TASK_PERIODIC)
    train_dataset, val_dataset = make_task_data(
        args,
        num_train=args.num_train,
        num_val=1024,
        seed=args.seed,
    )
    train_loader = DataLoader(train_dataset, batch_size=args.batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=args.batch_size, shuffle=False)
    logger.info(f"Data: train={len(train_dataset)}, val={len(val_dataset)} | task={task}")

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
        fresh_batches_fn = _make_fresh_batches_fn(args, args.seed) if args.fresh_batches else None

        run_resume_from = None
        if args.resume and args.checkpoint_every > 0:
            run_resume_from = str(checkpoint_path_for_seed(args.checkpoint_dir, "exp1", args.seed))
        elif args.resume_from:
            run_resume_from = args.resume_from
        t_run_start = time.monotonic()

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
            checkpoint_dir=args.checkpoint_dir if args.checkpoint_every > 0 else None,
            checkpoint_every=args.checkpoint_every,
            resume_from=run_resume_from,
            detect_every=args.detect_every,
            stop_on_confirmed=args.stop_on_confirmed,
            stop_rule=args.stop_rule,
            detect_patience=args.detect_patience,
            prefix_len=prefix_length_for(args.seq_len),
            task=task,
        )
        history["steps_per_epoch"] = float(len(train_loader))

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
        induction_mass = np.array(history["induction_mass"])
        if len(val_accs) > 100:
            val_smooth = np.convolve(val_accs, np.ones(10) / 10, mode="valid")
            max_smooth_idx = np.argmax(val_smooth)
            loss_bump_idx = np.argmax(np.abs(np.diff(history["val_loss"])))
            logger.info(
                f"Loss bump at epoch ~{loss_bump_idx} | "
                f"Peak smoothed val acc: {val_smooth[max_smooth_idx]:.4f} "
                f"at epoch ~{max_smooth_idx * 10}"
            )
        if len(induction_mass) > 100:
            peak_induction = np.argmax(induction_mass)
            induction_at_end = induction_mass[-1]
            logger.info(
                f"Peak induction mass at epoch {peak_induction} "
                f"(value: {induction_mass[peak_induction]:.3f}) | "
                f"Final induction mass: {induction_at_end:.3f}"
            )

    # Analyze induction heads
    prefix_len = prefix_length_for(args.seq_len)
    report, all_patterns, tokens = analyze_induction_heads_full(
        model, val_loader, prefix_len=prefix_len, task=task
    )
    induction_heads = report.confirmed

    # K-composition diagnostic (Nanda & Jacobsen): the "how far did the model
    # get" instrument — Step 1 (L0 duplicate-token head) and Step 2
    # (K-composition) are reported independently so a missing induction head
    # is measured, not just counted.
    diagnosis = diagnose_induction_formation(
        all_patterns, tokens=tokens, prefix_len=prefix_len, task=task
    )
    if diagnosis["best_l0_head"] >= 0:
        step1 = max(diagnosis["step1_l0_duplicate_mass"])
        logger.info("-" * 60)
        logger.info("How far did the model get? (Nanda & Jacobsen two-step path)")
        logger.info(
            f"Step 1 — L0 duplicate-token head: max duplicate-offset mass {step1:.3f} "
            f"(peakedness {diagnosis['l0_peakedness']:.3f})"
        )
        logger.info(
            f"Step 2 — K-composition: best score {diagnosis['step2_k_composition']:.3f} "
            f"(L0 head {diagnosis['best_l0_head']}, L1 head {diagnosis['best_l1_head']})"
        )
        plot_composition_diagnostic(all_patterns, diagnosis, FIGURES_DIR / "exp1_k_composition.png")

    logger.info("=" * 60)
    logger.info("Induction Head Analysis")
    logger.info("=" * 60)

    for layer_idx, heads in enumerate(induction_heads):
        logger.info(f"Layer {layer_idx}: {len(heads)} induction head(s): {heads}")
        for head_idx in heads[:2]:  # plot first 2 per layer
            plot_induction_pattern(
                all_patterns,
                layer=layer_idx,
                head=head_idx,
                save_path=(FIGURES_DIR / f"exp1_induction_pattern_L{layer_idx}H{head_idx}.png"),
            )

    total_induction = sum(len(h) for h in induction_heads)
    logger.info(f"Total induction heads: {total_induction} / {args.n_layers * args.n_heads}")
    logger.info(
        f"Screen (induction mass > {INDUCTION_MASS_THRESHOLD}): "
        f"{report.screen_count} | prev-token control peak: "
        f"{report.peak('prev_token'):.3f} | induction peak: "
        f"{report.peak('induction'):.3f} | best composition: "
        f"{report.best_composition:.3f}"
    )

    # The naming test. On the periodic task the content-vs-position
    # dissociation needs an off-distribution batch; on the variable task the
    # dissociation is native and the probe measures it in distribution.
    probe = None
    if args.probe_dissociation:
        probe = _run_task_probe(model, args, val_loader, seed=args.seed)
        logger.info(
            "Dissociation probe — content mass "
            f"{probe['peak_content_mass']:.3f} vs positional mass "
            f"{probe.get('peak_offset_mass', probe.get('peak_period_mass', 0.0)):.3f} -> "
            f"{'CONTENT-based' if probe['content_wins'] else 'POSITIONAL'} copy"
        )

    # The behavioural half of the claim: how well does the model copy, and
    # is the copy explained by a fixed offset?
    copy_stats = analyze_copy_metrics(model, val_loader)
    logger.info(
        f"Copy metrics — copy accuracy {copy_stats['copy_accuracy']:.4f} "
        f"(non-modal distance group: {copy_stats['copy_accuracy_nonmodal']:.4f}) | "
        f"best fixed-offset baseline {copy_stats['fixed_offset_baseline']:.4f} "
        f"at d={copy_stats['fixed_offset_best_d']:.0f} | "
        f"{copy_stats['n_distances']:.0f} distinct distances, "
        f"{copy_stats['n_copy_queries']:.0f} copy queries"
    )

    if total_induction == 0:
        logger.warning(
            "No induction head confirmed. Try: longer training, or lower threshold in detection."
        )
    else:
        logger.info("✓ Induction heads successfully identified!")
        logger.info("Running causal ablation to verify...")

        # Ablate each detected induction head and measure accuracy drop
        for layer_idx, heads in enumerate(induction_heads):
            for head_idx in heads:
                full_acc = history["val_acc"][-1] if not args.no_train else 0.0
                ablated_acc = causal_ablation(model, val_loader, layer_idx, head_idx)
                logger.info(
                    f"Ablation L{layer_idx}H{head_idx}: "
                    f"accuracy {full_acc:.4f} → {ablated_acc:.4f} "
                    f"(drop: {full_acc - ablated_acc:+.4f})"
                )

    # Micro-Phase 12: provenance for the single-seed standard run — the
    # headline manifest, same file `--seeds` writes, so RESULTS.md's tag
    # always points at the newest honest run.
    if not args.no_train and args.save_manifest:
        metrics = _seed_metrics(
            model,
            val_loader,
            history,
            induction_heads,
            diagnosis,
            report,
            probe,
            copy_stats,
            tokens,
            task,
        )
        _write_single_manifest(args, metrics, time.monotonic() - t_run_start)


if __name__ == "__main__":
    main()
