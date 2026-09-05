---
tags: [type/moc, phase/7, research/experiment, state/roadmap]
created: 2026-09-05
consumes: [ADR-0027]
---

# Micro-Phase 79 — Stabilize Then Showcase: My Next Dated Direction

> **STATUS: PRE-EXECUTION.** This is my personal study log and execution plan for MP-79, written from the MP-78 intake state. It consumes [[78_micro-phase-78-execution-roadmap|MP-78 · The Execution Roadmap]], the [[07_capstone/notes/mp-78-session-capstone-checkpoint-fix|MP-78 checkpoint-fix session note]], and the headline numbers in [[portfolio/RESULTS]]. The candidate set below freezes at Session 0 — I decide there, I never improvise later.

## Showcase Framing

If you have 30 seconds: I build a decoder-only transformer from scratch, then reverse-engineer the algorithms it learns. My strongest verified result is Rung 3's superposition phase transition. My most honest result is Rung 2's NO-GROK negative (val accuracy 1.0, Fourier dense at k_99 = 111/113). This phase I stabilize my capstone runner — three latent bugs fixed with tests first this week — and make my portfolio clickable, so every public number traces back to a manifest and a command.

## Part I — Where I Stand (My State Review)

I am on `dev`, clean, with 203 tests passing (199 + 4 new this week), `ruff` clean, blocking `mypy` clean on `src/results.py` + `src/experiments/runner.py`, and `verify-claims` at 0 with all six manifests on disk. See [[07_capstone/README|Capstone README]] for the full experiment ladder.

What I trust, in order: (1) Rung 3's phase transition — reproduced cleanly with its root cause understood. (2) Rung 2's dense negative — three seeds, dated 2026-08-11, with convergent small-P probes reproducing memorization-without-generalization. (3) Rung 1's fixed-vs-fresh comparison — a real, large, matched effect (fresh batches: 52.2% val accuracy vs fixed dataset's 0.05%), still below the induction-head detection threshold either way. (4) Rung 4's activation-patching signal (~0.20 recovery) — real but small, with path patching still unit-tested only. (5) Rung 5's SAE gap — synthetic FVE 0.9749 at L0 96.6/512, real-activation prose-only at 53% L0: an informative degradation, not a win. (6) My capstone runner — its `--save-model` crash fixed and pinned, its full 20k-step run not yet started.

## Part II — My Bottleneck Analysis (What I Fixed, What I Deferred)

### Fixed this week (test-first, GREEN locally)

1. **RoundRobin drained loader 0 first.** My `RoundRobinDataLoader.__next__` always tried iterator 0 first, yielding task order `[0,0,1,1]` — joint training with extra steps. I added a rotating cursor; batches now alternate `[0,1,0,1]`, pinned by `test_round_robin_alternates_tasks`. Code: `src/experiments/exp6_capstone.py` (`RoundRobinDataLoader`).
2. **SAE harvesting crashed on mixed batches.** My `harvest_activations` unpacked `for x, y in dataloader`, which raises `ValueError` on the 4-tuples my round-robin loader yields — the exact crash class as the checkpoint bug I fixed in MP-78, one call site over. It now accepts both shapes, pinned by `test_harvest_activations_accepts_round_robin_batches`.
3. **Probes could overwrite the flagship manifest.** My `--seeds` mode hardcoded `results/exp2_grokking.json`, and a P=67 probe already clobbered the P=113 flagship once (restored from git, per my session note). I extracted `build_parser()` and added `--manifest-path`; probes at non-flagship moduli must set it. Pinned by `tests/test_exp2_manifest_path.py`.
4. **Local residue removed.** The deleted Rung 6's PNG and a 0-byte neuron-ablation JSON are off my disk (both were gitignored build products, never tracked).

### Deferred honestly (known limitations, not silent debt)

- **K-composition in exp6 is a labeled placeholder** (appends `0.0`; the file says so). The real port from `exp1_induction_heads.py` is MP-79 Row 1 work, gated on the shakedown — I will not present placeholder zeros as measurements.
- **Shared embedding overlap** (modular ids `0..P-1` share rows with induction token ids; `pad_id = modulus` collides with a real induction token). Offsetting modular ids into a dedicated range is a semantic redesign — Row 1 scope, decided with its verdict, not patched blind.
- **Modular loss reads only `logits[:, 1]`** while 126 padded positions are ignored. Wasteful by design for now; the curriculum weighting (`modular_weight` / `induction_weight`) is the knob I will turn with data, not before it.

