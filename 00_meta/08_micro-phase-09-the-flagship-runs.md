---
tags: [type/moc, phase/6, phase/7, research/experiment, state/review]
created: 2026-08-02
---

# Micro-Phase 9 — The Flagship Runs (Roadmap)

A roadmap written before the work, deliberately. Micro-Phase 8 taught me that the most
useful discipline I have is writing down what I expect *before* I measure — the predictions
at the bottom of this note are dated 2026-08-02, and the postscript I add after the runs
will be held against them, not the other way around.

This note is the plan for the next micro-phase: two flagship runs batched into a single GPU
session, plus the study, documentation, and exercises that turn the runs into learning
rather than button-pushing. It is written to stand on its own — a reader can go end to end
without opening `src/` and know exactly what I set out to do and how I will judge it.

## Where this micro-phase starts

State at 2026-08-02, after [[07_micro-phase-08-evidence-pass]]:

- **Rung 3 (superposition)** is the only fully verified headline: the phase transition
  reproduces cleanly (10/20 → 20/20 features represented as sparsity drops), multi-seed,
  with the root cause documented.
- **Rung 2 (grokking, the primary flagship) has never run at full scale.** The code and the
  Colab notebook are ready; the missing ingredient is a GPU. The P=29 quick test is a
  genuine dense-Fourier negative — the code is honest, the scale was too small.
- **No induction head has ever been detected** (0/8 across all seeds and both rungs). The
  matched fixed-vs-fresh comparison (0.05% vs 52.2% validation accuracy) is my strongest
  evidence that a head is *reachable* at standard scale — not yet proof that it forms.
- **Path patching** is validated only by unit tests, and the **SAE's** real-activation run
  (99.97% FVE, 53% L0 — a dense autoencoder, honestly read) was trained on a model with no
  confirmed mechanism. Both are blocked on the two runs below.
- All three committed manifests were recorded against a dirty tree and a stale SHA
  (`6a5a54f`), and every on-disk figure predates the 2026-08-01/02 fixes.

Everything that matters next — the paper's flagship section, the path-patching
demonstration, the SAE dashboard, the Phase 6 gate — funnels through two runs. This
micro-phase is those runs.

## Run A — Grokking modular addition, P=113

The primary flagship, and the single most important open item in the repository. The
vehicle is `notebooks/colab_grokking_full_run.ipynb`, hardened in Micro-Phase 8: it clones
the repo (branch `dev`), asserts CUDA is available, syncs the pinned environment, runs one
plotted seed, then a three-seed manifest run, and zips figures, checkpoint, and
`results/exp2_grokking.json` for download.

Protocol, pre-decided:

- `python -m src.experiments.exp2_grokking --seeds 0,1,2` with the canonical defaults:
  P=113, 30% train fraction, 5000 epochs, lr 1e-3, weight decay 1.0 (the grokking engine),
  AdamW with decoupled no-decay parameter groups, cosine schedule.
- `--save-model` so the grokked checkpoint exists for Rung 5's real-activation SAE.
- Success targets (from the notebook): mean `final_val_acc > 0.9`, `generalization_epoch`
  well under 5000, Fourier `k_99_percent` in the ~10–20 band (a sparse Fourier algorithm),
  and sane progress measures (`phase1_end`/`phase2_end`).
- **Seed budget fixed before the run: 3 seeds × 5000 epochs.** If none grok, the outcome is
  a recorded genuine negative and the fallback ladder is climbed (Rung 1 becomes the
  headline) — not hyperparameter p-hacking.

## Run B — Induction heads at standard scale

The second blocker, and the one everything causal depends on. The fixed-vs-fresh matched
comparison from Micro-Phase 8 (fixed dataset → 0.05% validation accuracy and climbing loss;
fresh batches → 52.2% and still climbing at epoch 800) strongly suggests the task is
learnable with continuous resampling. Standard scale has never been tried with the fixed
task design.

Protocol, pre-decided:

- `exp1_induction_heads.py` with `--fresh-batches`, the corrected vocabulary (2048), and a
  standard-scale epoch budget — the Olsson et al. setup, not the quick-scale one.
- Head detection per seed: any head with diag+1 attention mass above 0.3 counts; the
  detection code is already locked by falsification tests.
- Outcome feeds the chain: a confirmed head unblocks path patching end-to-end (exp4),
  which unblocks the SAE re-run on a model with a real mechanism.

## 1. Deep-Dive Study and Research Topics

Study is what makes the runs interpretable rather than load-bearing on luck. Reading is
mapped to the exact artifact it informs.

