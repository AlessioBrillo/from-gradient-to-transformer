"""Tests for the decoder-only transformer model."""

import torch

from src.models.decoder_only_transformer import (
    DecoderOnlyTransformer,
    RMSNorm,
    RotaryEmbedding,
)


class TestRMSNorm:
    def test_scale_invariance(self) -> None:
        rmsnorm = RMSNorm(d_model=64)
        x = torch.randn(4, 16, 64)
        y1 = rmsnorm(x)
        y2 = rmsnorm(x * 5.0)
        assert torch.allclose(y1, y2, atol=1e-5)

    def test_output_shape(self) -> None:
        rmsnorm = RMSNorm(d_model=128)
        x = torch.randn(2, 8, 128)
        y = rmsnorm(x)
        assert y.shape == (2, 8, 128)


class TestRotaryEmbedding:
    def test_position_sensitivity(self) -> None:
        rope = RotaryEmbedding(d_head=16)
        x = torch.randn(1, 1, 1, 16)
        q0 = rope(x, torch.zeros(1, 1, dtype=torch.long))
        q1 = rope(x, torch.ones(1, 1, dtype=torch.long))
        assert not torch.allclose(q0, q1)

    def test_output_shape(self) -> None:
        rope = RotaryEmbedding(d_head=32)
        x = torch.randn(2, 4, 10, 32)
        pos = torch.arange(10).unsqueeze(0).expand(2, -1)
        y = rope(x, pos)
        assert y.shape == (2, 4, 10, 32)


class TestDecoderOnlyTransformer:
    def test_output_shape(self) -> None:
        model = DecoderOnlyTransformer(
            vocab_size=100, d_model=64, n_layers=2, n_heads=2, max_seq_len=32
        )
        x = torch.randint(0, 100, (4, 16))
        logits, _ = model(x, return_cache=True)
        assert logits.shape == (4, 16, 100)

    def test_gradient_flows(self) -> None:
        model = DecoderOnlyTransformer(
            vocab_size=100, d_model=32, n_layers=2, n_heads=2, max_seq_len=32
        )
        x = torch.randint(0, 100, (4, 16))
        y = torch.randint(0, 100, (4, 16))
        logits, _ = model(x)
        loss = torch.nn.functional.cross_entropy(logits.reshape(-1, 100), y.reshape(-1))
        loss.backward()
        has_grad = any(p.grad is not None for p in model.parameters())
        assert has_grad

    def test_causal_mask(self) -> None:
        model = DecoderOnlyTransformer(
            vocab_size=100, d_model=32, n_layers=2, n_heads=2, max_seq_len=32
        )
        model.eval()
        x = torch.randint(0, 100, (1, 8))
        _, cache = model(x, return_cache=True)
        attn = cache["blocks.0.attn.attn_probs"]
        upper = torch.triu(torch.ones(8, 8), diagonal=1)
        causal_mass = (attn[0, 0] * upper).sum()
        assert causal_mass < 0.01

    def test_generation(self) -> None:
        model = DecoderOnlyTransformer(
            vocab_size=100, d_model=32, n_layers=2, n_heads=2, max_seq_len=32
        )
        model.eval()
        input_ids = torch.randint(0, 100, (1, 8))
        generated = model.generate(
            input_ids, max_new_tokens=5, temperature=0.8, top_k=10
        )
        assert generated.shape == (1, 13)

    def test_cache_contents(self) -> None:
        model = DecoderOnlyTransformer(
            vocab_size=100, d_model=32, n_layers=2, n_heads=2, max_seq_len=32
        )
        x = torch.randint(0, 100, (2, 8))
        _, cache = model(x, return_cache=True)
        expected_keys = {
            "hook_embed",
            "blocks.0.attn.Q",
            "blocks.0.attn.K",
            "blocks.0.attn.V",
            "blocks.0.attn.attn_probs",
            "blocks.0.attn.attn_out",
            "blocks.0.resid_pre",
            "blocks.0.resid_post",
            "blocks.0.mlp_pre",
            "blocks.0.mlp_out",
            "blocks.1.resid_pre",
            "blocks.1.resid_post",
            "hook_ln_final",
            "hook_logits",
        }
        assert expected_keys.issubset(set(cache.keys()))

    def test_normalize_embeddings(self) -> None:
        model = DecoderOnlyTransformer(
            vocab_size=100, d_model=32, n_layers=2, n_heads=2, max_seq_len=32,
            normalize_embed=True,
        )
        model.normalize_embeddings()
        norms = model.embed.weight.norm(dim=-1)
        assert torch.allclose(norms, torch.ones_like(norms), atol=1e-5)
