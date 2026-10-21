"""Rung 4 — Circuit verification via activation patching on induction heads.

Trains (or loads) a transformer on repeated-token prediction, identifies
induction heads, then runs activation patching to causally validate the
circuit. Reports faithfulness and ablates individual components.

The model this rung analyses is, by default, **the model Rung 1 trained**:
`--from-checkpoint` loads exp1's rolling checkpoint instead of training a
second, different model. That is what makes the "one shared model" cascade
true — the previous behaviour (train a fresh `DecoderOnlyTransformer` here
while claiming to match exp1's `AttentionOnlyTransformer` config) produced
two different models under one claim, and the parity test that should have
caught it only compared hyper-parameters, not architecture or step count.

Usage:
    python -m src.experiments.exp4_circuit_patching --seed 42 [--quick]
    python -m src.experiments.exp4_circuit_patching --from-checkpoint \
        checkpoints/induction_standard/exp1_checkpoint_seed0.pt \
        --source-vocab-size 2048 --source-seq-len 64 --source-d-model 64 \
        --source-n-layers 2 --source-n-heads 4

Output:
    - figures/exp4_attention_patterns.png
    - figures/exp4_patching_results.png
    - figures/exp4_head_ablation.png
    - Console: circuit components, logit-diff recovery, faithfulness scores
"""

import argparse
import logging
from collections.abc import Callable
from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt
import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader
from tqdm import tqdm

from src.experiments.checkpointing import load_training_checkpoint
from src.experiments.exp1_induction_heads import (
    AttentionOnlyTransformer,
    _BatchesAction,
    _FreshBatchesAction,
    _make_fresh_batches_fn,
)
from src.experiments.induction_detection import (
    COMPOSITION_THRESHOLD,
    INDUCTION_MASS_THRESHOLD,
    detect_from_inputs,
    prefix_length_for,
    run_content_vs_offset_probe,
    run_dissociation_probe,
)
from src.experiments.induction_tasks import (
    TASK_PERIODIC,
    TASK_VARIABLE,
    TaskSpec,
    copy_query_batch,
    task_datasets,
)
from src.experiments.runner import parse_seeds, run_seeds
from src.models.decoder_only_transformer import DecoderOnlyTransformer
from src.reproducibility import set_seed
from src.results import ResultsManifest, count_parameters, resolve_manifest_path

logger = logging.getLogger(__name__)

FIGURES_DIR = Path("figures")

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def _task_spec(
    task: str,
    vocab_size: int,
    seq_len: int,
    key_len: Optional[int] = None,
    copy_blocks: Optional[int] = None,
    copy_block_len: Optional[int] = None,
) -> TaskSpec:
    """The task of the model this rung analyses.

    With ``--from-checkpoint`` the data must be generated with the
    *source* config, not with this rung's own flags: a checkpoint trained
    on the variable-distance task is analysed on variable-distance data,
    and one trained on the periodic task on periodic data.
    """
    if task != TASK_VARIABLE:
        return TaskSpec.periodic(vocab_size=vocab_size, seq_len=seq_len)
    from src.experiments.exp1_induction_heads import default_variable_geometry

    default_key, default_blocks, default_block = default_variable_geometry(seq_len)
    return TaskSpec.variable(
        vocab_size=vocab_size,
        seq_len=seq_len,
        key_len=key_len or default_key,
        copy_blocks=copy_blocks or default_blocks,
        copy_block_len=copy_block_len or default_block,
    )


def _run_task_probe(
    model: nn.Module,
    task: str,
    vocab_size: int,
    seq_len: int,
    seed: int,
    tokens: Optional[torch.Tensor] = None,
) -> dict:
    """The naming test of the task, in the task's own terms.

    The periodic task needs an off-distribution batch (its content target
    and its fixed offset are the same key in distribution); the
    variable-distance task does not, because its repeats sit at different
    distances by construction.
    """
    if task == TASK_VARIABLE:
        if tokens is None:
            raise ValueError("the variable-task probe needs the task's tokens")
        return run_content_vs_offset_probe(model, tokens)
    return run_dissociation_probe(
        model, vocab_size=vocab_size, seq_len=seq_len, num_samples=32, seed=seed
    )





# ---------------------------------------------------------------------------
# Model-family adapters
# ---------------------------------------------------------------------------
# Rung 1 trains an `AttentionOnlyTransformer` (LayerNorm, learned positional
# embeddings, no MLP); exp4's own training path uses the shared
# `DecoderOnlyTransformer` (RMSNorm, RoPE, MLP). The interventions below are
# written against the *cache* protocol both models implement, so the same
# code validates either family — and `--from-checkpoint` can therefore point
# at the very model Rung 1 trained.
def _forward_varnames(model: nn.Module) -> tuple:
    """The *parameters* of `model.forward`.

    `__code__.co_varnames` would also list local variables — and
    `DecoderOnlyTransformer.forward` has a local named `cache` while its
    signature only offers `return_cache` — so the parameter list is the
    only honest source here.
    """
    import inspect

    forward = getattr(model, "forward", None)
    if forward is None:
        return ()
    try:
        return tuple(inspect.signature(forward).parameters)
    except (TypeError, ValueError):  # pragma: no cover - exotic callables
        return ()


def _forward_with_cache(model: nn.Module, inputs: torch.Tensor) -> tuple:
    """`(logits, cache)` for either model family.

    `AttentionOnlyTransformer` fills the `cache` dict it is handed;
    `DecoderOnlyTransformer` returns its own cache. Both use the same key
    names (`blocks.{i}.resid_pre`, `blocks.{i}.attn.attn_probs`,
    `blocks.{i}.attn.V`, `blocks.{i}.resid_mid`, `blocks.{i}.resid_post`).
    """
    if "cache" in _forward_varnames(model):
        cache: dict = {}
        out = model(inputs, cache=cache)
        logits = out[0] if isinstance(out, tuple) else out
        return logits, cache
    out = model(inputs, return_cache=True)
    return out[0], out[1]


def _attn_module(model: nn.Module, layer: int) -> nn.Module:
    """The attention module of a layer, for either family.

    `DecoderOnlyTransformer` nests it (`blocks[i].attn`); the attention-only
    block *is* the attention module (`blocks[i]`).
    """
    block = model.blocks[layer]
    return getattr(block, "attn", block)


def _is_attention_only(model: nn.Module) -> bool:
    """True for the attention-only family (no MLP branch to keep clean)."""
    return not hasattr(getattr(model, "blocks", [])[0], "attn")


def _model_device(model: nn.Module) -> torch.device:
    """The device the model lives on.

    The interventions used to assume the caller had already moved every
    tensor to `DEVICE`. The cascade does not: it hands the interventions the
    validation tensors as the dataset produced them (CPU), while the model
    lives on the GPU. That mismatch is a hard error on CUDA ("Expected all
    tensors to be on the same device") and it is why the first GPU cascade
    run died in the patching step.
    """
    try:
        return next(model.parameters()).device
    except StopIteration:  # pragma: no cover - parameterless models
        return torch.device("cpu")


