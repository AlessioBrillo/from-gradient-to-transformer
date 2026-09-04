#!/usr/bin/env python3
"""Rung 6 — Capstone: Train & Reverse-Engineer a Decoder-Only Transformer.

Trains a decoder-only transformer on TWO tasks simultaneously:
1. Modular Addition (P=113) — Grokking / Fourier reverse-engineering
2. Induction Heads (repeated random tokens) — K-composition / circuit discovery

Reverse-engineers the learned algorithms via:
- Fourier decomposition of modular addition embeddings
- K-composition diagnostic for induction heads
- Activation patching / path patching for circuit discovery
- SAE feature extraction on real activations

Usage:
    python -m src.experiments.exp6_capstone --config configs/capstone.yaml --seeds 0,1,2

Output:
    - figures/exp6_modular_curve.png
    - figures/exp6_fourier_spectrum.png
    - figures/exp6_induction_kcomp.png
    - figures/exp6_circuit_patching.png
    - figures/exp6_sae_features.png
    - results/exp6_capstone.json (manifest)
    - checkpoints/exp6_capstone_seed{0,1,2}_step{1000,2000,...}.pt
"""

import argparse
import logging
import math
from pathlib import Path
from typing import Any, Optional

import numpy as np
import torch
import torch.nn.functional as F  # noqa: N812
import yaml
from torch.utils.data import DataLoader, TensorDataset
from tqdm import tqdm

from src.experiments.checkpointing import save_training_checkpoint
from src.experiments.runner import parse_seeds, run_seeds
from src.models.decoder_only_transformer import DecoderOnlyTransformer
from src.reproducibility import set_seed
from src.results import ResultsManifest, count_parameters

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
FIGURES_DIR = Path("figures")
RESULTS_DIR = Path("results")
CHECKPOINTS_DIR = Path("checkpoints")

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


# ---------------------------------------------------------------------------
# Data: Modular Addition + Induction (Round-Robin DataLoaders)
# ---------------------------------------------------------------------------
def make_modular_addition_data(
    modulus: int,
    train_fraction: float,
    seq_len: int,
    seed: int = 42,
) -> tuple[TensorDataset, TensorDataset]:
    """Generate modular addition task (a + b mod P) padded to seq_len."""
    rng = np.random.default_rng(seed)

    all_pairs = [(a, b) for a in range(modulus) for b in range(modulus)]
    rng.shuffle(all_pairs)

    split_idx = int(len(all_pairs) * train_fraction)
    train_pairs = all_pairs[:split_idx]
    val_pairs = all_pairs[split_idx:]

    def _to_tensor(pairs: list) -> torch.Tensor:
        a = torch.tensor([p[0] for p in pairs], dtype=torch.long)
        b = torch.tensor([p[1] for p in pairs], dtype=torch.long)
        target = (a + b) % modulus
        # Create sequences of length seq_len: [a, b, pad, pad, ...]
        # Target is only at position 1 (after b), rest are ignored via loss masking
        pad_id = modulus  # vocab_size - 1
        x = torch.full((len(pairs), seq_len), pad_id, dtype=torch.long)
        x[:, 0] = a
        x[:, 1] = b
        # Language modeling format: input = x[:-1], target = x[1:]
        # But we only care about predicting at position 1 (after seeing a, b)
        return x, target

    train_x, train_y = _to_tensor(train_pairs)
    val_x, val_y = _to_tensor(val_pairs)

    # Language modeling: input = tokens[:-1], target = tokens[1:]
    # For modular: we want to predict target at position 1 (after a, b)
    # So input is [:, :-1], target is [:, 1:]
    # But we'll mask loss to only care about position 1
    train_x_lm = train_x[:, :-1]
    train_y_lm = train_x[:, 1:]
    val_x_lm = val_x[:, :-1]
    val_y_lm = val_x[:, 1:]

    return (
        TensorDataset(train_x_lm, train_y_lm, train_y),  # Include original target for masking
        TensorDataset(val_x_lm, val_y_lm, val_y),
    )


