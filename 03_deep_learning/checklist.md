---
tags: [checklist, phase/3]
---

# Checklist — Phase 3 · Deep Learning

Operational subset of the [[00_meta/02_skill-tree|skill tree]]. Check an item only with an exercise **+** linked proof. Detailed items: [[00_meta/01_roadmap]].

**MI framing:** Grokking is a training-dynamics phenomenon. Understanding optimization (especially weight decay) is essential. The "memorization → circuit formation → cleanup" dynamic is the key insight for the capstone.

## Phase gate
- [ ] **Proof passed** → I can move to the next phase.

## Skills
- [x] Backprop from scratch (micrograd): autograd in pure Python (code: `src/training/micrograd.py`, exercise: [[03_deep_learning/exercises/ex-01-micrograd]])
- [x] PyTorch training loop from memory (nn.Module, optimizer, DataLoader) (note: [[03_deep_learning/notes/backpropagation-from-scratch]])
- [x] Optimization: Adam/AdamW, LR schedulers, gradient clipping (note: [[03_deep_learning/notes/training-dynamics-and-grokking]])
- [x] Regularization: dropout, batch/layer norm, **weight decay — critical for grokking** (same note)
- [x] **Grokking dynamics: delayed generalization, phase transitions, progress measures** (same note)
- [ ] RNN cell: implementation from scratch (context for why attention exists)
- [ ] CNN: convolution, pooling (breadth)
- [ ] Training tricks: gradient accumulation, mixed precision (note: [[03_deep_learning/notes/training-dynamics-and-grokking]])
