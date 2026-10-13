"""Smoke and falsification tests for the circuit patching experiment (Rung 4)."""

import argparse
import inspect

import torch

from src.experiments.exp1_induction_heads import make_repeated_token_data
from src.experiments.exp4_circuit_patching import (
    apply_config_presets,
    build_parser,
    detect_induction_heads,
    run_activation_patching,
    run_head_ablation,
    run_path_patching_to_logits,
    train_model,
)
from src.models.decoder_only_transformer import DecoderOnlyTransformer


def _sample_batch(vocab_size: int = 16, seq_len: int = 12, n: int = 16, seed: int = 42):
    data, _ = make_repeated_token_data(
        vocab_size=vocab_size, seq_len=seq_len, num_train=n, seed=seed
    )
    x = torch.stack([data[i][0] for i in range(n)])
    y = torch.stack([data[i][1] for i in range(n)])
    return x, y


class TestInductionHeadDetection:
    def test_detection_on_small_model(self) -> None:
        model = DecoderOnlyTransformer(
            vocab_size=16, d_model=32, n_layers=2, n_heads=2, max_seq_len=16
        )
        model.eval()
        inputs, _ = _sample_batch(n=32)
        heads = detect_induction_heads(model, inputs, threshold=0.1)
        assert isinstance(heads, list)
        for layer, head in heads:
            assert 0 <= layer < 2
            assert 0 <= head < 2

    def test_detection_empty_on_untrained(self) -> None:
        model = DecoderOnlyTransformer(
            vocab_size=16, d_model=32, n_layers=2, n_heads=2, max_seq_len=16
        )
        model.eval()
        inputs, _ = _sample_batch(n=32)
        heads = detect_induction_heads(model, inputs, threshold=0.5)
        assert isinstance(heads, list)


class TestHeadAblation:
    def test_ablation_runs(self) -> None:
        model = DecoderOnlyTransformer(
            vocab_size=16, d_model=32, n_layers=2, n_heads=2, max_seq_len=16
        )
        inputs, targets = _sample_batch(n=16)
        answers = targets[:, -1]
        counterfactuals, ctargets = _sample_batch(n=16, seed=7)
        induction_heads = detect_induction_heads(model, inputs, threshold=0.1)
        results = run_head_ablation(
            model, inputs, answers, ctargets[:, -1], induction_heads or [(0, 0)]
        )
        assert isinstance(results, dict)
        for key, val in results.items():
            assert isinstance(key, tuple)
            assert "clean_diff" in val
            assert "ablated_diff" in val
            assert "effect" in val


class TestActivationPatching:
    """Falsification tests for the resid_mid patch site.

    The previous implementation patched a forward-pre-hook on the MLP's
    input, which does not affect the residual skip (`x = x + mlp_out` still
    references the block's own unpatched `x`). These tests would not
    distinguish that bug from a no-op patch, so the strongest falsification
    check is: patching a run with *itself* as the "corrupted" source must be
    a true no-op (recovery == 0 exactly), and patching with a genuinely
    different run must generally change the logit diff.
    """

    def _setup(self):
        model = DecoderOnlyTransformer(
            vocab_size=16, d_model=32, n_layers=2, n_heads=2, max_seq_len=12
        )
        model.eval()
        clean, clean_y = _sample_batch(n=16, seed=1)
        corrupted, corrupted_y = _sample_batch(n=16, seed=2)
        return model, clean, clean_y[:, -1], corrupted, corrupted_y[:, -1]

    def test_self_patching_is_a_no_op(self) -> None:
        """Patching resid_mid from the clean run into itself must not move
        the logit diff at all — recovery is exactly 0 for every (layer, pos).
        """
        model, clean, clean_answers, _, _ = self._setup()
        results = run_activation_patching(
            model=model,
            clean_inputs=clean,
            clean_answers=clean_answers,
            corrupted_inputs=clean,
            corrupted_answers=clean_answers,
            layers_to_patch=[0, 1],
            positions_to_patch=[3, 6, 9],
        )
        for (layer, pos), vals in results.items():
            assert abs(vals["patched_diff"] - vals["clean_diff"]) < 1e-4, (
                f"Self-patching at layer {layer}, pos {pos} should be a no-op"
            )
            assert abs(vals["recovery"]) < 1e-3

    def test_patching_a_different_run_changes_the_output(self) -> None:
        """Patching in a genuinely different run's resid_mid should, at
        least at some (layer, position), change the logit diff — otherwise
        the patch isn't reaching the residual stream at all."""
        model, clean, clean_answers, corrupted, corrupted_answers = self._setup()
        results = run_activation_patching(
            model=model,
            clean_inputs=clean,
            clean_answers=clean_answers,
            corrupted_inputs=corrupted,
            corrupted_answers=corrupted_answers,
            layers_to_patch=[0, 1],
            positions_to_patch=list(range(2, 11)),
        )
        diffs = [abs(v["patched_diff"] - v["clean_diff"]) for v in results.values()]
        assert max(diffs) > 1e-4, "Patching should perturb the logit diff somewhere"