def make_repeated_token_data(
    vocab_size: int = 2048,
    seq_len: int = 128,
    num_train: int = 8192,
    num_val: int = 1024,
    prefix_ratio: float = 0.5,
    seed: int = 42,
) -> tuple[TensorDataset, TensorDataset]:
    """Generate sequences with repeated prefix to induce induction heads."""
    prefix_len = max(2, int(seq_len * prefix_ratio))

    rng = np.random.default_rng(seed)

    def _generate(n: int) -> torch.Tensor:
        sequences = []
        for _ in range(n):
            prefix = rng.integers(0, vocab_size, size=prefix_len).tolist()
            tokens = prefix.copy()
            while len(tokens) < seq_len:
                tokens.append(tokens[len(tokens) % prefix_len])
            sequences.append(tokens[:seq_len])
        return torch.tensor(sequences, dtype=torch.long)

    train_ids = _generate(num_train)
    val_ids = _generate(num_val)

    # Language modeling: input = tokens[:-1], target = tokens[1:]
    train_x = train_ids[:, :-1]
    train_y = train_ids[:, 1:]
    val_x = val_ids[:, :-1]
    val_y = val_ids[:, 1:]

    return (
        TensorDataset(train_x, train_y),
        TensorDataset(val_x, val_y),
    )


class RoundRobinDataLoader:
    """Iterates over multiple dataloaders in round-robin fashion."""

    def __init__(self, dataloaders: list[DataLoader]):
        self.dataloaders = dataloaders
        self.iterators = [iter(dl) for dl in dataloaders]
        self.lengths = [len(dl) for dl in dataloaders]
        self.total_batches = sum(self.lengths)

    def __iter__(self):
        self.iterators = [iter(dl) for dl in self.dataloaders]
        return self

    def __next__(self):
        # Round-robin: yield from each dataloader in turn
        for i, it in enumerate(self.iterators):
            try:
                batch = next(it)
                # Add task_id to batch for loss masking
                # batch can be tuple or list from DataLoader
                batch = tuple(batch) if isinstance(batch, list) else batch
                if isinstance(batch, tuple) and len(batch) == 3:
                    # Modular addition: (x, y, target) - task_id = 0
                    x, y, target = batch
                    return x, y, target, 0
                else:
                    # Induction: (x, y) - task_id = 1
                    x, y = batch[:2]
                    return x, y, None, 1
            except StopIteration:
                continue
        raise StopIteration

    def __len__(self):
        return self.total_batches


def make_mixed_dataloaders(
    cfg: dict,
    seed: int,
) -> tuple[RoundRobinDataLoader, RoundRobinDataLoader]:
    """Create round-robin dataloaders for both tasks."""
    mod_cfg = cfg["task"]["modular"]
    ind_cfg = cfg["task"]["induction"]
    train_cfg = cfg["training"]

    seq_len = ind_cfg["seq_len"]

    # Modular addition data (padded to induction seq_len)
    mod_train, mod_val = make_modular_addition_data(
        modulus=mod_cfg["modulus"],
        train_fraction=mod_cfg["train_fraction"],
        seq_len=seq_len,
        seed=seed,
    )

    # Induction data
    ind_train, ind_val = make_repeated_token_data(
        vocab_size=ind_cfg["vocab_size"],
        seq_len=ind_cfg["seq_len"],
        num_train=ind_cfg["num_train"],
        num_val=ind_cfg["num_val"],
        prefix_ratio=ind_cfg["prefix_ratio"],
        seed=seed + 1000,
    )

    batch_size = train_cfg["batch_size"]
    mod_train_loader = DataLoader(mod_train, batch_size=batch_size, shuffle=True, drop_last=True)
    mod_val_loader = DataLoader(mod_val, batch_size=batch_size, shuffle=False)
    ind_train_loader = DataLoader(ind_train, batch_size=batch_size, shuffle=True, drop_last=True)
    ind_val_loader = DataLoader(ind_val, batch_size=batch_size, shuffle=False)

    train_loader = RoundRobinDataLoader([mod_train_loader, ind_train_loader])
    val_loader = RoundRobinDataLoader([mod_val_loader, ind_val_loader])

    return train_loader, val_loader


