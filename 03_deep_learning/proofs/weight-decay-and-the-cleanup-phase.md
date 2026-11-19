---
tags: [type/proof, phase/3, state/review]
authorship: claude
created: 2026-11-17
---

# Proof: why decoupled weight decay drives the cleanup phase of grokking

> **Authorship.** Written by Claude on 2026-11-17, not reconstructed from memory by
> the repository owner. It is a derivation to be checked and re-done, and the
> skills that cite it say so. Companion exercise:
> [[03_deep_learning/exercises/ex-03-adamw-and-schedules]].

## Claim

Under AdamW with weight decay `wd` and learning rate `lr`, a weight that receives no
useful gradient shrinks geometrically at a rate set by `lr * wd` alone. That is
the pressure that removes the memorizing solution once a lower-norm, generalizing
circuit exists, and it is why the Nanda protocol uses a weight decay of 1.0.

## Derivation

**1. The decay in isolation.** With a zero gradient, the AdamW update reduces to
`w <- w * (1 - lr * wd)` (the moment terms contribute nothing once `m` has
decayed away). After `t` steps, `w_t = w_0 * (1 - lr * wd)^t`.

**2. Numbers for the grokking protocol.** The Nanda-protocol manifest records
`lr = 0.001` and `weight_decay = 1.0` over 40000 steps
(`results/grokking_nanda_p113.json`, `args`). The per-step factor is 0.999, so
the half-life of an unused weight is `ln 2 / 0.001`, about 693 steps, and after
the 40000-step budget the factor is `0.999^40000`, about `e^-40`. A weight the
task does not need is gone long before the run ends.

**3. Why it must be decoupled.** In Adam with an L2 penalty the decay enters the
gradient and is divided by `sqrt(v_hat)`. A memorizing weight that kept receiving
large gradients has a large `v_hat`, so its decay is divided down. The same
penalty is therefore weakest on exactly the weights that were fitted most
aggressively. Decoupling removes that dependence: every weight faces the same
`lr * wd`, and only a weight whose gradient keeps pushing back survives. The
exercise measures the two variants diverging on a toy problem.

**4. Why a lower-norm solution wins.** At equilibrium a weight survives only if
its loss gradient balances the decay, `|dL/dw| ~ wd * |w|`. A solution that
reaches low loss with a small norm (the Fourier circuit, which reuses a few
frequencies for every input) needs less gradient support than one that stores
each training example separately. Both fit the training set; only one is cheap
under the decay. This is the mechanism claim of Nanda et al. (2023), not
something this repository re-derives.

## What is and is not backed here

- The two numbers in step 2 are arithmetic on the manifest's `args`.
- That the run grokked is in the manifest: validation accuracy 0.9999 ± 0.0002 on
  3 of 3 seeds (see [[portfolio/RESULTS]]).
- That decay *causes* the transition is **not** tested here. The repository has no
  weight-decay ablation at P=113; the protocol-ablation sweep that would test it is
  the open issue #168. Treat step 4 as the literature's explanation.

## Outcome

- [x] Derivation written and numbers checked against the manifest.
- [ ] Reconstructed from memory by the repository owner. Not done; until it is,
      the skills that cite this file are marked as backed by a derivation written
      by Claude.
