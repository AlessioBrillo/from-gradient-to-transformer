---
tags: [type/exercise, phase/5]
skill: Model Instrumentation — activation harvesting at scale
created: 2026-07-08
---

# Exercise: Activation Harvesting Across Prompts

## Goal / skill it demonstrates
Harvest residual stream activations from a set of prompts using `return_cache`, store them in a compact format, verify deterministic reproducibility, and compute per-neuron firing rates in the MLP.

```python
import torch
from src.models.decoder_only_transformer import DecoderOnlyTransformer

def set_seed(seed=42):
    torch.manual_seed(seed)

def harvest_layer(model, prompts, layer_idx=0):
    """Harvest resid_pre activations for a specific layer across all prompts."""
    results = {}
    set_seed(42)
    for i, p in enumerate(prompts):
        logits, cache = model(p, return_cache=True)
        key = f"blocks.{layer_idx}.resid_pre"
        results[i] = cache[key]  # (1, seq_len, d_model)
    return results

model = DecoderOnlyTransformer(vocab_size=50, d_model=32, n_layers=2, n_heads=2)

prompts = torch.randint(0, 50, (10, 8))

harvest = harvest_layer(model, prompts, layer_idx=0)

residual_norms = {k: v.norm(dim=-1).mean().item() for k, v in harvest.items()}
print(f"Layer 0 resid_pre norms: min={min(residual_norms.values()):.4f}, max={max(residual_norms.values()):.4f}")

# Verify determinism: re-run and compare
harvest2 = harvest_layer(model, prompts, layer_idx=0)
assert all(torch.allclose(harvest[i], harvest2[i]) for i in range(len(prompts))), \
    "Deterministic harvest failed!"
print("Determinism verified: identical activations across two runs")

# MLP neuron firing rates
mlp_cache = {}
def harvest_mlp(model, prompts):
    set_seed(42)
    rates = []
    for p in prompts:
        _, cache = model(p, return_cache=True)
        mlp_pre = cache["blocks.0.mlp_pre"]  # (1, seq_len, d_mlp)
        rate = (mlp_pre > 0).float().mean().item()
        rates.append(rate)
    return rates

rates = harvest_mlp(model, prompts)
print(f"MLP layer 0 average firing rate: {sum(rates)/len(rates):.2%}")
```

## What I learned doing it
- Determinism gives bit-exact activation harvests across runs — critical for reproducible analysis.
- MLP firing rates (ReLU sparsity) depend on the input distribution.
- Storage scales as batch × seq_len × d_model; collecting a single layer across 10 prompts of seq_len=8, d_model=32 produces ~10 KB — trivial. At GPT-2 scale (100K prompts, seq_len=1024, d_model=768) it's ~150 GB per layer.

## Linked skill
- [[00_meta/02_skill-tree]] → Model Instrumentation: Activation harvesting at scale
