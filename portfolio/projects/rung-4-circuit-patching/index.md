---
title: "Rung 4: Circuit Patching"
description: "Causal circuit discovery via activation patching and path patching in trained transformers"
tags: [circuit-patching, activation-patching, path-patching, mechanistic-interpretability]
phase: 1
rung: 4
---

**Problem**: Discover and verify computational circuits in trained transformers using causal intervention methods: activation patching (swap activations between runs) and path patching (isolate specific pathways).

**Methodology**:
- Train models on induction and modular addition tasks
- Detect induction heads via K-composition diagnostic
- Activation patching: swap activations between clean/corrupted runs to measure causal effect
- Path patching: isolate direct/indirect effects through specific heads/MLPs
- Head ablation: verify necessity of detected heads

**Key Result**:
<!-- manifest: results/exp4_circuit_patching.json -->
Circuit patching infrastructure built and tested on small models. Self-patching is no-op; cross-run patching changes output. Path patching returns expected keys (direct/indirect effects). Awaiting confirmed induction head checkpoint for real circuit discovery.

**Figures**:
![Induction Head Detection](figures/exp4_induction_detection.png) <!-- manifest: results/exp4_circuit_patching.json -->
![Head Ablation](figures/exp4_head_ablation.png) <!-- manifest: results/exp4_circuit_patching.json -->
![Activation Patching](figures/exp4_activation_patching.png) <!-- manifest: results/exp4_circuit_patching.json -->

**Notebook**: `notebooks/exp4_circuit_patching_demo.ipynb`

**Limitations**:
- Gated on Rung 1 producing confirmed induction heads (0/8 at 3k epochs, 10k in progress)
- Tested only on small synthetic/untrained models so far
- No real circuit discovery yet — infrastructure ready, awaiting real heads

**Next Steps**:
- Run on first confirmed head checkpoint from Rung 1 (10k epoch run)
- Run on capstone model checkpoints (MP-78)
- Extend to modular addition circuits (Fourier frequencies as circuits)