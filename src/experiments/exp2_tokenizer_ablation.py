#!/usr/bin/env python3
"""Experiment 2 — Tokenizer ablation on micro-LM pretraining.

Train two identical decoder-only models (~10-50M params) on the same Italian
corpus, differing only in tokenizer. Compare validation bits-per-byte
(tokenizer-fair) and tokens-to-convergence.

Usage:
    python -m src.experiments.exp2_tokenizer_ablation

Output:
    - figures/exp2_tokenizer_ablation.png
    - Console: bits-per-byte and tokens-to-convergence for each tokenizer
"""

from src.reproducibility import set_seed

set_seed(42)


def main() -> None:
    print("=" * 60)
    print("Exp 2 — Tokenizer Ablation on Micro-LM Pretraining")
    print("=" * 60)

    # TODO(alessio): Implement micro-LM training with tokenizer ablation:
    #   1. Load Italian corpus (same as Exp 1)
    #   2. Build two tokenizers: English-centric baseline vs Italian-optimized
    #   3. Build two identical decoder-only models (same arch, different tokenizers)
    #   4. Train both to convergence with identical hyperparameters
    #   5. Compare: bits-per-byte (tokenizer-fair metric), tokens-to-convergence
    #   6. Report over ≥3 seeds with mean ± std

    print("\n[SKIP] Experiment scaffold — implement the pipeline above.")


if __name__ == "__main__":
    main()
