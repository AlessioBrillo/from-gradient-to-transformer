---
tags: [type/moc, phase/6, phase/7, research/experiment, state/review]
created: 2026-08-05
---

# Micro-Phase 9 — The Flagship Sprint (roadmap)

A roadmap written like a research plan: where I am, what blocks me, and the exact
sequence of steps I will run to convert the two flagship results from "pending" to
"evidence-backed". Written from my own perspective as a learning log, structured so it
can be read end to end by anyone reviewing the journey — including the parts where I
do not yet know the answer.

## Where this started

The Evidence Pass (Micro-Phase 8) ended with correct instruments and three open
blockers. This is the state I am starting from:

- **Rung 2 (grokking, primary flagship)** — still has no reproduced result. The code
  and the Colab notebook are ready (3-seed support wired), the run itself needs GPU
  hours I do not have in this environment. This is the single most important open
  item in the repository.
- **Rung 1 (induction heads, fallback flagship)** — task-design bug fixed, and the
  fixed-vs-fresh-batches comparison proved the fixed-dataset loop actively regresses
  while fresh batches were still improving at epoch 800. But no induction head has
  ever formed in any run at any scale so far. The standard-scale fresh-batches run
  (never yet executed) is the natural next experiment.
- **The cascade** — Rung 4 (path patching is validated only by unit tests) and Rung 5
  (the real-vs-synthetic SAE comparison is "informative rather than conclusive") are
  both blocked on a checkpoint with a confirmed induction head. One domino unblocks
  two rungs.
- **Infrastructure** — the multi-seed provenance harness works and has already caught
  real drift; `verify-claims` currently reports all three manifests as recorded
  against a dirty tree, so they must be re-baselined at a committed HEAD before any
  new number is quoted.
- **The paper** — scaffold exists with zero prose, deliberately. It becomes writable
  in evidence order: strongest result first.

The common thread: this micro-phase is not about writing new code. It is about
**sequencing existing code and compute so that the evidence dependency chain resolves
in the right order**.

## Bottleneck analysis — the dependency chain

```
                    ┌────────────────────────────────────────────────────┐
                    │  re-baseline manifests at HEAD (cheap, CPU, now)   │
                    │  → verify-claims green → results are citable       │
                    └───────────────────────┬────────────────────────────┘
                                            │
        ┌───────────────────────────────────┴───────────────────────────────────┐
        │                                                                       │
┌───────▼──────────┐                                                ┌──────────▼─────────┐
│ Rung 2: P=113    │      (async, Colab GPU, launch FIRST)          │ Rung 1: standard-  │
│ grokking ×3 seeds│                                                │ scale fresh-batches│
│ ──► flagship     │                                                │ ──► the DOMINO     │
│ evidence +       │                                                └──────────┬─────────┘
│ Fourier analysis │                                                           │
└──────────────────┘                                                    head formed? ──no──► document how far (K-composition diagnostic)
                                                                        │yes
                                                        ┌───────────────┴───────────────┐
                                                        │                               │
                                              ┌─────────▼─────────┐             ┌────────▼─────────┐
                                              │ Rung 4: path      │             │ Rung 5: SAE on  │
                                              │ patching E2E      │             │ head-bearing    │
                                              │ (first real-head  │             │ checkpoint      │
                                              │ validation)       │             │ (sparsity retest)│
                                              └─────────┬─────────┘             └────────┬─────────┘
                                                        └───────────────┬────────────────┘
                                                                        │
                                              ┌─────────────────────────▼─────────────────────┐
                                              │ Phase 6 gate: clean-clone reproducibility run │
                                              │ Paper: Methods + Rung 3 first, rest in order  │
                                              └───────────────────────────────────────────────┘
```

Two observations that shape the whole phase:

1. **Rung 1 is the highest-leverage experiment.** Its outcome (head or no head)
   resolves three open items at once: the Rung 1 headline, Rung 4's end-to-end
   validation gap, and Rung 5's honest re-test. Everything else this phase is either
   cheaper (manifest re-baseline) or parallel (the GPU run).
2. **GPU work must be launched before CPU work.** The Colab run is async compute:
   start it, then use the waiting time for everything that runs on this machine.

## The roadmap — eight steps in order

### Step 0 — Re-baseline the manifests at a committed HEAD

- **What:** re-run the three multi-seed quick experiments (`exp1`, `exp3`, `exp4`,
  `--seeds 0,1,2`) so `results/*.json` records `git_dirty: false` against the current
  commit, then confirm `make verify-claims` is green.
- **Why:** a manifest pinned to a dirty tree cannot back a citable claim. This is the
  cheapest fix in the phase and it restores meaning to the checker.
- **Definition of done:** `make verify-claims` reports zero problems; the numbers in
  `portfolio/RESULTS.md` still match the regenerated manifests (or are reconciled if
  the code drifted — itself worth knowing).

### Step 1 — Launch the grokking flagship on Colab (async, do this first)

