---
tags: [type/exercise, phase/4, state/review]
---

# Exercise 01 — Build a Decoder-Only Transformer from Scratch

## Objective
Implement a complete decoder-only transformer in PyTorch with RoPE positional encoding, Pre-RMSNorm, causal multi-head attention, and autoregressive generation. This is the model that powers GPT, Claude, and every modern LLM — and it will be the analysis vehicle for all MI work in the capstone.

## Prerequisites
- Phase 3 micrograd exercise (backprop understanding)
- Self-attention and multi-head attention concepts
- Positional encoding intuition (why absolute position isn't enough)

## Core Implementation

### Step 1: RMSNorm
Implement Pre-RMSNorm instead of LayerNorm. RMSNorm only scales by the RMS of activations (no mean-centering). It's the modern standard (Gemma, Llama, etc.) and is scale-invariant by construction.

```python
class RMSNorm(nn.Module):
    def __init__(self, d_model: int, eps: float = 1e-6) -> None:
        # scale: learnable parameter, shape (d_model,)
        # eps: small constant for numerical stability
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # Compute RMS: sqrt(mean(x^2)) per token
        # Normalize: x / (rms + eps) * scale
```

**Verify**: `rmsnorm(x * 5.0)` should equal `rmsnorm(x)`.

### Step 2: Rotary Positional Embedding (RoPE)
Implement Su et al., 2024 RoPE: apply a rotation to query and key vectors based on their position, so that the dot product Q·K naturally encodes relative position.

```python
class RotaryEmbedding(nn.Module):
    def __init__(self, d_head: int, base: float = 10000.0):
        inv_freq = 1.0 / (base ** (torch.arange(0, d_head, 2).float() / d_head))
    def forward(self, x: torch.Tensor, position_ids: torch.Tensor) -> torch.Tensor:
        # Compute frequency tensor from position_ids * inv_freq
        # Apply: x_rotated = x * cos + rotate_half(x) * sin
```

**Key insight**: RoPE makes the dot product `Q_i · K_j` a function of `(i - j)`, not just `i` and `j` independently. This gives the model a natural notion of relative position without extra parameters.

### Step 3: Multi-Head Causal Self-Attention
Implement the core attention mechanism with causal masking.

```python
class Attention(nn.Module):
    def __init__(self, d_model, n_heads, max_seq_len):
        # W_Q, W_K, W_V: (d_model, d_model) — no bias
        # W_O: (d_model, d_model) — output projection
        # rope: RotaryEmbedding per head
        # causal_mask: upper-triangular -inf matrix
    def forward(self, x, position_ids, past_kv=None, cache=None):
        # Project to Q, K, V: (B, S, d_model) → (B, n_heads, S, d_head)
        # Apply RoPE to Q and K
        # Scaled dot-product: scores = Q @ K.T / sqrt(d_head)
        # Add causal mask: scores + mask (upper triangle = -inf)
        # Softmax: attention probabilities
        # Weighted sum: output = attn_probs @ V
        # Concatenate heads: (B, n_heads, S, d_head) → (B, S, d_model)
        # Output projection: W_O @ output
```

**Verify**: All attention mass should be in the lower triangle (including diagonal). Mass above diagonal should be < 0.01.

### Step 4: MLP Block
Two-layer MLP with ReLU activation (grokking standard).

```python
class MLP(nn.Module):
    def __init__(self, d_model, d_mlp):
        # W_in: (d_model, d_mlp), W_out: (d_mlp, d_model)
    def forward(self, x):
        # hidden = ReLU(W_in(x))
        # output = W_out(hidden)
```

### Step 5: Transformer Block
Combine Attention + MLP with Pre-RMSNorm and residual connections.

```
TransformerBlock:
    x → RMSNorm → Attention → + (residual)
      → RMSNorm → MLP → + (residual)
```

### Step 6: Full Decoder-Only Transformer
```
Embed → (Block × N) → RMSNorm → Unembed
```

## Complete Architecture

| Component | Choice | Rationale |
|-----------|--------|-----------|
| Positional encoding | RoPE | Modern standard, relative position |
| Normalization | Pre-RMSNorm | Scale-invariant, simpler than LayerNorm |
| MLP activation | ReLU | Grokking standard |
| Attention | MHA | One independent head = one circuit component |
| Weight tying | Optional | Common for small models |
| Embedding norm | Optional | Critical for grokking (Nanda canonical) |

## Verification

```python
model = DecoderOnlyTransformer(vocab_size=100, d_model=128, n_layers=4, n_heads=4, max_seq_len=256)
x = torch.randint(0, 100, (4, 32))
logits, cache = model(x, return_cache=True)

assert logits.shape == (4, 32, 100)  # correct output shape

# Gradient flow
loss = torch.nn.functional.cross_entropy(logits.reshape(-1, 100), y.reshape(-1))
loss.backward()
assert all(p.grad is not None for p in model.parameters())

# Causal mask
attn_probs = cache['blocks.0.attn.attn_probs']
upper = torch.triu(torch.ones(32, 32), diagonal=1)
assert (attn_probs[0, 0] * upper).sum() < 0.01

# Generation
generated = model.generate(input_ids, max_new_tokens=20, temperature=0.8, top_k=10)
```

## Solution

The complete implementation lives at `src/models/decoder_only_transformer.py` (355 lines). Architecture:

| Component | Implementation |
|-----------|---------------|
| **RMSNorm** | `RMSNorm` class — scale-only normalization, no mean-centering |
| **RoPE** | `RotaryEmbedding` — rotates Q/K by position angle, `_rotate_half` helper |
| **Attention** | `Attention` — MHA with causal mask, RoPE, optional KV caching, head_mask for ablation |
| **MLP** | `MLP` — ReLU activation, two linear projections, dropout |
| **TransformerBlock** | Pre-RMSNorm → Attn → Residual → Pre-RMSNorm → MLP → Residual |
| **DecoderOnlyTransformer** | Embed → N blocks → ln_final → unembed, 27 cache entries per forward pass |

The cache dict captures activations at every sublayer (`resid_pre`, `ln_attn`, `Q/K/V/probs/out`, `resid_mid`, `ln_mlp`, `mlp_pre`, `mlp_out`, `resid_post`, `hook_ln_final`, `hook_logits`) — enabling QK/OV decomposition, logit lens, and activation patching without architecture changes.

### Verification
```python
# All tests pass in tests/test_decoder_only_transformer.py
# Key assertions:
# - Shape: (B, S, vocab_size) output
# - Gradients flow through all parameters
# - Causal mask: upper triangular attention < 0.01
# - Generation: outputs (B, S+new_tokens) tensor
# - Cache: all 27 expected keys present
```

## Deliverables
- `src/models/decoder_only_transformer.py` with the complete implementation
- Output shape, gradient flow, causal mask, and generation tests
- Verify autoregressive generation produces different outputs for different prompts

## Connection to MI
This model is the analysis vehicle for everything that follows. The hook points you built (`cache` dict) are the foundation for:
- **QK/OV decomposition**: extract Q, K, V, and attention probabilities per head
- **Logit lens**: project residual stream at each layer through the unembedding
- **Activation patching**: replace cached activations with counterfactual values
- **Induction head detection**: find the diagonal+1 attention pattern

**Don't move on until generating works and hook points capture all intermediate activations.**

## Links

- [[04_nlp_and_transformers/notes/qk-ov-circuits]] — the QK/OV abstraction that this transformer's attention heads implement and that you will analyze with the hook points built here.
- [[04_nlp_and_transformers/notes/mi-tooling]] — the MI tooling guide that explains how to use the cache dict and hook points for circuit analysis.

