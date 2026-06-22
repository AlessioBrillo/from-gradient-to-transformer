"""Mechanistic interpretability experiments.

Each experiment module in this package implements one rung of the MI experiment
ladder. Every module is callable as `python -m src.experiments.exp<N>_<name>`
and accepts `--seed`, `--device`, and experiment-specific flags.
"""

from src.experiments import (
    exp1_induction_heads,
    exp2_grokking,
    exp3_superposition,
    exp4_circuit_patching,
    exp5_sae_dashboard,
    exp6_automated_circuit,
)

__all__ = [
    "exp1_induction_heads",
    "exp2_grokking",
    "exp3_superposition",
    "exp4_circuit_patching",
    "exp5_sae_dashboard",
    "exp6_automated_circuit",
]
