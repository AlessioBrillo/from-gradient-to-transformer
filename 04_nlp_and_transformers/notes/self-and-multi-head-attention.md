---
title: "Self-Attention and Multi-Head Attention"
tags: [type/lesson, phase/4, state/consolidated]
created: 2026-10-11
---

## Self-Attention and Multi-Head Attention

## What it is

A single differentiable operation that lets every position in a sequence read
from every earlier position, computing a weighted average of value vectors
where the weights come from a learned query–key similarity.

## Why it exists

A feed-forward layer maps each position independently, so it cannot represent
anything that depends on *other* positions — and "copy the token that followed
the previous occurrence of this one" is exactly such a relation. Attention is
the operation that makes position-to-position information flow possible, and it
is the only place in the standard transformer block where it happens.

## How it works

For an input `x` of shape `(B, S, D)` — batch, sequence, model dimension —
`Attention.forward` in `src/models/decoder_only_transformer.py` computes:

```
Q = W_Q(x).view(B, S, n_heads, d_head).transpose(1, 2)   # (B, H, S, d_head)
K = W_K(x).view(B, S, n_heads, d_head).transpose(1, 2)   # (B, H, S, d_head)
V = W_V(x).view(B, S, n_heads, d_head).transpose(1, 2)   # (B, H, S, d_head)
```

with `d_head = d_model // n_heads`, then applies RoPE to `Q` and `K` (see
[[04_nlp_and_transformers/notes/positional-encoding-and-rope]]) and scores:

```
scores = Q @ K^T / sqrt(d_head)          # (B, H, S, S_kv)
scores = scores + causal_mask[:, :, offset:offset+S, :S_kv]
probs  = softmax(scores, dim=-1)         # attention probabilities
out    = probs @ V                       # (B, H, S, d_head)
out    = out.transpose(1, 2).reshape(B, S, D)
attn_out = W_O(out)
```

Three details that matter for interpretability:

**Scaling by `sqrt(d_head)`.** Without it, the raw dot product grows with
dimension, softmax saturates, and gradients vanish. This is why `d_head`, not
`d_model`, sets the scale.

**The causal mask.** `self.causal_mask` is a
`(1, 1, max_seq_len, max_seq_len)` buffer of `-inf` above the diagonal, added to
the scores before the softmax. Position `i` can only attend to `j <= i`, so the
model cannot see the future — which is what makes autoregressive training
valid. The `offset` in the slice exists because during KV-cached decoding the
query is a single token at absolute position `offset`, not at row 0; slicing
from row 0 would silently let it attend to the wrong things.

**The head split.** `n_heads` heads share the same `d_model` residual stream
but each gets its own `d_head` slice of `Q`, `K`, `V` and its own column block
of `W_O`. Splitting `d_model` across heads is what lets different heads
specialise — an induction head and a previous-token head can coexist in the same
layer because they read the same stream through different projections. See
[[04_nlp_and_transformers/notes/qk-ov-circuits]] for what each head's QK and OV
halves compute.

`Attention.forward` also takes a `head_mask` of shape `(n_heads,)`: multiplying
`attn_out` by it zeroes chosen heads' contributions without touching the
attention pattern. That is the ablation primitive
`src/experiments/exp1_induction_heads.py` uses to show that a detected head is
load-bearing.

The diagnostic tensors are cached under
`blocks.{layer}.attn.{Q,K,V,attn_probs,attn_out}` when `return_cache=True` —
which is the only reason any of this is analysable after the fact. See
[[05_llm_engineering/proofs/hook-intervention]].

## Links

- [[04_nlp_and_transformers/notes/positional-encoding-and-rope]] — where the rotation on Q and K comes from
- [[04_nlp_and_transformers/notes/qk-ov-circuits]] — the QK/OV decomposition of a single head
- [[04_nlp_and_transformers/notes/induction-heads]] — the head pattern this operation is being searched for
- [[05_llm_engineering/notes/01-transformer-lens-hooks]] — how the cached Q/K/V/attn_probs are reached

## Open questions

- #question Does head specialisation survive when `n_heads` is large enough that most heads are dead on a small task, or does the effective head count collapse?