def _install_resid_mid_patch(
    model: nn.Module,
    layer: int,
    pos: int,
    target_resid_mid: torch.Tensor,
    resid_pre: torch.Tensor,
):
    """Hook that makes the layer's mid-residual equal `target_resid_mid` at
    position `pos`.

    Two families, one intervention:

    * `DecoderOnlyTransformer` — the attention branch is its own module and
      its output is added to the residual stream. Replacing that output with
      `target - resid_pre` makes the mid-residual the target *and* lets the
      MLP branch see the patched value.
    * `AttentionOnlyTransformer` — the block's output *is*
      `resid_pre + attn_out` (there is no MLP), so replacing the block
      output at the target position is the exact analogue of the same
      intervention.
    """
    attn_module = _attn_module(model, layer)
    if _is_attention_only(model):

        def hook(module, input, output):
            out = output.clone()
            out[:, pos : pos + 1, :] = target_resid_mid
            return out

    else:

        def hook(module, input, output):
            attn_out, kv = output
            attn_out = attn_out.clone()
            attn_out[:, pos : pos + 1, :] = target_resid_mid - resid_pre
            return (attn_out, kv)

    return attn_module.register_forward_hook(hook)


@torch.no_grad()
def compute_attention_patterns(
    model: nn.Module, inputs: torch.Tensor
) -> tuple[dict, dict]:
    """Per-layer attention probabilities averaged over heads, plus the raw cache.

    Returns a tuple `(probs, cache)`, not a bare dict — the annotation used to
    say `-> dict` while the body returned two values, and every caller unpacks
    it as a tuple. The annotation was the lie, not the callers.
    """
    model.eval()
    # Only the hook cache is needed here; the logits are discarded.
    _, cache = _forward_with_cache(model, inputs[:8])
    probs = {}
    for layer in range(len(getattr(model, "blocks", []))):
        prefix = f"blocks.{layer}.attn"
        attn_probs = cache[f"{prefix}.attn_probs"]
        probs[f"layer_{layer}"] = attn_probs.mean(dim=1)  # avg over heads
    return probs, cache


def detect_induction_heads(
    model: nn.Module,
    inputs: torch.Tensor,
    threshold: float = INDUCTION_MASS_THRESHOLD,
    prefix_len: Optional[int] = None,
    composition_threshold: float = COMPOSITION_THRESHOLD,
    task: str = TASK_PERIODIC,
) -> list[tuple[int, int]]:
    """Detect induction heads by their attention pattern.

    The detection is the shared one (`src.experiments.induction_detection`):
    the head must put enough mass on the task's **copy key** — the
    key holding the token after the previous occurrence of the current token
    — and its layer must be composed with an earlier layer.

    The previous implementation measured `attn_probs.diagonal(offset=1)`,
    the strict upper triangle of a causal softmax: exactly zero, always.
    That is why this rung reported "0 / 4 induction heads" and skipped
    ablation and path patching for every run it ever made.

    On the periodic task the copy key is the fixed offset `q - (L-1)`; on
    the variable-distance task it is `prev(q) + 1`, which is not a fixed
    offset at all (ADR-0033). The task is a parameter, not an assumption.
    """
    report, _patterns = detect_from_inputs(
        model,
        inputs,
        prefix_len=prefix_len,
        mass_threshold=threshold,
        composition_threshold=composition_threshold,
        task=task,
    )
    return [
        (layer, head)
        for layer, heads in enumerate(report.confirmed)
        for head in heads
    ]


def train_model(
    model: nn.Module,
    train_loader: DataLoader,
    val_loader: DataLoader,
    epochs: int = 2000,
    lr: float = 1e-3,
    weight_decay: float = 0.1,
    seed: int = 42,
    gradient_clip: float = 1.0,
    fresh_batches_fn: Optional[Callable[[int], DataLoader]] = None,
) -> dict:
    """Train the model and return history.

    `fresh_batches_fn`, if given, is called once per epoch with the epoch
    index and must return a fresh DataLoader over a newly sampled set of
    sequences — the regime exp1's `--standard`/`--scale large` presets
    force, because the 2026-08-02 matched comparison found the fixed,
    epoch-reused dataset actively harmful (0.45% vs 53.5% val accuracy;
    see portfolio/RESULTS.md Rung 1). Without it this experiment's
    "standard" config trained on the harmful regime while claiming to
    match exp1's, and the Rung 1 -> Rung 4 cascade measured a different
    model than the one Rung 1 trained.
    """
    set_seed(seed)
    model.train()
    opt = torch.optim.AdamW(
        model.parameters(), lr=lr, weight_decay=weight_decay
    )
    history = {"train_loss": [], "val_loss": [], "val_acc": []}

    for epoch in tqdm(range(epochs), desc="Training"):
        model.train()
        if fresh_batches_fn is not None:
            train_loader = fresh_batches_fn(epoch)
        total_loss = 0.0
        for x, y in train_loader:
            opt.zero_grad()
            logits, _ = model(x)
            loss = nn.functional.cross_entropy(
                logits.view(-1, logits.size(-1)), y.view(-1)
            )
            loss.backward()
            # Gradient clipping, now that it is a parameter. exp4 used to
            # train with no clipping at all while exp2 and exp6 both apply
            # `gradient_clip` from config — the same adamw + wd recipe with an
            # unbounded step is a different experiment, not a matched one.
            if gradient_clip and gradient_clip > 0:
                nn.utils.clip_grad_norm_(model.parameters(), gradient_clip)
            opt.step()
            total_loss += loss.item()

        model.eval()
        val_loss_sum = 0.0
        val_tokens = 0
        correct = 0
        total = 0
        with torch.no_grad():
            for x, y in val_loader:
                logits, _ = model(x)
                # Per-token loss, weighted by batch size. The old code divided
                # the summed per-batch means by len(val_loader), which is a mean
                # of means: every batch counts equally regardless of size, so
                # the last (usually smaller) batch was over-weighted and
                # exp4's val_loss was not comparable with exp1's/exp2's.
                loss = nn.functional.cross_entropy(
                    logits.view(-1, logits.size(-1)), y.view(-1), reduction="sum"
                )
                val_loss_sum += loss.item()
                val_tokens += y.numel()
                preds = logits.argmax(dim=-1)
                correct += (preds == y).sum().item()
                total += y.numel()

        history["train_loss"].append(total_loss / len(train_loader))
        history["val_loss"].append(val_loss_sum / max(1, val_tokens))
        history["val_acc"].append(correct / total)

        if (epoch + 1) % 200 == 0:
            logger.info(
                f"Epoch {epoch+1:4d} | train loss: {history['train_loss'][-1]:.4f} "
                f"| val loss: {history['val_loss'][-1]:.4f} "
                f"| val acc: {history['val_acc'][-1]:.4f}"
            )

    return history


