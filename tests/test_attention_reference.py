"""The attention block against an independent reference, and its head additivity.

`tests/test_decoder_only_transformer.py` pins the properties RoPE and the KV
cache exist for. Two things were not pinned: that the block computes the same
function as a reference kernel, and that its output really is a sum over heads
(the fact every QK/OV decomposition in Phase 4 rests on).
"""

from __future__ import annotations

import torch
from torch.nn.functional import scaled_dot_product_attention

from src.models.decoder_only_transformer import Attention


def _block(seed: int = 0, d_model: int = 32, n_heads: int = 4) -> Attention:
    torch.manual_seed(seed)
    return Attention(d_model=d_model, n_heads=n_heads, max_seq_len=64).eval()


def _qkv(block: Attention, x: torch.Tensor, pos: torch.Tensor):
    B, S, _ = x.shape
    split = lambda t: t.view(B, S, block.n_heads, block.d_head).transpose(1, 2)  # noqa: E731
    q = block.rope(split(block.W_Q(x)), pos)
    k = block.rope(split(block.W_K(x)), pos)
    v = split(block.W_V(x))
    return q, k, v


def _probs(block: Attention, q: torch.Tensor, k: torch.Tensor) -> torch.Tensor:
    """Causal attention weights, recomputed here from Q and K."""
    S = q.size(2)
    scores = q @ k.transpose(-2, -1) / block.d_head**0.5
    return (scores + block.causal_mask[:, :, :S, :S]).softmax(-1)


def test_matches_torch_scaled_dot_product_attention() -> None:
    block = _block()
    x = torch.randn(2, 9, 32)
    pos = torch.arange(9).unsqueeze(0).expand(2, -1)
    out, _ = block(x, pos)

    q, k, v = _qkv(block, x, pos)
    ref = scaled_dot_product_attention(q, k, v, is_causal=True)
    ref = block.W_O(ref.transpose(1, 2).reshape(2, 9, 32))
    assert torch.allclose(out, ref, atol=1e-5), (out - ref).abs().max()


def test_a_future_token_cannot_change_an_earlier_output() -> None:
    block = _block()
    x = torch.randn(1, 8, 32)
    pos = torch.arange(8).unsqueeze(0)
    before, _ = block(x, pos)
    x2 = x.clone()
    x2[:, 5:] = torch.randn(1, 3, 32)  # rewrite the last three tokens
    after, _ = block(x2, pos)
    assert torch.allclose(before[:, :5], after[:, :5], atol=1e-6)
    assert not torch.allclose(before[:, 5:], after[:, 5:], atol=1e-3)


def test_the_output_is_a_sum_over_heads() -> None:
    """out = sum_h (A_h V_h) W_O[h]: each head writes its own slice of W_O."""
    block = _block()
    x = torch.randn(1, 7, 32)
    pos = torch.arange(7).unsqueeze(0)
    out, _ = block(x, pos)

    q, k, v = _qkv(block, x, pos)
    probs = _probs(block, q, k)
    per_head = probs @ v  # (1, heads, 7, d_head)
    d = block.d_head
    total = torch.zeros_like(out)
    for h in range(block.n_heads):
        total = total + per_head[:, h] @ block.W_O.weight[:, h * d : (h + 1) * d].T
    assert torch.allclose(out, total, atol=1e-5), (out - total).abs().max()


def test_zeroing_one_head_removes_exactly_its_contribution() -> None:
    block = _block()
    x = torch.randn(1, 7, 32)
    pos = torch.arange(7).unsqueeze(0)
    full, _ = block(x, pos)

    q, k, v = _qkv(block, x, pos)
    probs = _probs(block, q, k)
    d = block.d_head
    head = 2
    contribution = (probs @ v)[:, head] @ block.W_O.weight[:, head * d : (head + 1) * d].T

    block.head_mask = torch.ones(block.n_heads)
    block.head_mask[head] = 0.0
    ablated, _ = block(x, pos)
    assert torch.allclose(full - ablated, contribution, atol=1e-5)
