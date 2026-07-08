---
tags: [phase/3, note, state/review]
MI-forward-link: "Grokking is the single most important training-dynamics phenomenon for MI: it reveals how circuits form, compete, and consolidate. Understanding optimization is essential for reproducing grokking."
---

# Training Dynamics and Grokking — Notes

## Why Grokking Matters for MI
Grokking (Power et al. 2022) is the phenomenon where a model memorizes the training data first (train loss → 0, val loss stays high) and then suddenly generalizes (val loss drops to near zero). This delayed generalization reveals three distinct phases:

1. **Memorization:** Model fits each training example using high-norm, low-weight features
2. **Circuit Formation:** Weight decay penalizes the memorization features; the model discovers lower-norm, generalizing circuits
3. **Cleanup:** Unnecessary features are pruned; only the generalizing circuit remains

## Key Ingredients for Grokking

**Weight decay is the engine.** Without weight decay, the model stays in memorization phase forever. Weight decay creates constant pressure toward lower-norm solutions — and the generalizing circuit (Fourier decomposition for modular addition) has lower norm than memorization.

**AdamW vs Adam:** The decoupled weight decay in AdamW is critical because it applies weight decay *after* the adaptive gradient step, not as part of the L2 regularization. This means weight decay doesn't conflict with the adaptive learning rate.

**Cosine LR schedule:** The cosine schedule (starting high, decaying to near 0) gives the model time to "settle" into the generalizing circuit during the low-LR phase. The high initial LR helps escape memorization local minima.

**Embedding normalization:** Normalizing embedding weights to unit norm (per Nanda et al.) prevents the model from "cheating" by scaling up embedding magnitudes to avoid weight decay pressure.

## Progress Measures
The canonical progress measures for grokking (Nanda et al. 2023):
- **Fourier weight sparsity:** Fraction of Fourier frequencies needed to explain most embedding variance
- **Embedding norm:** Tracks the memorization → circuit transition
- **Attention entropy:** How focused attention patterns are (low entropy = circuit formed)

## The Three Phases in Detail

### Phase 1: Memorization
- Train loss → 0 quickly
- Val loss stays at random chance (~log(P))
- The embedding norm is high: the model assigns large vectors to each input token individually
- Fourier representation is dense: all frequencies have similar weight

### Phase 2: Circuit Formation (The Phase Transition)
- Val loss begins to decrease
- Embedding norm drops sharply
- Fourier frequencies become sparse: only a few frequencies carry significant weight
- Attention patterns become focused (lower entropy)

### Phase 3: Cleanup
- Val accuracy reaches ceiling (~100%)
- Embedding norm stabilizes
- Fourier sparsity is maximal: minimal frequencies needed
- Unnecessary circuit components are pruned

## Practical Takeaways for Reproducing Grokking
1. Weight decay must be ≥ 1.0 (I've been using 1.0, which is correct)
2. Embedding normalization is non-negotiable (I added this in the fix)
3. Cosine schedule should have T_max = epochs (current implementation is correct)
4. Small moduli (P < 30) may need more epochs than expected
5. Multiple seeds (3-5) are essential because grokking timing is seed-sensitive
6. Normalizing embeddings during training prevents the model from escaping weight decay pressure
