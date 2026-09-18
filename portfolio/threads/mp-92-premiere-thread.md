# MP-92 Premiere: Twitter/X Thread (12 Tweets)

**Draft for atomic launch — replace URL_TBD with actual URLs before posting**

---

## Tweet 1/12
I built a decoder-only transformer from scratch and reverse-engineered what it learns.

Strongest result: Rung 3's superposition phase transition (10/20 → 20/20 features, pentagon geometry ✓).

Most honest result: Rung 2's NO-GROK negative — model solves modular addition (val 1.0) WITHOUT the sparse Fourier circuit.

🧵👇

---

## Tweet 2/12
**Rung 2 — Grokking Modular Addition (P=113, 3 seeds)**

- Val accuracy: **1.0 ± 0.0** (perfect generalization)
- Generalization epoch: 1208 ± 117
- Fourier k₉₉: **111/113** (98.2% of frequencies — DENSE)
- Fourier sparsity: 0.079 ± 0.006 (0=sparse, 1=dense)

The model uses ALL frequencies. Not O(√P) sparse circuit.

<!-- manifest: results/exp2_grokking.json -->

---

## Tweet 3/12
**Causal proof:** Ablation confirms the dense mechanism.

- Keep 111/113 freqs → 1.0 acc ✓
- Keep top 20 freqs → chance (1/113) ✗
- Remove top 20 freqs → destroys performance ✗

Every frequency contributes. The model implements a dense DFT, not the sparse grokking algorithm.

<!-- manifest: results/exp2_grokking.json -->

---

## Tweet 4/12
**Rung 3 — Superposition Phase Transition (REPRODUCED ✓)**

20 features → 5 dimensions, sparsity 0.01:
- Features represented: **19.67 ± 0.47** / 20 (range 19–20)
- Mean dimensionality: **0.249 ± 0.001** (theory: 1/5 × n_avg)
- Mean abs correlation: **0.351 ± 0.001**

Sparsity sweep: 10/20 at sparsity 0.5 → **20/20 by sparsity 0.05**.

<!-- manifest: results/exp3_superposition.json -->

---

## Tweet 5/12
**Pentagon geometry verification:**
5 features → 2D at sparsity ≤ 0.1 sit on a **regular pentagon**.
- Angle gaps: 70.2°–73.8° (ideal: 72°)
- Std: ≤ 1.4° (dense regime: 22°+)

Equiangular geometry = sparse-phase attractor. Root cause of prior non-reproduction found: dataset pre-embedded features (no bottleneck).

<!-- manifest: results/exp3_superposition.json -->

---

## Tweet 6/12
**Rung 1 — Induction Heads: Fixed vs Fresh Batches**

Bug fix (2026-08-02): prefix must have no repeated tokens (birthday problem).

800-epoch matched comparison:

| | Fixed (reused) | Fresh (resampled) |
|---|---|---|
| Val acc | 0.05% (below chance!) | **52.2%** |
| Val loss | 24.31 (climbing) | 3.65 (tracks train) |
| Heads detected | 0/8 | 0/8 |

Fresh batches generalize; fixed batches catastrophically overfit. Still no head at this scale (diag+1 < 0.3).

---

## Tweet 7/12
**Rung 4 — Circuit Patching: Real signal, no head**

- Activation patching mean recovery: **~0.20 ± 0.007** (consistent across 3 seeds)
- Path patching: _vacuous (0 heads detected)
- Val acc: 0.489 ± 0.014

Circuit sensitivity exists (~0.20 recovery) but isn't concentrated in one head. Ablation skipped — 0 heads.

<!-- manifest: results/exp4_circuit_patching.json -->

---

## Tweet 8/12
**Rung 5 — SAE: Synthetic ✓, Real = Dense Reconstruction**

| | Synthetic | Real (shakedown ckpt) |
|---|---|---|
| FVE | 97.5% | **99.97%** |
| L0 (active) | 18.9% | **53.2%** |
| Dead features | 7.6% | 0% |

Real activations reconstruct better but far less sparsely. Small undertrained residual stream → no disentangled features yet. Next: SAE on confirmed-head checkpoint.

<!-- manifest: results/exp5_sae_dashboard.json -->

---

## Tweet 9/12
**Capstone — Joint Training Dissociation (THE FINDING)**

1 seed, 2000 steps, d_model=256, 4L, 8H:
- Induction: **0.5041** accuracy
- Modular: **0.0047** (chance = 0.0088)
- Fourier k₉₉: **98.1** (dense)
- Max K-comp: 0.394 (_vacuous)

Induction learns; modular doesn't. They compete; induction wins.

<!-- manifest: results/probe_capstone_shakedown.json -->

---

## Tweet 10/12
**Retune A/B: Falsified Both Hypotheses**

| Arm | Modular Acc | Induction Acc | k₉₉ | Max K-comp |
|---|---|---|---|---|
| Control | 0.0062 | 0.0005 | 98.2 | 0.369 |
| Vocab-offset (Arm A) | 0.0060 | 0.0005 | 98.6 | 0.173 |
| 10× mod weight (Arm B) | 0.0065 | 0.0005 | 98.1 | 0.305 |

**NO-MOVE.** Neither dedicated vocab range nor 10× curriculum weight moves modular off chance. Dense attractor is stable.

<!-- manifest: results/probe_capstone_ab_*.json -->

---

## Tweet 11/12
**Limitations (honest, not hidden):**

- Micro-scale models (4.3M params) — may not transfer to 7B+
- Algorithmic tasks — cleaner than natural language
- NO-GROK at ALL scales tested (P=11..113) — GPU verdict pending as follow-up
- SAE on real = dense (53% L0) — needs confirmed-head checkpoint
- Path patching unit-tested only — needs Rung 1 standard scale

---

## Tweet 12/12
**The dense attractor under joint training IS the contribution.**

Paper v20 (manifest-indexed), teaching artifact v22 (stranger-run ready), premiere launching now.

Repo: github.com/AlessioBrillo/from-gradient-to-transformer
Paper: portfolio/paper/main.tex
Teaching: notebooks/capstone_teaching_artifact_v22.ipynb
Results: portfolio/RESULTS.md

Every number has a manifest. `verify-claims=0` ✓

**#MechanisticInterpretability #Grokking #Transformers**

---

## Launch Checklist
- [ ] Essay published → URL_TBD
- [ ] Thread posted → URL_TBD  
- [ ] Site deployed → URL_TBD
- [ ] Space announced → URL_TBD
- [ ] Walkthrough uploaded → URL_TBD
- [ ] All 5 URLs committed in single commit
- [ ] premiere-ledger.md updated with timestamps