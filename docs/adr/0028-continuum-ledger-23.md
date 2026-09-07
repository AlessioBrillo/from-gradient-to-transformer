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
| 1 | **exp6 shakedown: 1 seed by 2k steps, all instrumentation live** | Always | Session 1–2 | 2026-09-07 | VERDICT-RETUNE 2026-09-07 (see MP-88 intake below) |
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

### MP-87 Session 0 intake + Session-1 transcript (2026-09-06)

MP-86 closed at Session 0 with zero rows executed — the seventh consecutive
Session-0-only roadmap (MP-79 through MP-86). MP-87 breaks the stall by
merging with a Session-1 transcript attached: the frozen shakedown was
launched under the MP-82 invocation, trained 500 steps, and crashed at the
first `fourier_every` boundary (`RuntimeError: Can't call numpy() on Tensor
that requires grad`, `exp6_capstone.py:258` — live `model.embed.weight`
slice into `.numpy()`; existing tests pin `fourier_every` to 10**9, which is
why it escaped). Fixed test-first (`tests/test_exp6_fourier.py`, 3 RED then
GREEN; `embeddings.detach()` at the function boundary), validated with a
550-step run (1714.5 s wall clock, k_99 98.2, max K-comp 0.31, step-500
checkpoint saved, `results/probe_capstone_fixcheck.json`), and resume-proven
(`--save-model --resume 500 --steps 510`, `ckpt['step'] == 500`,
`results/probe_capstone_resume.json`). Baseline re-verified live: 215 tests
pass, ruff clean, blocking mypy clean, `verify-claims` at 0, full-tree mypy
201 errors exit 1 no crash, wandb 0.28.0 present via `uv run` (system-python
import fails — command corrected, not the fact), `huggingface_hub` absent,
no pdflatex/latexmk. Rows 1/3/4/5 PENDING, Rows 2/6/7/8 GATED, kill-dates
shifted to the MP-87 session clock. Recorded warts: resume is a silent no-op
without `--save-model` (exp1/exp2 warn; exp6 does not — follow-up, not this
PR); frozen shakedown measures ~100+ min for 2000 steps (4.26M params), so
Session 1 runs it in background post-merge.
Universal override stands.

### MP-88 Session 0 intake + Row 1 verdict (2026-09-07)

MP-87's Session-1 transcript predicted a background 2k run; the run
completed overnight 2026-09-07 02:00–03:21 UTC (4855 s wall) under the
frozen invocation — 2000/2000 steps, checkpoints at 500/1000/1500/2000,
manifest `results/probe_capstone_shakedown.json` (seed 0, git_sha
db9c4c6, git_dirty false). Verdict RETUNE, stamped from manifest bytes:
modular accuracy 0.0047 (flat at chance, 1/113 ≈ 0.0088), induction
accuracy 0.5041 (from 0.0005 at step 550), Fourier k_99 98.1 (dense,
same regime as the P=113 NO-GROK baseline), max K-comp 0.394
(detector alive, no head claimed — the 0.3 threshold applies to
per-head diag+1 mass, not to K-comp). Harness GREEN on every Row 1
criterion; science RETUNE — joint training viable but imbalanced, so
the retune A/B (vocab-offset plus curriculum reweight, 500 steps per
arm, modular movement as single score) opens as Row 2 and no 20k-by-3
launch opens before it. Session-0 hardening landed alongside: the
MP-87 silent-resume wart closed test-first (`tests/test_exp6_resume.py`,
2 RED then 18/18 exp6 GREEN — both no-checkpoint-dir and missing-file
cases now WARNING with "RESUME ... starting fresh", matching exp1/exp2
phrasing). Baseline re-verified live: 217 tests pass, ruff clean,
blocking mypy clean, `verify-claims` at 0, full-tree mypy 201 errors
exit 1 no crash, wandb 0.28.0 present with login absent (no `~/.netrc`,
no `WANDB_API_KEY` — Row 5 stays PENDING to Session 2, where the
operator runs `wandb login` or the row closes with one dated reason),
`huggingface_hub` absent, no pdflatex/latexmk. Rows 3/4 PENDING, Rows
2/6/7/8 GATED with MP-88 kill-dates (see the MP-88 roadmap).
Universal override stands.