def run_activation_patching(
    model: nn.Module,
    clean_inputs: torch.Tensor,
    clean_answers: torch.Tensor,
    corrupted_inputs: torch.Tensor,
    corrupted_answers: torch.Tensor,
    layers_to_patch: list[int],
    positions_to_patch: list[int],
    batch_size: int = 32,
    pos: int = -1,
) -> dict:
    """Run residual stream activation patching.

    For each (layer, position), overrides resid_mid at that position with its
    value from a corrupted run, then measures how much of the logit
    difference (clean answer vs. counterfactual answer) is recovered.

    The patch is injected via a forward hook on the block's *attention*
    module (which returns the already-projected, post-W_O `attn_out` — see
    Attention.forward). The hook solves for the `attn_out` that makes
    `resid_pre + attn_out == corrupted_resid_mid` at the target position, so
    both the MLP branch *and* the residual skip see the patched value. A
    previous version hooked the MLP's pre-forward input instead: the MLP's
    input is `ln_mlp(resid_mid)` (normalized), and the residual skip
    (`x = x + mlp_out`) still referenced the block's own unpatched `x` — so
    that version silently patched nothing but the MLP's own view of an
    un-normalized tensor.

    `clean_answers` / `corrupted_answers` are the true next-token labels for
    each input under the induction task (see make_repeated_token_data) — the
    token the model should predict at the last position if the induction
    mechanism is intact. logit_diff = logits[answer] - logits[counterfactual]
    is the standard answer-vs-counterfactual metric (Wang et al., IOI), not a
    top1-top2 confidence margin, which conflates "confident about the right
    answer" with "confident about anything."

    Returns:
        dict mapping (layer, position) -> (clean_diff, patched_diff, recovery)
    """
    model.eval()
    results: dict = {}
    device = _model_device(model)
    clean_inputs = clean_inputs.to(device)
    corrupted_inputs = corrupted_inputs.to(device)
    batch_size = min(batch_size, clean_inputs.size(0), corrupted_inputs.size(0))

    with torch.no_grad():
        clean_logits, clean_cache = _forward_with_cache(model, clean_inputs[:batch_size])
        _, corrupted_cache = _forward_with_cache(model, corrupted_inputs[:batch_size])

    answer = clean_answers[:batch_size].to(device)
    counterfactual = corrupted_answers[:batch_size].to(device)
    idx = torch.arange(batch_size, device=device)

    def logit_diff(logits: torch.Tensor) -> torch.Tensor:
        # `pos` is the position the answer and the counterfactual belong
        # to. It defaults to the last position, which is a copy query on
        # the periodic task; on the variable-distance task the copy
        # queries sit at different positions per sequence, so the caller
        # passes the position it patched (and read) at.
        #
        # The read position is captured in a local of its own: the patch
        # loop below iterates over `positions_to_patch`, and a loop
        # variable named `pos` shadows this parameter, so the metric ends
        # up reading the *last patched* position instead of the one the
        # answer belongs to. That bug reached `main` and was caught by the
        # Pages workflow's `make reproduce-quick` (on a short sequence the
        # last patched position is out of range for the logits).
        read_at = pos if pos >= 0 else logits.shape[1] - 1
        at_logits = logits[:, read_at, :]
        return at_logits[idx, answer] - at_logits[idx, counterfactual]

    clean_diff = logit_diff(clean_logits).mean().item()
    logger.info(f"Clean logit diff (answer - counterfactual): {clean_diff:.4f}")

    for layer in tqdm(layers_to_patch, desc="Patching layers"):
        resid_pre = clean_cache[f"blocks.{layer}.resid_pre"].to(DEVICE)
        corrupted_resid_mid = corrupted_cache[f"blocks.{layer}.resid_mid"].to(DEVICE)

        for patch_pos in positions_to_patch:
            target = corrupted_resid_mid[:, patch_pos:patch_pos + 1, :]
            pre = resid_pre[:, patch_pos:patch_pos + 1, :]

            hook_handle = _install_resid_mid_patch(
                model, layer, patch_pos, target, pre
            )

            with torch.no_grad():
                patched_logits, _ = _forward_with_cache(model, clean_inputs[:batch_size])

            hook_handle.remove()

            patched_diff = logit_diff(patched_logits).mean().item()
            recovery = (patched_diff - clean_diff) / (-clean_diff) if clean_diff != 0 else 0.0
            results[(layer, patch_pos)] = {
                "clean_diff": clean_diff,
                "patched_diff": patched_diff,
                "recovery": recovery,
            }

    return results


