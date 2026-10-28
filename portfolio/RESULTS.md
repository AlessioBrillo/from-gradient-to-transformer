---
tags: [portfolio, results]
---

# Results — Headline Findings

> **Thesis**: I build a decoder-only transformer from scratch, then reverse-engineer the algorithms it learns — grokking modular addition with Fourier decomposition, induction heads, circuit verification via activation and path patching, and sparse autoencoder feature extraction.

All experiments are implemented in `src/experiments/`. Each has a `--quick` mode for fast
smoke tests (`make reproduce-quick`) and a full-scale mode (`make reproduce`).

---

## Honesty Ledger

Nine audits have now caught real problems in this repository's causal claims and
evidence base. Seven found claims that were wrong or unbacked; the eighth found a
claim that was **right and had been called wrong by its own metric**; the ninth
found that the experiment which was supposed to close the last open question
**could not have produced a verdict at all** — and fixed the instrument before
the run. All entries stay here — the point of this section is to make it easy to
see the trend (are correctness problems getting caught faster, or accumulating?),
not to keep only the latest one.

### 2026-10-22 — The content-task run could not have produced a verdict: a `KeyError`, a gate with no manifest, and a probe that contradicted the addendum

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

### 2026-10-25 — The content-task instrument cannot measure its own question: wrong chance level, invalid shares, an empty candidate group, and a missing standard-geometry de-risk

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

**What it does not change.** The seven criteria, their thresholds and the
decision rule are untouched. No number is re-tuned after seeing the de-risk
data.

### 2026-10-19 — The induction detector measured the *previous-token* head: every "0 / N heads" was a statement about the detector

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

### 2026-10-14 — The NO-GROK verdict was the metric's fault: the sparse circuit was there all along

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

### 2026-10-11 — Integrity pass: the one solid finding had no manifest behind it

The repo's own headline called the fixed-vs-fresh-batches comparison "the one solid
finding" and quoted **0.05% vs 52.2%** validation accuracy. That number appeared in nine
documents — README, this ledger, the LaTeX paper, the premiere ledger, three premiere
channels, and the induction-heads note — and **no manifest in `results/` contained it**.
`make verify-claims` reported 0 problems, because the checker only verifies numbers that
carry a manifest tag, and this one never had one.

Re-run for real, 3 seeds per arm, identical config, batch regime the only difference
(`make reproduce-induction-batches`):

| | Fixed | Fresh |
|---|---|---|
| Was claimed (prose only) | 0.05% | 52.2% |
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

### 2026-10-08 — Integrity pass: a paper section written ahead of its data

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

### 2026-08-02 — Micro-Phase 8, the Evidence Pass: correct-but-unmeasured code gets measured

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

### 2026-08-01 — Validity Pass: three causal claims were measuring the wrong thing

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

### 2026-07-26 — Reproducibility Audit: Real Bug Found, Claims Reconciled to Evidence

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

---

## Rung 1 — Prefix-Copying Heads (Fallback Flagship — the detector was wrong; a head does form, and it is positional)

<!-- manifest: results/exp1_induction_heads.json -->

**Question**: Do induction heads emerge in a 2-layer attention-only transformer trained on repeated tokens? Can we detect, verify, and ablate them causally?

