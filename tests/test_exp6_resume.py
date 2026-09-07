"""Resume-guardrail tests for exp6: --resume must never fail silently.

MP-87 Session 1 wart (dated 2026-09-06): a resume attempt without
`--save-model` set `checkpoint_dir=None`, so the
`if resume_step > 0 and checkpoint_dir:` branch skipped without a word and
the run trained from scratch while the operator waited. Exp1/exp2 log a
WARNING when the checkpoint cannot be found ("RESUME: ... starting fresh");
exp6 said nothing in either silent case:

1. `resume_step > 0` with `checkpoint_dir=None` (no --save-model).
2. `resume_step > 0` with a checkpoint dir whose file does not exist.

Contract pinned here: both cases log a WARNING containing "RESUME" and
"starting fresh", then train from step 0 — loud fallback, never silence.
"""

import logging
from pathlib import Path

from src.experiments.exp6_capstone import train_single_seed


def _tiny_cfg(steps: int = 4) -> dict:
    """Minimal CPU-seconds config; instrumentation never fires."""
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
        # The loop evaluates `step % cfg["checkpoint_every"]`
        # unconditionally, so 0 would divide by zero (mirrors the
        # established tests/test_exp6_capstone.py pattern).
        "checkpoint_every": 2,
    }


def test_resume_without_checkpoint_dir_warns_and_starts_fresh(
    caplog: object,
) -> None:
    """--resume without --save-model must warn, not silently restart."""
    cfg = _tiny_cfg()
    with caplog.at_level(logging.WARNING):  # type: ignore[attr-defined]
        metrics = train_single_seed(cfg, seed=0, resume_step=500)

    warnings = [
        r.message
        for r in caplog.records  # type: ignore[attr-defined]
        if r.levelno >= logging.WARNING
    ]
    assert any(
        "RESUME" in w and "starting fresh" in w for w in warnings
    ), f"no RESUME warning logged, got: {warnings}"
    assert isinstance(metrics, dict)


def test_resume_missing_checkpoint_file_warns_and_starts_fresh(
    tmp_path: Path, caplog: object
) -> None:
    """--resume pointing at an absent file must warn, not silently restart."""
    cfg = _tiny_cfg()
    with caplog.at_level(logging.WARNING):  # type: ignore[attr-defined]
        metrics = train_single_seed(
            cfg, seed=0, resume_step=500, checkpoint_dir=tmp_path
        )

    warnings = [
        r.message
        for r in caplog.records  # type: ignore[attr-defined]
        if r.levelno >= logging.WARNING
    ]
    assert any(
        "RESUME" in w and "starting fresh" in w for w in warnings
    ), f"no RESUME warning logged, got: {warnings}"
    assert isinstance(metrics, dict)
