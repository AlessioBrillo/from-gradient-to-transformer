# Proof — Logit Lens: Projecting Residual Stream to Vocabulary

## The Core Idea

The logit lens (nostalgebraist, 2020) is the simplest and most revealing tool in mechanistic interpretability: **project the residual stream at any layer through the unembedding matrix to see the model's partial predictions.**

Because the unembedding maps $d_{model}$-dimensional vectors to vocabulary logits:
$$\text{logits} = W_{unembed} \cdot x_{resid} + b_{unembed}$$

Any vector in the residual stream can be interpreted as the model's "best guess" at that point.

## Why It Works

The residual stream is additive:
$$x_{resid}^l = x_{embed} + \sum_{i=0}^{l} (\Delta_{attn}^i + \Delta_{mlp}^i)$$

Since the unembedding is a linear map, the predicted logits at layer $l$ are:
$$\text{logits}^l = W_{unembed} \cdot x_{embed} + \sum_{i=0}^{l} W_{unembed} \cdot \Delta^i$$

Each term $W_{unembed} \cdot \Delta^i$ is the contribution of layer $i$ to the final prediction.

## Implementation

```python
@torch.no_grad()
def logit_lens(model, x):
    """Apply logit lens at every layer."""
    _, cache = model(x, return_cache=True)
    unembed = model.unembed.weight

    predictions = {}
    for key, value in cache.items():
        if "resid_pre" in key or "resid_post" in key:
            # value: (B, S, d_model), project last position
            logits = value[:, -1, :] @ unembed.T
            predictions[key] = logits

    return predictions
```

## What You Can See

### 1. Prediction Refinement
At early layers, the logit lens often predicts high-frequency tokens (common words, punctuation). As information flows through later layers, the prediction sharpens toward the correct answer. This reveals the model's "reasoning chain."

### 2. Attention Head Contributions
By zeroing a specific head's output and observing the logit lens change, you measure that head's contribution to the final prediction:
```python
clean_logits = trace_with_logit_lens(model, clean_input)
ablated_logits = trace_with_logit_lens(model, ablated_input)
diff = clean_logits - ablated_logits  # the head's contribution
```

### 3. Grokking Fourier Structure
For grokking on modular addition: applying the logit lens to the residual stream at each layer shows how the model gradually separates the correct answer's logit from the others. In the Fourier basis, the logit lens reveals which frequencies are being constructed at each layer.

### 4. Induction Head Copying
At position `i` where `token[i] == token[i - k]`, the logit lens at the second layer often shows increased probability for `token[i - k + 1]` — the induction head copying mechanism in action.

## Limitations
- The logit lens is a **linear projection** — it can miss information that requires multiple layers of nonlinear processing to decode
- LayerNorm scaling can distort the projection (mitigated by `fold_layer_norm` in TransformerLens)
- Zero ablation of attention is not a clean counterfactual (the model may compensate)

## Verification
```python
# For a trained model on known task:
model = DecoderOnlyTransformer(...)
logits = logit_lens(model, test_input)

# The correct answer's logit should increase (or at least not decrease)
# as we move through layers
layer_order = sorted(logits.keys())
for i in range(len(layer_order) - 1):
    earlier = logits[layer_order[i]][0, correct_answer]
    later = logits[layer_order[i+1]][0, correct_answer]
    assert later >= earlier - 0.1, (
        f"Logit for correct answer dropped at {layer_order[i+1]}"
    )
```

## Reference
- nostalgebraist, "interpreting GPT: the logit lens," LessWrong, 2020
- Nanda's TransformerLens demo: `LogitLens` utility

**I have reconstructed this technique from memory without referring to notes.**
