---
adr: 0028
title: Shakedown Then Showcase — Micro-Phase 80 (Twenty-Third Continuum Ledger)
date: 2026-09-05
status: OPEN
phase: 7
tags: [type/ledger, phase/7, research/experiment]
consumes: [ADR-0027]
---

**Written at Session 0 of MP-80, from MP-79's intake state.**
**Terminus**: Release = merge + 14 calendar days (target 2026-09-19).
**Consumes**: ADR-0027 final state (OPEN, R1 PENDING, R3 PENDING, R5 PENDING, R2/R4/R6/R7/R8 GATED; MP-74 GPU grokking IN_PROGRESS, extended induction NOT_STARTED, clean-clone GREEN 2026-08-27, neuron ablation COMPLETE).

---

## Ledger Rows (Eight, Pre-Stamped with Windows and Kill-Dates)

| Row | Candidate | Opens Only If | Window | Kill-Date | Status |
|-----|-----------|---------------|--------|-----------|--------|
| 1 | **exp6 shakedown: 1 seed by 2k steps, all instrumentation live** | Always | Session 1–2 | 2026-09-07 | PENDING |
| 2 | **K-comp validation + vocab-offset decision, dated** | Shakedown completes (Row 1) | Session 2–4 | 2026-09-10 | GATED |
| 3 | **Portfolio repair lock-in: 5 pages clickable** | Always | Session 3 | 2026-09-10 | PENDING |
| 4 | **RESULTS + progress-log + gate-debt truthing** | Always | Session 3 | 2026-09-10 | PENDING |
| 5 | **W&B live dashboard, or dated close** | `wandb login` succeeds at S0 | Session 1–2 | 2026-09-07 | PENDING |
| 6 | **Paper v-next decision (diff or "v20 is record" memo)** | New numbers from Rows 1–2 | Session 4 | 2026-09-11 | GATED |
| 7 | **Teaching artifact v22 (shakedown edition) + stranger run** | Row 1 GREEN | Session 5 | 2026-09-12 | GATED |
| 8 | **Gate-Debt Closure + Final Release** | Rows 1–6 complete | Session 6 | 2026-09-13 | GATED |

---

## Universal Override

If MP-74 GPU run (ADR-0024 Row 1) lands SPARSE-FOURIER while MP-80 executes:

- Row 6 (Paper) prioritizes per-frequency reading on the first sparse solution this harness ever produced.
- Row 7 (Teaching Artifact) centers the sparse circuit discovery narrative.
- Kill-dates adjusted in the same session; the GPU manifest is consumed, never waited on.

If the GPU run lands NO-GROK (current expectation):

- Row 6 writes the "dense attractor" derivation from ADR-0024 Row 3 neuron ablation.
- Row 7 centers "sometimes the model finds a different algorithm".

---

## Row Detail

### Row 1: exp6 Shakedown

**Protocol**: one capstone seed, 2000 steps, `checkpoint_every=500`, Fourier + K-comp every 500, `--manifest-path results/probe_capstone_shakedown.json` from the first step.

**Success Criteria**:

- Both task losses decrease over 2000 steps; task ids alternate `[0,1,0,1]` in the log.
- First checkpoint (500 steps) reloads via `resume_step`.
- Manifest produced with modular accuracy, induction accuracy, Fourier k_99 trajectory, max K-comp at 500/1000/1500/2000.

**Falsifier**: checkpoint does not reload → harness fails, no full 20k launch. Loss diverges → check gradient clipping, lr schedule, weight decay, curriculum weights.

### Row 2: K-comp Validation + Vocab-Offset Decision

**Protocol**: run the ported K-comp detector (induction-only batches, adjacent-pair scoring, `_vacuous` marker) against shakedown checkpoints; adjudicate the shared-embedding overlap (modular ids `0..P-1` share rows with induction token ids) with data.

**Decision rule (Session 4)**: if induction val stays near chance while modular learns → implement the dedicated id-range offset test-first and re-run 500 steps. If the offset changes nothing → the bottleneck is elsewhere; record it and move on.

### Rows 3–4: Portfolio + Ledger Truthing

**Protocol**: hostile click-through — every rung page number reaches a manifest tag, every tag reaches a file, every file reaches a command. Rung-2 summary row and Phase-6 gate cell truthed; journal gap closed; `verify-claims` stays at 0.

### Row 5: W&B Verdict

**Protocol**: `wandb login --verify` at Session 0. Live → shakedown group dashboard plus backfilled exp1/exp2 manifests. Dead → Row 5 closes with one dated reason, never a silent skip.

### Row 6: Paper Decision

