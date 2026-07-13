---
tags: [type/exercise, phase/4, state/review]
---

# Exercise 03 — Activation Patching for Causal Circuit Verification

## Objective
Implement activation patching — the causal intervention that is the gold standard in mechanistic interpretability. Replace activations at specific (layer, position) with counterfactual values and measure the change in model output. This is how you prove that a specific component is causally responsible for a behavior.

## Background
Activation patching (also known as "causal tracing" or "interchange interventions") answers: *"Is this specific activation necessary for the model to produce the correct answer?"*

The procedure:
1. **Clean run**: forward pass on a clean input → logit difference for correct answer
2. **Corrupted run**: forward pass on a corrupted input (e.g., wrong token at a key position) → logit difference drops
3. **Patch**: forward pass with clean activations **replaced** by corrupted activations at a specific (layer, position) → logit difference recovery

A high recovery (patching restores performance) means that component is causally important.

## Implementation

### Step 1: Hook-Based Activation Caching
Use the hook points in `DecoderOnlyTransformer` to cache activations at every layer.

```python
model = DecoderOnlyTransformer(...)
clean_logits, clean_cache = model(clean_input, return_cache=True)
corrupted_logits, corrupted_cache = model(corrupted_input, return_cache=True)
```

Each cache entry has shape `(batch, seq_len, d_model)` at resid_pre/resid_post hooks.

### Step 2: Implement the Patching Function
Replace a cached activation at a specific (layer, position) and measure the effect.

```python
def patch_activation(
    model, clean_input, corrupted_cache, layer, position
) -> float:
    """Replace residual stream at (layer, position) with corrupted value."""

    def patching_hook(activations, hook):
        # activations: (B, S, D)
        activations[:, position, :] = corrupted_cache[hook.name][:, position, :]
        return activations

    with model.hooks([(f"blocks.{layer}.resid_pre", patching_hook)]):
        patched_logits = model(clean_input)

    return logit_diff(patched_logits) / logit_diff(clean_logits)
```

### Step 3: Compute Logit Difference
```python
def logit_diff(logits, correct_answer, wrong_answer):
    return logits[0, -1, correct_answer] - logits[0, -1, wrong_answer]
```

### Step 4: Build a Patching Heatmap
For every (layer, position) combination, measure recovery. The result is a heatmap showing which components are causally important.

```python
results = {}
for layer in range(n_layers):
    for position in range(seq_len):
        recovery = patch_activation(model, clean, corrupted, layer, position)
        results[(layer, position)] = recovery
```

## Task: IOI Circuit Verification
Test the activation patching on an Indirect Object Identification (IOI) task:

**Template**: "When [A] and [B] went to the store, [A] gave a book to" → answer: "[B]"

- **Clean input**: correct IOI sentence
- **Corrupted input**: replace [B] with [A] (same as subject)

Expected result (from Wang et al., 2023):
- **Duplicate-token heads** (early layers): attend to repeated names — high patching effect at positions of A
- **S-inhibition heads** (middle): suppress attention to A — high patching at the second occurrence of A
- **Name-mover heads** (late): move B's information to the output position — high patching at the final position

## Expected Pattern
```
Layer 3 ■■■□□□■■□□□□□□
Layer 2 □□□□□□■■□□□□□□
Layer 1 □□□□□□□□■■■□□□
Layer 0 □□□□□□□□□□□□□□□
         ↑position of first A    ↑position of B    ↑final answer position
```

## Deliverables
- Patching heatmap (layer × position) for the IOI task
- Top-5 most important (layer, position) pairs with recovery values
- One-sentence interpretation of the circuit: "The model uses heads at layers X-X for duplicate-token detection, Y for S-inhibition, and Z for name-moving"

## Verification
```python
# A head that is causally important should have high patching recovery
assert results[(important_layer, important_pos)] > 0.7

# A head that is not part of the circuit should have low recovery
assert results[(unimportant_layer, unimportant_pos)] < 0.2
```

## Reference
- Wang et al., "Interpretability in the Wild: a Circuit for IOI in GPT-2 small," ICLR 2023
- Nanda's TransformerLens demo: activation patching notebook
- Zhang & Nanda, "Interchange Interventions," 2023

## Links

- [[04_nlp_and_transformers/notes/activation-patching]] — the theory note on activation patching that this exercise implements in code.
- [[04_nlp_and_transformers/notes/path-patching]] — path patching extends single-node patching to edge-level interventions; the natural next step after mastering this exercise.

