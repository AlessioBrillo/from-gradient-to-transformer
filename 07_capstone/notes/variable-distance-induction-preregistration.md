---
tags: [phase/7, capstone, research/experiment, state/review]
created: 2026-10-20
---

# Variable-Distance Induction Task — Pre-Registration (issue #200)

## The question

**Does a content-based induction head form when the fixed-offset shortcut is
removed from the task?**

Rung 1's headline claim is that a head implements `[A][B]...[A] -> [B]`: at a
query position `q` whose token `x[q]` has already appeared, the model finds
that earlier occurrence and copies the token that followed it. On 2026-10-20
that claim was **not** earned, for a reason that has nothing to do with the
model: the task was periodic, so the previous occurrence of `x[q]` was
*always* at `q - L`, and a head that attends to `q - L + 1` by pure position
arithmetic is the *same function* as a head that attends to "the token after
the previous occurrence". The dissociation probe of 2026-10-19 said which one
the model had actually learned: the offset.

No amount of re-analysis of that checkpoint can answer the question. It takes
a different task. This note freezes that task, the measurements, the
thresholds and the decision rule **before** any run.

## What is frozen here

Everything below is fixed before the GPU run. Thresholds, seeds and the
budget are not adjusted afterwards — a run that misses a threshold is
reported as a miss, not re-tuned. The only thing that may change after a
run is the *narrative*, and only towards "it did not work".

### The task (`src/experiments/induction_tasks.py`, `GENERATOR_VERSION = induction-tasks-v1`)

| Parameter | Value | Why |
|---|---|---|
| `vocab_size` | 2048 | as the standard config; the key tokens must be distinct |
| `seq_len` | 64 | as the standard config, so the comparison with the periodic run is like-for-like |
| `key_len` | 36 | the source segment: 36 distinct tokens at positions 0..35 |
| `copy_blocks` | 4 | four verbatim copies of the key |
| `copy_block_len` | 5 | 20 copied tokens, of which 16 are copy queries |
| filler | 8 distinct tokens, none in the key | unpredictable, so only the copy queries are learnable |
| source windows | 4 disjoint windows of 5 inside the key, positions resampled per sequence | **this is the variable distance** |
| block positions | resampled per sequence (the gaps between the blocks are a random composition) | the distance varies per block *and* per sequence |

Invariants, all pinned by `tests/test_induction_tasks.py`:

1. every token appears at most twice — a copied token's previous occurrence
   is unique, so the task is well posed;
2. the copy queries are derived **from the tokens alone**
   (`tokens[q+1] == tokens[prev(q)+1]`), so the detector never has to trust
   the generator;
3. the distance `q - prev(q)` takes at least 8 distinct values per batch;
4. the best *fixed-offset* predictor explains **< 30%** of the copy queries
   (measured: 17.6% at the standard config). This is the ceiling of the
   positional explanation, and it is a property of the data, measured
   before the run.

### The measurements

| Metric | Meaning |
|---|---|
| `copy_accuracy` | accuracy on the copy queries only — the learnable positions |
| `copy_accuracy_nonmodal` | accuracy on the copy queries whose distance is *not* the most frequent one — the sharpest behavioural discriminator |
| `fixed_offset_baseline` | the best single fixed offset's accuracy on the copy queries (the positional ceiling) |
| `content_mass` | attention mass on `prev(q)+1`, the content hypothesis |
| `peak_offset_mass` | the largest attention mass any head puts on any fixed offset `q-d` |
| `peak_prev_token_mass` | the previous-token control |
| `k_composition_score` | Nanda & Jacobsen's Step 2, unchanged |
| `mean_ablation_drop` | copy-accuracy drop when the confirmed head is ablated |
| `mean_path_patch_effect` | the direct effect of the confirmed head on the logits |

### The thresholds (frozen)

A head is a **candidate** when its content mass is above `0.30` — the
per-head threshold this repository has used since 2026-08-01, applied to the
correct offset. A candidate is **confirmed** when the layer it lives in
composes with an earlier layer at a K-composition score of at least `0.40`
(the same two-stage rule as the periodic task; a first-layer head is
confirmed on the mass alone, and that limitation is reported).

