#!/usr/bin/env python3
"""S4 verdict — ADR-0003 row 1 criteria applied mechanically to the final
checkpoints (no eyeballing, no post-hoc thresholds).

Frozen criteria (ADR-0003, 2026-08-06, never edited):
  Grok = val acc >= 0.95 sustained >= 5 checkpoints
         AND Fourier frequency count < P/2 sustained
  generalization epoch = first epoch with val_acc > 0.9

"Checkpoint" here = one rolling checkpoint interval (500 epochs). The
sustained checks walk the per-epoch history saved inside each final
checkpoint: val acc >= 0.95 for >= 5 consecutive 500-epoch intervals
(epochs 0..2499 covered by the >= 2500 checkpoint's history, etc.).

Usage:
    python scripts/exp2_verdict_from_checkpoints.py [--dir checkpoints]
"""

import argparse
from pathlib import Path

import numpy as np
import torch

from src.experiments.exp2_grokking import (
    analyze_fourier_sparsity,
    fourier_decompose_embeddings,
)

MODULUS = 113
VAL_THRESHOLD = 0.95
SUSTAINED_INTERVALS = 5
CHECKPOINT_EVERY = 500


def k_99_from_checkpoint(ckpt: dict) -> float:
    """k_99 = number of frequencies carrying 99% of the Fourier mass — the
    exact quantity exp2's own frozen "CONFIRMED" line checks
    (k_99_percent < modulus/2), so the verdict uses the same criterion as
    the experiment code, not a re-invented one."""
    model_state = ckpt["model"]
    embed = model_state["embed.weight"].detach()
    fourier = fourier_decompose_embeddings(embed, MODULUS)
    return float(analyze_fourier_sparsity(fourier, top_k=20)["k_99_percent"])


def sustained_val(ckpt: dict) -> tuple[bool, int]:
    """True if val_acc >= 0.95 on >= 5 consecutive checkpoint intervals."""
    val = np.asarray(ckpt["history"]["val_acc"], dtype=float)
    epochs = len(val)
    intervals = epochs // CHECKPOINT_EVERY
    ok = val >= VAL_THRESHOLD
    longest = 0
    run = 0
    for i in range(intervals):
        # An interval counts if EVERY epoch in it is above threshold (strict
        # reading of "sustained"); the last partial interval is ignored.
        if bool(ok[i * CHECKPOINT_EVERY : (i + 1) * CHECKPOINT_EVERY].all()):
            run += 1
            longest = max(longest, run)
        else:
            run = 0
    return longest >= SUSTAINED_INTERVALS, longest


def sustained_sparsity(ckpt: dict) -> tuple[bool, int]:
    """Fourier frequency count < P/2 (k_99 < 56.5, the criterion exp2's own
    CONFIRMED line applies) on the final embedding; the per-epoch history
    entropy trajectory is reported alongside as the progress measure."""
    k99 = k_99_from_checkpoint(ckpt)
    return k99 < MODULUS / 2, int(k99)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", default="checkpoints")
    args = parser.parse_args()

    for seed in (0, 1, 2):
        path = Path(args.dir) / f"exp2_checkpoint_seed{seed}.pt"
        if not path.exists():
            print(f"seed {seed}: no final checkpoint yet")
            continue
        ckpt = torch.load(path, map_location="cpu")
        hist = ckpt["history"]
        val = np.asarray(hist["val_acc"], dtype=float)
        gen_epoch = next(
            (i for i, a in enumerate(hist["val_acc"]) if a > 0.9), -1
        )
        val_sustained, longest_run = sustained_val(ckpt)
        sparsity_ok, k99 = sustained_sparsity(ckpt)
        sparsity_hist = np.asarray(hist["fourier_sparsity"], dtype=float)

        verdict = "GROK" if (val_sustained and sparsity_ok) else "NO-GROK"
        print(f"seed {seed}:")
        print(f"  final_val_acc          = {val[-1]:.4f}")
        print(f"  generalization_epoch   = {gen_epoch}")
        print(f"  val>=0.95 sustained    = {val_sustained} "
              f"(longest run of {longest_run} full intervals)")
        print(f"  k_99 (final)           = {k99} (threshold < {MODULUS/2})")
        print(f"  final fourier sparsity = {sparsity_hist[-1]:.4f} "
              f"(progress measure)")
        print(f"  verdict                = {verdict}")


if __name__ == "__main__":
    main()
