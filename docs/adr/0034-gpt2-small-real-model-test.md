---
adr: 0034
title: Test the hand-written instrumentation on GPT-2 small, with the criteria frozen first
date: 2026-11-17
status: ACCEPTED
phase: 7
tags: [type/ledger, phase/7]
---

## Context

Every result in this repository comes from a model of at most 4.3 million parameters
trained on a synthetic task. The hooks, the attention-mass detector, head ablation and
patching are all written by hand. The open question is whether they work on a real
pretrained language model, where the literature gives a reference to compare against.
A method that only ever meets toy models has not been shown to be a method.

This ADR is written **before any code that touches GPT-2 weights**. Its git timestamp
is the pre-registration: the thresholds below are not adjusted after seeing a number.

## Decision

Add one rung, **Rung 7**: run the existing instruments on GPT-2 small (124M parameters,
12 layers, 12 heads per layer, `openai-community/gpt2`, Radford et al. 2019) in five
stages. Each stage is reported as PASS or FAIL on its own. **Stage 1 gates the rest**:
if it fails, nothing after it is reported as a result.

Model code: a pure-PyTorch GPT-2 in `src/models/gpt2.py` (learned positions, LayerNorm,
GELU, tied embeddings), with the same hookable cache protocol as the other models so the
shared detector in `src/experiments/induction_detection.py` applies unchanged. The
Hugging Face `transformers` package is used for two things only: loading the weights and
tokenizing text, and as the reference for stage 1. It is an optional `real` extra.

Everything runs on CPU, float32, in eval mode.

### Reference

Wang, Variengien, Conmy, Shlegeris & Steinhardt, *Interpretability in the Wild: a
Circuit for Indirect Object Identification in GPT-2 small* (arXiv:2211.00593). The heads
below are as that paper reports them, read from its text on 2026-11-17 (layer.head):

| Class | Heads |
|---|---|
| Name movers | 9.6, 9.9, 10.0 |
| Induction | 5.5, 6.9 |

The paper reports the circuit at 87% faithfulness with a model logit difference of 3.56.
Those numbers are context, not targets: this ADR uses different, simpler prompts.

### Stage 1: parity with the reference implementation (gate)

On 8 fixed prompts (listed in the experiment module), the maximum absolute difference
between this implementation and `transformers.GPT2LMHeadModel` is at most **1e-3** for
(a) the logits and (b) every layer's residual stream (`hidden_states`).
PASS needs both.

### Stage 2: induction heads by attention mass

Inputs: for each seed in {0, 1, 2}, 100 sequences made of a random prefix of 50 tokens
followed by the same prefix again (length 100, no BOS), tokens drawn uniformly from ids
0 to 50255 (the end-of-text id 50256 is excluded). Score: the mass on the induction key
`q - 49`, computed by `head_masses` of the shared detector, which reads the layout from
the tokens. PASS if, **on every seed**, both heads 5.5 and 6.9 are among the 10 highest
of the 144 heads by this score **and** each scores at least **0.3** (the repository's
existing screen threshold). The ten highest heads are also reported in full; heads
outside the reference set are exploratory and carry no criterion.

### Stage 3: induction heads are causally used

On the same sequences, the in-context gain is the mean next-token loss over the first
copy minus the mean over the second copy. Zero-ablate the output of heads 5.5 and 6.9
(the same `head_mask` mechanism as Rung 4). PASS if the gain falls by at least **10%**
relative to the unablated model, averaged over seeds. A control, ablating the ten
highest-scoring heads of stage 2, is reported and has no criterion. The criterion is
modest on purpose: GPT-2 small has more induction heads than the two in the reference,
so a small effect from two of them is the expected outcome, and a null is informative.

### Stage 4: the model solves the task

Indirect-object prompts from three templates, each in the ABBA and BABA orders:

1. `When {A} and {B} went to the store, {B} gave a drink to`
2. `Then, {A} and {B} had a long argument, and afterwards {B} said to`
3. `After {A} and {B} got to the school, {B} gave a book to`

The names are drawn from a fixed list of common first names, kept only if each is a
single GPT-2 token with a leading space; any name dropped is reported. The logit
difference is `logit(IO) - logit(S)` at the last position, where IO is the name that is
not repeated and S the one that is. 100 prompts per seed, 3 seeds. PASS if the mean
logit difference is at least **2.0** and it is positive on at least **90%** of prompts.

### Stage 5: name movers matter for that task

Zero-ablate heads 9.6, 9.9 and 10.0 on the stage 4 prompts. The control is 20 random
triples of heads drawn without replacement (a fixed generator seed), each ablated the
same way. PASS if the relative fall in mean logit difference from the name movers is at
least **30%** and exceeds the 95th percentile of the control falls.

Zero ablation is off-distribution and Wang et al. used mean ablation; backup name movers
can also compensate. A FAIL here is therefore weaker evidence against the method than a
FAIL in stage 1, and the report says so.

## What is reported

One manifest per stage (`results/gpt2_small_stage<N>.json`, seeds 0 to 2 where stages
use seeds), written by `ResultsManifest`, and a Honesty Ledger entry that states each
stage's outcome, including FAILs. The word "reproduced" is used only for a stage that
passes, and "the circuit" is not claimed on the strength of stages 4 and 5 alone.

## What would change this ADR

Nothing after the first measurement. If a stage turns out to be ill-posed (not merely
failed), the correction is a new dated ADR that supersedes this one and keeps this one
visible, in the manner of ADR-0032 and ADR-0033.

## Not in scope

- Training anything.
- Path patching, attribution patching and SAEs on GPT-2: separate rungs if this one
  lands.
- A comparison with TransformerLens. Stage 1 compares to the Hugging Face reference; a
  TransformerLens comparison would be a different, optional check.
