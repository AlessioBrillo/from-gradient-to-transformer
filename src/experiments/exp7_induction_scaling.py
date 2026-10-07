#!/usr/bin/env python3
"""Rung 1 (Scaled) — Induction benchmark for scaled transformers.

Designed for high-throughput GPU training and mechanistic probing.
"""
import argparse
import logging
from pathlib import Path

from src.experiments.exp1_induction_heads import (
    DEVICE,
    AttentionOnlyTransformer,
    ResultsManifest,
    count_parameters,
    parse_seeds,
    run_seeds,
    run_single_seed,
)

logger = logging.getLogger(__name__)

def main() -> None:
    parser = argparse.ArgumentParser(description="Scaled Induction Benchmark")
    parser.add_argument("--seeds", type=str, default="42", help="Comma-separated seeds")
    parser.add_argument("--d-model", type=int, default=256, help="Model dimension")
    parser.add_argument("--n-layers", type=int, default=4, help="Number of layers")
    parser.add_argument("--n-heads", type=int, default=8, help="Heads per layer")
    parser.add_argument("--epochs", type=int, default=1000, help="Training epochs")

    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)

    # Standard induction config for scaling
    class ScaledArgs:
        def __init__(self, d_model, n_layers, n_heads, epochs):
            self.seed = 42
            self.vocab_size = 2048
            self.seq_len = 128
            self.d_model = d_model
            self.n_layers = n_layers
            self.n_heads = n_heads
            self.epochs = epochs
            self.lr = 1e-3
            self.weight_decay = 0.1
            self.batch_size = 128
            self.num_train = 16384
            self.no_train = False
            self.quick = False
            self.standard = False
            self.wandb = False
            self.fresh_batches = True
            self.checkpoint_dir = "checkpoints"
            self.checkpoint_every = 0
            self.resume = False
            self.resume_from = None
            self.save_manifest = True

    scaled_args = ScaledArgs(args.d_model, args.n_layers, args.n_heads, args.epochs)
    seeds = parse_seeds(args.seeds)

    logger.info(
        f"Running Scaled Induction Benchmark: d_model={args.d_model}, layers={args.n_layers}"
    )

    result = run_seeds(lambda s: run_single_seed(s, scaled_args), seeds)

    # Save manifest
    probe_model = AttentionOnlyTransformer(
        vocab_size=scaled_args.vocab_size,
        d_model=scaled_args.d_model,
        n_layers=scaled_args.n_layers,
        n_heads=scaled_args.n_heads,
        max_seq_len=scaled_args.seq_len,
    )

    manifest = ResultsManifest.from_run(
        experiment="exp7_induction_scaling",
        seeds=seeds,
        args=vars(scaled_args),
        per_seed_metrics=result.per_seed,
        aggregate=result.aggregate,
        wall_clock_seconds=result.wall_clock_seconds,
        device=str(DEVICE),
        n_parameters=count_parameters(probe_model),
    )
    manifest_path = Path("results") / "exp7_induction_scaling.json"
    manifest.save(manifest_path)
    logger.info(f"Saved manifest to {manifest_path}")

if __name__ == "__main__":
    main()