def run_path_patching_to_logits(
    model: nn.Module,
    clean_inputs: torch.Tensor,
    clean_answers: torch.Tensor,
    corrupted_inputs: torch.Tensor,
    corrupted_answers: torch.Tensor,
    heads: list[tuple[int, int]],
    pos: int = -1,
    batch_size: int = 32,
) -> dict:
    """Path-patch a single head's *direct* contribution to the logits.

    Unlike activation patching (which corrupts resid_mid and lets the
    corruption propagate through every downstream layer), path patching to
    the logits isolates one head's direct effect: every other head, every
    MLP, and this head's own *indirect* effect through later layers stay at
    their clean values. Only the direct term this head adds to the final
    residual stream is swapped for its corrupted-run value.

    A head's post-W_O contribution is linearly separable: attn_out at a
    layer is `W_O(concat_h(head_h_out))`, and W_O applied to a concatenation
    is the sum of each head's slice through the matching column-block of
    W_O.weight. So `direct_effect_h = head_h_out @ W_O.weight[:, h_slice].T`.

    `pos` defaults to the last position, matching `clean_answers` /
    `corrupted_answers` (which are the next-token labels *for the last
    position* — see make_repeated_token_data). Passing a different `pos`
    without also supplying labels for that position is not meaningful.

    Returns:
        dict mapping (layer, head) -> (clean_diff, patched_diff, effect)
    """
    model.eval()
    results: dict = {}
    device = _model_device(model)
    clean_inputs = clean_inputs.to(device)
    corrupted_inputs = corrupted_inputs.to(device)
    batch_size = min(batch_size, clean_inputs.size(0), corrupted_inputs.size(0))
    n_layers = len(getattr(model, "blocks", []))

    with torch.no_grad():
        clean_logits, clean_cache = _forward_with_cache(model, clean_inputs[:batch_size])
        _, corrupted_cache = _forward_with_cache(model, corrupted_inputs[:batch_size])

    answer = clean_answers[:batch_size].to(device)
    counterfactual = corrupted_answers[:batch_size].to(device)
    idx = torch.arange(batch_size, device=device)

    def logit_diff(logits: torch.Tensor) -> torch.Tensor:
        # Read at `pos`, not always the last position: since ln_final/unembed
        # are per-position operations with no further cross-position mixing,
        # patching resid_final at `pos` only changes logits at that position.
        pos_logits = logits[:, pos, :]
        return pos_logits[idx, answer] - pos_logits[idx, counterfactual]

    clean_diff = logit_diff(clean_logits).mean().item()
    resid_final = clean_cache[f"blocks.{n_layers - 1}.resid_post"].to(DEVICE)

    for layer, head in tqdm(heads, desc="Path patching heads → logits"):
        attn_module = _attn_module(model, layer)
        d_head = attn_module.d_head
        w_o_head = attn_module.W_O.weight[:, head * d_head:(head + 1) * d_head]  # (d_model, d_head)

        probs_clean = clean_cache[f"blocks.{layer}.attn.attn_probs"].to(DEVICE)
        v_clean = clean_cache[f"blocks.{layer}.attn.V"].to(DEVICE)
        probs_corrupt = corrupted_cache[f"blocks.{layer}.attn.attn_probs"].to(DEVICE)
        v_corrupt = corrupted_cache[f"blocks.{layer}.attn.V"].to(DEVICE)

        head_out_clean = (probs_clean[:, head] @ v_clean[:, head])[:, pos, :]
        head_out_corrupt = (probs_corrupt[:, head] @ v_corrupt[:, head])[:, pos, :]

        direct_delta = (head_out_corrupt - head_out_clean) @ w_o_head.T
        patched_resid_final = resid_final.clone()
        patched_resid_final[:, pos, :] = patched_resid_final[:, pos, :] + direct_delta

        with torch.no_grad():
            h = model.ln_final(patched_resid_final)
            patched_logits = model.unembed(h)

        patched_diff = logit_diff(patched_logits).mean().item()
        effect = (clean_diff - patched_diff) / clean_diff if clean_diff != 0 else 0.0
        results[(layer, head)] = {
            "clean_diff": clean_diff,
            "patched_diff": patched_diff,
            "effect": effect,
        }

    return results


def run_head_ablation(
    model: nn.Module,
    inputs: torch.Tensor,
    answers: torch.Tensor,
    counterfactuals: torch.Tensor,
    induction_heads: list[tuple[int, int]],
    batch_size: int = 32,
    pos: int = -1,
) -> dict:
    """Zero-ablate individual induction heads and measure effect.

    Uses head_mask on the Attention module to zero a specific head's
    contribution before the W_O projection — clean, no shape issues.

    logit_diff = logits[answer] - logits[counterfactual] (see
    run_activation_patching's docstring for why this replaces a top1-top2
    confidence margin).
    """
    model.eval()
    results: dict = {}
    device = _model_device(model)
    inputs = inputs.to(device)
    batch_size = min(batch_size, inputs.size(0))

    with torch.no_grad():
        clean_logits, _ = model(inputs[:batch_size])

    answer = answers[:batch_size].to(device)
    counterfactual = counterfactuals[:batch_size].to(device)
    idx = torch.arange(batch_size, device=device)

    def logit_diff(logits: torch.Tensor) -> torch.Tensor:
        read_at = pos if pos >= 0 else logits.shape[1] - 1
        at_logits = logits[:, read_at, :]
        return at_logits[idx, answer] - at_logits[idx, counterfactual]

    clean_diff = logit_diff(clean_logits).mean().item()

    for layer, head in tqdm(induction_heads, desc="Ablating heads"):
        attn_module = _attn_module(model, layer)
        mask = torch.ones(attn_module.n_heads)
        mask[head] = 0.0
        attn_module.head_mask = mask

        with torch.no_grad():
            ablated_logits, _ = model(inputs[:batch_size])

        attn_module.head_mask = None

        ablated_diff = logit_diff(ablated_logits).mean().item()
        effect = (ablated_diff - clean_diff) / (-clean_diff) if clean_diff != 0 else 0.0
        results[(layer, head)] = {
            "clean_diff": clean_diff,
            "ablated_diff": ablated_diff,
            "effect": effect,
        }

    return results


def plot_attention_patterns(
    attention_probs: dict,
    save_path: Path,
    max_layers: int = 2,
) -> None:
    """Plot attention probability matrices for each layer."""
    n_layers = min(len(attention_probs), max_layers)
    fig, axes = plt.subplots(1, n_layers, figsize=(6 * n_layers, 5))

    if n_layers == 1:
        axes = [axes]

    for i in range(n_layers):
        key = f"layer_{i}"
        if key not in attention_probs:
            continue
        probs = attention_probs[key][0].numpy()
        im = axes[i].imshow(probs, cmap="Blues", aspect="auto", vmin=0, vmax=0.5)
        axes[i].set_title(f"Layer {i} — Attention (avg over heads)", fontsize=13)
        axes[i].set_xlabel("Key position")
        axes[i].set_ylabel("Query position")
        fig.colorbar(im, ax=axes[i], shrink=0.8)

    fig.tight_layout()
    fig.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    logger.info(f"Saved attention patterns to {save_path}")


def plot_patching_results(
    results: dict,
    n_layers: int,
    n_positions: int,
    save_path: Path,
) -> None:
    """Plot activation patching heatmap."""
    positions = sorted(set(k[1] for k in results))
    layers = sorted(set(k[0] for k in results))

    matrix = np.zeros((len(layers), len(positions)))
    for (l, p), v in results.items():
        li = layers.index(l)
        pi = positions.index(p)
        matrix[li, pi] = v["recovery"]

    fig, ax = plt.subplots(figsize=(10, 6))
    vmax = max(abs(matrix.min()), abs(matrix.max()), 0.01)
    im = ax.imshow(matrix, cmap="RdYlBu_r", aspect="auto", vmin=-vmax, vmax=vmax)
    ax.set_xticks(range(len(positions)))
    ax.set_xticklabels([f"Pos {p}" for p in positions])
    ax.set_yticks(range(len(layers)))
    ax.set_yticklabels([f"Layer {l}" for l in layers])
    ax.set_xlabel("Token Position")
    ax.set_ylabel("Layer")
    ax.set_title("Activation Patching — Logit-diff Recovery", fontsize=14)
    fig.colorbar(im, ax=ax, shrink=0.8, label="Recovery (1 = circuit essential)")

    fig.tight_layout()
    fig.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    logger.info(f"Saved patching results to {save_path}")


