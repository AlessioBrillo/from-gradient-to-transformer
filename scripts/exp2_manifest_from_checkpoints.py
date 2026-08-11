#!/usr/bin/env python3
"""exp2 manifest producer — builds results/exp2_grokking.json from disk.

Micro-Phase 28: the P=113 flagship runs as three parallel processes (one
per seed, separate cores), each writing a rolling checkpoint
(--checkpoint-every 500) whose final state holds the full training history
and the trained model. This script is the analysis side of that launch: it
loads the final checkpoints, recomputes the headline metrics exactly as
run_single_seed would, aggregates across seeds in the same mean/std/min/max
shape verify-claims expects, and saves the manifest. Every number it
reports is re-derivable from this command and the checkpoints on disk.

Figures are regenerated from the best seed's checkpoint (the same plot
functions the single-seed run uses), so the session-4 analysis needs no
second training run.

Usage:
    python scripts/exp2_manifest_from_checkpoints.py \
        --checkpoint-dir checkpoints \
        [--start-ts 2026-08-11T19:40:00Z] \
        [--output results/exp2_grokking.json]
"""

import argparse
import time
from datetime import datetime, timezone
from pathlib import Path

import torch
from torch.utils.data import DataLoader

from src.experiments.exp2_grokking import (
    FIGURES_DIR,
    OneLayerTransformer,
    analyze_fourier_sparsity,
    fourier_decompose_embeddings,
    make_modular_addition_data,
    plot_ablation_curve,
    plot_fourier_weights,
    plot_grokking_curve,
    plot_progress_measures,
    run_ablation_sweep,
)
from src.results import ResultsManifest, count_parameters

# The launch config shared by the three parallel processes (canonical P=113
# flagships, frozen in ADR-0003 and mirrored by `make reproduce-grokking`).
CANONICAL_ARGS = {
    "seed": 0,  # per-seed; listed here for provenance of the shared config
    "modulus": 113,
    "train_fraction": 0.3,
    "d_model": 128,
    "d_mlp": 512,
    "n_heads": 4,
    "epochs": 5000,
    "lr": 1e-3,
    "weight_decay": 1.0,
    "batch_size": 512,
    "progress_interval": 10,
    "checkpoint_every": 500,
}


def metrics_from_checkpoint(path: Path, args: argparse.Namespace) -> dict[str, float]:
    """Recompute the headline metrics from one final checkpoint on disk,
    mirroring run_single_seed's metric definitions exactly (generalization
    epoch = first epoch with val_acc > 0.9, etc.)."""
    ckpt = torch.load(path, map_location="cpu")
    history = ckpt["history"]
    modulus = args.modulus

    model = OneLayerTransformer(
        d_model=args.d_model, d_mlp=args.d_mlp, n_heads=args.n_heads, modulus=modulus,
    )
    model.load_state_dict(ckpt["model"])

    fourier_result = fourier_decompose_embeddings(
        model.embed.weight.data.detach().cpu(), modulus
    )
    sparsity = analyze_fourier_sparsity(fourier_result, top_k=20)

    return {
        "final_val_acc": float(history["val_acc"][-1]),
        "generalization_epoch": float(
            next((i for i, acc in enumerate(history["val_acc"]) if acc > 0.9), -1)
        ),
        "final_fourier_sparsity": float(history["fourier_sparsity"][-1]),
        "k_90_percent": float(sparsity["k_90_percent"]),
        "k_99_percent": float(sparsity["k_99_percent"]),
        "total_mass_top_k": float(sparsity["total_mass_top_k"]),
    }


def aggregate(per_seed: list[dict[str, float]]) -> dict[str, dict[str, float]]:
    """Identical shape to runner.run_seeds' aggregation (verify_claims
    checks aggregate[key]['n'] against len(seeds))."""
    import numpy as np

    keys = set(per_seed[0].keys())
    out: dict[str, dict[str, float]] = {}
    for key in keys:
        values = np.array([m[key] for m in per_seed], dtype=float)
        out[key] = {
            "mean": float(values.mean()),
            "std": float(values.std(ddof=0)) if len(values) > 1 else 0.0,
            "min": float(values.min()),
            "max": float(values.max()),
            "n": float(len(values)),
        }
    return out


def best_seed_checkpoint(checkpoint_dir: Path, seeds: list[int]) -> Path:
    """The seed with the highest final validation accuracy drives the
    figures, so the plotted curves are the flagship's best instance."""
    best_path, best_acc = None, -1.0
    for seed in seeds:
        path = checkpoint_dir / f"exp2_checkpoint_seed{seed}.pt"
        if not path.exists():
            raise SystemExit(f"missing checkpoint for seed {seed}: {path}")
        ckpt = torch.load(path, map_location="cpu")
        acc = float(ckpt["history"]["val_acc"][-1])
        if acc > best_acc:
            best_path, best_acc = path, acc
    assert best_path is not None
    return best_path


