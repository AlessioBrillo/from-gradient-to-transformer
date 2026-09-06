---
tags: [type/moc, phase/7, research/experiment, state/roadmap]
created: 2026-09-06
consumes: [ADR-0028]
---

# Micro-Phase 87 — From Roadmaps to Transcripts: My Execution Breakthrough

> **STATUS: ACTIVE EXECUTION with Session-1 transcript in this PR.**
> This is my personal study log and execution plan for MP-87, written from my
> live Session-0 intake state on `dev`. It consumes
> [[86_micro-phase-86-from-stamps-to-record|MP-86 · From Stamps to Record]],
> ADR-0028 (OPEN, Rows 1/3/4/5 PENDING, rest GATED), and the headline numbers
> in [[portfolio/RESULTS]]. I open zero new candidates — this phase turns
> ADR-0028's stamps into dated transcripts or closes each row with one dated
> reason. Unlike MP-79 through MP-86, this roadmap merges with a Session-1
> transcript already attached: the frozen shakedown ran, crashed, got fixed
> test-first, and re-validated past the crash boundary. The anti-stall gate
> held.

## Showcase Framing

If you have 30 seconds: I build a decoder-only transformer from scratch, then
reverse-engineer the algorithms it learns. My strongest verified result is
Rung 3's superposition phase transition (10/20 going to 20/20 features
represented, with regular pentagon geometry in the sparse regime). My most
honest result is Rung 2's NO-GROK negative (P=113, val accuracy 1.0 across
3 seeds, Fourier dense at k_99 = 111/113). In MP-87 I broke my
seven-roadmap Session-0-only stall the only way that counts — I ran the
frozen 1-seed by 2k-step capstone shakedown, watched it crash at step 500,
fixed the crash test-first, and proved the fix past the crash boundary with
a 550-step validation run plus a checkpoint-resume proof.

## Part I — Where I Stand (My State Review)

I am on `dev`, clean, reconciled with `main` through PR #138. My verified
baseline at Session 0, re-verified live before writing this file (no numbers
inherited from MP-86):

- **Tests:** 215 passing and collected (212 inherited + 3 new Fourier
  regression tests in `tests/test_exp6_fourier.py`).
  `ruff check src/ tests/` clean.
- **Types:** blocking `mypy --strict` clean on `src/results.py` plus
  `src/experiments/runner.py`. Full-tree strict still reports 201 errors
  (exit 1, no crash) — the Makefile and CI comments citing the dated
  2026-08-18 count of 176 stay as dated 08-18 facts; my one-line fix adds
  zero new errors.
- **Claims:** `verify-claims` at 0. Eight manifests on disk: the six
  committed flagships plus two new probe manifests
  (`results/probe_capstone_fixcheck.json`, 550 steps;
  `results/probe_capstone_resume.json`, resume proof) — both on the probe
  path, flagship bytes untouched.
- **Ledger:** ADR-0028 OPEN with eight rows (R1 shakedown PENDING, R3/R4/R5
  portfolio-and-truthing PENDING, rest GATED). MP-74 GPU grokking still
  IN_PROGRESS (Colab launched 2026-08-24, no manifest downloaded);
  extended induction 10k NOT_STARTED; clean-clone proof GREEN 2026-08-27;
  neuron ablation COMPLETE.
- **Toolchains (pinned live via `uv run`, not system python):** no
  `pdflatex`/`latexmk`; `wandb` 0.28.0 present, login unverified (Row 5
  work); `huggingface_hub` absent (import fails — MP-83 correction holds);
  `.github/workflows/pages.yml` exists, portfolio deploy unrehearsed.
  Correction to my own MP-86 note: `python -c "import wandb"` on system
  python fails — the pinned claim is `uv run python -c "import wandb"`
  reporting 0.28.0. Same venv, honest command.

What I trust, in order: (1) Rung 3's phase transition. (2) Rung 2's dense
negative, dated 2026-08-11. (3) Rung 1's fixed-vs-fresh comparison (52.2%
vs 0.05%). (4) Rung 4's activation-patching signal (~0.20 recovery), path
patching still unit-tested only. (5) Rung 5's SAE gap. (6) My capstone
runner — now one crash smarter: the Fourier guardrail, the probe-path
guardrail, real K-comp, and the checkpoint/resume contract all proven by
execution, not just by tests.

## Part II — My Bottleneck Analysis (What Broke, What I Fixed, What I Deferred)

### Session-1 transcript: the step-500 Fourier crash (FIXED test-first)

