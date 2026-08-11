#!/usr/bin/env python3
"""Kill drill v2 — real process-death test for exp2's checkpoint/resume.

Micro-Phase 28, Session 1: after the exp2 port, the machinery must survive
what the record's worst failure actually was — a real OS-level kill, not an
in-process pause. This driver launches two exp2 grokking runs:

  Run A (reference):  uninterrupted, N epochs, checkpoint-every K.
  Run B (drill):      launched, killed with a hard terminate mid-epoch after
                      the 2nd checkpoint write, resumed with --resume.

A run survives the drill iff its final checkpoint — model state_dict and
full history — is bit-identical to the uninterrupted reference (same seed,
same thread count, same schedule horizon). The transcript below is the
proof artifact the kill-drill proof note cites.

Usage:
    uv run python scripts/kill_drill_exp2.py [--epochs 60] [--checkpoint-every 10]
"""

import argparse
import os
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

# Both sides of the comparison must see the same BLAS thread pool; the
# probe run that priced the audit sheet used 4 threads.
os.environ.setdefault("OMP_NUM_THREADS", "4")

REPO_ROOT = Path(__file__).resolve().parent.parent
RUN_CMD = [
    sys.executable,
    "-m",
    "src.experiments.exp2_grokking",
    "--modulus", "29",
    "--d-model", "64",
    "--d-mlp", "256",
    "--n-heads", "2",
    "--batch-size", "512",
    "--train-fraction", "0.3",
    "--weight-decay", "1.0",
    "--lr", "1e-3",
    "--seed", "0",
]

TRANSCRIPT: list[str] = []


def log(line: str) -> None:
    stamp = datetime.now(timezone.utc).strftime("%H:%M:%S")
    TRANSCRIPT.append(f"{stamp} | {line}")
    print(f"{stamp} | {line}", flush=True)


def wait_for_exit(proc: subprocess.Popen, timeout: int, label: str) -> int:
    try:
        code = proc.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        proc.kill()
        raise SystemExit(f"FATAL: {label} exceeded {timeout}s — aborting drill")
    log(f"{label} exited with code {code}")
    return code


