---
tags: [type/exercise, phase/5]
skill: Model Instrumentation — hook-based activation capture
created: 2026-07-08
---

# Exercise: Hook-Based Activation Capture

## Goal / skill it demonstrates
Write a function that runs our `DecoderOnlyTransformer` with `return_cache=True`, collects every hook point, and extracts layer-wise activation norms — verifying that all 27 hook points fire with the correct shapes.

```python
import torch
from src.models.decoder_only_transformer import DecoderOnlyTransformer

def capture_all_activations(model, input_ids):
    logits, cache = model(input_ids, return_cache=True)
    return cache

def activation_norms(cache):
    return {k: v.norm(dim=-1).mean().item() for k, v in cache.items()}

model = DecoderOnlyTransformer(vocab_size=100, d_model=64, n_layers=3, n_heads=4)
x = torch.randint(0, 100, (2, 16))

cache = capture_all_activations(model, x)
norms = activation_norms(cache)

expected_keys = {"hook_embed", "hook_ln_final", "hook_logits"}
for i in range(model.n_layers):
    expected_keys.add(f"blocks.{i}.resid_pre")
    expected_keys.add(f"blocks.{i}.resid_mid")
    expected_keys.add(f"blocks.{i}.resid_post")
    expected_keys.add(f"blocks.{i}.ln_attn")
    expected_keys.add(f"blocks.{i}.ln_mlp")
    expected_keys.add(f"blocks.{i}.attn.Q")
    expected_keys.add(f"blocks.{i}.attn.K")
    expected_keys.add(f"blocks.{i}.attn.V")
    expected_keys.add(f"blocks.{i}.attn.attn_probs")
    expected_keys.add(f"blocks.{i}.attn.attn_out")
    expected_keys.add(f"blocks.{i}.mlp_pre")
    expected_keys.add(f"blocks.{i}.mlp_out")
assert set(cache.keys()) == expected_keys, f"Missing keys: {expected_keys - set(cache.keys())}"

print("Exercises passed:")
print(f"  Cache has {len(cache)} hook points (expected {len(expected_keys)})")
print(f"  Activation norms range from {min(norms.values()):.4f} to {max(norms.values()):.4f}")
```

### Bonus: PyTorch hooks (without our cache)
Register a forward hook on `model.blocks[0].attn` and collect the attention probabilities without using `return_cache`:

```python
captured = []
def hook_fn(module, input, output):
    captured.append(output[0].detach())  # attn_out

handle = model.blocks[0].attn.register_forward_hook(hook_fn)
model(x)
handle.remove()
print(f"Captured attn_out shape: {captured[0].shape}")
```

## What I learned doing it
- 27 hook points fire per forward pass: 5 per block (resid_pre, resid_mid, resid_post, ln_attn, ln_mlp) + 4 per block from attn (Q, K, V, attn_probs, attn_out) + 3 from attn (attn_out is already counted) + 3 global (embed, ln_final, logits).
- The cache dict pattern is simpler than `register_forward_hook` for our use case, but native PyTorch hooks work on any model without built-in cache support.

## Linked skill
- [[00_meta/02_skill-tree]] → Model Instrumentation: Hook-based activation capture
