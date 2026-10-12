---
title: "Positional Encoding and RoPE"
tags: [type/lesson, phase/4, state/consolidated]
created: 2026-10-11
---

## Positional Encoding and RoPE

## What it is

RoPE (Rotary Positional Embedding, Su et al., 2024) encodes position by
*rotating* each 2-D slice of the query and key vectors by an angle proportional
to the position, so that the attention score between positions `i` and `j`
depends only on `i - j`.

## Why it exists

Self-attention is a set function: permute the input sequence and every position
still gets the same weighted average of the same values. Without a position
signal a transformer cannot tell `a b` from `b a`, and cannot express "the token
after the previous occurrence of this one" at all — which is the induction
relation this repo is built to find.

Two families of fix exist:

- **Absolute** (sinusoidal, learned): add a position vector to each token. The
  model must *learn* relative position from it, and generalisation past the
  trained length is poor.
- **Relative**: make the score itself a function of `i - j`.

RoPE is the second kind, and it gets there without extra parameters: the
rotation is a fixed, parameter-free operation on `Q` and `K` only.

## How it works

`RotaryEmbedding` in `src/models/decoder_only_transformer.py`:

```python
inv_freq = 1.0 / (base ** (arange(0, d_head, 2) / d_head))   # (d_head/2,)

def forward(self, x, position_ids):
    freqs = position_ids.unsqueeze(-1) * inv_freq             # (B, S, d_head/2)
    emb   = cat([freqs, freqs], dim=-1)                       # (B, S, d_head)
    return x * emb.cos() + self._rotate_half(x) * emb.sin()
```

with `_rotate_half` splitting the last dimension into two halves:

```python
def _rotate_half(x):
    x1, x2 = x.chunk(2, dim=-1)
    return cat([-x2, x1], dim=-1)
```

The consequence is the whole point: the rotation applies to **halves** of the
vector (`chunk`), not to **interleaved pairs** (`repeat_interleave`). The two
conventions require different `cos`/`sin` layouts, and mixing them still gives
every position a distinct, injective signal — so training does not obviously
break — but the relative-position property is silently lost. That is exactly the
bug this repo shipped once, and
`tests/test_decoder_only_transformer.py::TestRotaryEmbedding::test_relative_position_invariance`
pins it: scores at a fixed offset must match across absolute positions, and
scores at different offsets must differ.

## The KV-cache position offset

The trap that bit this repo in a second, subtler way. `DecoderOnlyTransformer.forward`
computes

```python
past_len = 0
if past_kv is not None:
    for layer_kv in past_kv:
        if layer_kv is not None:
            past_len = layer_kv[0].size(2)
            break
position_ids = torch.arange(past_len, past_len + S).unsqueeze(0)
```

During incremental decoding `x` holds only the newest token, so `S == 1`. A
bare `arange(S)` therefore gives the single position `0` for *every* generated
token, and the newest token is rotary-encoded as if it were the first one —
destroying the property RoPE was chosen for. The offset must continue from the
cached length. See [[04_nlp_and_transformers/notes/decoder-only-architecture]]
for how `generate()` drives this.

## Base frequency

`base = 10000.0` by default. `inv_freq` spans
`[1/base^(d_head-2)/d_head, 1]`, so low-frequency pairs rotate slowly (they
carry coarse, long-range position) and high-frequency pairs rotate quickly
(coarse position aliases, fine discrimination). For the short sequences in this
repo (`seq_len` 16–128) the fast pairs dominate, which is why the induction
detector's diagonal+1 pattern is position-specific.

## Links

- [[04_nlp_and_transformers/notes/self-and-multi-head-attention]] — where the rotated Q and K are consumed
- [[04_nlp_and_transformers/notes/decoder-only-architecture]] — the `generate()` path that needs the offset
- [[04_nlp_and_transformers/proofs/residual-stream-communication-channel]] — why the residual stream carries no position on its own
- [[04_nlp_and_transformers/notes/qk-ov-circuits]] — the QK circuit that RoPE acts through

## Open questions

- #question At what `max_seq_len` does the default `base = 10000` start to alias, and would the modular-addition task at P=113 already be inside that regime?