class TestPathPatching:
    def test_self_patching_has_zero_direct_effect(self) -> None:
        model = DecoderOnlyTransformer(
            vocab_size=16, d_model=32, n_layers=2, n_heads=2, max_seq_len=12
        )
        model.eval()
        clean, clean_y = _sample_batch(n=16, seed=1)
        results = run_path_patching_to_logits(
            model=model,
            clean_inputs=clean,
            clean_answers=clean_y[:, -1],
            corrupted_inputs=clean,
            corrupted_answers=clean_y[:, -1],
            heads=[(0, 0), (1, 1)],
        )
        for (layer, head), vals in results.items():
            assert abs(vals["patched_diff"] - vals["clean_diff"]) < 1e-4, (
                f"Self-patching L{layer}H{head} should have zero direct effect"
            )

    def test_runs_and_returns_expected_keys(self) -> None:
        model = DecoderOnlyTransformer(
            vocab_size=16, d_model=32, n_layers=2, n_heads=2, max_seq_len=12
        )
        model.eval()
        clean, clean_y = _sample_batch(n=16, seed=1)
        corrupted, corrupted_y = _sample_batch(n=16, seed=2)
        results = run_path_patching_to_logits(
            model=model,
            clean_inputs=clean,
            clean_answers=clean_y[:, -1],
            corrupted_inputs=corrupted,
            corrupted_answers=corrupted_y[:, -1],
            heads=[(0, 0), (0, 1), (1, 0)],
        )
        assert set(results.keys()) == {(0, 0), (0, 1), (1, 0)}
        for vals in results.values():
            assert {"clean_diff", "patched_diff", "effect"} <= vals.keys()


class TestBatchRegimeAndPresets:
    """exp4's 'standard' config must train the same regime exp1's does.

    Before this, exp4 trained on a fixed, epoch-reused dataset while
    claiming to match exp1 --standard — which forces fresh batches, because
    the 2026-08-02 matched comparison found the fixed regime actively
    harmful (0.45% vs 53.5% val accuracy). An unmatched regime makes the
    "one shared model" cascade promise false, so the flags and presets are
    pinned here.
    """

    @staticmethod
    def _args(*argv: str) -> argparse.Namespace:
        return build_parser().parse_args(list(argv))

    def test_parser_defaults_to_fixed_batches(self) -> None:
        args = self._args()
        assert args.fresh_batches is False
        assert args.batches is None
        assert args.batch_size == 64  # the previously hardcoded value

    def test_batches_fresh_writes_through(self) -> None:
        args = self._args("--batches", "fresh")
        assert args.fresh_batches is True
        assert args.batch_mode == "fresh"
        args = self._args("--fresh-batches")
        assert args.fresh_batches is True
        assert args.batch_mode == "fresh"

    def test_standard_matches_exp1_standard_and_implies_fresh(self) -> None:
        from src.experiments.exp1_induction_heads import apply_config_presets as exp1_presets

        mine = self._args("--standard")
        theirs = exp1_presets.__globals__["build_parser"]().parse_args(["--standard"])
        apply_config_presets(mine)
        exp1_presets(theirs)
        for key in (
            "vocab_size", "seq_len", "d_model", "n_layers", "n_heads",
            "epochs", "num_train", "fresh_batches",
        ):
            assert getattr(mine, key) == getattr(theirs, key), (
                f"exp4 --standard disagrees with exp1 --standard on {key}"
            )

    def test_scale_large_matches_exp1_scale_large(self) -> None:
        from src.experiments.exp1_induction_heads import apply_config_presets as exp1_presets

        mine = self._args("--scale", "large")
        theirs = exp1_presets.__globals__["build_parser"]().parse_args(["--scale", "large"])
        apply_config_presets(mine)
        exp1_presets(theirs)
        for key in (
            "vocab_size", "seq_len", "d_model", "n_layers", "n_heads",
            "epochs", "num_train", "fresh_batches",
        ):
            assert getattr(mine, key) == getattr(theirs, key), (
                f"exp4 --scale large disagrees with exp1 --scale large on {key}"
            )

    def test_conflicting_presets_are_rejected(self) -> None:
        import pytest

        with pytest.raises(SystemExit):
            apply_config_presets(self._args("--standard", "--scale", "large"))

    def test_train_model_accepts_fresh_batches_fn(self) -> None:
        """The signature contract run_single_seed depends on: without the
        parameter the fresh regime cannot be threaded through."""

        params = inspect.signature(train_model).parameters
        assert "fresh_batches_fn" in params
        assert params["fresh_batches_fn"].default is None

    def test_manifest_path_flag_exists_and_routes_probes(self) -> None:
        """The --seeds branch reads args.manifest_path; before the flag
        existed, `exp4 --seeds 0,1,2` crashed with AttributeError — found
        by the remote-notebook contract lint (2026-10-13), not by a run."""
        args = self._args("--seeds", "0", "--manifest-path", "results/probe_exp4.json")
        assert args.manifest_path == "results/probe_exp4.json"
        assert self._args("--seeds", "0").manifest_path is None
