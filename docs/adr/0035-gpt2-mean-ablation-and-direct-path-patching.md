---
adr: 0035
title: Re-ask the two failed GPT-2 stages with mean ablation, and measure the direct path of the name movers
date: 2026-11-19
status: ACCEPTED
phase: 7
tags: [type/ledger, phase/7]
---

## Context

ADR-0034 ran five stages on GPT-2 small. Three passed. The two causal ones failed:

- **Stage 3.** Zero-ablating the induction heads 5.5 and 6.9 left the in-context gain
  unchanged: it rose by about 0.6% (a drop of -0.0062) against a required fall of 10%.
- **Stage 5.** Zero-ablating the name movers 9.6, 9.9 and 10.0 cut the logit difference by
  about 1.7% against a 30% threshold, less than random triples do at their 95th percentile
  (18.5%).

ADR-0034 said in advance that these failures are weak evidence: zero ablation is
off-distribution (the paper it follows used mean ablation) and backup heads can compensate.
Two defects of the instrument were also found in review and are not yet corrected:

1. The stage 3 control ablates the stage 2 top 10, which **contains the two heads under
   test**, so it measures the size of the redundant family and not the specificity of the two.
2. The five stage manifests share one wall-clock figure instead of recording their own.

The 0034 manifests stay as they are, with their failures: this ADR **adds** stages and does
not supersede 0034. It is written before any code that mean-ablates or path-patches GPT-2.

## Decision

Add three stages, 6 to 8, run on the same model, device and seeds as ADR-0034 (CPU,
float32, eval mode, evaluation seeds 0, 1, 2). Each is reported PASS or FAIL on its own.
Stage 1 of ADR-0034 still gates everything: the stages here are not run if it fails.

### Mean ablation, defined

The output of a head is its attention-weighted values, `probs @ v`, before the output
projection. **Mean ablation** replaces that tensor, for the ablated heads, with its mean over
a **reference set**, taken position by position. The reference set is disjoint from the
evaluation data:

- *Induction stages*: 300 sequences of the stage 2 form (a random prefix of 50 tokens,
  repeated), drawn from seeds 100, 101 and 102.
- *Indirect-object stages*: 300 prompts from the stage 4 generator, seeds 100, 101 and 102.
  Prompts are grouped by template and the mean is taken per template, because the token
  positions align only within a template.

### Stage 6: the induction heads are causally used (mean ablation)

Same data and measure as ADR-0034 stage 3: the in-context gain is the mean next-token loss
over the first copy minus the mean over the second. Mean-ablate 5.5 and 6.9.
PASS if, averaged over seeds, **both**:

- the gain falls by at least **10%**, and
- that fall exceeds the 95th percentile of the falls from **20 random pairs** of heads
  (generator seed 1234, drawn from the 142 heads other than 5.5 and 6.9).

Reported without a criterion: the same measure for the stage 2 top 10 **excluding** 5.5 and
6.9 (this replaces the contaminated control of stage 3), and for the stage 2 top 10 as a
whole.

### Stage 7: the name movers matter for the task (mean ablation)

Same prompts and measure as ADR-0034 stage 5. Mean-ablate 9.6, 9.9 and 10.0.
PASS if the relative fall in mean logit difference is at least **30%** and exceeds the 95th
percentile of the falls from **20 random triples** (generator seed 1234, drawn from the 141
other heads).

### Stage 8: the direct effect of each head on the answer (path patching, one hop)

This is path patching restricted to the one path that needs no re-running of the network:
**head output to the unembedding, skipping every later component.**

*Corrupted prompts.* For each stage 4 prompt, replace the repeated name S, in the final
clause, by a third name C that is neither of the two names of the opening clause
(the "ABC" corruption of Wang et al.). All names are one token, so clean and corrupted
prompts have equal length. C is drawn from the stage 4 name list with the seed's generator.

*Effect of a head `h`.* Run the clean and the corrupted prompt. At the last position, add to
the clean final residual stream (the output of the last block, before the final LayerNorm)
the difference between the corrupted and clean contribution of `h`, namely
`(z_h^corrupt - z_h^clean) W_O^h`, then apply the final LayerNorm and the unembedding. The
effect is

`e_h = (LD_clean - LD_patched(h)) / LD_clean`,

where `LD` is the mean logit difference `logit(IO) - logit(S)` over the seed's prompts.
All 144 heads are scored. A positive `e_h` means the head's direct path pushes towards the
correct name.

PASS if, **on every seed**, each of 9.6, 9.9 and 10.0 is among the **10** heads with the
largest `e_h` (ties count against the target, as in `rank_of`).

Reported without a criterion: the full top 10; the summed `e_h` of the three name movers;
and `e_h` of the negative name movers 10.7 and 11.10 of the reference, which the paper
reports as pushing against the correct name, so their sign is a check on the method.

## What is reported

One manifest per stage, `results/gpt2_small_stage6.json` to `stage8.json`, each with **its
own wall clock**, written by `ResultsManifest`, plus a Honesty Ledger entry that states the
outcome of each stage, FAILs included. The word "reproduced" is used only for a stage that
passes. Two stages passing or failing do not amount to "the circuit": that claim needs the
multi-hop paths below and is not made here.

## Implementation note

Mean ablation needs a replacement tensor per head and the direct path needs each head's
output before the projection, so `src/models/gpt2.py` gains a cached `blocks.{i}.attn.z`
and an `ablate_mean` context manager. The one-hop effect is a closed form on cached
tensors, so it is implemented in the experiment module and **does not** generalise the
multi-path code of `exp4_circuit_patching.py`; that refactor is deferred until a multi-hop
stage needs it. Parity with the Hugging Face reference (stage 1) is re-run after the
change, and a unit test checks that mean-ablating with the head's own mean over a batch of
identical inputs equals no ablation.

## What would change this ADR

Nothing after the first measurement. If a stage turns out to be ill-posed rather than
failed, the correction is a new dated ADR that supersedes this one and keeps it visible.

## Not in scope

- Multi-hop path patching (S-inhibition, induction and duplicate-token heads feeding the
  name movers' queries, keys and values). A separate ADR, only if stage 8 passes.
- Sparse autoencoders on GPT-2 (ADR-0036).
- Changing or re-running ADR-0034's stages: their manifests are the record.
