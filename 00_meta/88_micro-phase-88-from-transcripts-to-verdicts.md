---
tags: [type/moc, phase/7, research/experiment, state/roadmap]
created: 2026-09-07
consumes: [ADR-0028]
---

# Micro-Phase 88 — From Transcripts to Verdicts: My Execution Breakthrough

> **STATUS: ACTIVE EXECUTION with Row 1 verdict in this PR.** This is my
> personal study log and execution plan for MP-88, written from my live
> Session-0 intake state on `dev`. It consumes
> [[87_micro-phase-87-from-roadmaps-to-transcripts|MP-87 · From Roadmaps to
> Transcripts]], ADR-0028 (OPEN), and the headline numbers in
> [[portfolio/RESULTS]]. I open zero new candidates — this phase turns the
> completed shakedown into dated verdicts. Unlike MP-79 through MP-86, and
> one step past MP-87, this roadmap merges with the full 2000-step verdict
> already on disk: the frozen shakedown ran to completion overnight, all
> four checkpoints saved, the probe manifest committed. The anti-stall gate
> held twice — first the crash fix, now the verdict.

## Showcase Framing

If you have 30 seconds: I build a decoder-only transformer from scratch,
then reverse-engineer the algorithms it learns. My strongest verified
result is Rung 3's superposition phase transition (10/20 going to 20/20
features represented, with regular pentagon geometry in the sparse
regime). My most honest result is Rung 2's NO-GROK negative (P=113, val
accuracy 1.0 across 3 seeds, Fourier dense at k_99 = 111/113). In MP-88
my joint capstone shakedown delivered its first full verdict: after 2000
steps induction accuracy rose from chance (0.0005) to 0.504 while modular
addition stayed at chance (0.0047) with Fourier dense (k_99 = 98.1) —
the harness is GREEN, the science says RETUNE, and the dissociation
itself is the finding.

## Part I — Where I Stand (My State Review)

I am on `dev`, content-equal with `main` through PR #139 (one reconcile
merge ahead, zero content diff). My verified baseline at Session 0,
re-verified live before writing this file (no numbers inherited):

- **Tests:** 217 passing and collected (215 inherited + 2 new resume
  guardrail tests in `tests/test_exp6_resume.py`).
  `ruff check src/ tests/` clean.
- **Types:** blocking `mypy --strict` clean on `src/results.py` plus
  `src/experiments/runner.py`. Full-tree strict still reports 201 errors
  (exit 1, no crash) — the Makefile and CI comments citing the dated
  2026-08-18 count of 176 stay as dated 08-18 facts; my two-line fix adds
  zero new errors.
- **Claims:** `verify-claims` at 0. Nine manifests on disk: the six
  committed flagships, the two MP-87 probe manifests, plus the completed
  full-shakedown manifest (`results/probe_capstone_shakedown.json`,
  2000/2000 steps, committed in this PR).
- **Ledger:** ADR-0028 OPEN. Row 1 verdict lands in this PR (RETUNE, see
  Part II); Rows 3/4 PENDING; Row 5 PENDING with pre-gathered evidence
  (no `~/.netrc`, no `WANDB_API_KEY` — login is interactive-only, the
  Session-2 stamp is a formality either way); Rows 2/6/7/8 GATED.
  MP-74 GPU grokking still IN_PROGRESS (Colab launched 2026-08-24, no
  manifest after 14 days — the Session-2 hard close stands).
- **Toolchains (pinned live via `uv run`):** no `pdflatex`/`latexmk`;
  `wandb` 0.28.0 present, login absent (checked, not assumed);
  `huggingface_hub` absent; `.github/workflows/pages.yml` exists,
  portfolio deploy unrehearsed.

What I trust, in order: (1) Rung 3's phase transition. (2) Rung 2's
dense negative, dated 2026-08-11. (3) My shakedown verdict below — a
full-horizon, checkpointed, manifest-backed dissociation, n=1. (4) Rung
1's fixed-vs-fresh comparison (52.2% vs 0.05%). (5) Rung 4's
activation-patching signal (~0.20 recovery), path patching still
unit-tested only. (6) Rung 5's SAE gap. (7) My capstone runner — now two
crashes smarter: the Fourier guardrail and the resume WARNING are both
proven by execution, not just by tests.

## Part II — My Bottleneck Analysis (Verdict, Fix, Deferrals)

### Session-0 verdict: Row 1 shakedown COMPLETE — harness GREEN, science RETUNE

The frozen invocation ran overnight 2026-09-07 02:00–03:21 UTC (4855 s
wall, ~81 min) on a clean tree (`git_sha db9c4c6`, `git_dirty false`).
Seed 0, 2000/2000 steps, checkpoints at 500/1000/1500/2000 (~51 MB
each), manifest `results/probe_capstone_shakedown.json`. Full record:
[[07_capstone/notes/mp-88-shakedown-verdict|MP-88 shakedown verdict]].

