# MP-92 Walkthrough Video: 8-Minute Screen Recording Script

**Target length:** 8 minutes
**Format:** Screen recording with voiceover
**Thesis arc:** Rung 2 NO-GROK → Rung 3 phase transition → Capstone dissociation → Retune NO-MOVE → Teaching artifact

---

## Visual Narrative (Slide-by-Slide)

### 0:00–0:30 — Title Card
**Visual:** Repo name, paper title, "MP-92 Premiere"
**Voice:** "From Gradient to Transformer to Circuit — a micro-scale mechanistic interpretability pipeline. I'm Alessio Brillo. This is the MP-92 premiere walkthrough."

### 0:30–1:30 — The Pipeline Overview
**Visual:** Diagram showing 6 rungs → paper → teaching artifact → premiere
**Voice:** "Six rungs: induction heads, grokking, superposition, circuit patching, SAE, capstone. Every number backed by a manifest. verify-claims = 0. The pipeline trains from scratch, instruments fully, verifies causally, and reports honestly — especially the negatives."

### 1:30–3:00 — Rung 2: NO-GROK (The Headline)
**Visual:**
- Grokking curve (train/val loss + accuracy)
- Fourier weights bar chart (dense: 111/113 tall bars)
- Ablation curve (keep N freqs → accuracy)

**Voice:** "Rung 2 is the most surprising result. Three seeds, P=113, val accuracy 1.0 — perfect generalization. But Fourier k₉₉ = 111/113. The model uses 98% of all frequencies. Ablation proves it: keep 111 → 1.0; keep 20 → chance; remove top 1 → measurable drop. This is NO-GROK: generalization WITHOUT the sparse circuit."

### 3:00–4:00 — Rung 3: Superposition (The Positive Control)
**Visual:**
- Sparsity sweep: 10/20 → 20/20 features
- Pentagon geometry: 5 vectors in 2D, angle gaps ~72°
- Phase transition diagram

**Voice:** "Rung 3 is the strongest verified result. We root-caused the prior non-reproduction — the dataset pre-embedded features, removing the bottleneck. With the correct canonical architecture: phase transition at sparsity 0.05, 20/20 features represented, and the geometric smoking gun — 5 features in 2D form a regular pentagon. Equiangular geometry = sparse attractor."

### 4:00–5:00 — Capstone: Joint Training Dissociation
**Visual:**
- Table: Induction 0.504 | Modular 0.0047 | k₉₉ 98.1
- Retune A/B table: Control/Offset/Reweight all below chance
- K-comp trajectory

**Voice:** "The capstone trains both tasks together. Induction takes off to 0.504; modular stays at chance with dense Fourier. Two hypotheses: interference (shared embeddings) or schedule (1-token vs 127-token imbalance). Retune A/B falsifies BOTH. Dedicated vocab range? NO-MOVE. 10× curriculum weight? NO-MOVE. The dense attractor is the contribution."

### 5:00–6:00 — Honest Landscape
**Visual:** Limitations table + Rung 1 fixed-vs-fresh + Rung 4/5 results

**Voice:** "The honest landscape: Rung 1's 52.2% is sub-standard scale (800 epochs). Rung 4's ~0.20 recovery is real but no head detected. Rung 5's SAE on real activations: 99.97% FVE but 53% L0 — dense reconstruction. Limitations upfront: micro-scale, algorithmic tasks, NO-GROK at all scales, GPU pending as follow-up."

### 6:00–7:00 — Teaching Artifact v22 (Reproducibility Proof)
**Visual:** Notebook cells executing: load → Fourier (k₉₉=98) → K-comp (0.39, _vacuous) → Patching (~0.20) → SAE (99.97% FVE, 53% L0) → Literature table → Honest conclusion

**Voice:** "Teaching artifact v22 runs on the shakedown checkpoint. Stranger-run on fresh Colab: uv sync --frozen, all cells green, outputs match manifests. Kill-drill demo: resume from step 1000 → bit-identical. This IS the reproducibility proof."

### 7:00–8:00 — Continuum & Close
**Visual:** ADR-0029 candidate set, premiere channels, repo URL
**Voice:** "The continuum law: ADR-0029 opens with exactly one question from {phase diagram, scaled induction, SAE on head, ACDC on circuit}. Unchosen three close with dated reasons. Paper v20 compiles from manifests. Five-channel premiere: essay, thread, site, Space, walkthrough — atomic launch. Repo: github.com/AlessioBrillo/from-gradient-to-transformer. Thank you."

---

## Recording Checklist

### Technical
- [ ] 1920x1080 or higher
- [ ] Clear audio (external mic preferred)
- [ ] Cursor visible, smooth movements
- [ ] No notifications/popups during recording

### Content
- [ ] Show `verify-claims` passing
- [ ] Show manifests in `results/` directory
- [ ] Show notebook executing live (or pre-recorded cells)
- [ ] Show paper PDF (once compiled)
- [ ] Show GitHub Pages site

### Post-Production
- [ ] Trim to ≤ 8 minutes
- [ ] Add captions for key numbers
- [ ] Add chapter markers (YouTube)
- [ ] Upload to YouTube (unlisted) + commit link

---

## YouTube Upload Metadata

**Title:** From Gradient to Transformer to Circuit — MP-92 Walkthrough (8 min)
**Description:**
```
Micro-scale mechanistic interpretability pipeline: from-scratch training, full instrumentation, causal verification, honest negatives.

Paper v20: [URL_TBD]
Teaching artifact v22: notebooks/capstone_teaching_artifact_v22.ipynb
Results: portfolio/RESULTS.md
Repo: https://github.com/AlessioBrillo/from-gradient-to-transformer

Chapters:
0:00 Pipeline overview
1:30 Rung 2: NO-GROK negative
3:00 Rung 3: Superposition phase transition
4:00 Capstone: Joint training dissociation
5:00 Honest landscape
6:00 Teaching artifact v22 (reproducibility)
7:00 Continuum & close

#MechanisticInterpretability #Grokking #Transformers #ReverseEngineering
```

**Tags:** mechanistic interpretability, grokking, transformers, reverse engineering, modular addition, superposition, induction heads, circuit discovery, sparse autoencoders

---

## Cross-Links (Commit in Premiere Launch)
- Essay: `portfolio/essay/grokking-dense-attractor.md`
- Thread: `portfolio/threads/mp-92-premiere-thread.md`
- Space: `portfolio/space/mp-92-space.md`
- Site: GitHub Pages deploy
- Premiere ledger: `portfolio/premiere-ledger.md`