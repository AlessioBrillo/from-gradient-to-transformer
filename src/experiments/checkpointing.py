"""Rolling resume checkpoint helpers shared by the long-running experiments.

A single file per seed holds the latest state, so `--resume` points at it and
keeps the newest state without an ever-growing set of artifacts. The saved RNG
state is captured *after* the training loop of `epoch` has finished and
*before* any state of epoch `epoch + 1` has been drawn, which is exactly the
continuity point a seamless resume needs: a resumed run draws the same batches
it would have drawn had it never stopped. Falsified per-experiment by the
checkpoint-resume tests (resume must reproduce an uninterrupted run
bit-for-bit).

Each checkpoint also records the commit that wrote it. The content-task
cascade loads exp1's checkpoint in exp4, potentially in a later session on a
different commit; without this field the cascade can only check the epoch and
the architecture, not that the weights came from the pre-registered
instrument.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Optional

import torch

from src.results import git_provenance

logger = logging.getLogger(__name__)


def checkpoint_path_for_seed(checkpoint_dir: str, prefix: str, seed: int) -> Path:
    """Rolling resume checkpoint path for one seed."""
    return Path(checkpoint_dir) / f"{prefix}_checkpoint_seed{seed}.pt"


def _same_commit(left: str, right: str) -> bool:
    """True when two git SHAs name the same commit, allowing abbreviations.

    Manifests record ``git rev-parse --short HEAD``; a user may pass the full
    SHA from ``git rev-parse HEAD``. A prefix of an unambiguous abbreviation
    still names the same commit, so compare both directions.
    """
    left, right = left.strip(), right.strip()
    return bool(left and right) and (
        left == right or left.startswith(right) or right.startswith(left)
    )


def validate_checkpoint_provenance(
    state: Optional[dict[str, Any]],
    checkpoint_path: Path,
    *,
    expected_seed: Optional[int] = None,
    expected_task: Optional[str] = None,
    expected_git_sha: Optional[str] = None,
    expected_epochs: Optional[int] = None,
    expected_arch: Optional[dict[str, Any]] = None,
    source_label: str = "checkpoint",
) -> dict[str, Any]:
    """Validate a rolling training checkpoint's recorded provenance.

    Checks that every fact recorded in the checkpoint matches the expected
    value provided by the caller. Raises ``SystemExit`` on any mismatch so
    callers (exp4, exp5, exp1 resume) cannot silently analyse or resume
    from the wrong instrument. A dirty tree is logged as a warning (the
    remote-run pinner already refuses dirty manifests); it is not a hard
    refusal here because a local CPU run on a dirty tree is still useful
    for smoke tests.

    Returns the provenance dict: ``path, epoch, seed, task, git_sha,
    git_dirty, arch``.
    """
    if state is None or not isinstance(state, dict) or "model" not in state:
        raise SystemExit(
            f"{source_label} {checkpoint_path} is not a training checkpoint"
        )

    arch = state.get("arch") or {}
    state_seed = state.get("seed")
    state_task = state.get("task")
    state_sha = str(state.get("git_sha") or "unknown")
    state_dirty = bool(state.get("git_dirty", False))
    epoch = int(state.get("epoch", -1)) + 1

    # Architecture: the checkpoint must have been built with the declared shape.
    if expected_arch is not None and arch:
        mismatched = {
            k: (arch.get(k), v) for k, v in expected_arch.items() if arch.get(k) != v
        }
        if mismatched:
            raise SystemExit(
                f"{source_label} {checkpoint_path} was trained with {arch}, "
                f"but --source-* says {expected_arch}. Fix the source flags."
            )

    # Seed: the weights alone cannot say which model they are.
    if expected_seed is not None and state_seed is not None:
        if int(state_seed) != int(expected_seed):
            raise SystemExit(
                f"{source_label} {checkpoint_path} holds model seed "
                f"{state_seed}, but expected {expected_seed}. Would analyse "
                "a different model."
            )

    # Task: not recoverable from weights.
    if expected_task is not None and state_task is not None:
        if state_task != expected_task:
            raise SystemExit(
                f"{source_label} {checkpoint_path} was trained on the "
                f"{state_task!r} task, but expected {expected_task!r}."
            )

    # Commit: the instrument that wrote the weights.
    if expected_git_sha is not None:
        if state_sha == "unknown":
            raise SystemExit(
                f"{source_label} {checkpoint_path} does not record the commit "
                "that wrote it; provenance cannot be verified. Re-run the "
                "source experiment with the current checkpoint code."
            )
        if not _same_commit(state_sha, expected_git_sha):
            raise SystemExit(
                f"{source_label} {checkpoint_path} was written at {state_sha}, "
                f"but expected {expected_git_sha}. Would measure a model "
                "trained by a different instrument."
            )

    # Epoch: a rolling checkpoint can lag the run that wrote it.
    if expected_epochs is not None and epoch != expected_epochs:
        raise SystemExit(
            f"{source_label} {checkpoint_path} is epoch {epoch}, but "
            f"expected {expected_epochs}. The rolling checkpoint is stale: "
            "re-run the source experiment to the end."
        )

    if state_dirty:
        logger.warning(
            f"{source_label} {checkpoint_path} was written with a dirty "
            f"working tree (git_sha {state_sha}); its weights do not "
            "correspond to a committed instrument."
        )

    return {
        "path": str(checkpoint_path),
        "epoch": epoch,
        "seed": state_seed,
        "task": state_task,
        "git_sha": state_sha,
        "git_dirty": state_dirty,
        "arch": arch,
    }


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
    seed: Optional[int] = None,
    task: Optional[str] = None,
) -> None:
    """Atomically write a resume checkpoint: a kill mid-save leaves the *old*
    valid checkpoint, not a truncated one.

    ``seed`` and ``task`` are the facts about *what* was trained that the
    weights alone cannot say. The content-task cascade (exp4) checks them: a
    directory of per-seed checkpoints can be pointed at with the wrong
    ``--seeds``, and a checkpoint of the periodic task has the same shapes as
    one of the variable task.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    git_sha, git_dirty = git_provenance()
    payload: dict[str, Any] = {
        "epoch": epoch,
        "model": model.state_dict(),
        "optimizer": optimizer.state_dict(),
        "scheduler": scheduler.state_dict(),
        "rng_state": rng_state,
        "history": history,
        "git_sha": git_sha,
        "git_dirty": git_dirty,
    }
    if seed is not None:
        payload["seed"] = int(seed)
    if task is not None:
        payload["task"] = task
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
