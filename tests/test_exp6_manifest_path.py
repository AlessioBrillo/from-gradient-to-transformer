"""Probe guardrail for exp6: --manifest-path keeps shakedowns off the flagship.

Mirrors tests/test_exp2_manifest_path.py. Before the fix, exp6 hardcoded
RESULTS_DIR / cfg["output"]["manifest_name"], so any shakedown overwrote the
committed manifest — the exact P=67 clobber class from exp2.
"""

from src.experiments.exp6_capstone import build_parser


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