def plot_head_ablation(
    results: dict,
    save_path: Path,
) -> None:
    """Plot head ablation effects."""
    heads = sorted(results.keys(), key=lambda x: (x[0], x[1]))
    labels = [f"L{h[0]}.H{h[1]}" for h in heads]
    effects = [results[h]["effect"] for h in heads]

    fig, ax = plt.subplots(figsize=(8, 4))
    colors = ["crimson" if e > 0.1 else "gray" for e in effects]
    ax.bar(range(len(labels)), effects, color=colors)
    ax.axhline(y=0.1, color="red", linestyle="--", alpha=0.5, label="Significant threshold")
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=45)
    ax.set_ylabel("Logit-diff drop (fraction)")
    ax.set_title("Head Ablation — Causal Effect on Induction", fontsize=14)
    ax.legend()
    ax.grid(True, axis="y", alpha=0.3)

    fig.tight_layout()
    fig.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    logger.info(f"Saved head ablation plot to {save_path}")


# ---------------------------------------------------------------------------
# Multi-seed headline run
# ---------------------------------------------------------------------------
def _checkpoint_for_seed(args: argparse.Namespace, seed: int) -> Optional[Path]:
    """The checkpoint this seed should load, if any.

    `--from-checkpoint` accepts either a file or a *directory* of exp1's
    rolling per-seed checkpoints (`exp1_checkpoint_seed<N>.pt`), which is
    what the GPU cascade produces.
    """
    raw = getattr(args, "from_checkpoint", None)
    if not raw:
        return None
    path = Path(raw)
    if path.is_dir():
        return path / f"exp1_checkpoint_seed{seed}.pt"
    return path


def _build_model(
    args: argparse.Namespace, seed: int, load_weights: bool = True
) -> tuple[nn.Module, Optional[dict]]:
    """The model this rung analyses.

    With `--from-checkpoint` it is **the model Rung 1 trained** (an
    `AttentionOnlyTransformer`), loaded from disk and *not* retrained —
    which is what makes the cascade a single model instead of two. Without
    it, exp4 keeps its own training path (`DecoderOnlyTransformer`).

    The state-dict load is strict: a mismatched architecture raises rather
    than silently loading a partially-compatible model.

    Returns the model and a small provenance dict (`path`, `epoch`) — the
    epoch matters because the rolling checkpoint can be up to
    `--checkpoint-every` epochs behind the run that wrote it, and the
    manifest has to say which model was actually analysed.
    """
    checkpoint = _checkpoint_for_seed(args, seed)
    if checkpoint is None:
        model = DecoderOnlyTransformer(
            vocab_size=args.vocab_size,
            d_model=args.d_model,
            n_layers=args.n_layers,
            n_heads=args.n_heads,
            max_seq_len=args.seq_len,
        )
        return model, None

    model = AttentionOnlyTransformer(
        vocab_size=args.source_vocab_size,
        d_model=args.source_d_model,
        n_layers=args.source_n_layers,
        n_heads=args.source_n_heads,
        max_seq_len=args.source_seq_len,
    )
    if not load_weights:
        return model, {"path": str(checkpoint), "epoch": -1}
    if not checkpoint.exists():
        raise SystemExit(
            f"--from-checkpoint: {checkpoint} does not exist. The cascade "
            "needs exp1's rolling checkpoint (run exp1 with "
            "--checkpoint-dir/--checkpoint-every first)."
        )
    state = load_training_checkpoint(checkpoint, map_location="cpu")
    if state is None or "model" not in state:
        raise SystemExit(f"--from-checkpoint: {checkpoint} is not a training checkpoint")
    arch = state.get("arch")
    if arch:
        expected = {
            "vocab_size": args.source_vocab_size,
            "d_model": args.source_d_model,
            "n_layers": args.source_n_layers,
            "n_heads": args.source_n_heads,
            "max_seq_len": args.source_seq_len,
        }
        mismatched = {
            k: (arch.get(k), v) for k, v in expected.items() if arch.get(k) != v
        }
        if mismatched:
            raise SystemExit(
                f"--from-checkpoint: {checkpoint} was trained with {arch}, but "
                f"--source-* says {expected}. Fix the source flags."
            )
    # Strict load: a checkpoint without metadata still fails loudly (on the
    # shapes) rather than loading a partially-compatible model.
    model.load_state_dict(state["model"])
    epoch = int(state.get("epoch", -1)) + 1
    logger.info(
        f"Loaded checkpoint {checkpoint} (epoch {epoch}, no training in this rung)"
    )
    return model, {"path": str(checkpoint), "epoch": epoch}


