---
tags: [portfolio, results]
---

# Honesty Ledger

Every audit that caught a real problem in this repository, newest first. The results themselves are in [RESULTS](RESULTS.md); this file is the record of how that record was corrected.

<!-- manifest: results/grokking_nanda_p113.json -->
<!-- manifest: results/grokking_repo_p113_energy.json -->
<!-- manifest: results/grokking_p59_repo_energy.json -->
<!-- manifest: results/induction_content.json -->
<!-- manifest: results/exp4_content.json -->
<!-- manifest: results/exp1_induction_fixed_batches.json -->
<!-- manifest: results/exp1_induction_fresh_batches.json -->

Thirteen audits have now caught real problems in this repository's causal claims and
evidence base. They include claims that were wrong or unbacked, a claim that was
**right and had been called wrong by its own metric** (2026-10-14), four
content-task audits (2026-10-22, 2026-10-25, 2026-11-01 and 2026-11-11) that found the
experiment supposed to close the last open question **could not have produced a
verdict at all** — first because its verdict code would crash, then because its
instrument measured the wrong position, then because the verdict read the wrong
head and the cascade could silently analyse another model, and finally because
the published verdict was not the one the code computes — a twelfth (2026-11-12)
that found the run seed does not pin the model's initial weights, so two
commands of one configuration disagreed — and a thirteenth (2026-11-17) that found
the repository's own documentation of itself (a model card, a skill tree) stating
things its evidence did not. All
entries stay here — the point of this section is to make it easy to
see the trend (are correctness problems getting caught faster, or accumulating?),
not to keep only the latest one.

## 2026-11-17 — The record described models it never trained, and a rule nobody enforced

The thirteenth audit, and the first to audit the repository's *own documentation of
itself* rather than a result. It started from one question: does every sentence a
visitor reads match a manifest, and does every checked box have the evidence its own
rule demands?

**What was broken.**

1. **The model card described models this repository never trained.** It said
   "~1–50M parameters", "BPE for natural-text experiments", "English", and a "Synthetic
   IOI" Rung 4. The manifests say 120 to 4,259,584 parameters, integer token ids and no
   text at all, and a Rung 4 that analyses Rung 1's own checkpoint. It was rewritten from
   the manifests, and the false phrases joined the `docs-audit` ratchet.
2. **The skill tree's rule was written and never checked.** "Check a skill only when an
   exercise **and** a proof demonstrate it." Eighty-five checked items linked neither or
   one of the two: 32 of 44 skill-tree entries, a Phase 3 with eight checked skills and
   one proof, and checklists that ticked tools the repository had descoped or never used
   (TransformerLens, SAELens, nnsight, attribution patching) and a top-p sampler that was
   never implemented. `make vault-check` now enforces the rule. Of the 85: 32 linked to
   exercises and proofs that already existed, 22 became `[~]` (studied, not verified), 11
   became `[-]` (descoped, with a reason), and the rest cite the manifest or deliverable
   that already backed them. Exercises and proofs written afterwards to close gaps are
   marked `authorship: claude`: they show a skill is demonstrated and checkable, not that
   the repository owner reconstructed it from memory.
3. **Two defects in code that nothing published used**, found by writing the exercises
   whose tests then failed on the old code: the BPE tokenizer silently dropped newlines,
   tabs and repeated or trailing spaces, so `decode(encode(text))` was not `text`; and
   `roc_auc_score` ranked tied scores in the order they appeared, so a constant scorer
   got an AUC of 1.0 or 0.0 instead of 0.5.
4. **The seeding defect of the 2026-11-12 audit was documented but not fixed.** It is
   fixed now in `exp1`, `exp3` and `exp4` (see that entry's addendum).

**What it changes.** The model card, the README, the vault home, the descope register and
`results/INDEX.md` now say what the manifests say. Process documents (the micro-phase
roadmaps and ledger ADRs) moved to `archive/process/`, where they are marked as history.

**What it does not change.** No published number moved: none of the defects touched a
manifest. The two code defects are in functions no experiment calls.

## 2026-11-12 — The run seed did not pin the model's initial weights: two commands of one configuration disagreed

The twelfth audit, and the first one about *what a seed means* rather than
about a number being wrong: it found that the run seed `exp3` reports does
not determine the model that run starts from — and that
two commands differing only in which rung code path they take had been
published side by side as if they measured the same thing.

**What was broken.** In `exp3`, the model is constructed **before**
`train_autoencoder` calls `set_seed(seed)` — the seeding happens inside the
training function, one line after the weights have already been drawn. The data
is pinned (the dataset has its own `np.random.default_rng(seed)`), and the
training is pinned, but the **initialization is not**: the weights come from
whatever ambient torch RNG state happened to be at construction time. So a
"seed" pins the data and the batch order, but not the starting point of the
trajectory.

**How it was found.** The Rung 3 sweep manifest and the Rung 3 single-sparsity
manifest record **the same nominal configuration** — sparsity 0.01, epochs 600,
8000 samples, batch 512, lr 0.01, seeds 0, 1, 2 — and they disagree:
`results/exp3_superposition.json` says `n_represented` = 19.67 ± 0.47, while
`results/exp3_superposition_sweep.json` says 20.00 ± 0.00 for the same level.
Two commands that differ only in which code path they take should not report
different answers for one configuration.

**Why they disagree, measured rather than argued.** The two code paths build
the model at different points in the ambient RNG stream, so they start from
different weights:

- the **single-sparsity** path calls `set_seed(args.seed)` once in `main()`,
  before the per-seed loop: the first seed's model is built from that pinned
  state, and each later seed's model is built after the previous seed's
  training has consumed the ambient stream;
- the **sweep** path builds nine models per seed, one per sparsity level, so
  the model at sparsity 0.01 (the sixth level) is built after five trainings
  have consumed the stream — a different position in it, and therefore
  different initial weights, than the single-sparsity path's.

Reconstructing both positions end to end reproduces both numbers exactly: the
single-sparsity position gives 19/20 and the sweep position gives 20/20 at
sparsity 0.01, seed 0. The mechanism is confirmed, not inferred.

**How far the defect reaches, also measured.** The initialization never
depends on the per-seed value at all: a fresh process starts from the state
`main()` sets once with `set_seed(args.seed)`, so seed 0 alone and seed 1
alone build **identical** initial weights (`fcea0c2b467a6709`). What varies
is the position in the sequence: seed 1 after seed 0 starts from
`0ae834eafda3d9c0`. So "seed N" determines a run's *data* and *batch order*
but not its starting point — which is why `--seeds 1` alone happens to land
on 20/20 (the same saturated value the manifest records for seed 1) while
starting from different weights than seed 1 in a multi-seed run.

**What it changes.** The Rung 3 sweep table is now published from the sweep
manifest (mean ± std over three seeds, and the per-seed range at the two
sparsest levels), instead of from a single untracked run — the sweep's numbers
are now the record, and the audit's number check polices them (the table's
exemption from that check is gone, and a test fails if a number in it stops
matching the manifest). The paper's sweep paragraph and the Rung 3 portfolio
page carry the same manifest-backed numbers.

