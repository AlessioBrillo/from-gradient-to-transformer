"""Smoke tests for the induction heads experiment (Rung 1)."""

import torch

from src.experiments.exp1_induction_heads import (
    AttentionOnlyBlock,
    AttentionOnlyTransformer,
    make_repeated_token_data,
)


class TestAttentionOnlyTransformer:
    """Test the attention-only transformer."""

    def test_shape(self) -> None:
        """Output logits should have correct shape for next-token prediction."""
        model = AttentionOnlyTransformer(
            vocab_size=32, d_model=64, n_layers=2, n_heads=4, max_seq_len=64
        )
        x = torch.randint(0, 32, (4, 32))
        logits, attn = model(x, record_attn=True)
        assert logits.shape == (4, 32, 32), f"Expected (4, 32, 32), got {logits.shape}"
        assert attn is not None and len(attn) == 2  # 2 layers

    def test_causal_mask(self) -> None:
        """Attention should be causally masked (upper triangle = 0)."""
        block = AttentionOnlyBlock(d_model=32, n_heads=2)
        x = torch.randn(1, 10, 32)
        attn_records = []
        _ = block(x, past_attn=attn_records)
        attn_probs = attn_records[0]  # (1, 2, 10, 10)
        # Check that upper triangle (excluding diagonal) is ~0
        upper = torch.triu(torch.ones(10, 10), diagonal=1)
        causal_mass = (attn_probs[0, 0] * upper).sum()
        assert causal_mass < 0.01, f"Causal mask failed: {causal_mass:.4f} mass above diagonal"


class TestInductionData:
    """Test the repeated-token dataset."""

    def test_shapes(self) -> None:
        """Train dataset should produce correct shapes."""
        train, val = make_repeated_token_data(
            vocab_size=32, seq_len=64, num_train=100, num_val=20, seed=42
        )
        x, y = train[0]
        assert x.shape == (63,), f"Expected (63,), got {x.shape}"
        assert y.shape == (63,)
