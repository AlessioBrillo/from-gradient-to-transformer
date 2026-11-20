---
tags: [portfolio, model-card]
---

# Model Card — Interpretability Micro-Transformers

This card describes a *family* of small models, one per experiment, not a single
released checkpoint. Every figure below is read from a tracked run manifest
(`n_parameters` and `args`); the 2026-11-16 revision replaced an earlier card
that described models this repository never trained (see the
[Honesty Ledger](LEDGER.md) convention: the record follows the
manifests, not the plan).

## Model Overview

- **Name**: micro-transformers (from-gradient-to-transformer)
- **Architecture**: decoder-only transformers and two toy autoencoders, all
  written from scratch in PyTorch, with hand-rolled hooks and caches
- **Scale**: from 120 parameters (the superposition toy model) to about 4.3
  million (the capstone) for models trained here, plus one pretrained model that
  was not (GPT-2 small, 124 million, Rung 7); see the table below
- **Tokenizer**: none for the models trained here, which use integer token ids from a
  synthetic vocabulary. Rung 7 uses GPT-2's own tokenizer. A BPE tokenizer exists in `src/models/bpe_tokenizer.py`
  as a curriculum exercise; no experiment uses it
- **Language**: no model trained here has seen natural-language text. English enters only
  through Rung 7's pretrained GPT-2, which this repository did not train
- **Weights**: not distributed. Checkpoints are run products; the manifests in
  `results/` are the record
- **License**: MIT

## Models and Training Data

| Experiment | Model | Parameters | Task |
|------------|-------|------------|------|
| Rung 1 — Prefix copying | Attention-only, 2 layers, 4 heads per layer, d_model 64, vocabulary 2048, sequence length 64 | 299392 | Random token sequences whose second half repeats the first (`prefix + prefix`) |
| Rung 1b — Content-based copying | Same architecture, vocabulary 256 | 70016 | Variable-distance copy blocks: the distance to the previous occurrence changes per block, so a fixed offset cannot solve it |
| Rung 2 — Grokking ★ | 1 layer, 4 heads, d_model 128, d_mlp 512 (Nanda et al. 2023 protocol) | 225792 | Modular addition, modulus 113; the split holds out random *equations* |
| Rung 3 — Superposition | Toy ReLU autoencoder, 20 features into 5 dimensions | 120 | Synthetic sparse features with known ground truth |
| Rung 4 — Circuit patching | No model of its own: it analyses Rung 1's trained checkpoint | 299392 | The Rung 1 task, with clean and counterfactual batches |
| Rung 5 — Sparse autoencoder | Dictionary of 512 features on a 64-dimensional residual stream | 66112 | Activations harvested from Rung 1's checkpoint on its own task |
| Rung 7 — Instrumentation on a real model | GPT-2 small, pretrained (Radford et al. 2019), loaded into `src/models/gpt2.py`: 12 layers, 12 heads, d_model 768 | 124,439,808 | Repeated random tokens (induction) and indirect-object prompts; nothing is trained |
| Capstone | 4 layers, 8 heads, d_model 256, d_mlp 1024, RMSNorm + RoPE (`src/models/decoder_only_transformer.py`) | 4259584 | Modular addition and prefix copying, trained jointly |

The manifests behind this card: Rung 1
<!-- manifest: results/induction_standard.json -->, Rung 1b
<!-- manifest: results/induction_content.json -->, Rung 2
<!-- manifest: results/grokking_nanda_p113.json -->, Rung 3
<!-- manifest: results/exp3_superposition.json -->, Rung 4
<!-- manifest: results/exp4_standard.json -->, Rung 5
<!-- manifest: results/exp5_real_activations.json -->, capstone
<!-- manifest: results/capstone_20k.json -->, Rung 7
<!-- manifest: results/gpt2_small_stage2.json -->.

## Intended Use

Research and educational demonstration of mechanistic interpretability
techniques: reverse-engineering the algorithms small transformers learn. Not
intended for production use, and not usable as language models.

## Evaluation

Evaluation here is causal and structural rather than benchmark-based. These are
the metrics the experiments actually report; the values are in
[RESULTS](RESULTS.md).

| Experiment | Primary metric | Supporting metrics |
|------------|----------------|--------------------|
| Rung 1 / 1b | Attention mass on the copy source (offset mass, content mass) | K-composition score, copy accuracy against a fixed-offset baseline, single-head ablation drop |
| Rung 2 | Validation accuracy | Number of Fourier frequencies holding most of the embedding energy (`k_energy_90`) |
| Rung 3 | Number of features represented | Feature geometry |
| Rung 4 | Head-ablation effect | Path-patching effect |
| Rung 7 | Attention mass on the induction key; logit difference between the indirect object and the subject | Head ablation against a random-triple control; parity with a reference implementation |
| Rung 5 | Fraction of variance explained | L0 (active features), dead-feature fraction |

Rungs 1 to 4 and the capstone report mean ± std over three seeds. Rung 5 is a
single-seed run.

## Limitations

- **Scale**: the largest model trained here has about 4.3 million parameters
  (pretrained GPT-2 small, 124M, is used for inference and ablation only). Circuits
  in production-scale models may be qualitatively different.
- **Task specificity**: every task is algorithmic and synthetic, and Rung 7 only tests
  instruments on a pretrained model. Its causal stages did not reproduce, so nothing
  here is evidence about natural-language circuits.
- **Method limitations**: activation patching can mislead through
  normalization-denominator effects, and SAE features can be illusory (see
  Makelov, Lange & Nanda 2023).
- **Open results**: Rung 1b's per-head rule confirms no head on any of three
  seeds, and Rung 5's dictionary has most of its features dead. Both are
  reported as measured in [RESULTS](RESULTS.md).
- See the mini-paper's limitations section for the full discussion.