## Part III — My Roadmap, Step by Step (Sessions 0–6)

### My frozen candidate set (chosen at Session 0, never improvised)

| # | Candidate | Opens only if | Kill-date |
|---|---|---|---|
| 1 | **exp6 shakedown: 1 seed × 2k steps, all instrumentation live** | Always | S2 |
| 2 | **K-comp port + vocab-offset decision, dated** | Shakedown completes (Row 1) | S3 |
| 3 | **Portfolio repair: 5 pages clickable, figures resolved, ≥2 links each** | Always | S3 |
| 4 | **RESULTS + progress-log + gate-debt truthing** | Always | S3 |
| 5 | **W&B live dashboard, or dated close** | `wandb login` succeeds at S0 | S2, else close with reason |
| 6 | **Paper v-next decision (diff or "v20 is record" memo)** | New numbers from Rows 1–2 | S4 |
| 7 | **Teaching artifact v22 (shakedown edition) + stranger run** | Row 1 GREEN | S5 |
| 8 | **Release: merge, dev == main, home wired** | Rows 1–7 stamped | S6 |

### Session 0 (~1 h) — Gate truthing + toolchain pinning

I consume MP-78's release state, adjudicate all eight rows above, and pin my toolchains (`pdflatex`/`latexmk`, `wandb login --verify`, `hf auth status`, `.github/workflows/pages.yml` exists). I write my Ex-T32 execution memo. **Exit:** ADR-0028 eight rows stamped; toolchain status recorded; no row opens without its condition cited.

### Session 1 (~2 h) — Shakedown launch

I launch one capstone seed for 2000 steps (`checkpoint_every=500`, Fourier + K-comp every 500) with `--manifest-path results/probe_capstone_shakedown.json` discipline from the start. I verify the first 500 steps: loss decreasing on both tasks, task ids alternating in the log, checkpoints resuming. **Exit:** shakedown running; first checkpoint reloads via `resume_step`.

### Session 2 (~2 h) — Shakedown verdict + W&B verdict

I record modular/induction accuracy, Fourier k_99 trajectory, and max K-comp at 500/1000/1500/2000. W&B is either live with the shakedown group or Row 5 closes with one dated reason. **Exit:** Row 1 verdict stamped (extend / retune / stop); Row 5 stamped either way.

### Session 3 (~3 h) — Portfolio repair + ledger truthing

I fix every rung page: figure paths resolved or struck, manifest tags verified by `verify-claims`, ≥2 `[[links]]` each. I update the stale Rung-2 summary row and the Phase-6 gate cell in [[portfolio/RESULTS]], append the missing journal entries to `00_meta/03_progress-log.md`, and re-verify `checklists/gate-debt.md`. **Exit:** hostile click-through — every public number reaches a manifest and a command.

### Session 4 (~2 h) — Paper decision

New numbers exist → I draft the v-next diff from manifests. They do not → I write the dated "v20 is the record" memo. Either way `verify-claims` stays at 0. **Exit:** Row 6 stamped with a date.

### Session 5 (~3 h) — Teaching artifact v22 + stranger run

I build one runnable notebook on the shakedown checkpoint (Fourier → K-comp → patching with honest vacuous-zero reporting → SAE → literature → honest conclusion) and run it as a stranger on fresh Colab, committing the transcript. **Exit:** artifact shipped with transcript; four-register distillation written.

### Session 6 (~1 h) — Release

ADR-0028 at zero UNDECIDED rows; merge green locally and on GitHub; `dev == main`; home wired. **Exit:** the merge; my next dated direction.

## Part IV — My Deep-Dive Study Topics

1. **Why dense?** Varma et al. (2023), Lyu et al. (2024), Chughtai et al. (2023). *My question:* does joint modular-plus-induction training pressure my capstone toward modular sub-circuits or the same dense attractor? *My falsifier:* Fourier plus neuron ablation on shakedown checkpoints versus my P=113 dense baseline.
2. **Induction emergence at scale.** Olsson et al. (2022), Nanda and Jacobsen (2023). *My question:* does positional curriculum from addition accelerate Step 1 → Step 2? *My comparison:* K-comp trajectory at shakedown checkpoints versus my standard-scale run.
3. **The SAE sparsity gap.** Bricken et al. (2023), Cunningham et al. (2024). *My question:* is L0 96/512 against ~1 active ground-truth feature a dictionary-size artifact or an undertrained-residual artifact? *My sweep:* dictionary size plus harvest from my best-available checkpoint with explicit source-shape overrides.
4. **Patching validity without a head.** Zhang and Nanda (2024), Wang et al. (2023). *My question:* how do I keep path patching honest with no real head? *My answer:* report vacuous zeros as vacuous, keep the unit-test gate, never plot them as results.