**What it does not change.** The phase transition itself: **10/20 at sparsity
0.5 rising to 20/20 by sparsity 0.05**, reproduced by the three-seed sweep.
No threshold, budget, seed or decision rule changed, and no number was
re-tuned after seeing the data. The published 19.67 ± 0.47 for the
single-sparsity manifest is **not** retracted — it is exactly what that run
measured, and it is still what that manifest says. What changes is that the
repository now knows *why* it cannot be compared with the sweep's 20.00 ± 0.00
at the same nominal configuration, and the extreme-sparsity "capacity limit"
is quoted as a three-seed mean ± spread (17.00 ± 0.82 at sparsity 0.001)
rather than as one seed's 16/20.

**What is reproducible, measured.** Each path reproduces **its own** manifest
exactly, which is why this was never caught: re-running the single-sparsity
command reproduces its per-seed `n_represented` values (19, 20, 20) to the
digit, and re-running the sweep reproduces the tracked sweep's seed-0 row on
all 27 recorded fields to eight decimals. The defect is therefore not
non-determinism — it is that **two different commands that differ only in
which rung's code path they take were published as if they measured the same
thing**. The numbers were always reproducible; what was wrong was the
comparison between them.

**What it does not change either.** No other experiment's published number
moves, and the scoping was checked rather than assumed: `exp2` and `exp5` seed
**before** constructing their model, so their seeds are pinned; `exp1` and
`exp4` construct theirs before the seeding call, in the same way `exp3` does —
but neither records two code paths of one configuration, so no two tracked
manifests of this repository contradict each other because of it. The fixed-vs-fresh
comparison — this repository's one solid Rung 1 finding — is unaffected, and
was checked directly: the two arms draw **identical** per-seed initial weights
(`50b106e83b3bb8c7`, `26cec94b0ea967ef`, `19b718a593a9e645`), because both
arms consume the same number of permutations per epoch, so the batch regime
really is their only difference. The defect is in the *seed's meaning*, not in
any published figure. Fixing it properly (seeding before construction, then
re-running the affected rungs) is a separate measurement campaign with new
numbers, and it is not performed here: it would replace published manifests
rather than explain them.

**2026-11-16 — the code is fixed; the manifests are not yet re-measured.**
`exp1`, `exp3` and `exp4` now seed **before** constructing the model
(`build_seeded_model`, `build_autoencoder`, `_build_model`), and
`tests/test_seed_pins_init.py` holds the property with the audit's own
instrument: the digest of a seed's initial weights is the same alone, after
another seed, and at every level of the sparsity sweep. The consequence is
stated here rather than left to be discovered: the tracked manifests of those
three experiments were recorded **before** this change, so re-running their
commands today starts from different initial weights and will not reproduce
their per-seed values to the digit. They remain the record of what the pre-fix
code measured. The re-measurement that replaces them is open work, and no
published number has been changed in anticipation of it. `exp2`, `exp5` and the
capstone are unaffected: they already seeded before construction.

**2026-11-17 — the re-measurement.** The fix above was applied (`build_seeded_model`,
`build_autoencoder`, `_build_model`) and the affected experiments were re-run: Rung 3 on CPU,
Rung 1 and the content task on a free Kaggle GPU from the immutable tag `v2.0.0-rc1`, and the
Rung 4 and Rung 5 cascades on CPU against the new checkpoints. Every pre-fix manifest is kept,
unedited, as `results/<name>_pre_seedfix.json`. What the re-measurement showed:

- **Rung 3: the contradiction closed.** The single-sparsity manifest and the sweep's 0.010 row
  now agree (20.00 ± 0.00 both), which is the 2026-11-12 diagnosis confirmed. The phase transition did not
  move; the extreme-sparsity tail moved within its spread (16.33 ± 0.94 at 0.001).
  The pentagon geometry check (5 features into 2 dimensions) has no manifest and was **not** re-run in this pass
  (it takes hours on the CPU used here): its figure and its gap statistics predate the fix and are reported as such.
- **Rung 1 and the fixed-vs-fresh comparison: the findings held.** Heads form early, in the first layer,
  and copy by position; fixed batches still memorize (0.0046 ± 0.0003
  against 0.5352 ± 0.0001).
- **Rung 4: two numbers moved by more than their own error bar.** Head ablation 0.5895 ± 0.1405 (was
  0.4445 ± 0.0425) and path patching 0.7052 ± 0.0411 (was 0.8215 ± 0.1255).
- **Rung 5: the dictionary is less dead than reported.** 65.6% of features never fire (was 78.1%).
- **The content task changed verdict.** PARTIAL became NEGATIVE: no head is confirmed on any seed.
  The behaviour is unchanged (content-based on 3/3 seeds); the *circuit* is a single head on one
  seed and a distributed group on the other two, so the earlier "carried by a single head on 3/3
  seeds" described one initialization.

No threshold, budget or decision rule was changed after seeing a number, and no seed was dropped. The
documents that quote these numbers were updated in the same change, and `make docs-audit` checks the tables.

## 2026-11-11 — The published verdict was not the verdict the code computes, and the run's strongest numbers were never published

The eleventh audit, and the first one that audits the repository's own
*conclusion* rather than its instrument: it found that the headline result of
issue #200 — the content-based induction task — was published with a verdict
that the committed code could not reproduce, and that the run's strongest
measurements were missing from the record entirely.

**What was broken.** Four things, each independent of the others:

