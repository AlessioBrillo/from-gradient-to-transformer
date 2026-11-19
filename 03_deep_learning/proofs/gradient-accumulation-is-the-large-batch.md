---
tags: [type/proof, phase/3, state/review]
authorship: claude
created: 2026-11-17
---

# Proof: gradient accumulation equals the large batch (and when it does not)

> **Authorship.** Written by Claude on 2026-11-17, not reconstructed from memory by the
> repository owner. Companion exercise:
> [[03_deep_learning/exercises/ex-04-training-loop-and-accumulation]].

## Claim

Accumulating gradients over `k` equal-sized micro-batches, each loss divided by `k`,
produces the same gradient as one batch of `k` times the size, whenever the loss is an
average of per-example terms. When the loss is not, it does not.

## Proof

Let the large batch be `B = B_1 ∪ … ∪ B_k` with `|B_i| = m`, so `|B| = km`, and let
`ℓ(x; θ)` be the per-example loss.

```
∇ L_B(θ) = ∇ ( 1/(km) Σ_{x∈B} ℓ(x;θ) )
         = (1/k) Σ_i  ( 1/m Σ_{x∈B_i} ∇ℓ(x;θ) )
         = (1/k) Σ_i  ∇ L_{B_i}(θ)
```

Calling `backward()` on `L_{B_i} / k` for each `i` adds exactly the last line into
`.grad`, because PyTorch accumulates into `.grad` by default. Without the division the
sum is `k · ∇L_B`: a step `k` times too long for SGD. The exercise measures a ratio of
4.00 for `k = 4`. For Adam the scale cancels in the update, which is why the bug is
quieter there.

## Where it breaks

- **Unequal micro-batches.** The last step above needs `|B_i|` equal. With unequal sizes
  the average of averages is not the global average.
- **Normalisation by token count.** A language-model loss averaged per *token* over
  sequences of different length is a weighted average. The micro-batch losses must be
  weighted by their token counts, not divided by `k`.
- **Batch-dependent layers.** BatchNorm computes statistics over the micro-batch, so the
  forward pass itself differs from the large batch. LayerNorm and RMSNorm, which this
  repository's models use, are per-example and are not affected.
- **Dropout and other randomness** differs between micro-batches unless the random
  stream is arranged to match.

## What is backed here

The identity holds to 0.0 in the exercise's test
(`test_accumulating_four_micro_batches_equals_one_large_batch`), on a model with no
BatchNorm and no dropout. The failure modes in the list are standard consequences of
the derivation; this repository does not test them.

## Outcome

- [x] Derivation written; the equal-size case checked by a test.
- [ ] Reconstructed from memory by the repository owner. Not done.

## See also

- [[03_deep_learning/notes/training-dynamics-and-grokking]] - where the optimizer settings used by the grokking runs are discussed
- [[03_deep_learning/proofs/weight-decay-and-the-cleanup-phase]] - the optimizer-side companion to this derivation
