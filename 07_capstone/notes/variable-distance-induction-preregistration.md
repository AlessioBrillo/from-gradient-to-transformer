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

## Addendum — 2026-10-22: the CPU de-risk, and what it says about the thresholds

The CPU gate above was run before the GPU run, and its result is recorded
here **before** the GPU run happens, so that nothing about it can be read as
a post-hoc adjustment.

**The gate passes.** (1) The content oracle solves 100% of the copy queries
and the fixed-offset oracle 20.5% (`tests/test_induction_tasks.py`).
(2) The planted detector tests pass: a planted content head is detected, a
planted fixed-offset head and a planted previous-token head are not
(`tests/test_planted_variable_task.py`). (3) The end-to-end run completes and
writes a manifest with the new fields.

**The de-risk run** (CPU, the *quick* geometry: seq_len 24, key 15, two
blocks of three, vocab 256, d_model 64, 1500 epochs, fresh batches, one
seed):

| Measurement | Value | Chance / baseline |
|---|---|---|
| Overall validation accuracy | 0.1065 | 0.0039 (1/256) |
| **Copy accuracy** (on the copy queries) | **0.5288** | 0.2051 (best fixed offset) |
| **Copy accuracy, non-modal distance group** | **0.4521** | ~0 for a fixed-offset head |
| Content mass (per head, best) | 0.146 | screen 0.30 |
| K-composition | 0.183 | confirmation 0.40 |
| Confirmed heads | 0 / 8 | |

**What it says.** The task *is* learnable, and the copy is not a fixed
offset: the model reaches 0.53 on the copy queries against a 0.21 ceiling
for the best fixed offset, and 0.45 on the queries whose distance is *not*
the most frequent one — the group where a positional head scores ~0. The
behaviour is content-based.

**What it also says, and this is the part that matters for the GPU run.**
The *detector* does not fire: the best head's content mass is 0.146, below
the 0.30 screen, and the K-composition is 0.183, below the 0.40
confirmation bar. The most likely reading is that at this scale the copy is
**distributed over the heads** rather than concentrated in one: eight heads
at ~0.15 each can carry the copy while no single head crosses a per-head
threshold. That is the same drift the periodic task showed (the period mass
fell 0.909 → 0.695 with budget while the content mass stayed at 0.031).

**The thresholds are not changed.** The criteria above are frozen, and
0.30 is the per-head convention this repository has used since 2026-08-01
(a convention, not a derived boundary — see [[portfolio/RESULTS]]). The
consequence is stated plainly: **the GPU run can end in PARTIAL or in
"NEGATIVE (unexplained)" even if the model copies by content**, because the
behavioural criteria and the detector's screen can disagree. If they do, the
verdict says so, the word "induction head" is not used, and the
distribution over heads is the first thing to measure. That is a result
about the detector's granularity, and it is reported as one — not repaired
by lowering a bar that was written down before the data existed.

**A second probe, the same day, on the standard geometry** (CPU, seq_len 64,
key 36, four blocks of five, vocab 2048, d_model 64, 400 epochs, 2048
sequences per epoch, fresh batches, one seed): the model is still at the
uniform prediction at the end of the budget — train loss 7.6246 against
ln(2048) = 7.62, copy accuracy 0.0004 against a chance of 0.0005, content
mass 0.022, no confirmed head. The standard geometry is *not* yet learning at
400 CPU epochs, while the quick geometry (vocab 256, four copy queries per
sequence instead of twenty) had reached a copy accuracy of 0.53 by epoch
1500.

Two readings, and the record does not pick one yet: the standard task may
simply need its full budget (the pre-registered run is ~7.5× the optimizer
steps and 4× the data per epoch, on a GPU), or the larger vocabulary may
make the early phase much slower to leave. What this does *not* change is
the protocol: the GPU run is the pre-registered one, at its budget, with the
criteria above, and a negative there is a negative at that budget.

## Addendum — 2026-10-22 (b): four corrections, decided before the GPU run

This addendum is written **before** the GPU run and after the audit of the
2026-10-22 de-risk itself. It changes the *protocol* in four ways, and it
does not change a single one of the seven criteria.

### 1. The record above was wrong twice, and here is the correction