1. **The verdict could not be computed at all.** The training run was pinned
   at commit `88147ee`; the cascade that measures criterion 7 was executed
   afterwards, at `891ef46`. The verdict module refused the whole run for
   that difference ("a cascade from a different commit is not the
   pre-registered instrument"), so `make content-verdict` exited 1 with
   `RUN STATUS: INCOMPLETE` and **no verdict**, while
   `portfolio/RESULTS.md` published a PARTIAL verdict and told the reader the
   artifact was "regenerated with `make content-verdict`". The published
   number was not derivable from the committed evidence.

2. **The published per-seed table did not match the manifests.** The table
   said "Path patching: NOT MEASURED" on every seed. The exp4 addendum
   manifest records `path_patch_measured = 1` and
   `mean_path_patch_effect = 1.0771` on seed 0 — the criterion is *measured*
   and it *passes*. With the cascade joined, seed 0 is POSITIVE (7/7), not
   PARTIAL.

3. **The strongest numbers of the run were never published.** The mechanism
   report — the *secondary* report the pre-registration asks for — was
   computed, written into the manifest and then left out of the record. It
   says that on the two seeds the per-head rule calls NEGATIVE, the model
   copies at **0.9976 / 0.9988** (non-modal 0.9972 / 0.9986) against a
   fixed-offset baseline of **0.155 / 0.158**, and that **one head alone
   removes 0.9298 / 0.9402 of the copy accuracy**. The published table's
   "NOT MEASURED" cells made that look like an absence of evidence where the
   evidence was in the manifest all along.

4. **The paper described a sweep that has never run.** `main.tex` carried a
   "Deviations from Pre-Registration" paragraph about the phase-diagram
   cells ("no cell is DENSE", a SPARSE count of "4 / 2 / 6", a
   `NOT_GROKKED` gate). No `results/phase_diagram_*.json` manifest exists
   anywhere in the repository or in the downloaded GPU outputs, and
   `configs/phase_diagram_ablation.yaml` claimed the reduction decision was
   taken "after the sweep ran on GPU". The sweep has not run. This is the
   "documentation ahead of its evidence" failure the ledger exists to
   prevent, in the one document a reader is most likely to take at face
   value.

**What it changes.** The verdict is now **two verdicts, published side by
side**: the pre-registered one (the training run alone — criterion 7 was not
part of it, so it is `NOT MEASURED` there — seed 0 PARTIAL, seeds 1–2
NEGATIVE, run PARTIAL) and the causal addendum (the same run plus the
cascade, with the commit difference declared in its provenance — seed 0
POSITIVE, seeds 1–2 NEGATIVE, run NEGATIVE by the frozen majority rule). The
strict refusal still exists for the merged mode. The mechanism report is
published with its numbers. The paper's paragraph about the sweep is deleted
until the sweep has run.

**What it does not change.** The seven criteria, their thresholds and the
decision rule are untouched. No number is re-tuned after seeing the data, no
seed is dropped, and the budget is not extended. The word "induction head" is
still not used for this task. The retraction of the two "NEGATIVE" seeds as a
statement about the *model* is **not** a retraction of the verdict: the
verdict stands as the frozen rule applied to the frozen instrument, and what
changes is that the record now also carries the measurements that explain
what the verdict is about.

## 2026-11-04 — Finalization of Content Task Instrumentation
The standard-geometry CPU de-risk (`results/induction_content_derisk_standard.json`) was successfully run, and the verdict module (`src/experiments/content_verdict.py`) computed the verdict. The run is `INCOMPLETE` (due to being a de-risk pilot with seed 0 only), but the instrumentation and verdict criteria are verified. The full GPU run is queued and pending.

The tenth audit, again before the GPU run. The 2026-10-25 de-risk made the
central shape visible: the model copies by **content** (0.9993 overall,
0.9991 on non-modal queries, 0.8347 above the fixed-offset baseline) while
`total_induction_heads = 0`, because K-composition is 0.0918. Three
candidate heads carry the copy jointly: group ablation 0.9956 against a
largest single-head drop of 0.0986. The instrument as shipped would have
described that model as "NEGATIVE (unexplained)" without naming the circuit
it had measured, and could have computed its causal criteria from a model
it never trained.

**What was broken.** Four things, each independent of the others:

1. **Criteria 1–2 read the screen's peak, not the confirmed head's mass.**
   The pre-registration says "`content_mass` of the **confirmed** head";
   the code read `peak_content_mass`, the best head on the screen,
   confirmed or not. A strong head the detector rejected could carry both
   criteria for a weak confirmed one. `exp1` now records
   `confirmed_content_mass` (the strongest confirmed head; the key is
   omitted when none is confirmed) and the criteria read it. No threshold
   moved.

2. **A missing head was a verdict, not a missing measurement.** Criteria
   1–2 are head-dependent, so with no confirmed head there is nothing to
   measure. They are now `NOT MEASURED`, like criteria 6–7; the run can
   still fail the behavioural criteria 3–5, but it cannot fail a causal
   criterion it never measured. `exp1` no longer writes a fabricated
   `confirmed_content_mass`.

3. **The cascade could analyse a different model.** exp1's rolling
   checkpoint carried only weights, optimizer state and epoch: not the
   model seed, not the task, not the commit. exp4 could load
   `checkpoint_seed1.pt` for seed 0, a stale epoch, or weights trained by
   another commit, and exp5 could train its SAE on a different model's
   activations. Checkpoints now record `git_sha`, `git_dirty`, `seed` and
   `task`; exp4 checks the architecture, seed, task, final epoch and
   commit (`--source-epochs`, `--source-git-sha`) and exp5 takes
   `--source-model-seed`; both manifests record the loaded checkpoint in
   `source_provenance`, and the verdict refuses a cascade that fails any
   check.

4. **A dead session lost the seeds it had finished, and the verdict was
   never saved.** The multi-seed manifest was written only after the last
   seed; a disconnect at seed 2 discarded seeds 0 and 1. Each seed now
   writes a complete per-seed recovery manifest, `merge_manifests.py`
   rebuilds the aggregate (refusing mixed configs, commits, environments
   or seed sets), the GPU session saves `results/content_verdict.json`
   next to the manifests, and `pin_remote_run.py --only` names the records
   so the recovery files and the verdict are not installed as evidence.

**What it changes, measured before the GPU run.** The seven criteria and
their thresholds are untouched. The mechanism report now names a
distributed content circuit when it measured one — group ablation, content
mass, single-head drop, and exp4's group path-patch effect — and labels it
a **secondary finding**. A NEGATIVE stays NEGATIVE; the report explains
the mechanism the per-head rule did not confirm. The pre-registration's
2026-11-01 addendum records all of this, and the standard-geometry
de-risk's shape is written there **before** the GPU run.

<!-- manifest: results/induction_content_derisk_standard.json -->

**What it does not change.** No criterion, threshold or decision rule. No
number is re-tuned after seeing the de-risk data, and the headline is not
rewritten from "a head" to "a circuit": the repository reports that no
single head passed the frozen per-head criteria and that the behaviour was
carried by a group.

## 2026-10-25 — The content-task instrument cannot measure its own question: wrong chance level, invalid shares, an empty candidate group, and a missing standard-geometry de-risk

The ninth audit, and the one that reaches furthest forward again: it is about
the experiment that is supposed to **close** Rung 1's open question, and it
found that the instrument as shipped would have produced a vacuous mechanism
report on the very case it exists to measure — a distributed copy.

**What was broken.** Six things, each independent of the others:

1. **The chance level used the wrong position.** `chance_content_mass`
   divided by `key + 1` instead of `q + 1`: the uniform mass at query `q` is
   spread over the `q + 1` positions the causal mask allows, not over
   `key + 1`. The old formula overstated the bar, so on the quick geometry
   the candidate screen selected zero heads (`n_candidate_heads = 0`), and
   the group ablation was a no-op. The addendum's reading
   "the candidates are not the carriers" is retracted — there were no
   candidates. Fixed in `src/experiments/copy_circuit.py`; the old manifest
   (`results/induction_content_derisk.json`) is kept as evidence of the bug.

2. **Attribution shares could exceed 1.** `dla_positive_share` and
   `dla_top_head_share` divided by the signed total, so they could exceed
   1 (observed 1.0698 on the de-risk manifest). They now divide by
   `sum(|v|)` and stay in `[0, 1]`.

3. **No aggregate measurement before the fix.** The de-risk had no
   `content_mass_excess`, `content_mass_ratio`, or group-concentration
   numbers — the sum over heads (0.695) looked meaningless without a chance
   baseline. Added to `mass_summary`.

4. **An empty candidate group is not "no circuit."** `classify_mechanism`
   now returns `undetermined — no candidate passed the 3x chance screen`
   when `n_candidate_heads == 0`, instead of falling through to "none".

5. **Fabricated zeros for unmeasured causal effects.** `exp4_circuit_patching`
   wrote `0.0` for `mean_path_patch_effect` when no head was confirmed — a
   causal measurement that was never taken. `exp1_induction_heads` did the
   same for `mean_copy_ablation_drop` when the confirmed set was empty, which
   made criterion 6 fail by fabrication. Both keys are now omitted and the
   verdict reports `NOT MEASURED`.

6. **The standard-geometry CPU de-risk was missing.** `results/induction_content_derisk_standard.json`
   did not exist; the prior 600-epoch attempt was killed at epoch 30. The run
   was re-added as `make reproduce-induction-content-derisk-standard` and has
   now completed (0.706 h, clean tree): the corrected screen selects **3
   candidate heads**, the group ablation removes **0.9956** of the copy
   accuracy, the largest single-head drop is **0.0986** (distributed), the
   dissociation probe says content (0.9129 vs 0.1793), and the DLA positive
   share is 1.0. The per-head *confirmed* count is 0 because K-composition is
   0.0918, below 0.40 — the model's circuit is distributed, not the single-head
   K-composition pattern the per-head rule looks for. That is recorded before
   the GPU run, not after it.

**What it changes, measured before the GPU run.** The instrument now has a
correct chance level, valid shares, an explicit empty-group semantics, an
exploratory mass-covering group (top 80% of content mass), and no fabricated
zeros. The pre-registration's addendum (c), dated 2026-10-25, records all of
this with both new manifests. At the GPU geometry the corrected instrument
finds the distributed circuit it was built for: three candidate heads, group
ablation 0.9956, largest single-head drop 0.0986, DLA positive share 1.0. The
seven criteria and their thresholds are untouched, and the mechanism report
remains **secondary**.

<!-- manifest: results/induction_content_derisk_fixed.json -->
<!-- manifest: results/induction_content_derisk_standard.json -->

**What it does not change.** The seven criteria, their thresholds and the
decision rule are untouched. No number is re-tuned after seeing the de-risk
data.

## 2026-10-22 — The content-task run could not have produced a verdict: a `KeyError`, a gate with no manifest, and a probe that contradicted the addendum

The eighth audit, and the one that reaches furthest forward: it is about the
experiment that is supposed to **close** Rung 1's open question, and it found
that the experiment as written would have spent a GPU session and then died
before it could say anything.

**What was broken.** Six things, each of them independent of the others:

1. **The verdict cell could not compute the verdict.** The seven criteria lived
   in a notebook cell, and criterion 7 (`mean_path_patch_effect`) was read out
   of the **exp1** manifest — a metric only the **exp4** manifest carries. The
   cell raised `KeyError` on the first seed. The cell that printed the cascade's
   numbers had the same bug: it read `mean_ablation_effect`,
   `mean_path_patch_effect`, `mean_activation_recovery` and `checkpoint_epoch`
   out of the exp1 manifest. Step 2b was the last cell before the download, so
   the session's artifacts would have been lost with the crash.
2. **The CPU gate had no evidence.** The gate's third item — "the end-to-end run
   completes and writes a manifest with the new fields" — was not backed: both
   de-risk runs were launched without `--save-manifest` (`'save_manifest': False,
   'manifest_path': None` in both logs), no `results/*content*.json` exists, and
   the two logs are gitignored. The numbers the addendum quotes (0.5288, 0.4521,
   0.146, 0.183) were not traceable from a clone — the 2026-10-11 failure mode
   again, on the note that was written to prevent it.
3. **The addendum omitted the measurement that contradicted it.** The same
   de-risk run printed `content mass 0.122 vs positional mass 0.253 ->
   POSITIONAL copy`. The addendum reported the *behaviour* (copy accuracy 0.53
   against a 0.21 fixed-offset ceiling) and did not report the probe. Both are
   true and they are not the same kind of statement — the behaviour is the
   model's answer, the probe is a per-head attention maximum — but the omission
   hid the exact tension the run has to resolve.
4. **The per-head screen cannot see a distributed circuit.** The de-risk's best
   head held 0.146 of the content mass against a 0.30 screen, with 0/8 heads
   confirmed, *while the model copied by content*. A copy spread over k heads
   puts ~1/k of the mass in each head: every one of them falls below the screen
   while the sum does not. There was no aggregate measurement, no group
   ablation and no attribution in the repository — the addendum itself said the
   distribution over the heads was "the first thing to measure", and nothing
   measured it.
5. **The emergence run could have cost twice the budget.** `--stop-rule
   mechanism` waits for a head *above* the first layer, and the periodic task's
   whole circuit was in layer 0 — so the rule had a good chance of never
   firing, silently turning the emergence run into a second full-budget run.
6. **The vocabulary answered a constraint this task does not have.** The
   periodic task needs 2048 because its prefix is sampled *with replacement*;
   the content task's key is sampled *without* replacement, and 44 distinct
   tokens suffice. The standard-geometry CPU probe was still at the *uniform*
   prediction after 400 epochs at 2048 (train loss 7.6246 against
   ln(2048) = 7.6246), while the quick geometry at **vocab 256** had reached a
   copy accuracy of 0.53.

**What it invalidates.** Nothing that has been published — the content task
has not run yet. What it invalidates is the *plan*: the pre-registration's
addendum of 2026-10-22 (a) claimed a manifest that does not exist, (b) omitted
the probe's contrary verdict, and (c) left the GPU run with a verdict code that
could not execute and a stop rule that could not fire.

**What it changed, measured before the GPU run.** The instrument is now
testable, and the protocol is amended in the pre-registration's second
addendum — *before* the run, with the seven criteria untouched:

- `src/experiments/content_verdict.py` holds the seven frozen criteria, joins
  the exp1 and exp4 manifests per seed, and never guesses: a criterion whose
  measurement is missing is reported missing, and a run whose manifest does not
  carry the measurement gets the status `INCOMPLETE` and **no verdict** — "the
  model has no content-based induction head" and "this manifest never measured
  one" are different statements.
- `src/experiments/copy_circuit.py` adds the circuit-level measurement: the
  aggregate content mass and its concentration, the **group ablation** next to
  the single-head ablations, and the first-order **logit attribution** of every
  head to the content-vs-position contrast. The candidate group is fixed by a
  rule that reads the data and the attention masses and never the outcome.
- The cascade's counterfactual is a **minimal pair** (one token changed, in the
  same sequence) instead of a different sequence, and the cascade now runs when
  the *behaviour* is content-based — not only when a per-head detector fires.