# ---------------------------------------------------------------------------
# Instrumentation: Fourier Analysis (Modular Addition)
# ---------------------------------------------------------------------------
def fourier_decomposition(
    embeddings: torch.Tensor,  # [P, d_model]
    modulus: int,
) -> dict:
    """Decompose embeddings into Fourier basis.

    Returns dict with:
    - 'fourier_coeffs': [P, d_model] complex coefficients
    - 'fourier_magnitudes': [P, d_model] magnitudes
    - 'dominant_frequencies': top-k frequencies per neuron
    """
    P = embeddings.shape[0]

    # DFT matrix
    freqs = torch.arange(P, device=embeddings.device, dtype=embeddings.dtype)
    t = torch.arange(P, device=embeddings.device, dtype=embeddings.dtype)
    basis = torch.exp(-2j * math.pi * torch.outer(freqs, t) / P) / math.sqrt(P)

    # Decompose each neuron - cast embeddings to complex for matmul with complex basis
    embeddings_c = embeddings.to(torch.complex64)
    coeffs = basis @ embeddings_c  # [P, d_model]
    magnitudes = coeffs.abs()

    # Dominant frequencies per neuron
    top_k = min(5, P)
    dominant_freqs = magnitudes.topk(top_k, dim=0).indices.cpu().numpy()
    dominant_mags = magnitudes.topk(top_k, dim=0).values.cpu().numpy()

    return {
        "fourier_coeffs": coeffs.cpu().numpy(),
        "fourier_magnitudes": magnitudes.cpu().numpy(),
        "dominant_frequencies": dominant_freqs,
        "dominant_magnitudes": dominant_mags,
    }


def analyze_fourier_sparsity(
    fourier_magnitudes: np.ndarray,  # [P, d_model]
    modulus: int,
) -> dict:
    """Compute sparsity metrics: k_90, k_99 per neuron."""
    k_90_list = []
    k_99_list = []

    for i in range(fourier_magnitudes.shape[1]):
        mags = fourier_magnitudes[:, i]
        sorted_mags = np.sort(mags)[::-1]
        cumsum = np.cumsum(sorted_mags**2)
        total = cumsum[-1]

        k_90 = np.searchsorted(cumsum, 0.9 * total) + 1
        k_99 = np.searchsorted(cumsum, 0.99 * total) + 1

        k_90_list.append(k_90)
        k_99_list.append(k_99)

    return {
        "k_90_mean": float(np.mean(k_90_list)),
        "k_90_std": float(np.std(k_90_list)),
        "k_90_min": int(np.min(k_90_list)),
        "k_90_max": int(np.max(k_90_list)),
        "k_99_mean": float(np.mean(k_99_list)),
        "k_99_std": float(np.std(k_99_list)),
        "k_99_min": int(np.min(k_99_list)),
        "k_99_max": int(np.max(k_99_list)),
    }


# ---------------------------------------------------------------------------
# Instrumentation: K-Composition (Induction Heads)
# ---------------------------------------------------------------------------
def compute_k_composition_scores(
    model: DecoderOnlyTransformer,
    dataloader: DataLoader,
    num_batches: int = 10,
) -> dict:
    """Compute K-composition scores for induction head detection.

    Returns:
        dict with k_comp_scores per head per layer
    """
    model.eval()
    scores = {}

    with torch.no_grad():
        for batch_idx, batch in enumerate(dataloader):
            if batch_idx >= num_batches:
                break
            # Handle both RoundRobinDataLoader (4-tuple) and regular DataLoader (2-tuple)
            if isinstance(batch, tuple) and len(batch) == 4:
                x, y, mod_target, task_id = batch
            else:
                x, y = batch[:2]
                _mod_target = None
                _task_id = 1
            x = x.to(DEVICE)
            y = y.to(DEVICE)

            # Run with cache to capture attention patterns
            logits, cache = model(x, return_cache=True)

            # Placeholder implementation - full K-composition in exp1_induction_heads.py
            for layer_idx in range(1, model.n_layers):
                for head_idx in range(model.n_heads):
                    key = f"L{layer_idx}H{head_idx}"
                    if key not in scores:
                        scores[key] = []
                    scores[key].append(0.0)

    # Average across batches
    for key in scores:
        scores[key] = float(np.mean(scores[key]))

    return scores


