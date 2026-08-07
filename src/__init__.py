"""From Gradient to Transformer to Circuit.

A research showcase and structured learning journey in mechanistic
interpretability: train small transformers and reverse-engineer the
algorithms they learn.

Submodules are imported explicitly where they are used (e.g.
``python -m src.experiments.exp2_grokking``) rather than eagerly here —
importing every experiment at package-import time pulled in the full
torch/matplotlib stack on any ``import src`` (and made ``python -m
src.results verify`` warn about a module imported before runpy ran it).
"""
