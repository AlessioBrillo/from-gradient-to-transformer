---
tags: [type/moc, phase/7, research/experiment, state/roadmap]
created: 2026-09-06
consumes: [ADR-0028]
---

# Micro-Phase 86 — From Stamps to Record: My Execution Record

> **STATUS: ACTIVE EXECUTION.** This is my personal study log and execution plan
> for MP-86, written from my live Session-0 intake state on `dev`. It consumes
> [[85_micro-phase-85-from-stall-to-stamps|MP-85 · From Stall to Stamps]],
> ADR-0028 (OPEN, Rows 1/3/4/5 PENDING, rest GATED), and the headline numbers in
> [[portfolio/RESULTS]]. I open zero new candidates — this phase turns
> ADR-0028's stamps into a dated record or closes each row with one dated
> reason. The candidate set below freezes at Session 0; I decide there,
> I never improvise later.

## Showcase Framing

If you have 30 seconds: I build a decoder-only transformer from scratch, then
reverse-engineer the algorithms it learns. My strongest verified result is
Rung 3's superposition phase transition (10/20 going to 20/20 features
represented, with regular pentagon geometry in the sparse regime). My most
honest result is Rung 2's NO-GROK negative (P=113, val accuracy 1.0 across
3 seeds, Fourier dense at k_99 = 111/113). In MP-86 I convert stamps into
record — I run the frozen 1-seed by 2k-step capstone shakedown, I stamp at
least Rows 1 and 5 with dated verdicts, and I make every public number click
back to a manifest and a command.

## Part I — Where I Stand (My State Review)

I am on `dev`, clean, reconciled with `main` through PR #137. My verified
baseline at Session 0, re-verified live before writing this file:

- **Tests:** 212 passing and collected (`pytest --collect-only -q` agrees: 212).
  `ruff check src/ tests/` clean.
- **Types:** blocking `mypy --strict` clean on `src/results.py` plus
  `src/experiments/runner.py`. Full-tree strict reports 201 errors (exit 1, no
  crash) — the Makefile and CI comments still cite the dated 2026-08-18 count
  of 176, which stays as a dated 08-18 fact; 201 is my new dated observation,
  mostly missing-generic-args pedantry plus my own exp6 additions, tracked
  follow-up, never rushed.
- **Claims:** `verify-claims` at 0, all six manifests on disk
  (`results/exp{1,2,3,4,5}_*.json` plus `results/exp6_capstone.json`, the latter
  still smoke-scale: P=17, 100 steps). See [[07_capstone/README|Capstone README]]
  for the full experiment ladder.
- **Ledger:** ADR-0028 OPEN with eight rows (R1 shakedown PENDING, R3/R4/R5
  portfolio-and-truthing PENDING, rest GATED). MP-74 GPU grokking still
  IN_PROGRESS (Colab launched 2026-08-24, no manifest downloaded after 13 days);
  extended induction 10k NOT_STARTED; clean-clone proof GREEN 2026-08-27;
  neuron ablation COMPLETE.
- **Toolchains (pinned live):** no `pdflatex`/`latexmk` (paper PDF stays
  scaffold-only); `wandb` 0.28.0 installed, login unverified (Row 5 work);
  `huggingface_hub` is **absent** from this venv — confirmed again this session
  via failed import, matching the MP-83 correction; `.github/workflows/pages.yml`
  exists, portfolio deploy unrehearsed.

What I trust, in order: (1) Rung 3's phase transition — reproduced cleanly with
its root cause understood. (2) Rung 2's dense negative — three seeds, dated
2026-08-11. (3) Rung 1's fixed-vs-fresh comparison — fresh batches at 52.2%
val accuracy versus fixed dataset at 0.05%, still below the induction-head
detection threshold either way. (4) Rung 4's activation-patching signal (about
0.20 recovery) — real but small, with path patching still unit-tested only.
(5) Rung 5's SAE gap — synthetic FVE 0.9749 at L0 96.6/512, real-activation
prose-only at 99.97% FVE but 53% L0: an informative degradation, not a win.
(6) My capstone runner — RoundRobin alternation, harvester 4-tuple fix,
`--manifest-path` guardrail, real K-comp port, `--steps`/`--warmup-steps`
overrides and `resolve_manifest_path` all landed test-first; its full 2k-step
shakedown not yet started.

## Part II — My Bottleneck Analysis (What I Fixed, What I Deferred)

### My top bottleneck: stamps without a record

MP-79 through MP-85 are seven consecutive Session-0 roadmaps. Each re-pins the
same baseline, re-stamps the same eight rows, and freezes the same invocation
— and none has produced a Session-1 transcript. My countermeasure in MP-86 is
structural, not motivational: **one row owns this phase (Row 1 shakedown),
Sessions 1 and 2 are specified to the command level, Session 6 cannot open
until Rows 1 and 5 are stamped, and every session after Session 0 appends its
transcript to the ledger the same day.** An eighth Session-0-only roadmap
would be a verdict on my process, not on my plans.

