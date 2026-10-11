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

    def test_relative_position_invariance(self) -> None:
        """The defining property of RoPE: <RoPE(q, i), RoPE(k, j)> depends
        only on i - j, not on i and j individually.

        This is the property that distinguishes correct RoPE from an
        arbitrary injective position code — and it only holds if the cos/sin
        construction matches the rotate-half convention actually used to
        rotate the vectors. Mixing repeat_interleave-built cos/sin with a
        chunk-based rotate_half (as a previous version did) still gives every
        position a distinct signal, so it would pass a weaker "position
        sensitivity" check, but fails this one.
        """
        torch.manual_seed(0)
        d_head = 16
        rope = RotaryEmbedding(d_head=d_head)
        q = torch.randn(1, 1, 1, d_head)
        k = torch.randn(1, 1, 1, d_head)

        def score(i: int, j: int) -> float:
            q_rot = rope(q, torch.tensor([[i]]))
            k_rot = rope(k, torch.tensor([[j]]))
            return (q_rot[0, 0, 0] @ k_rot[0, 0, 0]).item()

        # Same offset (i - j), different absolute positions: scores must match.
        pairs_offset_3 = [(3, 0), (10, 7), (50, 47)]
        scores = [score(i, j) for i, j in pairs_offset_3]
        for s in scores[1:]:
            assert abs(s - scores[0]) < 1e-3, (
                f"Scores at the same offset should match, got {scores}"
            )

        # Different offsets should (generically) give a different score —
        # otherwise the check above would be vacuous.
        assert abs(score(5, 0) - score(1, 0)) > 1e-3


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
        generated = model.generate(input_ids, max_new_tokens=5, temperature=0.8, top_k=10)
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

    def test_kv_cache_semantics(self) -> None:
        """KV-cached generation must match full forward pass logits.

        This test used to assert only that the output shape was right and that
        new tokens differed from the prompt — which is why two real bugs in
        `generate()` survived:

        1. The prompt was never prefilled. `generate()` called
           `self(generated[:, -1:], past_kv=past_kv)` with an *empty* cache on
           the first step, so every token of the prompt except its last was
           silently discarded before any attention ran.
        2. RoPE positions restarted at 0. `forward()` computed
           `position_ids = torch.arange(S)`, and during incremental decoding
           `S == 1`, so every generated token was rotary-encoded at position 0
           — destroying the relative-position property RoPE exists for.

        Both are invisible to a shape check, so this test actually compares
        logits now.
        """
        torch.manual_seed(0)
        model = DecoderOnlyTransformer(
            vocab_size=100, d_model=32, n_layers=2, n_heads=2, max_seq_len=32
        )
        model.eval()
        x = torch.randint(0, 100, (1, 6))

        with torch.no_grad():
            logits_full, _ = model(x)

        # Incrementally re-run the same prefix one token at a time, rebuilding
        # the cache the way generate() does, and compare the final logits.
        with torch.no_grad():
            past: list = [None] * model.n_layers
            step_logits = []
            for t in range(x.shape[1]):
                logits, cache = model(x[:, t : t + 1], past_kv=past, return_cache=True)
                past = model._extend_past_kv(past, cache, x.device)
                step_logits.append(logits[:, -1])
            incremental = torch.cat(step_logits, dim=0)

        assert incremental.shape == logits_full[0].shape
        assert torch.allclose(
            incremental, logits_full[0], atol=1e-5
        ), f"KV-cached forward diverges from full pass: max diff \
{(incremental - logits_full[0]).abs().max().item():.3e}"

    def test_generate_sees_the_whole_prompt(self) -> None:
        """Greedy generation must continue the full prompt, not its last token.

        If the prompt is not prefilled into the KV cache, the first sampled
        token is a function of one token alone. The discriminator: run
        `generate` on the prompt, then run the equivalent greedy walk with an
        explicit full-input forward and compare token by token.
        """
        torch.manual_seed(1)
        model = DecoderOnlyTransformer(
            vocab_size=50, d_model=32, n_layers=2, n_heads=2, max_seq_len=32
        )
        model.eval()
        prompt = torch.randint(0, 50, (1, 5))
        n_new = 4

        # top_k=1 makes multinomial sampling effectively greedy.
        gen = model.generate(prompt, max_new_tokens=n_new, temperature=1.0, top_k=1)

        with torch.no_grad():
            seq = prompt.clone()
            for _ in range(n_new):
                logits, _ = model(seq)
                next_tok = logits[:, -1].argmax(dim=-1, keepdim=True)
                seq = torch.cat([seq, next_tok], dim=1)

        msg = f"generate() diverged: {gen.tolist()} vs {seq.tolist()}"
        assert torch.equal(gen, seq), msg

    def test_rope_position_advances_with_cache(self) -> None:
        """RoPE must see the true absolute position during incremental decoding.

        Direct regression test for the position-offset bug: the cache holds N
        tokens, so the token being decoded sits at position N, not 0.
        """
        torch.manual_seed(2)
        model = DecoderOnlyTransformer(
            vocab_size=40, d_model=32, n_layers=1, n_heads=2, max_seq_len=32
        )
        model.eval()
        x = torch.randint(0, 40, (1, 3))

        with torch.no_grad():
            past: list = [None] * model.n_layers
            for t in range(x.shape[1]):
                _, cache = model(x[:, t : t + 1], past_kv=past, return_cache=True)
                past = model._extend_past_kv(past, cache, x.device)

            # Decode a fresh token with 3 tokens already cached.
            nxt = torch.randint(0, 40, (1, 1))
            _, cache_new = model(nxt, past_kv=past, return_cache=True)

        # The Q for the new token must have been rotated at position 3, i.e.
        # it must equal a direct RoPE call with position_ids == [[3]] applied
        # to the *normalised* hidden state (the block applies RMSNorm first).
        block = model.blocks[0]
        expected_pos = torch.tensor([[x.shape[1]]])
        with torch.no_grad():
            h = block.ln_attn(model.embed(nxt))
            q_expected = block.attn.W_Q(h)
            q_expected = (
                q_expected.view(1, 1, block.attn.n_heads, block.attn.d_head).transpose(1, 2)
            )
            q_expected = block.attn.rope(q_expected, expected_pos)

        assert torch.allclose(cache_new["blocks.0.attn.Q"], q_expected, atol=1e-6), (
            "the decoded token was not rotary-encoded at its true position"
        )

    def test_generate_with_kv_cache_reproduces(self) -> None:
        """Generation with identical seeds should be deterministic."""
        model = DecoderOnlyTransformer(
            vocab_size=100, d_model=32, n_layers=2, n_heads=2, max_seq_len=32
        )
        model.eval()
        x = torch.randint(0, 100, (1, 4))
        torch.manual_seed(42)
        gen1 = model.generate(x, max_new_tokens=5, temperature=0.5, top_k=10)
        torch.manual_seed(42)
        gen2 = model.generate(x, max_new_tokens=5, temperature=0.5, top_k=10)
        assert torch.equal(gen1, gen2), "Deterministic generation should be identical"