**Status**: [x] **A head forms at standard scale — and it is a *prefix-copying* head, not an induction head.** The detector that reported "0 / N heads" was measuring the previous-token offset (see the Honesty Ledger's 2026-10-19 entry); with the corrected detector the standard-scale run confirms **2–3 heads per seed** with a copy-offset mass of **0.95**, and the causal interventions land: ablating the confirmed head costs **44%** of the logit difference and path patching attributes **82%** of its direct effect on the logits to that head. But the **dissociation probe** shows the copy follows the *fixed offset* (`q-(L-1)`), not the previous occurrence of the same token (period mass 0.70 vs content mass 0.03, 3/3 seeds), and the K-composition between layers stays at **0.05** — so there is **no two-step circuit**. The task is perfectly periodic, which makes "copy by content" and "copy by offset" the same function in-distribution; the model found the cheaper one. See [ADR-0032](../docs/adr/0032-induction-detector-and-the-positional-shortcut.md).

### Standard scale, GPU, 3 seeds (the measurement that replaces the retracted counts)

<!-- manifest: results/induction_standard.json -->
<!-- manifest: results/induction_standard_emergence.json -->
<!-- manifest: results/exp4_standard.json -->

| Metric | Emergence run (early stop) | Full budget (3000 epochs) | Rung 4 on the same checkpoint |
|--------|--------------------------|----------------------------|--------------------------------|
| Manifest | `induction_standard_emergence.json` | `induction_standard.json` | `exp4_standard.json` |
| Device / wall clock | CUDA, 391 s | CUDA, 3 h 13 min | CPU re-analysis of the GPU checkpoint (epoch 3000) |
| Budget | stopped at the confirmation (epoch 100, two consecutive checks) | 3000 epochs = 384k optimizer steps/seed | — |
| **Confirmed heads (per seed)** | **3, 3, 3** | **3, 2, 3** | 3, 2, 3 |
| … in the first layer | 3, 3, 3 | 3, 2, 3 | 3, 2, 3 |
| … above the first layer (mechanism confirmed) | **0** | **0** | — |
| Peak induction mass (copy offset `q-(L-1)`) | **0.947 ± 0.003** | **0.945 ± 0.001** | — |
| Previous-token mass (control, `q-1`) | 0.033 ± 0.013 | 0.046 ± 0.007 | — |
| K-composition score (L→L) | 0.080 ± 0.020 | 0.052 ± 0.008 | — |
| L0 duplicate-token mass | 0.019 ± 0.002 | 0.200 ± 0.082 | — |
| Final val accuracy | 0.5082 ± 0.0000 | 0.5081 ± 0.0000 | 0.5083 ± 0.0002 |
| **Head ablation — accuracy drop** (exp1, on its own model) | 0.038 ± 0.026 | 0.078 ± 0.044 | — |
| **Head ablation — logit-diff drop** (exp4, same checkpoint) | — | — | **0.4445 ± 0.0425** |
| **Path-patching effect** (direct effect on logits) | not run | not run | **0.8215 ± 0.1255** |
| Activation-patching recovery (layer/position) | not run | not run | 0.0834 ± 0.0002 |
| Dissociation probe — content mass | 0.031 ± 0.001 | 0.031 ± 0.000 | 0.0309 ± 0.0003 |
| Dissociation probe — period mass | 0.909 ± 0.015 | 0.695 ± 0.100 | 0.6950 ± 0.0996 |
| **Copy is content-based?** | **no (3/3 seeds)** | **no (3/3 seeds)** | **no (3/3 seeds)** |

Reading the table:

- **The retracted "0 / 8" really was a detector artifact.** At standard scale the
  model forms heads within 50 epochs (the emergence run stops at epoch 100 after
  two consecutive confirmations), with a copy-offset mass of 0.95 against the
  0.3 threshold, while the previous-token control stays at 0.03–0.05.
- **They are not the two-step circuit.** Every confirmed head is in the *first*
  layer, where the detector can only confirm it on the mass (there is no earlier
  layer to compose with). The K-composition between layers is 0.05–0.08, far
  below the 0.4 confirmation bar, and the L0 duplicate-token mass — the head
  that is supposed to find the previous occurrence — stays at 0.02 (early) and
  0.20 (full budget) against a copy-offset mass of 0.95.
- **The causal interventions land, and they are the first end-to-end path-patching
  result in this repository.** On the same checkpoint (epoch 3000), ablating the
  confirmed head costs **0.44** of the answer-minus-counterfactual logit
  difference, and path patching — which isolates the head's *direct* contribution
  to the logits — attributes **0.82** of it to that head. The head is the circuit
  for this task. (The smaller accuracy drops in the first two columns are exp1's
  own ablation, measured as validation *accuracy*: the copy only buys accuracy
  on the second half of the sequence, so a 0.04–0.08 accuracy drop and a 0.44
  logit-difference drop are the same intervention measured on two scales.)
- **But it is a positional copy.** The dissociation probe (a batch whose second
  half is a *permuted* copy of the prefix, so the content target and the fixed
  offset point at different keys) puts the model's mass on the **position**
  target (0.70) and not on the content target (0.03) on 3/3 seeds, in both runs
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

### The content-based task (issue #200) — pre-registered, run pending

The task that *does* contain the question is specified, frozen and waiting for
its GPU run. The short version:

| | |
|---|---|
| **The task** | A key of 36 distinct tokens; four verbatim copy blocks of five, with the source windows **and** the block positions resampled per sequence, so the distance between a token and its previous occurrence changes from block to block. Every token appears at most twice (the task is well posed), the filler is distinct and unpredictable, and the copy queries are derived **from the tokens alone** — the detector never has to trust the generator. |
| **Why it separates the mechanisms** | The best *single fixed offset* explains **17.6%** of the copy queries (measured on the data before the run). A content-matching head can reach 100%. That gap is the claim, and it is a property of the data, not an assumption. |
| **The verdict** | Seven pre-registered criteria (content mass ≥ 0.30, content mass above the best fixed offset by ≥ 0.10, copy accuracy ≥ 0.60, non-modal-distance accuracy ≥ 0.50, copy accuracy above the fixed-offset baseline by ≥ 0.20, ablation drop ≥ 0.10, path-patching effect ≥ 0.20), computed **by code** — `src/experiments/content_verdict.py`, which joins the exp1 and exp4 manifests per seed (`make content-verdict`). The criteria and their thresholds are frozen; a criterion whose measurement is missing is reported missing, and a run whose manifest does not carry it gets the status `INCOMPLETE` and **no verdict**. |
| **The mechanism report** | A *secondary* report, always produced, that describes the circuit rather than deciding the verdict: the aggregate content mass and its concentration, the **group ablation** (the drop in copy accuracy when the whole candidate group is removed) next to the single-head ablations, and the first-order **logit attribution** of every head to the content-vs-position contrast. The candidate group is fixed by a rule that reads the data and the attention masses and never the outcome. |
| **The budget** | 3 seeds × 3000 epochs = 384k optimizer steps per seed, GPU. A negative at that budget is a negative: the budget is not extended after the fact, and no seed is dropped. |
| **The amendments (2026-10-22 and 2026-10-25, before the run)** | The vocabulary drops from 2048 to **256** (`--content-standard`): the periodic task's 2048 answered a constraint this task does not have, and the standard-geometry CPU probe was still at the uniform prediction after 400 epochs at 2048. The cascade's counterfactual is a **minimal pair** — one token changed, in the same sequence — instead of a different sequence. The 2026-10-25 audit fixed the chance level (`mean(1/(q+1))`), normalized the attribution shares by `sum(|v|)`, made an empty candidate group *undetermined*, added the exploratory top-80% mass group, and removed the fabricated zeros for unmeasured ablation/path patching. The separate emergence run was removed: the full-budget run records `confirmed_epoch`, so it added no measurement and would have doubled the GPU budget. The standard-geometry CPU de-risk is tracked and finds a distributed circuit (3 candidate heads, group drop 0.9956, largest single-head drop 0.0986). The seven criteria are untouched. |
| **Where it is** | [ADR-0033](../docs/adr/0033-content-based-induction-task.md), the [pre-registration](../07_capstone/notes/variable-distance-induction-preregistration.md) (with its two addenda), the notebook `notebooks/kaggle_induction_content.ipynb` (`make remote-run-induction-content`). |

**Status: [ ] not run.** No number is reported here, because there is none
yet. The experiment exists, its rules are frozen, the instrument is tested (the
verdict is a module, not a notebook cell — see the Honesty Ledger's 2026-10-22
entry), and the run is the open item — the one measurement in this repository
that can still change a headline claim.

### Quick scale (the historical scale, for continuity)

| Metric | Tiny multi-seed (3 seeds, confirmed 2026-08-02) |
|--------|-------|
| Layers / Heads | 2 / 4 |
| d_model | 24 |
| Epochs | 150 |
| Train samples | 256 (resampled every epoch, `--fresh-batches`) |
| Val accuracy | 0.0047 ± 0.0012 (n=3) |
| Peak previous-token mass (the old "diag+1") | 0.177 ± 0.006 (n=3) |
| Induction heads detected (>0.3 threshold) | **RETRACTED — uninterpretable** (the detector measured the previous-token offset; see the Honesty Ledger's 2026-10-19 entry) |

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
| Final val accuracy | **0.45% ± 0.03%** (n=3) | **53.53% ± 0.03%** (n=3) |
| Peak previous-token mass (the old "diag+1") | 0.217 ± 0.010 | 0.201 ± 0.012 |
| Induction heads (>0.3 threshold) | **RETRACTED** (old detector) | **RETRACTED** (old detector) |
| K-composition score | 0.145 ± 0.011 | 0.157 ± 0.012 |

Both arms are far apart in accuracy — two orders of magnitude, in the same
direction as the original prose-only claim — and neither crosses the 0.3
detection threshold in this budget.

**These numbers replace the prose-only "0.05% vs 52.2%" that appeared in nine
documents with no manifest behind it anywhere in `results/`.** The direction and
the conclusion are unchanged; the values are not. See the Honesty Ledger's
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
> *The manifests behind these rows record the same quantity under the old key
> `peak_diag1_mass` — it is the previous-token mass, renamed in the table above
> for what it actually measures.*

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
now scheduled for v1.1, with its taxonomy clarified before the first cell runs
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

| Sparsity | Features represented | Mean dimensionality | Mean \|corr\| |
|----------|----------------------|----------------------|--------------|
| 0.500 | 10 / 20 | 0.250 | 0.302 |
| 0.200 | 15 / 20 | 0.250 | 0.316 |
| 0.100 | 19 / 20 | 0.250 | 0.340 |
| 0.050 | 20 / 20 | 0.250 | 0.349 |
| 0.020 | 20 / 20 | 0.250 | 0.348 |
| 0.010 | 20 / 20 | 0.248 | 0.352 |
| 0.005 | 20 / 20 | 0.248 | 0.352 |
| 0.002 | 20 / 20 | 0.249 | 0.350 |
| 0.001 | 16 / 20 | 0.250 | 0.326 |

Multi-seed manifest (3 seeds, `single_sparsity=0.01`, otherwise identical config):
`n_represented` = 19.67 ± 0.47 (one seed of three landed at 19/20 rather than 20/20 — a
real, small seed-to-seed spread, not noise-free).

Expected (Elhage et al.): as sparsity decreases (features rarely co-active), interference
pressure drops and the model represents more features. **Observed: exactly this — 10/20 at
the densest setting rising to 20/20 by sparsity=0.05, holding through 0.002.** (The drop to
16/20 at the sparsest setting, 0.001, is a genuine capacity limit — the 2000-vs-600-epoch
drill (2026-08-06) refuted the under-training hypothesis (see the MP10 honesty
ledger).) The old flat/near-zero "recovery" numbers above the fix are struck through in
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

**Status**: [x] **The cascade ran end to end on Rung 1's own checkpoint (2026-10-20)** — and path patching is no longer unit-test-only. Patch site and metric fixed 2026-08-01 (see Honesty Ledger — the previous
implementation patched a tensor that never reached the residual stream, and measured
confidence rather than correctness). Path patching added; it did not exist in any form
before this pass. The pre-fix standard-scale recovery numbers (0.787, 0.270, ...) that
used to live in this section are **retracted** — they measured `top1 − top2` under a patch
that mostly didn't land, so they don't mean what they claimed to. Vocabulary-ambiguity task
design bug (see Rung 1) fixed 2026-08-02, since this rung reuses
`make_repeated_token_data`; `--seeds` added.

### The cascade, on the model Rung 1 trained (2026-10-20)

<!-- manifest: results/exp4_standard.json -->

Standard scale, the checkpoint of the full-budget run (epoch 3000), 3 seeds, analysed
with `--from-checkpoint` (the model is loaded, not retrained — the cascade is one
model, not two):

| Metric | Value (mean ± std, n=3) |
|--------|--------------------------|
| Confirmed heads (per seed) | 3, 2, 3 (all in the first layer) |
| **Head ablation effect** (drop in the answer−counterfactual logit difference) | **0.4445 ± 0.0425** (range 0.398–0.501) |
| **Path-patching effect** (the head's *direct* effect on the logits) | **0.8215 ± 0.1255** (range 0.730–0.999) |
| Mean activation-patching recovery (layer/position combos) | 0.0834 ± 0.0002 |
| Dissociation probe — content mass / period mass | 0.0309 / 0.6950 (**positional**, 3/3 seeds) |

**This is the first end-to-end path-patching result in this repository**: the
head that the corrected detector finds is also the head that carries the task's
answer. Ablating it costs 44% of the logit difference; path patching — which
isolates the head's direct contribution to the logits, with every other head,
every MLP and the head's own indirect effects kept clean — attributes 82% of
that to it.

**What the interventions do not settle**: the *mechanism* of the copy. The
dissociation probe says the head copies from a fixed offset rather than from
the previous occurrence of the same token (see Rung 1 and
[ADR-0032](../docs/adr/0032-induction-detector-and-the-positional-shortcut.md)),
and the K-composition between layers is 0.05, so this is a single-head circuit
on a periodic task, not the two-step induction circuit.

### Quick-mode 3-seed manifest, 2026-08-02 (historical)

(`vocab_size=64, seq_len=12, d_model=32, epochs=500`):

| Metric | Value (mean ± std, n=3) |
|--------|--------------------------|
| Final val accuracy | 0.489 ± 0.014 |
| Mean activation-patching recovery (10 layer/position combos) | 0.197 ± 0.007 |
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

| Metric | Synthetic (d_model=64, 8× dict, manifest 2026-08-13) | Real, old (d_model=32, from a 2000-step shakedown checkpoint) | Real, **new** (d_model=64, from the standard-scale confirmed-head checkpoint, 2026-10-20) |
|--------|-------|-------|-------|
| Dictionary size | 512 | 256 | 512 |
| L0 sparsity | 96.60 / 512 (18.9%) | 136.25 / 256 (**53.2%**) | **15.12 / 512 (3.0%)** |
| Fraction of variance explained (FVE) | 0.9749 (97.5%) | 0.9997 (99.97%) | **0.99998** |
| Reconstruction MSE | 0.00101 | 0.1251 | 0.00041 |
| Dead features (fixed 1e-4 threshold) | 39 / 512 (7.6%) | 0 / 256 (0%) | **400 / 512 (78.1%)** |

**What changed, and why it matters.** The old real-activation row read *dense*: 53% of
the dictionary firing per input, with a reconstruction MSE an order of magnitude worse
than the synthetic baseline. This repository read that as "the residual stream of a
small, undertrained model has no sparse structure to find". The new run replaces the
model with the one Rung 1 actually trained (standard scale, 3000 epochs, confirmed head)
and the picture inverts: **L0 15.1 of 512 (3.0%)** with FVE 99.998% and an MSE of 0.0004.
The activations *are* sparse — but only once the model has a circuit to write into
them. The old "dense reconstruction" was a statement about an undertrained model, not
about the SAE.

**And the remaining weakness is the other one.** With 8× the dictionary, **78% of the
features never fire** — the dictionary is far larger than this residual stream needs.
That is a dictionary-size choice, not a property of the model, and it is the honest
"what did I add" reading of this rung: the sparsity gap is closed (53% → 3% L0), and
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
problem is **gone** (53% → 3% L0) and what remains is a dictionary 8× too large, not a
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
(L0 15.12/512, 400/512 dead, 78.1%). A figure that cannot be regenerated
from the evidence is a claim, not a figure.

---

## Open Question — Solution-Regime Phase Diagram (protocol ablation, unblocked 2026-10-14; scheduled for v1.1)

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

## Summary

| Rung | Status | Key Result |
|------|--------|------------|
| 1 — Prefix-Copying Heads (fallback flagship) | ✅ **A head forms at standard scale — and it is positional** (2026-10-20) | Corrected detector, GPU, 3 seeds, 3000 epochs: **2–3 heads/seed**, copy-offset mass **0.945** (previous-token control 0.046), all in the first layer; ablation effect **0.44**, path-patch effect **0.82**; the dissociation probe says the copy follows the **fixed offset** (period 0.70 vs content 0.03), and the K-composition is 0.05 — a single-head prefix-copying circuit, not the two-step induction circuit (ADR-0032) |
| 2 — Grokking (primary flagship) | ✅ **REPRODUCED 2026-10-14** (the 2026-08-11 NO-GROK was a metric artifact) | Nanda protocol, P=113, GPU, 3 seeds: val accuracy 0.9999 ± 0.0002, **k_energy_90 = 5.7 ± 1.2 of 56 — sparse on 3/3 seeds**; the historical repo protocol re-reads the same way |
| 3 — Superposition | ✅ Phase transition confirmed | Root cause found (no real bottleneck); rewritten, reproduces cleanly: 10/20 → 20/20 features represented |
| 4 — Circuit Patching | ✅ **Cascade ran end to end on Rung 1's checkpoint** (2026-10-20) | Head ablation **0.4445 ± 0.0425**, path patching **0.8215 ± 0.1255** — the first end-to-end path-patching result against a real head; activation recovery 0.0834 |
| 5 — SAE Dashboard | ✅ Synthetic reproduced; ✅ **the real-activation gap closed** (2026-10-20) | On the confirmed-head checkpoint the SAE is now *sparse*: L0 15.1/512 (3.0%), FVE 99.998%, MSE 0.0004 — against 53% L0 for the old undertrained model. What remains is a dictionary 8× too large (78% dead features) |
| 6 — ACDC | ❌ Deleted | Was fabricated data; removed 2026-08-01 rather than fixed |
| 1b — Content-based induction (issue #200) | [ ] **Pre-registered, run pending** | The task that removes the positional shortcut (repeats at varying distances; the best fixed offset explains 17.6% of the copy queries), its seven criteria, its budget and its decision rule are frozen in [ADR-0033](../docs/adr/0033-content-based-induction-task.md) and the [pre-registration](../07_capstone/notes/variable-distance-induction-preregistration.md). It is the one measurement in this repository that can still change a headline claim — and it is reported whatever it says |

**What to trust right now, in order**: (1) Rung 2's sparse-circuit reproduction —
GPU, 3 seeds, both protocols, post-audit energy metric, manifests pinned with
provenance; the checkpoints are on disk
(`results/remote/grokking-p113/output2/repo/checkpoints/nanda/`) and the four
`exp2_*` figures were regenerated from them 2026-10-17. (2) Rung 1's
prefix-copying head — GPU, 3 seeds, standard scale, 3000 epochs, with the
causal interventions (ablation 0.44, path patching 0.82) and the dissociation
probe that says the copy is positional rather than content-based; the
detector behind it is planted-tested, and the previous "0 / 8" was a detector
artifact. (3) Rung 3's phase
transition — reproduced cleanly, root cause understood, multi-seed manifest
backs it. (4) Rung 5's real-activation SAE on the confirmed-head checkpoint:
L0 3.0% with FVE 99.998% — the old "dense reconstruction" was a statement
about the old undertrained model, and what remains is a dictionary 8× too
large. (5) Rung 1's
fixed-vs-fresh comparison — a real, large, matched effect, though at a scale still
well below standard. (6) Rung 4's quick multi-seed re-run — activation patching
runs cleanly; the standard-scale cascade above is the current number. The
protocol-ablation phase diagram (issue #168) is scheduled for v1.1.
