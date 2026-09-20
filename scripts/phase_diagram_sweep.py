#!/usr/bin/env python3
"""Phase Diagram Sweep Runner for Grokking.

Runs a targeted sweep over modulus P, model size, weight decay, and training mode
(solo vs joint), collecting per-cell aggregates across 3 seeds. Emits a manifest
with all cell measurements for phase diagram analysis.

Usage:
    python scripts/phase_diagram_sweep.py --config configs/phase_diagram_sweep.yaml
"""

import argparse
import logging
import math
import subprocess
import sys
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import torch
import yaml

from src.experiments.runner import parse_seeds, run_seeds
from src.reproducibility import set_seed
from src.results import ResultsManifest, count_parameters

logger = logging.getLogger(__name__)

RESULTS_DIR = Path("results")
CHECKPOINTS_DIR = Path("checkpoints")
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


@dataclass
class SweepCell:
    """A single cell in the phase diagram sweep."""
    cell_id: str
    modulus: int
    d_model: int
    n_layers: int
    n_heads: int
    d_mlp: int
    weight_decay: float
    mode: str  # "solo" or "joint"
    train_fraction: float = 0.3
    lr: float = 1e-3
    epochs: int = 2000
    batch_size: int = 128
    warmup_steps: int = 100
    checkpoint_every: int = 500
    seed: int = 42  # base seed, actual seeds = seed + 0,1,2

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "SweepCell":
        return cls(**d)


@dataclass
class CellResult:
    """Aggregated results for one cell (3 seeds)."""
    cell_id: str
    modulus: int
    d_model: int
    n_layers: int
    n_heads: int
    d_mlp: int
    weight_decay: float
    mode: str
    seeds: list[int]
    wall_clock_seconds: float
    # Aggregate metrics (mean/std/min/max/n)
    final_val_acc: dict[str, float]
    generalization_epoch: dict[str, float]
    final_fourier_sparsity: dict[str, float]
    k_90_percent: dict[str, float]
    k_99_percent: dict[str, float]
    total_mass_top_k: dict[str, float]
    # Joint-specific metrics (if mode == "joint")
    final_induction_acc: dict[str, float] | None = None
    final_kcomp: dict[str, float] | None = None

    def is_sparse(self) -> bool:
        """Check if cell shows sparse Fourier regime (k_99 / P < 0.5)."""
        return self.k_99_percent["mean"] < self.modulus * 0.5

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "CellResult":
        return cls(**d)


def load_existing_manifest(manifest_path: Path) -> dict[str, CellResult] | None:
    """Load existing phase diagram manifest if it exists."""
    if not manifest_path.exists():
        return None
    try:
        data = torch.load(manifest_path, map_location="cpu", weights_only=False)
        if isinstance(data, dict) and "cells" in data:
            return {k: CellResult.from_dict(v) for k, v in data["cells"].items()}
        return None
    except Exception as e:
        logger.warning(f"Failed to load existing manifest: {e}")
        return None


def save_manifest(manifest_path: Path, cells: dict[str, CellResult], metadata: dict[str, Any]) -> None:
    """Save phase diagram manifest with provenance."""
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    data = {
        "metadata": metadata,
        "cells": {k: v.to_dict() for k, v in cells.items()},
    }
    torch.save(data, manifest_path)
    logger.info(f"Saved sweep manifest to {manifest_path} ({len(cells)} cells)")


# Import experiment functions
from src.experiments.exp2_grokking import (
    OneLayerTransformer,
    make_modular_addition_data,
    train_model,
    fourier_decompose_embeddings,
    analyze_fourier_sparsity,
)
from src.experiments.exp6_capstone import (
    DecoderOnlyTransformer,
    make_mixed_dataloaders,
    compute_k_composition_scores,
    make_modular_addition_data as make_capstone_modular_data,
    make_repeated_token_data,
)
from tqdm import tqdm


