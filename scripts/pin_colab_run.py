#!/usr/bin/env python3
"""Pin a Colab/GPU-run experiment into the results manifest system.

Experiments that run inside the Colab notebook
(notebooks/colab_grokking_full_run.ipynb) never hit the local runner, so
`ResultsManifest.from_run` inside the experiment's own `--seeds` branch
never fires for them. Without this tool, `results/exp2_grokking.json`
would have to be hand-written — untraceable JSON with a hand-typed git
SHA is not a manifest.

Usage:
    python scripts/pin_colab_run.py \
        --metrics-json results/colab_exp2_per_seed.json \
        --args-json results/colab_exp2_args.json \
        --seeds 0,1,2 \
        --experiment exp2_grokking \
        --notes "3-seed P=113 grokking run, Colab T4 GPU, see notebook"

Input formats (both produced by the notebook's post-processing cell):

--metrics-json: a JSON list of per-seed metric dicts, one per seed, in
    seed order:
        [{"final_val_acc": 0.97, "generalization_epoch": 2100.0, ...}, ...]
    Every seed must report the same metric keys — the same rule the local
    runner enforces (`src.experiments.runner.run_seeds`).

--args-json: the argparse namespace the run actually used, as a flat
    JSON object (e.g. {"modulus": 113, "epochs": 5000, "weight_decay": 1.0}).

The tool aggregates per-seed metrics into mean/std/min/max/n exactly as
`run_seeds` does, stamps provenance (`git_sha`/`git_dirty` of this
checkout — so run it at the commit the notebook pinned), and writes a
standard `ResultsManifest` to results/<experiment>.json. Then
`make verify-claims` treats the Colab run exactly like a local one.

`--git-sha` overrides the recorded SHA only if it differs from this
checkout's HEAD, in which case the tool refuses unless --allow-sha-mismatch
is given — a mismatched pin is exactly the drift this system exists to
prevent.
"""

import argparse
import json
import sys
from pathlib import Path

from src.experiments.runner import aggregate_metrics, parse_seeds
from src.results import ResultsManifest, git_provenance


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--metrics-json", type=Path, required=True)
    parser.add_argument("--args-json", type=Path, required=True)
    parser.add_argument("--seeds", type=str, required=True)
    parser.add_argument("--experiment", type=str, default="exp2_grokking")
    parser.add_argument("--out", type=Path, default=None)
    parser.add_argument("--device", type=str, default="cuda")
    parser.add_argument("--n-parameters", type=int, default=None)
    parser.add_argument("--git-sha", type=str, default=None)
    parser.add_argument("--allow-sha-mismatch", action="store_true")
    parser.add_argument("--notes", type=str, default=None)
    args = parser.parse_args()

    per_seed = json.loads(args.metrics_json.read_text())
    if not isinstance(per_seed, list) or not per_seed:
        sys.exit("--metrics-json must be a non-empty JSON list of per-seed metric dicts")
    if len(per_seed) != len(parse_seeds(args.seeds)):
        sys.exit(
            f"--seeds has {len(parse_seeds(args.seeds))} seeds but --metrics-json "
            f"has {len(per_seed)} per-seed records"
        )
    run_args = json.loads(args.args_json.read_text())
    if not isinstance(run_args, dict):
        sys.exit("--args-json must be a JSON object")

    sha, dirty = git_provenance()
    if args.git_sha and args.git_sha != sha:
        if not args.allow_sha_mismatch:
            sys.exit(
                f"--git-sha {args.git_sha} differs from this checkout's HEAD "
                f"({sha}). Run this tool at the commit the notebook pinned, or "
                "pass --allow-sha-mismatch only if you are deliberately "
                "recording provenance against an older commit."
            )
        sha = args.git_sha

    aggregate = aggregate_metrics(per_seed)
    manifest = ResultsManifest.from_run(
        experiment=args.experiment,
        seeds=parse_seeds(args.seeds),
        args=run_args,
        per_seed_metrics=per_seed,
        aggregate=aggregate,
        wall_clock_seconds=0.0,
        device=args.device,
        n_parameters=args.n_parameters,
        notes=args.notes,
    )
    # The Colab run cannot truthfully claim a wall-clock measured by the
    # local runner; keep the stamp honest instead of a fabricated number.
    manifest.wall_clock_seconds = 0.0
    manifest.git_sha = sha
    # git_dirty: this checkout is where the pin happened, not where the run
    # happened; re-probe the current tree so the manifest doesn't lie about
    # the state of the code it was pinned against.
    manifest.git_dirty = dirty

    out = args.out or (Path("results") / f"{args.experiment}.json")
    manifest.save(out)
    print(f"Pinned Colab run -> {out}")
    for key in aggregate:
        agg = aggregate[key]
        print(f"  {key}: {agg['mean']:.4f} ± {agg['std']:.4f} (n={int(agg['n'])})")
    print("Next: make verify-claims")


if __name__ == "__main__":
    main()
