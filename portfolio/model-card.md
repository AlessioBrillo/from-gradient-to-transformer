---
tags: [portfolio, model-card]
---

# Model Card — Interpretability Micro-Transformer

## Model Overview

- **Name**: micro-transformer (from-gradient-to-transformer)
- **Architecture**: Decoder-only Transformer (designed for interpretability)
- **Parameters**: ~1–50M (configuration varies by experiment)
- **Primary variants**:
  - 1-layer, 4-head, d_model=128, d_mlp=512 (grokking config, per Nanda et al. 2023)
  - 2-layer, attention-only, ~1–4 heads/layer (induction head config, per Olsson et al. 2022)
- **Tokenizer**: BPE (for natural-text experiments); character-level / token-id (for algorithmic experiments)
- **Language**: English (primary); trained on algorithmic datasets (modular addition, repeated tokens, synthetic IOI)
- **License**: MIT

## Intended Use

Research and educational demonstration of mechanistic interpretability techniques — reverse-engineering the algorithms learned by small transformers. Not intended for production use.

## Training Data (by experiment)

| Experiment | Dataset | Description |
|------------|---------|-------------|
| Rung 1 — Induction heads | Repeated random tokens | Sequences of random tokens from a small vocabulary, designed to induce prefix-matching behavior |
| Rung 2 — Grokking ★ | Modular addition pairs | Equation (a + b) mod P = c for all pairs; train/test split by hold-out modulus values |
| Rung 3 — Superposition | Synthetic sparse features | Randomly activated features with controlled sparsity; ground-truth features known |
| Rung 4 — Circuit patching | Synthetic IOI / task-specific templates | Controlled templates (e.g., "When [A] and [B] went to the store, [A] gave a book to") |
| Rung 5 — SAE | Residual stream activations | Harvested from forward passes of the capstone model on evaluation prompts |

## Factors

- **Scale limitation**: Findings are on micro-scale models (1–50M params). Circuits in larger models may be qualitatively different.
- **Task specificity**: Algorithmic tasks (modular addition) admit complete reverse-engineering; natural-language circuits may be more complex and less faithful.
- **Method limitations**: Attribution patching is a linear approximation; activation patching can mislead through layernorm denominator effects; SAE features can be illusory (see Makelov, Lange & Nanda 2023).

## Evaluation

Evaluation in MI is different from standard ML. Metrics are causal and structural:

| Experiment | Primary Metric | Supporting Metrics |
|------------|---------------|-------------------|
| Induction heads | Attention-pattern entropy | Logit-lens projection, ablation logit diff |
| Grokking | Generalization accuracy | Fourier weight sparsity, progress measures |
| Superposition | Fraction of features recovered | Feature geometry (mean cosine similarity) |
| Circuit patching | Logit-difference recovery | Faithfulness, minimality, completeness |
| SAE | Loss recovered (L0 vs MSE) | Interpretability score, dead feature rate |

All results reported as mean ± std over ≥3 seeds where applicable.

## Limitations

- Micro-scale models — capabilities do not match large-scale LLMs.
- Algorithmic tasks are cleaner than natural language; circuits found may not transfer.
- Single architecture family (decoder-only Transformer with ReLU/GELU MLP).
- SAE interpretability is human-judged and inherently subjective.
- See the mini-paper's limitations section for a full discussion.
