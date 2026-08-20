#!/usr/bin/env python3
"""Manifest producer — builds results/<experiment>.json from disk checkpoints.

Micro-Phase 28: a rung's standard-scale run launches as parallel processes
(one per seed), each writing a rolling checkpoint (--checkpoint-every N)
whose final state holds the full training history and the trained model.
This script is the analysis side of that launch: it loads the final
checkpoints, recomputes the headline metrics exactly as the live runner
would, aggregates across seeds in the same mean/std/min/max shape
verify-claims expects, and saves the manifest. Every number it reports is
re-derivable from this command and the checkpoints on disk.

exp2 additionally regenerates its flagship figures from the best seed's
checkpoint (the same plot functions the single-seed run uses), so the
analysis needs no second training run.

Usage:
    python scripts/manifest_from_checkpoints.py --experiment exp1_induction_heads \
        --checkpoint-dir checkpoints \
        [--start-ts 2026-08-11T21:04:00Z] \
        [--output results/exp1_induction_heads.json]
    python scripts/manifest_from_checkpoints.py --experiment exp2_grokking \
        --checkpoint-dir checkpoints --no-figures
"""

import argparse
import time
from datetime import datetime
from pathlib import Path
from typing import Callable, Optional

import torch
from torch.utils.data import DataLoader

from src.experiments.exp1_induction_heads import AttentionOnlyTransformer
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
from src.experiments.runner import aggregate_metrics
from src.results import ResultsManifest, count_parameters

# Row-3 frozen verdict criteria (ADR-0003): diag+1 mass threshold and the
# required sustained checkpoints.
DIAG1_THRESHOLD = 0.3
SUSTAINED_CKPT_COUNT = 5
VAL_ACC_GENERALIZATION = 0.9


def exp1_metrics(path: Path, args: argparse.Namespace) -> dict[str, float]:
    """Recompute the R1 headline metrics from one final checkpoint, mirroring
    the per-seed run's metric definitions exactly."""
    ckpt = torch.load(path, map_location="cpu")
    history = ckpt["history"]
    val_acc = history["val_acc"]
    diag1 = history["diag1_mass"]
    cadence = args.checkpoint_every

    # Cadence checkpoints: the points the rolling checkpointer would have
    # written ((epoch + 1) % cadence == 0, 0-indexed history).
    idxs = [i for i in range(len(val_acc)) if (i + 1) % cadence == 0]

    def sustained(series: list[float], threshold: float, n: int) -> int:
        """Trailing count of consecutive cadence checkpoints above threshold."""
        at_cadence = [series[i] > threshold for i in idxs]
        count = 0
        for ok in reversed(at_cadence):
            if not ok:
                break
            count += 1
        return count

    head_formed = diag1[-1] > DIAG1_THRESHOLD
    sustained_ok = sustained(diag1, DIAG1_THRESHOLD, SUSTAINED_CKPT_COUNT)

    return {
        "final_val_acc": float(val_acc[-1]),
        "final_diag1_mass": float(diag1[-1]),
        "generalization_epoch": float(
            next((i for i, acc in enumerate(val_acc) if acc > VAL_ACC_GENERALIZATION), -1)
        ),
        "head_formation_epoch": float(
            next((i for i, d in enumerate(diag1) if d > DIAG1_THRESHOLD), -1)
        ),
        "sustained_head_checkpoints": float(sustained_ok),
        "head_formed": float(head_formed),
        "head_formed_and_sustained": float(head_formed and sustained_ok >= SUSTAINED_CKPT_COUNT),
    }


def exp2_metrics(path: Path, args: argparse.Namespace) -> dict[str, float]:
    """Recompute the grokking headline metrics from one final checkpoint,
    mirroring run_single_seed's metric definitions exactly (generalization
    epoch = first epoch with val_acc > 0.9, etc.)."""
    ckpt = torch.load(path, map_location="cpu")
    history = ckpt["history"]
    modulus = args.modulus

    model = OneLayerTransformer(
        d_model=args.d_model,
        d_mlp=args.d_mlp,
        n_heads=args.n_heads,
        modulus=modulus,
    )
    model.load_state_dict(ckpt["model"])

    fourier_result = fourier_decompose_embeddings(model.embed.weight.data.detach().cpu(), modulus)
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


def exp2_figures(checkpoint_dir: Path, seeds: list[int], args: argparse.Namespace) -> None:
    """Regenerate the four flagship figures from the best seed's checkpoint —
    the same plots the single-seed path produces, but from disk (no second
    training run needed)."""

    def best_seed_checkpoint() -> Path:
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

    path = best_seed_checkpoint()
    print(f"Regenerating figures from best seed checkpoint: {path}")
    ckpt = torch.load(path, map_location="cpu")
    history = ckpt["history"]
    modulus = args.modulus

    model = OneLayerTransformer(
        d_model=args.d_model,
        d_mlp=args.d_mlp,
        n_heads=args.n_heads,
        modulus=modulus,
    )
    model.load_state_dict(ckpt["model"])

    _, val_dataset = make_modular_addition_data(
        modulus=modulus, train_fraction=args.train_fraction, seed=0
    )
    val_loader = DataLoader(val_dataset, batch_size=args.batch_size, shuffle=False)

    fourier_result = fourier_decompose_embeddings(model.embed.weight.data.detach().cpu(), modulus)
    ablation = run_ablation_sweep(model, val_loader, fourier_result, modulus)

    plot_grokking_curve(history, save_path=FIGURES_DIR / "exp2_grokking_curve.png")
    plot_fourier_weights(
        fourier_result,
        modulus=modulus,
        save_path=FIGURES_DIR / "exp2_fourier_weights.png",
    )
    plot_ablation_curve(
        ablation,
        modulus=modulus,
        save_path=FIGURES_DIR / "exp2_frequency_ablation.png",
    )
    plot_progress_measures(history, save_path=FIGURES_DIR / "exp2_progress_measures.png")


