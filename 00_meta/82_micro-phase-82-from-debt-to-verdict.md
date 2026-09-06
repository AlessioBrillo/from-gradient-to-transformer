---
tags: [type/moc, phase/7, research/experiment, state/roadmap]
created: 2026-09-06
consumes: [ADR-0028]
---

# Micro-Phase 82 — From Debt to Verdict: My Next Dated Direction

> **STATUS: ACTIVE EXECUTION.** This is my personal study log and execution plan for MP-82, written from the MP-81 intake state. It consumes [[81_micro-phase-81-from-shakedown-to-evidence|MP-81 · From Shakedown to Evidence]], ADR-0028 (OPEN, Rows 1/3/4/5 PENDING, rest GATED), and the headline numbers in [[portfolio/RESULTS]]. The candidate set below freezes at Session 0 — I decide there, I never improvise later.

## Showcase Framing

If you have 30 seconds: I build a decoder-only transformer from scratch, then reverse-engineer the algorithms it learns. My strongest verified result is Rung 3's superposition phase transition. My most honest result is Rung 2's NO-GROK negative (val accuracy 1.0, Fourier dense at k_99 = 111/113). This phase I stop planning the shakedown and run it — one seed by 2k steps with real K-composition and probe-safe manifests — and I close the portfolio click-through, so every public number traces back to a manifest and a command.

## Part I — Where I Stand (My State Review)

I am on `dev`, clean, reconciled with `main` through PR #132. My verified baseline at Session 0:

- **Tests:** 208 passing, `ruff check src/ tests/` clean.
- **Types:** blocking `mypy --strict` clean on `src/results.py` + `src/experiments/runner.py`; full-tree strict debt remains tracked follow-up, not rushed.
- **Claims:** `verify-claims` at 0, all six manifests on disk (`results/exp{1,2,3,4,5}_*.json` + `results/exp6_capstone.json`). See [[07_capstone/README|Capstone README]] for the full experiment ladder.
- **Ledger:** ADR-0028 OPEN with eight rows (R1 shakedown PENDING, R3/R4/R5 portfolio-and-truthing PENDING, rest GATED). MP-74 GPU grokking still IN_PROGRESS (Colab launched 2026-08-24, no manifest downloaded yet); extended induction 10k NOT_STARTED; clean-clone proof GREEN 2026-08-27; neuron ablation COMPLETE.

What I trust, in order: (1) Rung 3's phase transition — reproduced cleanly with its root cause understood. (2) Rung 2's dense negative — three seeds, dated 2026-08-11. (3) Rung 1's fixed-vs-fresh comparison — fresh batches at 52.2% val accuracy versus fixed dataset at 0.05%, still below the induction-head detection threshold either way. (4) Rung 4's activation-patching signal (~0.20 recovery) — real but small, with path patching still unit-tested only. (5) Rung 5's SAE gap — synthetic FVE 0.9749 at L0 96.6/512, real-activation prose-only at 99.97% FVE but 53% L0: an informative degradation, not a win.
(6) My capstone runner — its RoundRobin alternation, harvester 4-tuple crash, `--manifest-path` guardrail, real K-comp port, plus new `--steps`/`--warmup-steps` overrides and `resolve_manifest_path` contract landed test-first; its full 2k-step shakedown not yet started, and my `results/exp6_capstone.json` is still smoke-scale (P=17, 100 steps).

## Part II — My Bottleneck Analysis (What I Fixed, What I Deferred)

### Fixed test-first (GREEN locally, on disk at Session 0)

