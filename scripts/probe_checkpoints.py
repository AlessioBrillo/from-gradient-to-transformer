#!/usr/bin/env python3
"""Read epoch/val_acc from the rolling exp2 checkpoints (MP-28 S2 monitoring).

Usage: python scripts/probe_checkpoints.py [--dir checkpoints]
"""

import argparse
import time
from pathlib import Path

import torch


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", default="checkpoints")
    args = parser.parse_args()

    for seed in (0, 1, 2):
        path = Path(args.dir) / f"exp2_checkpoint_seed{seed}.pt"
        if not path.exists():
            print(f"seed {seed}: no checkpoint yet")
            continue
        ckpt = torch.load(path, map_location="cpu")
        hist = ckpt["history"]
        epoch = ckpt["epoch"] + 1
        val = hist["val_acc"][-1]
        mtime = time.strftime("%H:%M:%S", time.localtime(path.stat().st_mtime))
        print(
            f"seed {seed}: epoch={epoch}/5000 val_acc={val:.4f} "
            f"mtime={mtime}"
        )


if __name__ == "__main__":
    main()
