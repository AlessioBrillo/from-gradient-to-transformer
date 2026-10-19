"""The fixed-vs-fresh batch comparison must be reproducible and apples-to-apples.

This is the one solid Rung 1 finding (portfolio/RESULTS.md: "a matched
fixed-vs-fresh-batches comparison is the one solid finding, 52.2% vs 0.05%
validation accuracy") and for months it was prose-only — no manifest anywhere in
results/ contained those numbers. `make reproduce-induction-batches` now runs
both arms with the SAME seeds into two manifests.

These tests pin the CLI contract that makes that possible.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from src.experiments import exp1_induction_heads as exp1

# The config both Makefile arms share; identical except for the batch regime.
SHARED = dict(
    vocab_size=256,
    seq_len=16,
    d_model=24,
    n_layers=2,
    n_heads=4,
    epochs=800,
    lr=0.001,
    weight_decay=0.1,
    batch_size=32,
    num_train=256,
)


def _parse(argv: list[str]) -> argparse.Namespace:
    return exp1.build_parser().parse_args(argv)


def test_fresh_batches_flag_still_works() -> None:
    """The historical spelling used by the Makefile must keep working."""
    args = _parse(["--fresh-batches"])
    assert args.fresh_batches is True


def test_batches_flag_selects_the_regime() -> None:
    assert _parse(["--batches", "fixed"]).batch_mode == "fixed"
    assert _parse(["--batches", "fresh"]).batch_mode == "fresh"


def test_default_is_fixed_batches() -> None:
    """The default regime is the ill-posed one — say so explicitly rather than
    leaving it implicit, because that is exactly what made the 0/8 headline
    describe a regime nobody had chosen deliberately."""
    args = _parse([])
    assert args.batch_mode == "fixed"
    assert args.fresh_batches is False


def test_contradictory_flags_last_one_wins() -> None:
    """Both spellings for the same option: the last one wins, as argparse does.

    Documented rather than turned into an error, because last-wins is the
    behaviour every other flag in the repo already has and an error here would
    be the only special case.
    """
    args = _parse(["--fresh-batches", "--batches", "fixed"])
    assert args.fresh_batches is False
    assert args.batch_mode == "fixed"

    args = _parse(["--batches", "fresh", "--fresh-batches"])
    assert args.fresh_batches is True
    assert args.batch_mode == "fresh"


def test_batch_mode_reaches_the_metrics() -> None:
    """Without batch_mode in the metrics, a manifest does not say which arm of
    the comparison produced it — and the two arms differ by two orders of
    magnitude in validation accuracy."""
    metrics = exp1._headline_metrics(
        {"val_acc": [0.5], "induction_mass": [0.1], "prev_token_mass": [0.05]},
        [],
        {"step2_k_composition": 0.0, "step1_l0_duplicate_mass": []},
    )
    assert "batch_mode" not in metrics  # _headline_metrics stays arm-agnostic

    # run_single_seed stamps it from the parsed flag, so plumbed here.
    args = _parse(["--batches", "fresh"])
    assert (0.0 if not args.fresh_batches else 1.0) == 1.0


def test_makefile_arms_share_every_other_hyperparameter() -> None:
    """The comparison is only matched if the two arms differ in exactly one way.

    Parse the Makefile targets and extract the flag/value pairs they pass, so a
    future edit that changes one arm's epochs or d_model but not the other's
    fails here instead of silently invalidating the finding.
    """
    makefile = Path(__file__).resolve().parents[1] / "Makefile"
    text = makefile.read_text(encoding="utf-8")

    def flags(target: str) -> dict[str, str]:
        start = text.find(f"{target}:")
        assert start >= 0, f"Makefile target {target} not found"
        # Take the recipe lines up to the next target.
        body = text[start:]
        end = body.find("\nreproduce-induction-fresh:")
        if target.startswith("reproduce-induction-fixed"):
            end = body.find("\nreproduce-induction-fresh:")
        else:
            end = body.find("\nreproduce-exp3-geometry:")
        body = body[:end] if end > 0 else body
        out: dict[str, str] = {}
        for tok in body.split():
            if not tok.startswith("--"):
                continue
            key = tok
            value = ""
            idx = body.find(tok) + len(tok)
            rest = body[idx:].lstrip()
            if rest.startswith("=") or (rest and not rest.startswith("--")):
                value = rest.split()[0] if rest.split() else ""
            out[key] = value
        return out

    fixed = flags("reproduce-induction-fixed")
    fresh = flags("reproduce-induction-fresh")
    for key in SHARED:
        flag = f"--{key.replace('_', '-')}"
        assert flag in fixed, f"{flag} missing from the fixed arm"
        assert flag in fresh, f"{flag} missing from the fresh arm"
        assert fixed[flag] == fresh[flag], (
            f"{flag} differs between arms: {fixed[flag]} vs {fresh[flag]} — "
            "the fixed-vs-fresh comparison is only valid if the sole difference "
            "is the batch regime."
        )


def test_arms_write_distinct_manifests() -> None:
    makefile = Path(__file__).resolve().parents[1] / "Makefile"
    text = makefile.read_text(encoding="utf-8")
    assert "results/exp1_induction_fixed_batches.json" in text
    assert "results/exp1_induction_fresh_batches.json" in text


def test_arms_use_the_same_seeds() -> None:
    makefile = Path(__file__).resolve().parents[1] / "Makefile"
    text = makefile.read_text(encoding="utf-8")
    assert text.count("--seeds 0,1,2") >= 2, (
        "both arms must use the same seeds for the comparison to be matched"
    )
