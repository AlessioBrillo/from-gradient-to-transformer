---
tags: [type/moc, phase/7, research/experiment, state/roadmap]
created: 2026-09-07
consumes: [ADR-0028]
---

# Micro-Phase 89 — From RETUNE to Signal: My Retune A/B Execution

> **STATUS: ACTIVE EXECUTION — Session 0 harness landed test-first, A/B
> running.** This is my personal study log and execution plan for MP-89,
> written from my live Session-0 intake state on `dev`. It consumes
> [[88_micro-phase-88-from-transcripts-to-verdicts|MP-88 · From Transcripts
> to Verdicts]], ADR-0028 (OPEN, Row 1 VERDICT-RETUNE 2026-09-07), and the
> headline numbers in [[portfolio/RESULTS]]. I open zero new candidates —
> this phase answers the one load-bearing question my shakedown verdict
> opened: does a vocab-offset plus curriculum reweight move modular
> addition off chance in 500 steps?

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
itself is the finding. In MP-89 I isolate the cause with a 500-step A/B:
a vocab-offset arm against the frozen control, a reweight arm against
the frozen control, modular movement as the single score.

## Part I — Where I Stand (My State Review)

I am on `dev`, synced with `origin/dev`, working tree clean at Session 0.
My verified baseline, re-verified live before writing this file (no
numbers inherited):

- **Tests:** 217 passing pre-change (`pytest -q`, 71.8 s).
  `ruff check src/ tests/` clean. Blocking `mypy --strict` clean on
  `src/results.py` plus `src/experiments/runner.py`.
- **Claims:** `verify-claims` at 0 (`all manifests and RESULTS.md tags
  check out`). Nine manifests on disk, flagship `exp6_capstone.json`
  untouched.
- **Ledger:** ADR-0028 OPEN. Row 1 VERDICT-RETUNE (MP-88); Row 2 GATED —
  opens in this phase; Rows 3/4 PENDING; Row 5 PENDING (no `~/.netrc`,
  no `WANDB_API_KEY` — login is interactive-only); Rows 6/7/8 GATED.
  MP-74 GPU grokking still IN_PROGRESS (Colab launched 2026-08-24, no
  manifest).
- **Toolchains (pinned live via `uv run`):** no `pdflatex`/`latexmk`;
  `wandb` present, login absent; `huggingface_hub` absent;
  `.github/workflows/pages.yml` exists, portfolio deploy unrehearsed.

What I trust, in order: (1) Rung 3's phase transition. (2) Rung 2's
dense negative, dated 2026-08-11. (3) My shakedown dissociation — a
full-horizon, checkpointed, manifest-backed dissociation, n=1.
(4) Rung 1's fixed-vs-fresh comparison (52.2% vs 0.05%). (5) Rung 4's
activation-patching signal (~0.20 recovery), path patching still
unit-tested only. (6) Rung 5's SAE gap. (7) My capstone runner — now
three crashes smarter: the Fourier guardrail, the resume WARNING, and
(landing in this phase) the retune argument plumbing.

## Part II — My Bottleneck Analysis (Verdict, Fix, Deferrals)

### The two standing hypotheses (from my MP-88 verdict)

My shakedown ended with modular *below* chance (0.0047 < 1/113 ≈
0.0088) while induction reached 0.5041. Below-chance is not slow
learning — it is consistent with active interference. Two candidates,
in order:

1. **Shared-embedding overlap.** Modular ids `0..P-1` share rows with
   induction token ids `0..2047`, and `pad_id = modulus (113)` collides
   with real induction token 113. Induction updates rotate the exact
   rows modular readout depends on. Fix under test: dedicated id range
   `[2048, 2161)` with pad at 2161 — disjoint from induction
   `[0, 2048)` (Arm A).
2. **Curriculum imbalance.** Round-robin is 50/50 by batch, but modular
   `F.cross_entropy(logits[:, 1], mod_target)` supervises 1 token while
   induction supervises 127 LM tokens — at 1.0/1.0 induction gradient
   dominates. Fix under test: modular 5.0 / induction 0.5, a 10×
   relative boost strong enough to detect movement in 500 steps without
   collapsing induction entirely (Arm B).