- **What:** run `notebooks/colab_grokking_full_run.ipynb` with the canonical P=113
  config, 3 seeds. Save checkpoints to Drive, download figures and per-seed metrics
  back into `results/` and `figures/`.
- **Why:** it is the primary flagship and it is pure wait time — everything else on
  this phase can happen while it runs.
- **Definition of done:** three per-seed manifests for `exp2` (with a manual,
  honestly-dated provenance entry — the notebook path bypasses the local runner), the
  grokking curve, the Fourier decomposition and the frequency-ablation figures in
  `figures/`, and a new row in `RESULTS.md`.

### Step 2 — Rung 1 standard-scale fresh-batches: the domino experiment

- **What:** train with `d_model=64, seq_len=64, vocab_size=2048, --fresh-batches`,
  extended budget (2000+ epochs), 3 seeds. Where possible, fold this into the same
  Colab session as Step 1; otherwise run it overnight on CPU.
- **Why:** every prior run was at quick scale or sub-standard budget. The
  fixed-vs-fresh comparison says the trajectory was still rising at epoch 800 — the
  question "does a real induction head form?" has never actually been asked at the
  scale it is supposed to form at.
- **Definition of done:** 3-seed standard-scale manifest, the training-curve +
  attention-pattern figures, and a verdict in `RESULTS.md`: head detected (≥0.3
  diag+1 mass, causally verified) or a measured "how far" answer via the
  K-composition diagnostic (Step 4 of the exercises).

### Step 3 — The cascade (conditional on Step 2 forming a head)

- **Rung 4, end-to-end:** point activation patching, path patching, and head ablation
  at the confirmed head. This closes the last validation gap in the repository —
  path patching finally runs against a real circuit, not just its unit tests.
- **Rung 5, honest re-test:** re-run `--activations-from` on the head-bearing
  checkpoint and compare L0/FVE against the previous dense-reconstruction reading
  (99.97% FVE, 53% L0). Sparse and clean → the earlier ambiguity was the
  undertrained checkpoint; still dense → that is itself the honest result to publish.
- **If no head forms:** Step 2 still produces the diagnostic figure showing how far
  the network got toward the mechanism — the phase does not hinge on a forced
  positive.

### Step 4 — Close Rung 3's two small open ends

- Verify the geometric claim on the known small case (5 features → 2 dimensions must
  show the pentagon in the Gram matrix), and resolve whether the 16/20 at sparsity
  0.001 is under-training (more epochs at that setting) or something real.

### Step 5 — Phase 6 gate: reproducible from a clean clone

- Fresh clone → `uv sync --frozen` → `make ci-check` → `make reproduce-quick` →
  `make verify-claims`. Identical numbers, no manual steps. This turns the
  `reproducible-from-clean-clone` proof green and is the moment the repository
  qualifies as citable research infrastructure.

### Step 6 — Paper first draft, in evidence order

- Methods + Rung 3 first (strongest, already manifest-backed), then Rung 1/4/5
  sections as Step 2/3 land, then grokking. Every section written from its manifest,
  not from memory — the `% TODO` comments in `portfolio/paper/main.tex` each already
  name the artifact they should be written from.

### Step 7 — Honesty Ledger + RESULTS.md reconciliation

- One ledger entry for this phase, whatever the outcome. The phase's success is
  defined as *knowing* the answers (does grokking grok at P=113? does a head form at
  standard scale with fresh batches?), not as both answers being yes.

### Step 8 — Close the phase

- Verify `verify-claims` green, tests ≥158, CI green on `dev`, then the dev → main
  merge. Archive this roadmap in the progress log as the plan it turned out to be,
  with deviations noted.

## Deep-dive study and research topics

1. **Nanda & Jacobsen, "Attention as a Step Towards the Emergence of the Induction
   Head" (2023)** — the single most relevant paper for Step 2. It decomposes
   induction-head formation into three steps (duplicate-token head → K-composition →
   induction head) in a 2-layer attention-only model very close to mine. Reading it
   gives me the diagnostic instruments to answer "how far did the model get?" instead
   of just "did it form?".
2. **Olsson et al. §3–4, re-read with calibration in mind** — the section on the
   conditions under which induction heads form (model scale, dataset size, sequence
   length). My Step 2 config should be checked against their regimes before I burn
   GPU hours.
3. **Nanda et al., "Progress Measures for Grokking" (ICLR 2023)** — implement the
   Fourier-sparsity and weight-norm progress measures *before* the GPU run, so the
   run is analysis-ready the moment it finishes. The three phases (memorization →
   circuit formation → cleanup) are the story the paper will tell.
4. **Zhang & Nanda, "Towards Best Practices of Activation Patching" (ICLR 2024)** —
   re-read before Step 3: patch-site selection, metric choice, layernorm caveats.
   Rung 4 is the first place these lessons get applied to a real, named head.
5. **Elhage et al., "Toy Models of Superposition" §3–4** — the geometry section, for
   Step 4's pentagon check and the phase-change plot interpretation.
6. **Matched-comparison statistics** — formalize what I already did once in the
   fixed-vs-fresh study: one variable per comparison, identical config otherwise,
   seed spread reported as mean ± std with n. This discipline will back every claim
   in the paper.