1. **Shakedown overrides were config edits.** My shakedown needed 2000 steps and 100 warmup steps against a 20000-step flagship config with 1000 warmup steps — editing the YAML risked the flagship. I added `--steps` and `--warmup-steps` CLI overrides plus `resolve_manifest_path()` extraction, pinned by `tests/test_exp6_manifest_path.py`. Code: `src/experiments/exp6_capstone.py`.
2. **RoundRobin tail was unasserted.** My unequal-length loader test covered only 2+2 equal batches; the real mixed loader has unequal modular/induction lengths, so the tail is single-task. I added the unequal-tail test pinning total count and explicit `[0,1,0,0]` tail. Pinned by `test_round_robin_unequal_tail_does_not_silently_single_task`.
3. **Portfolio prose drifted from RESULTS.** My rung-3 page said 14–16/20 where RESULTS says 16/20; my rung-1 page cited a 3k-epoch run that does not exist; three existing PNGs were unlinked from their rung pages. I fixed the two prose cells and linked `exp2_progress_measures.png`, `exp3_phase_change.png`, and `exp3_feature_geometry.png` with manifest tags.
4. **Prior guardrails stand:** RoundRobin alternation, harvester 4-tuple unpack, `--manifest-path` probe guardrail, real K-comp port with `_vacuous` markers.

### Deferred honestly (known limitations, not silent debt)

- **Shared embedding overlap** (modular ids `0..P-1` share rows with induction token ids; `pad_id = modulus` collides with a real induction token). Offsetting modular ids into a dedicated range is a semantic redesign — Row 2 scope, decided with shakedown data at Session 4, not patched blind.
- **Modular loss reads only `logits[:, 1]`** while 126 padded positions are ignored. Wasteful by design for now; the curriculum weighting (`modular_weight` / `induction_weight`) is the knob I will turn with data, not before it.
- **Warmup choice frozen at 100 for the shakedown** (vs 1000 flagship): the 2k shakedown must observe early phase-change dynamics; a 50%-of-horizon warmup would mask them. If the start is too noisy I record it as a dated fact and adjust, never silently.
- **Toolchains:** no `pdflatex`/`latexmk` locally (paper PDF stays scaffold-only), `wandb` installed but login unverified, `hf` installed but no Space exists, `pages.yml` exists but the portfolio deploy is unrehearsed.

### New risks I am watching

1. **Planning without execution is now my top bottleneck.** I hold 81 micro-phase files and three consecutive PRE-EXECUTION roadmaps (MP-78, MP-79, MP-80). My countermeasure: no new roadmap until ADR-0028 hits zero unstamped rows — this phase executes rows, it does not propose candidates.
2. **GPU verdict still missing.** My primary flagship's scale follow-up (P=113 by 3 seeds on Colab) is IN_PROGRESS with no downloaded manifest. I do not let it silently gate my CPU shakedown — Row 1 runs regardless; the GPU manifest is consumed when it lands, not waited on.
3. **Gate-debt cannot sign off as written.** Ten of twelve cells block Session 8 (2 PENDING, 4 GATED which is not a sign-off state, 4 LAUNCHED without transcripts). Session 3 converts every cell to LAUNCHED-with-transcript or CLOSED-with-one-reason.
4. **Path patching without a head.** Reporting vacuous zeros as results would repeat the exact error class my 2026-08-01 Validity Pass fixed. I report them as vacuous, keep the unit-test gate, never plot them.

## Part III — My Roadmap, Step by Step (Sessions 0–6)

### My frozen candidate set (chosen at Session 0, never improvised)

| # | Candidate | Opens only if | Kill-date |
|---|---|---|---|
| 1 | **exp6 shakedown: 1 seed by 2k steps, all instrumentation live** | Always | S2 |
| 2 | **K-comp validation + vocab-offset decision, dated** | Shakedown completes (Row 1) | S3 |
| 3 | **Portfolio repair lock-in: unlinked figures linked, prose drift fixed** | Always | S3 |
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

I consume MP-81's intake state, adjudicate all eight rows above, freeze the invocation, and pin my toolchains. **Exit:** ADR-0028 eight rows stamped; invocation frozen; no row opens without its condition cited.

### Session 1 (~2 h) — Shakedown launch

I launch one capstone seed per the frozen invocation. I verify the first 500 steps: loss decreasing on both tasks, task ids alternating in the log, checkpoints resuming via `resume_step`. **Exit:** shakedown running; first checkpoint reloads.