- The content task's standard config is a pinned preset (`--content-standard`)
  with the vocabulary amended to 256. The 2026-10-25 addendum removed the
  separate emergence run: the full run records `confirmed_epoch`, so the
  early-stopped run added no measurement the verdict uses.
- The notebook's artifacts are zipped **before** the verdict, and the verdict
  cell is the last one: a verdict that crashes must not cost the session.

**What it does not change.** The seven criteria, their thresholds and the
decision rule are untouched, and the mechanism report is explicitly
**secondary**: it describes the circuit, it does not decide the verdict. The
periodic task's numbers, the Rung 2/3/5 results and the 2026-10-19 audit's
verdicts are untouched — this audit is about the instrument of the *next* run.

## 2026-10-19 — The induction detector measured the *previous-token* head: every "0 / N heads" was a statement about the detector

The seventh audit, and the one that reaches furthest back: it invalidates the
head counts this repository has published since 2026-08-02 — not by finding them
wrong, but by finding that **the thing that measured them measured a different
circuit**.

**What was broken.** Two detectors, both wrong, in different ways:

- `exp1_induction_heads.analyze_induction_heads` and
  `compute_attention_entropy` measured the attention mass on the offset
  `q → q-1` — the **previous token** — and called it "diag+1". On this task's
  `prefix + prefix` layout the induction (copy) offset is `q → q-L+1`, where
  `L` is the prefix length: at a second-copy query `q`, the token `x[q]` has
  its previous occurrence at `q-L`, and the token to copy sits one position
  later. A head that attends to `q-1` is a different circuit, and it does not
  copy the repeated token at all.