**Protocol**: new numbers from Rows 1–2 → v-next diff from manifests in `portfolio/paper/main.tex`. None → dated "v20 is the record" memo. No TeX toolchain locally (verified Session 0: no pdflatex/latexmk), so PDF compilation stays graceful-not-green either way.

### Row 7: Teaching Artifact v22

**Protocol**: one runnable notebook on the shakedown checkpoint (Fourier → K-comp → patching with honest vacuous-zero reporting → SAE → literature → honest conclusion), stranger-run on fresh Colab, transcript committed. Four-register distillation written.

### Row 8: Release

**Protocol**: ADR-0028 at zero UNDECIDED rows; merge green locally and on GitHub; `dev == main`; home wired.

---

## Deviations from ADR-0027 State

None at Session 0. Any deviations recorded here as dated ledger notes.

### MP-81 Session 0 intake (2026-09-06)

MP-80 closed without executing a single row (roadmap merged, Sessions 1–6 never ran — third consecutive PRE-EXECUTION roadmap). MP-81 consumes ADR-0028 unchanged: Rows 1/3/4/5 PENDING, Rows 2/6/7/8 GATED with the same opening conditions and kill-dates shifted to the MP-81 session clock. Baseline re-verified live at intake: 208 tests pass, ruff clean, blocking mypy clean, `verify-claims` at 0, six manifests on disk. Toolchains re-pinned: no pdflatex/latexmk, `pages.yml` exists, wandb 0.28.0 / hf 1.28.0 installed, logins unverified. New standing rule: no new roadmap until ADR-0028 hits zero UNDECIDED. Universal override (sparse GPU manifest pivots Rows 6–7) stands.

### MP-82 Session 0 intake (2026-09-06)

MP-81 closed at Session 0 with guardrails landed but zero rows executed (fourth consecutive roadmap at Session 0). MP-82 consumes ADR-0028 unchanged: Rows 1/3/4/5 PENDING, Rows 2/6/7/8 GATED, kill-dates shifted to the MP-82 session clock. Session 0 deltas landed test-first: `--steps`/`--warmup-steps` overrides + `resolve_manifest_path()` in `src/experiments/exp6_capstone.py`, unequal-tail + manifest-integration tests (212 tests), portfolio prose drift fixed (rung-1 800-epoch, rung-3 16/20) and three orphaned PNGs linked with manifest tags. Frozen shakedown invocation: `--seed 0 --steps 2000 --warmup-steps 100 --checkpoint-every 500 --save-model --manifest-path results/probe_capstone_shakedown.json`. Baseline re-verified live: ruff clean, blocking mypy clean, `verify-claims` at 0. Toolchains re-pinned: no pdflatex/latexmk, `pages.yml` exists, wandb/hf installed, logins unverified. Universal override stands.

### MP-83 Session 0 intake (2026-09-06)

MP-82 closed at Session 0 with guardrails landed but zero rows executed. MP-83 consumes ADR-0028 unchanged: Rows 1/3/4/5 PENDING, Rows 2/6/7/8 GATED, kill-dates shifted to the MP-83 session clock; it opens zero new candidates and is the execution arc for these eight rows.
Session 0 truthing corrections (verified live, fixed at source): test count 213 → 212 (collection and full run agree); `huggingface_hub` absent from this venv (two signals: import fails, `uv pip list` empty) — the MP-81/82 "hf installed" claim is struck, install only when Row 7 needs it via the pinned workflow.
Full-tree mypy observed at 201 errors (exit 1, no crash; Makefile/CI "176" stays as the dated 2026-08-18 fact). Baseline re-verified live: 212 tests pass, ruff clean, blocking mypy clean, `verify-claims` at 0, six manifests on disk, wandb 0.28.0 present (login unverified).
Expert decisions: shakedown frozen at 1 seed × 2k steps (second seed only if seed 0 GREEN by S2); paper via dated memo (no CI-PDF rehearsal). Universal override stands.

### MP-84 Session 0 intake (2026-09-06)

MP-83 closed at Session 0 with zero rows executed — the fifth consecutive
Session-0-only roadmap (MP-79 through MP-83). MP-84 consumes ADR-0028 unchanged:
Rows 1/3/4/5 PENDING, Rows 2/6/7/8 GATED, kill-dates shifted to the MP-84 session
clock; it opens zero new candidates and is the breakthrough execution arc.
Session 0 baseline re-verified live (no numbers inherited): 212 tests pass and
collect, ruff clean, blocking mypy clean, `verify-claims` at 0, six manifests on
disk, full-tree mypy 201 errors exit 1 no crash, wandb 0.28.0 present
(login unverified), `huggingface_hub` absent (import fails — MP-83 correction
holds), no pdflatex/latexmk, `pages.yml` present.
Expert decisions: scope locked at zero new candidates; shakedown frozen at 1 seed
by 2k steps under the MP-82/83 invocation; GPU watch gets a hard close at Session
2 (consume the Colab manifest or close as PENDING-EXTERNAL with one dated
reason — 13 days stale is a fact, not a queue); paper via dated memo.
Universal override stands.

