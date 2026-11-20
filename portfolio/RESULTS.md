---
tags: [portfolio, results]
---

# Results — Headline Findings

> **Thesis**: I build a decoder-only transformer from scratch, then reverse-engineer the algorithms it learns — grokking modular addition with Fourier decomposition, induction heads, circuit verification via activation and path patching, and sparse autoencoder feature extraction.

All experiments are implemented in `src/experiments/`. Each has a `--quick` mode for fast
smoke tests (`make reproduce-quick`) and a full-scale mode (`make reproduce`).

---

## Summary

The current status of every rung, and what to trust in what order. The audit trail
that explains how each number came to be this one (thirteen audits, each with what
was wrong and what changed) is the [Honesty Ledger](#honesty-ledger) below; the
per-rung detail follows the ledger.

| Rung | Status | Key Result |
|------|--------|------------|
| 1 — Prefix-Copying Heads (fallback flagship) | ✅ **A head forms at standard scale — and it is positional** (2026-10-20) | Corrected detector, GPU, 3 seeds, 3000 epochs: **3 heads/seed**, copy-offset mass **0.81** (previous-token control 0.05), all in the first layer; ablation effect **0.59**, path-patch effect **0.71** (re-measured 2026-11-17 after the seeding fix); the dissociation probe says the copy follows the **fixed offset** (period 0.81 vs content 0.03), and the K-composition is 0.08 — a single-head prefix-copying circuit, not the two-step induction circuit (ADR-0032) |
| 2 — Grokking (primary flagship) | ✅ **REPRODUCED 2026-10-14** (the 2026-08-11 NO-GROK was a metric artifact) | Nanda protocol, P=113, GPU, 3 seeds: val accuracy 0.9999 ± 0.0002, **k_energy_90 = 5.7 ± 1.2 of 56 — sparse on 3/3 seeds**; the historical repo protocol re-reads the same way |
| 3 — Superposition | ✅ Phase transition confirmed | Root cause found (no real bottleneck); rewritten, reproduces cleanly: 10/20 → 20/20 features represented |
| 4 — Circuit Patching | ✅ **Cascade ran end to end on Rung 1's checkpoint** (2026-10-20, re-measured 2026-11-17) | Head ablation **0.5895 ± 0.1405**, path patching **0.7052 ± 0.0411** — the first end-to-end path-patching result against a real head; activation recovery 0.0834 |
| 5 — SAE Dashboard | ✅ Synthetic reproduced; ✅ **the real-activation gap closed** (2026-10-20, re-measured 2026-11-17) | On the confirmed-head checkpoint the SAE is now *sparse*: L0 19.0/512 (3.7%), FVE 99.998%, MSE 0.0005 — against 53% L0 for the old undertrained model. What remains is a dictionary 8× too large (66% dead features) |
| 6 — ACDC | ❌ Deleted | Was fabricated data; removed 2026-08-01 rather than fixed |
| 1b — Content-based induction (issue #200) | [x] **Complete, verdict NEGATIVE (run 2026-11-09, re-run 2026-11-17)** | The task that removes the positional shortcut (repeats at varying distances; the best fixed offset explains 15.5–16.5% of the copy queries) is frozen in [ADR-0033](../docs/adr/0033-content-based-induction-task.md) and the [pre-registration](../07_capstone/notes/variable-distance-induction-preregistration.md). The 2026-11-09 run (PARTIAL, kept as `results/induction_content_pre_seedfix.json`) was repeated on GPU after the seeding fix (tag `v2.0.0-rc1`, `results/induction_content.json`; cascade on CPU, `results/exp4_content.json`). Both verdicts are now **NEGATIVE on all three seeds**: no head passes the frozen per-head rule. The behaviour is content-based on 3/3 seeds; the circuit is one head on one seed and a distributed group on two. Verdict artifact: `results/content_verdict.json` (derived, `make content-verdict`). |
| 7 — GPT-2 small (pre-registered, ADR-0034) | ⚠️ **Instruments validated; causal stages not reproduced** (2026-11-17) | The hand-written implementation equals the Hugging Face reference; the shared detector ranks the two induction heads of the literature first and second of 144 heads; the model solves the indirect-object task. Zero-ablating those two heads, or the three name movers, changed the behaviour no more than random heads do |

The manifests behind that table: Rung 1
<!-- manifest: results/induction_standard.json -->, Rung 2
<!-- manifest: results/grokking_nanda_p113.json -->, Rung 3
<!-- manifest: results/exp3_superposition.json -->, Rung 4
<!-- manifest: results/exp4_standard.json -->, Rung 5
<!-- manifest: results/exp5_real_activations.json -->, Rung 1b
<!-- manifest: results/induction_content.json -->
<!-- manifest: results/exp4_content.json -->, Rung 7
<!-- manifest: results/gpt2_small_stage2.json -->.

**What to trust right now, in order**: (1) Rung 2's sparse-circuit reproduction —
GPU, 3 seeds, both protocols, post-audit energy metric, manifests pinned with
provenance; the checkpoints are on disk
(`results/remote/grokking-p113/output2/repo/checkpoints/nanda/`) and the four
`exp2_*` figures were regenerated from them 2026-10-17. (2) Rung 1's
prefix-copying head — GPU, 3 seeds, standard scale, 3000 epochs, with the
causal interventions (ablation 0.59, path patching 0.71, re-measured after the seeding fix) and the dissociation
probe that says the copy is positional rather than content-based; the
detector behind it is planted-tested, and the previous "0 / 8" was a detector
artifact. (3) Rung 3's phase
transition — reproduced cleanly, root cause understood, multi-seed manifest
backs it. (4) Rung 5's real-activation SAE on the confirmed-head checkpoint:
L0 3.7% with FVE 99.998% — the old "dense reconstruction" was a statement
about the old undertrained model, and what remains is a dictionary 8× too
large. (5) Rung 1's
fixed-vs-fresh comparison — a real, large, matched effect, though at a scale still
well below standard. (6) Rung 4's quick multi-seed re-run — activation patching
runs cleanly; the standard-scale cascade above is the current number. The
protocol-ablation phase diagram (issue #168) has not run and is not scheduled.

---

## Honesty Ledger

The audit trail (thirteen audits, newest first) is in [LEDGER](LEDGER.md). It stays a separate file so this page starts with results, not with corrections. Every retraction that changes a number quoted here is applied here too.


---

## Rung 1 — Prefix-Copying Heads (Fallback Flagship — the detector was wrong; a head does form, and it is positional)

<!-- manifest: results/exp1_induction_heads.json -->

**Question**: Do induction heads emerge in a 2-layer attention-only transformer trained on repeated tokens? Can we detect, verify, and ablate them causally?

**Status**: [x] **A head forms at standard scale — and it is a *prefix-copying* head, not an induction head.** The detector that reported "0 / N heads" was measuring the previous-token offset (see the Honesty Ledger's 2026-10-19 entry); with the corrected detector the standard-scale run confirms **3 heads per seed** with a copy-offset mass of **0.81** at the final checkpoint (0.95 at epoch 100), and the causal interventions land: ablating the confirmed head costs **59%** of the logit difference and path patching attributes **71%** of its direct effect on the logits to that head.
But the **dissociation probe** shows the copy follows the *fixed offset* (`q-(L-1)`), not the previous occurrence of the same token (period mass 0.81 vs content mass 0.03, 3/3 seeds), and the K-composition between layers stays at **0.08** — so there is **no two-step circuit**. The task is perfectly periodic, which makes "copy by content" and "copy by offset" the same function in-distribution; the model found the cheaper one. See [ADR-0032](../docs/adr/0032-induction-detector-and-the-positional-shortcut.md).

### Standard scale, GPU, 3 seeds (the measurement that replaces the retracted counts)

<!-- manifest: results/induction_standard.json -->
<!-- manifest: results/induction_standard_emergence.json -->
<!-- manifest: results/exp4_standard.json -->

| Metric | Emergence run (early stop) | Full budget (3000 epochs) | Rung 4 on the same checkpoint |
|--------|--------------------------|----------------------------|--------------------------------|
| Manifest | `induction_standard_emergence.json` | `induction_standard.json` | `exp4_standard.json` |
| Device / wall clock | CUDA, 393 s | CUDA, 3 h 07 min | CPU re-analysis of the GPU checkpoint (epoch 3000) |
| Budget | stopped at the confirmation (epoch 100, two consecutive checks) | 3000 epochs = 384k optimizer steps/seed | — |
| **Confirmed heads (per seed)** | **3, 3, 4** | **3, 3, 3** | 3, 3, 3 |
| … in the first layer | 3, 3, 4 | 3, 3, 3 | 3, 3, 3 |
| … above the first layer (mechanism confirmed) | **0** | **0** | — |
| Peak induction mass (copy offset `q-(L-1)`) | **0.949 ± 0.019** | **0.808 ± 0.070** | — |
| Previous-token mass (control, `q-1`) | 0.027 ± 0.008 | 0.047 ± 0.025 | — |
| K-composition score (L→L) | 0.066 ± 0.016 | 0.083 ± 0.034 | — |
| L0 duplicate-token mass | 0.018 ± 0.006 | 0.198 ± 0.113 | — |
| Final val accuracy | 0.5082 ± 0.0000 | 0.5082 ± 0.0001 | 0.5083 ± 0.0005 |
| **Head ablation — accuracy drop** (exp1, on its own model) | 0.018 ± 0.012 | 0.081 ± 0.011 | — |
| **Head ablation — logit-diff drop** (exp4, same checkpoint) | — | — | **0.5895 ± 0.1405** |
| **Path-patching effect** (direct effect on logits) | not run | not run | **0.7052 ± 0.0411** |
| Activation-patching recovery (layer/position) | not run | not run | 0.0834 ± 0.0002 |
| Dissociation probe — content mass | 0.030 ± 0.001 | 0.031 ± 0.000 | 0.0310 ± 0.0002 |
| Dissociation probe — period mass | 0.948 ± 0.019 | 0.809 ± 0.070 | 0.8096 ± 0.0694 |
| **Copy is content-based?** | **no (3/3 seeds)** | **no (3/3 seeds)** | **no (3/3 seeds)** |

**Re-measured after the seeding fix (2026-11-17).** Everything in this table was measured twice: the
first time on 2026-10-20, with the model constructed before it was seeded, and again on 2026-11-17
from the tag `v2.0.0-rc1` with the model seeded first (GPU for the training runs, CPU for the Rung 4
cascade). The first set is kept, unedited, as `results/induction_standard_pre_seedfix.json`,
`results/induction_standard_emergence_pre_seedfix.json` and `results/exp4_standard_pre_seedfix.json`.
**The qualitative result did not move**: heads form early, all in the first layer, with no two-step
circuit, and the dissociation probe puts the copy on the fixed offset on every seed. The numbers
moved within the seed spread, and two moved enough to name: the head count is now 3 on every seed
(it was 3, 2, 3), and Rung 4's head-ablation effect rose from 0.4445 ± 0.0425 to 0.5895 ± 0.1405 while its path-patching
effect fell from 0.8215 ± 0.1255 to 0.7052 ± 0.0411. Those two intervention numbers
are the ones a reader should treat as having a wide, seed-dependent error bar: they changed by more
than their own previous standard deviations when only the initial weights changed.

Reading the table:

- **The retracted "0 / 8" really was a detector artifact.** At standard scale the
  model forms heads within 50 epochs (the emergence run stops at epoch 100 after
  two consecutive confirmations), with a copy-offset mass of 0.95 against the
  0.3 threshold, while the previous-token control stays at 0.03–0.05.
- **They are not the two-step circuit.** Every confirmed head is in the *first*
  layer, where the detector can only confirm it on the mass (there is no earlier
  layer to compose with). The K-composition between layers is 0.07–0.08, far
  below the 0.4 confirmation bar, and the L0 duplicate-token mass — the head
  that is supposed to find the previous occurrence — stays at 0.02 (early) and
  0.20 (full budget) against a copy-offset mass of 0.95 (early).
- **The causal interventions land, and they are the first end-to-end path-patching
  result in this repository.** On the same checkpoint (epoch 3000), ablating the
  confirmed head costs **0.59** of the answer-minus-counterfactual logit
  difference, and path patching — which isolates the head's *direct* contribution
  to the logits — attributes **0.71** of it to that head. The head is the circuit
  for this task. (The smaller accuracy drops in the first two columns are exp1's
  own ablation, measured as validation *accuracy*: the copy only buys accuracy
  on the second half of the sequence, so a 0.02–0.08 accuracy drop and a 0.59
  logit-difference drop are the same intervention measured on two scales.)
- **But it is a positional copy.** The dissociation probe (a batch whose second
  half is a *permuted* copy of the prefix, so the content target and the fixed
  offset point at different keys) puts the model's mass on the **position**
  target (0.81) and not on the content target (0.03) on 3/3 seeds, in both runs
  and in the Rung 4 re-analysis. On a perfectly periodic sequence the previous
  occurrence of the current token is *always* at `q-L`, so "copy from the
  previous occurrence of the same token" and "copy from the fixed offset" are
  the same function on this task — and the model took the shortcut.
- **The accuracy plateau (0.508) is the same plateau the capstone measured**
  (induction accuracy 0.5034 in the joint run): the model copies the periodic
  continuation, which is exactly right on the second half of the sequence and
  unpredictable on the first.

**What this does not claim**: that the model implements Olsson-style content-based
induction. It does not, on this task. The content-based claim is not testable
here — it needs a task with repeats at *varying* distances.

### The content-based task (issue #200) — run complete, both verdicts NEGATIVE

The task that *does* contain the question was specified and frozen before its
GPU run; the run and its verdicts follow the specification below. The short
version of the specification:

| | |
|---|---|
| **The task** | A key of 36 distinct tokens; four verbatim copy blocks of five, with the source windows **and** the block positions resampled per sequence, so the distance between a token and its previous occurrence changes from block to block. Every token appears at most twice (the task is well posed), the filler is distinct and unpredictable, and the copy queries are derived **from the tokens alone** — the detector never has to trust the generator. |
| **Why it separates the mechanisms** | The best *single fixed offset* explains **17.6%** of the copy queries (measured on the data before the run). A content-matching head can reach 100%. That gap is the claim, and it is a property of the data, not an assumption. |
| **The verdict** | Seven pre-registered criteria (the **confirmed head's** content mass ≥ 0.30, that mass above the best fixed offset by ≥ 0.10, copy accuracy ≥ 0.60, non-modal-distance accuracy ≥ 0.50, copy accuracy above the fixed-offset baseline by ≥ 0.20, ablation drop ≥ 0.10, path-patching effect ≥ 0.20), computed **by code** — `src/experiments/content_verdict.py`, which joins the exp1 and exp4 manifests per seed (`make content-verdict`). The criteria and their thresholds are frozen; a criterion whose measurement is missing is reported `NOT MEASURED` — never a fabricated zero — and a run whose manifest does not carry it gets the status `INCOMPLETE` and **no verdict**. |
| **The mechanism report** | A *secondary* report, always produced, that describes the circuit rather than deciding the verdict: the aggregate content mass and its concentration, the **group ablation** (the drop in copy accuracy when the whole candidate group is removed) next to the single-head ablations, and the first-order **logit attribution** of every head to the content-vs-position contrast. The candidate group is fixed by a rule that reads the data and the attention masses and never the outcome. When it finds a distributed circuit it says so, with the exp4 group path-patch effect, and labels the finding **secondary**. |
| **The budget** | 3 seeds × 3000 epochs = 384k optimizer steps per seed, GPU. A negative at that budget is a negative: the budget is not extended after the fact, and no seed is dropped. |
| **The amendments** | Vocabulary 2048 → 256 (`--content-standard`), minimal-pair counterfactuals, audit fixes for chance level and attribution shares (2026-10-25), confirmed-head mass criteria, provenance checks, recovery manifests, and distributed secondary circuit reporting (2026-11-01). See the pre-registration addenda for details. |
| **Where it is** | [ADR-0033](../docs/adr/0033-content-based-induction-task.md), the [pre-registration](../07_capstone/notes/variable-distance-induction-preregistration.md) (with its four addenda), the notebook `notebooks/kaggle_induction_content.ipynb` (`make remote-run-induction-content`). |

<!-- manifest: results/induction_content_derisk_fixed.json -->
<!-- manifest: results/induction_content_derisk_standard.json -->
<!-- manifest: results/exp4_content.json -->

**Status: [x] run complete and re-run — both verdicts NEGATIVE.** The run was first
executed 2026-11-09 (3 seeds × 3000 epochs, pinned at ref `v1.1.0-rc2`, commit `88147ee`). It was
**executed again on 2026-11-17, after the seeding fix** (the model is now seeded before it is
constructed, 2026-11-16), on GPU, from the immutable tag
`v2.0.0-rc1` (commit `191cde3`, clean tree, 6 h 27 min): `results/induction_content.json`. The
causal cascade was re-run on CPU on those checkpoints (`results/exp4_content.json`). The 2026-11-09
manifests are kept, unedited, as `results/induction_content_pre_seedfix.json` and
`results/exp4_content_pre_seedfix.json`: they are the record of what the old code measured and
of the verdict that was published until now. No threshold, budget or decision rule changed.

<!-- manifest: results/induction_content.json -->
<!-- manifest: results/exp4_content.json -->

| Verdict | Instrument | Seed 0 | Seed 1 | Seed 2 | Run |
|---|---|---|---|---|---|
| **Pre-registered** | the training run alone; criterion 7 was not part of it | NEGATIVE | NEGATIVE | NEGATIVE | **NEGATIVE** |
| **Causal addendum** | the same run plus the cascade | NEGATIVE | NEGATIVE | NEGATIVE | **NEGATIVE** |

Before the seeding fix the pre-registered verdict was PARTIAL (seed 0 PARTIAL, seeds 1 and 2
NEGATIVE) and the addendum made seed 0 POSITIVE while the run stayed NEGATIVE by the majority
rule. With the model seeded before construction, **no seed confirms a head**: the frozen per-head
rule asks for a head whose own attention mass on the content key is at least 0.30 *and* whose
layer composes with an earlier one at K-composition at least 0.40, and the largest K-composition
on any seed is 0.1311.

Per-seed detail of the pre-registered verdict:

| Seed | Verdict | Confirmed heads | Copy acc. | Non-modal acc. | Beats fixed offset | Content mass (confirmed head) | Ablation drop | Path patching (addendum) |
|------|---------|-----------------|-----------|----------------|-------------------|------------------------------|---------------|------------------------|
| 0 | NEGATIVE | 0 | 0.9968 | 0.9962 | 0.8322 | NOT MEASURED | NOT MEASURED | NOT MEASURED |
| 1 | NEGATIVE | 0 | 0.9997 | 0.9996 | 0.8447 | NOT MEASURED | NOT MEASURED | NOT MEASURED |
| 2 | NEGATIVE | 0 | 0.9995 | 0.9995 | 0.8410 | NOT MEASURED | NOT MEASURED | NOT MEASURED |

**Decision:** per the pre-registration, the verdicts are reported as they come out. No seed was
dropped and the budget was not extended. The missing measurements (content mass and ablation of
a *confirmed* head) are reported as not measured, never as zeros.

### The secondary mechanism report — what the run actually shows

The mechanism report is *secondary* by construction (the seven criteria decide; the report
explains). It carries the strongest numbers the run produced:

| Measurement (from `results/induction_content.json`) | Seed 0 | Seed 1 | Seed 2 |
|---|---|---|---|
| Copy accuracy on the copy queries | 0.9968 | 0.9997 | 0.9995 |
| Copy accuracy on the **non-modal** distance group | 0.9962 | 0.9996 | 0.9995 |
| Best single fixed offset (the positional baseline) | 0.1646 | 0.1550 | 0.1584 |
| Aggregate content mass (vs chance) | 0.5236 (3.2×) | 0.2124 (1.3×) | 2.3590 (14.4×) |
| Peak content mass of any single head | 0.1137 | 0.0673 | 0.8629 |
| **Group ablation drop** (candidate group removed) | 0.9938 | 0.9469 | 0.9940 |
| **Largest single-head ablation drop** | 0.8903 | 0.9469 | 0.0275 |
| Exploratory group ablation (top-80% mass group) | 0.9943 | 0.9963 | 0.9940 |
| K-composition score (the per-head confirmation bar is 0.40) | 0.0407 | 0.0347 | 0.1311 |
| Logit attribution: positive share on the content-vs-position contrast | 0.9825 | 0.9970 | 0.9827 |

**What this says, stated as sharply as the evidence allows.** On **all three seeds** the model
copies by *content*: the copy queries are answered at 0.9968–0.9997
while the best single fixed offset explains only 15.5–16.5% of them, and the logit attribution
favours the content answer on 98.3–99.7% of the queries. What differs between seeds is the
**shape of the circuit**:

- seed 1: **one head carries the copy** (single-head ablation drop 0.9469), but its own content mass is 0.0673;
- seed 0: a group of 6 candidate heads; removing the group removes 0.9938 of the copy accuracy, the best single head 0.8903;
- seed 2: a group of 3 heads, one with content mass 0.8629 — the strongest content attention this task has produced — yet removing it alone costs only 0.0275, while the group removes 0.9940.

**What the seeding fix taught about this result.** Before the fix the same experiment reported
"one head carries the copy on 3/3 seeds" and a per-head confirmation on 1/3. After it, the
behaviour is the same (content-based, 3/3) and the *causal structure* is not: a single head on one
seed, a distributed group on the other two, and no confirmation on any. A description of "the"
circuit on this task was a description of one initialization. The verdict is therefore not a
statement that the model lacks an induction mechanism, nor that it has one: it is that **the
frozen per-head instrument does not confirm one on any seed, and the circuit is not stable across
seeds**. The word "induction head" is not used for this task.

The open question narrows to a measurable one: **what do the distributed groups compute?** The
candidate explanation (a two-stage circuit in which the first layer writes *where* the previous
occurrence is and the second layer reads *what* follows it) is not tested, and K-composition cannot
see it, because it assumes the first layer's argmax *is* the previous occurrence, which on this
task it need not be. That is the next experiment, not a conclusion.

### Quick scale (the historical scale, for continuity)

| Metric | Tiny multi-seed (3 seeds, confirmed 2026-08-02) |
|--------|-------|
| Layers / Heads | 2 / 4 |
| d_model | 24 |
| Epochs | 150 |
| Train samples | 256 (resampled every epoch, `--fresh-batches`) |
| Val accuracy | 0.0058 ± 0.0024 (n=3) |
| Peak previous-token mass (control, `q-1`) | 0.095 ± 0.004 (n=3) |
| Induction-detector heads (>0.3 threshold) | 0.67 ± 0.94 per seed (corrected detector, re-measured 2026-11-17; the 2026-08-02 count was **retracted**, see the 2026-10-19 entry) |

### Fixed-vs-fresh-batches, matched 3-seed comparison

(see
[induction-heads](../04_nlp_and_transformers/notes/induction-heads.md) for the full writeup).
Identical config except the batch regime; both arms run the same seeds
(0, 1, 2), so the difference is attributable to the regime alone. Regenerate with
`make reproduce-induction-batches` (each arm: `vocab_size=256, seq_len=16,
d_model=24, n_layers=2, n_heads=4, epochs=800, lr=1e-3, weight_decay=0.1,
batch_size=32, num_train=256`).

<!-- manifest: results/exp1_induction_fixed_batches.json -->
<!-- manifest: results/exp1_induction_fresh_batches.json -->

| | Fixed (reused every epoch) | Fresh (resampled every epoch) |
|---|---|---|
| Final val accuracy | **0.46% ± 0.03%** (n=3) | **53.52% ± 0.01%** (n=3) |
| Peak copy-offset mass (`q-(L-1)`) | 0.175 ± 0.016 | 0.985 ± 0.005 |
| Peak previous-token mass (control, `q-1`) | 0.115 ± 0.026 | 0.160 ± 0.053 |
| Induction-detector heads (>0.3 threshold, per seed) | 0 | 4 |
| K-composition score | 0.144 ± 0.009 | 0.149 ± 0.007 |

Both arms are far apart in accuracy — two orders of magnitude, in the same
direction as the original prose-only claim — and, measured with the corrected
detector (2026-11-17, after the seeding fix), they now also differ in mechanism:
the fixed-batches arm forms **no** copy head (copy-offset mass below the 0.3
threshold), while the fresh-batches arm forms four per seed at a copy-offset
mass near 1.

**These numbers replace the prose-only "0.05% vs 52.2%" that appeared in nine
documents with no manifest behind it anywhere in `results/`.** The direction and
the conclusion are unchanged; the values are not. The first manifest-backed values
(2026-10-12) were 0.45% against 53.53%; after the seeding fix both arms were
re-measured (2026-11-17), and the accuracy gap did not move (kept as
`results/exp1_induction_fixed_batches_pre_seedfix.json` and
`results/exp1_induction_fresh_batches_pre_seedfix.json`). See the Honesty Ledger's
2026-10-11 entry.

> **2026-10-19 — the head counts in this section are retracted.** The detector
> behind the "0 / 8" rows measured the previous-token offset (`q → q-1`) and
> called it the induction signature; the copy offset on this task is
> `q → q-L+1`. The rows above are kept (with the old metric relabelled) because
> the *accuracy* comparison they support is unaffected, but the head-count
> annotation is not a measurement. The corrected detector
> (`src/experiments/induction_detection.py`) reports the induction mass, the
> previous-token control, the duplicate mass and the K-composition score, and
> the standard-scale run that will produce the corrected numbers is issue
> #169.
>
> *The 2026-10-12 manifests recorded the previous-token mass under the old key
> `peak_diag1_mass`; the re-measured ones use `peak_prev_token_mass` and add the
> copy-offset mass and the corrected head counts, so the "RETRACTED" annotation
> that stood in this table is replaced by measurements.*

**Features**: attention entropy tracking, the induction signal on the copy offset plotted
(metric scale consistent with the detection threshold) with the previous-token mass as a
control, W&B logging (`--wandb`), model saving
(`--save-model`), loss bump detection, 2×2 training curves plot, `--fresh-batches` (resample
per epoch), `--detect-every` / `--stop-on-confirmed` (detection cadence and early stop) and
`--seeds` (multi-seed manifest) added 2026-08-02; the detector and the content-vs-position
dissociation probe added 2026-10-19.

**Reference**: Olsson et al., "In-context Learning and Induction Heads," Transformer Circuits Thread (Anthropic), 2022.

**Figures**: `portfolio/figures/exp1_training_bump.png` — regenerated 2026-10-20 with the corrected detector: the fourth panel is now the **copy-offset** induction mass with the previous-token mass as a control (the old figure plotted the previous-token mass under the label "diag+1"). Quick scale (2L/4H, d_model 24, 150 epochs, fresh batches, seed 0), the configuration the `figures` target pins.

---

## Rung 2 — Grokking Modular Addition (Primary Flagship — REPRODUCED 2026-10-14; the 2026-08-11 NO-GROK was a metric artifact)

<!-- manifest: results/grokking_nanda_p113.json -->
<!-- manifest: results/grokking_repo_p113_energy.json -->

> **2026-10-14 — verdict REVERSED.** The NO-GROK claim (2026-08-11) was measured with
> the L1-mass `k_99`, the exact classifier the 2026-10-08 audit falsified on a synthetic
> noisy-sparse embedding. Re-run on a GPU with the **Nanda-faithful protocol** (job A:
> 40k full-batch steps, 3 seeds) and with the **old repo protocol plus the energy
> metric** (job B: the exact historical config re-run), the model **does** form the
> sparse Fourier circuit: `energy_sparse = 1.0` on all three seeds of **both** runs,
> `k_energy_90 = 5.7 ± 1.2` of 56 frequencies holding 90% of the embedding energy.
> The mechanism was sparse all along; the classifier was wrong.

**Question**: Can I reproduce the grokking phase transition on modular addition (a+b mod P) and reverse-engineer the discrete Fourier transform algorithm the model learns?

**Status**: [x] **REPRODUCED** — the question is answered *yes*, on both protocols, on a
GPU, with the post-audit metric. The historical CPU run that produced the NO-GROK
verdict reached the same embeddings (its L1 `k_99 = 111/113` matches job B's `110/113`);
it measured them with the broken classifier. Nothing about the training or the model was
ever wrong — only the reading.

| Metric | Job A — Nanda protocol, P=113, 3 seeds (manifest) | Job B — repo protocol (historical config), P=113, 3 seeds (manifest) |
|--------|----------------------------------------------------|---------------------------------------------------------------------|
| Device / runtime | CUDA, torch 2.11.0+cu128 | CUDA, torch 2.11.0+cu128 |
| Steps | 40,000 full-batch × 3 seeds | 5,000 epochs (batch 512) × 3 seeds |
| Final val accuracy | **0.9999 ± 0.0002** | **1.0000 ± 0.0000** |
| Generalization epoch (val ≥ 0.9) | 5919 ± 547 (range 5151–6386) | 759 ± 140 (range 657–957) |
| **Frequencies for 90% of energy (k_energy_90)** | **5.7 ± 1.2 of 56** | **8.7 ± 1.2 of 56** |
| Energy in the top-5 frequencies | 0.875 ± 0.038 | 0.764 ± 0.074 |
| **Sparse (energy criterion)** | **yes — 3/3 seeds** | **yes — 3/3 seeds** |
| L1-mass k_99 on the same embeddings | 109–110 / 113 | 110 / 113 |
| Wall clock | ~1.5h GPU (Kaggle, resumable) | ~1h GPU (Kaggle, resumable) |

**The audit's prediction, confirmed on the real embeddings.** The 2026-10-08 audit
pinned that a clean 5-frequency embedding with 1% additive noise reads as dense under
the L1-mass `k_99`, because L1 mass is dominated by noise spread over every bin. Both
GPU runs carry that fingerprint: `k_99` (L1) says 109–110 of 113 frequencies while the
energy metric says 5.7–8.7 of 56 carry the signal. The dense label was the noise.

**What the historical work got right, and stays right**: the train/val split fix
(2026-07-26), the checkpoint/resume machinery, the multi-seed manifests, the frequency
ablation (keep 59/59 → 0.0000 — a causal result about the dense *reading* that now
re-reads as confirmation that the few real frequencies are load-bearing), and the
generalization-epoch progress measures.

**Verdict ledger**: ADR-0003 row 1's NO-GROK stamp (2026-08-11) is **retracted** by this
run. The reversal is recorded in the Honesty Ledger (2026-10-14) and in issue #167's
closure. Per the gate note's own contract, the capstone's Phase 7 gate answer changes
from the honest negative to the positive (see
[capstone-gate-honest-negative](../07_capstone/notes/capstone-gate-honest-negative.md),
superseded 2026-10-14).

**The P=59 positive control, re-measured (2026-10-19, issue #196)**: the probe
was re-run with the post-audit energy metric, on the **repo protocol** (not the
Nanda config the old note claimed) — `results/grokking_p59_repo_energy.json`,
3 seeds, CPU, 5000 epochs, batch 128:

<!-- manifest: results/grokking_p59_repo_energy.json -->

| Seed | val accuracy | k_energy_90 (of 29) | k_energy_90 / n_freq | energy_sparse |
|------|--------------|---------------------|----------------------|---------------|
| 42 | 1.0000 | 5 | 0.172 | ✅ sparse |
| 43 | 0.9918 | 8 | 0.276 | ❌ not sparse |
| 44 | 0.9988 | 7 | 0.241 | ✅ sparse |

**Verdict: MIXED (2 of 3 seeds sparse), not "sparse".** The classification is
knife-edge — the `is_sparse` convention is "90% of the energy in fewer than
25% of the frequencies", and seed 44 sits at 0.241 while seed 43 sits at
0.276 — so the honest reading is "2/3, with one seed's solution slightly
denser", not the "SPARSE" label the first reading of this probe carried. No
re-run was attempted to move the label: re-running a seed until it agrees is
selection, not measurement. The probe's role (a cheap positive control for the
recipe) is served by P=113, which is 3/3 on both protocols; P=59 is kept here
as a footnote with its per-seed numbers.

**Still open, now smaller**: the protocol-ablation phase diagram (issue #168)
unblocks on this result and starts from the Nanda-faithful setup as designed —
still open and not scheduled, with its taxonomy clarified before the first cell runs
(see the Open Question below).

**Reference**: Nanda et al., "Progress Measures for Grokking via Mechanistic Interpretability," ICLR 2023 (oral).

**Figures**: `portfolio/figures/exp2_grokking_curve.png`,
`portfolio/figures/exp2_fourier_weights.png`,
`portfolio/figures/exp2_frequency_ablation.png`,
`portfolio/figures/exp2_progress_measures.png` — regenerated 2026-10-17 from the
P=113 seed-0 GPU checkpoint of job A (`results/grokking_nanda_p113.json`;
re-analysis provenance: `results/grokking_p113_gpu_reanalysis.json`). The
embeddings are identical to the earlier CPU-era rendering; the *dense*
captions/labels that predated the 2026-10-14 reversal have been corrected to the
sparse (energy) reading below. The GPU checkpoints are on disk
(`results/remote/grokking-p113/output2/repo/checkpoints/nanda/`), so no re-run
was needed — only a re-analysis.

---

## Rung 3 — Toy Models of Superposition

<!-- manifest: results/exp3_superposition.json -->

**Question**: How do features organize in a toy ReLU autoencoder under varying sparsity?

**Status**: [x] Phase transition reproduced 2026-08-02, after finding the actual root
cause of the 2026-07-26/2026-08-01 flat-recovery observations: the architecture had no
real bottleneck (see Honesty Ledger and
[superposition-setup-validity](../05_llm_engineering/proofs/superposition-setup-validity.md)). Rewritten to the canonical
Elhage et al. setup; the transition reproduces on the first run, cleanly, with no tuning.

<!-- manifest: results/exp3_superposition_sweep.json -->

| Sparsity | Features represented (mean ± std over 3 seeds) | Mean dimensionality | Mean \|corr\| |
|----------|----------------------|----------------------|--------------|
| 0.500 | 10.00 ± 0.00 | 0.250 ± 0.000 | 0.299 ± 0.004 |
| 0.200 | 14.67 ± 0.47 | 0.250 ± 0.000 | 0.315 ± 0.005 |
| 0.100 | 18.33 ± 0.47 | 0.250 ± 0.000 | 0.337 ± 0.003 |
| 0.050 | 20.00 ± 0.00 | 0.250 ± 0.000 | 0.349 ± 0.000 |
| 0.020 | 20.00 ± 0.00 | 0.249 ± 0.000 | 0.350 ± 0.001 |
| 0.010 | 20.00 ± 0.00 | 0.249 ± 0.000 | 0.349 ± 0.002 |
| 0.005 | 20.00 ± 0.00 | 0.249 ± 0.000 | 0.351 ± 0.001 |
| 0.002 | 18.00 ± 0.82 | 0.248 ± 0.000 | 0.346 ± 0.006 |
| 0.001 | 16.33 ± 0.94 | 0.248 ± 0.001 | 0.336 ± 0.006 |

**The sweep above had no manifest behind it (2026-11-11), and now it does.** The
2026-11-11 audit's number check found what the record had been hiding: the sweep path of
this experiment wrote figures and a stdout table and **never a record** — the only
tracked exp3 manifest was the multi-seed run at a single sparsity, so Rung 3's headline
table was the one public table in this ledger with no evidence behind it. `exp3` grew a
`--sweep-seeds` flag, the three-seed sweep ran on a clean tree
(`results/exp3_superposition_sweep.json`, 3 seeds x 9 sparsity levels), and the table
above is now **that manifest's numbers**, read back from it rather than from the
sweep's stdout.

**What the three-seed sweep changed, and what it did not.** The phase transition is
unchanged in shape: **10/20 at sparsity 0.5 rising to 20/20 by sparsity 0.05**, and
20/20 held down to sparsity 0.005. What the seed spread adds is the *tail*, which the
single-seed table could not show: at sparsity 0.002 the three seeds land at 19, 17, 18
of 20 (mean 18.00 ± 0.82) and at sparsity 0.001 at 17, 17, 15 (mean 16.33 ± 0.94).
The old table's single-seed "16 / 20" at sparsity 0.001 was one draw from that spread —
so the previously published "capacity limit at extreme sparsity" number is now a
**three-seed mean of 16.33 ± 0.94** rather than a single observation. The honest
statement of the limit is the mean ± spread, and the level at which the model stops
representing every feature moves with the seed.

**Re-measured after the seeding fix (2026-11-17).** The three-seed manifest at the
reference sparsity (`results/exp3_superposition.json`, 3 seeds, `single_sparsity=0.01`)
now records `n_represented` = 20.00 ± 0.00, and the sweep's 0.010 row is
20.00 ± 0.00: **the two code paths agree**, which is what the 2026-11-12 audit
said they would once the model was seeded before it was constructed. Before the fix the
single-sparsity manifest recorded 19.67 ± 0.47 (19, 20, 20) and the sweep 20.00 ± 0.00; both
are kept as `results/exp3_superposition_pre_seedfix.json` and
`results/exp3_superposition_sweep_pre_seedfix.json`, the record of what the old code
measured. The phase transition did not move: 10/20 at sparsity 0.5 and 20/20 from
sparsity 0.05 to 0.005. What moved is the tail, within its spread (see the table).

Expected (Elhage et al.): as sparsity decreases (features rarely co-active), interference
pressure drops and the model represents more features. **Observed: exactly this — 10/20 at
the densest setting rising to 20/20 by sparsity=0.05**, now measured over three seeds
rather than one. The old
flat/near-zero "recovery" numbers above the fix are struck through in
spirit, not deleted from this table's history: the root cause was that the model had no
actual compression to perform (the dataset pre-embedded features before the model saw
them), not a metric-scale issue, not a training-budget issue, and not the untied-weights
hypothesis tested 2026-08-01. `mean_dimensionality` sits close to `1/n_dimensions × n_avg`
across the sweep as expected for features sharing the bottleneck roughly evenly.

**Geometry check (2026-08-06, 5 features → 2 dims)**: the small-case Gram check is now
done — at and below sparsity 0.1 the 5 directions sit on a regular pentagon (gaps
70.2–73.8°, std ≤ 1.4° vs ideal 72°; best 71.6–73.0°, std 0.5° at sparsity 0.02);
the dense regime (0.2–0.5) is 4/5 represented and off-pentagon (std 22°+). The
equiangular geometry is the sparse-phase attractor, not a dense-phase property.
Figure: `portfolio/figures/exp3_pentagon_geometry.png`.

**Reference**: Elhage et al., "Toy Models of Superposition," Transformer Circuits Thread (Anthropic), 2022.

**Figures**: `portfolio/figures/exp3_feature_geometry.png`, `portfolio/figures/exp3_phase_change.png`

---

## Rung 4 — Circuit Verification via Activation and Path Patching

<!-- manifest: results/exp4_circuit_patching.json -->

**Question**: Can I find and causally validate a specific circuit via activation patching, path patching, and head ablation?

**Status**: [x] **The cascade ran end to end on Rung 1's own checkpoint (2026-10-20, re-measured 2026-11-17)** — and path patching is no longer unit-test-only. Patch site and metric fixed 2026-08-01 (see Honesty Ledger — the previous
implementation patched a tensor that never reached the residual stream, and measured
confidence rather than correctness). Path patching added; it did not exist in any form
before this pass. The pre-fix standard-scale recovery numbers (0.787, 0.270, ...) that
used to live in this section are **retracted** — they measured `top1 − top2` under a patch
that mostly didn't land, so they don't mean what they claimed to. Vocabulary-ambiguity task
design bug (see Rung 1) fixed 2026-08-02, since this rung reuses
`make_repeated_token_data`; `--seeds` added.

### The cascade, on the model Rung 1 trained (2026-10-20, re-measured 2026-11-17)

<!-- manifest: results/exp4_standard.json -->

Standard scale, the checkpoint of the full-budget run (epoch 3000), 3 seeds, analysed
with `--from-checkpoint` (the model is loaded, not retrained — the cascade is one
model, not two):

| Metric | Value (mean ± std, n=3) |
|--------|--------------------------|
| Confirmed heads (per seed) | 3, 3, 3 (all in the first layer) |
| **Head ablation effect** (drop in the answer−counterfactual logit difference) | **0.5895 ± 0.1405** (range 0.464–0.786) |
| **Path-patching effect** (the head's *direct* effect on the logits) | **0.7052 ± 0.0411** (range 0.648–0.742) |
| Mean activation-patching recovery (layer/position combos) | 0.0834 ± 0.0002 |
| Dissociation probe — content mass / period mass | 0.0310 / 0.8096 (**positional**, 3/3 seeds) |

**This is the first end-to-end path-patching result in this repository**: the
head that the corrected detector finds is also the head that carries the task's
answer. Ablating it costs 59% of the logit difference; path patching — which
isolates the head's direct contribution to the logits, with every other head,
every MLP and the head's own indirect effects kept clean — attributes 71% of
that to it.

**Re-measured after the seeding fix.** The first measurement (2026-10-20) was 0.4445 ± 0.0425 for the
ablation and 0.8215 ± 0.1255 for path patching, on checkpoints trained before the model was seeded
before construction (kept as `results/exp4_standard_pre_seedfix.json`). On the re-trained checkpoints
the ablation effect is higher and path patching lower, each by more than the earlier standard
deviation: the two interventions measure the same head from two angles, and the split between
"what removing it costs" and "how much of that cost is its direct effect" is not stable across
initializations, even though the finding (one first-layer head carries the answer, positionally)
is.

**What the interventions do not settle**: the *mechanism* of the copy. The
dissociation probe says the head copies from a fixed offset rather than from
the previous occurrence of the same token (see Rung 1 and
[ADR-0032](../docs/adr/0032-induction-detector-and-the-positional-shortcut.md)),
and the K-composition between layers stays far below its 0.4 bar (Rung 1), so this is a
single-head circuit on a periodic task, not the two-step induction circuit.

### Quick-mode 3-seed manifest, 2026-08-02 (re-measured 2026-11-17)

(`vocab_size=64, seq_len=12, d_model=32, epochs=500`):

| Metric | Value (mean ± std, n=3) |
|--------|--------------------------|
| Final val accuracy | 0.446 ± 0.039 |
| Mean activation-patching recovery (10 layer/position combos) | 0.203 ± 0.005 |
| Induction heads detected | **RETRACTED — uninterpretable** (this rung's detector measured `attn_probs.diagonal(offset=1)`, the strict upper triangle of a causal softmax: identically zero. See the Honesty Ledger's 2026-10-19 entry) |
| Head ablation / path patching | not run (no head to target) |

Dated correction 2026-09-06 (MP-85 Session 0): this row previously read `0 / 8`.
The manifest ran `n_layers=2, n_heads=2` (4 heads total). Superseded on
2026-10-19: the count itself was never a measurement — this rung's detector
could not fire on any model, so "0 / 4" and Rung 1's "0 / 8" were both
statements about broken code.

Activation patching runs cleanly and finds a real, small, consistent recovery signal
(~0.20, not zero) even without a detected induction head — some circuit sensitivity exists
at these (layer, position) combinations. In the quick manifest, head ablation and path
patching were skipped (no head to target), so path patching's implementation was
validated only by its unit tests (self-patch-is-zero, runs-and-returns-expected-keys);
the 2026-10-20 cascade run above closes that gap on a real head.

**Method**:
1. Analyse the model Rung 1 trained (`--from-checkpoint`, the default for the
   cascade) or train one here; detect induction heads with the shared detector
   on the copy offset `q-(L-1)`, confirmed by the K-composition mechanism.
2. **Residual stream activation patching**: hook the block's attention module
   (its output is already post-`W_O`) to override `resid_mid` at a given (layer,
   position) from a corrupted run — a second, disjoint batch from the same task
   generator, not a within-sequence permutation (which destroys the induction
   structure and leaves no well-defined correct answer). Metric:
   `logits[answer] − logits[counterfactual]` against each batch's real
   next-token label. The attention-only model (no MLP) is patched by
   overriding the block output at the target position, which is the exact
   analogue of the same intervention.
3. **Path patching**: isolate a single head's *direct* effect on the logits by decomposing
   `attn_out` through `W_O`'s per-head column blocks and swapping only that head's
   contribution to the final residual stream — everything else (other heads, all MLPs,
   this head's own indirect effects through later layers) stays clean.
4. **Head-level zero ablation**: `head_mask` zeroes a head's contribution before `W_O`.

All three interventions carry falsification tests: self-patching (corrupted == clean) must
be an exact no-op for both activation and path patching
(`tests/test_exp4_circuit_patching.py`), and patching against a genuinely different run
must move the logit diff somewhere.

**Outputs**: `portfolio/figures/exp4_attention_patterns.png`,
`portfolio/figures/exp4_patching_results.png`,
`portfolio/figures/exp4_head_ablation.png` — all three regenerated on
2026-10-20 from the **standard-scale checkpoint** (the GPU run's
`exp1_checkpoint_seed0.pt`, epoch 3000), not from a quick-mode model: the
head-ablation figure is the one that used to be missing, because head
ablation is skipped whenever 0 induction heads are detected, and the cascade
had never had a head to point at. It does now.

**Reference**: Wang et al., "Interpretability in the Wild: a Circuit for Indirect Object Identification in GPT-2 small," ICLR 2023. Zhang & Nanda, "Towards Best Practices of Activation Patching," ICLR 2024 — the corrective paper for exactly the site/metric mistakes found here.

---

## Rung 5 — Sparse Autoencoder Feature Dashboard

<!-- manifest: results/exp5_sae_dashboard.json -->

**Question**: Can I train an SAE on synthetic residual stream activations and extract interpretable features? Does it work on real activations, not just synthetic ones?

**Status**: [x] Synthetic baseline reproduces exactly. [x] Real-activation upgrade shipped
2026-08-02: `--activations-from` harvests genuine residual-stream activations from a
trained induction-heads checkpoint via a forward hook on `ln_final`, and the architecture
gained the pre-encoder bias (`x - b_dec`) it was missing — Bricken et al.'s actual SAE, not
an approximation of it. Dead-feature threshold fixed 2026-08-01 (see Honesty Ledger).
[x] **2026-10-20 — the real-activation run landed on a checkpoint with a confirmed
head**, which is the pending item this rung had been carrying: the SAE now sees a
*circuit-bearing* residual stream, and the picture changes qualitatively (below).

<!-- manifest: results/exp5_real_activations.json -->

| Metric | Synthetic (d_model=64, 8× dict, manifest 2026-08-13) | Real, old (d_model=32, from a 2000-step shakedown checkpoint — no tracked manifest, historical) | Real, **new** (d_model=64, from the standard-scale confirmed-head checkpoint, 2026-10-20, re-measured 2026-11-17) |
|--------|-------|-------|-------|
| Dictionary size | 512 | 256 | 512 |
| L0 sparsity | 96.60 / 512 (18.9%) | 136.25 / 256 (**53.2%**) | **19.01 / 512 (3.7%)** |
| Fraction of variance explained (FVE) | 0.9749 (97.5%) | 0.9997 (99.97%) | **0.99998** |
| Reconstruction MSE | 0.00101 | 0.1251 | 0.00054 |
| Dead features (fixed 1e-4 threshold) | 39 / 512 (7.6%) | 0 / 256 (0%) | **336 / 512 (65.6%)** |

**What changed, and why it matters.** The old real-activation row read *dense*: 53% of
the dictionary firing per input, with a reconstruction MSE an order of magnitude worse
than the synthetic baseline. This repository read that as "the residual stream of a
small, undertrained model has no sparse structure to find". The new run replaces the
model with the one Rung 1 actually trained (standard scale, 3000 epochs, confirmed head)
and the picture inverts: **L0 19.0 of 512 (3.7%)** with FVE 99.998% and an MSE of 0.0005.
The activations *are* sparse — but only once the model has a circuit to write into
them. The old "dense reconstruction" was a statement about an undertrained model, not
about the SAE.

**And the remaining weakness is the other one.** With 8× the dictionary, **66% of the
features never fire** — the dictionary is far larger than this residual stream needs.
That is a dictionary-size choice, not a property of the model, and it is the honest
"what did I add" reading of this rung: the sparsity gap is closed (53% → 3.7% L0), and
what is left is an oversized dictionary, not a missing mechanism.

**Read honestly, not as an unqualified win.** The *old* real-activation row
reconstructed better but far less sparsely than synthetic — 53% of the dictionary fired
per input versus 17% for synthetic — and this repository read that as "a 32-dimensional
residual stream from a small, undertrained model may simply not contain many genuinely
sparse, disentangled features". That was the "what did I add beyond the original?"
distinctiveness gate (`07_capstone/research-plan.md`) this rung was missing: a real
degradation in the metric that matters (sparsity, not just reconstruction) is a more
informative result than a second clean synthetic number would have been. The
2026-10-20 run answers that gate with the model the rung was waiting for: the sparsity
problem is **gone** (53% → 3.7% L0) and what remains is a dictionary 8× too large, not a
missing mechanism.

**Reference**: Bricken et al., "Towards Monosemanticity" (2023); Cunningham et al., "Sparse Autoencoders Find Highly Interpretable Features in Language Models," ICLR 2024.

**Figures**: `portfolio/figures/exp5_sparsity_tradeoff.png`,
`portfolio/figures/exp5_feature_histogram.png` (synthetic),
`portfolio/figures/exp5_sparsity_tradeoff_real.png`,
`portfolio/figures/exp5_feature_histogram_real.png` (real activations).

The real-activation figures were a recorded pending item until 2026-10-22:
they are regenerated from **the same checkpoint the tracked manifest names**
(the GPU run's `exp1_checkpoint_seed0.pt`, epoch 3000) with the manifest's
own configuration, and the re-run reproduces the manifest's numbers exactly
(L0 19.01/512, 336/512 dead, 65.6%). A figure that cannot be regenerated
from the evidence is a claim, not a figure.

---

## Rung 7 — The instrumentation on GPT-2 small (pre-registered, ADR-0034; instrument validated, causal stages not reproduced)

<!-- manifest: results/gpt2_small_stage1.json -->
<!-- manifest: results/gpt2_small_stage2.json -->
<!-- manifest: results/gpt2_small_stage3.json -->
<!-- manifest: results/gpt2_small_stage4.json -->
<!-- manifest: results/gpt2_small_stage5.json -->

Every other rung here studies a model of at most 4.3 million parameters trained on a
synthetic task. This one runs the same hand-written instruments (the hook cache, the
shared attention-mass detector, head ablation) on **GPT-2 small**, 124 million
parameters, 12 layers of 12 heads, loaded from `openai-community/gpt2` into a
pure-PyTorch implementation (`src/models/gpt2.py`). The five stages, their thresholds
and their reference (Wang et al. 2022, arXiv:2211.00593) were frozen in
[ADR-0034](../docs/adr/0034-gpt2-small-real-model-test.md) **before any code touched the
weights**; stage 1 was amended once, before any run, because an absolute tolerance of
1e-3 is below float32 resolution on GPT-2's very large residual activations. No
threshold was changed after a number was seen. Everything ran on CPU, three seeds
where a stage uses seeds.

| Stage | Frozen criterion | Measured (mean ± std) | Outcome |
|---|---|---|---|
| 1. Parity with the Hugging Face reference (gate) | scale-normalised error at most 1e-5 on logits and on every residual stream | the largest error is about 1e-6 on 8 fixed prompts | **PASS** |
| 2. Induction heads by attention mass | heads L5H5 and L6H9 both in the top 10 of 144 and at least 0.3, on every seed | L5H5: mass 0.9291 ± 0.0006, rank 1; L6H9: mass 0.9180 ± 0.0015, rank 2 | **PASS** |
| 3. Induction heads are causally used | ablating L5H5 and L6H9 cuts the in-context gain by at least 10% | gain 12.8604 ± 0.0237 unablated, 12.9398 ± 0.0346 ablated (see text); ablating the stage-2 top 10 instead cuts it by 0.7723 ± 0.0089 | **FAIL** |
| 4. The model solves the indirect-object task | mean logit difference at least 2, positive on at least 90% of prompts | 2.7535 ± 0.1134, positive on 0.99 of 100 prompts per seed | **PASS** |
| 5. Name movers matter for that task | ablating L9H6, L9H9 and L10H0 cuts the logit difference by at least 30% and more than the 95th percentile of 20 random triples | cut by 0.0168 ± 0.0192; random-triple 95th percentile 0.1847 ± 0.0157 | **FAIL** |

**What passed.** The implementation equals the reference. On repeated random tokens the
repository's detector, written for a 4-head toy model, ranks the two induction heads the
literature reports (5.5 and 6.9) **first and second of 144** on all three seeds, at
roughly 0.93 and 0.92 of their attention mass. The next three heads by this score were
not in the reference set: 7.10 (about 0.91), 5.1 (about 0.90 to 0.91) and 7.2 (about 0.83
to 0.84), after which the mass falls to about 0.5 (10.1, 9.6, 9.9, 10.7, 5.0). The
instrument transfers to a real model, and it found more induction-like heads than the
two it was asked about. On the indirect-object prompts the model prefers the indirect
object by a mean logit difference of about 2.75 (the paper's 3.56 is on different
prompts and is not a comparison).

**What failed, and what that does and does not mean.**

- *Stage 3.* Zero-ablating heads 5.5 and 6.9 left the in-context gain **unchanged**: it
  rose by 0.6% (the relative fall, a negative number, was -0.0062 ± 0.0008; the criterion
  asked for at least 0.1), while ablating the whole stage-2 top 10 removed
  77% of it. The criterion expected a small effect and got none. The reading the data
  support is *redundancy*: at least five heads attend to the copy position about as
  strongly as 6.9 does, so removing two is compensated. It does not show that 5.5 and
  6.9 are unused.
- *Stage 5.* Ablating the three name movers cut the logit difference by about 1.7% and
  twenty random triples had a 95th percentile of about 18%, so by the frozen rule the
  name movers do **not** stand out. Two known effects could produce this and neither was
  separated here: the circuit has *backup* name movers that take over when the primary
  ones are removed, and zero ablation (used here, as in Rung 4) is off-distribution where
  Wang et al. used mean ablation. The ADR said in advance that a FAIL in this stage is
  weaker evidence than a FAIL in stage 1.

**What this establishes and what it does not.** It establishes that the hand-written
hook cache, detector and ablation machinery work on a pretrained 124-million-parameter
model and agree with the literature on *which heads attend like induction heads*. It
does **not** reproduce the causal claims about the indirect-object circuit, and the
repository does not claim that circuit. A follow-up with mean ablation and with path
patching, which is how the paper localised the name movers, would be a new
pre-registered ADR superseding none of this one; it has not been run.

**Two limits of the instrument, found in review (2026-11-19).** The stage-3 "top-10" set (the manifest key
`icl_gain_drop_top10_control`) contains the two ablated heads, because stage 2 requires them to be in the top ten; it
therefore measures how large the redundant family of induction-like heads is, not whether 5.5 and 6.9 are specific, and
it carries no criterion in the ADR. And the `wall_clock_seconds` of stages 2 to 5 is the combined time of the whole
seed loop (about 15 minutes), written into each of the four manifests. The run was not repeated for either point: the
numbers above are as recorded, and the code was tightened afterwards (a context manager that always restores the
model, a rank that counts ties against the target head, the device read from the model) without changing a result.

**Reproduce**: `uv run --extra real python -m src.experiments.exp7_gpt2_small` (about 15
minutes on CPU after a one-time weight download).

## Open Question — Solution-Regime Phase Diagram (protocol ablation, unblocked 2026-10-14; not scheduled)

**Status**: [ ] No claim yet — but no longer *blocked*. The 2026-10-08 audit removed
the earlier draft (a 100-epoch test manifest, empty aggregate, models that had not
generalized) and asked for the audit to run first. It has: the Nanda-faithful
positive control grokked with a sparse Fourier circuit (Rung 2 above), so the
question "where is the boundary between the sparse circuit and its absence across
protocol deviations?" is now answerable by a sweep instead of speculation. The
sweep runner is refactored and tested (delegates to exp2's own protocol code,
budgets in optimizer steps, records the energy metric); the run itself
(issue #168) is one command on the free GPU tier. No numbers are cited here
until that sweep's manifests land.

**Moved to v1.1 on 2026-10-19.** The sweep is ten cells × three seeds × 20k
full-batch steps at P=113 — one to two weeks of the free GPU quota — while the
v1.0 milestone's one open issue (#169, the standard-scale induction run and the
head validation it unlocks) is still open. The run is therefore scheduled
*after* #169, not instead of it: the boundary question is worth a milestone of
its own, and spending the quota on it first would have delayed the rung that
the milestone is about. Issue #168 was reopened and moved to the v1.1
milestone for that reason.

**Update 2026-11-19.** #169 is closed and v1.0, v1.1 and v2.0.0 have shipped, but the
sweep has not run and is **not scheduled**: it still costs one to two weeks of the
free GPU quota, and no claim in this repository depends on it. Until its manifests
land, no phase-diagram number appears anywhere in the record.

**Pre-registered taxonomy, clarified before any cell ran** (2026-10-19): the
runner used to compare the aggregate mean against 0.5 — a *majority* rule —
while the configuration file's comment said "3/3 seeds", and the disagreement
was invisible because no cell had ever been executed. The reading that will be
applied is the explicit one:

| Label | Meaning |
|---|---|
| **SPARSE** | every seed sparse (3/3) — the same bar the P=113 positive control clears |
| **MIXED** | 1 or 2 of 3 seeds sparse: a *boundary* cell, reported as such and never folded into SPARSE |
| **DENSE** | no seed sparse (0/3) |

The per-seed count (k/3) and the per-seed `k_energy_90` are reported next to
every cell, so no reader has to infer them from an aggregate.

---

## Phase Gate Progress

| Phase | Status | Gate proof |
|-------|--------|------------|
| 1 — Foundations | ✅ Complete | — |
| 2 — Classical ML | ✅ Complete | complete-ml-pipeline |
| 3 — Deep Learning | ✅ Complete | gradient-flow-and-architectures |
| 4 — NLP & Transformers | ✅ Complete | circuit-analysis-complete |
| 5 — LLM Engineering | [~] Instrumentation done (hooks, determinism, harvesting, circuit datasets proven; nnsight pending — not installed, and the capture protocol the repo uses does not need it) | — |
| 6 — Production AI | [~] Reproducibility harness built (multi-seed + manifests + `verify-claims` + figure-provenance gate 2026-08-07, kill drill + bit-identical checkpoint/resume, CI/mypy fixed, paper compiled and shipped) — **W&B descoped 2026-09-08** (no credential ever worked; the manifests are the record), **HF Spaces descoped 2026-10-11** (the dashboard is a product, the science is in the manifests), **the mini-paper prose is written** (`portfolio/paper/main.tex`) | [reproducible-from-clean-clone](../06_production_ai/proofs/reproducible-from-clean-clone.md) (GREEN 2026-08-27, transcript committed) |
| 7 — Capstone | ✅ Gate passed 2026-10-12 on the honest negative, **upgraded to the positive 2026-10-14** | [capstone-gate-honest-negative](../07_capstone/notes/capstone-gate-honest-negative.md) (dense mechanism defended with manifests) → superseded: the sparse circuit is real ([Rung 2](#rung-2--grokking-modular-addition-primary-flagship--reproduced-2026-10-14-the-2026-08-11-no-grok-was-a-metric-artifact)). The planned 3×20k joint run executed 2026-10-14: the modular/induction **dissociation persists at full budget** (induction 0.5034 ± 0.0002 — the same plateau as the 2k shakedown; modular 0.1699 ± 0.0286 vs 1.0 solo), recorded in the [capstone execution log](../07_capstone/execution-log.md), `results/capstone_20k.json` |