**(a) The gate's item (3) was not backed.** The addendum above says "the
end-to-end run completes and writes a manifest with the new fields". It did
not write one: both de-risk runs were launched without `--save-manifest`
(`'save_manifest': False, 'manifest_path': None` in both logs), no
`results/*content*.json` exists, and the two logs are gitignored — so the
numbers 0.5288 / 0.4521 / 0.146 / 0.183 were not traceable from a clone.
The gate is re-run with a **tracked** manifest
(`results/induction_content_derisk.json`, `make reproduce-induction-content-derisk`)
and the numbers below are quoted from it.

**(b) The probe's verdict was omitted.** The same de-risk run printed
`Dissociation probe — content mass 0.122 vs positional mass 0.253 ->
POSITIONAL copy`. The addendum above reports the *behaviour* (copy accuracy
0.53 against a 0.21 ceiling) and does not report this. Both are true, and
they are not the same kind of statement: the behaviour is the model's
answer, the probe is a **per-head attention maximum** compared with another
per-head maximum. A circuit that spreads the copy over several heads puts
~0.12 on the content key in each head while a head that does nothing for
the answer can still hold 0.25 on some offset. The addendum's sentence
"the behaviour is content-based" stands; the sentence it should have
qualified — "and the probe still says POSITIONAL" — was missing, and the
qualification is the whole reason for the mechanism report below.

### 2. The vocabulary: 2048 → 256

The periodic task's 2048 answered a constraint the content task does not
have. The periodic prefix is sampled **with replacement**, so at 2048 the
probability of a duplicate token inside the prefix is what keeps the task
well posed (that is the `prefix_duplicate_probability` machinery). The
content task's key is sampled **without replacement**: 44 distinct tokens
are enough (36 key + 8 filler) and the constraint does not exist.

