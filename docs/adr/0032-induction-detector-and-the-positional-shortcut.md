---
adr: 0032
title: The induction detector was wrong, and the task admits a positional shortcut
date: 2026-10-20
status: ACCEPTED
phase: 7
tags: [type/research, phase/7, research/experiment]
consumes: [ADR-0031]
---

## Context

Two facts, established on 2026-10-19 and 2026-10-20, that change what this
repository can claim about Rung 1.

**1. The detector measured the wrong circuit.** `exp1`'s detector measured the
attention mass on the offset `q -> q-1` — the *previous token* — and called it
"diag+1"; the induction (copy) offset on this task's `prefix + prefix` layout is
`q -> q-L+1`. `exp4`'s detector measured `attn_probs.diagonal(offset=1)`, the
strict upper triangle of a causal softmax, which is identically zero. The
planted tests planted the same wrong pattern, so a test that encoded the bug
passed the bug, and every "0 / N induction heads" figure the repository
published was a statement about the detector rather than about the model.

**2. The task hands the model a shortcut.** With the corrected detector, the
standard-scale GPU run (issue #169, three seeds, T4) confirms **three heads per
seed** with a copy-offset mass of **0.945 ± 0.004** — the retracted "0 / 8"
really was a detector artifact. But:

- the confirmed heads are in the **first layer**; the K-composition between
  layers is **0.06–0.11**, below the 0.4 confirmation bar, and the L0
  duplicate-token mass is **0.017–0.022** — there is **no two-step circuit**;
- the dissociation probe (a batch whose second half is a *permuted* copy of the
  prefix, so the content target and the fixed offset point at different keys)
  puts the model's mass on the **position** target (0.90) and not on the content
  target (0.03), on **3/3 seeds**.

The reason is structural, not a property of the model: on a perfectly periodic
sequence the previous occurrence of the current token is *always* at `q-L`, so
"copy from the previous occurrence of the same token" and "copy from the fixed
offset `L-1`" are **the same function** on this task. No in-distribution
measurement can separate them — not the attention mass, not the K-composition
score (which reads the previous occurrence from a layer-0 head's argmax, which
on a periodic task is the same position). Only the off-distribution probe can.

## Decision

1. **The claim is renamed.** What this repository measures on this task is a
   *prefix-copying head at offset L-1*, not an induction head. The wording in
   `portfolio/RESULTS.md`, the paper and the notes follows the measurement. The
   Olsson-style headline ("induction heads emerge and implement
   `[A][B]...[A]->[B]`") is **not earned** by a periodic task and is not claimed
   anywhere.
2. **The retraction stands.** Every "0 / 8" and "0 / 4" head count is retracted
   as uninterpretable. The accuracy comparisons those documents support (the
   fixed-vs-fresh-batches result) are unaffected and stay.
3. **The content-based task is a v1.1 task-design increment, not a scale
   increment.** Repeats at *varying* distances (so the copy distance is not
   predictable from the position) are the only way to make the induction claim
   testable here; no amount of epochs or parameters removes a shortcut the task
   hands the model. It is scheduled as a new experiment with its own
   pre-registration, not folded into this one.
4. **The cascade is one model.** `exp4 --from-checkpoint` analyses Rung 1's
   checkpoint instead of training a second model under the same claim; the
   parity test covers the batch size and the optimizer-step count, not just the
   flags both presets happened to set.
5. **The phase-diagram sweep moves to v1.1** (issue #168 reopened) with its
   taxonomy clarified *before* the first cell runs: SPARSE = 3/3 seeds, MIXED =
   1–2/3 (a boundary cell, reported as such), DENSE = 0/3, with the per-seed
   count always reported.

## Alternatives considered

- **Keep the periodic task and claim induction anyway.** Rejected: the probe
  falsifies it, and the probe is exactly the measurement the claim needed. A
  claim that survives only by not measuring is not a claim.
- **Change the task now, in this increment.** Rejected as a scope decision, not
  a scientific one: a new task needs its own pre-registration, its own
  ambiguity analysis (the birthday problem returns, with a different shape) and
  its own budget, and folding it into a detector-fix increment would make both
  harder to read. It is scheduled for v1.1.
- **Drop Rung 1.** Rejected: the machinery (the detector, the dissociation
  probe, the causal interventions, the cascade) is the asset, and the negative
  result it produces is informative — it is the first *measured* statement this
  repository makes about what the task actually elicits.

## Consequences

- The paper's Rung 1 section reports a copy head and a negative result about
  the two-step circuit, with the probe as the reason.
- `exp4`'s path patching gets its first end-to-end run against a real head
  (the same checkpoint Rung 1 trained), and `exp5`'s SAE gets its first
  real-activation run from a checkpoint with a confirmed head.
- v1.0 closes with the cascade measured and the claims honest; the
  content-based induction question is explicitly a v1.1 item.

## Notes

The GPU run that established these facts is recorded in
`portfolio/RESULTS.md` (Honesty Ledger, 2026-10-19 and 2026-10-20) and in
`00_meta/03_progress-log.md`. The detector lives in
`src/experiments/induction_detection.py`; the probe is
`run_dissociation_probe`.
