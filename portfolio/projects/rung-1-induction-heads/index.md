---
title: "Rung 1: Induction Heads"
description: "Detect and verify induction heads in a 2-layer attention-only transformer using K-composition diagnostics"
tags: [induction-heads, mechanistic-interpretability, transformer, k-composition]
phase: 1
rung: 1
---

**Problem**: Detect and verify induction heads in a small 2-layer attention-only transformer trained on repeated random tokens. Induction heads implement the algorithm `\`[A][B]...[A] → [B]\`` — they attend from the current token to its previous occurrence and copy the next token.

**Methodology**:
- Train 2-layer attention-only transformer on repeated random token sequences (Olsson et al. 2022)
- Identify induction heads via K-composition diagnostic (Nanda & Jacobsen 2023): L1 head composes with L0 duplicate-token head
- Verify causal role via head ablation and activation patching
- Track Step 1 (L0 duplicate mass) and Step 2 (K-composition) independently

**Key Result**:
<!-- manifest: results/exp1_induction_heads.json -->
Extended 10k-epoch run at standard scale (d_model=64, 2-layer, 4 heads, fresh batches) — Step 1 and Step 2 trajectories tracked every 500 epochs.

**Figure**:
![K-composition Trajectory](figures/exp1_step1_step2_trajectory.png) <!-- manifest: results/exp1_induction_heads.json -->

**Notebook**: `notebooks/exp1_induction_heads_demo.ipynb`

**Limitations**:
- Standard scale (d_model=64) may not reflect larger model dynamics
- Fresh-batches training prevents memorization but may slow induction emergence
- 0/8 heads at 3k epochs; 10k epoch run in progress to find emergence boundary
- No W&B integration in earlier runs (added in MP-78)

**Next Steps**:
- Complete 10k epoch run and document emergence boundary
- Run SAE on first confirmed head checkpoint (Rung 5 dependency)
- Test at larger scales (d_model=128, 256)