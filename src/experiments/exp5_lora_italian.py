#!/usr/bin/env python3
"""Experiment 5 — LoRA fine-tuning on an Italian task.

Apply LoRA fine-tuning to the micro-LLM on an Italian NLU or generation task.
Measure the performance delta vs. full fine-tuning.

Usage:
    python -m src.experiments.exp5_lora_italian

Output:
    - Console: LoRA vs full fine-tuning metrics
"""

from src.reproducibility import set_seed

set_seed(42)


def main() -> None:
    print("=" * 60)
    print("Exp 5 — LoRA Fine-Tuning on Italian Task")
    print("=" * 60)

    # TODO(alessio): Implement LoRA experiment:
    #   1. Load pretrained micro-LLM
    #   2. Apply LoRA adapters to attention projections
    #   3. Fine-tune on Italian NLU / generation task
    #   4. Compare against full fine-tuning baseline
    #   5. Report metrics, parameter count, and training time

    print("\n[SKIP] Experiment scaffold — implement the pipeline above.")


if __name__ == "__main__":
    main()
