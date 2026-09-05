"""Regression tests for the capstone runner's save/resume checkpoint contract.

train_single_seed() writes rolling step checkpoints when `checkpoint_dir` is
set and reads them back via `resume_step`. The save side once called the
shared epoch-oriented helper with keyword arguments it does not accept
(`step=`, `seed=`, `config=`), so any `--save-model` run reaching its first
checkpoint step crashed with TypeError — while the resume side reads raw
torch.save dicts with keys model/optimizer/scheduler/step. These tests pin
the symmetric contract: what the saver writes, the resumer must read.
"""

from pathlib import Path

import torch

from src.experiments.exp6_capstone import train_single_seed


def _tiny_cfg(steps: int, checkpoint_every: int) -> dict:
    """Minimal CPU-seconds config exercising the checkpoint branch."""
    return {
        "task": {
            "modular": {"modulus": 7, "train_fraction": 0.5},
            "induction": {
                "vocab_size": 32,
                "seq_len": 8,
                "num_train": 64,
                "num_val": 16,
                "prefix_ratio": 0.5,
            },
        },
        "model": {
            "d_model": 16,
            "n_layers": 1,
            "n_heads": 2,
            "d_mlp": 32,
            "dropout": 0.0,
            "rotary_base": 10000,
            "rmsnorm_eps": 1e-5,
        },
        "training": {
            "steps": steps,
            "batch_size": 8,
            "lr": 1e-3,
            "weight_decay": 0.0,
            "warmup_steps": 1,
            "gradient_clip": 1.0,
        },
        "instrumentation": {
            "fourier_every": 10**9,
            "kcomp_every": 10**9,
        },
        "checkpoint_every": checkpoint_every,
    }


def test_checkpoint_written_and_readable(tmp_path: Path) -> None:
    """Checkpoints land on disk with the keys the resume path reads."""
    cfg = _tiny_cfg(steps=6, checkpoint_every=2)
    train_single_seed(cfg, seed=0, checkpoint_dir=tmp_path)

    for step in (2, 4, 6):
        ckpt_path = tmp_path / f"exp6_capstone_seed0_step{step}.pt"
        assert ckpt_path.exists(), f"missing checkpoint for step {step}"
        ckpt = torch.load(ckpt_path, map_location="cpu")
        assert ckpt["step"] == step
        for key in ("model", "optimizer", "scheduler"):
            assert key in ckpt, f"checkpoint step {step} missing '{key}'"


def test_resume_continues_from_checkpoint(tmp_path: Path) -> None:
    """A resumed run picks up at the saved step and finishes the horizon."""
    cfg = _tiny_cfg(steps=4, checkpoint_every=2)
    train_single_seed(cfg, seed=0, checkpoint_dir=tmp_path)

    cfg["training"]["steps"] = 6
    metrics = train_single_seed(
        cfg, seed=0, resume_step=4, checkpoint_dir=tmp_path
    )

    assert metrics["total_steps"] == 6
    resumed = torch.load(
        tmp_path / "exp6_capstone_seed0_step6.pt", map_location="cpu"
    )
    assert resumed["step"] == 6
