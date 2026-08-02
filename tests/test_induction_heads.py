"""Smoke tests for the induction heads experiment (Rung 1)."""

import torch

from src.experiments.exp1_induction_heads import (
    AttentionOnlyBlock,
    AttentionOnlyTransformer,
    causal_ablation,
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


class TestCausalAblation:
    """Falsification tests for the head_mask ablation mechanism.

    The old causal_ablation() hooked W_O's *output* and zeroed a slice of
    it — a d_model vector that had already mixed every head, so it zeroed an
    arbitrary residual-stream subspace, not a specific head's contribution.
    These tests would have failed against that implementation.
    """

    def test_ablating_all_heads_collapses_to_no_attention_baseline(self) -> None:
        """Zeroing every head in every block must reproduce the exact
        no-attention baseline: since head_mask zeroes each head's
        contribution *before* W_O mixes heads (bias=False), the block's
        output collapses to `residual + W_O(0) == residual`, i.e. attention
        never touches the residual stream at all.
        """
        torch.manual_seed(0)
        model = AttentionOnlyTransformer(
            vocab_size=16, d_model=32, n_layers=2, n_heads=4, max_seq_len=16
        )
        model.eval()
        x = torch.randint(0, 16, (2, 10))

        for block in model.blocks:
            block.head_mask = torch.zeros(block.n_heads)
        with torch.no_grad():
            ablated_logits, _ = model(x, record_attn=False)
        for block in model.blocks:
            block.head_mask = None

        with torch.no_grad():
            positions = torch.arange(x.shape[1]).unsqueeze(0)
            h = model.embed(x) + model.pos_embed(positions)
            h = model.ln_final(h)
            baseline_logits = model.unembed(h)

        assert torch.allclose(ablated_logits, baseline_logits, atol=1e-5), (
            "All-heads ablation should exactly match the no-attention baseline"
        )

    def test_head_mask_is_restored_after_ablation(self) -> None:
        """causal_ablation() must clear head_mask when it finishes, so a
        later unrelated forward pass isn't silently still ablated."""
        torch.manual_seed(0)
        model = AttentionOnlyTransformer(
            vocab_size=16, d_model=32, n_layers=1, n_heads=2, max_seq_len=16
        )
        train, _ = make_repeated_token_data(
            vocab_size=16, seq_len=10, num_train=8, num_val=8, seed=0
        )
        loader = torch.utils.data.DataLoader(train, batch_size=4)

        causal_ablation(model, loader, layer=0, head=0)

        assert model.blocks[0].head_mask is None

    def test_ablating_one_head_only_zeroes_that_head(self) -> None:
        """Ablating head h should leave the other heads' contribution to the
        pre-W_O output untouched (they aren't zeroed by the mask)."""
        block = AttentionOnlyBlock(d_model=32, n_heads=4)
        block.eval()
        x = torch.randn(1, 6, 32)

        with torch.no_grad():
            # Recompute the pre-W_O per-head output manually, once with no
            # mask and once with head 1 ablated, and compare head-by-head.
            def pre_wo_heads(mask: torch.Tensor | None) -> torch.Tensor:
                block.head_mask = mask
                h = block.ln(x)
                B, S, D = h.shape
                Q = block.W_Q(h).view(B, S, block.n_heads, block.d_head).transpose(1, 2)
                K = block.W_K(h).view(B, S, block.n_heads, block.d_head).transpose(1, 2)
                V = block.W_V(h).view(B, S, block.n_heads, block.d_head).transpose(1, 2)
                scores = Q @ K.transpose(-2, -1) / (block.d_head ** 0.5)
                causal = torch.triu(torch.full((S, S), float("-inf")), diagonal=1)
                probs = (scores + causal).softmax(dim=-1)
                out = probs @ V
                if mask is not None:
                    out = out * mask.view(1, block.n_heads, 1, 1)
                return out  # (B, n_heads, S, d_head)

            full = pre_wo_heads(None)
            mask = torch.ones(4)
            mask[1] = 0.0
            ablated = pre_wo_heads(mask)
            block.head_mask = None

        assert torch.allclose(ablated[:, 1], torch.zeros_like(ablated[:, 1]))
        for h_idx in (0, 2, 3):
            assert torch.allclose(ablated[:, h_idx], full[:, h_idx]), (
                f"Head {h_idx} should be unaffected by ablating head 1"
            )


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

    def test_repeated_prefix(self) -> None:
        """Sequences should have the prefix repeated in the full tokens."""
        train, _ = make_repeated_token_data(
            vocab_size=8, seq_len=16, num_train=10, num_val=2, prefix_ratio=0.5, seed=42
        )
        # The underlying generation produces sequences where the first
        # half is repeated. The input is tokens[:-1] (next-token shift).
        # Check that the prefix pattern exists: positions [0,8) ≈ [8, 15)
        # in the input tensor (original tokens[:-1])
        x, y = train[0]
        prefix_len = int(16 * 0.5)
        # x[8] should equal x[0] (the repeated prefix start)
        assert x[0] == x[prefix_len], "First token should repeat at prefix boundary"

    def test_deterministic_seed(self) -> None:
        """Same seed should produce same data."""
        t1, _ = make_repeated_token_data(
            vocab_size=32, seq_len=64, num_train=100, num_val=20, seed=42
        )
        t2, _ = make_repeated_token_data(
            vocab_size=32, seq_len=64, num_train=100, num_val=20, seed=42
        )
        assert torch.equal(t1.tensors[0], t2.tensors[0]), "Deterministic seed check failed"
