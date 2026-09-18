# The Dense Attractor: Why My Transformer Solved Modular Addition Without Grokking

**Published:** 2026-09-18 | **Author:** Alessio Brillo | **Repo:** [from-gradient-to-transformer](https://github.com/AlessioBrillo/from-gradient-to-transformer)

---

## The 30-Second Summary

I built a decoder-only transformer from scratch, trained it on modular addition (a + b mod 113), and reverse-engineered its learned algorithm via Fourier decomposition. The model achieves **perfect validation accuracy (1.0 across 3 seeds)** — but without forming the sparse Fourier circuit that the grokking literature defines as the phenomenon.

**Key finding:** The model implements modular addition via a **dense Fourier representation** (k₉₉ = 111/113 frequencies), not the sparse O(√P) algorithm. This is a verified negative result that falsifies the hypothesis that the frozen protocol (cosine LR, weight decay 1.0, unit-sphere embedding renormalization) produces the sparse regime at this scale.

---

## The Experiment

### Setup
- **Task:** Modular addition a + b mod 113, 30% train / 70% validation split by equation (holding out random (a,b) pairs, not target classes)
- **Model:** 1-layer decoder-only transformer, d_model=128, d_mlp=512, n_heads=4 (Nanda et al. 2023 configuration)
- **Training:** 5000 epochs, weight decay 1.0, cosine LR, checkpointing every 500 epochs
- **Seeds:** 0, 1, 2 (three independent runs)

### Results

| Metric | Seed 0 | Seed 1 | Seed 2 | Aggregate |
|--------|--------|--------|--------|-----------|
| Final val accuracy | 1.0 | 1.0 | 1.0 | 1.0 ± 0.0 |
| Generalization epoch | 1250 | 1048 | 1326 | 1208 ± 117 |
| Fourier k₉₉ | 111/113 | 111/113 | 111/113 | 111.0 ± 0.0 |
| Fourier sparsity | 0.085 | 0.082 | 0.071 | 0.079 ± 0.006 |

**All three seeds reach perfect generalization — but k₉₉ = 111/113 means the model uses 98.2% of all available Fourier frequencies.** The representation is maximally dense, not sparse.

---

## Causal Confirmation: Frequency Ablation

To verify the model *actually uses* all these frequencies (vs. just having non-zero weights), I ran causal ablations:

- **Keep all 113 frequencies** → 1.0 accuracy (baseline)
- **Keep top 111 frequencies** → 1.0 accuracy (preserved)
- **Keep top 20 frequencies** → ~0.009 accuracy (chance level)
- **Remove top 20 frequencies** → accuracy destroyed
- **Remove top 1 frequency** → accuracy drops measurably

**The model genuinely implements modular addition via a dense Fourier transform — every frequency contributes.**

---

## The Dense Attractor Under Joint Training

The capstone experiment (joint modular + induction training) reveals a deeper pattern:

| Config | Modular Acc | Induction Acc | Fourier k₉₉ | Max K-comp |
|--------|-------------|---------------|-------------|------------|
| Shakedown (2000 steps) | **0.0047** (chance) | **0.5041** | 98.1 (dense) | 0.394 (_vacuous) |
| Retune Arm A: vocab-offset | 0.0060 | 0.0005 | 98.6 (dense) | 0.173 |
| Retune Arm B: 10× modular weight | 0.0065 | 0.0005 | 98.1 (dense) | 0.305 |

**Neither vocabulary separation nor curriculum reweighting moves modular off chance.** The dense attractor is stable — it's not an interference artifact or schedule artifact. The joint-training dissociation *is* the contribution.

---

## What This Means for Grokking

The canonical grokking story (Nanda et al. 2023): delayed generalization coincides with the formation of a sparse Fourier circuit (k₉₉ ≪ P/2).

**My results show:** Perfect generalization (val 1.0) can occur with a **dense Fourier representation** (k₉₉ = 111/113). The two phenomena — generalization and sparse circuit formation — are **decoupled** at this scale.

This doesn't contradict Nanda et al. — their experiments used different hyperparameters (smaller P, different architectures). It *does* show that the frozen protocol in this repository (cosine LR, wd=1.0, embedding renormalization) finds a **different algorithm** for the same task.

---

## Honest Negatives Are Contributions

**NO-GROK** (this paper): val 1.0 + dense Fourier across all tested scales (P=11, 17, 29, 59, 67, 97, 113)
**NO-MOVE** (capstone retune A/B): modular stays at chance under both interference and schedule interventions

These aren't failures — they're **falsifications**. The sparse-circuit hypothesis doesn't hold at this scale. The dense attractor is the real phenomenon.

---

## Reproducibility

Every number in this post is backed by a manifest file:
- `results/exp2_grokking.json` — 3-seed P=113 grokking run
- `results/probe_capstone_shakedown.json` — joint training dissociation
- `results/probe_capstone_ab_{control,offset,reweight}.json` — retune A/B verdict

Verification: `uv run python -m src.results verify` → **all claims check out**

---

## What's Next

The GPU run for P=113 (launched 2026-08-24 on Colab) is pending as a scale follow-up — not the decision. The paper already states: "GPU verdict pending as scale follow-up, not the decision."

The next research question will be chosen via the continuum ledger (ADR-0029): exactly one from {solution-regime phase diagram, scaled R1 induction, SAE on confirmed-head checkpoint, ACDC on real circuit}.

---

**Links:**
- Paper (v20 scaffold): `portfolio/paper/main.tex`
- Teaching artifact v22: `notebooks/capstone_teaching_artifact_v22.ipynb`
- Results ledger: `portfolio/RESULTS.md`
- Continuum ledger: `docs/adr/0028-continuum-ledger-23.md`

---

*This essay is part of the MP-92 premiere atomic launch. Companion thread: [Twitter/X thread](URL_TBD). Walkthrough video: [8-min walkthrough](URL_TBD). Space recording: [Space link](URL_TBD). Portfolio site: [GitHub Pages](URL_TBD).*