def run_solo_cell(cell: SweepCell) -> CellResult:
    """Run a solo modular addition cell (3 seeds) via exp2_grokking."""

    def run_single_seed(seed: int) -> dict[str, float]:
        set_seed(seed)

        # Data - use the exact same function as exp2_grokking
        train_dataset, val_dataset = make_modular_addition_data(
            modulus=cell.modulus,
            train_fraction=cell.train_fraction,
            seed=seed,
        )
        train_loader = torch.utils.data.DataLoader(
            train_dataset, batch_size=cell.batch_size, shuffle=True
        )
        val_loader = torch.utils.data.DataLoader(
            val_dataset, batch_size=cell.batch_size, shuffle=False
        )

        # Model (Nanda config: 1-layer)
        model = OneLayerTransformer(
            d_model=cell.d_model,
            d_mlp=cell.d_mlp,
            n_heads=cell.n_heads,
            modulus=cell.modulus,
        ).to(DEVICE)

        # Train - use the exact same training function
        history = train_model(
            model=model,
            train_loader=train_loader,
            val_loader=val_loader,
            epochs=cell.epochs,
            lr=cell.lr,
            weight_decay=cell.weight_decay,
            seed=seed,
            use_wandb=False,
            progress_interval=10,
            checkpoint_dir=str(CHECKPOINTS_DIR) if cell.checkpoint_every > 0 else None,
            checkpoint_every=cell.checkpoint_every,
            resume_from=None,
            schedule="cosine",
        )

        # Fourier analysis
        fourier_result = fourier_decompose_embeddings(
            model.embed.weight.data.detach().cpu(), cell.modulus
        )
        sparsity = analyze_fourier_sparsity(fourier_result, top_k=20)

        final_val_acc = history["val_acc"][-1]
        generalization_epoch = next(
            (i for i, acc in enumerate(history["val_acc"]) if acc > 0.9), -1
        )

        return {
            "final_val_acc": float(final_val_acc),
            "generalization_epoch": float(generalization_epoch),
            "final_fourier_sparsity": float(history["fourier_sparsity"][-1]),
            "k_90_percent": float(sparsity["k_90_percent"]),
            "k_99_percent": float(sparsity["k_99_percent"]),
            "total_mass_top_k": float(sparsity["total_mass_top_k"]),
        }

    seeds = [cell.seed, cell.seed + 1, cell.seed + 2]
    result = run_seeds(run_single_seed, seeds)

    return CellResult(
        cell_id=cell.cell_id,
        modulus=cell.modulus,
        d_model=cell.d_model,
        n_layers=cell.n_layers,
        n_heads=cell.n_heads,
        d_mlp=cell.d_mlp,
        weight_decay=cell.weight_decay,
        mode="solo",
        seeds=seeds,
        wall_clock_seconds=result.wall_clock_seconds,
        final_val_acc=result.aggregate.get("final_val_acc", {"mean": 0, "std": 0, "min": 0, "max": 0, "n": 3}),
        generalization_epoch=result.aggregate.get("generalization_epoch", {"mean": 0, "std": 0, "min": 0, "max": 0, "n": 3}),
        final_fourier_sparsity=result.aggregate.get("final_fourier_sparsity", {"mean": 0, "std": 0, "min": 0, "max": 0, "n": 3}),
        k_90_percent=result.aggregate.get("k_90_percent", {"mean": 0, "std": 0, "min": 0, "max": 0, "n": 3}),
        k_99_percent=result.aggregate.get("k_99_percent", {"mean": 0, "std": 0, "min": 0, "max": 0, "n": 3}),
        total_mass_top_k=result.aggregate.get("total_mass_top_k", {"mean": 0, "std": 0, "min": 0, "max": 0, "n": 3}),
    )


