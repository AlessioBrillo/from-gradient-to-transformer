---
tags: [type/proof, phase/4, state/review]
authorship: claude
created: 2026-11-17
---

# Proof: the attention block is attention, RoPE is relative, and the cache is exact

> **Authorship.** Written by Claude on 2026-11-17, not reconstructed from memory by
> the repository owner. Every claim below is pinned by a test, so the proof can be
> checked by running them; re-deriving it unaided is still open.
> Companion exercise: [[04_nlp_and_transformers/exercises/ex-01-transformer-from-scratch]].

## Claim

The decoder-only transformer in `src/models/decoder_only_transformer.py` (a) computes
scaled dot-product causal attention, (b) is a sum over independent heads, (c) encodes
position only through the *offset* between two tokens, and (d) generates the same
tokens with a KV cache as without one.

## Why each holds

**(a) It is attention.** Scores are `Q K^T / sqrt(d_head)`, a causal mask of `-inf`
above the diagonal, a softmax over keys, then a weighted sum of `V`. The scale keeps
the score variance near 1 as `d_head` grows; without it the softmax saturates and
gradients vanish. The test recomputes the block with PyTorch's reference kernel,
`scaled_dot_product_attention(..., is_causal=True)`, and requires agreement to 1e-5
(`tests/test_attention_reference.py::test_matches_torch_scaled_dot_product_attention`).

**(b) The output is a sum over heads.** With the heads concatenated and projected by
`W_O`, the output is `sum_h (A_h V_h) W_O[:, h-th block]^T`: each head writes through
its own slice of `W_O` and nothing else. That is what makes a head's contribution
separable, ablatable and attributable, and it is the premise of the QK/OV
decomposition ([[04_nlp_and_transformers/proofs/qk-ov-decomposition]]). Two tests pin
it: the explicit sum over heads equals the block's output, and zeroing one head
removes exactly that head's term
(`test_the_output_is_a_sum_over_heads`, `test_zeroing_one_head_removes_exactly_its_contribution`).

**(c) RoPE is relative.** RoPE rotates each 2-D pair of a query or key by an angle
proportional to its position. A rotation by `i*theta` applied to `q` and by `j*theta`
to `k` gives `<R_i q, R_j k> = <q, R_(j-i) k>`, which depends on `i - j` alone. The
property survives only if the cos/sin layout matches the rotation convention actually
used: a previous version of this file built them for interleaved pairs but rotated
halves, still gave every position a distinct code, trained without complaint, and
broke relativity. `test_relative_position_invariance` is the test that catches it;
`test_position_sensitivity` alone does not.

**(d) The cache is exact.** Keys and values of earlier tokens do not depend on later
tokens (causality), so they can be stored. The one subtlety is the position of the new
token: it must be the cached length, for both the RoPE angle and the row of the causal
mask. The code slices the mask at the query's absolute offset, and the history records
the bug where row 0 was used and generation collapsed to a function of the first token
(`test_kv_cache_semantics`, `test_rope_position_advances_with_cache`,
`test_generate_with_kv_cache_reproduces`).

**Causality, directly.** Rewriting the last three tokens leaves the first five outputs
unchanged to 1e-6 and changes the last three
(`test_a_future_token_cannot_change_an_earlier_output`).

## What is not claimed

- Training behaviour. These are properties of the forward pass, not evidence that the
  model learns anything.
- Sinusoidal encodings. The skill tree once listed them; only RoPE is implemented here.
- Any property of the *attention-only* model of Rung 1, which has its own class
  (`src/models/attention_only_transformer.py`) and is covered by its own tests.

## Outcome

- [x] Each claim is backed by a test that fails on a plausible bug (the RoPE convention
      mismatch and the cache-offset bug are both real defects from this repository's
      history).
- [ ] Reconstructed from memory by the repository owner. Not done.