# experiment -> (launch config, notes, metrics extractor, figure regenerator).
# The launch configs are the canonical flagships frozen in ADR-0003 and
# mirrored by `make reproduce-<rung>`.
EXPERIMENTS: dict[
    str,
    tuple[
        dict,
        str,
        Callable[[Path, argparse.Namespace], dict[str, float]],
        Optional[Callable[[Path, list[int], argparse.Namespace], None]],
    ],
] = {
    "exp1_induction_heads": (
        {
            "seed": 0,  # per-seed; listed here for provenance of the shared config
            "vocab_size": 2048,
            "seq_len": 64,
            "d_model": 64,
            "n_layers": 2,
            "n_heads": 4,
            "epochs": 3000,
            "lr": 1e-3,
            "weight_decay": 0.1,
            "batch_size": 64,
            "num_train": 8192,
            "fresh_batches": True,
            "checkpoint_every": 250,
        },
        "R1 standard x3 seeds launched as three parallel processes (one per "
        "core, OMP_NUM_THREADS=3 each, checkpoint-every 250); manifest "
        "built from the final checkpoints by "
        "scripts/manifest_from_checkpoints.py; wall clock = ",
        exp1_metrics,
        None,
    ),
    "exp2_grokking": (
        {
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
        },
        "P=113 x3 seeds launched as three parallel processes (one per "
        "core, OMP_NUM_THREADS=3 each, checkpoint-every 500); manifest "
        "built from the final checkpoints by "
        "scripts/manifest_from_checkpoints.py; wall clock = ",
        exp2_metrics,
        exp2_figures,
    ),
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--experiment", required=True, choices=sorted(EXPERIMENTS))
    parser.add_argument("--checkpoint-dir", default="checkpoints")
    parser.add_argument("--seeds", default="0,1,2")
    parser.add_argument("--output", default=None)
    parser.add_argument(
        "--start-ts",
        default=None,
        help="ISO launch timestamp of the parallel runs (from the heartbeat "
        "log); wall clock is computed from it when given, else from the "
        "checkpoint mtimes (a lower bound).",
    )
    parser.add_argument("--no-figures", action="store_true")
    args = parser.parse_args()

    launch_args, notes_prefix, metrics_fn, figures_fn = EXPERIMENTS[args.experiment]
    args.output = args.output or f"results/{args.experiment}.json"
    for key, value in launch_args.items():
        if not hasattr(args, key):
            setattr(args, key, value)

    checkpoint_dir = Path(args.checkpoint_dir)
    seeds = [int(s) for s in args.seeds.split(",") if s.strip()]
    prefix = args.experiment.split("_")[0]
    run_args = dict(launch_args)
    run_args.update({"seeds": seeds, "checkpoint_dir": args.checkpoint_dir})

    per_seed = [
        metrics_fn(checkpoint_dir / f"{prefix}_checkpoint_seed{seed}.pt", args) for seed in seeds
    ]

    if args.start_ts:
        # LAUNCH_TS in the heartbeat log is stamped in LOCAL time (with a
        # cosmetic "Z"); parse it naive-local and compare against the last
        # final-checkpoint mtime, also local — same clock, no tz math.
        start_local = datetime.fromisoformat(args.start_ts.replace("Z", ""))
        end_local = datetime.fromtimestamp(
            max(
                (checkpoint_dir / f"{prefix}_checkpoint_seed{seed}.pt").stat().st_mtime
                for seed in seeds
            )
        )
        wall_clock = (end_local - start_local).total_seconds()
        wall_source = "heartbeat-log launch ts -> last final-checkpoint mtime (local clock)"
    else:
        mtimes = [
            (checkpoint_dir / f"{prefix}_checkpoint_seed{seed}.pt").stat().st_mtime
            for seed in seeds
        ]
        wall_clock = max(mtimes) - min(mtimes)
        wall_source = "lower bound from final-checkpoint mtimes"

    if args.experiment == "exp1_induction_heads":
        probe_model: torch.nn.Module = AttentionOnlyTransformer(
            vocab_size=args.vocab_size,
            d_model=args.d_model,
            n_layers=args.n_layers,
            n_heads=args.n_heads,
            max_seq_len=args.seq_len,
        )
    else:
        probe_model = OneLayerTransformer(
            d_model=args.d_model,
            d_mlp=args.d_mlp,
            n_heads=args.n_heads,
            modulus=args.modulus,
        )

    manifest = ResultsManifest.from_run(
        experiment=args.experiment,
        seeds=seeds,
        args=run_args,
        per_seed_metrics=per_seed,
        aggregate=aggregate_metrics(per_seed),
        wall_clock_seconds=float(wall_clock),
        device="cpu",
        n_parameters=count_parameters(probe_model),
        notes=notes_prefix + f"{wall_source}.",
    )
    manifest.save(Path(args.output))
    print(f"Saved manifest: {args.output} (wall_clock={wall_clock:.0f}s, source: {wall_source})")
    for key in sorted(manifest.aggregate):
        agg = manifest.aggregate[key]
        print(
            f"  {key}: {agg['mean']:.4f} ± {agg['std']:.4f} "
            f"(n={int(agg['n'])}, range [{agg['min']:.4f}, {agg['max']:.4f}])"
        )

    if figures_fn is not None and not args.no_figures:
        t0 = time.monotonic()
        figures_fn(checkpoint_dir, seeds, args)
        print(f"Figures regenerated in {time.monotonic() - t0:.1f}s")


if __name__ == "__main__":
    main()
