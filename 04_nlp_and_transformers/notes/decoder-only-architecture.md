---
title: "Decoder-Only Architecture"
tags: [type/lesson, phase/4, state/consolidated]
created: 2026-10-11
---

# Decoder-Only Architecture

## What it is

The full stack in `src/models/decoder_only_transformer.py`:
`DecoderOnlyTransformer` takes token ids and returns next-token logits, with
every intermediate activation reachable through a hook cache.

## Why it exists

Everything downstream in this repo — induction-head detection, activation and
path patching, the logit lens, SAE training on real activations — is a
conversation with *this* model's internals. So the model is built to be read,
not just run: every sublayer writes its activations into a dict keyed by a
stable, hierarchical name.

## How it works

```python
model = DecoderOnlyTransformer(
    vocab_size=2161, d_model=256, n_layers=4, n_heads=8,
    d_mlp=1024, max_seq_len=128, tie_weights=True,
)
logits, cache = model(x, return_cache=True)   # (B, S, vocab), dict
```

The forward pass, in order:

| Stage | Code | Shape |
|---|---|---|
| Token embedding | `self.embed(x)` | `(B, S, d_model)` |
| N blocks | `self.blocks[i]` | `(B, S, d_model)` |
| Final norm | `self.ln_final(h)` | `(B, S, d_model)` |
| Unembed | `self.unembed(h)` | `(B, S, vocab)` |

Each `TransformerBlock` is a **pre-RMSNorm residual block**:

```
h     = ln_attn(x);  x = x + W_O(attn(rope(W_Q h, W_K h), W_V h))
h     = ln_mlp(x);   x = x + W_out(relu(W_in(h)))
```

Pre-norm (normalise the *input* to each sublayer rather than its output) is what
makes the residual stream a clean communication channel: the sublayer only ever
*writes a delta* to it (see
[[04_nlp_and_transformers/proofs/residual-stream-communication-channel]]).
RMSNorm (`x / rms(x) * scale`, no mean-centring) is the modern standard.

**`tie_weights`.** When true, `unembed.weight is embed.weight`. Halves the
parameter count and is the standard choice for small models; it also means the
embedding matrix is directly interpretable through the vocabulary.

**Causal masking** is applied inside every `Attention` (see
[[04_nlp_and_transformers/notes/self-and-multi-head-attention]]), so the whole
stack is autoregressive by construction.

## Generation and the KV cache

`generate()` prefills the whole prompt in one forward pass, then decodes one
token at a time against the cache:

```python
# Prefill: every prompt token into the cache.
logits, cache = self(generated, return_cache=True)
past_kv = self._extend_past_kv([None] * n_layers, cache, device)

# Decode: one token per forward.
logits, cache = self(generated[:, -1:], past_kv=past_kv, return_cache=True)
past_kv = self._extend_past_kv(past_kv, cache, device)
```

`_extend_past_kv` reads `blocks.{i}.attn.K_new` / `.V_new` — the
**pre-concatenation** tensors for the step being added. `blocks.{i}.attn.K` /
`.V` hold the full sequence (past + this step) for circuit analysis, and
concatenating those instead of `.K_new` would double the cached prefix on every
step. That is a bug this repo shipped; the distinction is documented on
`Attention.forward` and pinned by
`tests/test_decoder_only_transformer.py::test_kv_cache_semantics`.

Greedy generation (`top_k=1`) must reproduce the full forward pass token for
token; `test_generate_sees_the_whole_prompt` checks exactly that.

## The hook cache

`return_cache=True` fills a dict with these keys — the surface area of every
analysis in this repo:

| Key | Meaning |
|---|---|
| `hook_embed` | post-embedding residual stream at position 0 |
| `blocks.{i}.resid_pre`, `.resid_post` | residual stream in and out of block `i` |
| `blocks.{i}.ln_attn` | the normalised input to block `i`'s attention |
| `blocks.{i}.attn.{Q,K,V}` | per-head query/key/value **for the whole sequence** |
| `blocks.{i}.attn.{K_new,V_new}` | the same, for this step only (cache growth) |
| `blocks.{i}.attn.attn_probs` | `(B, n_heads, S, S_kv)` attention probabilities |
| `blocks.{i}.attn.attn_out` | post-`W_O` attention output |
| `blocks.{i}.mlp_pre`, `.mlp_out` | ReLU activation and its linear read-out |
| `hook_ln_final` | the final normalised residual stream |
| `hook_logits` | unembedded logits |

`attn_probs` is what the induction detector reads (`diag+1` mass);
`hook_ln_final`'s input is what `exp5` harvests for SAE training; `resid_pre`
/`attn_out` are what activation patching moves.

## Links

- [[04_nlp_and_transformers/notes/self-and-multi-head-attention]] — the attention sublayer in detail
- [[04_nlp_and_transformers/notes/positional-encoding-and-rope]] — RoPE and the position offset
- [[04_nlp_and_transformers/proofs/logit-lens]] — reading the residual stream through `unembed`
- [[05_llm_engineering/notes/01-transformer-lens-hooks]] — the hook conventions this cache implements
- [[04_nlp_and_transformers/proofs/circuit-analysis-complete]] — the Phase 4 gate proof built on this model

## Open questions

- #question How much does unembed-tying help or hurt the Fourier analysis — does the tied unembed bias which frequencies survive?