### Fixed as Session 0 truthing (verified live, in this commit)

1. **Baseline re-pinned, no drift inherited.** 212 tests pass, ruff clean,
   blocking mypy clean, `verify-claims` at 0, six manifests on disk,
   `huggingface_hub` absent, wandb 0.28.0 present. I re-ran every gate instead
   of copying MP-85's numbers, because a portfolio that copies its own
   baselines cannot ask to be trusted on Fourier sparsity.
2. **Full-tree mypy re-observed at 201.** Same count as MP-83/84/85, same
   interpretation: non-blocking, tracked follow-up. The Makefile and CI
   comments citing 176 stay as dated 2026-08-18 facts; I do not rewrite history
   to match my observation.
3. **Prior guardrails stand:** RoundRobin alternation, unequal-tail pinning,
   harvester 4-tuple unpack, `--manifest-path` probe guardrail with
   `resolve_manifest_path`, real K-comp port with `_vacuous` markers, frozen
   shakedown invocation below.

### Deferred honestly (known limitations, not silent debt)

- **Shared embedding overlap** (modular ids `0..P-1` share rows with induction
  token ids; `pad_id = modulus` collides with a real induction token).
  Offsetting modular ids into a dedicated range is a semantic redesign — Row 2
  scope, decided with shakedown data at Session 4, not patched blind.
- **Modular loss reads only `logits[:, 1]`** while padded positions are
  ignored. Wasteful by design for now; the curriculum weighting
  (`modular_weight` and `induction_weight`) is the knob I will turn with data,
  not before it.
- **Warmup frozen at 100 for the shakedown** (versus 1000 flagship): the 2k
  shakedown must observe early phase-change dynamics; a 50%-of-horizon warmup
  would mask them. If the start is too noisy I record it as a dated fact and
  adjust, never silently.
- **Full-tree mypy (201 errors) stays non-blocking.** The blocking allowlist
  (`src/results.py`, `src/experiments/runner.py`) is green and is the CI gate
  that matters; paying down 201 generic-args annotations inside an execution
  phase would be motion disguised as progress.
- **GPU manifest 13 days stale.** I consume it when it lands; I never wait on
  it. MP-86 keeps the hard close set in MP-85 (see expert decision 3).

### Expert decisions I took at Session 0 (tradeoffs closed, with reasons)

1. **Scope lock: zero new candidates.** ADR-0028 stays the governing document
   and MP-86 is its execution arc. The standing rule from MP-81 holds: no new
   roadmap until ADR-0028 hits zero unstamped rows. My bottleneck is execution,
   and new candidates are its camouflage.
2. **Hybrid premise: consume-or-force.** If MP-85's Sessions 1–6 produced
   transcripts, I consume them as intake. If it stalled again, I force the
   shakedown under the same frozen invocation rather than writing another
   intake-only roadmap. Either way this file's Sessions 1–6 execute.
3. **Shakedown stays 1 seed by 2k steps — no 2-seed expansion upfront.**
   A second seed opens only if seed 0 is GREEN by Session 2. Parallel seeds on
   an unshaken harness multiply unexamined failure modes; discipline first,
   statistics second.
4. **GPU watch gets a hard close at Session 2.** If no Colab manifest has
   landed by my Session 2 verdict sitting, I close the GPU-watch as
   PENDING-EXTERNAL with one dated reason and keep the CPU shakedown
   independent. Thirteen days without a manifest is a supervision failure, not
   a compute bottleneck — the close converts silence into a dated fact.
5. **Paper goes the memo route — no CI-PDF rehearsal in Session 4.** With no
   local TeX toolchain and no new numbers guaranteed, a "v20 is the record"
   memo is the honest artifact; a rehearsal would burn a session to prove what
   the scaffold already documents (graceful-not-green).

### New risks I am watching

1. **An eighth Session-0-only roadmap would be a verdict on my process.**
   Sessions 1–6 below are specified to the command level so that "execute"
   never again means "decide what execute means."
2. **Gate-debt cannot sign off as written.** Ten of eleven cells block release
   (2 PENDING, 4 GATED which is not a sign-off state, 4 LAUNCHED without
   transcripts). Session 3 converts every cell to LAUNCHED-with-transcript or
   CLOSED-with-one-reason.
3. **Path patching without a head.** Reporting vacuous zeros as results would
   repeat the exact error class my 2026-08-01 Validity Pass fixed. I report
   them as vacuous, keep the unit-test gate, never plot them.

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

### Frozen shakedown invocation (Session 0 decision, never improvised)

