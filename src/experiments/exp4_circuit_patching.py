"""Rung 4 — Circuit verification via activation patching on induction heads.

Trains a decoder-only transformer on repeated-token prediction, identifies
induction heads, then runs activation patching to causally validate the
circuit. Reports faithfulness and ablates individual components.

Usage:
    python -m src.experiments.exp4_circuit_patching --seed 42 [--quick]

Output:
    - figures/exp4_attention_patterns.png
    - figures/exp4_patching_results.png
    - figures/exp4_head_ablation.png
    - Console: circuit components, logit-diff recovery, faithfulness scores
"""

import argparse
import logging
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader
from tqdm import tqdm

from src.experiments.exp1_induction_heads import make_repeated_token_data as make_induction_data
from src.experiments.runner import parse_seeds, run_seeds
from src.models.decoder_only_transformer import DecoderOnlyTransformer
from src.reproducibility import set_seed
from src.results import ResultsManifest, count_parameters

logger = logging.getLogger(__name__)

FIGURES_DIR = Path("figures")

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")





@torch.no_grad()
def compute_attention_patterns(
    model: DecoderOnlyTransformer, inputs: torch.Tensor
) -> dict:
    """Compute per-layer attention probabilities averaged over heads."""
    model.eval()
    logits, cache = model(inputs[:8], return_cache=True)
    probs = {}
    for layer in range(model.n_layers):
        prefix = f"blocks.{layer}.attn"
        attn_probs = cache[f"{prefix}.attn_probs"]
        probs[f"layer_{layer}"] = attn_probs.mean(dim=1)  # avg over heads
    return probs, cache


def detect_induction_heads(
    model: DecoderOnlyTransformer, inputs: torch.Tensor, threshold: float = 0.3
) -> list[tuple[int, int]]:
    """Detect induction heads by diagonal+1 attention pattern."""
    model.eval()
    induction_heads = []
    with torch.no_grad():
        logits, cache = model(inputs[:8], return_cache=True)

    for layer in range(model.n_layers):
        prefix = f"blocks.{layer}.attn"
        attn_probs = cache[f"{prefix}.attn_probs"]  # (B, n_heads, S, S_kv)
        if attn_probs is None:
            continue
        B, n_heads, S, _ = attn_probs.shape
        diag1 = attn_probs.diagonal(offset=1, dim1=-2, dim2=-1)
        diag1_mass = diag1.mean(dim=-1)  # (B, n_heads)
        avg_diag1 = diag1_mass.mean(dim=0)  # (n_heads,)
        for head in range(n_heads):
            if avg_diag1[head] > threshold and S > 1:
                induction_heads.append((layer, head))

    return induction_heads


def train_model(
    model: DecoderOnlyTransformer,
    train_loader: DataLoader,
    val_loader: DataLoader,
    epochs: int = 2000,
    lr: float = 1e-3,
    weight_decay: float = 0.1,
    seed: int = 42,
) -> dict:
    """Train the model and return history."""
    set_seed(seed)
    model.train()
    opt = torch.optim.AdamW(
        model.parameters(), lr=lr, weight_decay=weight_decay
    )
    history = {"train_loss": [], "val_loss": [], "val_acc": []}

    for epoch in tqdm(range(epochs), desc="Training"):
        model.train()
        total_loss = 0.0
        for x, y in train_loader:
            opt.zero_grad()
            logits, _ = model(x)
            loss = nn.functional.cross_entropy(
                logits.view(-1, logits.size(-1)), y.view(-1)
            )
            loss.backward()
            opt.step()
            total_loss += loss.item()

        model.eval()
        val_loss = 0.0
        correct = 0
        total = 0
        with torch.no_grad():
            for x, y in val_loader:
                logits, _ = model(x)
                loss = nn.functional.cross_entropy(
                    logits.view(-1, logits.size(-1)), y.view(-1)
                )
                val_loss += loss.item()
                preds = logits.argmax(dim=-1)
                correct += (preds == y).sum().item()
                total += y.numel()

        history["train_loss"].append(total_loss / len(train_loader))
        history["val_loss"].append(val_loss / len(val_loader))
        history["val_acc"].append(correct / total)

        if (epoch + 1) % 200 == 0:
            logger.info(
                f"Epoch {epoch+1:4d} | train loss: {history['train_loss'][-1]:.4f} "
                f"| val loss: {history['val_loss'][-1]:.4f} "
                f"| val acc: {history['val_acc'][-1]:.4f}"
            )

    return history