### Session-0 fix: the retune harness, test-first

RED first (`tests/test_exp6_retune.py`, 6 failures: missing
`--vocab-offset` / `--modular-weight` / `--induction-weight` flags,
missing `vocab_offset` plumbing, no overflow guard), then GREEN (6/6,
whole exp6 suite 24/24, ruff clean, `--help` lists the new flags, tiny
offset end-to-end trains 4 steps with Fourier firing on the offset
slice at k_99 = 6.62):

- `make_modular_addition_data(..., vocab_offset=0)` — ids relocate to
  `[offset, offset+P)`, pad to `offset+P`, targets recomputed from
  un-offset values. Default 0 keeps the frozen control bit-identical.
- `make_mixed_dataloaders()` validates loudly: offset + P beyond
  vocab raises `ValueError` (never silent wrap); nonzero offset below
  induction vocab raises `ValueError` (use 0 or a dedicated range).
- `train_single_seed()` reads `cfg["task"]["modular"]["vocab_offset"]`
  and slices Fourier at `[offset:offset+P]` in both the periodic and
  final analyses; final eval regenerates modular data with the offset.
- CLI `--vocab-offset` / `--modular-weight` / `--induction-weight`
  override config explicitly (defaults `None` — never silent).
- Intermediate validation at every 1000 steps now logs **per-task**
  loss/accuracy (the mixed mean hid modular movement — the exact
  failure mode of my MP-88 dissociation table, fixed at source).
- `make reproduce-retune-{control,offset,reweight}` — frozen 500-step
  arms, seed 0, warmup 100, probe manifests only
  (`results/probe_capstone_ab_{control,offset,reweight}.json`).

### Deferred honestly (known limitations, not silent debt)

- **Modular loss reads only `logits[:, 1]`** — wasteful by design for
  now; the weighting knobs turn with data at Session 2.
- **No combined offset+reweight arm** until the singles report — a
  combined arm before the singles is an uninterpretable experiment.
- **No second seed** until a 500-step arm shows modular movement —
  discipline first, statistics second.
- **Full-tree mypy stays non-blocking**; the blocking allowlist is
  green and is the CI gate that matters.
- **GPU manifest stale.** Consumed when it lands, never waited on.
- **Row 5 (W&B):** closes at Session 2 either way — dashboard or one
  dated reason.

### Expert decisions I took at Session 0

1. **Scope lock: zero new candidates.** ADR-0028 governs; MP-89
   executes it.
2. **Harness before runs.** The A/B launches only after its flags,
   validation, and manifests are pinned by tests — the MP-87 lesson
   (untested instrumentation paths crash after 34 minutes of compute).
3. **Arms differ in exactly one intervention each.** Offset-vs-control,
   reweight-vs-control. No combined arm, no second seed, no 20k launch
   before the verdict.
4. **Per-task logging fixed at source.** The mixed-mean val that hid my
   dissociation is gone from the loop, not just from my reading.
5. **Probes commit their manifests.** The three A/B manifests land on
   the probe path; flagship bytes untouched (`verify-claims` at 0).

## Part III — My Roadmap, Step by Step (Sessions 0–6)

### My frozen candidate set (chosen at Session 0, never improvised)

| # | Candidate | Opens only if | Kill-date |
|---|---|---|---|
| 1 | **Retune harness test-first (this PR)** | Always (done) | S0 |
| 2 | **Retune A/B verdict: 500-step arms, modular movement as score** | Harness GREEN (running) | S2 |
| 3 | **W&B live dashboard, or dated close + GPU-watch hard close** | Always | S2 |
| 4 | **Portfolio repair lock-in + RESULTS + log + gate-debt truthing** | Always | S3 |
| 5 | **Retune decision: full retuned 2k or "v20 is the record" memo** | A/B verdict | S4 |
| 6 | **Teaching artifact (retune edition) + stranger run** | Modular movement | S5 |
| 7 | **Release: merge, dev == main, home wired** | Rows 1–6 stamped | S6 |

### Session 0 (done, in this PR) — Harness + A/B launch