| Metric | Step 550 (MP-87) | Step 2000 (this PR) | Reading |
|---|---|---|---|
| Modular accuracy | 0.0057 | **0.0047** (chance ≈ 0.0088) | Flat at chance — below it, even |
| Induction accuracy | 0.0005 | **0.5041** | ~1000× rise, the run learned |
| Fourier k_99 | 98.2 | **98.1** | Dense throughout, same regime as P=113 |
| Fourier k_90 | — | **67.2** | Dense at every cutoff |
| Max K-comp | 0.31 | **0.394** | Detector alive, head unconfirmed |

Every Row 1 success criterion met: both task streams flowed, task ids
alternated, every checkpoint reloads, instrumentation fired at all four
boundaries with zero crashes post-fix. The harness verdict is GREEN.

The science verdict is **RETUNE** (neither EXTEND nor STOP): joint
training is viable — one task takes off strongly — but imbalanced.
Modular addition never leaves chance while induction reaches 0.50, which
points at the two standing hypotheses, in order: (a) the shared
embedding overlap (modular ids `0..P-1` collide with induction token
ids) actively harms the modular readout — modular finishing *below*
chance is consistent with interference, not just slow learning; (b) the
curriculum weighting (`modular_weight = induction_weight = 1.0`) lets
induction dominate. Both are decided by the Session-4 A/B (vocab-offset
plus reweight, 500 steps, compare modular movement), never by argument.
No full 20k-by-3-seed launch until a retuned 2k shows modular movement.

I claim no induction head: K-comp 0.394 is a composition score, not the
per-head diag+1 mass the 0.3 detection threshold applies to. Path
patching stays unit-tested-only. The dissociation is the finding; a
head would be a second finding I do not have.

### Session-0 fix: resume is loud now (test-first)

The MP-87 wart is closed: `train_single_seed()` logged nothing when
`--resume` could not load — neither for a missing file nor for the
`--save-model`-less invocation that silently trained from scratch.
`tests/test_exp6_resume.py` pins both cases (2 RED, then GREEN with the
whole exp6 suite at 18/18): each logs `RESUME: ... starting fresh` at
WARNING, matching the exp1/exp2 phrasing so one grep covers all three
harnesses, then falls back to step 0. Loud fallback, never silence.

### Deferred honestly (known limitations, not silent debt)

- **Vocab-offset + curriculum reweight** stay a Session-4 decision with
  A/B data, not patched blind on verdict day.
- **Modular loss reads only `logits[:, 1]`** — wasteful by design for
  now; the weighting knobs turn with data.
- **Full-tree mypy (201 errors) stays non-blocking**; the blocking
  allowlist is green and is the CI gate that matters.
- **GPU manifest 14 days stale.** Consumed when it lands, never waited
  on; the hard close lands at Session 2 per the standing rule.
- **Row 5 (W&B):** evidence pre-gathered (no netrc, no env key,
  `wandb` 0.28.0 present). The operator runs `wandb login` or the row
  closes with one dated reason at Session 2 — five minutes either way.

### Expert decisions I took at Session 0

1. **Scope lock: zero new candidates.** ADR-0028 governs; MP-88
   executes it. The standing rule from MP-81 holds.
2. **Verdict before roadmap prose.** Row 1 stamps in this PR from the
   manifest on disk — a roadmap that re-plans a completed run would be
   ceremony.
3. **RETUNE, not EXTEND.** A second seed on the current config would
   multiply an unexamined imbalance; discipline first, statistics
   second. The A/B (offset + reweight, 500 steps) is cheaper than any
   seed and answers the load-bearing question.
4. **Paper via dated memo** — no TeX toolchain, no CI-PDF rehearsal.
5. **Probes commit their manifests.** The 2k manifest lands on the
   probe path; flagship bytes untouched (`verify-claims` at 0).

## Part III — My Roadmap, Step by Step (Sessions 0–6)

### My frozen candidate set (chosen at Session 0, never improvised)

| # | Candidate | Opens only if | Kill-date |
|---|---|---|---|
| 1 | **exp6 verdict: Row 1 stamped RETUNE from the 2k manifest** | Always (done) | S0 |
| 2 | **Retune A/B: vocab-offset + curriculum reweight, 500 steps** | Row 1 RETUNE (landed) | S3 |
| 3 | **Portfolio repair lock-in: every figure linked, prose drift fixed** | Always | S3 |
| 4 | **RESULTS + progress-log + gate-debt truthing to sign-off states** | Always | S3 |
| 5 | **W&B live dashboard, or dated close** | Operator runs `wandb login` | S2, else close with reason |
| 6 | **Paper v-next decision (diff or "v20 is record" memo)** | New numbers from Row 2 | S4 |
| 7 | **Teaching artifact (shakedown edition) + stranger run** | Retune shows modular movement | S5 |
| 8 | **Release: merge, dev == main, home wired** | Rows 1–7 stamped | S6 |

