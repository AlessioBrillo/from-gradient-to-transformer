---
tags: [type/proof, phase/4, state/review]
---

# Gate Proof: Complete Circuit Analysis Pipeline

## Claim
I can take a trained transformer, identify specific circuits (induction heads, QK/OV decomposition), causally validate them with activation/path patching, and use tooling (TransformerLens, SAELens) to scale the analysis.

## Proof: Induction Head Circuit — End to End

### Step 1: Load and probe
```python
from transformer_lens import HookedTransformer
model = HookedTransformer.from_pretrained("gpt2-small")
```

### Step 2: Run with cache
```python
tokens = model.to_tokens("The cat sat on the [COMPANY] mat")
logits, cache = model.run_with_cache(tokens)
```

### Step 3: Detect induction heads
Compute diagonal-offset-1 attention mass per head. Heads where diag+1 > 0.4 are candidates.
In GPT-2 small: L4H11, L5H5, L5H8, L6H9 are known induction heads.

### Step 4: QK/OV decomposition
For each induction head, decompose into the QK circuit (which tokens it attends to) and OV circuit (what it copies to the output).
- QK: `W_QK = W_Q @ W_K.T` — shows the similarity structure that drives attention
- OV: `W_OV = W_V @ W_O` — shows the embedding-space transformation

### Step 5: Activation patching
```python
model.act_patch(
    tokens, corrupted_tokens,
    activation_name="blocks.4.hook_q",
    patch_type="mlp",
)
```
Measure logit difference recovery. Confirms causal role of each head.

### Step 6: Path patching (if needed)
For a suspected edge L4H11 → L6H9, isolate the path:
- Run corrupted forward with L4H11 output replaced by clean (enables source)
- All other activations remain corrupted
- Measure how much L6H9's effect is restored

### Step 7: SAE feature analysis
```python
from sae_lens import SAE
sae = SAE.from_pretrained("gpt2-small-res-jb", "blocks.4.hook_resid_pre")
features = sae.encode(cache["blocks.4.hook_resid_pre"])
```
Which features activate on the repeated token? Which features are causally necessary for induction?

### Step 8: Document the circuit

```
Circuit: Induction Head (GPT-2 small)
├── L4H7: Previous token head (QK attends to pos-1)
├── L4H11: Induction head (QK attends to one-before-previous, OV copies)
├── L5H5: Induction head (same pattern)
├── L5H8: Induction head (same pattern)
└── L6H9: Induction head (same pattern)

Features (SAE Latent):
- Latent 1247: "token is repeated" detector
- Latent 8912: "copy from position -1" copier
- Latent 3301: "completes the repeated pattern" predictor
```

## What I learned
- Induction heads are the simplest complete circuit in transformers — they involve exactly one attention mechanism per layer
- QK/OV decomposition is the lens; activation patching is the hammer; together they let you read any circuit
- SAEs on real activations reveal feature-level structure that head-level analysis misses (multiple features per head)
- TransformerLens makes the analysis 10× faster than building hooks from scratch

## References
- Olsson et al., *In-context Learning and Induction Heads* (2022)
- Wang et al., *Interpretability in the Wild: a Circuit for IOI in GPT-2 Small* (2023)
- Bricken et al., *Towards Monosemanticity* (2023)
- Conmy et al., *Automated Circuit Discovery* (2023)
