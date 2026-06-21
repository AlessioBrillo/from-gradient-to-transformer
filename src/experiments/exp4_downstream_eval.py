#!/usr/bin/env python3
"""Experiment 4 — Downstream evaluation on Italian NLU tasks.

Fine-tune or probe the tokenizer-aware micro-LLM on one Italian NLU benchmark
(UINAUIL or ItaCoLA) and report mean ± std over ≥3 seeds.

Usage:
    python -m src.experiments.exp4_downstream_eval

Output:
    - Console: downstream task performance with confidence intervals
"""

from src.reproducibility import set_seed

set_seed(42)


def main() -> None:
    print("=" * 60)
    print("Exp 4 — Downstream Italian NLU Evaluation")
    print("=" * 60)

    # TODO(alessio): Implement downstream eval:
    #   1. Load micro-LLM checkpoint from Exp 2 (best tokenizer variant)
    #   2. Prepare Italian NLU task: UINAUIL (Basile et al., ACL 2023) or ItaCoLA
    #   3. Fine-tune or probe on the task
    #   4. Report accuracy / F1 with mean ± std over ≥3 seeds
    #   5. Compare against baseline (English-centric tokenizer variant)

    print("\n[SKIP] Experiment scaffold — implement the pipeline above.")


if __name__ == "__main__":
    main()