### Session 0 (done, in this PR) — Verdict + guardrail + truthing

Committed the 2k manifest, stamped Row 1 RETUNE with the dissociation
table, landed the resume WARNING test-first (2 RED then 18/18 GREEN),
re-pinned every gate live (217 tests, ruff, blocking mypy,
verify-claims, nine manifests). **Exit:** this file, the verdict note,
the ADR-0028 stamp, 217 tests green. *(Landed.)*

### Session 1 — Retune A/B launch (background)

I implement the vocab-offset (dedicated id range for modular tokens)
test-first plus the curriculum reweight, and I launch the 500-step A/B
against the frozen config in background. Cost is ~20 min, not ~81 —
the A/B answers the question before any full horizon spends compute.
**Exit:** A/B running with heartbeat; transcript appended same day.

### Session 2 — W&B verdict + GPU-watch close

`wandb login` live → backfill dashboard from committed manifests. Dead
→ Row 5 closes with one dated reason (evidence pre-gathered at Session
0). The GPU watch consumes a landed manifest or closes as
PENDING-EXTERNAL — 14 days stale is a fact, not a queue. **Exit:** Row
5 stamped either way; GPU-watch closed or consumed.

### Session 3 — Portfolio repair + ledger truthing

I lock every rung page, update RESULTS and my journal, and convert
every gate-debt cell to LAUNCHED-with-transcript or
CLOSED-with-one-reason. `verify-claims` stays at 0. **Exit:** hostile
click-through — every public number reaches a manifest and a command.

### Session 4 — Retune decision + paper decision

Modular moves in the A/B → I launch the retuned full 2k and draft the
paper diff from manifests. It does not → I write the dated "v20 is the
record" memo and characterize the interference as the contribution.
**Exit:** Rows 2 and 6 stamped with a date.

### Session 5 — Teaching artifact + stranger run

One runnable notebook on the best-available checkpoint (Fourier going
to K-comp going to patching with honest vacuous-zero reporting going
to SAE going to literature going to honest conclusion), stranger-run on
fresh Colab, transcript committed. **Exit:** artifact shipped with
transcript.

### Session 6 — Release

ADR-0028 at zero unstamped rows; merge green locally and on GitHub;
`dev == main`; home wired. **Exit:** the merge; my next dated
direction.

## Part IV — My Deep-Dive Study Topics

1. **Why dense under joint training?** Varma et al. (2023) on grokking
   versus memorization dynamics; Lyu et al. (2024) on scale and
   data-fraction effects. *My question:* does the induction stream
   actively suppress modular circuit formation, or does modular simply
   learn slower? *My falsifier:* the Session-1 A/B — if the offset
   moves modular off chance in 500 steps, interference was the
   suppressor; if nothing moves, the schedule is.
2. **Induction at 0.50 without a confirmed head.** Olsson et al.
   (2022); Nanda and Jacobsen (2023) on K-composition phase changes.
   *My question:* is 0.50 accuracy compositional circuitry or
   sophisticated memorization? *My comparison:* per-head diag+1 mass
   trajectory across the four saved checkpoints versus my
   fresh-batches run.
3. **Below-chance modular: interference signature.** *My question:*
   what mechanism drives accuracy *below* 1/113? A shared-embedding
   collision predicts exactly this: induction updates rotate the rows
   modular readout depends on. *My check:* per-row embedding drift
   correlated with induction gradient steps — cheap, from saved
   checkpoints, no new training.
4. **The SAE sparsity gap, revisited with a learning checkpoint.**
   Bricken et al. (2023); Cunningham et al. (2024). *My question:* does
   harvesting from the step-2000 shakedown checkpoint (induction at
   0.50) narrow the 53%-L0 gap measured on the undertrained source?
   *My run:* `--activations-from` the new checkpoint, gated on the
   retune decision so I harvest once, not twice.
5. **Warmup and curriculum as confounders.** *My falsifier:* the A/B
   reweight arm — if modular moves under reweight alone, the 1.0/1.0
   balance was load-bearing and the schedule, not the architecture,
   owned the dissociation.

## Part V — My Documentation Requirements