def run_joint_cell(cell: SweepCell) -> CellResult:
    """Run a joint modular+induction cell (3 seeds) via exp6_capstone."""

    def run_single_seed(seed: int) -> dict[str, float]:
        set_seed(seed)

        vocab_size = 2048 + cell.modulus + 10
        seq_len = 128

        model = DecoderOnlyTransformer(
            vocab_size=vocab_size,
            d_model=cell.d_model,
            n_layers=cell.n_layers,
            n_heads=cell.n_heads,
            d_mlp=cell.d_mlp,
            max_seq_len=seq_len,
            dropout=0.1,
        ).to(DEVICE)

        # Data - use the exact same function as exp6_capstone
        train_loader, val_loader = make_mixed_dataloaders(
            {
                "task": {
                    "modular": {
                        "modulus": cell.modulus,
                        "train_fraction": cell.train_fraction,
                    },
                    "induction": {
                        "vocab_size": 2048,
                        "seq_len": seq_len,
                        "num_train": 8192,
                        "num_val": 1024,
                        "prefix_ratio": 0.5,
                    },
                },
                "training": {
                    "batch_size": cell.batch_size,
                },
            },
            seed,
        )

        # Optimizer
        optimizer = torch.optim.AdamW(
            model.parameters(), lr=cell.lr, weight_decay=cell.weight_decay
        )

        def lr_lambda(step):
            if step < cell.warmup_steps:
                return step / cell.warmup_steps
            progress = (step - cell.warmup_steps) / (cell.epochs - cell.warmup_steps)
            return 0.5 * (1 + math.cos(math.pi * progress))

        scheduler = torch.optim.lr_scheduler.LambdaLR(optimizer, lr_lambda)

        # Training loop (step-based like exp6_capstone)
        model.train()
        step = 0
        pbar = tqdm(total=cell.epochs, desc=f"Seed {seed}", leave=False)

        mod_accs = []
        ind_accs = []

        while step < cell.epochs:
            for batch in train_loader:
                if step >= cell.epochs:
                    break
                x, y, mod_target, task_id = batch
                x = x.to(DEVICE)
                y = y.to(DEVICE)

                optimizer.zero_grad()
                logits, _ = model(x)

                if task_id == 0:
                    loss = torch.nn.functional.cross_entropy(
                        logits[:, 1, :], mod_target.to(DEVICE)
                    )
                else:
                    loss = torch.nn.functional.cross_entropy(
                        logits.view(-1, logits.size(-1)), y.view(-1)
                    )

                loss.backward()
                torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
                optimizer.step()
                scheduler.step()

                step += 1
                pbar.update(1)

                if step % 500 == 0:
                    # Quick validation
                    model.eval()
                    with torch.no_grad():
                        mod_correct = 0
                        mod_total = 0
                        ind_correct = 0
                        ind_total = 0
                        for vbatch in val_loader:
                            vx, vy, vmod_target, vtask_id = vbatch
                            vx = vx.to(DEVICE)
                            vy = vy.to(DEVICE)
                            vlogits, _ = model(vx)

                            if vtask_id == 0:
                                vacc = (
                                    vlogits[:, 1, :].argmax(-1) == vmod_target.to(DEVICE)
                                ).float().mean()
                                mod_correct += (vlogits[:, 1, :].argmax(-1) == vmod_target.to(DEVICE)).sum().item()
                                mod_total += vmod_target.numel()
                            else:
                                vacc = (vlogits.argmax(-1) == vy).float().mean()
                                ind_correct += (vlogits.argmax(-1) == vy).sum().item()
                                ind_total += vy.numel()

                        mod_acc = mod_correct / mod_total if mod_total > 0 else 0.0
                        ind_acc = ind_correct / ind_total if ind_total > 0 else 0.0
                        mod_accs.append(mod_acc)
                        ind_accs.append(ind_acc)
                    model.train()

        pbar.close()

        # Final evaluation
        model.eval()
        with torch.no_grad():
            # Modular - use capstone's data format (seq_len=128)
            mod_train, mod_val = make_capstone_modular_data(
                cell.modulus, cell.train_fraction, seq_len=seq_len, seed=seed, vocab_offset=0
            )
            mod_val_loader = torch.utils.data.DataLoader(mod_val, batch_size=cell.batch_size)

            mod_correct = 0
            mod_total = 0
            for x, y, mod_target in mod_val_loader:
                x = x.to(DEVICE)
                mod_target = mod_target.to(DEVICE)
                logits, _ = model(x)
                pred = logits[:, 1, :].argmax(-1)
                mod_correct += (pred == mod_target).sum().item()
                mod_total += mod_target.numel()
            mod_acc = mod_correct / mod_total if mod_total > 0 else 0.0

            # Induction
            ind_train, ind_val = make_repeated_token_data(
                vocab_size=2048, seq_len=seq_len, num_train=8192, num_val=1024, prefix_ratio=0.5, seed=seed + 1000
            )
            ind_val_loader = torch.utils.data.DataLoader(ind_val, batch_size=cell.batch_size)

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

            # Fourier on modular embeddings
            mod_embeddings = model.embed.weight[:cell.modulus]
            fourier_result = fourier_decompose_embeddings(mod_embeddings.detach().cpu(), cell.modulus)
            sparsity = analyze_fourier_sparsity(fourier_result, top_k=20)

            # K-composition
            kcomp_scores = compute_k_composition_scores(model, ind_val_loader, num_batches=5)
            head_scores = [v for k, v in kcomp_scores.items() if not k.startswith("_")]
            max_kcomp = max(head_scores) if head_scores else 0.0

        return {
            "final_val_acc": float(mod_acc),
            "generalization_epoch": float(next((i for i, acc in enumerate(mod_accs) if acc > 0.9), -1) * 500),
            "final_fourier_sparsity": float(sparsity["k_99_percent"] / cell.modulus),
            "k_90_percent": float(sparsity["k_90_percent"]),
            "k_99_percent": float(sparsity["k_99_percent"]),
            "total_mass_top_k": float(sparsity["total_mass_top_k"]),
            "final_induction_acc": float(ind_acc),
            "final_max_kcomp": float(max_kcomp),
        }

    seeds = [cell.seed, cell.seed + 1, cell.seed + 2]
    result = run_seeds(run_single_seed, seeds)

    return CellResult(
        cell_id=cell.cell_id,
        modulus=cell.modulus,
        d_model=cell.d_model,
        n_layers=cell.n_layers,
        n_heads=cell.n_heads,
        d_mlp=cell.d_mlp,
        weight_decay=cell.weight_decay,
        mode="joint",
        seeds=seeds,
        wall_clock_seconds=result.wall_clock_seconds,
        final_val_acc=result.aggregate.get("final_val_acc", {"mean": 0, "std": 0, "min": 0, "max": 0, "n": 3}),
        generalization_epoch=result.aggregate.get("generalization_epoch", {"mean": 0, "std": 0, "min": 0, "max": 0, "n": 3}),
        final_fourier_sparsity=result.aggregate.get("final_fourier_sparsity", {"mean": 0, "std": 0, "min": 0, "max": 0, "n": 3}),
        k_90_percent=result.aggregate.get("k_90_percent", {"mean": 0, "std": 0, "min": 0, "max": 0, "n": 3}),
        k_99_percent=result.aggregate.get("k_99_percent", {"mean": 0, "std": 0, "min": 0, "max": 0, "n": 3}),
        total_mass_top_k=result.aggregate.get("total_mass_top_k", {"mean": 0, "std": 0, "min": 0, "max": 0, "n": 3}),
        final_induction_acc=result.aggregate.get("final_induction_acc", {"mean": 0, "std": 0, "min": 0, "max": 0, "n": 3}),
        final_kcomp=result.aggregate.get("final_max_kcomp", {"mean": 0, "std": 0, "min": 0, "max": 0, "n": 3}),
    )


