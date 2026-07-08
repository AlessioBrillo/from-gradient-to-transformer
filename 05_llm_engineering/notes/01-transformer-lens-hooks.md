---
tags: [type/lesson, phase/5]
state: review
created: 2026-07-08
---

# TransformerLens Hooks and Model Instrumentation

## What it is
A hook is a function that fires during a model's forward pass, giving read/write access to internal activations at specific sublayers — the core primitive for mechanistic interpretability.

## Why it exists / what problem it solves
Model internals are black boxes by default: you get logits out, but not the intermediate representations (residual stream states, attention patterns, MLP activations) that actually explain *how* the model computes. Hooks expose those internals without modifying the model's source code, enabling causal intervention, activation patching, and feature extraction.

## How it works

### Registering hooks in PyTorch
PyTorch provides `register_forward_hook` on any `nn.Module`. A hook receives `(module, input, output)`:

```python
activations = {}
def capture(name):
    def hook(module, input, output):
        activations[name] = output.detach()
    return hook

handle = model.blocks[0].attn.register_forward_hook(capture("blocks.0.attn"))
# ... forward pass ...
handle.remove()  # clean up
```

### Our DecoderOnlyTransformer cache
Our model builds the cache dict inline (no `register_forward_hook` needed) — every sublayer writes its activations into a shared dict:

```python
logits, cache = model(x, return_cache=True)
cache["blocks.0.resid_pre"]      # residual stream before block 0
cache["blocks.0.attn.attn_probs"]# attention pattern, block 0
cache["blocks.2.mlp_pre"]        # MLP hidden activations
cache["hook_embed"]              # embedding layer output
cache["hook_ln_final"]           # final layernorm output
cache["hook_logits"]             # unembed output
```

27 hook points per forward pass (5 per block × 4 layers + 3 global + 4 KV pairs).

### TransformerLens convention
[Hook points](https://transformerlens.readthedocs.io/) follow a naming convention: `blocks.{i}.{sublayer}_{position}`. Pre/post hooks allow reading activations *before* and *after* each sublayer. Our cache keys follow this convention: `blocks.{i}.resid_pre`, `blocks.{i}.resid_mid`, `blocks.{i}.resid_post`, `blocks.{i}.attn.attn_probs`, `blocks.{i}.mlp_pre`.

### Causal intervention via hooks
Hooks can *replace* (not just read) activations:

```python
def patching_hook(act, hook):
    act[:, :, :] = source_activations[key]  # overwrite
    return act
```

This is the mechanism behind activation patching — the workhorse of circuit discovery.

## Links
- [[05_llm_engineering/notes/02-deterministic-inference|Deterministic Inference]]
- [[05_llm_engineering/notes/03-activation-harvesting|Activation Harvesting]]
- [[04_nlp_and_transformers/exercises/ex-03-activation-patching|Activation Patching Exercise (Phase 4)]]

## Open questions
- #question How do hooks interact with `torch.compile` and dynamic shapes?