1. **Grokking's mechanism, from the source.** Power et al. (2022), the original paper, then
   Nanda et al. (2023) on progress measures — the direct template for `exp2_grokking.py`:
   Fourier decomposition of the embeddings, k_90/k_99 sparsity, frequency ablation, and
   weight decay ≥ 1.0 as the engine of the phase transition. Before the run I want to be
   able to derive, on paper, why modular addition is computable in one layer via the
   trig-identity algorithm (Exercise 7 turns this into a proof note).
2. **Why grokking happens at all.** Liu et al. (2022, Omnigrok) on simplicity bias and
   Varma et al. (2023) on grokking as circuit efficiency — the frame I will use to
   interpret the P=29 negative and to predict which of my P=113 seeds will grok.
3. **Reading a negative result.** Micro-Phase 8 established the discipline: a negative is
   only as informative as its controls. My P=29 result (val acc 0.0017, 29/29 Fourier
   frequencies dense) is a genuine negative because the split bug is fixed and the Fourier
   spectrum is measured correctly — but I still need to understand *why* small P has no
   room to phase-transition, so that "scale" and "bug" never blur again.
4. **Induction-head formation dynamics.** Olsson et al. (2022): the phase change, the role
   of continuous resampling (which my 0.05% vs 52.2% ablation confirmed dramatically), and
   what diag+1 mass actually measures. Why would my model refuse to form heads at quick
   scale — capacity, entropy, or task size?
5. **SAE theory for the re-run.** Bricken et al. (2023) and Cunningham et al. (2023): what
   FVE and L0 should look like on genuinely sparse features, and why 53% L0 reads as a
   wide dense autoencoder. This is my benchmark for the Rung 5 re-run on the grokked
   checkpoint — I need to know what "good" looks like before I look at numbers.
6. **GPU operations for the run.** Colab free-tier session limits, artifact download
   hygiene, and CUDA-vs-CPU determinism caveats. Operational, not theoretical — but it is
   the difference between a run I can cite and a run I have to redo.

## 2. Documentation Requirements

Every artifact the runs must produce, and where it lands:

1. **Commit before running.** The harness only guarantees provenance when `git_dirty:
   false` and `git_sha` is a real commit. All current manifests fail this; the runs fix it
   by being executed from a clean tree.
2. **`results/exp2_grokking.json`** — the first grokking manifest ever, and a re-run of
   `exp1_induction_heads.json` at standard scale, both with the `--seeds` provenance tags.
3. **`portfolio/RESULTS.md`** — Rung 2 table (mean ± std over 3 seeds, generalization
   epoch, Fourier sparsity, phase boundaries), Rung 1 standard-scale row, Rung 5 re-run
   row, and Honesty Ledger entry #4. The ledger stays append-only.
4. **Skill tree** — boxes checked *only with proof*: "Grokking reproduction + Fourier
   reverse-engineering" flips `[x]` only if the manifest exists and the targets are met.
   The vault's own rule applies: a checked box without proof is a lie you tell yourself.
5. **Progress log** — a dated entry for the session, following the journal convention.
6. **Checkpoint** — stored with the run artifacts (Rung 5 depends on it).
7. **Figures** — regenerated from the fixed code (all current PNGs are pre-fix, including
   the stale `exp6_automated_vs_manual.png`, which gets deleted).
8. **Mini-paper** — the grokking section is *unblocked* by this phase, not written in it.
   Prose stays behind evidence, per the ordering Micro-Phase 8 made deliberate.

## 3. Practical Exercises and Hands-On Challenges

Ordered by dependency; each has a defined "done" condition.

1. **Run A — the flagship exercise.** Execute the full protocol above. *Done when* the
   manifest exists and targets are met — or the pre-registered negative is recorded.
2. **Run B — induction heads at standard scale.** *Done when* a standard-scale manifest
   exists with per-seed head detection reported.
3. **Frequency-ablation confirmation.** After a grokked run, `run_ablation_sweep` ablates
   the Fourier frequencies that carry the algorithm. *Done when* the sweep shows
   accuracy collapse exactly at the k_99-identified frequencies — the causal confirmation
   that the Fourier decomposition found the real circuit.
4. **Path patching, end to end.** Point exp4's path patching at a confirmed head.
   *Done when* self-patching is a no-op (already locked by tests) and head patching moves
   logits in the predicted direction on a real model.
5. **SAE re-run on the grokked checkpoint.** `--activations-from` with real activations.
   *Done when* the FVE/L0 comparison against the 99.97%/53% baseline is recorded honestly —
   sparser, denser, or unchanged, all acceptable answers.
