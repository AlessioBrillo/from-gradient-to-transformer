"""Rolling resume checkpoint helpers shared by the long-running experiments.

A single file per seed holds the latest state, so `--resume` points at it and
keeps the newest state without an ever-growing set of artifacts. The saved RNG
state is captured *after* the training loop of `epoch` has finished and
*before* any state of epoch `epoch + 1` has been drawn, which is exactly the
continuity point a seamless resume needs: a resumed run draws the same batches
it would have drawn had it never stopped. Falsified per-experiment by the
checkpoint-resume tests (resume must reproduce an uninterrupted run
bit-for-bit).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Optional

import torch


def checkpoint_path_for_seed(checkpoint_dir: str, prefix: str, seed: int) -> Path:
    """Rolling resume checkpoint path for one seed."""
    return Path(checkpoint_dir) / f"{prefix}_checkpoint_seed{seed}.pt"


def save_training_checkpoint(
    path: Path,
    epoch: int,
    model: torch.nn.Module,
    optimizer: torch.optim.Optimizer,
    scheduler: torch.optim.lr_scheduler.LRScheduler,
    history: dict,
    rng_state: Any,
) -> None:
    """Atomically write a resume checkpoint: a kill mid-save leaves the *old*
    valid checkpoint, not a truncated one."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    torch.save(
        {
            "epoch": epoch,
            "model": model.state_dict(),
            "optimizer": optimizer.state_dict(),
            "scheduler": scheduler.state_dict(),
            "rng_state": rng_state,
            "history": history,
        },
        tmp,
    )
    tmp.replace(path)


def load_training_checkpoint(path: Path, map_location: Any | None = None) -> Optional[dict]:
    """Load a checkpoint written by save_training_checkpoint. Returns None
    if the file does not exist, so `--resume` on a machine with nothing to
    resume degrades to a fresh, logged start rather than a crash."""
    if not path.exists():
        return None
    return torch.load(path, map_location=map_location)