def run_activation_patching(
    model: DecoderOnlyTransformer,
    clean_inputs: torch.Tensor,
    clean_answers: torch.Tensor,
    corrupted_inputs: torch.Tensor,
    corrupted_answers: torch.Tensor,
    layers_to_patch: list[int],
    positions_to_patch: list[int],
    batch_size: int = 32,
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
    batch_size = min(batch_size, clean_inputs.size(0), corrupted_inputs.size(0))

    with torch.no_grad():
        clean_logits, clean_cache = model(clean_inputs[:batch_size], return_cache=True)
        _, corrupted_cache = model(corrupted_inputs[:batch_size], return_cache=True)

    answer = clean_answers[:batch_size].to(DEVICE)
    counterfactual = corrupted_answers[:batch_size].to(DEVICE)
    idx = torch.arange(batch_size, device=DEVICE)

    def logit_diff(logits: torch.Tensor) -> torch.Tensor:
        last_logits = logits[:, -1, :]
        return last_logits[idx, answer] - last_logits[idx, counterfactual]

    clean_diff = logit_diff(clean_logits).mean().item()
    logger.info(f"Clean logit diff (answer - counterfactual): {clean_diff:.4f}")

    for layer in tqdm(layers_to_patch, desc="Patching layers"):
        attn_module = model.blocks[layer].attn
        resid_pre = clean_cache[f"blocks.{layer}.resid_pre"].to(DEVICE)
        corrupted_resid_mid = corrupted_cache[f"blocks.{layer}.resid_mid"].to(DEVICE)

        for pos in positions_to_patch:
            target = corrupted_resid_mid[:, pos:pos + 1, :]
            pre = resid_pre[:, pos:pos + 1, :]

            def make_hook(
                p_pos: int, target_resid_mid: torch.Tensor, resid_pre_slice: torch.Tensor
            ):
                def hook(module, input, output):
                    attn_out, kv = output
                    attn_out = attn_out.clone()
                    attn_out[:, p_pos:p_pos + 1, :] = target_resid_mid - resid_pre_slice
                    return (attn_out, kv)
                return hook

            hook_handle = attn_module.register_forward_hook(
                make_hook(pos, target, pre)
            )

            with torch.no_grad():
                patched_logits, _ = model(clean_inputs[:batch_size])

            hook_handle.remove()

            patched_diff = logit_diff(patched_logits).mean().item()
            recovery = (patched_diff - clean_diff) / (-clean_diff) if clean_diff != 0 else 0.0
            results[(layer, pos)] = {
                "clean_diff": clean_diff,
                "patched_diff": patched_diff,
                "recovery": recovery,
            }

    return results


def run_path_patching_to_logits(
    model: DecoderOnlyTransformer,
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
    batch_size = min(batch_size, clean_inputs.size(0), corrupted_inputs.size(0))
    n_layers = model.n_layers

    with torch.no_grad():
        clean_logits, clean_cache = model(clean_inputs[:batch_size], return_cache=True)
        _, corrupted_cache = model(corrupted_inputs[:batch_size], return_cache=True)

    answer = clean_answers[:batch_size].to(DEVICE)
    counterfactual = corrupted_answers[:batch_size].to(DEVICE)
    idx = torch.arange(batch_size, device=DEVICE)

    def logit_diff(logits: torch.Tensor) -> torch.Tensor:
        # Read at `pos`, not always the last position: since ln_final/unembed
        # are per-position operations with no further cross-position mixing,
        # patching resid_final at `pos` only changes logits at that position.
        pos_logits = logits[:, pos, :]
        return pos_logits[idx, answer] - pos_logits[idx, counterfactual]

    clean_diff = logit_diff(clean_logits).mean().item()
    resid_final = clean_cache[f"blocks.{n_layers - 1}.resid_post"].to(DEVICE)

    for layer, head in tqdm(heads, desc="Path patching heads → logits"):
        attn_module = model.blocks[layer].attn
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
    model: DecoderOnlyTransformer,
    inputs: torch.Tensor,
    answers: torch.Tensor,
    counterfactuals: torch.Tensor,
    induction_heads: list[tuple[int, int]],
    batch_size: int = 32,
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
    batch_size = min(batch_size, inputs.size(0))

    with torch.no_grad():
        clean_logits, _ = model(inputs[:batch_size])

    answer = answers[:batch_size].to(DEVICE)
    counterfactual = counterfactuals[:batch_size].to(DEVICE)
    idx = torch.arange(batch_size, device=DEVICE)

    def logit_diff(logits: torch.Tensor) -> torch.Tensor:
        last_logits = logits[:, -1, :]
        return last_logits[idx, answer] - last_logits[idx, counterfactual]

    clean_diff = logit_diff(clean_logits).mean().item()

    for layer, head in tqdm(induction_heads, desc="Ablating heads"):
        attn_module = model.blocks[layer].attn
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
def run_single_seed(seed: int, args: argparse.Namespace) -> dict[str, float]:
    """Train one circuit-patching run end-to-end and return headline metrics
    for one seed. Mirrors main()'s single-seed data/model/train/analysis
    steps (detection, activation patching, head ablation, path patching),
    minus plotting — used by `--seeds` to aggregate across seeds via
    `src.experiments.runner.run_seeds`. Path patching only runs when at
    least one induction head is detected for that seed (it needs a real
    head to patch); its metric is 0.0 for seeds with none, same convention
    as head ablation.
    """
    train_dataset, val_dataset = make_induction_data(
        vocab_size=args.vocab_size,
        seq_len=args.seq_len,
        num_train=args.num_train,
        seed=seed,
    )
    train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=256, shuffle=False)

    model = DecoderOnlyTransformer(
        vocab_size=args.vocab_size,
        d_model=args.d_model,
        n_layers=args.n_layers,
        n_heads=args.n_heads,
        max_seq_len=args.seq_len,
    )
    model.to(DEVICE)

    history = train_model(
        model=model,
        train_loader=train_loader,
        val_loader=val_loader,
        epochs=args.epochs,
        lr=args.lr,
        seed=seed,
    )

    sample_inputs = next(iter(val_loader))[0][:8]
    induction_heads = detect_induction_heads(model, sample_inputs)

    val_x, val_y = val_dataset.tensors
    n_pair = min(32, val_x.size(0) // 2)
    val_batch, val_batch_answers = val_x[:n_pair], val_y[:n_pair, -1]
    corrupted, corrupted_answers = val_x[n_pair:2 * n_pair], val_y[n_pair:2 * n_pair, -1]

    layers_to_patch = list(range(args.n_layers))
    positions_to_patch = list(range(max(2, args.seq_len // 4), args.seq_len, 2))
    patching_results = run_activation_patching(
        model=model,
        clean_inputs=val_batch,
        clean_answers=val_batch_answers,
        corrupted_answers=corrupted_answers,
        corrupted_inputs=corrupted,
        layers_to_patch=layers_to_patch,
        positions_to_patch=positions_to_patch,
        batch_size=min(32, val_batch.size(0)),
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
    }


def main() -> None:
    FIGURES_DIR.mkdir(exist_ok=True)
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
    parser.add_argument("--num-train", type=int, default=8192, help="Training samples")
    parser.add_argument("--quick", action="store_true", help="Quick test mode")
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
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )

    if args.quick:
        args.vocab_size = 64
        args.seq_len = 12
        args.d_model = 32
        args.n_layers = 2
        args.n_heads = 2
        args.epochs = 500
        args.num_train = 1024
        logger.info("QUICK MODE: reduced config for fast iteration")

    logger.info(f"Device: {DEVICE}")
    logger.info(f"Arguments: {vars(args)}")

    set_seed(args.seed)

    if args.seeds:
        seeds = parse_seeds(args.seeds)
        logger.info(
            f"MULTI-SEED MODE: {len(seeds)} seeds {seeds} (skipping plots)"
        )
        result = run_seeds(lambda s: run_single_seed(s, args), seeds)
        probe_model = DecoderOnlyTransformer(
            vocab_size=args.vocab_size,
            d_model=args.d_model,
            n_layers=args.n_layers,
            n_heads=args.n_heads,
            max_seq_len=args.seq_len,
        )
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
        manifest_path = Path("results") / "exp4_circuit_patching.json"
        manifest.save(manifest_path)
        logger.info(f"Saved multi-seed manifest to {manifest_path}")
        for key in result.aggregate:
            logger.info(f"  {key}: {result.summary_line(key)}")
        return

    # Data
    train_dataset, val_dataset = make_induction_data(
        vocab_size=args.vocab_size,
        seq_len=args.seq_len,
        num_train=args.num_train,
        seed=args.seed,
    )
    train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=256, shuffle=False)
    logger.info(f"Data: train={args.num_train} sequences, seq_len={args.seq_len}")

    # Model
    model = DecoderOnlyTransformer(
        vocab_size=args.vocab_size,
        d_model=args.d_model,
        n_layers=args.n_layers,
        n_heads=args.n_heads,
        max_seq_len=args.seq_len,
    )
    model.to(DEVICE)
    n_params = sum(p.numel() for p in model.parameters())
    logger.info(f"Model parameters: {n_params:,}")

    if not args.no_train:
        history = train_model(
            model=model,
            train_loader=train_loader,
            val_loader=val_loader,
            epochs=args.epochs,
            lr=args.lr,
            seed=args.seed,
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

    induction_heads = detect_induction_heads(model, sample_inputs)
    logger.info("=" * 60)
    logger.info("Induction Head Detection")
    logger.info("=" * 60)
    for layer in range(args.n_layers):
        layer_heads = [(l, h) for l, h in induction_heads if l == layer]
        head_ids = [h for _, h in layer_heads]
        logger.info(f"  Layer {layer}: {len(layer_heads)} induction head(s): {head_ids}")
    total_found = len(induction_heads)
    total_heads = args.n_layers * args.n_heads
    logger.info(f"  Total induction heads: {total_found} / {total_heads}")
    if not induction_heads:
        logger.warning("No induction heads detected.")

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
    n_pair = min(32, val_x.size(0) // 2)
    val_batch, val_batch_answers = val_x[:n_pair], val_y[:n_pair, -1]
    corrupted, corrupted_answers = val_x[n_pair:2 * n_pair], val_y[n_pair:2 * n_pair, -1]

    layers_to_patch = list(range(args.n_layers))
    positions_to_patch = list(range(max(2, args.seq_len // 4), args.seq_len, 2))

    patching_results = run_activation_patching(
        model=model,
        clean_inputs=val_batch,
        clean_answers=val_batch_answers,
        corrupted_answers=corrupted_answers,
        corrupted_inputs=corrupted,
        layers_to_patch=layers_to_patch,
        positions_to_patch=positions_to_patch,
        batch_size=min(32, val_batch.size(0)),
    )

    if patching_results:
        plot_patching_results(
            patching_results,
            n_layers=args.n_layers,
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
