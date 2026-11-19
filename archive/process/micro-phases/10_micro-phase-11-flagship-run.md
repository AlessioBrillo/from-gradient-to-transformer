---
tags: [type/moc, phase/6, phase/7, research/experiment, state/review]
created: 2026-08-06
---

# Micro-Phase 11 — The Flagship Run (roadmap + record)

Micro-Phase 10 left all the instruments built and nothing pulled: the P=113 grokking run,
the standard-scale Rung 1 run, and the Rung 4/5 cascade were instrumented and unpulled.
This phase pulls the triggers — on this machine where the runs fit, and on Colab for the
flagship — and converts the instruments into evidence. Written from my perspective as a
learning log, with the failed hypotheses recorded as loudly as the confirmed ones.

## Where this started (state review, 2026-08-06)

- **Rung 2 (primary flagship)** — code, notebook, progress measures, and the CPU de-risk
  probe all exist; the P=113 ×3-seed run still needs GPU hours I do not have here.
- **Rung 1 (the domino)** — the standard-scale fresh-batches config is pinned
  (`--standard`); never executed. No induction head has ever formed in any run.
- **The K-composition diagnostic was missing.** Micro-Phase 9's exercise #1 (the "how far
  did the model get" instrument, per Nanda & Jacobsen) was never built — if no head forms,
  there is no measurement, only a blind re-run. This phase builds it first.
- **Rung 4/5 cascade** — path patching is still validated only by unit tests; the SAE
  real-vs-synthetic re-test still needs a head-bearing checkpoint.
