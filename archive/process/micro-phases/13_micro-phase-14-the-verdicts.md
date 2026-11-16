---
tags: [type/moc, phase/6, phase/7, research/experiment, state/review]
created: 2026-08-08
---

# Micro-Phase 14 — The Flagships, Executed (roadmap)

Written before the runs, as a personal learning log and a public record.
Builds on [[12_micro-phase-13-flagships-landed]] — its Step 0 has shipped (verified
against the repository, not memory); its Steps 1–7 have not.

## Where this phase starts (state review, verified against the repo)

Checked `git status` / `git log` / the manifests before writing a single claim — the
standing lesson of MP-12 is that memory is not evidence.

- **MP-13 Step 0 is shipped** (`c171b86` → `500c2b0`, merged to `main` via PR #38):
  the platform-dependent test now stringifies args with `os.fspath` and asserts
  neutrally on both OS families; the 12 curated figures are committed in
  `portfolio/figures/`; `docs/agents/` is tracked; the tree is clean and `dev == main`.
- **Rung 1 `--standard` (~17–20 h CPU): never launched.** `results/exp1_induction_heads.json`
  holds only the tiny 150-epoch multi-seed run; `checkpoints/` holds only the kill-drill
  artifacts. No standard-scale verdict exists.
- **P=113 × 3 seeds (Colab GPU): never launched.** Rung 2 has **no manifest ever
  produced**; its RESULTS section is still prose-only.
- **Rung 3 full-scale geometry: never re-run.** The canonical claim (gaps 70.2–73.8°) is
  backed by the pre-death full-scale record; the on-disk regeneration is a `--quick`
  stand-in (70.7–73.6°).
- **Rung 4/5 cascade: blocked as designed.** Path patching is still validated only by
  unit tests; the real-activation SAE comparison (99.97% FVE / 53% L0) is still
  "informative, not conclusive" without a head-bearing checkpoint; `exp5` also has no
  manifest.
- **Clean-clone gate:** `scripts/clean_clone_check.sh` exists, never run end-to-end.
- **Paper:** `portfolio/paper/main.tex` is still scaffold-only — zero prose.

### Bottleneck diagnosis (ranked by what blocks what)

1. **The two verdicts are the critical path.** Every downstream deliverable (R4 end-to-end,
   R5 re-test, Phase-6 gate proof, first paper prose) waits on "does a real head form at
   standard scale?" and "does P=113 actually grok?"
2. **A genuine external dependency:** P=113 needs a Colab session only I can run — the only
   item in this repo that cannot be advanced by the repo itself.
3. **Two knowledge gaps the drills admitted:** cross-process BLAS determinism was never
   tested under CPU contention; the figure-generator death class (silent, buffered,
   untraced) was never drilled.
4. **Manifest coverage debt:** exp2 and exp5 have never produced a manifest; they are the
   only sections `verify-claims` still flags — correctly.

This phase launches both flagships in the same wall-clock window (local CPU + Colab async);
every step after them is conditional, named, and gated.

## 2. Deep-dive study and research topics

1. **Nanda et al., ICLR 2023 — re-read with weights in hand.** Study it as a recipe for
   reading my own model: why the Fourier progress measure is `Freq^k`-sparsity on the MLP
   input, why weight decay is the dial that moves the model into the Fourier regime, and
   the embedding-normalization detail I deviated from (named suspect #1 if P=113 fails).
2. **Power et al. 2022 hyperparameter landscape.** Weight decay is the grokking dial; LR
   and optimizer are supports. Keep the landscape in view when interpreting a negative.
3. **Zhang & Nanda, "Towards Best Practices of Activation Patching" (ICLR 2024)** —
   *before* Step 4's first real use of `run_path_patching_to_logits()`. This repo has
   committed that paper's site/metric errors twice on activation patching; path
   patching's first real run must not be the third.
4. **Olsson et al. 2022, the K-composition curriculum.** Which ingredient (d_model?
   seq_len? vocab? loss?) most plausibly gates head formation at my scale — so the "how
   far" figure can be interrogated, not just rendered.
5. **Cross-process float determinism, the untested hypothesis.** PyTorch reproducibility
   docs (`torch.use_deterministic_algorithms`, seeded generators, BLAS thread counts) plus
   a deliberate under-load drill. Closes the one gap the kill drill honestly logged.
6. **Process supervision as a research skill.** Heartbeat logs, watchdog restart
   semantics, `python -u` / `PYTHONUNBUFFERED` — the silent-death class that killed two
   real full-scale jobs is a buffering bug plus a supervision gap, both fixable with a
   small driver script.
7. **GPU session durability.** Drive checkpointing, keep-alive, and `pin_colab_run.py`'s
   SHA contract — the GPU-side analogue of the kill drill, applied this time.
8. **Evidence-ordered paper craft** (Pineau et al. reproducibility checklist): Methods →
   strongest result (R3) → each manifest-backed rung, every paragraph tied to a file.
   No sentence whose evidence isn't already in `RESULTS.md`.

## 3. Documentation requirements

- **Progress log:** one dated entry per session; raw pass/fail recorded *before* any
  interpretation — including failures.
- **New notes:** a *figure supervision + watchdog* note under `06_production_ai/notes/`
  (now a standing pattern, not a one-off); a *Fourier progress measures* note once P=113
  lands (the decomposition and my hand-verified frequency, not the plot default).
- **Updated notes:** `04_nlp_and_transformers/notes/induction-heads.md` gets the Step 1
  verdict either way; `path-patching.md` gets real end-to-end numbers for the first time;
  the grokking note gets the P=113 manifests.
- **Skill tree:** flips only with proofs — *induction-head reproduction* (confirmed +
  causally verified head), *grokking reproduction* (P=113 manifests), and a new line for
  *reproducible long-job durability* once the watchdog (Step 3) and the contention drill
  (Exercise 7) are real, checked patterns.
- **Proofs:** `reproducible-from-clean-clone` written from the *actual transcript*; the
  under-load kill-drill entry appended to the existing durability proof.
- **RESULTS.md:** reconcile every new manifest; fold the Rung 2/5 numbers in from
  manifests (not prose); ledger entry including this phase's own missteps.
- **Vault conventions:** every new artifact carries the two-link minimum and proper tags;
  nothing ships with a dangling figure citation.

## 4. Practical exercises and hands-on challenges

1. **Challenge — the supervised R1 run.** The phase in essence: heartbeat, a deliberate
   mid-run `Stop-Process -Force` + `--resume` at realistic scale (no longer a 30-epoch
   toy), and a verdict: confirmed head, causally verified — or the committed
   K-composition "how far" figure. Silence is failure.
2. **Challenge — P=113 × 3 seeds on Colab.** Launch, monitor, Drive-checkpoint, download,
   pin via `pin_colab_run.py`, verify, `RESULTS.md` entry. Success targets pre-decided
   before launch: mean final val acc > 0.9, generalization epoch < 5000,
   `k_99_percent` ∈ 10–20.
3. **Challenge — under-load kill drill (the untested hypothesis).** Re-run the kill drill
   while a second CPU-heavy process contends; diff against the reference. Either
   bit-identical → hypothesis retired; or a measured divergence class → recorded honest
   residual risk.
4. **Challenge — the R3 watchdog regeneration.** Driver script (heartbeat +
   abnormal-exit restart), full-scale geometry, pentagon confirmed at the canonical
   budget, documented as reusable infra.
5. **Exercise — one Fourier product, verified by hand.** After a grokked P=113, take the
   top-frequency component, write the trig expression it implies for `logits[a+b]` from
   the embeddings by hand, verify against the trained weights — proof at the weight
   level, not the plot level.
6. **Challenge — the clean-close gate.** `scripts/clean_clone_check.sh` end to end, proof
   written from the transcript; any required manual step is a failed gate.
7. **Exercise — score the MP-9/MP-10 predictions** against what actually happened. Costs
   nothing but honesty, and is exactly the calibration drill that catches a roadmap
   drifting from its own plan.
8. **Habit — the three-question self-audit** before every commit this phase: *figure on
   disk? tracked in git? bound to a manifest?* — the same questions `verify-claims` asks,
   asked one commit earlier.

## 5. Strategic tips and architectural best practices

- **Verify state against the repository before believing any narrative about it.** One
  `git diff origin/dev` collapsed the supposed MP-12 crisis into a real but small fork;
  this note opened the same way.
- **A supervised "no, here are the diagnostics" is a stronger deliverable than a silent
  vanished run.** Supervision is the ducting that turns compute-hours into evidence.
- **Quick scale is a smoke test, never a result.** It survives for CI and one-variable
  exploration only; it never enters `RESULTS.md` as the canonical number.
- **Never trust an unattended long job with a path that hasn't survived a real death.**
  Training checkpoints are drilled; figure generation and GPU sessions get the same
  treatment this phase, in the same vault.
- **Pre-decide budgets and success targets before the launch.** A genuinely negative
  result is evidence; deciding thresholds after seeing the numbers is p-hacking.
- **When a number looks too clean, re-derive one of them by hand** before believing it —
  the first real activation-patching numbers are the prime suspect.
- **One variable per experiment, one ledger entry per phase.** A negative with named
  suspects always beats a silent gap.
- **Run both flagships in the same wall-clock window.** Local CPU (~17–20 h) and Colab
  GPU (minutes × 3 seeds) are independent machines; the rest of the phase waits on both.
- **The merge closes only on green CI.** `dev` green → `dev → main` clean →
  post-merge tree verified.

## 6. Step-by-step execution roadmap

```
Step 0: Pre-flight (10 min) — verify MP-13 Step 0 is shipped: platform-neutral
        test green on this machine, ruff + blocking mypy + ≥185 tests, CI green on dev
          ┌──────────────────────────────┴───────────────────────────────┐
          ▼                                                               ▼
Step 1: Stably supervised R1 --standard     Step 2: P=113 x3 seeds on Colab GPU,
        local CPU, ~17-20 h,                 async, Drive-checkpointed, SHA-pinned,
        heartbeat + mid-run revive drill     manual launch only, verdicts in-flight
          └──────────────────────────────┬───────────────────────────────┘
                                         ▼
Step 3: R3 full-scale geometry under a real watchdog (silent-death class becomes
        reusable infra: python -u, heartbeat, restart-on-abnormal-exit)
                                         ▼
Step 4: The cascade — only if a head formed:
        R4 end-to-end (activation + path patching + head ablation on the real head,
        skeptical-number protocol); R5 re-test on the head-bearing checkpoint
        (new manifest either way); R2 manifest + Fourier figures
Step 5: Clean-clone gate end-to-end, proof written from the transcript
                                         ▼
Step 6: Paper prose in evidence order — Methods, then Rung 3 (strongest), then each
        rung whose manifest landed; nothing beyond RESULTS.md is written
                                         ▼
Step 7: Reconcile RESULTS.md; verify-claims to zero; ledger entry; merge dev→main
        on green CI; archive this roadmap with its deviations noted
```

## 7. Gate criteria

1. Pre-flight green locally (≥185 tests, ruff, blocking mypy) and CI green on `dev`.
2. R1 `--standard`: a verdict that is **not silence** — confirmed + causally verified
   head, or the committed "how far" figure. Both are results.
3. P=113: ≥1 grokked seed, manifests pinned, Fourier figures committed — or an honest
   negative with named suspects.
4. R3: full-scale geometry at the canonical budget, under the watchdog.
5. Clean-clone gate run end-to-end, once, transcript-based proof.
6. R4 end-to-end on a real head (or the gap named in the ledger, never silently closed);
   R5 re-test with a real manifest.
7. Paper prose in evidence order; `verify-claims` at zero unexpected problems;
   `dev → main` on green CI; tree clean post-merge.

## Links

- [[12_micro-phase-13-flagships-landed]] — the phase this executes (Step 0 already landed).
- [[11_micro-phase-12-resilient-flagship-run]] — the evidence gate and kill drill this
  phase extends to GPU sessions and figure gates.
- [[10_micro-phase-11-flagship-run]] — K-composition detector and probe verdicts that
  Step 1 goes to verify.
- [[09_micro-phase-10-evidence-run]] — the run instruments that make Step 2 safe to launch.
- [[04_nlp_and_transformers/notes/induction-heads]] — Rung 1's working note, updated by
  Step 1's verdict.
- [[portfolio/RESULTS]] — the ledger this phase must change.
- [[06_production_ai/proofs/kill-drill-checkpoint-resume]] — the durability proof this
  phase extends to the GPU and to figure generation.
- [[06_production_ai/proofs/reproducible-from-clean-clone]] — the Phase 6 gate proof,
  still waiting for its first real transcript.