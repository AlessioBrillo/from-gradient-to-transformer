---
adr: 0033
title: The induction claim needs a task without the fixed-offset shortcut
date: 2026-10-20
status: ACCEPTED
phase: 7
tags: [type/research, phase/7, research/experiment]
consumes: [ADR-0032]
---

## Context

ADR-0032 established two facts on 2026-10-19/20:

1. the detector behind every "0 / N induction heads" number this repository
   published measured the **previous-token** offset, so those numbers were
   statements about the detector, not about the model;
2. with the corrected detector, the standard-scale run on the periodic
   (`prefix + prefix`) task finds a **prefix-copying** head: the copy
   follows a fixed offset, not the previous occurrence of the same token.

The second fact is not a bug that more compute would fix. On the periodic
task the previous occurrence of `x[q]` is *always* at `q - L`, so
"attend to `q - L + 1`" and "attend to the token after the previous
occurrence of the same token" are **the same function on the training
distribution**. The task does not contain the question the rung asks. Every
further measurement on that checkpoint can only re-derive the same
ambiguity.

The rung's headline ("induction heads emerge and I show, causally, that
they implement `[A][B]...[A] -> [B]`") therefore stays unearned, and Rungs 4
and 5 inherit the ambiguity: the circuit they measured is a prefix-copying
circuit, and the dictionary they learned was learned on a model that never
had to match content.

## Decision

1. **A second task is added**: the *variable-distance* task
   (`src/experiments/induction_tasks.py`), in which the repeats sit at
   distances that change from block to block and from sequence to
   sequence. The fixed-offset shortcut does not exist on it: the best single
   fixed offset explains 17.6% of the copy queries, while a content-matching
   head can reach 100%.
2. **The task is well posed by construction**: every token appears at most
   twice, so the previous occurrence is unique; the copy queries are derived
   from the tokens alone, not from the generator; the filler tokens are
   distinct and unpredictable, so the copy queries are the only learnable
   positions.
3. **The detector becomes task-agnostic** (`CopyLayout` in
   `src/experiments/induction_detection.py`): the periodic path keeps its
   historical query sets bit-for-bit, and the variable path measures the
   content hypothesis on the copy queries. The fixed-offset mass is now
   *measured* (`offset_profile`) instead of assumed, so the positional
   ceiling is a number in the manifest.
4. **The naming test changes with the task**: on the periodic task it is the
   off-distribution dissociation probe (ADR-0032); on the variable task the
   dissociation is native — the training distribution itself separates the
   two mechanisms — so `run_content_vs_offset_probe` measures it in
   distribution.
5. **The experiment is pre-registered** in
   [[07_capstone/notes/variable-distance-induction-preregistration]]:
   thresholds, seeds, budget, decision rule and falsifiers are frozen
   before the run, and a negative is reported as a negative.
6. **The periodic task is kept.** It is the control: the same detector, the
   same budget, the same interventions. The two results are reported side
   by side, and the periodic one keeps its name — *prefix-copying head*.

## Consequences

- Rung 1 gets a verdict that can be positive or negative, and either way it
  is a verdict about a mechanism rather than about a detector.
- Rungs 4 and 5 can be re-run on a checkpoint whose head is (or is not) a
  content head; until then their numbers describe the prefix-copying
  circuit, and the record says so.
- The cost of the new task is that it is harder than the periodic one: only
  16 of the 63 predicted positions are learnable, against roughly half on
  the periodic task. A copy accuracy around 0.25 is therefore *not* a
  failure on this task, and the headline metric is the accuracy on the copy
  queries, never the overall accuracy.
- The data generator is 3x slower than the periodic one (0.66 s per 8192
  sequences against 0.21 s), about 14% of an epoch's cost. That is accepted
  rather than optimized, because the budget's wall clock is dominated by
  the training step.

## Links

- [[docs/adr/0032-induction-detector-and-the-positional-shortcut]] — the
  audit this decision follows from.
- [[07_capstone/notes/variable-distance-induction-preregistration]] — the
  frozen protocol.
- [[portfolio/RESULTS]] — where the verdict will be recorded.