The **positive** verdict requires **all** of:

| # | Criterion | Threshold |
|---|---|---|
| 1 | `content_mass` of the confirmed head | ≥ 0.30 |
| 2 | `content_mass` − `peak_offset_mass` | ≥ 0.10 |
| 3 | `copy_accuracy` | ≥ 0.60 |
| 4 | `copy_accuracy_nonmodal` | ≥ 0.50 |
| 5 | `copy_accuracy` − `fixed_offset_baseline` | ≥ 0.20 |
| 6 | `mean_ablation_drop` (copy accuracy) | ≥ 0.10 |
| 7 | `mean_path_patch_effect` | ≥ 0.20 |

Criterion 4 is the one that separates the two mechanisms behaviourally: a
fixed-offset head is right on the queries that share its offset and wrong
everywhere else, so its non-modal accuracy is ~0. A content head is right
on all of them.

### The budget and the seeds

- 3 seeds (0, 1, 2), the standard config of Rung 1: 3000 epochs, 384k
  optimizer steps per seed, `d_model=64`, 2 layers, 4 heads, attention only,
  fresh batches every epoch, detection every 50 epochs.
- Two runs: an **emergence** run with `--stop-on-confirmed --stop-rule
  mechanism` (when does the circuit appear?) and a **full-budget** run
  without the early stop (the headline; the model Rungs 4 and 5 analyse).
- The budget is the same as the periodic run's, so the two are comparable.
  A negative at this budget is a negative *at this budget*, and it is
  reported as such — the budget is not extended after the fact.

### The decision rule

| Outcome | Reading | The sentence the repository may publish |
|---|---|---|
| all 7 criteria met on a majority of seeds (≥ 2/3) | **POSITIVE** | "A content-based induction head forms on a variable-distance task, and the causal interventions land." |
| a head is confirmed but criterion 4 or 6 or 7 fails | **PARTIAL** | "A copy head forms, but the causal evidence does not support the induction claim." |
| copy accuracy is high but the content mass is low | **NEGATIVE (unexplained)** | "The model solves the task by a mechanism the detector does not identify." The word "induction head" is not used. |
| no head is confirmed | **NEGATIVE** | "No induction head forms on the variable-distance task at this budget." |

The verdict is reported **per seed** and then aggregated. A seed is never
dropped and a run is never repeated "to get a better label": the negative
outcomes of this repository's own audit history were manufactured by
exactly that move.

### The CPU gate (before any GPU hour)

The GPU run only happens after these pass on CPU:

1. the content oracle solves 100% of the copy queries, the fixed-offset
   oracle solves < 30%;
2. the planted detector tests pass — a planted content head **is** detected,
   a planted fixed-offset head is **not**
   (`tests/test_planted_variable_task.py`);
3. a `--quick` end-to-end run completes and writes a manifest with the new
   fields.

If the gate fails, the bug is in the task or the detector, and no GPU hour is
spent looking for it.

## What this run cannot claim

- It cannot claim that *all* induction heads are content-based — it claims
  what it measured, on one architecture, at one budget, on one task.
- It cannot claim anything about the periodic task's head: that one stays a
  *prefix-copying* head, which is what the 2026-10-19 probe found.
- A negative here does not retract the periodic result; it closes the
  question the periodic task could not answer.

## Links

- [[portfolio/RESULTS]] — the authority on what is true; the Rung 1 section
  is where the verdict will be recorded.
- [[07_capstone/notes/positive-control-protocol]] — the same discipline
  (a negative that cannot be produced by a positive control is a negative
  about the harness, not about the phenomenon): here, the content oracle and
  the fixed-offset oracle are the two controls.
- [[docs/adr/0032-induction-detector-and-the-positional-shortcut]] — the
  audit that found the detector bug and the shortcut.
- [[07_capstone/research-plan]] — the ladder this rung belongs to.
- [[04_nlp_and_transformers/notes/induction-heads]] — the mechanism's
  background.