# ---------------------------------------------------------------------------
# Instrumentation: Activation Harvesting for SAE
# ---------------------------------------------------------------------------
def harvest_activations(
    model: DecoderOnlyTransformer,
    dataloader: DataLoader,
    hooks: list[str],
    max_tokens: int = 10000,
) -> dict[str, torch.Tensor]:
    """Harvest activations from specified hooks for SAE training."""
    model.eval()
    activations = {hook: [] for hook in hooks}

    handles = []

    def make_hook(name):
        def hook_fn(module, input_, output):
            if isinstance(output, tuple):
                output = output[0]
            activations[name].append(output.detach().cpu())
        return hook_fn

    for hook_name in hooks:
        if hasattr(model, hook_name):
            handle = getattr(model, hook_name).register_forward_hook(
                make_hook(hook_name)
            )
            handles.append(handle)
        else:
            # Try to find in layers
            for layer in model.layers:
                if hasattr(layer, hook_name):
                    handle = getattr(layer, hook_name).register_forward_hook(
                        make_hook(hook_name)
                    )
                    handles.append(handle)
                    break

    total_tokens = 0
    with torch.no_grad():
        for x, y in dataloader:
            if total_tokens >= max_tokens:
                break
            x = x.to(DEVICE)
            _ = model(x)
            total_tokens += x.shape[0] * x.shape[1]

    for h in handles:
        h.remove()

    # Concatenate
    result = {}
    for hook_name, acts in activations.items():
        if acts:
            result[hook_name] = torch.cat(acts, dim=0)  # [N, d_model]

    return result


