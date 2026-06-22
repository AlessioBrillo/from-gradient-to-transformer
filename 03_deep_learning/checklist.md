---
tags: [checklist, phase/3]
---

# Checklist — Phase 3 · Deep Learning

Operational subset of the [[00_meta/02_skill-tree|skill tree]]. Check an item only with an exercise **+** linked proof. Detailed items: [[00_meta/01_roadmap]].

**MI framing:** Grokking is a training-dynamics phenomenon. Understanding optimization (especially weight decay) is essential. The "memorization → circuit formation → cleanup" dynamic is the key insight for the capstone.

## Phase gate
- [ ] **Proof passed** → I can move to the next phase.

## Skills
- [ ] Backprop from scratch (micrograd): autograd in pure Python
- [ ] PyTorch training loop from memory (nn.Module, optimizer, DataLoader)
- [ ] Optimization: Adam/AdamW, LR schedulers, gradient clipping
- [ ] Regularization: dropout, batch/layer norm, **weight decay — critical for grokking**
- [ ] **Grokking dynamics: delayed generalization, phase transitions, progress measures**
- [ ] RNN cell: implementation from scratch (context for why attention exists)
- [ ] CNN: convolution, pooling (breadth)
- [ ] Training tricks: gradient accumulation, mixed precision