### Session 2 (~2 h) — Shakedown verdict + W&B verdict

I record modular/induction accuracy, Fourier k_99 trajectory, and max K-comp at 500/1000/1500/2000. W&B is either live with the shakedown group or Row 5 closes with one dated reason. **Exit:** Row 1 verdict stamped (extend / retune / stop); Row 5 stamped either way.

### Session 3 (~3 h) — Portfolio repair + ledger truthing

I lock in every rung page, update RESULTS and the journal, and convert every gate-debt cell to LAUNCHED-with-transcript or CLOSED-with-one-reason. `verify-claims` stays at 0. **Exit:** hostile click-through — every public number reaches a manifest and a command.

### Session 4 (~2 h) — Paper decision + vocab-offset decision

New numbers exist → I draft the v-next diff from manifests. They do not → I write the dated "v20 is the record" memo. In the same sitting I decide the vocab-offset redesign with shakedown data. **Exit:** Rows 2 and 6 stamped with a date.

### Session 5 (~3 h) — Teaching artifact + stranger run

I build one runnable notebook on the shakedown checkpoint (Fourier → K-comp → patching with honest vacuous-zero reporting → SAE → literature → honest conclusion) and run it as a stranger on fresh Colab, committing the transcript. **Exit:** artifact shipped with transcript; four-register distillation written.

### Session 6 (~1 h) — Release

ADR-0028 at zero unstamped rows; merge green locally and on GitHub; `dev == main`; home wired. **Exit:** the merge; my next dated direction.

## Part IV — My Deep-Dive Study Topics

1. **Why dense? Grokking vs. dense memorization-generalization.** Varma et al. (2023) on grokking vs. memorization dynamics; Lyu et al. (2024) on scale and data-fraction effects; Chughtai et al. (2023) on toy-model grokking constructions. *My question:* does joint modular-plus-induction training pressure my capstone toward modular sub-circuits or the same dense attractor I measured at P=113? *My falsifier:* Fourier plus neuron ablation on shakedown checkpoints versus my P=113 dense baseline.
2. **Induction emergence at scale: Step 1 to Step 2.** Olsson et al. (2022) on induction heads and in-context learning; Nanda and Jacobsen (2023) on K-composition phase changes. *My question:* does joint training accelerate duplicate-detection into composition? *My comparison:* K-comp trajectory at shakedown checkpoints versus my fresh-batches run (peak diag+1 0.145, still rising at epoch 800).
3. **The SAE sparsity gap: dictionary size vs. residual quality.** Bricken et al. (2023) on monosemanticity and the pre-encoder bias; Cunningham et al. (2024) on SAE scaling. *My question:* is L0 96/512 a dictionary-size artifact or an undertrained-residual artifact? *My sweep:* dictionary size plus harvest from my best-available checkpoint.
4. **Patching validity without a head.** Zhang and Nanda (2024) on activation-patching best practices; Wang et al. (2023) on IOI circuit validation. *My question:* how do I keep path patching honest with no real head? *My answer:* report vacuous zeros as vacuous, keep the self-patch-is-zero gate, never plot them.
5. **Warmup and curriculum as confounders.** *My question:* does a 1000-step warmup on a 2000-step shakedown suppress the phase change I am looking for? *My falsifier:* loss and K-comp curves with the 100-step override — if trajectories diverge before step 500, the schedule is load-bearing.

## Part V — My Documentation Requirements

| Artifact | Location | Trigger |
|---|---|---|
| This roadmap | `00_meta/82_micro-phase-82-from-debt-to-verdict.md` | Session 0 |
| ADR-0028 row stamps + frozen invocation | `docs/adr/0028-continuum-ledger-23.md` | Each session |
| Shakedown manifest (probe path) | `results/probe_capstone_shakedown.json` | Sessions 1–2 |
| K-comp + vocab-offset verdict | `07_capstone/notes/mp-82-shakedown-verdict.md` | Session 4 |
| Portfolio pages, locked | `portfolio/projects/rung-{1..5}/index.md` | Session 3 |
| RESULTS + log + gate-debt truthing | `portfolio/RESULTS.md`, `00_meta/03_progress-log.md`, `checklists/gate-debt.md` | Session 3 |
| Paper diff or record memo | `portfolio/paper/main.tex` or dated memo | Session 4 |
| Teaching artifact + transcript | `notebooks/` | Session 5 |
| Release report | `00_meta/82_micro-phase-82-release-report.md` | Session 6 |