I launched the frozen shakedown exactly as MP-82 through MP-86 specified
it (`--seed 0 --steps 2000 --warmup-steps 100 --checkpoint-every 500
--save-model --manifest-path results/probe_capstone_shakedown.json`). It
trained 500 steps, then died at the first `fourier_every` boundary:

```text
File "src/experiments/exp6_capstone.py", line 258, in fourier_decomposition
    dominant_mags = magnitudes.topk(top_k, dim=0).values.cpu().numpy()
RuntimeError: Can't call numpy() on Tensor that requires grad.
```

Root cause: `train_single_seed()` passes a live `model.embed.weight`
slice (`requires_grad=True`) into `fourier_decomposition()`, which called
`.numpy()` on it. The existing capstone tests pin `fourier_every` to
10**9 (never fires) — that is exactly why the bug escaped every suite.
Seven roadmaps froze an invocation no test had ever executed past step 500.

Fix (one line + docstring, matching the exp2 convention of
`weight.data.detach()` but enforced at the function boundary so all
callers are protected): `embeddings = embeddings.detach()` at the top of
`fourier_decomposition()`. Regression tests first — 3 failed with the exact
production `RuntimeError` (RED), then 16/16 exp6 tests pass after the fix
(GREEN), ruff clean. Full validation run: 550 steps in 1714.5 s wall clock,
crossed the step-500 boundary cleanly, Fourier k_99 = 98.2 and max K-comp
= 0.31 logged, step-500 checkpoint saved (51 MB), probe manifest written.
Resume proof: `--save-model --resume 500 --steps 510` reloaded the
checkpoint (`ckpt['step'] == 500`, keys
model/optimizer/scheduler/seed/step) and continued — `results/probe_capstone_resume.json`
on disk.

Early shakedown numbers (550/2000 steps, chance-level as expected — this is
a harness verdict, not a science verdict): modular acc 0.0057, induction
acc 0.0005, k_99 98.2 (dense, early), max K-comp 0.31 (non-zero — the
detector is alive on joint data).

### Two warts I found and recorded (not silently fixed)

1. **Resume is a silent no-op without `--save-model`.** My first resume
   attempt omitted `--save-model`, so `checkpoint_dir=None` and the
   `if resume_step > 0 and checkpoint_dir:` branch skipped without a word —
   the run trained from scratch while I waited. Exp1/exp2 log a WARNING in
   this case ("starting fresh"); exp6 says nothing. I used the correct
   invocation for the proof; unifying exp6 with the exp1/exp2 warning is a
   tracked follow-up, never a drive-by in this PR.
2. **Throughput is the real schedule driver.** Measured, not estimated: the
   frozen shakedown is a 4.26M-parameter model at ~3.1 s/step early,
   accelerating to ~1.7 s/step (550 steps = 29 min). My old "few minutes"
   estimate used the 135k-param smoke config — wrong model, wrong number.
   The full 2000-step shakedown costs ~100+ min and runs in background;
   sessions plan around it, never wait on it.

### Deferred honestly (known limitations, not silent debt)

- **Shared embedding overlap** stays a Row 2 decision with shakedown data
  at Session 4, not patched blind.
- **Modular loss reads only `logits[:, 1]`** — wasteful by design for now.
- **Warmup frozen at 100** for the shakedown; if the start is too noisy I
  record it, never silently adjust.
- **Full-tree mypy (201 errors) stays non-blocking**; the blocking
  allowlist is green.
- **GPU manifest stale** — consumed when it lands, never waited on; hard
  close at Session 2 per MP-85/86.

### Expert decisions I took at Session 0

1. **Scope lock: zero new candidates.** ADR-0028 governs; MP-87 executes it.
2. **No merge without a transcript.** This PR carries the crash log, the
   fix, the 550-step validation manifest, and the resume manifest. An
   eighth intake-only roadmap would have been a verdict on my process.
3. **Probes commit their manifests.** `probe_*.json` files are dated
   execution evidence on a path that cannot touch the flagship — committed,
   not gitignored.
4. **Paper via dated memo** — no TeX toolchain, no CI-PDF rehearsal.
5. **Full 2k shakedown launches in background post-merge** under the frozen
   invocation; its verdict stamps Row 1 next sitting.

## Part III — My Roadmap, Step by Step (Sessions 0–6)

### My frozen candidate set (chosen at Session 0, never improvised)