## Documentation requirements

- **Progress log:** one dated entry per experiment session, using the
  Studied/Built/Open-question template — including negative results.
- **Skill tree:** flip `induction-head reproduction` to `[x]` only with a
  standard-scale confirmed head + causal verification (the vault's own rule: a
  checked box without proof is a lie). Same for `grokking reproduction` when the
  P=113 manifests exist, and for the Phase 6 clean-clone proof when Step 5 passes.
- **Notes:** update `04_nlp_and_transformers/notes/induction-heads` (standard-scale
  results + composition diagnostics), write a grokking progress-measures note, a
  Nanda & Jacobsen composition note, a patching-E2E note, and a
  matched-comparison methodology note (reusable by every future rung).
- **RESULTS.md:** new manifests, new tables, ledger entry — always reconciled with
  `make verify-claims`.
- **Paper:** fill sections in evidence order; each paragraph must cite its manifest
  or figure.

## Practical exercises and hands-on challenges

1. **Exercise — K-composition detector.** Given a trained checkpoint, produce
   per-head attention patterns and detect the two intermediate steps toward the
   induction head: the L0 duplicate-token head (diag+1 attention) and the L1
   K-composition step. Deliverable: a small script + diagnostic figure. This is the
   "how far are we" instrument for Step 2.
2. **Exercise — grokking progress measures.** Implement Fourier sparsity and
   weight-norm trajectories; validate them on cheap P=59 CPU quick runs where the
   three phases should be visible. Land this *before* the GPU run.
3. **Challenge — the full Colab P=113 run.** Execute the notebook, download
   checkpoints and figures, verify the run's claims against the manifests, update
   RESULTS.md. This is the flagship, end to end.
4. **Exercise — matched-comparison drill.** Repeat the fixed-vs-fresh methodology on
   one new factor (e.g., `seq_len` 24 vs 48 at matched budget) to build fluency in
   the discipline, not just familiarity with one result.
5. **Challenge — clean-clone gate.** Fresh clone, `uv sync --frozen`, `make
   ci-check`, `make reproduce-quick`, `make verify-claims` — identical numbers, no
   manual steps. Write the Phase 6 proof note from the actual transcript.
6. **Exercise — publication figures.** Rebuild the 3–5 headline figures with a
   consistent publication style (fonts, sizes, colormap), all committed and
   regenerable via `make reproduce`.

## Strategic tips and architectural best practices

- **GPU-first scheduling:** the Colab run starts before any CPU work — it is the
  only truly parallel resource this phase has.
- **One variable per experiment:** every claim this phase makes must come from a
  matched comparison. The fixed-vs-fresh study is the template, not the exception.
- **Quick scale is a smoke test, never a result:** only standard-scale, manifest-
  backed numbers enter RESULTS.md headline tables.
- **Commit after every experiment:** manifests recorded against a clean HEAD are the
  difference between evidence and anecdotes. This phase opens with exactly that
  discipline restored (Step 0).
- **Checkpoint hygiene:** Colab checkpoints go to Drive with seed + date in the
  name; verify sizes/checksums after download before trusting them.
- **Diagnostic before verdict:** when a mechanism does not form, the deliverable is
  an instrument that shows how far it got (the K-composition detector), not another
  blind re-run.
- **Keep the mypy ratchet:** any module I touch this phase must be clean enough to
  join the blocking allowlist.
- **Scope discipline:** W&B dashboards and Hugging Face Spaces remain stretch goals.
  Nothing this phase spends time on should fail to back a headline number or a
  paper section.
- **The honesty ledger is the brand:** a "no head formed, here is exactly how far it
  got" write-up is a stronger portfolio artifact than a forced positive.

## Gate criteria — what green looks like

1. `make verify-claims` green at a committed HEAD (Step 0).
2. P=113 grokking: ≥2 seeds with manifests and Fourier-analysis figures (Step 1).
3. Rung 1 standard-scale fresh-batches run complete and reported — head confirmed
   and causally verified, or an honest "how far" answer from the composition
   diagnostic (Step 2).
4. If a head formed: Rung 4 end-to-end validation and Rung 5's re-test complete
   (Step 3).
5. Rung 3 geometry + sparsity-0.001 questions closed (Step 4).
6. Phase 6 clean-clone proof green (Step 5).
7. Paper draft: Methods + Rung 3 written; remaining sections mapped to landed
   evidence (Step 6).
8. Tests ≥158, local CI mirror green, GitHub CI green on `dev`, merge done.

## Links

- [[00_meta/03_progress-log]] — the journal this roadmap will be executed in
- [[portfolio/RESULTS]] — the ledger and per-rung status this phase must change
- [[07_capstone/research-plan]] — the experiment ladder and flagship strategy this
  roadmap operationalizes
- [[04_nlp_and_transformers/notes/induction-heads]] — Rung 1's working note
- [[00_meta/07_micro-phase-08-evidence-pass]] — the pass this one builds on