def generate_sweep_grid(config: dict) -> list[SweepCell]:
    """Generate cells from explicit config list."""
    cells = []

    # Fixed hyperparameters
    train_fraction = config.get("train_fraction", 0.3)
    lr = config.get("lr", 1e-3)
    batch_size = config.get("batch_size", 128)
    warmup_steps = config.get("warmup_steps", 100)
    checkpoint_every = config.get("checkpoint_every", 500)
    base_seed = config.get("base_seed", 42)
    epochs_default = config.get("epochs", 2000)
    epochs_small_p = config.get("epochs_small_p", 5000)

    for cell_config in config.get("cells", []):
        modulus = cell_config["modulus"]

        # Adjust epochs based on modulus
        epochs = epochs_small_p if modulus <= 59 else epochs_default

        cell = SweepCell(
            cell_id=cell_config["cell_id"],
            modulus=modulus,
            d_model=cell_config["d_model"],
            n_layers=cell_config["n_layers"],
            n_heads=cell_config["n_heads"],
            d_mlp=cell_config["d_mlp"],
            weight_decay=cell_config["weight_decay"],
            mode=cell_config["mode"],
            train_fraction=train_fraction,
            lr=lr,
            epochs=epochs,
            batch_size=batch_size,
            warmup_steps=warmup_steps,
            checkpoint_every=checkpoint_every,
            seed=base_seed,
        )
        cells.append(cell)

    logger.info(f"Generated {len(cells)} explicit cells from config")
    return cells