- **Rung 3** — phase transition and pentagon sweep confirmed; the canonical small case
  (5 features → 2 dims, Elhage's actual pentagon figure) is still unverified.
- **Infra** — MP10 merged to `main` (PR #34); manifests for exp2/exp5 do not exist yet;
  the clean-clone gate has never run end to end; the paper scaffold still has zero prose.
- **MP10's own record is slightly stale** (it lists "pending: push/CI/merge" which have
  since happened) — corrected in the progress log entry for this phase.

## Bottleneck analysis — the dependency chain

```
 Step 0: K-composition detector (MISSING instrument, build first)
 Step 1: P=59 probe on CPU ─────────► Step 2: P=113 grokking ×3 (Colab GPU, async)
                                          │            fold Rung 1 --standard into the session
                                          ▼                    │ (or overnight CPU fallback)
                           head formed? ──no──► K-composition diagnostic figure (Step 0)
                                          │yes
                       Rung 4 path-patching E2E + Rung 5 SAE re-test on the head ckpt
                                          ▼
             clean-clone gate (Phase 6 green) → paper in evidence order → merge
```

Facts that shape the sequencing:

1. **Rung 1 is the highest-leverage experiment** — its verdict resolves three open items
   at once (Rung 1 headline, Rung 4's E2E validation gap, Rung 5's honest re-test).
   Its verdict is only *measurable* if Step 0 exists first.
2. **GPU work is async** — launch Colab before any CPU work and fold Rung 1 standard into
   the same session (MP9's advice: amortize session spin-up). If no GPU session is
   available, Rung 1 standard runs overnight on this machine.
3. **The probe de-risks the recipe** — one bad P=113 run costs a day; a P=59 probe costs
   30 CPU minutes and tells me whether the canonical recipe groks at all.

## Steps

### Step 0 — K-composition detector (the missing instrument)

Built and committed this phase: per-head attention-pattern diagnostics for the three-step
induction path (Nanda & Jacobsen 2023): the L0 duplicate-token head (diag+1 attention),
the L1 K-composition step (does L1 attend to the position L0 attended?), and the final
induction-head pattern. Falsification tests: must detect a hand-constructed chain on
synthetic attention stacks, must return null on random patterns. Module held to the
blocking mypy allowlist.

### Step 1 — P=59 probe on CPU

`make reproduce-grokking-probe`. Three readings: groks → recipe validated; train high but
val flat at 1500 epochs → more epochs or weight-decay tuning, cheap on CPU; no
memorization → LR/scale problem. Read the Fourier-sparsity/weight-norm progress curves,
not just accuracy. **Verdict recorded in this file and the progress log.**

### Step 2 — The flagships

- **P=113 ×3 seeds on Colab** via `notebooks/colab_grokking_full_run.ipynb`, results
  pinned via `scripts/pin_colab_run.py` (exercises that path end-to-end), Fourier +
  frequency-ablation figures committed.
- **Rung 1 standard-scale fresh-batches** — folded into the Colab session if available,
  otherwise overnight on this machine. Verdict: head confirmed + causally verified, or the
  K-composition diagnostic showing exactly how far.

### Step 3 — While the GPU runs (CPU work)

1. Rung 3 small-case pentagon: 5 features → 2 dims, Gram matrix check, Elhage's figure.
2. 1-layer headless lower bound (`reproduce-induction-1layer`): a 1-layer model cannot do
   K-composition, so its diag+1 mass is the matched floor the 2-layer result must beat.
3. Paper scaffold: Methods + Rung 3 Results in evidence order.
4. Mypy ratchet: pay down `src/models/` toward the blocking allowlist.

### Step 4 — The cascade (conditional on a head)

Rung 4 E2E at the named (layer, head): activation patching, path patching, head ablation.
Rung 5 re-test: `--activations-from` on the head-bearing checkpoint; compare L0/FVE
against the dense 53%-L0 reading. If no head forms: the Step 0 diagnostic is the
deliverable; the phase succeeds by knowing, not by forcing a positive.

### Step 5 — Manifest discipline

All multi-seed manifests re-baselined at a committed HEAD (`git_dirty: false`),
`make verify-claims` green, RESULTS.md reconciled row by row.

### Step 6 — Clean-clone gate (Phase 6 completion)

`scripts/clean_clone_check.sh` end to end, transcript captured, the
`reproducible-from-clean-clone` proof written from the actual output.

### Step 7 — Paper + publication figures

Headline figures rebuilt in a consistent publication style, regenerable via
`make reproduce`; paper extended in evidence order, grokking last.

### Step 8 — Close the phase

One honesty-ledger entry whatever the outcome. Tests ≥168, CI green on `dev`, merge
`dev → main`, roadmap archived in the progress log with deviations noted.

## Deep-dive study and research topics

1. **Nanda & Jacobsen, "Attention as a Step Towards the Emergence of the Induction Head"
   (2023)** — the three-step decomposition is the spec for Step 0's detector.
2. **Olsson et al. §3–4, re-read with calibration in mind** — the regimes under which
   induction heads form; the `--standard` config must be checked against them before GPU
   hours are spent.
3. **Nanda et al., "Progress Measures for Grokking" (ICLR 2023)** — reading the three
   phases off the probe's curves (Fourier sparsity dense → dropping; weight norm falling
   only at cleanup).
4. **Zhang & Nanda, "Towards Best Practices of Activation Patching" (ICLR 2024)** —
   re-read before Step 4: patch-site choice, layernorm caveats, aggregation.
5. **Elhage et al., "Toy Models of Superposition" §3–4** — pentagon geometry and the
   Gram matrix, for the small-case check (hand-derive the 5-point Gram matrix first).
6. **Why small P does not grok** — Power et al. (2022) + Nanda's combinatorial-diversity
   discussion, to interpret the P=29 negative result and the P=59 probe outcome.
7. **Matched-comparison statistics** — the one-variable rule, seed spread as mean ± std
   with n, and honest "no effect" reporting; formalized once, reused by every rung.

## Documentation requirements

- **Progress log:** one dated entry per session, negative results included.
- **Notes:** induction-heads note (standard-scale + K-composition results), grokking
  progress-measures note, Nanda & Jacobsen composition note, patching-E2E note,
  matched-comparison methodology note.
- **Skill tree:** flips only with proof — `induction-head reproduction` on a confirmed
  head + causal verification; `grokking reproduction` on P=113 manifests;
  `reproducible-from-clean-clone` on a passed gate.
- **RESULTS.md:** new manifests, new tables, ledger entry, always reconciled with
  `make verify-claims`.
- **Paper:** Methods + Rung 3 first, evidence order after, every paragraph tied to a
  manifest or figure.

## Practical exercises and hands-on challenges

1. **Exercise — K-composition detector (Step 0).** Script + diagnostic figure + falsification tests.
2. **Challenge — P=59 probe (Step 1).** Run it; explain the progress curves in writing.
3. **Challenge — Colab P=113 ×3 seeds (Step 2).** Launch, monitor, download, verify
   checksums, pin, update RESULTS.md. The flagship, end to end.
4. **Exercise — matched-comparison drill.** Weight decay 0.3 vs 1.0 at P=59 (2 seeds):
   tests the "weight decay is critical" claim and keeps the discipline fluent.
5. **Exercise — Rung 3 small case.** Hand-derive the regular-pentagon Gram matrix,
   verify numerically, produce Elhage's 5→2 figure.
6. **Challenge — clean-clone gate (Step 6).** Fresh clone → sync → CI → reproduce →
   verify-claims; proof written from the transcript.
7. **Exercise — publication figures.** Headline figures in one consistent style,
   regenerable via `make reproduce`.

## Strategic tips and architectural best practices

- **GPU-first scheduling:** the Colab run launches before any CPU work; it is the only
  parallel resource. Fold Rung 1 standard into the same session.
- **Diagnostic before verdict:** Step 0 exists so that "no head" produces a measurement,
  not another blind re-run.
- **One variable per experiment:** every claim from a matched comparison.
- **Quick scale is a smoke test, never a result:** only standard-scale, manifest-backed
  numbers enter headline tables.
- **Commit after every experiment:** manifests against a clean HEAD; Colab results pinned
  to their SHA or not recorded.
- **Checkpoint hygiene:** Drive, seed+date names, checksums verified after download.
- **Keep the mypy ratchet:** the K-composition detector joins the blocking allowlist on
  day one; `src/models/` is paid down while GPU time runs.
- **Falsification tests for every new instrument** — the detector gets its own.
- **Scope discipline:** W&B and HF Spaces remain stretch goals; nothing this phase
  touches fails to back a headline number or a paper section.
- **The honesty ledger is the brand:** a "no head formed, here is exactly how far it got"
  write-up is a stronger portfolio artifact than a forced positive.

## Gate criteria — what green looks like

1. P=59 probe verdict recorded (grok or diagnosed) — recipe validated or tuned before GPU.
2. P=113: ≥2 seeds grokked, manifests pinned, Fourier + ablation figures committed.
3. Rung 1 standard-scale verdict: confirmed head + causal verification, or a K-composition
   "how far" figure.
4. If a head formed: Rung 4 E2E and Rung 5 re-test manifests.
5. Rung 3 small-case pentagon (5→2 Gram matrix) confirmed.
6. Clean-clone gate green → Phase 6 proof passed.
7. Paper: Methods + Rung 3 written; remaining sections mapped to evidence.
8. Tests ≥168, local CI mirror green, GitHub CI green on `dev`, merge done.

## Links

- [[00_meta/09_micro-phase-10-evidence-run]] — where the instruments came from.
- [[00_meta/08_micro-phase-09-flagship-sprint]] — the parent roadmap this executes.
- [[00_meta/03_progress-log]] — the journal this phase is being recorded in.
- [[portfolio/RESULTS]] — the ledger this phase must change.
- [[04_nlp_and_transformers/notes/induction-heads]] — Rung 1's working note.

---

## Execution record (appended as results land)

### 2026-08-06 — Step 0 built: the K-composition detector

`k_composition_scores` / `diagnose_induction_formation` / `plot_composition_diagnostic`
landed in `exp1_induction_heads.py`. The detector implements the Nanda & Jacobsen
two-step path: Step 1 = L0 duplicate-token head (diag+1 mass per L0 head), Step 2 =
K-composition score per (L0, L1) head pair — L1 attending to `prev(q)+1` where
`prev(q)` is the position L0 attended to at q. Two guards keep it falsifiable:
queries where the L0 head attends to itself, and queries where `prev(q)+1 == q`
(plain self-attention), are excluded.

Tests: 6 new falsification tests in `tests/test_induction_heads.py::TestKComposition`
— a hand-built L0→K-composition chain must score ~1.0, self-attention ~0, wrong
offset ~0, uniform patterns exactly the 1/S baseline, and the full diagnostic must
run on a tiny trained model. All pass; suite is 174 pytest, ruff clean. The detector
is wired into `run_single_seed` (two new manifest metrics: `k_composition_score`,
`l0_duplicate_head_mass`) and into `main()` with the `figures/exp1_k_composition.png`
diagnostic figure. First target for the mypy ratchet, per plan.

### 2026-08-06 — Step 1 verdict: the P=59 probe does not grok (and that is data)

`--probe` (P=59, canonical hyperparameters, 1500 epochs) completed: train loss
memorized to 0.0004, validation accuracy 0.0000 the whole way, generalization epoch
-1, Fourier frequencies used 59/59 (100% dense) — the model never left the
memorization phase. This matches the 2026-08-01 P=29 negative result and points the
same direction as Power et al./Nanda's combinatorial-diversity argument: small P
does not grok reliably in a fixed budget. **The probe's real de-risk value is
pipeline validation, not a recipe confirmation**: the canonical recipe runs clean
end-to-end on CPU with progress measures working; it also says plainly *do not spend
GPU hours on P=59* — the P=113 run goes straight to the full canonical budget.

Matched drills all landed on the same verdict:

| drill | config delta | result |
|---|---|---|
| P=59 ×3000 ep | budget 1500→3000 | val acc 0.0000 at end, val loss *rising* to 9.5, Fourier 59/59 dense |
| P=59 wd 0.3 ×1500 | weight decay 1.0→0.3 | val acc 0.0012, Fourier 59/59 dense |

Three probes, two P-values, two budgets, two weight-decay regimes: the model
memorizes and never leaves the memorization phase. **The recipe is not falsified by
any drill — small P in this fixed budget does not grok.** Residual risk for the GPU
run is now narrowed to P=113 itself: if the canonical budget run fails there too,
the top suspects are the embedding re-normalization and the cosine schedule (both
deviations from Nanda's constant-LR setup) — the probes can't distinguish those
from small-P effects.

### 2026-08-06 — Step 2 launched: Rung 1 standard-scale domino (CPU, overnight)

`exp1_induction_heads --standard` (vocab 2048, seq 64, d_model 64, 2 layers, 4
heads, fresh batches, 3000 epochs, 8192 train) launched detached on this machine —
the highest-leverage experiment of the phase. Honest reality: ~20 s/epoch on this
CPU → ~17 h wall, verdict expected overnight (started 11:26 → ~04:00). Verdict
(head confirmed + causally verified, or the K-composition "how far" reading) gets
appended to this record when the run lands. Colab P=113 ×3-seed launch is the
remaining GPU item, exercised manually when a session is available.

### 2026-08-06 — Rung 3 small case re-confirmed, with a sharper claim

`--geometry-check` re-run (600 epochs / 8000 samples, 6 sparsities, 5 features → 2
dims): at and below sparsity 0.1 the features sit on a regular pentagon (gaps
70.2–73.8°, std ≤1.4° vs ideal 72°; best 71.6–73.0°, std 0.5° at 0.02); at 0.2–0.5
they are 4/5 represented and **off** the pentagon (gaps 23–91°, std 22°+). The
equiangular geometry is the sparse-phase attractor, not a dense-phase property —
"every level" in the MP10 writeup was wrong and is corrected in the progress log.