## Part VI — My Practical Exercises

- **Ex-1 · Shakedown drill.** One seed, 2k steps, warmup 100, checkpoint every 500 with `--save-model`. I log task alternation, both losses, Fourier k_99, K-comp. *Falsifier:* a checkpoint that does not reload via `resume_step` fails the run.
- **Ex-2 · Probe discipline drill.** Every non-flagship run sets `--manifest-path` via `resolve_manifest_path`; I verify the flagship sha is unchanged after each probe. *Falsifier:* flagship bytes move.
- **Ex-3 · Tail drill.** Unequal-length RoundRobin loaders. *Falsifier:* the tail silently becomes single-task without a log line.
- **Ex-4 · Portfolio click-through.** For each rung page I click every number to its manifest tag, every tag to its file, every file to its command. *Falsifier:* a dangling ref or an orphan page blocks Session 6.
- **Ex-5 · W&B verdict drill.** `wandb login --verify` at Session 0. Live → dashboard; dead → Row 5 closes with one dated reason, never a silent skip.
- **Ex-6 · Vocab-offset decision drill.** If induction val stays near chance while modular learns, I implement the dedicated id-range offset test-first and re-run 500 steps. *Falsifier:* the offset changes nothing — the bottleneck is elsewhere.
- **Ex-7 · Four-register distillation.** I write my shakedown verdict as the paper's sentence, the annex's sentence, the 30-second spoken claim, and the 5-minute teaching explanation a stranger can run.

## Part VII — My Strategic Tips and Architectural Best Practices

1. **A session stamps, it never re-decides.** My candidate set froze at Session 0; Sessions 1–6 execute.
2. **Freeze the invocation, not just the candidate set.** Warmup steps, `--save-model`, and `--manifest-path` are part of the frozen protocol.
3. **Negatives ship as loudly as positives.** My vacuous path-patching zeros and my dense SAE prove my positives were not cherry-picked.
4. **Toolchains pinned at Session 0, never discovered at Session 6.** `uv sync --frozen` plus `make reproduce-quick` before every session; `make verify-claims` after every numbers change.
5. **No full 20k by 3-seed launch until the 2k shakedown is GREEN.** Compute spent on an unshaken harness is drift.
6. **Every public number clicks back to disk.** No manifest tag, no claim. No transcript, no closure.
7. **Tests first, always — especially for interpretability interventions.** Self-patch-is-zero and ablate-all-collapses-to-baseline are the difference between a circuit claim and a plotting artifact.
8. **CI must pass before merging dev to main. Never bypass failed checks.** Conventional Commits with GPG sign-off; `pytest` plus `ruff check src/ tests/` plus blocking `mypy` plus `verify-claims` green locally before every PR.

## Links

- [[81_micro-phase-81-from-shakedown-to-evidence|MP-81 · From Shakedown to Evidence]] — the phase this roadmap consumes
- [[07_capstone/notes/mp-78-session-capstone-checkpoint-fix|MP-78 checkpoint-fix session]] — my TDD precedent
- [[portfolio/RESULTS]] — my honesty ledger and per-rung numbers
- [[07_capstone/README|Capstone README]] — my experiment ladder and pipeline
- [[07_capstone/research-plan]] — my research plan, including the Rung 6 descoping rationale

**Written:** 2026-09-06
**Perspective:** my personal study notes, learning log, and portfolio showcase
**Status:** ACTIVE EXECUTION — candidate set frozen, Sessions 0–6 defined, no improvisation