## Part V — My Documentation Requirements

| Artifact | Location | Trigger |
|---|---|---|
| This roadmap | `00_meta/79_micro-phase-79-next-phase-roadmap.md` | Session 0 |
| ADR-0028 ledger | `docs/adr/0028-continuum-ledger-23.md` | Each session |
| Ex-T32 execution memo | Companion section of this file | Session 0 |
| Shakedown manifest (probe path) | `results/probe_capstone_shakedown.json` | Session 1–2 |
| Portfolio pages, repaired | `portfolio/projects/rung-{1..5}/index.md` | Session 3 |
| RESULTS + log + gate-debt truthing | `portfolio/RESULTS.md`, `00_meta/03_progress-log.md`, `checklists/gate-debt.md` | Session 3 |
| Paper diff or record memo | `portfolio/paper/main.tex` or dated memo | Session 4 |
| Teaching artifact v22 + transcript | `notebooks/` | Session 5 |
| Release report | `00_meta/79_micro-phase-79-release-report.md` | Session 6 |

## Part VI — My Practical Exercises

- **Ex-1 · Shakedown drill.** One seed, 2k steps, checkpoint every 500. Log task alternation, both losses, Fourier k_99, K-comp. *Falsifier:* a checkpoint that does not reload via `resume_step` fails the run.
- **Ex-2 · Probe discipline drill.** Every non-flagship run sets `--manifest-path`; I verify the flagship sha is unchanged after each probe. *Falsifier:* flagship bytes move, the probe protocol failed.
- **Ex-3 · Portfolio click-through.** For each rung page I click every number to its manifest tag, every tag to its file, every file to its command. *Falsifier:* a dangling figure ref or an orphan page (fewer than 2 links) blocks Session 6.
- **Ex-4 · W&B verdict drill.** `wandb login --verify` at Session 0. Live → dashboard with the shakedown group plus backfilled exp1/exp2 manifests. Dead → Row 5 closes with one dated reason, never a silent skip.
- **Ex-5 · Four-register distillation.** I write my shakedown verdict as the paper's sentence, the annex's sentence, the 30-second spoken claim, and the 5-minute teaching explanation with a worked toy a stranger can run. The gap between the last two is where my teaching leaks, and I measure it deliberately.

## Part VII — My Strategic Tips

1. **A session stamps, it never re-decides.** My candidate set froze at Session 0; Sessions 1–6 execute.
2. **Negatives ship as loudly as positives.** My vacuous path-patching zeros and my dense SAE are results, not embarrassments — they prove my positives were not cherry-picked.
3. **Toolchains pinned at Session 0, never discovered at Session 6.** A missing TeX toolchain or dead W&B login is a dated close-reason, not a crisis.
4. **No full 20k × 3-seed launch until the 2k shakedown is GREEN.** Compute spent on an unshaken harness is drift.
5. **Every public number clicks back to disk.** No manifest tag, no claim. No transcript, no closure.
6. **Tests first, always.** This week's three fixes worked because RED came first — I repeat that for the K-comp port and the vocab offset.

## Links

- [[78_micro-phase-78-execution-roadmap|MP-78 · The Execution Roadmap]] — the phase this roadmap consumes
- [[07_capstone/notes/mp-78-session-capstone-checkpoint-fix|MP-78 checkpoint-fix session]] — the TDD precedent (checkpoint crash, probe reproduction)
- [[portfolio/RESULTS]] — my honesty ledger and per-rung numbers
- [[07_capstone/README|Capstone README]] — my experiment ladder and pipeline
- [[07_capstone/research-plan]] — my research plan, including the Rung 6 descoping rationale

**Written:** 2026-09-05
**Perspective:** my personal study notes, learning log, and portfolio showcase
**Status:** ready for Session 0 — candidate set proposed, conditions explicit, no improvisation.
