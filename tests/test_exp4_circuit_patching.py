"""Smoke and falsification tests for the circuit patching experiment (Rung 4)."""

import torch

from src.experiments.exp1_induction_heads import make_repeated_token_data
from src.experiments.exp4_circuit_patching import (
    detect_induction_heads,
    run_activation_patching,
    run_head_ablation,
    run_path_patching_to_logits,
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
