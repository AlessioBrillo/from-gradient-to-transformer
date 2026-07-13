---
tags: [phase/4, note, state/review, research/experiment]
MI-core: "Activation patching is the causal intervention tool that lets us test hypotheses about circuit components."
---

# Activation Patching — Causal Intervention for Circuit Discovery

## The Core Idea
Activation patching answers: "Is this specific component (head, MLP neuron, layer) causally important for this specific behavior?"

**Setup:**
1. Run the model on a **clean** input (produces correct output)
2. Run the model on a **corrupted** input (produces wrong output)
3. For each component, replace its activation in the clean run with its activation from the corrupted run
4. Measure how much the output moves from clean → corrupted

If patching a component reverts the output to corrupted → that component is causally important.

## Mathematical Formulation
Let f(x) be the model's output on input x. Let aᵢ(x) be the activation of component i on input x.

The patching effect for component i is:
$$Effect_i = \frac{metric(f(clean)) - metric(f(clean \ with \ a_i(patch)))}{metric(f(clean)) - metric(f(patch))}$$

An effect of 1.0 means: patching this component fully recovers the corrupted behavior (component is entirely responsible). An effect of 0.0 means: this component doesn't matter for the behavior.

## Variants

### Activation Patching (Direct)
Replace the hidden state at a specific layer/position with the corrupted state. The most direct intervention.

### Path Patching
Trace the effect along a specific edge in the computational graph. More targeted than activation patching.

### Attribution Patching (AtP)
Use gradients to approximate the effect of patching without running multiple forward passes. Much faster but makes a linear approximation that can be inaccurate for large activations (e.g., the residual stream).

## Practical Implementation (with TransformerLens)

```python
from transformer_lens import HookedTransformer
import torch

model = HookedTransformer.from_pretrained("gpt2-small")

clean_tokens = model.to_tokens("When Alice and Bob went to the store, Alice gave a book to")
corrupted_tokens = model.to_tokens("When Alice and Bob went to the store, Bob gave a book to")

# Run clean and corrupted forward passes, caching activations
clean_logits, clean_cache = model.run_with_cache(clean_tokens)
corrupted_logits, corrupted_cache = model.run_with_cache(corrupted_tokens)

# Patch a specific residual stream position
def patch_hook(resid_post, hook, position=8):
    resid_post[:, position, :] = corrupted_cache[hook.name][:, position, :]
    return resid_post

# Run with hook
patched_logits = model.run_with_hooks(
    clean_tokens,
    fwd_hooks=[(utils.get_act_name("resid_post", 6), patch_hook)]
)
```

## Common Pitfalls
1. **LayerNorm denominator effect:** Changing a large activation at one position affects the LayerNorm scaling at ALL positions. This can make patching seem important when it's actually a normalization artifact.
2. **Subspace projection illusions:** Patching in the residual stream may only affect a small subspace that matters for the behavior, but the effect looks large if that subspace has high variance.
3. **Linear approximation failure:** AtP can miss important components whose effect is non-linear.

## Honest Caveats (Document These)
- "Attribution patching is a flawed linear approximation (bad for large activations like the residual stream)"
- "Activation patching can mislead via the layernorm denominator and subspace projection illusions"
- "Circuit faithfulness metrics are not robust" (Heimersheim & Janiak 2024)

## Links

- [[04_nlp_and_transformers/notes/induction-heads]]
- [[04_nlp_and_transformers/notes/path-patching]]
- [[04_nlp_and_transformers/notes/mi-tooling]]
