---
tags: [type/lesson, phase/5]
state: review
created: 2026-07-08
---

# Activation Harvesting at Scale

## What it is
Activation harvesting is the process of collecting internal activations (residual stream states, attention patterns, neuron activations) across many prompts to build a dataset for downstream analysis — feature visualization, sparse autoencoders, or circuit discovery.

## Why it exists / what problem it solves
A single forward pass gives you a snapshot of activations for one input. But understanding a model's behavior requires observing how activations vary across many inputs: Which neurons fire for "doctor" vs. "nurse"? Which attention heads attend to subject tokens across contexts? Harvesting collects these at scale.

## How it works

### Batching
Collect activations over multiple prompts efficiently using batch inference:

```python
def harvest_activations(model, prompts, batch_size=8):
    all_caches = []
    for i in range(0, len(prompts), batch_size):
        batch = prompts[i:i+batch_size]
        tokens = tokenizer(batch, padding=True, return_tensors="pt")
        with torch.no_grad():
            _, cache = model(tokens["input_ids"], return_cache=True)
        all_caches.append(cache)
    return all_caches
```

### Storage strategy
Activations are large (batch × seq_len × d_model × n_layers). Storage strategies by ascending cost:

1. **Compute on the fly** — cheapest for memory, most expensive CPU time. Re-run the model each time you need activations.
2. **Per-layer caching** — store only the layers you need for a given analysis.
3. **Disk-backed buffers** — memory-map activations to disk using `numpy.memmap` or `torch.save` per sample.
4. **Compressed formats** — quantize to float16 or int8, or use sparse representations when activations are predominantly zero (e.g., ReLU MLPs).

### Selective harvesting
Don't collect everything — specify hook points:

```python
def harvest_selected(model, x, hooks=["blocks.0.attn.attn_probs", "blocks.2.mlp_pre"]):
    captured = {}
    handles = []
    for name in hooks:
        def make_hook(n):
            def hook(module, input, output):
                captured[n] = output.detach().cpu()
            return hook
        # resolve module by name
        module = dict(model.named_modules())[name]
        handles.append(module.register_forward_hook(make_hook(name)))
    model(x)
    for h in handles: h.remove()
    return captured
```

### Memory management
For GPT-2 scale (12 layers, 768-dim): a single sequence of 1024 tokens produces ~12 MB of activations in float32. Across 100K prompts that's 1.2 TB. Practical strategies:
- Harvest in passes (one layer at a time)
- Use float16 storage
- Build streaming datasets (harvest → analyze → discard)

## Links
- [[05_llm_engineering/notes/01-transformer-lens-hooks|TransformerLens Hooks]]
- [[05_llm_engineering/notes/02-deterministic-inference|Deterministic Inference]]
- [[05_llm_engineering/exercises/ex-02-activation-harvesting|Activation Harvesting Exercise]]

## Open questions
- #question What compression ratios can we achieve with SAE-style feature sparsity?
