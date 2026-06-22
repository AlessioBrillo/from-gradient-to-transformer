---
tags: [moc, phase/7, capstone]
---

# Capstone — Train + Reverse-Engineer

The capstone converges everything from Phases 1–6 into a single arc: **build a decoder-only transformer from scratch, then reverse-engineer the algorithms it learns.** This is the primary research vehicle for the MI thesis.

## Thesis (one sentence)

> I build a decoder-only transformer from scratch, then reverse-engineer the algorithms it learns — grokking modular addition with Fourier decomposition, induction heads, circuit verification via activation patching, and sparse autoencoder feature extraction.

## Experiment Ladder

Do in order; each produces a defensible standalone result:

### Rung 1 — Induction Heads (reliable fallback flagship)
Train a 2-layer attention-only transformer (~1–4 heads/layer) on repeated-random-token sequences. Identify induction heads by their characteristic attention pattern ([A][B]…[A]→[B]). Verify causally via head ablation and logit-lens analysis.

- *Metric:* Per-token loss vs. context position; induction attention pattern; prefix-matching + copying decomposition; training-loss bump.
- *Compute:* Minutes to a couple hours on one GPU.
- *Reference:* Olsson et al., 2022; Connor Kissane's TransformerLens replication.

### Rung 2 — Grokking Modular Addition ★ (Primary Flagship)
Train a 1-layer transformer (d_model=128, 4 heads, d_mlp=512, ReLU) on a+b mod P (P=113). Observe delayed generalization (the grokking curve). Reverse-engineer the algorithm via Fourier decomposition of embeddings: the model learns a discrete Fourier transform and implements addition via trigonometric identities. Ablate individual Fourier frequencies to confirm.

- *Metric:* Train/test loss; Fourier weight sparsity; progress measures (memorization → circuit formation → cleanup).
- *Compute:* ~minutes/GPU per seed.
- *Reference:* Nanda et al., *Progress Measures for Grokking*, ICLR 2023 (oral).

### Rung 3 — Toy Models of Superposition
Train a tiny ReLU autoencoder on synthetic sparse features. Sweep sparsity to observe the phase change from monosemantic to superposed features. Plot feature geometry (pentagon/polygon polytopes).

- *Metric:* Feature recovery fraction; mean cosine similarity; phase-change sparsity threshold.
- *Compute:* CPU-minutes to GPU-seconds.
- *Reference:* Elhage et al., *Toy Models of Superposition*, 2022.

### Rung 4 — Circuit Verification via Activation Patching
Find and causally validate a circuit (IOI-style or task-specific) in GPT-2-small or the capstone model. Use activation patching / path patching to confirm each component's role. Evaluate faithfulness and minimality.

- *Metric:* Logit-difference recovery under patching; circuit faithfulness.
- *Compute:* Hours; GPT-2-small inference is cheap.
- *Reference:* Wang et al., *IOI Circuit*, ICLR 2023.

### Rung 5 — Sparse Autoencoder on Residual Stream
Train an SAE (start with ReLU baseline, then BatchTopK/JumpReLU) on activations from the capstone model's residual stream or MLP layer. Build a browsable feature dashboard via `sae-vis`. Report sparsity/reconstruction tradeoff.

- *Metric:* L0 vs. loss-recovered; dead feature rate; interpretability score.
- *Compute:* Moderate — activation harvesting + SAE training over hours to a day.
- *Reference:* Bricken et al., *Towards Monosemanticity*, 2023; Cunningham et al., ICLR 2024.

### Rung 6 (Stretch) — Automated vs. Hand-Found Circuit Comparison
Run ACDC (automated circuit discovery) on the Rung 4 task and compare the recovered subgraph to your manual circuit. Edge-recovery rate, faithfulness comparison, runtime analysis. Where does automation fail?

- *Reference:* Conmy et al., *ACDC*, NeurIPS 2023 (spotlight).

## Pipeline

