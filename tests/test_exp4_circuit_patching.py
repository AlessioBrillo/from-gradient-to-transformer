"""Smoke tests for the circuit patching experiment (Rung 4)."""

import torch

from src.experiments.exp1_induction_heads import make_repeated_token_data
from src.experiments.exp4_circuit_patching import (
    detect_induction_heads,
    run_head_ablation,
)
from src.models.decoder_only_transformer import DecoderOnlyTransformer


class TestInductionHeadDetection:
    def test_detection_on_small_model(self) -> None:
        model = DecoderOnlyTransformer(
            vocab_size=16, d_model=32, n_layers=2, n_heads=2, max_seq_len=16
        )
        model.eval()
        data, _ = make_repeated_token_data(
            vocab_size=16, seq_len=12, num_train=32, seed=42
        )
        inputs = torch.stack([data[i][0] for i in range(8)])
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
        data, _ = make_repeated_token_data(
            vocab_size=16, seq_len=12, num_train=32, seed=42
        )
        inputs = torch.stack([data[i][0] for i in range(8)])
        heads = detect_induction_heads(model, inputs, threshold=0.5)
        assert isinstance(heads, list)


class TestHeadAblation:
    def test_ablation_runs(self) -> None:
        model = DecoderOnlyTransformer(
            vocab_size=16, d_model=32, n_layers=2, n_heads=2, max_seq_len=16
        )
        data, _ = make_repeated_token_data(
            vocab_size=16, seq_len=12, num_train=32, seed=42
        )
        inputs = torch.stack([data[i][0] for i in range(8)])
        induction_heads = detect_induction_heads(model, inputs, threshold=0.1)
        results = run_head_ablation(model, inputs, induction_heads or [(0, 0)])
        assert isinstance(results, dict)
        for key, val in results.items():
            assert isinstance(key, tuple)
            assert "clean_diff" in val
            assert "ablated_diff" in val
            assert "effect" in val
