---
tags: [type/proof, phase/4, state/review]
---

# Proof — The Residual Stream as a Communication Channel

The residual stream is the central highway of a transformer. Every layer reads from it and writes to it. Understanding this is essential for all MI work.

## The Architecture

A transformer block computes:
$$x_{out} = x_{in} + Attention(x_{in}) + MLP(x_{in})$$

Each layer:
1. **Reads** from the residual stream ($x_{in}$)
2. **Computes** a delta ($\Delta_{attn} + \Delta_{mlp}$)
3. **Writes** the delta back to the same stream

This means the final representation before the unembed is:
$$x_{final} = x_{embed} + \sum_{l=0}^{L-1} (\Delta_{attn}^l + \Delta_{mlp}^l)$$

## Key Properties

### 1. Additive Updates
The residual stream is a running sum of all layer contributions. Each layer adds its output to the stream — nothing is overwritten. This makes the stream a **direct sum decomposition** of the model's computation.

### 2. Shared Vector Space
Every layer reads from and writes to the *same* $d_{model}$-dimensional space. This means:
- Different layers can communicate by writing to aligned directions
- A circuit can span multiple layers if they agree on the encoding
- The unembedding reads from this shared space to produce logits

### 3. Logit Lens
Because the residual stream is a shared vector space, we can project *any intermediate state* through the unembedding to see the model's "partial predictions" at each layer:
$$\text{logits}_l = x_{resid}^l \cdot W_{unembed}$$

This is the logit lens — a direct window into the model's step-by-step reasoning.

### 4. Low-Rank Updates
Each attention head writes a rank-$d_{head}$ update to the residual stream (since it's the sum of $d_{head}$-dimensional vectors per head). This limits how much information a single head can contribute.

## Code Verification

```python
def trace_residual_stream(model, x):
    """Show how predictions evolve through layers."""

    def hook_fn(activations, hook):
        resid = activations[0, -1, :]  # last position
        logits = resid @ model.unembed.weight.T
        layer = int(hook.name.split(".")[1])
        print(f"Layer {layer} resid -> top prediction: {logits.argmax().item()}")

    with model.hooks(fwd_hooks=[
        (lambda name: "resid_pre" in name, hook_fn)
    ]):
        model(x)
```

## Connection to MI
- **Activation patching**: replace the residual stream at a specific (layer, position) with a counterfactual value and measure the effect. Because the stream is additive, the patch propagates forward to all downstream layers.
- **Circuit discovery**: a circuit is a subset of the computational graph that, when all other edges are zeroed, still produces the correct output. The residual stream's additivity makes this tractable.
- **TransformerLens caching**: `ActivationCache` stores residual stream states at every layer, enabling fast patching without re-running.

**I can explain the residual stream metaphor to a non-technical colleague: *"Think of the residual stream as a shared whiteboard. Each layer reads what's written, adds its own notes, and passes the whiteboard to the next layer."***

**I have reconstructed this analysis from memory without referring to notes.**

## Links

- [[04_nlp_and_transformers/notes/qk-ov-circuits]] — the QK/OV circuits that write to and read from the residual stream, making the additive update concrete.
- [[04_nlp_and_transformers/proofs/logit-lens]] — the logit lens technique that exploits the shared vector space to read partial predictions at every layer.
