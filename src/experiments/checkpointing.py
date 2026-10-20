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


def architecture_metadata(model: torch.nn.Module) -> dict[str, Any]:
    """The architecture facts a checkpoint needs to be re-loaded correctly.

    A bare state-dict does not say which architecture produced it, so a
    consumer that rebuilds the model has to be told the shape by hand — and
    a mistake there loads a *different* model (or crashes). Recording the
    metadata in the checkpoint turns that into a checkable fact: the
    consumer compares it against what it was told and refuses to continue
    on a mismatch.

    Works for both model families in this repository: the attention-only
    transformer (Rung 1) and the shared decoder-only transformer.
    """
    blocks = getattr(model, "blocks", [])
    attn = getattr(blocks[0], "attn", blocks[0]) if blocks else None
    embed = getattr(model, "embed", None)
    meta: dict[str, Any] = {
        "class": type(model).__name__,
        "n_layers": len(blocks),
    }
    if embed is not None:
        meta["vocab_size"] = int(getattr(embed, "num_embeddings"))
        meta["d_model"] = int(getattr(embed, "embedding_dim"))
    if attn is not None:
        meta["n_heads"] = int(getattr(attn, "n_heads", 0))
    pos_embed = getattr(model, "pos_embed", None)
    if pos_embed is not None:
        meta["max_seq_len"] = int(getattr(pos_embed, "num_embeddings"))
    elif hasattr(model, "max_seq_len"):
        meta["max_seq_len"] = int(getattr(model, "max_seq_len"))
    return meta


def save_training_checkpoint(
    path: Path,
    epoch: int,
    model: torch.nn.Module,
    optimizer: torch.optim.Optimizer,
    scheduler: torch.optim.lr_scheduler.LRScheduler,
    history: dict[str, Any],
    rng_state: Any,
    arch: Optional[dict[str, Any]] = None,
) -> None:
    """Atomically write a resume checkpoint: a kill mid-save leaves the *old*
    valid checkpoint, not a truncated one."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    payload: dict[str, Any] = {
        "epoch": epoch,
        "model": model.state_dict(),
        "optimizer": optimizer.state_dict(),
        "scheduler": scheduler.state_dict(),
        "rng_state": rng_state,
        "history": history,
    }
    if arch is not None:
        payload["arch"] = arch
    torch.save(payload, tmp)
    tmp.replace(path)


def load_training_checkpoint(
    path: Path, map_location: Any | None = None
) -> Optional[dict[str, Any]]:
    """Load a checkpoint written by save_training_checkpoint. Returns None
    if the file does not exist, so `--resume` on a machine with nothing to
    resume degrades to a fresh, logged start rather than a crash."""
    if not path.exists():
        return None
    state: Optional[dict[str, Any]] = torch.load(path, map_location=map_location)
    return state