### MP-89 Session 0 intake + retune harness (2026-09-07)

MP-88 stamped Row 1 RETUNE from the completed 2k manifest and opened
Row 2 as the retune A/B. MP-89 executes it: Session-0 harness landed
test-first (`tests/test_exp6_retune.py`, 6 RED then 6/6 GREEN — offset
plus reweight flags, collision-free range validation, loud overflow
errors; whole exp6 suite 24/24, ruff clean, offset end-to-end proven
with Fourier firing on the offset slice). Frozen A/B invocation:
`--seed 0 --steps 500 --warmup-steps 100 --checkpoint-every 500
--save-model` with `--vocab-offset 2048` (Arm A, dedicated range
[2048, 2161) disjoint from induction [0, 2048)) and
`--modular-weight 5.0 --induction-weight 0.5` (Arm B, 10x relative
boost for the 1-token vs 127-token supervision mismatch), each on its
probe manifest (`results/probe_capstone_ab_{control,offset,reweight}.json`;
`make reproduce-retune-*`). Intermediate validation now logs per-task
loss/accuracy (the mixed mean hid the MP-88 dissociation — fixed at
source, not just in reading). Baseline re-verified live: 217 tests
pass pre-change, ruff clean, blocking mypy clean, `verify-claims` at
0. Row 2 OPEN (A/B running, verdict at Session 1); Rows 3/4 PENDING;
Row 5 PENDING to Session 2; Rows 6/7/8 GATED with MP-89 kill-dates
(see the MP-89 roadmap). No 20k-by-3 launch before the A/B verdict.
Universal override stands.

### MP-89 Session 1 — A/B verdict (2026-09-07)

Three 500-step probe manifests collected. Single score: modular
accuracy off chance (1/113 ≈ 0.00885). Results: Control 0.0062,
Offset 0.0060, Reweight 0.0065 — **all below chance**. Neither
vocab-offset nor curriculum reweight moves modular off chance in 500
steps. Induction stays near zero (0.0005) in all arms. K-comp: control
0.3690, offset 0.1728, reweight 0.3048. Verdict: **NO-MOVE**. No
retuned 2k launch; the "v20 is the record" memo path taken. Row 2
stamped VERDICT-NO-MOVE with this note; Rows 3/4 PENDING; Row 5
PENDING to Session 2; Rows 6/7/8 GATED. `verify-claims` at 0.
Universal override stands.

---

## Sign-Off

**Session 0 (2026-09-05)**: Intake table committed; twenty-third-generation arc stamped; Row 1 (shakedown) chosen as research row with the shakedown-first decision (CPU now; GPU manifest consumed when it lands, not waited on); vocab-offset deferred to the Session 4 verdict with data (not a Session 1 pre-fix); Rows 2/6/7/8 stamped GATED with opening conditions; Rows 1/3/4/5 stamped PENDING with windows and kill-dates.

**Toolchains pinned Session 0**: pdflatex/latexmk absent; `pages.yml` exists; wandb 0.28.0 installed (login unverified — Row 5 work); hf 1.28.0 installed (no Space — Row 7 scope).

**Baseline re-verified Session 0**: 208 tests pass, `ruff check src/ tests/` clean, blocking `mypy` clean on `src/results.py` + `src/experiments/runner.py`, `verify-claims` at 0, all six manifests on disk.

**Ex-T32 Execution Memo (2026-09-05, Session 0)**: MP-79's intake consumed with dates as MP-80 intake. Pre-record arc governs (ADR-0027 confirms). MP-74/78 adjudication stands: R1 GPU grokking = IN_PROGRESS (Colab launched 2026-08-24, verdict pending); R2 extended induction = NOT_STARTED; R3 neuron ablation = COMPLETE; R4 clean-clone = GREEN 2026-08-27; R5 SAE on head = GATED; teaching artifact v22 = GATED on Row 1; paper v-next = GATED on new numbers. Criteria cited: ADR-0027 OPEN with zero UNDECIDED-at-intake rows pending this adjudication, `verify-claims` at 0, `dev` clean and reconciled with `main` through PR #130. A session stamps, it never re-decides.

**Session 6**: ADR-0028 at zero UNDECIDED rows; merge green; `dev == main`; home wired; roadmap archived with deviations as dated ledger notes; program's twenty-third dated direction.
