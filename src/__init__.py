"""From Gradient to Transformer to Circuit.

A research showcase and structured learning journey in mechanistic
interpretability: train small transformers and reverse-engineer the
algorithms they learn.

Modules:
    reproducibility: Seed control and deterministic execution.
    experiments: MI experiment implementations (Rungs 1-6).
"""

from src import experiments, reproducibility

__all__ = ["reproducibility", "experiments"]
