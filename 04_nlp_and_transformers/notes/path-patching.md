---
tags: [type/lesson, phase/4, state/review]
---

# Path Patching — Tracing Causal Edges

## Activation patching vs path patching

| Method | What it measures | Level |
|--------|-----------------|-------|
| Activation patching | Replace a node's activation at a specific position | Node-level |
| Path patching | Replace a specific *edge* between two nodes | Edge-level |
| Attribution patching | Approximate patching via gradients | Approximate |

Path patching isolates the causal contribution of a **specific computational path**, e.g., "head L0H1 → head L1H2" rather than "all paths through L0H1".

## How it works

1. **Run clean + corrupted** forward passes, cache all activations
2. For edge (source_node, dest_node):
   - In the **corrupted run**, patch ONLY the activation at source_node back to clean
   - In the **clean run**, corrupt the activation at dest_node
   - Run forward with these combined interventions
   - If model behavior matches clean → the edge was necessary

More concretely, for an edge between attention heads:
```python
# Clean run: normal forward
# Corrupted run: everything except the head output is corrupted
# To test edge L0H1 → L1H2:
#   Forward with clean input, but manually replace:
#     - L0H1 output → corrupted L0H1 output (disable the source)
#     - L1H2 → use clean L1H2's normal computation
#   OR: corrupted forward, but replace:
#     - L0H1 output → clean L0H1 output (enable source)
#     - L1H2's Q/K/V inputs → keep everything else corrupted
```

## Why it matters for circuit discovery

Activation patching tells you "this head matters" but not "what does it communicate to." Path patching traces the **information flow** through the residual stream:

```
Input → L0H1 (attends to prev token) → resid_mid → L1H2 (reads resid_mid and predicts)
```

Without path patching, you know L0H1 and L1H2 are both important. With path patching, you know L0H1 → L1H2 is the specific circuit edge.

## MI forward link

Path patching is the most precise causal tool in circuit analysis — it isolates individual edges in the computational graph. Combined with QK/OV circuit decomposition (which tells you *what* each head computes), path patching tells you *where* the computation flows. This is the closest MI gets to a complete circuit diagram.

## References
- Wang et al., *Interpretability in the Wild: a Circuit for Indirect Object Identification in GPT-2 small* (ICLR 2023)
- Goldowsky-Dill et al., *Localizing Model Behavior with Path Patching* (2023)
- Nanda, *Patching vs. Patching* (blog post, 2023)

## Links

- [[04_nlp_and_transformers/notes/activation-patching]]
- [[04_nlp_and_transformers/proofs/circuit-analysis-complete]]
