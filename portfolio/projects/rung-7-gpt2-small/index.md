---
title: "Rung 7: The instrumentation on GPT-2 small"
description: "Run the hand-written hooks, detector and ablation on a pretrained 124M-parameter model, with the criteria frozen first"
tags: [gpt2, induction-heads, ioi, pre-registration, mechanistic-interpretability]
phase: 7
rung: 7
---

**Problem**: every other rung studies a model of at most a few million parameters trained here on a synthetic task. Do the same instruments work on a real pretrained language model, where the literature gives a reference to compare against?

**Methodology**:
- Load GPT-2 small (124M parameters, 12 layers x 12 heads) into a pure-PyTorch implementation with the repository's hookable cache (`src/models/gpt2.py`), and check it against the Hugging Face reference (stage 1, the gate).
- Run the shared induction detector on repeated random tokens and compare to the heads Wang et al. (2022) report (stage 2).
- Zero-ablate those heads and measure the in-context gain (stage 3).
- Score indirect-object prompts (stage 4) and ablate the name movers against 20 random triples of heads (stage 5).
- The five stages and every threshold were frozen in [ADR-0034](../../../docs/adr/0034-gpt2-small-real-model-test.md) before any code touched the weights.

**Key Result**:
<!-- manifest: results/gpt2_small_stage1.json -->
<!-- manifest: results/gpt2_small_stage2.json -->
<!-- manifest: results/gpt2_small_stage3.json -->
<!-- manifest: results/gpt2_small_stage4.json -->
<!-- manifest: results/gpt2_small_stage5.json -->
Four stages pass and four fail (stages 1 to 5 are ADR-0034, stages 6 to 8 ADR-0035). The implementation equals the reference. The detector, written for a 4-head toy model, ranks the two reference induction heads first and second of 144. The model solves the indirect-object task with a mean logit difference of about 2.75. The causal stages did not reproduce: ablating the two induction heads left the in-context gain unchanged while ablating the top ten removed about 77% of it (redundancy), and ablating the three name movers cut the logit difference by about 1.7%, less than random triples do at their 95th percentile. Mean ablation, which the paper used, does not change that (stages 6 and 7 fail), but one-hop path patching ranks the three name movers first, second and third by direct effect on every seed (stage 8 passes). See [RESULTS](../../RESULTS.md#rung-7--the-instrumentation-on-gpt-2-small-pre-registered-adr-0034-instrument-validated-causal-stages-not-reproduced).

**Reproduce**: `uv run --extra real python -m src.experiments.exp7_gpt2_small` (about 15 minutes on CPU after a one-time weight download).

**Limitations**:
- Zero ablation is off-distribution and the paper used mean ablation; backup name movers can also compensate. A stage 5 failure is weaker evidence than a stage 1 failure, as the ADR said in advance.
- The repository does not claim the indirect-object circuit. Path patching and mean ablation on GPT-2 would be a new pre-registered ADR and have not been run.
- Only the single model GPT-2 small; no other checkpoint was tried.

**Links**: [[portfolio/RESULTS]], [[07_capstone/_MOC]].