```
07_capstone/
├── data/              ← synthetic datasets (modular addition, repeated tokens, IOI)
├── src/
│   ├── model.py       ← decoder-only Transformer (from scratch)
│   ├── train.py       ← training loop with W&B logging
│   ├── config.py      ← experiment configurations in one place
│   ├── analysis.py    ← Fourier decomposition, progress measures
│   └── sae.py         ← SAE training wrapper
├── experiments/       ← tracked ablations and sweeps
├── notebooks/         ← exploratory analysis, figure generation
└── writeup.md         ← architectural decisions and final report
```

Shared research code lives in `src/` at the repository root (experiments, reproducibility). Capstone-specific code lives here.

## Architectural Decisions

| Component | Option | Selection (to decide) |
|-----------|--------|----------------------|
| Positional encoding | Sinusoidal / Learned / RoPE | RoPE (default; modern standard) |
| Normalization | Pre RMSNorm / Post LayerNorm | Pre RMSNorm (stable, simpler) |
| MLP activation | GELU / ReLU | ReLU (grokking standard) |
| Attention | MHA / MQA / GQA | MHA (interpretability: each head independent) |
| Weight decay | 0.1 / 1.0 / variable | 1.0 (grokking standard, critical for phase transition) |

Each choice is justified in the writeup.

## Definition of Done

- [ ] Pipeline runs end-to-end for at least one experiment
- [ ] Grokking reproduction with progress measures and Fourier analysis
- [ ] At least one circuit verification (activation patching)
- [ ] Rungs 1–5 completed and results documented in [[portfolio/RESULTS]]
- [ ] Mini-paper (LaTeX) written with abstract, method, results, ablations, limitations, references to primary literature
- [ ] Reproducibility harness: `uv sync && make reproduce` regenerates flagship figures
- [ ] One interactive artifact: SAE feature dashboard on HF Spaces (Rung 5)

## Datasets (synthetic, generated on-the-fly)

| Dataset | Purpose | Generation |
|---------|---------|------------|
| Modular addition pairs | Rung 2 (grokking) | All (a, b, (a+b) mod P) for P=113; split by modulus value |
| Repeated random tokens | Rung 1 (induction heads) | Random sequences from vocabulary of size V; repeated tokens at controlled positions |
| Synthetic sparse features | Rung 3 (superposition) | Randomly active features with controlled sparsity; known ground-truth directions |
| IOI templates | Rung 4 (circuit patching) | Templated English sentences: "When [A] and [B] went to the store, [A] gave a book to" |

## Hardware

All experiments train on a single modern GPU (A100/4090-class or modest cloud instance). No experiment requires industrial-scale pretraining. Tokenizer-adjacent experiments (superposition) run on CPU.

## Reference Resources

### Primary Literature (MI canon)
- Elhage et al., *A Mathematical Framework for Transformer Circuits* (Anthropic, 2021)
- Olsson, Elhage, Nanda et al., *In-context Learning and Induction Heads* (Anthropic, 2022)
- Nanda et al., *Progress Measures for Grokking via Mechanistic Interpretability* (ICLR 2023)
- Wang et al., *Interpretability in the Wild: a Circuit for IOI in GPT-2 small* (ICLR 2023)
- Elhage et al., *Toy Models of Superposition* (Anthropic, 2022)
- Bricken et al., *Towards Monosemanticity: Decomposing Language Models With Dictionary Learning* (Anthropic, 2023)
- Cunningham et al., *Sparse Autoencoders Find Highly Interpretable Features in Language Models* (ICLR 2024)
- Conmy et al., *Towards Automated Circuit Discovery for Mechanistic Interpretability* (NeurIPS 2023)

### Tooling
- TransformerLens (Nanda; maintained by Bryce Meyer)
- SAELens (Bloom, Tigges et al.)
- nnsight / NDIF (Fiotto-Kaufman et al.)
- sae-vis (McDougall & Bloom)
- Neuronpedia (Lin & Bloom)

### Architecture References
- Vaswani et al., *Attention Is All You Need* (NeurIPS 2017)
- Su et al., *RoFormer: RoPE* (2024)
- Karpathy — `nanoGPT`, `minGPT`; *Let's build GPT* (YouTube)
- Raschka — *Build a LLM From Scratch* (Manning)