| Artifact | Location | Trigger |
|---|---|---|
| This roadmap | `00_meta/88_micro-phase-88-from-transcripts-to-verdicts.md` | Session 0 |
| Shakedown verdict note | `07_capstone/notes/mp-88-shakedown-verdict.md` | Session 0 |
| ADR-0028 row stamps | `docs/adr/0028-continuum-ledger-23.md` | Each session |
| Full-shakedown manifest (probe path) | `results/probe_capstone_shakedown.json` | Session 0 |
| Resume guardrail tests | `tests/test_exp6_resume.py` | Session 0 |
| Retune A/B manifest (probe path) | `results/probe_capstone_retune.json` | Session 1 |
| Portfolio pages, locked | `portfolio/projects/rung-{1..5}/index.md` | Session 3 |
| RESULTS + log + gate-debt truthing | `portfolio/RESULTS.md`, `00_meta/03_progress-log.md`, `checklists/gate-debt.md` | Session 3 |
| Paper diff or record memo | `portfolio/paper/main.tex` or dated memo | Session 4 |
| Teaching artifact + transcript | `notebooks/` | Session 5 |
| Release report | `00_meta/88_micro-phase-88-release-report.md` | Session 6 |

## Part VI — My Practical Exercises

- **Ex-1 · Verdict drill.** From manifest bytes to stamped row: total
  steps, wall clock, git sha + dirty flag, all four checkpoints
  present, every number traced to its manifest key. *Falsifier:* a
  verdict number with no manifest key blocks the stamp.
- **Ex-2 · Resume-loudness drill.** Both silent cases (`--resume`
  without `--save-model`; `--resume` at a missing file) must WARNING
  with "RESUME" and "starting fresh". *Falsifier:* a resume that
  restarts quietly.
- **Ex-3 · Retune A/B drill.** Offset-plus-reweight versus frozen
  config, 500 steps each, modular accuracy as the single score.
  *Falsifier:* an A/B whose arms differ in more than the two
  interventions.
- **Ex-4 · Interference-check drill.** Per-row embedding drift on the
  four saved checkpoints, correlated with induction steps.
  *Falsifier:* uniform drift — no row-level story, no claim.
- **Ex-5 · Probe discipline drill.** Flagship sha unchanged after every
  probe run; `verify-claims` at 0 after every numbers change.
  *Falsifier:* flagship bytes move.
- **Ex-6 · Portfolio click-through.** Every number to a manifest tag,
  every tag to a file, every file to a command. *Falsifier:* a
  dangling ref blocks Session 6.
- **Ex-7 · Four-register distillation.** My verdict as the paper's
  sentence, the annex's sentence, the 30-second claim, and the
  5-minute teaching explanation a stranger can run.

## Part VII — My Strategic Tips and Architectural Best Practices

1. **A session stamps, it never re-decides.** My candidate set froze at
   Session 0; Sessions 1–6 execute.
2. **Verdicts come from manifests, never from memory.** Total steps,
   wall clock, sha, dirty flag — cited or it did not happen.
3. **Test the instrumentation, not just the model.** Two execution
   bugs in two phases both lived in code paths the suites never fired.
   Every periodic callback and every CLI combination gets a live test.
4. **Make silent failures loud.** Resume, vacuous K-comp, missing
   checkpoints — each gets a WARNING or a marker. Silence is where
   validity bugs compound.
5. **RETUNE before REPLICATE.** A second seed on an imbalanced config
   prices statistics on top of an unexamined confound. The A/B is
   cheaper than any seed and answers the better question.
6. **Negatives ship as loudly as positives.** My dense Fourier, my
   flat modular curve, and my below-chance footnote prove my 0.50
   induction number was not cherry-picked.
7. **Every public number clicks back to disk.** No manifest tag, no
   claim. `uv sync --frozen` plus `make reproduce-quick` before every
   session; `make verify-claims` after every numbers change.
8. **CI must pass before merging dev to main. Never bypass failed
   checks.** Conventional Commits with GPG sign-off; `pytest` plus
   `ruff check src/ tests/` plus blocking `mypy` plus `verify-claims`
   green locally before every PR.

## Links

- [[87_micro-phase-87-from-roadmaps-to-transcripts|MP-87 · From Roadmaps
  to Transcripts]] — the phase this roadmap consumes
- [[07_capstone/notes/mp-88-shakedown-verdict|MP-88 shakedown verdict]]
  — the Row 1 evidence this roadmap stamps
- [[07_capstone/notes/mp-78-session-capstone-checkpoint-fix|MP-78
  checkpoint-fix session]] — my TDD precedent
- [[portfolio/RESULTS]] — my honesty ledger and per-rung numbers
- [[07_capstone/README|Capstone README]] — my experiment ladder and
  pipeline
- [[07_capstone/research-plan]] — my research plan, including the Rung
  6 descoping rationale

**Written:** 2026-09-07
**Perspective:** my personal study notes, learning log, and portfolio
showcase
**Status:** ACTIVE EXECUTION — Session 0 landed with Row 1 verdict +
resume guardrail, Sessions 1–6 defined, no improvisation