| # | Candidate | Opens only if | Kill-date |
|---|---|---|---|
| 1 | **exp6 shakedown: 1 seed by 2k steps, all instrumentation live** | Always | S2 |
| 2 | **K-comp validation + vocab-offset decision, dated** | Shakedown completes (Row 1) | S3 |
| 3 | **Portfolio repair lock-in: every figure linked, prose drift fixed** | Always | S3 |
| 4 | **RESULTS + progress-log + gate-debt truthing to sign-off states** | Always | S3 |
| 5 | **W&B live dashboard, or dated close** | `wandb login` succeeds at S0 | S2, else close with reason |
| 6 | **Paper v-next decision (diff or "v20 is record" memo)** | New numbers from Rows 1–2 | S4 |
| 7 | **Teaching artifact (shakedown edition) + stranger run** | Row 1 GREEN | S5 |
| 8 | **Release: merge, dev == main, home wired** | Rows 1–7 stamped | S6 |

### Frozen shakedown invocation (unchanged since MP-82, now crash-proven to 550)

```bash
uv run python -m src.experiments.exp6_capstone \
  --seed 0 --steps 2000 --warmup-steps 100 \
  --checkpoint-every 500 --save-model \
  --manifest-path results/probe_capstone_shakedown.json
```

### Session 0 (done, in this PR) — Truthing + crash fix + validation

Re-pinned every gate live, launched the frozen shakedown, captured the
step-500 crash, fixed it test-first (RED then GREEN), validated past the
boundary (550 steps, manifest + checkpoint), proved resume (510 steps from
step-500 checkpoint, manifest). **Exit:** this file, ADR-0028 intake stamp,
215 tests green. *(Landed.)*

### Session 1 — Full shakedown launch (background)

Launch the frozen 2000-step invocation in background with log redirect;
verify the first post-fix 500-step checkpoint reloads (already proven —
re-verify on the new run). Cost ~100+ min; the session does not wait.
**Exit:** shakedown running with heartbeat; transcript appended same day.

### Session 2 — Shakedown verdict + W&B verdict + GPU-watch close

Record modular/induction accuracy, Fourier k_99 trajectory, max K-comp at
500/1000/1500/2000. W&B live or Row 5 closes with one dated reason. GPU
watch consumes a landed manifest or closes as PENDING-EXTERNAL.
**Exit:** Rows 1 and 5 stamped either way.

### Session 3 — Portfolio repair + ledger truthing

Lock every rung page, update RESULTS and my journal, convert every
gate-debt cell to LAUNCHED-with-transcript or CLOSED-with-one-reason.
`verify-claims` stays at 0. **Exit:** hostile click-through — every public
number reaches a manifest and a command.

### Session 4 — Paper decision + vocab-offset decision

New numbers exist → v-next diff from manifests. They do not → dated "v20
is the record" memo. Same sitting: vocab-offset redesign decided with
shakedown data. **Exit:** Rows 2 and 6 stamped with a date.

### Session 5 — Teaching artifact + stranger run

One runnable notebook on the shakedown checkpoint (Fourier going to K-comp
going to patching with honest vacuous-zero reporting going to SAE going to
literature going to honest conclusion), stranger-run on fresh Colab,
transcript committed. **Exit:** artifact shipped with transcript.

### Session 6 — Release

ADR-0028 at zero unstamped rows; merge green locally and on GitHub;
`dev == main`; home wired. **Exit:** the merge; my next dated direction.

## Part IV — My Deep-Dive Study Topics

1. **Why dense? Grokking versus dense memorization-generalization.** Varma
   et al. (2023); Lyu et al. (2024); Chughtai et al. (2023). *My
   question:* does joint modular-plus-induction training pressure my
   capstone toward modular sub-circuits or the dense attractor of P=113?
   *My falsifier:* Fourier plus neuron ablation on shakedown checkpoints
   versus my P=113 dense baseline. Early signal: k_99 = 98.2 at step 550
   (dense, but 550 steps is harness territory, not science).
2. **Induction emergence at scale.** Olsson et al. (2022); Nanda and
   Jacobsen (2023). *My question:* does joint training accelerate
   duplicate-detection into composition? *My comparison:* K-comp trajectory
   versus my fresh-batches run. Early signal: max K-comp 0.31 at step 550 —
   the detector is alive; the trajectory decides.
3. **The SAE sparsity gap.** Bricken et al. (2023); Cunningham et al.
   (2024). *My question:* dictionary-size artifact or
   undertrained-residual artifact?
4. **Patching validity without a head.** Zhang and Nanda (2024); Wang et
   al. (2023). *My answer:* vacuous zeros reported as vacuous, never
   plotted.