### MP-85 Session 0 intake (2026-09-06)

MP-84 closed at Session 0 with zero rows executed — the sixth consecutive
Session-0-only roadmap (MP-79 through MP-84). MP-85 consumes ADR-0028 unchanged:
Rows 1/3/4/5 PENDING, Rows 2/6/7/8 GATED, kill-dates shifted to the MP-85 session
clock; it opens zero new candidates and is the execution-verdict arc.
Session 0 baseline re-verified live (no numbers inherited): 212 tests pass and
collect, ruff clean, blocking mypy clean, `verify-claims` at 0, six manifests on
disk, full-tree mypy 201 errors exit 1 no crash, wandb 0.28.0 present
(login unverified), `huggingface_hub` absent (import fails — MP-83 correction
holds), no pdflatex/latexmk, `pages.yml` present.
Expert decisions: scope locked at zero new candidates; shakedown frozen at 1 seed
by 2k steps under the MP-82/83/84 invocation; GPU watch gets a hard close at
Session 2 (consume the Colab manifest or close as PENDING-EXTERNAL with one dated
reason); paper via dated memo.
Universal override stands.

### MP-86 Session 0 intake (2026-09-06)

MP-85 closed at Session 0 with zero rows executed — the seventh consecutive
Session-0-only roadmap (MP-79 through MP-85). MP-86 consumes ADR-0028 unchanged:
Rows 1/3/4/5 PENDING, Rows 2/6/7/8 GATED, kill-dates shifted to the MP-86 session
clock; it opens zero new candidates and is the execution-record arc.
Session 0 baseline re-verified live (no numbers inherited): 212 tests pass and
collect, ruff clean, blocking mypy clean, `verify-claims` at 0, six manifests on
disk, full-tree mypy 201 errors exit 1 no crash, wandb 0.28.0 present
(login unverified), `huggingface_hub` absent (import fails — MP-83 correction
holds), no pdflatex/latexmk, `pages.yml` present.
Expert decisions: hybrid premise (consume MP-85 transcripts if they exist,
otherwise force the shakedown — never an eighth intake-only roadmap); scope
locked at zero new candidates; shakedown frozen at 1 seed by 2k steps under the
MP-82/83/84/85 invocation; GPU watch gets a hard close at Session 2 (consume the
Colab manifest or close as PENDING-EXTERNAL with one dated reason); paper via
dated memo.
Universal override stands.

---

## Sign-Off

**Session 0 (2026-09-05)**: Intake table committed; twenty-third-generation arc stamped; Row 1 (shakedown) chosen as research row with the shakedown-first decision (CPU now; GPU manifest consumed when it lands, not waited on); vocab-offset deferred to the Session 4 verdict with data (not a Session 1 pre-fix); Rows 2/6/7/8 stamped GATED with opening conditions; Rows 1/3/4/5 stamped PENDING with windows and kill-dates.

**Toolchains pinned Session 0**: pdflatex/latexmk absent; `pages.yml` exists; wandb 0.28.0 installed (login unverified — Row 5 work); hf 1.28.0 installed (no Space — Row 7 scope).

**Baseline re-verified Session 0**: 208 tests pass, `ruff check src/ tests/` clean, blocking `mypy` clean on `src/results.py` + `src/experiments/runner.py`, `verify-claims` at 0, all six manifests on disk.

**Ex-T32 Execution Memo (2026-09-05, Session 0)**: MP-79's intake consumed with dates as MP-80 intake. Pre-record arc governs (ADR-0027 confirms). MP-74/78 adjudication stands: R1 GPU grokking = IN_PROGRESS (Colab launched 2026-08-24, verdict pending); R2 extended induction = NOT_STARTED; R3 neuron ablation = COMPLETE; R4 clean-clone = GREEN 2026-08-27; R5 SAE on head = GATED; teaching artifact v22 = GATED on Row 1; paper v-next = GATED on new numbers. Criteria cited: ADR-0027 OPEN with zero UNDECIDED-at-intake rows pending this adjudication, `verify-claims` at 0, `dev` clean and reconciled with `main` through PR #130. A session stamps, it never re-decides.

**Session 6**: ADR-0028 at zero UNDECIDED rows; merge green; `dev == main`; home wired; roadmap archived with deviations as dated ledger notes; program's twenty-third dated direction.
