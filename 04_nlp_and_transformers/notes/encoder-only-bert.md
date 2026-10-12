---
title: "Encoder-Only Models (BERT) — The Deliberate Gap"
tags: [type/lesson, phase/4, state/consolidated]
created: 2026-10-11
---

# Encoder-Only Models (BERT) — The Deliberate Gap

## What it is

BERT (Devlin et al., 2019) is an encoder-only transformer trained with a
**masked language modelling** objective: corrupt random input tokens and
predict them. Because every position's prediction can attend to *both*
directions, it is not autoregressive.

## Why it exists as a note

It is a gap note. `04_nlp_and_transformers/checklist.md` marks encoder-only
breadth as covered, but the honest description is *deliberately out of scope*,
recorded here so the checkbox is not mistaken for content.

## How it differs from what this repo builds

| | BERT (encoder-only) | This repo (`DecoderOnlyTransformer`) |
|---|---|---|
| Objective | Masked LM — fill in blanks | Next-token prediction |
| Attention | Bidirectional | Causal (masked) |
| Training signal | Every masked position at once | One position per step |
| Output use | Classification, NLI, embeddings | Generation + mechanistic analysis |
| Positional encoding | Learned absolute embeddings | RoPE, parameter-free |

The differences are not cosmetic. Bidirectional attention means a token's
representation depends on tokens *after* it, so there is no "the model knew X
when it predicted position i" decomposition to make — the whole premise of a
progress measure like Nanda et al.'s (grokking's Fourier circuit) is absent. And
a masked objective gives no generalization event to study: there is no
memorisation plateau followed by a drop in validation loss, because the model is
never trained to interpolate a held-out function the way modular addition is.

## Why it is not needed here

The thesis of this repo is: *train a decoder-only transformer from scratch on an
algorithmic task where the ground-truth algorithm is known, then reverse-engineer
what it learned.* Three properties of that thesis each rule BERT out:

1. **The task must be algorithmic and fully specified.** `a + b mod P` and
   repeated-token induction are both synthetic, deterministic, and checkable.
   BERT's natural tasks are natural language.
2. **The mechanism must be extractable.** The Fourier decomposition in
   [[04_nlp_and_transformers/notes/qk-ov-circuits]] works because a 1-layer
   model on P=113 has a low-dimensional, structured embedding. Bidirectional
   attention over natural text has no equivalent closed form.
3. **The circuit must be causal.** Every intervention in
   `src/experiments/exp4_circuit_patching.py` — activation patching, path
   patching, head ablation — is defined in terms of a directed information flow
   that encoder attention does not have.

## Where it would matter

If this work were extended toward applied NLP — fine-tuning, RAG, LoRA — an
encoder would become relevant, because those are encoder-shaped problems. That
extension is recorded as descoped in the Phase 5 checklist and in
`00_meta/02_skill-tree.md`, not silently dropped.

## Links

- [[04_nlp_and_transformers/notes/decoder-only-architecture]] — the architecture this note contrasts with
- [[04_nlp_and_transformers/notes/self-and-multi-head-attention]] — where the causal mask acts
- [[04_nlp_and_transformers/notes/bpe-tokenizer]] — the input side BERT shares with this repo
- [[portfolio/RESULTS]] — the Honesty Ledger, where descopes are recorded rather than hidden

## Open questions

- #question Would a bidirectional variant on the same repeated-token task make the induction circuit *easier* to isolate — more signal, or just less structure?