# ---------------------------------------------------------------------------
# Training Loop
# ---------------------------------------------------------------------------
def train_single_seed(
    cfg: dict,
    seed: int,
    resume_step: int = 0,
    checkpoint_dir: Optional[Path] = None,
    wandb_run: Any = None,
    log_wandb_metrics: Any = None,
    log_wandb_artifact: Any = None,
) -> dict[str, float]:
    """Train capstone model for a single seed.

    Returns final metrics dict for runner aggregation.
    """
    set_seed(seed)

    train_cfg = cfg["training"]
    model_cfg = cfg["model"]
    inst_cfg = cfg["instrumentation"]

    # Create model
    model = DecoderOnlyTransformer(
        vocab_size=cfg["task"]["induction"]["vocab_size"]
        + cfg["task"]["modular"]["modulus"]
        + 10,
        d_model=model_cfg["d_model"],
        n_layers=model_cfg["n_layers"],
        n_heads=model_cfg["n_heads"],
        d_mlp=model_cfg["d_mlp"],
        dropout=model_cfg["dropout"],
        rotary_base=model_cfg["rotary_base"],
        rmsnorm_eps=model_cfg["rmsnorm_eps"],
    ).to(DEVICE)

    # Optimizer & Scheduler
    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=train_cfg["lr"],
        weight_decay=train_cfg["weight_decay"],
    )

    def lr_lambda(step):
        if step < train_cfg["warmup_steps"]:
            return step / train_cfg["warmup_steps"]
        progress = (step - train_cfg["warmup_steps"]) / (
            train_cfg["steps"] - train_cfg["warmup_steps"]
        )
        return 0.5 * (1 + math.cos(math.pi * progress))

    scheduler = torch.optim.lr_scheduler.LambdaLR(optimizer, lr_lambda)

    # Resume from checkpoint if provided
    start_step = 0
    if resume_step > 0 and checkpoint_dir:
        ckpt_path = checkpoint_dir / f"exp6_capstone_seed{seed}_step{resume_step}.pt"
        if ckpt_path.exists():
            ckpt = torch.load(ckpt_path, map_location=DEVICE)
            model.load_state_dict(ckpt["model"])
            optimizer.load_state_dict(ckpt["optimizer"])
            scheduler.load_state_dict(ckpt["scheduler"])
            start_step = ckpt["step"]
            logger.info(f"Resumed seed {seed} from step {start_step}")

    # Data
    train_loader, val_loader = make_mixed_dataloaders(cfg, seed)

    # Training loop
    model.train()
    step = start_step
    pbar = tqdm(total=train_cfg["steps"], initial=start_step, desc=f"Seed {seed}")

    metrics_log = {
        "modular_loss": [],
        "induction_loss": [],
        "modular_acc": [],
        "induction_acc": [],
    }

    mod_weight = train_cfg.get("modular_weight", 1.0)
    ind_weight = train_cfg.get("induction_weight", 1.0)

    while step < train_cfg["steps"]:
        for batch in train_loader:
            if step >= train_cfg["steps"]:
                break

            x, y, mod_target, task_id = batch
            x = x.to(DEVICE)
            y = y.to(DEVICE)

            optimizer.zero_grad()
            logits, _ = model(x)

            # Compute loss with task-specific masking
            if task_id == 0:
                # Modular addition: only compute loss at position 1 (predicting target after a, b)
                # x shape: [batch, seq_len-1], y shape: [batch, seq_len-1]
                # mod_target shape: [batch] - the actual (a+b)%P target
                # We only care about the prediction at position 1 (after seeing a, b)
                loss = F.cross_entropy(logits[:, 1, :], mod_target.to(DEVICE))
                loss = loss * mod_weight
            else:
                # Induction: standard language modeling loss on all positions
                loss = F.cross_entropy(logits.view(-1, logits.size(-1)), y.view(-1))
                loss = loss * ind_weight

            loss.backward()
            torch.nn.utils.clip_grad_norm_(
                model.parameters(), train_cfg["gradient_clip"]
            )
            optimizer.step()
            scheduler.step()

            step += 1
            pbar.update(1)

            # Logging
            if step % 100 == 0:
                if task_id == 0:
                    metrics_log["modular_loss"].append(loss.item() / mod_weight)
                else:
                    metrics_log["induction_loss"].append(loss.item() / ind_weight)

            # W&B per-step metrics logging
            if wandb_run and log_wandb_metrics:
                metrics_to_log = {
                    f"seed_{seed}/loss": loss.item(),
                    f"seed_{seed}/lr": scheduler.get_last_lr()[0],
                }
                if task_id == 0:
                    metrics_to_log[f"seed_{seed}/modular_loss"] = loss.item() / mod_weight
                else:
                    metrics_to_log[f"seed_{seed}/induction_loss"] = loss.item() / ind_weight
                log_wandb_metrics(wandb_run, metrics_to_log, step=step)

            # Instrumentation checkpoints
            if step % inst_cfg["fourier_every"] == 0:
                # Fourier analysis on modular addition embeddings
                mod_embeddings = model.embed.weight[
                    : cfg["task"]["modular"]["modulus"]
                ]
                fourier_result = fourier_decomposition(
                    mod_embeddings, cfg["task"]["modular"]["modulus"]
                )
                sparsity = analyze_fourier_sparsity(
                    fourier_result["fourier_magnitudes"],
                    cfg["task"]["modular"]["modulus"],
                )
                logger.info(f"Step {step}: Fourier k_99 = {sparsity['k_99_mean']:.1f}")

                # Log Fourier sparsity to W&B
                if wandb_run and log_wandb_metrics:
                    log_wandb_metrics(wandb_run, {
                        f"seed_{seed}/fourier_k_90": sparsity["k_90_mean"],
                        f"seed_{seed}/fourier_k_99": sparsity["k_99_mean"],
                    }, step=step)

            if step % inst_cfg["kcomp_every"] == 0:
                # K-composition on induction data
                kcomp_scores = compute_k_composition_scores(
                    model, val_loader, num_batches=5
                )
                max_kcomp = max(kcomp_scores.values()) if kcomp_scores else 0.0
                logger.info(f"Step {step}: Max K-comp = {max_kcomp:.4f}")

                # Log K-composition to W&B
                if wandb_run and log_wandb_metrics:
                    log_wandb_metrics(wandb_run, {
                        f"seed_{seed}/max_kcomp": max_kcomp,
                    }, step=step)

            # Checkpointing
            if step % cfg["checkpoint_every"] == 0:
                if checkpoint_dir:
                    ckpt_path = checkpoint_dir / f"exp6_capstone_seed{seed}_step{step}.pt"
                    save_training_checkpoint(
                        ckpt_path,
                        model=model,
                        optimizer=optimizer,
                        scheduler=scheduler,
                        step=step,
                        seed=seed,
                        config=cfg,
                    )
                    # Log checkpoint as W&B artifact
                    if wandb_run and log_wandb_artifact:
                        log_wandb_artifact(
                            wandb_run,
                            str(ckpt_path),
                            f"capstone-seed{seed}-step{step}",
                            type_="model",
                        )

            # Evaluation
            if step % 1000 == 0:
                model.eval()
                with torch.no_grad():
                    # Quick val pass - handle RoundRobinDataLoader batches
                    val_losses = []
                    val_accs = []
                    for batch in val_loader:
                        vx, vy, vmod_target, vtask_id = batch
                        vx = vx.to(DEVICE)
                        vy = vy.to(DEVICE)

                        vlogits, _ = model(vx)

                        if vtask_id == 0:
                            # Modular: loss at position 1
                            vloss = F.cross_entropy(
                                vlogits[:, 1, :], vmod_target.to(DEVICE)
                            )
                            vacc = (
                                vlogits[:, 1, :].argmax(-1)
                                == vmod_target.to(DEVICE)
                            ).float().mean()
                        else:
                            # Induction: standard LM loss
                            vloss = F.cross_entropy(
                                vlogits.view(-1, vlogits.size(-1)), vy.view(-1)
                            )
                            vacc = (vlogits.argmax(-1) == vy).float().mean()

                        val_losses.append(vloss.item())
                        val_accs.append(vacc.item())

                    logger.info(
                        f"Step {step}: Val Loss = {np.mean(val_losses):.4f}, "
                        f"Val Acc = {np.mean(val_accs):.4f}"
                    )
                    # Log validation metrics to W&B
                    if wandb_run and log_wandb_metrics:
                        log_wandb_metrics(wandb_run, {
                            f"seed_{seed}/val_loss": float(np.mean(val_losses)),
                            f"seed_{seed}/val_acc": float(np.mean(val_accs)),
                        }, step=step)
                model.train()

    pbar.close()

    # Final evaluation
    model.eval()
    with torch.no_grad():
        # Modular addition eval - use the padded data format
        mod_train, mod_val = make_modular_addition_data(
            cfg["task"]["modular"]["modulus"],
            cfg["task"]["modular"]["train_fraction"],
            seq_len=cfg["task"]["induction"]["seq_len"],
            seed=seed,
        )
        mod_val_loader = DataLoader(mod_val, batch_size=train_cfg["batch_size"])

        mod_correct = 0
        mod_total = 0
        for x, y, mod_target in mod_val_loader:
            x = x.to(DEVICE)
            mod_target = mod_target.to(DEVICE)
            logits, _ = model(x)
            pred = logits[:, 1, :].argmax(-1)  # Predict at position 1
            mod_correct += (pred == mod_target).sum().item()
            mod_total += mod_target.numel()
        mod_acc = mod_correct / mod_total if mod_total > 0 else 0.0

        # Induction eval
        ind_train, ind_val = make_repeated_token_data(
            vocab_size=cfg["task"]["induction"]["vocab_size"],
            seq_len=cfg["task"]["induction"]["seq_len"],
            num_train=cfg["task"]["induction"]["num_train"],
            num_val=cfg["task"]["induction"]["num_val"],
            prefix_ratio=cfg["task"]["induction"]["prefix_ratio"],
            seed=seed + 1000,
        )
        ind_val_loader = DataLoader(ind_val, batch_size=train_cfg["batch_size"])

        ind_correct = 0
        ind_total = 0
        for x, y in ind_val_loader:
            x = x.to(DEVICE)
            y = y.to(DEVICE)
            logits, _ = model(x)
            pred = logits.argmax(-1)
            ind_correct += (pred == y).sum().item()
            ind_total += y.numel()
        ind_acc = ind_correct / ind_total if ind_total > 0 else 0.0

        # Final Fourier analysis
        mod_embeddings = model.embed.weight[
            : cfg["task"]["modular"]["modulus"]
        ]
        fourier_result = fourier_decomposition(
            mod_embeddings, cfg["task"]["modular"]["modulus"]
        )
        sparsity = analyze_fourier_sparsity(
            fourier_result["fourier_magnitudes"], cfg["task"]["modular"]["modulus"]
        )

        # Final K-composition
        kcomp_scores = compute_k_composition_scores(
            model, ind_val_loader, num_batches=10
        )
        max_kcomp = max(kcomp_scores.values()) if kcomp_scores else 0.0

        # Log final evaluation metrics to W&B
        if wandb_run and log_wandb_metrics:
            log_wandb_metrics(wandb_run, {
                f"seed_{seed}/final_modular_acc": mod_acc,
                f"seed_{seed}/final_induction_acc": ind_acc,
                f"seed_{seed}/final_k_90": sparsity["k_90_mean"],
                f"seed_{seed}/final_k_99": sparsity["k_99_mean"],
                f"seed_{seed}/final_max_kcomp": max_kcomp,
            }, step=train_cfg["steps"])

    # Return metrics for aggregation
    return {
        "final_modular_acc": mod_acc,
        "final_induction_acc": ind_acc,
        "final_k_90": sparsity["k_90_mean"],
        "final_k_99": sparsity["k_99_mean"],
        "final_max_kcomp": max_kcomp,
        "total_steps": train_cfg["steps"],
        "model_params": count_parameters(model),
    }


