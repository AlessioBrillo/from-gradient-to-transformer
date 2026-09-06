"""Probe guardrail for exp6: --manifest-path keeps shakedowns off the flagship.

Mirrors tests/test_exp2_manifest_path.py. Before the fix, exp6 hardcoded
RESULTS_DIR / cfg["output"]["manifest_name"], so any shakedown overwrote the
committed manifest — the exact P=67 clobber class from exp2.
"""

from pathlib import Path

from src.experiments.exp6_capstone import build_parser, resolve_manifest_path


def test_manifest_path_defaults_to_none_flagship() -> None:
    """Without the flag, the manifest path stays config-driven (flagship)."""
    args = build_parser().parse_args([])
    assert args.manifest_path is None


def test_manifest_path_override_accepted() -> None:
    """A shakedown can redirect its manifest away from the flagship file."""
    args = build_parser().parse_args(
        ["--seeds", "0", "--manifest-path", "results/probe_capstone_shakedown.json"]
    )
    assert args.manifest_path == "results/probe_capstone_shakedown.json"


def test_checkpoint_every_defaults_to_none_config() -> None:
    """--checkpoint-every must not silently override config/--quick values."""
    args = build_parser().parse_args([])
    assert args.checkpoint_every is None


def test_steps_and_warmup_overrides_default_to_none() -> None:
    """Shakedown overrides must be explicit, never silent."""
    args = build_parser().parse_args([])
    assert args.steps is None
    assert args.warmup_steps is None


def test_steps_and_warmup_overrides_accepted() -> None:
    """Frozen shakedown invocation: 2000 steps, 100 warmup, probe manifest."""
    args = build_parser().parse_args(
        [
            "--steps",
            "2000",
            "--warmup-steps",
            "100",
            "--checkpoint-every",
            "500",
            "--manifest-path",
            "results/probe_capstone_shakedown.json",
            "--save-model",
        ]
    )
    assert args.steps == 2000
    assert args.warmup_steps == 100
    assert args.checkpoint_every == 500


def test_resolve_manifest_path_never_touches_flagship() -> None:
    """Probe path resolves to probe; None resolves to flagship manifest."""
    cfg = {"output": {"manifest_name": "exp6_capstone.json"}}
    probe = resolve_manifest_path("results/probe_capstone_shakedown.json", cfg)
    assert probe == Path("results/probe_capstone_shakedown.json")
    flagship = resolve_manifest_path(None, cfg)
    assert flagship.name == "exp6_capstone.json"
