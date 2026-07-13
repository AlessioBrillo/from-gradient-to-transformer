---
tags: [type/exercise, phase/4, state/review]
---

# Exercise 02 — Detect Induction Heads by Attention Pattern

## Objective
Train a 2-layer attention-only transformer on repeated-token sequences, then identify induction heads by their characteristic attention pattern: `[A][B]...[A]` → attends to the position after the previous `[A]` to predict `[B]`. Confirm causally via head ablation.

## Background
Induction heads (Olsson, Elhage, Nanda et al., 2022) are the mechanism behind in-context learning. An induction head at layer L performs:
1. **Prefix-matching**: attend to the previous occurrence of the current token (QK circuit)
2. **Copying**: copy the token that followed that previous occurrence (OV circuit)

The signature is the **diagonal+1** attention pattern: from position `i`, strong attention to position `i - (prefix_len - 1)` when the token at `i` matches the token at `i - prefix_len`.

## Implementation

### Step 1: Generate Repeated-Prefix Data
```
Sequence: [A₀, A₁, ..., Aₖ] [A₀, A₁, ..., Aₖ] ...
```
Half the sequence is a random prefix; the rest repeats it. For next-token prediction at the boundary, when A₀ reappears, the correct next token is A₁ — the induction head's job.

### Step 2: Train Attention-Only Transformer
```
2 layers, 4 heads/layer, d_model=64
AdamW, lr=1e-3, weight_decay=0.1
1000 epochs
```

### Step 3: Detect Induction Heads
For each head, compute the diagonal+1 mass:
```python
# attn_probs: (B, n_heads, S, S)
diag = attn_probs[:, :, 1:, :-1].diagonal(dim1=-2, dim2=-1)
induction_score = diag.mean(dim=(0, -1))  # mean over batch and positions
```
A head is an induction head if `induction_score > 0.3`.

### Step 4: Causal Ablation
Zero the output of each candidate induction head and measure the accuracy drop. If the head is causally important, accuracy should decrease significantly.

```python
def zero_head_hook(module, input, output):
    # Zero the output of the specific head
    output_view = output.view(B, S, n_heads, d_head)
    output_view[:, :, head_idx, :] = 0.0
    return output_view.view(B, S, D)
```

## Expected Results
- After ~500-1000 epochs, 1-2 induction heads emerge in layer 1 (the second layer)
- The diagonal+1 pattern is clearly visible in the attention heatmap
- Ablating an induction head drops accuracy by 10-30% on validation data
- The "loss bump" during training correlates with induction head formation

## Deliverables
- Trained model with validation accuracy > 30% (significantly above random)
- Attention pattern plots for each detected induction head
- Ablation table: accuracy before/after for each head
- Logit-lens analysis showing the induction head's output at the boundary position

## Verification
```python
induction_heads, patterns = analyze_induction_heads(model, val_loader)
for layer_idx, heads in enumerate(induction_heads):
    print(f"Layer {layer_idx}: {len(heads)} induction heads: {heads}")

# Causal ablation
for layer, head in induction_heads:
    ablated_acc = causal_ablation(model, val_loader, layer, head)
    print(f"Ablation L{layer}H{head}: {full_acc:.4f} → {ablated_acc:.4f}")
```

## Reference
Olsson, Elhage, Nanda et al., "In-context Learning and Induction Heads," Transformer Circuits Thread (Anthropic), 2022.

## Links

- [[04_nlp_and_transformers/notes/induction-heads]] — the theory note on induction head formation, prefix-matching, and the diagonal+1 attention pattern.
- [[04_nlp_and_transformers/notes/activation-patching]] — the causal intervention technique used in this exercise to confirm that detected induction heads are causally necessary.

