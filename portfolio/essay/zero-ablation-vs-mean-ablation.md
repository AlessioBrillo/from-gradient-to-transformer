---
tags: [portfolio, essay, mechanistic-interpretability, ablation, pre-registration]
published: 2026-11-21
status: verified
---

# Zero ablation, mean ablation, and the stage that passed anyway

On GPT-2 small, two causal stages failed. Zero-ablating the two induction heads left the in-context gain unchanged, and zero-ablating the three name movers lowered the logit difference by under 2%. The easy story was that the method was to blame: zero ablation pushes a head's output off-distribution, and the paper being reproduced used mean ablation. So that was tested, in a second pre-registration written before any number existed.

## What was frozen

Same prompts, same seeds, same thresholds as the first round, with two changes the first round had taught: the control set must not contain the heads being ablated, and each stage gets its own wall clock. Mean ablation replaced the zero. A third stage was added, one-hop path patching, because the paper localised the name movers that way and not by ablation.

## What came out

- Mean-ablating the two induction heads lowered the in-context gain by 0.8%. FAIL.
- Mean-ablating the three name movers lowered the logit difference by 12.8%, below what random triples reach at their 95th percentile (22.1%). FAIL.
- Path patching ranked the three name movers first, second and third by direct effect, on all three seeds, and the two heads the paper says oppose the correct name came out negative. PASS.

The obvious excuse did not hold: the method change did not rescue the ablation stages. And the stage that passed says something the other two cannot: a head can write the answer directly and still be absent from an ablation result, because other heads take over when it is removed. That is a reading, not a result. Nothing here tested for backup heads.

## What nearly went wrong, twice

The run takes about an hour on a CPU and was killed for memory before it wrote a single file. The fix was to save one file per finished seed and resume from them. Then a run finished, and its manifests said `git_sha: unknown, git_dirty: true`, because it had run in a container without a checkout. The repository's own check refuses such evidence, and the temptation to edit two fields into place was there and was wrong: the numbers would have been right and the provenance still false. The run was repeated in a clean clone instead, and agreed with the discarded one to every digit shown.

## What to take from it

- **Pre-register the follow-up too.** The second round had thresholds before it had data, so a failure could not be reinterpreted into a pass.
- **Report the method change that did not help.** "We tried the better method and it did not rescue the result" is information.
- **A passing stage and two failing ones are not a circuit.** Say which claim each supports and stop there.
- **Resumable beats fast.** An hour-long run that saves nothing until the end will eventually be killed.
- **Never repair provenance by hand.** Re-run it.

The full account is in the [Honesty Ledger](../LEDGER.md), and the numbers are in [RESULTS](../RESULTS.md).