5. **Warmup and curriculum as confounders.** *My falsifier:* loss and
   K-comp curves with the 100-step override versus flagship 1000.

## Part V — My Documentation Requirements

| Artifact | Location | Trigger |
|---|---|---|
| This roadmap | `00_meta/87_micro-phase-87-from-roadmaps-to-transcripts.md` | Session 0 |
| ADR-0028 row stamps + frozen invocation | `docs/adr/0028-continuum-ledger-23.md` | Each session |
| Fix validation manifests (probe path) | `results/probe_capstone_fixcheck.json`, `results/probe_capstone_resume.json` | Session 0 |
| Fourier regression tests | `tests/test_exp6_fourier.py` | Session 0 |
| Shakedown manifest (probe path) | `results/probe_capstone_shakedown.json` | Sessions 1–2 |
| K-comp + vocab-offset verdict | `07_capstone/notes/mp-87-shakedown-verdict.md` | Session 4 |
| Portfolio pages, locked | `portfolio/projects/rung-{1..5}/index.md` | Session 3 |
| RESULTS + log + gate-debt truthing | `portfolio/RESULTS.md`, `00_meta/03_progress-log.md`, `checklists/gate-debt.md` | Session 3 |
| Paper diff or record memo | `portfolio/paper/main.tex` or dated memo | Session 4 |
| Teaching artifact + transcript | `notebooks/` | Session 5 |
| Release report | `00_meta/87_micro-phase-87-release-report.md` | Session 6 |

## Part VI — My Practical Exercises

- **Ex-1 · Crash reproduction drill.** Grad-requiring tensor into
  `fourier_decomposition` must raise before the fix, pass after.
  *Falsifier:* RED suite that stays red.
- **Ex-2 · Boundary drill.** Any run crossing `fourier_every` on live
  weights without crashing. *Falsifier:* step-500 traceback.
- **Ex-3 · Resume drill.** `--save-model --resume 500 --steps 510`
  continues from `ckpt['step'] == 500`. *Falsifier:* manifest starts at
  step 0 or checkpoint keys mismatch.
- **Ex-4 · Probe discipline drill.** Flagship sha unchanged after every
  probe run. *Falsifier:* flagship bytes move.
- **Ex-5 · Portfolio click-through.** Every number to a manifest tag,
  every tag to a file, every file to a command. *Falsifier:* a dangling
  ref blocks Session 6.
- **Ex-6 · W&B verdict drill.** `wandb login --verify` at execution
  Session 0. Live goes to dashboard; dead closes Row 5 with one dated
  reason.
- **Ex-7 · Four-register distillation.** My verdict as the paper's
  sentence, the annex's sentence, the 30-second claim, and the 5-minute
  teaching explanation a stranger can run.

## Part VII — My Strategic Tips and Architectural Best Practices

1. **A session stamps, it never re-decides.** My candidate set froze at
   Session 0; Sessions 1–6 execute.
2. **Freeze the invocation, not just the candidate set.** Then *run* it —
   a frozen invocation no test executes past step 500 is a wish.
3. **Test the instrumentation, not just the model.** My suites pinned
   `fourier_every` to 10**9 and measured nothing; the crash lived exactly
   there.
4. **Negatives ship as loudly as positives.** My crash log and dense early
   numbers prove my positives were not cherry-picked.
5. **No full 20k by 3-seed launch until the 2k shakedown is GREEN.**
6. **Every public number clicks back to disk.** No manifest tag, no claim.
7. **Tests first, always — especially for interpretability
   interventions.**
8. **CI must pass before merging dev to main. Never bypass failed
   checks.** Conventional Commits with GPG sign-off; `pytest` plus
   `ruff check src/ tests/` plus blocking `mypy` plus `verify-claims`
   green locally before every PR.

## Links

- [[86_micro-phase-86-from-stamps-to-record|MP-86 · From Stamps to Record]] — the phase this roadmap consumes
- [[07_capstone/notes/mp-78-session-capstone-checkpoint-fix|MP-78 checkpoint-fix session]] — my TDD precedent
- [[portfolio/RESULTS]] — my honesty ledger and per-rung numbers
- [[07_capstone/README|Capstone README]] — my experiment ladder and pipeline
- [[07_capstone/research-plan]] — my research plan, including the Rung 6 descoping rationale

**Written:** 2026-09-06
**Perspective:** my personal study notes, learning log, and portfolio showcase
**Status:** ACTIVE EXECUTION — Session 0 landed with crash fix + validation transcripts, Sessions 1–6 defined, no improvisation