6. **Rung 3 geometry check.** The one open sub-item: the pentagon Gram-matrix
   (5 features → 2 dimensions) against the known small case. *Done when* verified or
   falsified with a note in RESULTS.md.
7. **Written proofs, closing the vault gap.** No dedicated grokking proof or exercise
   exists in the vault. Write (a) a proof note deriving the modular-addition Fourier
   algorithm (why trig identities make f(a + b) computable in one layer), and (b) a note on
   induction-head formation dynamics. *Done when* both exist, link to the skill tree, and
   are written from my own derivation, not a summary of the papers.

## 4. Strategic Tips and Architectural Best Practices

1. **Commit before you run.** Provenance is the whole point of the harness; a manifest
   pinned to a dirty tree cannot back a claim. This is the cheapest correctness habit I
   have.
2. **Batch the GPU session.** Run A, Run B, and the ablation share one Colab session —
   minutes of compute each, one session's overhead. Download artifacts (the zip) the
   moment they exist; Colab sessions evaporate.
3. **Pre-register, then do not move the goalposts.** Seed budget, thresholds, and the
   ~2-week time-box from the research plan are fixed now. If grokking does not reproduce in
   honest effort, Rung 1 becomes the headline — that decision is made *today*, when I have
   no stake in the outcome.
4. **Save checkpoints while training.** Rung 5 depends on the grokked checkpoint; a run
   without a saved checkpoint is a run that has to be redone.
5. **Keep the honesty ledger append-only.** Micro-Phase 8's three audit entries stay; this
   phase's entry is #4, written in the same register whether the runs succeed or fail.
6. **One negative result is a result.** The P=29 dense-Fourier negative was genuine and
   useful; the standard-scale negatives will be too. Record them; do not retune against
   them.
7. **Defer cleanly, name the deferral.** `exp5 --seeds`, `reproduce-multiseed` for
   exp2/exp5, the 154 mypy strict-mode errors, and W&B tracking are later micro-phases.
   They are written down so the roadmap does not quietly grow.
8. **CI discipline.** Ruff, mypy (the blocking scope), pytest, and markdownlint must pass
   before `dev → main`; conventional, GPG-signed commits throughout.

## Risks and Bottlenecks

- **Colab session loss** — mitigated by downloading artifacts as they appear; the
  notebook's final zip is a convenience, not the only copy.
- **Variance vs. the 3-seed budget** — a small budget is honest, not conclusive; mean ±
  std over 3 seeds is the declared resolution, and RESULTS.md will say so.
- **Run B may still not form heads** — pre-registered. The fixed-vs-fresh comparison
  remains my strongest signal either way; a second 0-heads result at standard scale is a
  finding about my task design, not a reason to keep pushing the same lever.
- **Stale artifacts polluting the ledger** — the exp6 figure and pre-fix PNGs are on the
  cleanup checklist; every figure claimed in RESULTS.md will be regenerated from the
  committed code.
- **My own bias** — after a P=29 negative, the temptation will be to "help" the run with
  hyperparameters. The budget is fixed; the fallback ladder is fixed; this note is the
  contract.

## Predicted Outcomes (Pre-Registration)

Written 2026-08-02, before any run:

- **Run A:** I expect 2–3 of 3 seeds to grok within 5000 epochs — the scale is the
  canonical Nanda reproduction, so failure would be surprising in a way worth explaining.
  I expect `generalization_epoch` in the 1000–4000 band and `k_99_percent` in the 10–20
  band. My honest prior: P(≥ 1 seed groks) ≈ 0.75. One grokking seed is partial success —
  informative, but the claim must say "1 of 3".
- **Run B:** I expect at least one seed to produce a head above the 0.3 diag+1 threshold at
  standard scale with fresh batches, because the fresh-batches trajectory was still
  climbing when its budget ran out. My honest prior: P(≥ 1 head) ≈ 0.6. A 0-head result is
  a finding, not a silence.
- Either way, the micro-phase is a success if the honest ledger entry, the manifests, and
  the regenerated figures exist and match what happened.

## Links

- [[portfolio/RESULTS]] — the full per-rung numbers and Honesty Ledger this phase extends
- [[07_micro-phase-08-evidence-pass]] — the pass this phase builds on
- [[03_deep_learning/notes/training-dynamics-and-grokking]] — the grokking concept note
- [[04_nlp_and_transformers/notes/induction-heads]] — the induction-head concept note
- [[01_roadmap]] — where this micro-phase sits in the full path
- [[02_skill-tree]] — the boxes this phase earns the right to check
- [[03_progress-log]] — the dated journal this phase will enter
- [[06_production_ai/notes/results-manifests-and-provenance]] — the harness this phase runs on