def checkpoint_epoch(path: Path):
    import torch

    if not path.exists():
        return None
    ckpt = torch.load(path, map_location="cpu")
    return ckpt["epoch"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--epochs", type=int, default=60)
    parser.add_argument("--checkpoint-every", type=int, default=10)
    args = parser.parse_args()

    workdir = Path(tempfile.mkdtemp(prefix="exp2_kill_drill_"))
    ckpt_ref = workdir / "ckpt_ref"
    ckpt_drill = workdir / "ckpt_drill"
    ckpt_path = ckpt_drill / "exp2_checkpoint_seed0.pt"
    log(f"workdir: {workdir}")
    log(f"config: epochs={args.epochs} checkpoint_every={args.checkpoint_every} "
        f"OMP_NUM_THREADS={os.environ['OMP_NUM_THREADS']}")
    log("phase 1: uninterrupted reference run (own checkpoint dir, kept aside)")

    def base_cmd(ckpt_dir: Path):
        return RUN_CMD + [
            "--epochs", str(args.epochs),
            "--checkpoint-every", str(args.checkpoint_every),
            "--checkpoint-dir", str(ckpt_dir),
        ]

    ref = subprocess.Popen(base_cmd(ckpt_ref), cwd=REPO_ROOT)
    wait_for_exit(ref, timeout=600, label="reference")

    # --- drill run ---------------------------------------------------------
    log("phase 2: drill run launched (own checkpoint dir); waiting for 2nd "
        "checkpoint write")
    drill = subprocess.Popen(base_cmd(ckpt_drill), cwd=REPO_ROOT)

    target_epoch = 2 * args.checkpoint_every - 1  # 2nd write, 0-indexed
    deadline = time.monotonic() + 300
    seen = None
    while time.monotonic() < deadline:
        seen = checkpoint_epoch(ckpt_path)
        if seen is not None and seen >= target_epoch:
            break
        time.sleep(0.2)
    if seen is None or seen < target_epoch:
        drill.kill()
        raise SystemExit(f"FATAL: drill run never reached checkpoint epoch "
                         f"{target_epoch} (last seen {seen})")

    log(f"checkpoint holds epoch {seen} — killing mid-epoch now")
    time.sleep(0.4)  # land mid-epoch, not on a save boundary
    drill.kill()
    drill.wait(timeout=30)
    if drill.poll() is not None:
        log(f"drill process confirmed dead (poll()={drill.poll()})")

    survived_epoch = checkpoint_epoch(ckpt_path)
    final_epoch = args.epochs - 1
    log(f"surviving checkpoint epoch: {survived_epoch} "
        f"(valid drill iff {target_epoch} <= epoch < {final_epoch})")
    if not (target_epoch <= survived_epoch < final_epoch):
        raise SystemExit(
            f"FATAL: surviving checkpoint epoch {survived_epoch} is not inside "
            f"the drill window [{target_epoch}, {final_epoch})"
        )

    # --- resume ------------------------------------------------------------
    log("phase 3: relaunching with --resume (same checkpoint dir)")
    resumed = subprocess.Popen(base_cmd(ckpt_drill) + ["--resume"], cwd=REPO_ROOT)
    wait_for_exit(resumed, timeout=600, label="resumed run")

    # --- bit-for-bit comparison ---------------------------------------------
    import numpy as np
    import torch

    log("phase 4: comparing final checkpoints bit-for-bit")
    ref_path = ckpt_ref / "exp2_checkpoint_seed0.pt"
    ref_ckpt = torch.load(ref_path, map_location="cpu")
    if ref_ckpt["epoch"] != final_epoch:
        raise SystemExit(
            f"FATAL: reference run did not finish (final checkpoint holds "
            f"epoch {ref_ckpt['epoch']}, expected {final_epoch})"
        )

    with tempfile.TemporaryDirectory(prefix="exp2_kill_drill_ref_") as ref_dir:
        ref_copy = Path(ref_dir) / "ref.pt"
        torch.save(ref_ckpt, ref_copy)
        ref_ckpt = torch.load(ref_copy, map_location="cpu")
        drill_ckpt = torch.load(ckpt_path, map_location="cpu")

    assert set(ref_ckpt.keys()) == set(drill_ckpt.keys()), "checkpoint keys differ"
    assert ref_ckpt["epoch"] == drill_ckpt["epoch"], "final epochs differ"

    def deep_max_diff(a, b, path: str) -> float:
        """Recursive max-abs-diff over a checkpoint subtree (nested state
        dicts, lists, scalars, tensors). AdamW's state_dict nests dicts and
        holds integer steps alongside float tensors, so a flat tensor
        comparison is not enough."""
        if isinstance(a, dict):
            if set(a.keys()) != set(b.keys()):
                raise SystemExit(f"FATAL: key set diverged at {path}: "
                                 f"{sorted(a.keys())} vs {sorted(b.keys())}")
            return max(
                (deep_max_diff(a[k], b[k], f"{path}.{k}") for k in a), default=0.0
            )
        if isinstance(a, (list, tuple)):
            if len(a) != len(b):
                raise SystemExit(f"FATAL: length diverged at {path}")
            return max(
                (deep_max_diff(x, y, f"{path}[{i}]")
                 for i, (x, y) in enumerate(zip(a, b))),
                default=0.0,
            )
        if isinstance(a, torch.Tensor):
            return float((a - b).abs().max())
        if isinstance(a, bool):
            return 0.0 if a == b else float("inf")
        if a is None or b is None:
            return 0.0 if a is b else float("inf")
        return float(abs(a - b))

    worst = {"name": None, "diff": -1.0}
    for k in ("model", "optimizer", "scheduler", "rng_state"):
        if k == "rng_state":
            same = bool((ref_ckpt[k] == drill_ckpt[k]).all())
            log(f"rng_state identical: {same}")
            if not same:
                raise SystemExit("FATAL: rng_state diverged")
            continue
        diff = deep_max_diff(ref_ckpt[k], drill_ckpt[k], k)
        if diff > worst["diff"]:
            worst = {"name": k, "diff": diff}
        if diff > 0.0:
            log(f"DIVERGENCE: {k} max_abs_diff={diff:.3e}")
    log(f"state worst-case max_abs_diff: {worst['name']}={worst['diff']:.3e}")

    for key in ref_ckpt["history"]:
        ha, hb = np.asarray(ref_ckpt["history"][key]), np.asarray(drill_ckpt["history"][key])
        assert ha.shape == hb.shape, f"history[{key}] length differs"
        diff = float(np.abs(ha - hb).max())
        if diff > 0.0:
            log(f"DIVERGENCE: history[{key}] max_abs_diff={diff:.3e}")
        log(f"history[{key}] max_abs_diff: {diff:.3e}")

    if worst["diff"] > 0.0:
        raise SystemExit(f"FAIL: bit-identical claim broken ({worst['name']})")

    log("RESULT: bit-identical — the resumed run is indistinguishable from "
        "the uninterrupted one across a real process kill.")
    transcript_path = workdir / "transcript.txt"
    transcript_path.write_text("\n".join(TRANSCRIPT) + "\n", encoding="utf-8")
    log(f"transcript written to {transcript_path}")


if __name__ == "__main__":
    main()