The evidence that 2048 was a liability, not a gift: the standard-geometry
probe (400 CPU epochs, 2048 sequences per epoch) was still at the *uniform*
prediction — train loss 7.6246 against ln(2048) = 7.6246, copy accuracy
0.0004 — while the *quick* geometry at **vocab 256** had reached a copy
accuracy of 0.53. A vocabulary that puts the model at chance for 400 epochs
is a budget question with a 30× multiplier attached (the pre-registered run
is 384k steps against the probe's 12.8k).

**The amended standard config** (`--content-standard`, pinned in
`src/experiments/exp1_induction_heads.py` and tested in
`tests/test_induction_heads.py`): `vocab_size=256`, `seq_len=64`,
`key_len=36`, `copy_blocks=4`, `copy_block_len=5`, `d_model=64`, 2 layers,
4 heads, attention only, fresh batches every epoch, 3000 epochs, batch 64,
8192 sequences per epoch, 3 seeds. Everything except the vocabulary is
unchanged. The trade-off is stated plainly: the content run is **not**
like-for-like with the periodic run on the vocabulary axis, and it is not
comparable on the task axis either — which is why the comparison that
matters is *within* this task (content against the best fixed offset, on
the same data).

### 3. The emergence run's stop rule: `mechanism` → `any`

`--stop-rule mechanism` stops when a head is confirmed **above the first
layer** (the two-step circuit). On the periodic task the whole circuit was
in layer 0, and the de-risk confirmed no head at all — so the two-step rule
had a good chance of never firing, silently turning the emergence run into a
second full-budget run and doubling the GPU bill. The question the
emergence run asks is "when does a copy head appear?", and `--stop-rule any`
answers it at the first confirmation (twice in a row, as before). The full
run records `confirmed_epoch` anyway, so nothing is lost.

### 4. The secondary mechanism report (and what it may and may not say)

The criteria above are **unchanged** and still decide the verdict. What is
added is a *report*, always produced, that describes the circuit:

| Measurement | What it is | How it is computed |
|---|---|---|
| `content_mass_total` | the attention mass the whole circuit puts on the content key | the sum over every head of every layer |
| `content_mass_top_share` | the top head's share of it | 1.0 = one head does all of it |
| `content_mass_heads_for_80pct` | how wide the circuit is | the heads that cover 80% of the total |
| `offset_mass_total` | the same sum for the best fixed offset | the ceiling of the positional explanation, on the same queries |
| `group_ablation_drop` | the causal version: the drop in copy accuracy when the **whole candidate group** is ablated | an intervention, not a correlation |
| `max_single_ablation_drop` | the drop of the best single member of the group | next to the group drop, it separates "one head" from "a group" |
| `dla_content_minus_offset` | the first-order logit attribution of every head to the content-vs-position contrast | the head's OV output projected on the difference of the two unembedding directions |
| `mechanism_kind` | the classification, as a code (0 none, 1 single head, 2 distributed, 3 undetermined) | `src/experiments/copy_circuit.classify_mechanism` |

**The candidate group is fixed by a rule that reads the data and the
attention masses, never the outcome**: a head is a candidate when its
content mass is at least **3× the chance level**, and the chance level is
what a uniform head would put on that key (computed from the copy queries'
positions, not from the model).

**The classification thresholds** (also fixed in advance):

- *distributed* — the group ablation costs ≥ 0.20 of the copy accuracy and
  no single head costs more than 0.10;
- *single head* — one head alone costs ≥ 0.20;
- *none* — the group costs ≤ 0.05 and the attribution does not favour the
  content;
### The CPU gate's numbers, traced to a manifest

The gate was re-run with `--save-manifest`, and both manifests are tracked:
`results/induction_content_derisk.json` (quick geometry) and
`results/induction_content_derisk_standard.json` (standard geometry, once the
second run finishes). Every number below is quoted from the quick-run manifest;
the standard-geometry numbers will be added here when its run finishes —
before the GPU session starts.

**Quick geometry** (vocab 256, seq_len 24, key 15, two blocks of three,
d_model 64, 2 layers, 4 heads, fresh batches, 1500 epochs, one seed,
`results/induction_content_derisk.json`):

| Measurement | Value | Chance / baseline |
|---|---|---|
| Copy accuracy (copy queries) | 0.9988 | 0.193 (best fixed offset) |
| Copy accuracy, non-modal distance group | 0.9988 | ~0 for a fixed-offset head |
| Content mass (per head, best) | 0.154 | screen 0.30 |
| Offset mass (best fixed offset, per head, best) | 0.330 | |
| Content mass, total over heads | 0.695 | |
| Top head's share of the content mass | 0.221 | 1.0 = one head does all of it |
| Heads covering 80% of the content mass | 5 | 1 = a single-head circuit |
| First-order attribution to content minus position | 5.87 | sign favours content |
| Group ablation drop (candidate group) | 0.0 | ≥ 0.20 = the group carries the copy |
| Max single-head ablation drop | 0.0 | ≥ 0.20 = one head carries the copy |
| Exploratory group size (top 80% mass) | 5 | not used for the verdict |
| Exploratory group ablation drop | 0.0 | not used for the verdict |
| Confirmed heads | 0 / 8 | |
| Mechanism kind | undetermined (code 3) | — |

**What it says.** The task is learnable — 0.999 copy accuracy on the copy
queries against a 0.19 fixed-offset ceiling — and the behaviour is clearly
content-based. But the detector does not fire: the best head's content mass is
0.154, below the 0.30 screen, and no head is confirmed. The aggregate content
mass over all heads is 0.695, spread over five heads to cover 80% of it —
exactly the distributed copy the per-head screen cannot see. The group ablation
of the candidate group costs 0.0 because **the candidate group was empty**:
`n_candidate_heads` is 0, so the ablation was a no-op. The sentence
"the candidates are not the carriers" in earlier drafts of this addendum is
**retracted** — it mistook an empty group for a measured null. There were no
candidates to carry anything. The first-order attribution (5.87, favouring
content) and the DLA positive share confirm the behaviour is content-based;
the mechanism class is "undetermined — no candidate passed the 3x chance
screen", not "none". The thresholds are not changed.

**Standard geometry** (vocab 256, seq_len 64, key 36, four blocks of five,
d_model 64, 2 layers, 4 heads, fresh batches, 600 epochs, one seed,
`results/induction_content_derisk_standard.json`):
tracked manifest; numbers quoted here once the run finishes, before the GPU
session starts. (The prior 600-epoch attempt was killed at epoch 30 by a host
reboot and is being re-run.)

- *undetermined* — anything else (for instance a group that costs a lot
  **and** a head that costs a lot: a redundant circuit).

**What the report may say.** It may say that the copy is content-based and
carried by a group of heads rather than by one. It may not change the
verdict: a run whose seven criteria are not met is **not** a positive
induction result, whatever the report says. The sentence the repository may
publish in that case is the one the decision rule already allows —
"NEGATIVE (unexplained): the model solves the task by a mechanism the
detector does not identify" — with the report attached as the description
of that mechanism. The word "induction head" is not used.

## Addendum — 2026-10-25: instrument audit before the GPU run

This addendum records corrections to the instrument, decided **before** the
GPU run, so that nothing here can be read as a post-hoc adjustment. The seven
frozen criteria and their thresholds are unchanged.

1. **Chance level fixed.** `chance_content_mass` used `1 / (key + 1)` where it
   should use `1 / (q + 1)`: the uniform mass at query `q` is spread over the
   `q + 1` positions the causal mask allows, not over `key + 1`. The old
   formula overstated the bar, so on the quick geometry the candidate screen
   selected zero heads (`n_candidate_heads = 0`), making the group ablation a
   no-op. Fixed in `src/experiments/copy_circuit.py`; the old manifest
   (`results/induction_content_derisk.json`, SHA 1fc85d7) is kept as evidence
   of the bug, and the corrected run writes
   `results/induction_content_derisk_fixed.json`.

2. **Attribution shares normalized by absolute total.** `dla_positive_share`
   and `dla_top_head_share` divided by the signed total, so they could exceed
   1 (observed 1.0698 on the de-risk manifest). They now divide by
   `sum(|v|)` and stay in `[0, 1]`; the sign remains in `dla_total`.

3. **Empty candidate group is not "no circuit."** `classify_mechanism` now
   returns `undetermined — no candidate passed the 3x chance screen` when
   `n_candidate_heads == 0`, instead of falling through to "none" or letting
   a vacuous 0.0 group ablation speak. The sentence "the candidates are not
   the carriers" from the 2026-10-22 addendum is retracted: there were no
   candidates.

4. **Exploratory mass-covering group.** `mass_covering_heads` measures the
   smallest set of heads covering 80% of the content mass. It is explicitly
   exploratory, not used for the verdict, and reported alongside the
   pre-registered candidate group in `exp1_induction_heads.py` as
   `exploratory_group_size` / `exploratory_group_ablation_drop`.

5. **No fabricated zeros for unmeasured path patching.** `exp4_circuit_patching`
   omits `mean_path_patch_effect` (and `mean_ablation_effect`,
   `group_path_patch_effect`) when no head was confirmed, and adds
   `path_patch_measured` / `group_path_patch_measured` flags. The verdict
   reports `NOT MEASURED`, never a measured 0.0.

6. **Redundant emergence run removed.** The emergence run's only unique
   output was `confirmed_epoch`, which the full run already records. The GPU
   protocol is now one session, 3 seeds, full-budget run only; see
   `docs/agents/gpu-runs.md`. This is a budget amendment, not a threshold
   change.

7. **Verdict wording follows the decision table.** `content_verdict.py`
   prints "NEGATIVE (unexplained): the model solves the task by a mechanism
   the detector does not identify" for the high-copy / low-content-mass case,
   and the mechanism report prints the aggregate numbers next to the verdict.

The standard-geometry CPU de-risk (`results/induction_content_derisk_standard.json`)
must be tracked and its numbers added here before the GPU session starts.

### 5. The counterfactual of the causal cascade: the minimal pair

The 2026-10-20 cascade built the corrupted half of the intervention from a
*different* sequence, so the contrast it measured was "the answer of this
sequence against the answer of another sequence" — which every mechanism
has to lose. That is why its activation-patching recovery is 0.0834, a
number that is hard to read as "this circuit carries the answer".

The content run uses a **minimal pair**: the same sequence with exactly one
token changed — the token at the source of the copy (`prev(q) + 1`). The
replacement token is drawn from the ids that do **not** occur in the
sequence, so the corrupted sequence keeps every token unique and the read
position stays a copy query: only the answer changes. The intervention is
then "the head's direct contribution carries the *content* of the source",
which is the claim the criterion is about.

The criterion (7) is unchanged. The design is expected to make the effect
**larger**, so the criterion is at least as strict as it was.

## Links

- [[portfolio/RESULTS]] — the authority on what is true; the Rung 1 section
  is where the verdict will be recorded.
- [[07_capstone/notes/positive-control-protocol]] — the same discipline
  (a negative that cannot be produced by a positive control is a negative
  about the harness, not about the phenomenon): here, the content oracle and
  the fixed-offset oracle are the two controls.
- [[docs/adr/0032-induction-detector-and-the-positional-shortcut]] — the
  audit that found the detector bug and the shortcut.
- [[docs/adr/0033-content-based-induction-task]] — the design decision.
- [[07_capstone/research-plan]] — the ladder this rung belongs to.
- [[04_nlp_and_transformers/notes/induction-heads]] — the mechanism's
  background.
