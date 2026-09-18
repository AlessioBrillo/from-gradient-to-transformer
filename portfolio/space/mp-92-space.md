# MP-92 Twitter Space: 10-Minute Talk Script

**Scheduled for:** Release week (TBD)  
**Duration:** 10 minutes + Q&A  
**Format:** Solo talk from four-register distillation

---

## Four-Register Distillation (Source of Truth)

| Register | Purpose | Length | Audience |
|----------|---------|--------|----------|
| **Paper** | Full technical record | ~12 pages | Researchers |
| **Annex** | Supplementary details | ~4 pages | Reproducers |
| **30-sec pitch** | Hook + thesis | 30 sec | Twitter/X, elevator |
| **5-min walkthrough** | Visual narrative | 5 min | Space, video |

All registers cite the SAME manifest numbers. Zero drift.

---

## 30-Second Pitch (Tweet 1)

> "I built a decoder-only transformer from scratch. Strongest result: superposition phase transition with pentagon geometry. Most honest result: model solves modular addition perfectly (val 1.0) but WITHOUT the sparse Fourier circuit — dense attractor instead. The negative IS the contribution."

---

## 10-Minute Talk Outline

### 0:00–1:00 — Hook & Thesis
- "What if the model solves the task but learns a DIFFERENT algorithm than the literature predicts?"
- Thesis: **The dense attractor under joint training is the finding.** NO-GROK and NO-MOVE are positive-negative contributions — they falsify the sparse-circuit hypothesis at this scale.

### 1:00–3:00 — Rung 2: The NO-GROK Negative
- Setup: 1L transformer, P=113, 3 seeds, frozen protocol (Nanda et al. config)
- Result: val 1.0 across all seeds, generalization at ~1200 epochs
- BUT: Fourier k₉₉ = 111/113 (98.2% of frequencies)
- Ablation proof: keep 111 → 1.0; keep 20 → chance; remove top 1 → drops
- **Interpretation:** Generalization ≠ sparse circuit. They're decoupled at this scale.

### 3:00–4:30 — Rung 3: The Positive Control (Superposition)
- Root-caused prior non-reproduction: dataset pre-embedded features (no bottleneck)
- Reproduced Elhage et al. 2022: 10/20 → 20/20 features by sparsity 0.05
- Pentagon geometry: 5 features → 2D = regular pentagon (std ≤ 1.4°)
- **This is the strongest verified result in the repo.**

### 4:30–6:00 — Capstone: Joint Training Dissociation
- 1 seed, 2000 steps, modular + induction together
- Induction: 0.504 accuracy | Modular: 0.0047 (chance) | Fourier: dense (k₉₉=98.1)
- **The dissociation IS the finding:** tasks compete, induction wins
- Retune A/B: vocab-offset (interference hypothesis) → NO-MOVE; 10× weight (schedule hypothesis) → NO-MOVE
- Dense attractor stable under both interventions

### 6:00–7:30 — The Honest Landscape
| Rung | Result | Status |
|------|--------|--------|
| 1 Induction | 52.2% fresh batches, 0 heads at 800 epochs | Sub-standard scale |
| 2 Grokking | val 1.0, k₉₉=111/113 (dense) | **NO-GROK** |
| 3 Superposition | Phase transition, pentagon ✓ | **REPRODUCED** |
| 4 Patching | ~0.20 recovery, 0 heads | Real signal, no head |
| 5 SAE | 99.97% FVE, 53% L0 (dense) | Needs confirmed head |
| 6 Capstone | Dissociation + NO-MOVE | Dense attractor |

### 7:30–8:30 — Limitations (Upfront)
- Micro-scale (4.3M params)
- Algorithmic tasks only
- NO-GROK at ALL scales tested
- GPU P=113 pending as follow-up, not decision
- Single architecture, limited seeds

### 8:30–9:30 — Continuum: What's Next
ADR-0029 opens with exactly ONE research question:
1. Solution-regime phase diagram (sparse vs dense across P, size, joint/solo)
2. Scaled Rung 1 induction (standard config, GPU)
3. SAE on confirmed-head checkpoint
4. ACDC on real circuit

Unchosen three close with dated reasons. Same sitting.

### 9:30–10:00 — Reproducibility Commitment
- Every number → manifest tag → `verify-claims=0`
- Teaching artifact v22: stranger-run on fresh Colab
- Kill-drill: bit-identical checkpoint resume proven
- Paper compiles from manifests only

---

## Q&A Prep (Likely Questions)

**Q: "Why not just use TransformerLens on a real model?"**
A: Post-hoc observation ≠ learning dynamics. We trace HOW it learned, not just what it does.

**Q: "Is NO-GROK just a hyperparameter issue?"**
A: Tested P=11,17,29,59,67,97,113; cosine/constant LR; wd=1.0/1.5; embedding renorm on/off. Dense at all. It's the protocol.

**Q: "Does this contradict Nanda et al. 2023?"**
A: No — different hyperparameters. We show the *frozen protocol in this repo* finds a different algorithm. The decoupling is the insight.

**Q: "What about the GPU run?"**
A: Pending as scale follow-up. Paper already states: "GPU verdict pending as scale follow-up, not the decision."

**Q: "Why should we care about micro-scale?"**
A: Full causal access. Ground-truth algorithms. The pipeline (train → instrument → verify → report) scales; the findings are honest about scope.

---

## Space Announcement Tweet (Pre-Draft)

> 🎙️ **Twitter Space: The Dense Attractor**
> 
> Tomorrow [DATE] at [TIME] — 10 min talk + Q&A on why my from-scratch transformer solves modular addition WITHOUT grokking's sparse circuit.
> 
> Paper: [URL_TBD]
> Repo: github.com/AlessioBrillo/from-gradient-to-transformer
> 
> #MechanisticInterpretability

---

## Post-Space Deliverables
- [ ] Recording link committed to `portfolio/space/mp-92-space.md`
- [ ] Transcript commitment (will transcribe key Q&A)
- [ ] Cross-link in essay, thread, walkthrough