```bash
uv run python -m src.experiments.exp6_capstone \
  --seed 0 --steps 2000 --warmup-steps 100 \
  --checkpoint-every 500 --save-model \
  --manifest-path results/probe_capstone_shakedown.json
```

### Session 0 (~1 h) — Gate truthing + toolchain pinning + invocation freeze

I consumed MP-85's intake state, adjudicated all eight rows above, froze the
invocation, pinned toolchains live (212 tests, ruff, blocking mypy,
verify-claims, six manifests, wandb 0.28.0 present and hf absent, no TeX, pages
workflow present). **Exit:** ADR-0028 eight rows stamped; invocation frozen; no
row opens without its condition cited. *(This file is that exit.)*

### Session 1 (~2 h) — Shakedown launch

I launch one capstone seed per the frozen invocation. I verify the first 500
steps: loss decreasing on both tasks, task ids alternating in the log,
checkpoints resuming via `resume_step`. **Exit:** shakedown running; first
checkpoint reloads or the harness fails loudly.

### Session 2 (~2 h) — Shakedown verdict + W&B verdict + GPU-watch close

I record modular and induction accuracy, Fourier k_99 trajectory, and max
K-comp at 500/1000/1500/2000. W&B is either live with the shakedown group or
Row 5 closes with one dated reason. The GPU watch either consumes a landed
manifest or closes as PENDING-EXTERNAL with one dated reason — 13 days stale
is a fact, not a queue. **Exit:** Row 1 verdict stamped (extend / retune /
stop); Row 5 stamped either way; GPU-watch closed or consumed.

### Session 3 (~3 h) — Portfolio repair + ledger truthing

I lock in every rung page, update RESULTS and the journal, and convert every
gate-debt cell to LAUNCHED-with-transcript or CLOSED-with-one-reason.
`verify-claims` stays at 0. **Exit:** hostile click-through — every public
number reaches a manifest and a command.

### Session 4 (~2 h) — Paper decision + vocab-offset decision

New numbers exist → I draft the v-next diff from manifests. They do not → I
write the dated "v20 is the record" memo (decision taken at Session 0,
executed here). In the same sitting I decide the vocab-offset redesign with
shakedown data. **Exit:** Rows 2 and 6 stamped with a date.

### Session 5 (~3 h) — Teaching artifact + stranger run

I build one runnable notebook on the shakedown checkpoint (Fourier going to
K-comp going to patching with honest vacuous-zero reporting going to SAE going
to literature going to honest conclusion) and run it as a stranger on fresh
Colab, committing the transcript. **Exit:** artifact shipped with transcript;
four-register distillation written.

### Session 6 (~1 h) — Release

ADR-0028 at zero unstamped rows; merge green locally and on GitHub;
`dev == main`; home wired. **Exit:** the merge; my next dated direction.

## Part IV — My Deep-Dive Study Topics

1. **Why dense? Grokking versus dense memorization-generalization.** Varma et
   al. (2023) on grokking versus memorization dynamics; Lyu et al. (2024) on
   scale and data-fraction effects; Chughtai et al. (2023) on toy-model
   grokking constructions. *My question:* does joint modular-plus-induction
   training pressure my capstone toward modular sub-circuits or the same dense
   attractor I measured at P=113? *My falsifier:* Fourier plus neuron ablation
   on shakedown checkpoints versus my P=113 dense baseline.
2. **Induction emergence at scale: from duplicate-detection to composition.**
   Olsson et al. (2022) on induction heads and in-context learning; Nanda and
   Jacobsen (2023) on K-composition phase changes. *My question:* does joint
   training accelerate duplicate-detection into composition? *My comparison:*
   K-comp trajectory at shakedown checkpoints versus my fresh-batches run (peak
   diag+1 0.145, still rising at epoch 800).
3. **The SAE sparsity gap: dictionary size versus residual quality.** Bricken
   et al. (2023) on monosemanticity and the pre-encoder bias; Cunningham et
   al. (2024) on SAE scaling. *My question:* is L0 96/512 a dictionary-size
   artifact or an undertrained-residual artifact? *My sweep:* dictionary size
   plus harvest from my best-available checkpoint.
4. **Patching validity without a head.** Zhang and Nanda (2024) on
   activation-patching best practices; Wang et al. (2023) on IOI circuit
   validation. *My question:* how do I keep path patching honest with no real
   head? *My answer:* report vacuous zeros as vacuous, keep the self-patch
   gate, never plot them.
5. **Warmup and curriculum as confounders.** *My question:* does a 1000-step
   warmup on a 2000-step shakedown suppress the phase change I am looking for?
   *My falsifier:* loss and K-comp curves with the 100-step override — if
   trajectories diverge before step 500, the schedule is load-bearing.

## Part V — My Documentation Requirements

