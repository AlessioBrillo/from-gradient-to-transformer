---
tags: [portfolio, essay, grokking, metrics]
published: 2026-11-17
status: verified
---

# The metric that called a circuit dense

This repository once published a negative result for its flagship experiment: a transformer trained on modular addition reached perfect validation accuracy, but its embeddings were "dense" in the Fourier basis, so the sparse Fourier circuit of Nanda et al. was declared absent. The accuracy was real. The verdict was the metric's.

## The reading that failed

The question is how many Fourier frequencies carry the embedding. The first reading counted the frequencies needed to hold 99% of the **L1 mass** of the spectrum (`k_99`). On a clean sparse embedding that count is small. On a real one it is not, because noise spreads a little mass over every bin, and with 113 bins, the tail of a hundred tiny contributions is enough to pass 99% of the total. The reader reported 109 to 110 of 113 frequencies on embeddings whose energy sat in a handful.

The audit that found it did not need the original run. It asked what the metric would say about a vector that is *known* to be sparse plus a little noise, and the answer was "dense". A metric that cannot tell sparse from noisy-sparse says nothing about sparsity.

## The re-measurement

The post-audit reading counts the frequencies that hold 90% of the embedding **energy** (squared magnitude), which noise barely moves. On the Nanda-faithful protocol (40,000 full-batch steps, 3 seeds, GPU) the model reaches validation accuracy 0.9999 ± 0.0002 with its energy in 5.7 ± 1.2 of 56 frequencies, on 3 of 3 seeds ([`results/grokking_nanda_p113.json`](../../results/grokking_nanda_p113.json)). The same embeddings, read by the old metric, still say 109 to 110 of 113.

<!-- manifest: results/grokking_nanda_p113.json -->

The mechanism had been sparse all along; the classifier was wrong. The training, the split, the checkpointing and the manifests were all correct. Only the *reading* was not, and a reading is where a result is easiest to get wrong without anyone noticing, because nothing about it crashes.

## What carried over, and what did not

A control run on a smaller modulus had carried the same defect and was re-measured with the energy metric: two of three seeds sparse, a mixed verdict, not the clean label the first reading had given it. The frequency ablation and the generalization-epoch measurements were unaffected, since they never used the falsified classifier.

## What to take from it

- **Test a metric on inputs whose answer you know.** Plant a sparse vector, add noise, and check the metric still says sparse. Do this before the run, not after the verdict.
- **A negative result needs the same scrutiny as a positive one**, and arguably more: nobody tries to reproduce a null.
- **Separate the instrument from the experiment in the record.** The ledger says what was wrong (the reading), what was right (the training), and what was retracted (the verdict), and keeps all three visible.
- **Publish the retraction where the claim was.** The README, the paper and the skill tree each carried the old sentence; a ratchet of retracted sentences, checked in CI, now stops any of them returning.

The full account is the 2026-10-14 entry of the [Honesty Ledger](../RESULTS.md).