Landed the retune harness test-first (6 RED then 6/6 GREEN, exp6 suite
24/24, ruff clean, offset end-to-end proven), added the three frozen
`make reproduce-retune-*` targets, launched control/offset/reweight in
background (500 steps each, ~20 min per arm, probe manifests). **Exit:**
this file, the harness tests, the Makefile targets, A/B running with
heartbeat.

### Session 1 (done, 2026-09-07) — A/B verdict: NO-MOVE

Three probe manifests collected. Single score: modular accuracy off
chance (1/113 ≈ 0.00885). Results: Control 0.0062, Offset 0.0060,
Reweight 0.0065 — **all below chance**. Neither vocab-offset nor
curriculum reweight moves modular off chance in 500 steps. Induction
stays near zero (0.0005) in all arms. K-comp: control 0.3690, offset
0.1728, reweight 0.3048. Verdict: **NO-MOVE**. No retuned 2k launch;
the "v20 is the record" memo path taken. **Exit:**
`07_capstone/notes/mp-89-retune-verdict.md` plus ADR-0028 Row 2 stamp
(VERDICT-NO-MOVE 2026-09-07).

### Session 2 — W&B verdict + GPU-watch close

`wandb login` live going to backfilled dashboard from committed
manifests. Dead going to Row 5 closes with one dated reason (evidence
pre-gathered). The GPU watch consumes a landed manifest or closes as
PENDING-EXTERNAL. **Exit:** Row 5 stamped either way; GPU-watch closed
or consumed.

### Session 3 — Portfolio repair + ledger truthing

I lock every rung page, update RESULTS and my journal, and convert
every gate-debt cell to LAUNCHED-with-transcript or
CLOSED-with-one-reason. `verify-claims` stays at 0. **Exit:** hostile
click-through — every public number reaches a manifest and a command.

### Session 4 — Paper decision (NO-MOVE path taken)

A/B verdict was NO-MOVE; no retuned 2k launch. The dated "v20 is the
record" memo is written (or the paper diff from existing manifests if
any new numbers emerge from portfolio truthing). **Exit:** Row 6 stamped
with a date.

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
   data-fraction effects; Nanda et al. (2023) on Fourier progress
   measures. *My question:* does the induction stream actively suppress
   modular circuit formation, or does modular simply learn slower under
   equal weighting? *My falsifier:* my Session-1 A/B — offset movement
   implicates interference; reweight-only movement implicates schedule;
   neither moving implicates architecture or horizon.
2. **Below-chance modular as interference signature.** *My question:*
   what mechanism drives accuracy *below* 1/113? A shared-embedding
   collision predicts exactly this: induction updates rotate the rows
   modular readout depends on. *My check:* per-row embedding drift on
   my four saved shakedown checkpoints, correlated with induction steps
   — cheap, from disk, no new training.
3. **Induction at 0.50 without a confirmed head.** Olsson et al.
   (2022); Nanda and Jacobsen (2023) on K-composition phase changes.
   *My question:* is 0.50 accuracy compositional circuitry or
   sophisticated memorization? *My comparison:* per-head diag+1 mass
   trajectory across my four saved checkpoints versus my
   fresh-batches run. K-comp 0.394 is a composition score, never the
   0.3 per-head detection threshold — I claim no head.
4. **The SAE sparsity gap, revisited with a learning checkpoint.**
   Bricken et al. (2023); Cunningham et al. (2024). *My question:* does
   harvesting from my step-2000 shakedown checkpoint (induction at
   0.50) narrow the 53%-L0 gap measured on the undertrained source?
   *My run:* `--activations-from` the new checkpoint, gated on the
   retune decision so I harvest once, not twice.
5. **Warmup and curriculum as confounders.** Power et al. (2022) on
   grokking sensitivity to optimization. *My falsifier:* my reweight
   arm — if modular moves under reweight alone, the 1.0/1.0 balance was
   load-bearing and the schedule, not the architecture, owned my
   dissociation.

## Part V — My Documentation Requirements

