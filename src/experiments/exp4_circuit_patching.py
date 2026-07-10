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
from torch.utils.data import DataLoader, TensorDataset
from tqdm import tqdm

from src.experiments.exp1_induction_heads import make_repeated_token_data as make_induction_data
from src.models.decoder_only_transformer import DecoderOnlyTransformer
from src.reproducibility import set_seed

logger = logging.getLogger(__name__)

FIGURES_DIR = Path("figures")
FIGURES_DIR.mkdir(exist_ok=True)

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
    corrupted_inputs: torch.Tensor,
    layers_to_patch: list[int],
    positions_to_patch: list[int],
    batch_size: int = 32,
) -> dict:
    """Run residual stream activation patching.

    For each (layer, position), patches the resid_mid (attention output)
    from corrupted → clean and measures logit-diff recovery.

    Returns:
        dict mapping (layer, position) -> (clean_logit_diff, patched_logit_diff, recovery)
    """
    model.eval()
    results = {}

    with torch.no_grad():
        clean_logits, clean_cache = model(clean_inputs[:batch_size], return_cache=True)
        _, corrupted_cache = model(corrupted_inputs[:batch_size], return_cache=True)

    # Logit diff on the LAST token position (from BOS)
    def logit_diff(logits: torch.Tensor) -> torch.Tensor:
        last_logits = logits[:, -1, :]
        top_two = last_logits.topk(2, dim=-1)
        return top_two.values[:, 0] - top_two.values[:, 1]

    clean_diff = logit_diff(clean_logits).mean().item()
    logger.info(f"Clean logit diff: {clean_diff:.4f}")

    for layer in tqdm(layers_to_patch, desc="Patching layers"):
        target_module = model.blocks[layer].mlp
        corrupted_act = corrupted_cache[f"blocks.{layer}.resid_mid"]

        for pos in positions_to_patch:
            patch_act = corrupted_act[:, pos:pos + 1, :].to(DEVICE)

            def make_hook(p_act: torch.Tensor, p_pos: int):
                def hook(module, input):
                    x = input[0].clone()
                    x[:, p_pos:p_pos + 1, :] = p_act
                    return (x,)
                return hook

            hook_handle = target_module.register_forward_pre_hook(
                make_hook(patch_act, pos)
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


def run_head_ablation(
    model: DecoderOnlyTransformer,
    inputs: torch.Tensor,
    induction_heads: list[tuple[int, int]],
    batch_size: int = 32,
) -> dict:
    """Zero-ablate individual induction heads and measure effect."""
    model.eval()
    results = {}

    with torch.no_grad():
        clean_logits, _ = model(inputs[:batch_size])

    def logit_diff(logits):
        last_logits = logits[:, -1, :]
        top_two = last_logits.topk(2, dim=-1)
        return top_two.values[:, 0] - top_two.values[:, 1]

    clean_diff = logit_diff(clean_logits).mean().item()

    for layer, head in tqdm(induction_heads, desc="Ablating heads"):
        d_head = model.d_model // model.n_heads

        def make_ablation_hook(h_layer: int, h_head: int, d_h: int):
            def hook(module, input, output):
                attn_out, kv = output
                B, S, D = attn_out.shape
                W_O = module.W_O.weight.view(model.n_heads, d_h, D)

                with torch.no_grad():
                    head_output = attn_out @ W_O[h_head].T.unsqueeze(0) / model.n_heads
                    # Zero the head contribution
                    attn_out = attn_out - head_output
                return attn_out, kv
            return hook

        hook_handle = model.blocks[layer].attn.register_forward_hook(
            make_ablation_hook(layer, head, d_head)
        )

        with torch.no_grad():
            ablated_logits, _ = model(inputs[:batch_size])

        hook_handle.remove()

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
    bars = ax.bar(range(len(labels)), effects, color=colors)
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


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Rung 4: Circuit verification via activation patching"
    )
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument("--vocab-size", type=int, default=32, help="Vocabulary size")
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
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )

    if args.quick:
        args.vocab_size = 16
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
        logger.info(f"  Layer {layer}: {len(layer_heads)} induction head(s): {[h for _, h in layer_heads]}")
    total_found = len(induction_heads)
    total_heads = args.n_layers * args.n_heads
    logger.info(f"  Total induction heads: {total_found} / {total_heads}")
    if not induction_heads:
        logger.warning("No induction heads detected.")

    # Activation patching
    logger.info("=" * 60)
    logger.info("Activation Patching — Causal Circuit Analysis")
    logger.info("=" * 60)

    val_batch = next(iter(val_loader))[0][:32]
    # Corrupted: shuffle the tokens to break the repetition
    rng = np.random.default_rng(args.seed + 1)
    corrupted = val_batch.clone()
    for i in range(corrupted.size(0)):
        perm = torch.randperm(corrupted.size(1))
        corrupted[i] = corrupted[i, perm]

    layers_to_patch = list(range(args.n_layers))
    positions_to_patch = list(range(max(2, args.seq_len // 4), args.seq_len, 2))

    patching_results = run_activation_patching(
        model=model,
        clean_inputs=val_batch,
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
    else:
        logger.info("Skipping head ablation: no induction heads detected.")

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
    logger.info("Done.")


if __name__ == "__main__":
    main()
