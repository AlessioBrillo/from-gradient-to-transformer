#!/usr/bin/env python3
"""Re-analyse the capstone joint-training checkpoints with the post-audit
energy metric.

The 3×20k-step capstone run (issue #170, executed 2026-10-14 on Kaggle)
wrote its final checkpoints to disk
(`results/remote/capstone-20k/output3/repo/checkpoints/exp6_capstone_seed{0,1,2}_step20000.pt`),
but `results/capstone_20k.json` carries only the L1 k_99 reading — the metric
the 2026-10-08 audit falsified. Its Fourier regime (sparse vs dense) is
therefore "not established" in the paper.

This script is the analysis side: it rebuilds the model from configs/capstone.yaml,
loads each final checkpoint, slices the modular-addition embedding and
recomputes exp2's fourier_energy_sparsity. No retraining — every number is
re-derivable from this command and the checkpoints on disk.

Output: a new manifest `results/capstone_20k_energy.json` (the original
`capstone_20k.json` is left immutable — manifests are the record).

Usage:
    python scripts/capstone_energy_from_checkpoints.py \
        --checkpoint-glob "results/remote/capstone-20k/output3/repo/checkpoints/"
        "exp6_capstone_seed*_step20000.pt" \
        --config configs/capstone.yaml \
        --output results/capstone_20k_energy.json
"""

from __future__ import annotations

import glob
import re
import time
from pathlib import Path
from typing import Any

import torch
import yaml

from src.experiments.exp2_grokking import fourier_energy_sparsity
from src.models.decoder_only_transformer import DecoderOnlyTransformer
from src.results import ResultsManifest, count_parameters, git_provenance


def _seed_from_path(path: Path) -> int:
    m = re.search(r"seed(\d+)", path.name)
    return int(m.group(1)) if m else -1


def _energy_from_checkpoint(path: Path, cfg: dict[str, Any]) -> dict[str, float]:
    """Rebuild the model, load the checkpoint, slice the modular embedding,
    return the energy metric + modular accuracy proxy."""
    mod_cfg = cfg["task"]["modular"]
    model_cfg = cfg["model"]
    vocab_size = (
        cfg["task"]["induction"]["vocab_size"]
        + mod_cfg["modulus"]
        + 10  # pad + reserved (same as exp6_capstone.train_single_seed)
    )
    model = DecoderOnlyTransformer(
        vocab_size=vocab_size,
        d_model=model_cfg["d_model"],
        n_layers=model_cfg["n_layers"],
        n_heads=model_cfg["n_heads"],
        d_mlp=model_cfg["d_mlp"],
        dropout=model_cfg["dropout"],
        rotary_base=model_cfg["rotary_base"],
        rmsnorm_eps=model_cfg["rmsnorm_eps"],
    )
    ckpt = torch.load(path, map_location="cpu")
    model.load_state_dict(ckpt["model"], strict=True)

    offset = int(mod_cfg.get("vocab_offset", 0))
    p = int(mod_cfg["modulus"])
    mod_embeddings = model.embed.weight[offset : offset + p].detach().cpu()
    energy = fourier_energy_sparsity(mod_embeddings, p)

    return {
        "k_energy_90": float(energy["k_energy_90"]),
        "k_energy_99": float(energy["k_energy_99"]),
        "frac_energy_top5": float(energy["frac_energy_top5"]),
        "energy_sparse": float(energy["is_sparse"]),
        "n_freq": float(energy["n_freq"]),
    }, count_parameters(model)


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Capstone energy re-analysis from checkpoints")
    parser.add_argument(
        "--checkpoint-glob",
        default="results/remote/capstone-20k/output3/repo/checkpoints/"
        "exp6_capstone_seed*_step20000.pt",
        help="Glob for the final capstone checkpoints (one per seed).",
    )
    parser.add_argument(
        "--config", default="configs/capstone.yaml", help="Capstone config YAML."
    )
    parser.add_argument(
        "--output", default="results/capstone_20k_energy.json", help="Manifest path."
    )
    args = parser.parse_args()

    with open(args.config) as f:
        cfg = yaml.safe_load(f)

    paths = sorted((Path(p) for p in glob.glob(args.checkpoint_glob)), key=_seed_from_path)
    if not paths:
        raise SystemExit(f"no checkpoints matched: {args.checkpoint_glob}")

    per_seed = []
    seeds = []
    n_parameters = None
    t0 = time.monotonic()
    for path in paths:
        seed = _seed_from_path(path)
        seeds.append(seed)
        m, n_parameters = _energy_from_checkpoint(path, cfg)
        per_seed.append(m)
        print(f"seed {seed}: k_energy_90={m['k_energy_90']} is_sparse={m['energy_sparse']}")

    n = len(per_seed)
    import math

    def stats(key: str) -> dict[str, float]:
        vals = [m[key] for m in per_seed]
        mean = sum(vals) / n
        var = sum((v - mean) ** 2 for v in vals) / n
        return {
            "mean": mean,
            "std": math.sqrt(var),
            "min": min(vals),
            "max": max(vals),
            "n": float(n),
        }

    aggregate = {key: stats(key) for key in per_seed[0]}
    sha, dirty = git_provenance()
    manifest = ResultsManifest.from_run(
        experiment="capstone_20k_energy",
        seeds=seeds,
        args={
            "config": args.config,
            "checkpoint_glob": args.checkpoint_glob,
            "reanalysis_of": "results/capstone_20k.json",
            "modulus": cfg["task"]["modular"]["modulus"],
            "steps": cfg["training"]["steps"],
        },
        per_seed_metrics=per_seed,
        aggregate=aggregate,
        wall_clock_seconds=time.monotonic() - t0,
        device="cpu",
        n_parameters=n_parameters,
        notes=(
            "Re-analysis of the 3x20k-step capstone checkpoints with the "
            "post-audit energy metric; NO retraining. Original run: "
            "results/capstone_20k.json (checkpoints on disk under "
            "results/remote/capstone-20k/). git tree dirty=" + str(dirty) +
            " (analysis committed separately from the run)."
        ),
    )
    manifest.save(Path(args.output))
    print(f"Saved manifest: {args.output}")
    for key in sorted(aggregate):
        agg = aggregate[key]
        print(f"  {key}: {agg['mean']:.4f} ± {agg['std']:.4f} (n={int(agg['n'])})")


if __name__ == "__main__":
    main()