| Artifact | Location | Trigger |
|---|---|---|
| This roadmap | `00_meta/89_micro-phase-89-from-retune-to-signal.md` | Session 0 |
| Retune harness tests | `tests/test_exp6_retune.py` | Session 0 |
| Retune Makefile targets | `Makefile` (reproduce-retune-*) | Session 0 |
| A/B manifests (probe path) | `results/probe_capstone_ab_{control,offset,reweight}.json` | Session 1 |
| A/B verdict note | `07_capstone/notes/mp-89-retune-verdict.md` | Session 1 |
| ADR-0028 row stamps | `docs/adr/0028-continuum-ledger-23.md` | Each session |
| Portfolio pages, locked | `portfolio/projects/rung-{1..5}/index.md` | Session 3 |
| RESULTS + log + gate-debt truthing | `portfolio/RESULTS.md`, `00_meta/03_progress-log.md`, `checklists/gate-debt.md` | Session 3 |
| Paper diff or record memo | `portfolio/paper/main.tex` or dated memo | Session 4 |
| Teaching artifact + transcript | `notebooks/` | Session 5 |
| Release report | `00_meta/89_micro-phase-89-release-report.md` | Session 6 |

## Part VI — My Practical Exercises

- **Ex-1 · Harness drill.** Offset changes ids and nothing else;
  reweight changes loss scaling and nothing else; flagship sha
  unchanged; `verify-claims` at 0. *Falsifier:* an arm whose config
  differs in more than its single intervention blocks launch.
- **Ex-2 · A/B discipline drill.** Control vs offset vs reweight, 500
  steps each, same seed/warmup/batch, separate probe manifests,
  modular accuracy as the single score. *Falsifier:* a verdict number
  with no manifest key blocks the stamp.
- **Ex-3 · Interference-check drill.** Per-row embedding drift on my
  four saved checkpoints, correlated with induction steps.
  *Falsifier:* uniform drift — no row-level story, no claim.
- **Ex-4 · No-head-honesty drill.** K-comp trajectory reported
  alongside per-head diag+1 mass; path patching stays unit-tested-only
  until a real head exists. *Falsifier:* a head claimed from a
  composition score.
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
   Every periodic callback and every CLI combination gets a live test —
   my retune flags shipped with one before any compute burned.
4. **Make silent failures loud.** Resume, vacuous K-comp, missing
   checkpoints, overflowing offsets — each gets a WARNING, a marker, or
   a `ValueError`. Silence is where validity bugs compound.
5. **RETUNE before REPLICATE.** A second seed on an imbalanced config
   prices statistics on top of an unexamined confound. My A/B (~20 min
   per arm) is cheaper than any seed and answers the better question.
6. **Isolate one variable per arm.** Offset tests interference;
   reweight tests schedule. A combined arm before the singles is an
   uninterpretable experiment.
7. **Negatives ship as loudly as positives.** My dense Fourier, my
   flat modular curve, and my below-chance footnote prove my 0.50
   induction number was not cherry-picked.
8. **Every public number clicks back to disk.** No manifest tag, no
   claim. `uv sync --frozen` plus `make reproduce-quick` before every
   session; `make verify-claims` after every numbers change.
9. **CI must pass before merging dev to main. Never bypass failed
   checks.** Conventional Commits with GPG sign-off; `pytest` plus
   `ruff check src/ tests/` plus blocking `mypy` plus `verify-claims`
   green locally before every PR.

## Links

- [[88_micro-phase-88-from-transcripts-to-verdicts|MP-88 · From
  Transcripts to Verdicts]] — the phase this roadmap consumes
- [[07_capstone/notes/mp-88-shakedown-verdict|MP-88 shakedown verdict]]
  — the Row 1 evidence this roadmap acts on
- [[07_capstone/notes/mp-89-retune-verdict|MP-89 retune verdict]] — my
  Session-1 verdict (lands with the A/B manifests)
- [[portfolio/RESULTS]] — my honesty ledger and per-rung numbers
- [[07_capstone/README|Capstone README]] — my experiment ladder and
  pipeline
- [[07_capstone/research-plan]] — my research plan, including the Rung
  6 descoping rationale

**Written:** 2026-09-07
**Perspective:** my personal study notes, learning log, and portfolio
showcase
**Status:** ACTIVE EXECUTION — Session-0 harness landed test-first,
A/B running, Sessions 1–6 defined, no improvisation
