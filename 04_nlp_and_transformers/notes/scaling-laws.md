---
tags: [type/lesson, phase/4, state/review]
---

# Scaling Laws — Kaplan & Chinchilla

## The core finding
Transformer loss scales as a **power law** with compute, data, and parameters — independent of model shape (depth/width/heads). More of any resource helps, but there is an optimal allocation.

## Kaplan et al. (2020) — OpenAI
```python
L(N, D) ≈ (N_c / N)^α_N + (D_c / D)^α_D + L_∞
```
- α_N ≈ 0.076, α_D ≈ 0.103 (loss scales slower with params than data)
- **Key result**: models are undertrained — we should train smaller models on more data
- **Compute-optimal**: 10× more compute → 5.5× more params, 1.8× more data
- **No overfitting**: even at extreme param/data ratios, test loss keeps improving

## Chinchilla (2022) — DeepMind
- Retested scaling laws on a larger sweep
- **Key revision**: Kaplan's optimal was wrong by ~4× — models should be **much smaller** given compute budget
- **Chinchilla optimal**: for compute budget C, optimal N* = C / (6 * D*), where D* ≈ 20 × N*
- Chinchilla 70B outperforms GPT-3 175B at 1/6 the compute

## Practical implications

| Budget | Kaplan optimal | Chinchilla optimal |
|--------|---------------|-------------------|
| 1e21 FLOP | 83B params / 190B tokens | 17B params / 940B tokens |
| 1e22 FLOP | 480B params / 370B tokens | 130B params / 4.1T tokens |
| 1e23 FLOP | 2.8T params / 720B tokens | 1.0T params / 18T tokens |

## Current best practice
- **Llama 1**: trained on 1.0–1.4T tokens (under-Chinchilla by ~2×)
- **Llama 3**: 8B on 15T tokens, 70B on 15T tokens (over-Chinchilla for 8B, close for 70B)
- **Training recipe**: weight decay ~0.1, AdamW, cosine LR, gradient clipping 1.0

## MI forward link
Scaling laws have direct implications for mechanistic interpretability: as models scale, individual neurons become more monosemantic (Bricken et al., 2023). Larger models learn more structured features per unit of compute, which means circuit discovery scales *better* than linearly — the returns to interpretability effort increase with model size.

## References
- Kaplan et al., *Scaling Laws for Neural Language Models* (2020)
- Hoffmann et al., *Training Compute-Optimal Large Language Models* (Chinchilla, 2022)
- Bricken et al., *Towards Monosemanticity: Decomposing Language Models With Dictionary Learning* (2023)
