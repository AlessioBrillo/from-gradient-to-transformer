---
tags: [phase/4, note, state/review, research/experiment]
MI-core: "Induction heads are the mechanism behind in-context learning. They are the most well-understood circuit in mechanistic interpretability."
---

# Induction Heads — The Mechanism of In-Context Learning

## Definition (Olsson et al. 2022)
An **induction head** is an attention head that performs the operation:
`[A][B]...[A] → [B]`

That is, when it sees token A at a later position, it attends to the token *after* the previous occurrence of A, predicting that B will follow again.

## The Induction Head Mechanism
An induction head requires two sub-mechanisms:

1. **Prefix-matching:** A head that attends from the current token to the previous occurrence of the same token (often a previous-token head or a duplicate-token head)
2. **Copying:** A head that copies the token after the matched position

In a 2-layer model:
- Layer 1: previous-token head attends to the position just before each token
- Layer 2: induction head uses the Layer 1 output to match prefixes and copy the correct continuation

## The Characteristic Attention Pattern
An induction head's attention pattern shows a distinctive diagonal-offset:
- Strong attention from position i to position i-1 (or more generally, to the position after the previous occurrence of the current token)
- Visualized as a diagonal band in the attention pattern heatmap

## Training Dynamics
Induction heads emerge partway through training, marked by:
- A sudden drop in validation loss (the "bump" or phase change)
- An increase in attention-pattern structure (from diffuse to diagonal)
- The increase of a specific progress measure: "induction-head score" = attention mass on the diagonal+1 offset

## Verification via Ablation
To causally verify an induction head:
1. Locate heads with the characteristic diagonal attention pattern
2. Ablate that head (zero its output)
3. Measure the drop in performance on repeated-token sequences
4. If performance drops significantly, the head is causally important

## Why This Is the Most Robust MI Result
Induction heads are the most reproduced result in MI because:
- They emerge reliably in small (2-layer) models
- The pattern is visually unmistakable
- Ablation produces clear, measurable effects
- The mechanism is simple enough to fully understand
