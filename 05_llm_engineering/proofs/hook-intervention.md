---
tags: [type/proof, phase/5, state/review]
created: 2026-07-08
---

# Proof to myself: Hook Intervention Changes Model Output

**Rule:** reconstructed without looking at notes.

## What I needed to demonstrate
That intervening on a specific layer's residual stream (via hooks) changes the model's output in a predictable direction, proving that layer causally contributes to the final prediction.

## What I produced from memory

```python
import torch
from src.models.decoder_only_transformer import DecoderOnlyTransformer

model = DecoderOnlyTransformer(vocab_size=50, d_model=32, n_layers=2, n_heads=2)
x = torch.randint(0, 50, (1, 8))

# Baseline: normal forward pass
logits_clean, cache_clean = model(x, return_cache=True)
pred_clean = logits_clean[:, -1, :].argmax(dim=-1)

# Intervention: zero out block 0's resid_post via a hook
def zero_out_hook(module, input, output):
    output[:, :, :] = 0.0  # zero the residual stream
    return output

handle = model.blocks[0].register_forward_hook(zero_out_hook)
logits_ablated, _ = model(x, return_cache=False)
handle.remove()
pred_ablated = logits_ablated[:, -1, :].argmax(dim=-1)

# Compare
changed = (pred_clean != pred_ablated).item()
print(f"Clean prediction: {pred_clean.item()}")
print(f"Ablated prediction: {pred_ablated.item()}")
print(f"Output changed: {changed}")
```

The output differs when block 0 contributes non-trivially to the final prediction. This demonstrates that intervening via hooks is a valid causal intervention: the model's behavior changes because the internal computation was disrupted, not because the intervention itself is an artifact.

## Outcome
- [x] Passed → check the skill in [[00_meta/02_skill-tree]]
- [ ] Retry needed (what was missing): ...

## See also
- [[05_llm_engineering/notes/01-transformer-lens-hooks|TransformerLens Hooks]] — the lesson on `register_forward_hook` that supplies the write path this proof exercises
- [[04_nlp_and_transformers/proofs/residual-stream-communication-channel|Residual Stream as a Communication Channel]] — why zeroing resid_post at block 0 propagates all the way to the final prediction
- [[05_llm_engineering/proofs/activation-patching|Activation Patching]] — the same hook machinery used to swap activations between two runs instead of erasing them
