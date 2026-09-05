"""Probe guardrail: --manifest-path keeps probes off the flagship manifest.

On 2026-09-04 a P=67 probe overwrote results/exp2_grokking.json (the P=113
NO-GROK flagship) because --seeds always wrote the same path. Probes must be
routable elsewhere; the flagship path stays the default.
"""

from src.experiments.exp2_grokking import build_parser


def test_manifest_path_defaults_to_flagship() -> None:
    """Without the flag, multi-seed runs keep writing the flagship path."""
    args = build_parser().parse_args(["--seeds", "0"])
    assert args.manifest_path is None


def test_manifest_path_override_accepted() -> None:
    """A probe can redirect its manifest away from the flagship file."""
    args = build_parser().parse_args(
        ["--seeds", "0", "--manifest-path", "results/probe_p67.json"]
    )
    assert args.manifest_path == "results/probe_p67.json"