def regenerate_figures(path: Path, args: argparse.Namespace) -> None:
    """Regenerate the four flagship figures from one checkpoint's history
    and weights — the same plots the single-seed path produces, but from
    disk (no second training run needed)."""
    ckpt = torch.load(path, map_location="cpu")
    history = ckpt["history"]
    modulus = args.modulus

    model = OneLayerTransformer(
        d_model=args.d_model, d_mlp=args.d_mlp, n_heads=args.n_heads, modulus=modulus,
    )
    model.load_state_dict(ckpt["model"])

    _, val_dataset = make_modular_addition_data(
        modulus=modulus, train_fraction=args.train_fraction, seed=0
    )
    val_loader = DataLoader(val_dataset, batch_size=args.batch_size, shuffle=False)

    fourier_result = fourier_decompose_embeddings(
        model.embed.weight.data.detach().cpu(), modulus
    )
    ablation = run_ablation_sweep(model, val_loader, fourier_result, modulus)

    plot_grokking_curve(history, save_path=FIGURES_DIR / "exp2_grokking_curve.png")
    plot_fourier_weights(
        fourier_result, modulus=modulus,
        save_path=FIGURES_DIR / "exp2_fourier_weights.png",
    )
    plot_ablation_curve(
        ablation, modulus=modulus,
        save_path=FIGURES_DIR / "exp2_frequency_ablation.png",
    )
    plot_progress_measures(history, save_path=FIGURES_DIR / "exp2_progress_measures.png")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint-dir", default="checkpoints")
    parser.add_argument("--seeds", default="0,1,2")
    parser.add_argument("--output", default="results/exp2_grokking.json")
    parser.add_argument(
        "--start-ts",
        default=None,
        help="ISO launch timestamp of the parallel runs (from the heartbeat "
             "log); wall clock is computed from it when given, else from the "
             "checkpoint mtimes (a lower bound).",
    )
    parser.add_argument("--no-figures", action="store_true")
    args = parser.parse_args()

    for key, value in CANONICAL_ARGS.items():
        if not hasattr(args, key):
            setattr(args, key, value)

    checkpoint_dir = Path(args.checkpoint_dir)
    seeds = [int(s) for s in args.seeds.split(",") if s.strip()]
    launch_args = dict(CANONICAL_ARGS)
    launch_args.update({"seeds": seeds, "checkpoint_dir": args.checkpoint_dir})

    per_seed = [
        metrics_from_checkpoint(
            checkpoint_dir / f"exp2_checkpoint_seed{seed}.pt", args
        )
        for seed in seeds
    ]

    if args.start_ts:
        start = datetime.fromisoformat(args.start_ts.replace("Z", "+00:00"))
        end = datetime.now(timezone.utc)
        wall_clock = (end - start).total_seconds()
        wall_source = "heartbeat-log launch timestamp"
    else:
        mtimes = [
            (checkpoint_dir / f"exp2_checkpoint_seed{seed}.pt").stat().st_mtime
            for seed in seeds
        ]
        wall_clock = max(mtimes) - min(mtimes)
        wall_source = "lower bound from final-checkpoint mtimes"

    probe_model = OneLayerTransformer(
        d_model=args.d_model, d_mlp=args.d_mlp, n_heads=args.n_heads,
        modulus=args.modulus,
    )
    manifest = ResultsManifest.from_run(
        experiment="exp2_grokking",
        seeds=seeds,
        args=launch_args,
        per_seed_metrics=per_seed,
        aggregate=aggregate(per_seed),
        wall_clock_seconds=float(wall_clock),
        device="cpu",
        n_parameters=count_parameters(probe_model),
        notes="P=113 x3 seeds launched as three parallel processes (one per "
              f"core, OMP_NUM_THREADS=3 each, checkpoint-every 500); manifest "
              f"built from the final checkpoints by "
              f"scripts/exp2_manifest_from_checkpoints.py; wall clock = "
              f"{wall_source}.",
    )
    manifest.save(Path(args.output))
    print(f"Saved manifest: {args.output} (wall_clock={wall_clock:.0f}s, "
          f"source: {wall_source})")
    for key in sorted(manifest.aggregate):
        agg = manifest.aggregate[key]
        print(f"  {key}: {agg['mean']:.4f} ± {agg['std']:.4f} "
              f"(n={int(agg['n'])}, range [{agg['min']:.4f}, {agg['max']:.4f}])")

    if not args.no_figures:
        best = best_seed_checkpoint(checkpoint_dir, seeds)
        print(f"Regenerating figures from best seed checkpoint: {best}")
        t0 = time.monotonic()
        regenerate_figures(best, args)
        print(f"Figures regenerated in {time.monotonic() - t0:.1f}s")


if __name__ == "__main__":
    main()