def main():
    parser = argparse.ArgumentParser(description="Phase Diagram Sweep Runner")
    parser.add_argument("--config", type=str, default="configs/phase_diagram_sweep.yaml")
    parser.add_argument("--manifest-path", type=str, default="results/phase_diagram.pt")
    parser.add_argument("--max-cells", type=int, default=None, help="Limit number of cells (for testing)")
    parser.add_argument("--dry-run", action="store_true", help="Print cells without running")
    parser.add_argument("--resume", action="store_true", help="Resume from existing manifest")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )

    # Load config
    with open(args.config) as f:
        config = yaml.safe_load(f)

    # Generate grid
    cells = generate_sweep_grid(config)

    if args.max_cells:
        cells = cells[:args.max_cells]
        logger.info(f"Limited to {args.max_cells} cells")

    if args.dry_run:
        for cell in cells:
            logger.info(f"  {cell.cell_id}: P={cell.modulus}, d_model={cell.d_model}, "
                       f"n_layers={cell.n_layers}, wd={cell.weight_decay}, mode={cell.mode}")
        return

    # Load existing manifest if resuming
    manifest_path = Path(args.manifest_path)
    existing = load_existing_manifest(manifest_path) if args.resume else {}
    completed = set(existing.keys()) if existing else set()

    # Filter out completed cells
    cells_to_run = [c for c in cells if c.cell_id not in completed]
    logger.info(f"Cells to run: {len(cells_to_run)} (completed: {len(completed)})")

    if not cells_to_run:
        logger.info("All cells already completed!")
        return

    # Run cells
    cells_results = dict(existing) if existing else {}
    start_time = time.monotonic()
    metadata = {}  # Initialize early

    for i, cell in enumerate(cells_to_run):
        logger.info(f"[{i+1}/{len(cells_to_run)}] Running {cell.cell_id}: "
                   f"P={cell.modulus}, d_model={cell.d_model}, "
                   f"n_layers={cell.n_layers}, wd={cell.weight_decay}, mode={cell.mode}")

        try:
            if cell.mode == "solo":
                result = run_solo_cell(cell)
            else:
                result = run_joint_cell(cell)

            cells_results[cell.cell_id] = result

            # Save incrementally
            metadata = {
                "config": config,
                "git_sha": subprocess.check_output(
                    ["git", "rev-parse", "--short", "HEAD"], text=True, stderr=subprocess.DEVNULL
                ).strip() if subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True).returncode == 0 else "unknown",
                "started_at": datetime.fromtimestamp(start_time, tz=timezone.utc).isoformat(),
                "updated_at": datetime.now(timezone.utc).isoformat(),
                "total_cells": len(cells),
                "completed_cells": len(cells_results),
            }
            save_manifest(manifest_path, cells_results, metadata)

            logger.info(f"  -> val_acc={result.final_val_acc['mean']:.4f}, "
                       f"k_99/P={result.k_99_percent['mean']/cell.modulus:.3f}, "
                       f"sparse={result.is_sparse()}")

        except Exception as e:
            logger.error(f"Cell {cell.cell_id} failed: {e}")
            import traceback
            traceback.print_exc()
            # Continue with other cells

    total_time = time.monotonic() - start_time
    logger.info(f"Sweep complete: {len(cells_results)}/{len(cells)} cells in {total_time/60:.1f} min")

    # Final save
    metadata["completed_at"] = datetime.now(timezone.utc).isoformat()
    metadata["total_wall_clock_seconds"] = total_time
    save_manifest(manifest_path, cells_results, metadata)

    # Summary
    sparse_cells = sum(1 for r in cells_results.values() if r.is_sparse())
    logger.info(f"Sparse regime cells: {sparse_cells}/{len(cells_results)}")


if __name__ == "__main__":
    main()