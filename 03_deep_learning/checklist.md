---
tags: [type/moc, phase/3, state/consolidated]
---

# Checklist — Phase 3 · Deep Learning

Operational subset of the [[00_meta/02_skill-tree|skill tree]]. Check an item only with an exercise **+** linked proof. Detailed items: [[00_meta/01_roadmap]].

**MI framing:** Grokking is a training-dynamics phenomenon. Understanding optimization (especially weight decay) is essential. The "memorization → circuit formation → cleanup" dynamic is the key insight for the capstone.

## Phase gate
- [x] **Proof passed** → I can move to the next phase. (gate proof: [[03_deep_learning/proofs/gradient-flow-and-architectures]])

## Skills
- [x] Backprop from scratch (micrograd): autograd in pure Python (code: `src/training/micrograd.py`, exercise: [[03_deep_learning/exercises/ex-01-micrograd]]) — proof: [[01_foundations/proofs/chain-rule-and-gradient-check]]
- [x] PyTorch training loop from memory (nn.Module, optimizer, DataLoader) (note: [[03_deep_learning/notes/backpropagation-from-scratch]]) — exercise: [[03_deep_learning/exercises/ex-04-training-loop-and-accumulation]]; proof: [[03_deep_learning/proofs/gradient-accumulation-is-the-large-batch]]
- [x] Optimization: Adam/AdamW, LR schedulers, gradient clipping (note: [[03_deep_learning/notes/training-dynamics-and-grokking]]) — exercise: [[03_deep_learning/exercises/ex-03-adamw-and-schedules]]; proof: [[03_deep_learning/proofs/weight-decay-and-the-cleanup-phase]]
- [x] Regularization: dropout, batch/layer norm, **weight decay — critical for grokking** (same note) — exercise: [[03_deep_learning/exercises/ex-03-adamw-and-schedules]]; proof: [[03_deep_learning/proofs/weight-decay-and-the-cleanup-phase]]
- [x] **Grokking dynamics: delayed generalization, phase transitions, progress measures** (same note) — exercise: [[03_deep_learning/exercises/ex-03-adamw-and-schedules]]; proof: [[03_deep_learning/proofs/weight-decay-and-the-cleanup-phase]]
- [x] RNN cell: implementation from scratch — context for why attention exists (note: [[03_deep_learning/notes/rnn-from-scratch]], exercise: [[03_deep_learning/exercises/ex-02-rnn-and-cnn]]) — proof: [[03_deep_learning/proofs/gradient-flow-and-architectures]]
- [x] CNN: convolution, pooling — breadth (note: [[03_deep_learning/notes/cnn-basics]], same exercise) — exercise: [[03_deep_learning/exercises/ex-02-rnn-and-cnn]]; proof: [[03_deep_learning/proofs/gradient-flow-and-architectures]]
- [x] Training tricks: gradient accumulation (mixed precision not covered) (note: [[03_deep_learning/notes/training-dynamics-and-grokking]]) — exercise: [[03_deep_learning/exercises/ex-04-training-loop-and-accumulation]]; proof: [[03_deep_learning/proofs/gradient-accumulation-is-the-large-batch]]
