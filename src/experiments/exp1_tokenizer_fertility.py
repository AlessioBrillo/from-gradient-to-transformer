#!/usr/bin/env python3
"""Experiment 1 — Tokenizer fertility study.

Quantifies the "Italian tokenization tax" by training BPE/Unigram tokenizers
at several vocabulary sizes and measuring fertility, Rényi efficiency, and
compression ratio on Italian vs. English text, compared against reference
English-centric tokenizers (GPT-2, Mistral, Gemma, Llama-3).

Usage:
    python -m src.experiments.exp1_tokenizer_fertility

Output:
    - figures/exp1_fertility_comparison.png
    - Console table of fertility numbers across tokenizers and languages
"""

from src.reproducibility import set_seed

set_seed(42)


def main() -> None:
    print("=" * 60)
    print("Exp 1 — Tokenizer Fertility Study")
    print("=" * 60)

    # TODO(alessio): Implement tokenizer training pipeline:
    #   1. Load Italian and English subsets from PAISÀ / Italian Wikipedia / mC4
    #   2. Train BPE tokenizers at vocab sizes [8k, 16k, 32k]
    #   3. Train Unigram tokenizer at same vocab sizes (SentencePiece)
    #   4. Load reference tokenizers (GPT-2, Mistral, etc.) via transformers
    #   5. Compute fertility (tokens / word) on held-out Italian and English text
    #   6. Compute Rényi efficiency (Galle, 2019) and compression ratio
    #   7. Identify morphological patterns driving Italian over-segmentation
    #   8. Report mean ± std over ≥3 random corpus samples
    #   9. Save figure to figures/exp1_fertility_comparison.png

    print("\n[SKIP] Experiment scaffold — implement the pipeline above.")
    print("See: src/experiments/exp1_tokenizer_fertility.py")


if __name__ == "__main__":
    main()