| Artifact | Location | Trigger |
|---|---|---|
| This roadmap | `00_meta/86_micro-phase-86-from-stamps-to-record.md` | Session 0 |
| ADR-0028 row stamps + frozen invocation | `docs/adr/0028-continuum-ledger-23.md` | Each session |
| Shakedown manifest (probe path) | `results/probe_capstone_shakedown.json` | Sessions 1–2 |
| K-comp + vocab-offset verdict | `07_capstone/notes/mp-86-shakedown-verdict.md` | Session 4 |
| Portfolio pages, locked | `portfolio/projects/rung-{1..5}/index.md` | Session 3 |
| RESULTS + log + gate-debt truthing | `portfolio/RESULTS.md`, `00_meta/03_progress-log.md`, `checklists/gate-debt.md` | Session 3 |
| Paper diff or record memo | `portfolio/paper/main.tex` or dated memo | Session 4 |
| Teaching artifact + transcript | `notebooks/` | Session 5 |
| Release report | `00_meta/86_micro-phase-86-release-report.md` | Session 6 |

## Part VI — My Practical Exercises

- **Ex-1 · Shakedown drill.** One seed, 2k steps, warmup 100, checkpoint every
  500 with `--save-model`. I log task alternation, both losses, Fourier k_99,
  K-comp. *Falsifier:* a checkpoint that does not reload via `resume_step`
  fails the run.
- **Ex-2 · Probe discipline drill.** Every non-flagship run sets
  `--manifest-path` via `resolve_manifest_path`; I verify the flagship sha is
  unchanged after each probe. *Falsifier:* flagship bytes move.
- **Ex-3 · Tail drill.** Unequal-length RoundRobin loaders. *Falsifier:* the
  tail silently becomes single-task without a log line.
- **Ex-4 · Portfolio click-through.** For each rung page I click every number
  to its manifest tag, every tag to its file, every file to its command.
  *Falsifier:* a dangling ref or an orphan page blocks Session 6.
- **Ex-5 · W&B verdict drill.** `wandb login --verify` at Session 0 of
  execution. Live → dashboard; dead → Row 5 closes with one dated reason,
  never a silent skip.
- **Ex-6 · Vocab-offset decision drill.** If induction val stays near chance
  while modular learns, I implement the dedicated id-range offset test-first
  and re-run 500 steps. *Falsifier:* the offset changes nothing — the
  bottleneck is elsewhere.
- **Ex-7 · Four-register distillation.** I write my shakedown verdict as the
  paper's sentence, the annex's sentence, the 30-second spoken claim, and the
  5-minute teaching explanation a stranger can run.

## Part VII — My Strategic Tips and Architectural Best Practices

1. **A session stamps, it never re-decides.** My candidate set froze at
   Session 0; Sessions 1–6 execute.
2. **Freeze the invocation, not just the candidate set.** Warmup steps,
   `--save-model`, and `--manifest-path` are part of the frozen protocol.
3. **Negatives ship as loudly as positives.** My vacuous path-patching zeros
   and my dense SAE prove my positives were not cherry-picked.
4. **Toolchains pinned at Session 0, never discovered at Session 6.** `uv sync
   --frozen` plus `make reproduce-quick` before every session; `make
   verify-claims` after every numbers change.
5. **No full 20k by 3-seed launch until the 2k shakedown is GREEN.** Compute
   spent on an unshaken harness is drift.
6. **Every public number clicks back to disk.** No manifest tag, no claim. No
   transcript, no closure.
7. **Tests first, always — especially for interpretability interventions.**
   Self-patch-is-zero and ablate-all-collapses-to-baseline are the difference
   between a circuit claim and a plotting artifact.
8. **CI must pass before merging dev to main. Never bypass failed checks.**
   Conventional Commits with GPG sign-off; `pytest` plus `ruff check src/
   tests/` plus blocking `mypy` plus `verify-claims` green locally before every
   PR; body lines wrapped under 200 chars so the commitlint mirror never needs
   a pardon.

## Links

- [[85_micro-phase-85-from-stall-to-stamps|MP-85 · From Stall to Stamps]] — the phase this roadmap consumes
- [[07_capstone/notes/mp-78-session-capstone-checkpoint-fix|MP-78 checkpoint-fix session]] — my TDD precedent
- [[portfolio/RESULTS]] — my honesty ledger and per-rung numbers
- [[07_capstone/README|Capstone README]] — my experiment ladder and pipeline
- [[07_capstone/research-plan]] — my research plan, including the Rung 6 descoping rationale

**Written:** 2026-09-06
**Perspective:** my personal study notes, learning log, and portfolio showcase
**Status:** ACTIVE EXECUTION — Session 0 landed with live-pinned toolchains, Sessions 1–6 defined, no improvisation
