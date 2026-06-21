#!/usr/bin/env python3
"""Experiment 3 — Positional encoding ablation.

Compare sinusoidal, learned, and Rotary Position Embedding (RoPE) on the same
micro-LM architecture. Reports validation perplexity over ≥3 seeds.

Usage:
    python -m src.experiments.exp3_positional_encoding

Output:
    - figures/exp3_positional_encoding.png
    - Console: perplexity per positional encoding variant
"""

from src.reproducibility import set_seed

set_seed(42)


def main() -> None:
    print("=" * 60)
    print("Exp 3 — Positional Encoding Ablation")
    print("=" * 60)

    # TODO(alessio): Implement positional encoding comparison:
    #   1. Three model variants: sinusoidal, learned, RoPE
    #   2. Same micro-LM architecture, tokenizer, and training regime
    #   3. Train each variant ≥3 seeds
    #   4. Report validation perplexity per variant
    #   5. Discuss: which encoding works best at micro scale?

    print("\n[SKIP] Experiment scaffold — implement the pipeline above.")


if __name__ == "__main__":
    main()