- `exp4_circuit_patching.detect_induction_heads` measured
  `attn_probs.diagonal(offset=1)` — the strict upper triangle of a *causal*
  softmax, which is identically zero. That detector could never fire, on any
  model, at any scale.

**Why it survived a year of audits.** The planted tests planted the same wrong
pattern: `_planted_patterns` put the mass on `q-1` and asserted it was
detected. A test that encodes the bug passes the bug — and the "0 / 8 heads"
headline it protected was, all along, the detector's verdict.

**What it invalidates.** Every head count this repository has published —
"0 / 8" at Rung 1 (2 layers × 4 heads), "0 / 4" at Rung 4 (2 layers × 2
heads, three seeds) — is retracted as *uninterpretable*: it is a statement
about the detector, not about the model. The numbers are not "wrong" in the
direction they point (no head was confirmed, and the planted tests still show
the previous-token head is not an induction head); they are simply not
measurements of induction.

**What it changed, measured the next day.** The corrected detector on the
standard-scale GPU run (2026-10-20) finds **2–3 heads per seed** with a
copy-offset mass of **0.95** — so the retracted "0 / 8" really was a detector
artifact, and the model *does* form a copy head within 50 epochs. The causal
interventions land too: ablating the confirmed head costs **0.44** of the
logit difference and path patching attributes **0.82** of its direct effect
on the logits to that head. What the probe adds is the *mechanism*: the copy
follows the fixed offset, not the previous occurrence of the same token, and
the K-composition between layers is 0.05 — so this is a single-head
**prefix-copying** circuit, not the two-step induction circuit. The full
numbers are in the Rung 1 and Rung 4 sections; the decision is ADR-0032.

**What replaced it.** One detector, shared by Rungs 1, 4 and 5
(`src/experiments/induction_detection.py`):

- the **induction mass** on the copy offset `q-(L-1)`, averaged over the
  *collision-free* queries only (those whose nearest previous occurrence is
  exactly `q-L`), so the ambiguous positions in a prefix that contains a
  repeated token neither dilute nor inflate it;
- the **previous-token mass** on `q-1`, kept as an explicitly labelled
  control — the number the old detector called "diag+1";
