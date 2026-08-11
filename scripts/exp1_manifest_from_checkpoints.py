#!/usr/bin/env python3
"""exp1 manifest producer — builds results/exp1_induction_heads.json from disk.

Micro-Phase 28: the R1 `--standard` run (ADR-0003 row 3) runs as three
parallel processes (one per seed), each writing a rolling checkpoint
(--checkpoint-every 250) whose final state holds the full training history.
This script is the analysis side of that launch: it loads the final
checkpoints, recomputes the headline metrics from the saved per-epoch
history (val accuracy, diag+1 mass, generalization epoch), applies the
row-3 verdict criteria mechanically (head formed = diag+1 mass > 0.3
sustained >= 5 cadence checkpoints), aggregates across seeds in the
mean/std/min/max shape verify-claims expects, and saves the manifest.

Every number it reports is re-derivable from this command and the
checkpoints on disk. Figures are NOT regenerated here: each parallel seed
run's own pipeline already wrote them.

Usage:
    python scripts/exp1_manifest_from_checkpoints.py \
        --checkpoint-dir checkpoints \
        [--start-ts 2026-08-11T21:04:00Z] \
        [--output results/exp1_induction_heads.json]
"""

import argparse
from datetime import datetime
from pathlib import Path

import numpy as np
import torch

from src.experiments.exp1_induction_heads import AttentionOnlyTransformer
from src.results import ResultsManifest, count_parameters

# The launch config shared by the three parallel processes (the Micro-Phase
# 10 standard pinning, mirrored by `make reproduce-induction`).
STANDARD_ARGS = {
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
}

# Row-3 frozen verdict criteria (ADR-0003): diag+1 mass threshold and the
# required sustained checkpoints.
DIAG1_THRESHOLD = 0.3
SUSTAINED_CKPT_COUNT = 5
VAL_ACC_GENERALIZATION = 0.9


def metrics_from_checkpoint(path: Path, args: argparse.Namespace) -> dict[str, float]:
    """Recompute the headline metrics from one final checkpoint on disk,
    mirroring the per-seed run's metric definitions exactly."""
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


def aggregate(per_seed: list[dict[str, float]]) -> dict[str, dict[str, float]]:
    """Identical shape to runner.run_seeds' aggregation (verify_claims
    checks aggregate[key]['n'] against len(seeds))."""
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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint-dir", default="checkpoints")
    parser.add_argument("--seeds", default="0,1,2")
    parser.add_argument("--output", default="results/exp1_induction_heads.json")
    parser.add_argument(
        "--start-ts",
        default=None,
        help="ISO launch timestamp of the parallel runs (from the heartbeat "
             "log); wall clock is computed from it when given, else from the "
             "checkpoint mtimes (a lower bound).",
    )
    args = parser.parse_args()

    for key, value in STANDARD_ARGS.items():
        if not hasattr(args, key):
            setattr(args, key, value)

    checkpoint_dir = Path(args.checkpoint_dir)
    seeds = [int(s) for s in args.seeds.split(",") if s.strip()]
    launch_args = dict(STANDARD_ARGS)
    launch_args.update({"seeds": seeds, "checkpoint_dir": args.checkpoint_dir})

    per_seed = [
        metrics_from_checkpoint(
            checkpoint_dir / f"exp1_checkpoint_seed{seed}.pt", args
        )
        for seed in seeds
    ]

    if args.start_ts:
        # LAUNCH_TS in the heartbeat log is stamped in LOCAL time (with a
        # cosmetic "Z"); parse it naive-local and compare against the last
        # final-checkpoint mtime, also local — same clock, no tz math.
        start_local = datetime.fromisoformat(args.start_ts.replace("Z", ""))
        end_local = datetime.fromtimestamp(
            max(
                (checkpoint_dir / f"exp1_checkpoint_seed{seed}.pt")
                .stat()
                .st_mtime
                for seed in seeds
            )
        )
        wall_clock = (end_local - start_local).total_seconds()
        wall_source = "heartbeat-log launch ts -> last final-checkpoint mtime (local clock)"
    else:
        mtimes = [
            (checkpoint_dir / f"exp1_checkpoint_seed{seed}.pt").stat().st_mtime
            for seed in seeds
        ]
        wall_clock = max(mtimes) - min(mtimes)
        wall_source = "lower bound from final-checkpoint mtimes"

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
        args=launch_args,
        per_seed_metrics=per_seed,
        aggregate=aggregate(per_seed),
        wall_clock_seconds=float(wall_clock),
        device="cpu",
        n_parameters=count_parameters(probe_model),
        notes="R1 standard x3 seeds launched as three parallel processes (one "
              "per core, OMP_NUM_THREADS=3 each, checkpoint-every 250); "
              "manifest built from the final checkpoints by "
              "scripts/exp1_manifest_from_checkpoints.py; wall clock = "
              f"{wall_source}.",
    )
    manifest.save(Path(args.output))
    print(f"Saved manifest: {args.output} (wall_clock={wall_clock:.0f}s, "
          f"source: {wall_source})")
    for key in sorted(manifest.aggregate):
        agg = manifest.aggregate[key]
        print(f"  {key}: {agg['mean']:.4f} ± {agg['std']:.4f} "
              f"(n={int(agg['n'])}, range [{agg['min']:.4f}, {agg['max']:.4f}])")


if __name__ == "__main__":
    main()