def run_single_seed(seed: int, args: argparse.Namespace) -> dict[str, float]:
    """Train (or load) one circuit-patching run end-to-end and return
    headline metrics for one seed. Mirrors main()'s single-seed
    data/model/train/analysis steps (detection, activation patching, head
    ablation, path patching), minus plotting — used by `--seeds` to aggregate
    across seeds via `src.experiments.runner.run_seeds`. Path patching only
    runs when at least one induction head is detected for that seed (it
    needs a real head to patch); its metric is 0.0 for seeds with none, same
    convention as head ablation.
    """
    model, checkpoint = _build_model(args, seed)
    model.to(DEVICE)

    # With a checkpoint, the data must be generated with the *source* config
    # (vocab/seq_len), not with this rung's own flags.
    task = getattr(args, "source_task", TASK_PERIODIC)
    if checkpoint is not None:
        vocab_size = args.source_vocab_size
        seq_len = args.source_seq_len
    else:
        vocab_size = args.vocab_size
        seq_len = args.seq_len
    spec = _task_spec(
        task,
        vocab_size,
        seq_len,
        key_len=getattr(args, "source_key_len", None),
        copy_blocks=getattr(args, "source_copy_blocks", None),
        copy_block_len=getattr(args, "source_copy_block_len", None),
    )
    train_dataset, val_dataset = task_datasets(spec, args.num_train, 1024, seed)
    train_loader = DataLoader(train_dataset, batch_size=args.batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=256, shuffle=False)

    # Same fresh-batches regime as exp1's presets so the cascade measures
    # one shared model (see train_model's docstring).
    fresh_batches_fn = _make_fresh_batches_fn(args, seed) if args.fresh_batches else None

    if checkpoint is not None:
        history = {"train_loss": [], "val_loss": [], "val_acc": []}
        with torch.no_grad():
            logits, _ = model(val_loader.dataset.tensors[0][:32].to(DEVICE))
            labels = val_loader.dataset.tensors[1][:32].to(DEVICE)
            history["val_acc"].append(
                float((logits.argmax(-1) == labels).float().mean().item())
            )
            history["val_loss"].append(0.0)
            history["train_loss"].append(0.0)
    else:
        history = train_model(
            model=model,
            train_loader=train_loader,
            val_loader=val_loader,
            epochs=args.epochs,
            lr=args.lr,
            weight_decay=args.weight_decay,
            seed=seed,
            gradient_clip=args.gradient_clip,
            fresh_batches_fn=fresh_batches_fn,
        )

    sample_inputs = next(iter(val_loader))[0][:8]
    prefix_len = prefix_length_for(seq_len)
    induction_heads = detect_induction_heads(
        model, sample_inputs, prefix_len=prefix_len, task=task
    )

    probe = _run_task_probe(
        model, task, vocab_size, seq_len, seed, tokens=sample_inputs
    )

    val_x, val_y = val_dataset.tensors
    if task == TASK_VARIABLE:
        patch = copy_query_batch(val_x, val_y, vocab_size=vocab_size)
        val_batch = patch["clean_inputs"]
        val_batch_answers = patch["clean_answers"]
        corrupted = patch["corrupted_inputs"]
        corrupted_answers = patch["corrupted_answers"]
        read_pos = int(patch["pos"])
    else:
        n_pair = min(32, val_x.size(0) // 2)
        val_batch, val_batch_answers = val_x[:n_pair], val_y[:n_pair, -1]
        corrupted, corrupted_answers = val_x[n_pair:2 * n_pair], val_y[n_pair:2 * n_pair, -1]
        read_pos = -1

    layers_to_patch = list(range(len(getattr(model, "blocks", []))))
    positions_to_patch = (
        [read_pos] if read_pos >= 0 else list(range(max(2, seq_len // 4), seq_len, 2))
    )
    patching_results = run_activation_patching(
        model=model,
        clean_inputs=val_batch,
        clean_answers=val_batch_answers,
        corrupted_answers=corrupted_answers,
        corrupted_inputs=corrupted,
        layers_to_patch=layers_to_patch,
        positions_to_patch=positions_to_patch,
        batch_size=min(32, val_batch.size(0)),
        pos=read_pos,
    )
    mean_activation_recovery = (
        float(np.mean([v["recovery"] for v in patching_results.values()]))
        if patching_results
        else 0.0
    )

    mean_ablation_effect = 0.0
    mean_path_patch_effect = 0.0
    if induction_heads:
        ablation_results = run_head_ablation(
            model=model,
            inputs=val_batch,
            answers=val_batch_answers,
            counterfactuals=corrupted_answers,
            induction_heads=induction_heads,
            pos=read_pos,
        )
        mean_ablation_effect = float(
            np.mean([v["effect"] for v in ablation_results.values()])
        )

        path_results = run_path_patching_to_logits(
            model=model,
            clean_inputs=val_batch,
            clean_answers=val_batch_answers,
            corrupted_inputs=corrupted,
            corrupted_answers=corrupted_answers,
            heads=induction_heads,
            pos=read_pos,
        )
        mean_path_patch_effect = float(
            np.mean([v["effect"] for v in path_results.values()])
        )

    return {
        "final_val_acc": float(history["val_acc"][-1]),
        "total_induction_heads": float(len(induction_heads)),
        "mean_activation_recovery": mean_activation_recovery,
        "mean_ablation_effect": mean_ablation_effect,
        "mean_path_patch_effect": mean_path_patch_effect,
        "probe_content_mass": float(probe["peak_content_mass"]),
        "probe_period_mass": float(probe["peak_period_mass"]),
        "probe_content_wins": float(bool(probe["content_wins"])),
        "checkpoint_epoch": float(checkpoint["epoch"]) if checkpoint else -1.0,
    }


def apply_config_presets(args: argparse.Namespace) -> None:
    """Resolve the named config presets (--quick / --standard / --scale).

    Extracted from main() so the preset matrix is directly testable —
    every preset is a pinned config that must match the exp1 preset of
    the same name, because the cascade's three rungs share one model.
    `--scale` resolves first: `--scale standard` is an alias for
    `--standard`, and a conflicting combination fails loudly.
    """
    if args.quick:
        args.vocab_size = 64
        args.seq_len = 12
        args.d_model = 32
        args.n_layers = 2
        args.n_heads = 2
        args.epochs = 500
        args.num_train = 1024
        logger.info("QUICK MODE: reduced config for fast iteration")

    if args.scale == "standard":
        args.standard = True
    elif args.scale == "large" and args.standard:
        raise SystemExit(
            "--standard and --scale large select different configs; "
            "pass only --scale large (or only --standard)."
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
        logger.info(
            "STANDARD MODE: canonical standard-scale config matching exp1 "
            "--standard (vocab=2048, seq=64, d_model=64, epochs=3000, "
            "batch=64, fresh batches)"
        )

    if args.scale == "large":
        # The same scaled GPU config exp1's --scale large selects; the
        # cascade measures one model at whichever scale Rung 1 ran.
        args.vocab_size = 2048
        args.seq_len = 128
        args.d_model = 256
        args.n_layers = 4
        args.n_heads = 8
        args.epochs = 1500
        args.num_train = 16384
        args.batch_size = 128
        args.fresh_batches = True
        logger.info(
            "SCALE=large: vocab=2048, seq=128, d_model=256, 4 layers, "
            "8 heads, epochs=1500, batch=128, fresh batches"
        )


def build_parser() -> argparse.ArgumentParser:
    """exp4's CLI, extracted from main() so tests can pin the flag contract
    (same pattern as exp1/exp2)."""
    parser = argparse.ArgumentParser(
        description="Rung 4: Circuit verification via activation patching"
    )
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument(
        "--vocab-size",
        type=int,
        default=256,
        help=(
            "Vocabulary size. Default raised from 32 (2026-08-02): at "
            "seq-len=24 (prefix_len=12), vocab_size=32 gave a ~87%% chance "
            "of a repeated token inside the prefix. See "
            "src.experiments.exp1_induction_heads.prefix_duplicate_probability."
        ),
    )
    parser.add_argument("--seq-len", type=int, default=24, help="Sequence length")
    parser.add_argument("--d-model", type=int, default=64, help="Model dimension")
    parser.add_argument("--n-layers", type=int, default=2, help="Number of layers")
    parser.add_argument("--n-heads", type=int, default=4, help="Heads per layer")
    parser.add_argument("--epochs", type=int, default=3000, help="Training epochs")
    parser.add_argument("--lr", type=float, default=1e-3, help="Learning rate")
    parser.add_argument(
        "--weight-decay",
        type=float,
        default=0.1,
        help="AdamW weight decay (matches exp1/exp2 so the cascade measures one recipe)",
    )
    parser.add_argument(
        "--gradient-clip",
        type=float,
        default=1.0,
        help="Global-norm gradient clipping, matching exp2/exp6. 0 disables.",
    )
    parser.add_argument("--num-train", type=int, default=8192, help="Training samples")
    parser.add_argument(
        "--batch-size",
        type=int,
        default=64,
        help=(
            "Training batch size. Was hardcoded at 64; now a flag so the "
            "fresh-batches regime can share exp1's batching semantics."
        ),
    )
    parser.add_argument("--quick", action="store_true", help="Quick test mode")
    parser.add_argument(
        "--standard",
        action="store_true",
        help=(
            "Canonical standard-scale config (Micro-Phase 10 pinning), "
            "identical to exp1's --standard so the cascade's three rungs "
            "measure one shared model: vocab_size=2048, seq_len=64, "
            "d_model=64, 2 layers, 4 heads, epochs=3000, num_train=8192, "
            "fresh batches on."
        ),
    )
    parser.add_argument(
        "--scale",
        type=str,
        choices=["standard", "large"],
        default=None,
        help=(
            "Named config preset. 'standard' is identical to --standard. "
            "'large' is the scaled GPU config (vocab_size=2048, seq_len=128, "
            "d_model=256, 4 layers, 8 heads, epochs=1500, num_train=16384, "
            "fresh batches) — the same preset exp1's --scale large selects, "
            "so a Rung 4 run can be matched to a Rung 1 run at either scale."
        ),
    )
    parser.add_argument(
        "--fresh-batches",
        action=_FreshBatchesAction,
        help=(
            "Resample a fresh set of training sequences every epoch instead "
            "of reusing one fixed set. Same flag and same semantics as "
            "exp1's; the presets imply it (see train_model's docstring for "
            "why the fixed regime is not a matched control)."
        ),
    )
    parser.add_argument(
        "--batches",
        choices=["fixed", "fresh"],
        default=None,
        action=_BatchesAction,
        help=(
            "Which training-batch regime to use, writing through to "
            "--fresh-batches (same convention as exp1)."
        ),
    )
    parser.add_argument(
        "--no-train", action="store_true", help="Skip training (untrained model)"
    )
    parser.add_argument(
        "--seeds",
        type=str,
        default=None,
        help=(
            "Comma-separated seeds (e.g. '0,1,2'). If set, runs the full "
            "train+detection+patching pipeline once per seed, saves a "
            "results/exp4_circuit_patching.json manifest, and skips plotting."
        ),
    )
    parser.add_argument(
        "--manifest-path",
        type=str,
        default=None,
        help=(
            "Explicit results/*.json path for the multi-seed manifest "
            "(default: results/exp4_circuit_patching.json). The --seeds "
            "branch reads this; without the flag the branch crashed on an "
            "undefined attribute — a remote cascade run must be able to "
            "route its manifest away from the flagship file."
        ),
    )
    parser.add_argument(
        "--from-checkpoint",
        type=str,
        default=None,
        help=(
            "Analyse exp1's checkpoint instead of training a second model: "
            "a file, or a directory holding the per-seed rolling "
            "checkpoints (exp1_checkpoint_seed<N>.pt). This is what makes "
            "the Rung 1 -> Rung 4 cascade measure ONE model; the "
            "alternative (train here) is a different model under the same "
            "claim."
        ),
    )
    parser.add_argument(
        "--source-vocab-size", type=int, default=2048,
        help="The checkpoint's vocab size (must match how it was trained)",
    )
    parser.add_argument(
        "--source-seq-len", type=int, default=64,
        help="The checkpoint's sequence length (must match how it was trained)",
    )
    parser.add_argument(
        "--source-d-model", type=int, default=64,
        help="The checkpoint's d_model (must match how it was trained)",
    )
    parser.add_argument(
        "--source-n-layers", type=int, default=2,
        help="The checkpoint's layer count (must match how it was trained)",
    )
    parser.add_argument(
        "--source-n-heads", type=int, default=4,
        help="The checkpoint's head count (must match how it was trained)",
    )
    parser.add_argument(
        "--source-task",
        choices=[TASK_PERIODIC, TASK_VARIABLE],
        default=TASK_PERIODIC,
        help=(
            "The task the checkpoint was trained on. 'periodic' is the "
            "historical prefix+prefix layout; 'variable' is the "
            "content-based task of ADR-0033, whose repeats sit at varying "
            "distances. The data this rung analyses and the position it "
            "measures the interventions at follow from it."
        ),
    )
    parser.add_argument(
        "--source-key-len", type=int, default=None,
        help="Variable task only: the checkpoint's key length.",
    )
    parser.add_argument(
        "--source-copy-blocks", type=int, default=None,
        help="Variable task only: the checkpoint's number of copy blocks.",
    )
    parser.add_argument(
        "--source-copy-block-len", type=int, default=None,
        help="Variable task only: the checkpoint's copy block length.",
    )
    parser.set_defaults(fresh_batches=False, batch_mode="fixed")
    return parser


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
            f"MULTI-SEED MODE: {len(seeds)} seeds {seeds} (skipping plots)"
        )
        result = run_seeds(lambda s: run_single_seed(s, args), seeds)
        # The parameter count must describe the model that was actually
        # analysed (an attention-only model when --from-checkpoint points at
        # Rung 1's checkpoint), not a throwaway probe of another family.
        probe_model, _ = _build_model(args, seeds[0], load_weights=False)
        manifest = ResultsManifest.from_run(
            experiment="exp4_circuit_patching",
            seeds=seeds,
            args={k: v for k, v in vars(args).items() if k != "seeds"},
            per_seed_metrics=result.per_seed,
            aggregate=result.aggregate,
            wall_clock_seconds=result.wall_clock_seconds,
            device=str(DEVICE),
            n_parameters=count_parameters(probe_model),
        )
        manifest_path = resolve_manifest_path(
            "exp4_circuit_patching",
            Path("results") / "exp4_circuit_patching.json",
            args.manifest_path,
            args.quick,
        )
        manifest.save(manifest_path)
        logger.info(f"Saved multi-seed manifest to {manifest_path}")
        for key in result.aggregate:
            logger.info(f"  {key}: {result.summary_line(key)}")
        return

    # Data
    model, checkpoint = _build_model(args, args.seed)
    model.to(DEVICE)
    task = getattr(args, "source_task", TASK_PERIODIC)
    if checkpoint is not None:
        vocab_size = args.source_vocab_size
        seq_len = args.source_seq_len
    else:
        vocab_size = args.vocab_size
        seq_len = args.seq_len

    spec = _task_spec(
        task,
        vocab_size,
        seq_len,
        key_len=getattr(args, "source_key_len", None),
        copy_blocks=getattr(args, "source_copy_blocks", None),
        copy_block_len=getattr(args, "source_copy_block_len", None),
    )
    train_dataset, val_dataset = task_datasets(spec, args.num_train, 1024, args.seed)
    train_loader = DataLoader(train_dataset, batch_size=args.batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=256, shuffle=False)
    logger.info(
        f"Data: train={args.num_train} sequences, seq_len={seq_len} | task={task}"
    )

    n_params = sum(p.numel() for p in model.parameters())
    logger.info(f"Model parameters: {n_params:,}")

    if not args.no_train and checkpoint is None:
        # Same fresh-batches regime as run_single_seed so the single-seed
        # and multi-seed paths cannot drift apart.
        fresh_batches_fn = _make_fresh_batches_fn(args, args.seed) if args.fresh_batches else None
        history = train_model(
            model=model,
            train_loader=train_loader,
            val_loader=val_loader,
            epochs=args.epochs,
            lr=args.lr,
            weight_decay=args.weight_decay,
            seed=args.seed,
            gradient_clip=args.gradient_clip,
            fresh_batches_fn=fresh_batches_fn,
        )
        logger.info(
            f"Training done | final val acc: {history['val_acc'][-1]:.4f}"
        )

    # Induction head detection
    sample_inputs = next(iter(val_loader))[0][:8]
    attention_probs, _ = compute_attention_patterns(model, sample_inputs)
    plot_attention_patterns(
        attention_probs,
        save_path=FIGURES_DIR / "exp4_attention_patterns.png",
    )

    induction_heads = detect_induction_heads(
        model, sample_inputs, prefix_len=prefix_length_for(seq_len), task=task
    )
    logger.info("=" * 60)
    logger.info("Induction Head Detection")
    logger.info("=" * 60)
    for layer in range(len(getattr(model, "blocks", []))):
        layer_heads = [(l, h) for l, h in induction_heads if l == layer]
        head_ids = [h for _, h in layer_heads]
        logger.info(f"  Layer {layer}: {len(layer_heads)} induction head(s): {head_ids}")
    total_found = len(induction_heads)
    blocks = getattr(model, "blocks", [])
    total_heads = len(blocks) * getattr(blocks[0], "n_heads", 0) if blocks else 0
    logger.info(f"  Total induction heads: {total_found} / {total_heads}")
    if not induction_heads:
        logger.warning("No induction heads detected.")

    probe = _run_task_probe(
        model, task, vocab_size, seq_len, args.seed, tokens=sample_inputs
    )
    logger.info(
        "Dissociation probe — content mass "
        f"{probe['peak_content_mass']:.3f} vs positional mass "
        f"{probe.get('peak_offset_mass', probe.get('peak_period_mass', 0.0)):.3f} -> "
        f"{'CONTENT-based' if probe['content_wins'] else 'POSITIONAL'} copy"
    )

    # Activation patching
    logger.info("=" * 60)
    logger.info("Activation Patching — Causal Circuit Analysis")
    logger.info("=" * 60)

    # Clean and corrupted are two *disjoint* draws from the same induction
    # task, each with well-defined next-token labels (see
    # make_repeated_token_data) — not a shuffled/permuted version of the
    # clean batch, which destroys the repeat structure and leaves no
    # well-defined "correct answer" for the corrupted run to provide as a
    # counterfactual.
    val_x, val_y = val_dataset.tensors
    if task == TASK_VARIABLE:
        patch = copy_query_batch(val_x, val_y, vocab_size=vocab_size)
        val_batch = patch["clean_inputs"]
        val_batch_answers = patch["clean_answers"]
        corrupted = patch["corrupted_inputs"]
        corrupted_answers = patch["corrupted_answers"]
        read_pos = int(patch["pos"])
    else:
        n_pair = min(32, val_x.size(0) // 2)
        val_batch, val_batch_answers = val_x[:n_pair], val_y[:n_pair, -1]
        corrupted, corrupted_answers = val_x[n_pair:2 * n_pair], val_y[n_pair:2 * n_pair, -1]
        read_pos = -1

    layers_to_patch = list(range(len(getattr(model, "blocks", []))))
    positions_to_patch = (
        [read_pos] if read_pos >= 0 else list(range(max(2, seq_len // 4), seq_len, 2))
    )

    patching_results = run_activation_patching(
        model=model,
        clean_inputs=val_batch,
        clean_answers=val_batch_answers,
        corrupted_answers=corrupted_answers,
        corrupted_inputs=corrupted,
        layers_to_patch=layers_to_patch,
        positions_to_patch=positions_to_patch,
        batch_size=min(32, val_batch.size(0)),
        pos=read_pos,
    )

    if patching_results:
        plot_patching_results(
            patching_results,
            n_layers=len(getattr(model, "blocks", [])),
            n_positions=len(positions_to_patch),
            save_path=FIGURES_DIR / "exp4_patching_results.png",
        )

        # Summarize circuit importance
        logger.info("\nCircuit component importance (top by recovery):")
        sorted_results = sorted(
            patching_results.items(), key=lambda x: x[1]["recovery"], reverse=True
        )
        for (layer, pos), vals in sorted_results[:6]:
            logger.info(
                f"  Layer {layer}, Pos {pos}: recovery={vals['recovery']:.3f} "
                f"(clean_diff={vals['clean_diff']:.3f}, patched_diff={vals['patched_diff']:.3f})"
            )

    # Head ablation
    if induction_heads:
        logger.info("=" * 60)
        logger.info("Head Ablation — Causal Validation")
        logger.info("=" * 60)
        ablation_results = run_head_ablation(
            model=model,
            inputs=val_batch,
            answers=val_batch_answers,
            counterfactuals=corrupted_answers,
            induction_heads=induction_heads,
            pos=read_pos,
        )
        plot_head_ablation(
            ablation_results,
            save_path=FIGURES_DIR / "exp4_head_ablation.png",
        )

        for (layer, head), vals in ablation_results.items():
            logger.info(
                f"  Layer {layer}, Head {head}: effect={vals['effect']:.3f} "
                f"(diff drop: {vals['clean_diff']:.3f} → {vals['ablated_diff']:.3f})"
            )

        # Path patching: isolate each induction head's *direct* effect on
        # the logits, distinct from activation patching's inclusion of
        # effects mediated through later layers.
        logger.info("=" * 60)
        logger.info("Path Patching — Direct Effect on Logits")
        logger.info("=" * 60)
        path_results = run_path_patching_to_logits(
            model=model,
            clean_inputs=val_batch,
            clean_answers=val_batch_answers,
            corrupted_inputs=corrupted,
            corrupted_answers=corrupted_answers,
            heads=induction_heads,
            pos=read_pos,
        )
        for (layer, head), vals in path_results.items():
            logger.info(
                f"  Layer {layer}, Head {head}: direct effect={vals['effect']:.3f} "
                f"(diff: {vals['clean_diff']:.3f} → {vals['patched_diff']:.3f})"
            )
    else:
        logger.info("Skipping head ablation and path patching: no induction heads detected.")

    # Summary
    logger.info("=" * 60)
    logger.info("Circuit Summary")
    logger.info("=" * 60)
    if induction_heads:
        for (layer, head) in induction_heads:
            logger.info(f"  Induction head: L{layer}H{head}")
    logger.info(f"  Total heads patched: {len(patching_results)}")
    if induction_heads:
        logger.info(f"  Heads ablated: {len(ablation_results)}")
        logger.info(f"  Heads path-patched: {len(path_results)}")
    logger.info("Done.")


if __name__ == "__main__":
    main()