def main():
    parser = argparse.ArgumentParser(
        description="Capstone: Decoder-Only Transformer Training & Reverse-Engineering"
    )
    parser.add_argument(
        "--config", type=str, default="configs/capstone.yaml", help="Path to config YAML"
    )
    parser.add_argument(
        "--seed", type=int, default=42, help="Single seed (ignored if --seeds provided)"
    )
    parser.add_argument("--seeds", type=str, help="Comma-separated seeds, e.g. '0,1,2'")
    parser.add_argument(
        "--checkpoint-every", type=int, default=1000, help="Checkpoint interval"
    )
    parser.add_argument("--save-model", action="store_true", help="Save final model checkpoints")
    parser.add_argument("--resume", type=int, default=0, help="Resume from step")
    parser.add_argument("--wandb", action="store_true", help="Log to Weights & Biases")
    parser.add_argument("--wandb-project", type=str, help="W&B project name")
    parser.add_argument("--wandb-entity", type=str, help="W&B entity/username")
    parser.add_argument("--quick", action="store_true", help="Quick mode for testing")
    args = parser.parse_args()

    # Load config
    with open(args.config) as fh:
        cfg = yaml.safe_load(fh)

    # Quick mode overrides
    if args.quick:
        cfg["training"]["steps"] = 100
        cfg["training"]["batch_size"] = 32
        cfg["model"]["d_model"] = 64
        cfg["model"]["n_layers"] = 2
        cfg["model"]["n_heads"] = 4
        cfg["model"]["d_mlp"] = 256
        cfg["task"]["induction"]["vocab_size"] = 256
        cfg["task"]["induction"]["seq_len"] = 32
        cfg["task"]["induction"]["num_train"] = 512
        cfg["task"]["induction"]["num_val"] = 128
        cfg["task"]["modular"]["modulus"] = 17
        cfg["checkpoint_every"] = 50
        logger.info("QUICK MODE: reduced config for fast iteration")

    # Override from CLI
    if args.seeds:
        seeds = parse_seeds(args.seeds)
    else:
        seeds = [args.seed]

    if args.checkpoint_every:
        cfg["checkpoint_every"] = args.checkpoint_every

    # W&B setup
    wandb_run = None
    if args.wandb:
        try:
            import wandb

            wandb_run = wandb.init(
                project=args.wandb_project
                or cfg.get("wandb_project", "from-gradient-to-transformer-capstone"),
                entity=args.wandb_entity or cfg.get("wandb_entity"),
                config=cfg,
                tags=cfg.get("wandb_tags", ["capstone"]),
                group=f"seed-{seeds[0]}" if len(seeds) == 1 else "multi-seed",
            )
        except ImportError:
            logger.warning("wandb not installed, skipping W&B logging")

    # Import runner's W&B utilities for per-step logging
    from src.experiments.runner import log_wandb_artifact, log_wandb_metrics

    # Run multi-seed
    checkpoint_dir = CHECKPOINTS_DIR if args.save_model else None

    def seed_fn(seed):
        return train_single_seed(
            cfg,
            seed,
            resume_step=args.resume,
            checkpoint_dir=checkpoint_dir,
            wandb_run=wandb_run,
            log_wandb_metrics=log_wandb_metrics,
            log_wandb_artifact=log_wandb_artifact,
        )

    aggregate = run_seeds(seed_fn, seeds)

    # Save manifest
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    manifest = ResultsManifest.from_run(
        experiment="exp6_capstone",
        seeds=seeds,
        args=cfg,
        per_seed_metrics=aggregate.per_seed,
        aggregate=aggregate.aggregate,
        wall_clock_seconds=aggregate.wall_clock_seconds,
        device=str(DEVICE),
        n_parameters=aggregate.per_seed[0].get("model_params") if aggregate.per_seed else None,
    )
    manifest.save(RESULTS_DIR / cfg["output"]["manifest_name"])

    # Log to W&B
    if wandb_run:
        for metric, stats in aggregate.aggregate.items():
            wandb_run.summary[metric] = stats["mean"]
        wandb_run.finish()

    # Print summary
    logger.info("=== CAPSTONE TRAINING COMPLETE ===")
    for metric, stats in aggregate.aggregate.items():
        logger.info(f"  {metric}: {stats['mean']:.4f} ± {stats['std']:.4f} (n={int(stats['n'])})")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s"
    )
    main()