- the **duplicate mass** on `q-L` (Nanda's Step 1) and the **content mass**
  on `prev(q)+1`;
- **confirmation** requires the mechanism, not just the mass: a head counts
  only when its layer is composed with an earlier layer at a K-composition
  score ≥ 0.4 (the first layer has no earlier layer and is confirmed on the
  mass alone, and the report says so).

The planted tests were rebuilt around the *task layout*: the copy offset must
fire; the previous-token offset, the duplicate offset, an off-by-one, uniform
attention and self-attention must not. The same constructions are repeated at
the weights level, on a real model.

**The caveat that the fix exposes.** On `prefix + prefix` the previous
occurrence of the current token is *always* at `q-L`, so a circuit that
copies by content and a circuit that copies by a fixed offset are the same
function on this task — no in-distribution measurement can separate them, and
the K-composition score cannot either (it reads the previous occurrence from
a layer-0 head's argmax, which on a periodic task is the same position). The
new **dissociation probe** does separate them: it feeds a batch whose second
half is a *permuted* copy of the prefix, where the content target and the
fixed offset point at different keys. Until that probe has run on a given
checkpoint, the honest wording for a detected head is *"prefix-copying head
at offset L-1"*, not *"induction head"*.

**What it does not change.** Rung 2 (grokking), Rung 3 (superposition) and
Rung 5's synthetic SAE baseline are untouched — none of them depends on the
induction detector. The fixed-vs-fresh-batches comparison (53.5% vs 0.45%)
survives: it is an accuracy measurement, not a head count. What is retracted
is only the *head-count annotation* on both arms.

**The cascade, finally one model.** Rung 4 used to train its *own*
decoder-only model while claiming to match exp1's attention-only config, with
a batch size of 64 against exp1's 128 — so the two "matched" runs took 384k
and 192k optimizer steps respectively over the same data, and the parity test
only compared the flags both presets happened to set. `exp4 --from-checkpoint`
now loads exp1's checkpoint and analyses *that* model; the parity test covers
the batch size and the step count, and the interventions (activation
patching, head ablation, path patching) run unchanged on either model family.

## 2026-10-14 — The NO-GROK verdict was the metric's fault: the sparse circuit was there all along

The 2026-10-08 audit predicted exactly this: an L1-mass `k_99` calls a clean
sparse embedding dense because noise spreads over every bin. The re-run it asked
for (`notebooks/kaggle_grokking_p113.ipynb`, run on a free Kaggle GPU 2026-10-14)
confirms the prediction on real embeddings:

| Run | Protocol | val accuracy | k_energy_90 (of 56) | energy_sparse | L1 k_99 (the old reader) |
|-----|----------|--------------|---------------------|---------------|--------------------------|
| Job A | Nanda-faithful, 40k full-batch steps × 3 seeds | 0.9999 ± 0.0002 | **5.7 ± 1.2** | **3/3 seeds sparse** | 109–110 / 113 |
| Job B | the historical repo protocol, re-run × 3 seeds | 1.0000 ± 0.0000 | **8.7 ± 1.2** | **3/3 seeds sparse** | 110 / 113 |

The model solved modular addition **with** the sparse Fourier circuit in both
protocols; the 2026-08-11 NO-GROK verdict read the same embeddings through the
falsified classifier. The training, the split fix, the checkpoint machinery and
the multi-seed manifests were all correct — only the reading was wrong.

**What this changes**: the primary flagship is REPRODUCED, not a negative. ADR-0003
row 1's NO-GROK stamp is retracted; the Phase 7 capstone gate flips from the
honest-negative answer to the positive one (as that note's own supersession
clause required); issue #167 closes; the protocol-ablation phase diagram (#168)
unblocks from the Nanda-faithful setup. The P=59 positive control (2026-09-27)
carried the same metric defect and was re-measured on 2026-10-19 (issue #196):
**2 of 3 seeds sparse** — a MIXED verdict, not the "sparse" label the first
reading carried. See Rung 2 below for the per-seed numbers.

**What this does not change**: the frequency ablation (keep 59/59 → 0.0000) and
the generalization-epoch progress measures remain valid evidence; the figures
generated from the seed-0 CPU checkpoint remain valid visualizations, and were
regenerated 2026-10-17 from the P=113 seed-0 GPU checkpoint of job A with their
captions corrected to the sparse (energy) reading (`portfolio/figures/exp2_grokking_curve.png`,
`portfolio/figures/exp2_fourier_weights.png`, `portfolio/figures/exp2_frequency_ablation.png`,
`portfolio/figures/exp2_progress_measures.png`;
re-analysis provenance `results/grokking_p113_gpu_reanalysis.json`).

## 2026-10-11 — Integrity pass: the one solid finding had no manifest behind it

The repo's own headline called the fixed-vs-fresh-batches comparison "the one solid
finding" and quoted **0.05% vs 52.2%** validation accuracy. That number appeared in nine
documents — README, this ledger, the LaTeX paper, the premiere ledger, three premiere
channels, and the induction-heads note — and **no manifest in `results/` contained it**.
`make verify-claims` reported 0 problems, because the checker only verifies numbers that
carry a manifest tag, and this one never had one.

Re-run for real, 3 seeds per arm, identical config, batch regime the only difference
(`make reproduce-induction-batches`):

<!-- manifest: results/exp1_induction_fixed_batches.json -->
<!-- manifest: results/exp1_induction_fresh_batches.json -->

| | Fixed | Fresh |
|---|---|---|
| Was claimed (prose only — no tracked manifest, and never had one) | 0.05% | 52.2% |
| Actually measured | **0.45% ± 0.03%** | **53.53% ± 0.03%** |

Same conclusion — two orders of magnitude in the same direction — but different numbers,
and the claimed config (`vocab_size=2048, seq_len=24, d_model=32, num_train=1024`) was not
the config that produced them either. The corrected values, the real config, and the
manifest tags are now in Rung 1 above, in
`results/exp1_induction_{fixed,fresh}_batches.json`.

**This is the fifth audit and the first one that found a *good* claim was unbacked rather
than a bad claim being wrong.** The distinction matters: the previous four found numbers
that were wrong. This one found the repository's strongest number had no evidence at all,
which is a different failure — it would have survived any number of correctness checks,
because nothing was checking it.

**Also found the same day.** `verify_claims()` globbed `results/*.json` and checked every
file, including untracked scratch. Running `--quick` (a reduced smoke config, which is
necessarily recorded against a dirty tree) failed the whole checker for a file no document
cites. It now checks only git-tracked manifests; the contract for tracked files is
unchanged.

**Fixes**: both arms are now runnable and re-runnable
(`make reproduce-induction-batches`), every public number carries a manifest tag, and
`verify_claims()` gained three rules that would have caught this class of bug on day one —
see `src/results.py` and `tests/test_verify_claims_scope.py`.

## 2026-10-08 — Integrity pass: a paper section written ahead of its data

`verify-claims` reported 0 problems while `portfolio/paper/` contained a phase-diagram
section with claims that no manifest backed. Root cause: the checker only read RESULTS.md
and only tested that a tagged path *existed*. Found by reading the paper, not by running it:

- `grokking_phase_diagram_section.tex` asserted "sparse at P=11, 17, 29", a fitted boundary
  `C≈60` and a model-size sweep; the only manifest behind it
  (`portfolio/phase_diagram_manifest.json`) was a 100-epoch test run with
  `aggregate: {}` and validation accuracy ≈ 0.004.
- `main.tex` tagged `results/phase_diagram_*.pt` (gitignored, not even JSON) and included
  figures from `../../figures/` (gitignored), so the paper could not be built from a clone.
  Its `<!-- manifest -->` tags were HTML comments inside LaTeX (typeset as text), and one
  figure was closed with an HTML `</figure>`.

**Rung 2's Fourier metric (found the same day).** `analyze_fourier_sparsity` takes `k_99` as the
number of frequencies holding 99% of the *L1* mass. L1 mass is dominated by noise spread over every
bin, so a clean 5-frequency embedding with 1% additive noise is called dense
(`tests/test_grokking.py::TestFourierEnergySparsity` pins this); `k_99 = 111/113` therefore could
not tell a sparse circuit from a dense one. The protocol also differs from Nanda et al. in five ways
(minibatches, gradient clipping, per-step embedding renormalization, LayerNorm, default Adam betas),
and `run_single_seed` silently ignored `--no-normalize-embeddings` and `--schedule`. Small-modulus
cells were also untrained: the budget was counted in epochs, and at P=29 an epoch is 2 steps. The
P=113 checkpoints no longer exist, so the verdict is re-run, not re-analysed: `--protocol nanda`
plus the new `fourier_energy_sparsity`, jobs in `notebooks/kaggle_grokking_p113.ipynb` (GPU; ~0.6
s/step on the author's CPU). Until it lands, Rung 2 carries no dense/sparse claim.

**Fixes**: `verify_claims` now also checks the `.tex` sources; a manifest tag must resolve to
a git-tracked `.json` with a non-empty aggregate; every `\includegraphics` target must exist
and be tracked; LaTeX tags use `% manifest: …`. All falsified by tests that fail on the old
code (`tests/test_results.py::TestVerifyClaimsPaperAndManifestQuality`). The unsupported
section, its 3 figures and the test manifest were deleted rather than caveated, as with
Rung 6 ACDC on 2026-08-01.

## 2026-08-02 — Micro-Phase 8, the Evidence Pass: correct-but-unmeasured code gets measured

The 2026-08-01 Validity Pass fixed *what the code measures*. It left the repository
correct and almost entirely **unmeasured**: Rung 2 had never run, Rungs 1 and 4 had no
post-fix standard-scale numbers, Rung 3 had never reproduced, Rung 5 was real only on
synthetic data. This pass built a multi-seed provenance harness
(`src/experiments/runner.py`, `src/results.py`, `make verify-claims` —
[results-manifests-and-provenance](../06_production_ai/notes/results-manifests-and-provenance.md)) and pointed it at every rung
that fits this machine's CPU budget. What it found:

- **Rung 3's root cause, finally found.** The 2026-07-26 and 2026-08-01 audits both
  observed flat, near-zero "feature recovery" and could not explain it (the 2026-08-01
  tied-weights fix was a real correctness fix that changed nothing measurable). The
  architecture had no actual bottleneck — the dataset pre-compressed features before the
  model ever saw them, so the model was expanding an already-solved problem, not
  compressing anything. Rewritten to the canonical Elhage et al. setup (real
  `n_dimensions < n_features` bottleneck, decoder bias, ground-truth-free metrics); the
  phase transition now reproduces cleanly and immediately: **10/20 → 20/20 features
  represented as sparsity drops from 0.5 to 0.01.** See
  [superposition-setup-validity](../05_llm_engineering/proofs/superposition-setup-validity.md) for the full reconstruction
  with the diagnostic numbers that found it, and
  [ex-01-falsify-your-own-metric](../06_production_ai/exercises/ex-01-falsify-your-own-metric.md) for why the *old* metric
  couldn't have told the difference between broken and working even if the architecture
  had been right.
- **Rung 1's task design was ill-posed for its entire history.** The repeated-token
  generator's prefix needs no repeated tokens (else "the previous occurrence of the current
  token" is ambiguous). The pre-existing `vocab_size=32`/prefix-length-32 default gave a
  **>99.99%** chance of a repeated token in the prefix — a birthday-problem calculation, not
  a guess (`prefix_duplicate_probability()`,
  [ex-03-induction-task-design](../06_production_ai/exercises/ex-03-induction-task-design.md)). Fixed (`vocab_size=2048`
  standard / `256` quick, ~20-23% collision). Fixing it alone did **not** produce induction
  heads at quick scale (`diag1_mass` peaked at 0.125, still below the 0.3 threshold) — a
  second, independent question this pass also built the tooling to test.
- **The fixed-dataset memorization hypothesis: confirmed, and it's large.** A matched
  800-epoch comparison (identical config, only `--fresh-batches` toggled) found the fixed,
  reused-every-epoch dataset causes catastrophic overfitting — val accuracy decays to
  **0.45%** (below random chance) while val loss climbs to 24.3 — versus fresh, resampled
  batches stabilizing at **53.5%** val accuracy with no train/val gap at all. Neither
  condition crossed the induction-head detection threshold within this (still sub-standard)
  budget, but the fresh-batches trajectory was still improving at epoch 800 while the fixed
  condition was actively regressing. See
  [induction-heads](../04_nlp_and_transformers/notes/induction-heads.md) for the full table.
- **SAE on real activations, for the first time.** `exp5_sae_dashboard.py --activations-from`
  now harvests genuine residual-stream activations from a trained induction-heads
  checkpoint via a forward hook on `ln_final`, instead of only ever training on
  `ActivationGenerator`'s synthetic baseline. Added the pre-encoder bias (`x - b_dec`,
  Bricken et al.'s actual architecture — the prior SAE had no `b_dec` at all). First real
  run: **99.97% FVE, L0 = 136/256 (53% of the dictionary active), 0% dead features** —
  reconstructs *better* than the synthetic baseline (97.2% FVE) but far less sparsely (53%
  active vs. 17.4%). Read honestly, not as an unqualified win: this is more consistent with
  a small, undertrained 32-dimensional residual stream being easy to reconstruct densely
  than with the SAE finding genuinely sparse, interpretable features — see Rung 5 below.
  **Smoke check (2026-10-03)**: `scripts/verify_sae_induction.py` on a local SAE saw max
  activation ~8.1 and L0 ~250/512 (~49% active). This is not evidence of induction features;
  it is consistent with the dense-reconstruction reading above. See
  [execution log](../07_capstone/execution-log.md).
- **Also this pass**: fixed a CI/local dev mismatch where `python-version: '3.11'` was
  pinned in `.github/workflows/python-ci.yml` while `uv.lock` and `[tool.mypy]` both target
  3.12 — the same class of silent mismatch that hid mypy crashing on numpy's stubs for an
  unknown period before 2026-08-01. The non-blocking mypy step now distinguishes "reported
  errors" (exit 1, fine) from "mypy itself crashed" (exit 2, now fails the build) instead of
  swallowing both with `|| true`. Added a small, honestly-scoped blocking mypy allowlist
  (`src/results.py`, `src/experiments/runner.py` — the only two candidate modules that
  turned out to actually be clean; `src/reproducibility.py` and `src/models/` were checked
  and are not). `portfolio/paper/` LaTeX scaffold added (structure only — no prose; see its
  own `main.tex` for what's still a `% TODO`).
- **Not done this pass, tracked as the next blocker**: the P=113 grokking flagship still
  has not run — `exp2_grokking.py` now has `--seeds` and
  `notebooks/colab_grokking_full_run.ipynb` is hardened for a 3-seed Colab run, but the run
  itself needs a GPU this environment doesn't have. This is still the single most important
  open item in the repository.

## 2026-08-01 — Validity Pass: three causal claims were measuring the wrong thing

A code-level audit (not a re-run — a *reading* of what each intervention actually touches)
found that Rungs 1 and 4's causal claims rested on interventions that didn't do what their
names said:

| # | What was wrong | Where | What it actually did |
|---|---|---|---|
| 1 | Ablation zeroed a post-mixing tensor | `exp1_induction_heads.py`, `causal_ablation()` | Hooked `W_O`'s *output* — already mixed across every head — and zeroed an `n_heads`-way slice of it. That zeroes an arbitrary residual-stream subspace, not a head. |
| 2 | Patch never reached the residual stream | `exp4_circuit_patching.py`, `run_activation_patching()` | Hooked the MLP's *input* (a normalized copy of resid_mid). The residual skip two lines later re-reads the block's own unpatched `x` — the patch changed the MLP branch's output but nothing that survives to the next layer. |
| 3 | Metric measured confidence, not correctness | same function | `top1 − top2` on the model's own logits. A model confidently wrong scores identically to a model confidently right. |
| 4 | A plotted metric was on the wrong scale | `exp1_induction_heads.py`, `compute_attention_entropy()` | `diag1_mass` summed per-head signal across heads instead of taking the max — a `[0, n_heads]`-scale number plotted against a per-head `0.3` threshold. Root cause of the 2026-07-26 "mass ≈ 1.0 but 0 heads detected" discrepancy: never the same unit. |

**Fixes applied**, all with falsification tests that would have failed against the old code
(see [intervention-validity](../05_llm_engineering/proofs/intervention-validity.md) for the full reconstruction):
- `causal_ablation()` now uses a `head_mask` applied *before* `W_O`, matching the approach
  `exp4_circuit_patching.py` already had right for its own head ablation. Falsified with:
  ablating every head in every block must reproduce the model's no-attention baseline
  *exactly* — `tests/test_induction_heads.py::test_ablating_all_heads_collapses_to_no_attention_baseline`.
- `run_activation_patching()` now hooks the block's `attn` module directly (its output is
  already post-`W_O`, the exact tensor added to `resid_pre`), and defines
  `logit_diff = logits[answer] − logits[counterfactual]` against real task labels instead
  of `top1 − top2`. Falsified with: patching a run against *itself* must be an exact no-op
  — `tests/test_exp4_circuit_patching.py::TestActivationPatching::test_self_patching_is_a_no_op`.
- **Path patching was added** (`run_path_patching_to_logits()`) — it had a note
  (`04_nlp_and_transformers/notes/path-patching.md`) and a commit scope but no
  implementation anywhere in `src/` before this pass. It isolates a single head's *direct*
  effect on the logits by decomposing `attn_out` through `W_O`'s per-head column blocks,
  distinct from activation patching's inclusion of effects mediated through later layers.
- `diag1_mass` now takes the max over heads (and over layers), making it comparable to the
  0.3 per-head threshold it's plotted against.

**Also this pass:**
- **Rung 6 deleted, not fixed.** `exp6_automated_circuit.py` plotted `rng.poisson`/`rng.beta`/`rng.exponential`
  draws labeled "Faithfulness" and "Time to Discovery." Labeled a placeholder in logs, but
  fabricated numbers next to real results in a portfolio repo are a liability even when
  labeled. Revisit only with a real ACDC implementation.
- **RoPE convention fixed.** `cos`/`sin` were built with `repeat_interleave(2)` (interleaved-pairs
  convention) but rotated with a `chunk(2)`-based `_rotate_half` (half-split convention) — two
  incompatible layouts. Every position still got a distinct signal (so training didn't
  obviously break), but the relative-position property RoPE exists for — that the attention
  score between positions *i* and *j* depends only on *i − j* — did not hold. Fixed and now
  covered by `tests/test_decoder_only_transformer.py::test_relative_position_invariance`.
- **Superposition (Rung 3) weights are now tied** (`decoder.weight == encoder.weight.T`,
  the canonical Elhage et al. setup) instead of two independently-learned matrices. This
  was a real correctness fix — but a single-point empirical check (sparsity=0.01, quick
  mode) shows it **did not change** the flat/near-zero recovery the 2026-07-26 audit found
  (0.100 before, 0.100 after). My hypothesis that untied weights explained the
  discrepancy is **not supported**. The real root cause of Rung 3's non-reproduction is
  still open.
- **SAE dead-feature threshold fixed.** Was `1/(10·n_features)` — a threshold that got
  *looser* as the dictionary grew (backwards). Now a fixed `1e-4`, independent of
  dictionary size; `never_fires` (a stricter, unambiguous "dead") is also reported.
- **Unused MI tooling dependencies dropped**: `transformer-lens`, `sae-lens`, `circuitsvis`,
  `einops`, `seaborn`, `datasets`, `accelerate` were all pinned in `pyproject.toml` and
  never imported anywhere in `src/`. Removing them dropped ~100 transitive packages from
  `uv.lock`. The one prior reference (`transformer_lens.utils.reset_hooks()` in
  `src/reproducibility.py`) wasn't a real TransformerLens function and silently no-op'd.
- **`mypy`'s `python_version` was mismatched with the actual resolved interpreter**
  (config said 3.11, `uv.lock` resolves 3.12), which made mypy crash on numpy's stub files
  *before checking a single line of `src/`*. CI's `mypy ... || true` silently swallowed
  this, so the "54 pre-existing errors" comment that lived in `python-ci.yml` was never
  actually observed — mypy hadn't gotten far enough to produce it. Fixed the version
  mismatch; real strict-mode count is 154 errors (mostly missing generic type args, not
  caught bugs), left as tracked follow-up rather than rushed through in this pass.
- **Import-time filesystem side effect removed.** `import src` used to create a `figures/`
  directory as a side effect (each experiment module ran `FIGURES_DIR.mkdir()` at module
  scope). Moved into each `main()`.

## 2026-07-26 — Reproducibility Audit: Real Bug Found, Claims Reconciled to Evidence

`figures/` did not exist prior to this audit despite being referenced throughout this
document and `00_meta/00_home.md`. This session installed the minimal runtime deps
(torch-cpu, numpy, matplotlib, tqdm) and ran every rung's `--quick` mode on CPU to generate
real figures and cross-check the numbers already documented. Findings:

- **Grokking (Rung 2): found and fixed a real bug**, not just a compute bottleneck.
  `make_modular_addition_data` split train/val by **target class** (`(a+b) % P`) instead
  of by **equation** `(a, b)`. This left some output classes with zero training signal —
  the model was asked to predict classes its unembedding row never saw, which is not
  generalization, it's an unsolvable task. Produced exactly 0% validation accuracy even at
  trivial P=11 with no compute constraint, independent of the CPU/GPU bottleneck
  previously blamed. Fixed to hold out random `(a, b)` pairs, matching the canonical
  Power et al. / Nanda et al. setup where every target class appears in both splits.
- **Induction heads (Rungs 1 & 4): quick-mode detected 0 heads** despite diagonal+1
  attention mass reported near 1.0 — root-caused in the 2026-08-01 pass above (a metric
  scale bug, not a detection failure or a real absence of heads at standard scale).
- **Superposition (Rung 3): no phase transition observed** in a reduced sweep — flagged,
  partially investigated 2026-08-01 (see above), still open.
- **SAE (Rung 5): reproduced exactly** (97.2% FVE) on synthetic data.
- **ACDC (Rung 6): confirmed simulated/placeholder**, exactly as labeled — deleted 2026-08-01.
