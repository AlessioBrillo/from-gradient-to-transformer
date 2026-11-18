---
tags: [portfolio, essay, reproducibility, seeds]
published: 2026-11-17
status: verified
---

# What a seed pins

A run reports `seed = 1`. What has been fixed?

In this repository the honest answer, until 2026-11-17, was: the data, and the order the batches arrive in, but **not the model's starting weights**. Two commands of one configuration printed different results, and both were reproducible to the digit. It took a contradiction between two manifests to see it.

## The contradiction

Rung 3 trains a toy autoencoder to study superposition. Two tracked manifests record the same nominal configuration: sparsity 0.01, 600 epochs, 8000 samples, batch 512, seeds 0, 1, 2. One says 19.67 ± 0.47 features represented, the other 20.00 ± 0.00. Two code paths of the same experiment should not disagree about one configuration.

## The cause

The model was built *before* `set_seed`, and the seeding happened inside the training function, one line after the weights had been drawn. The data had its own generator, and the training was seeded, but the initialization came from whatever state the global random stream happened to be in. That state depended on what ran before:

- the single-sparsity path seeded once at the start, so the first seed's model was drawn from a pinned state and each later seed's model after the previous seed's training had consumed the stream;
- the sweep path built nine models per seed, one per sparsity level, so the model at sparsity 0.01 was the sixth in line, a different position in the stream.

Reconstructing both positions reproduced both numbers. Worse, seed 0 alone and seed 1 alone built **identical** initial weights, because a fresh process starts from the same state: "seed N" selected a data set and a batch order, not a starting point.

## Why nothing failed

Each command reproduced its own manifest exactly. The defect was not non-determinism; it was that two commands had been *published side by side as if they measured the same thing*. A reproducibility check that re-runs a command and compares the output cannot see this, because the command agrees with itself.

## The fix, and the test that holds it

Seed immediately before the model is constructed, in one helper per experiment. The test uses the audit's own instrument: a digest of the initial weights. It asks that a seed's digest be the same when the seed is built alone, after another seed, after a throwaway model has consumed the stream, and at every level of the sweep. It fails on the old code and passes on the new.

The tracked manifests of the three affected experiments were recorded before the fix. They are not edited: they remain, renamed `*_pre_seedfix.json`, the record of what the old code measured. The experiments were then re-run.

For Rung 3 the contradiction that started this closed: with the model seeded before it is constructed, the single-sparsity path and the sweep path both report 20.00 ± 0.00 features represented at sparsity 0.01, where before they reported 19.67 ± 0.47 and 20.00 ± 0.00. That agreement is the diagnosis confirmed, not merely a fix: the two numbers differed because of where the model sat in the random stream, and removing that dependence removed the difference. The phase transition itself did not move.

## What to take from it

- **A seed is a claim about a specific object.** Say which: the data, the batch order, the initialization, the dropout masks. Then test each.
- **Pin the initialization with a digest.** Hash the weights before the first step; assert it is equal across the ways of reaching the same configuration.
- **Compare across code paths, not only across repeats.** Two paths to "the same" configuration are an experiment in themselves.
- **Do not edit the old record to match the new code.** Keep it, label it, and say what changed.
