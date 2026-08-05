"""Mechanistic interpretability experiments.

Each experiment module in this package implements one rung of the MI experiment
ladder. Every module is callable as `python -m src.experiments.exp<N>_<name>`
and accepts `--seed`, `--device`, and experiment-specific flags.

Modules are intentionally NOT imported here: eager importing them at package
level dragged the full torch/matplotlib stack into every `import src`, even
for light callers like `python -m src.results verify`.
"""
