---
tags: [type/proof, phase/5]
created: 2026-07-08
---

# Proof to myself: Activation Patching Localizes Model Behavior

**Rule:** reconstructed without looking at notes.

## What I needed to demonstrate
Replacing a specific layer's activations from one forward pass with activations from another pass (with different input) changes the output in a way that localizes which layer encodes which information.

## What I produced from memory

```python
import torch
from src.models.decoder_only_transformer import DecoderOnlyTransformer

model = DecoderOnlyTransformer(vocab_size=50, d_model=32, n_layers=2, n_heads=2)
x_a = torch.randint(0, 50, (1, 8))
x_b = torch.randint(0, 50, (1, 8))

# Forward pass for prompt A (collect activations)
logits_a, cache_a = model(x_a, return_cache=True)
pred_a = logits_a[:, -1, :].argmax(dim=-1)

# Forward pass for prompt B (collect activations)
logits_b, cache_b = model(x_b, return_cache=True)
pred_b = logits_b[:, -1, :].argmax(dim=-1)

# Patch: replace block 0's resid_post from A with B's
activation_to_patch = cache_b["blocks.0.resid_post"]  # B's activation

def patching_hook(module, input, output):
    output[:, :, :] = activation_to_patch  # overwrite with B's
    return output

handle = model.blocks[0].register_forward_hook(patching_hook)
logits_patched, _ = model(x_a, return_cache=False)
handle.remove()
pred_patched = logits_patched[:, -1, :].argmax(dim=-1)

# Patch another layer
activation_to_patch_2 = cache_b["blocks.1.resid_post"]
def patching_hook_2(module, input, output):
    output[:, :, :] = activation_to_patch_2
    return output

handle2 = model.blocks[1].register_forward_hook(patching_hook_2)
logits_patched_2, _ = model(x_a, return_cache=False)
handle2.remove()
pred_patched_2 = logits_patched_2[:, -1, :].argmax(dim=-1)

print(f"Prompt A prediction: {pred_a.item()}")
print(f"Prompt B prediction: {pred_b.item()}")
print(f"Patch block 0 → A: {pred_patched.item()}")
print(f"Patch block 1 → A: {pred_patched_2.item()}")

# If patching block 0 flips the prediction toward B's answer,
# then block 0 causally encodes the information that differs
patch_flipped_0 = (pred_patched.item() == pred_b.item())
patch_flipped_1 = (pred_patched_2.item() == pred_b.item())
print(f"Block 0 patch flipped to B: {patch_flipped_0}")
print(f"Block 1 patch flipped to B: {patch_flipped_1}")
```

This is the core method behind circuit discovery in TransformerLens (Wang et al., 2022) — activation patching via hooks localizes which layers and heads encode specific behaviors by measuring how much the patched output shifts toward the donor input's answer.

## Outcome
- [x] Passed → check the skill in [[00_meta/02_skill-tree]]
- [ ] Retry needed (what was missing): ...
