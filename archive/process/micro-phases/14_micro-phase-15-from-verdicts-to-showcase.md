---
tags: [type/moc, phase/6, phase/7, research/experiment, state/review]
created: 2026-08-08
---

# Micro-Phase 15 — From Verdicts to Showcase (roadmap)

Written before the verdicts land, as a personal learning log and a public record.
[[13_micro-phase-14-the-verdicts]] is the phase that *launches* the two flagships; this
phase is the half that must never be allowed to wait on them. Its design principle: **no
idle verdict time.** Everything that does not need the two runs starts now, in parallel;
everything that does is pre-registered in this note with its terms already decided.

## Where this phase starts (state review, verified against the repo)

Checked `git status` / `git log` / the manifests before writing a single claim — the
standing lesson of MP-12 is that memory is not evidence.

- **MP-14 Step 0 is shipped** (`f853c88`, merged to `main` via PR #39): the pre-flight ran
  green locally (185 tests, ruff clean, blocking mypy clean) and the verdicts phase's
  roadmap is wired into [[00_meta/00_home]].
- **MP-14 Steps 1–7 are not yet executed** (as this roadmap is written): no R1
  `--standard` verdict, no P=113 manifest, no R3 full-scale re-run, no R4/R5 cascade, no
  clean-clone transcript, no paper prose. Their execution belongs to MP-14; this phase
  consumes their outputs through the two lanes pre-registered in Step 6 below.
- **`make verify-claims` reports exactly 2 problems** — Rung 2 and Rung 5 have no manifest
  ever produced. The gate is working as designed: it will keep failing until those runs
  land, and it is the release's honest floor.
- **The evidence that exists is strong and committed**: 12 curated figures tracked in
  `portfolio/figures/`, manifests for exp1 (tiny multi-seed), exp3 (phase transition,
  pentagon geometry), exp4 (quick multi-seed). The strongest verified result — Rung 3's
  superposition phase transition — needs *no* verdict to be written up.
- **The committed fallback is already implemented**: the K-composition detector and
  `plot_composition_diagnostic` ("how far did the model get") live in
  `src/experiments/exp1_induction_heads.py` (`k_composition_scores` → the step-2 diagnosis
  → `exp1_k_composition.png`). A headless verdict still ends in a figure, not a hole.
- **The mypy ratchet slipped**: 154 tracked full-tree errors on 2026-08-01 became 171 on
  2026-08-08, after the lockfile resolved numpy 2.5.0 / torch 2.12.1+cpu. Non-blocking
  per CI policy, but a drift — this phase pays it down or freezes it, it does not ignore it.
- **Two drills never performed**: the figure-generator death class (silent, buffered,
  untraced) still has no watchdog, and the clean-clone gate (`scripts/clean_clone_check.sh`)
  has never produced a transcript.

### Bottleneck diagnosis (ranked by what blocks what)

1. **The two verdicts stay the critical path** — and both need compute that only I can
   launch (17–20 h supervised CPU; a Colab GPU session for P=113 × 3 seeds). This phase's
   entire job on the non-compute side is to be *done* by the time they land.
2. **A negative R1 verdict is a real possibility** (0/8 heads at every scale ever run).
   The design response is pre-registration: lane B below converts “no head” into the
   committed K-composition “how far” deliverable instead of letting the phase collapse.
3. **The release is verdict-gated by design**: `verify-claims` will block `dev → main`
   until Rung 2 and Rung 5 manifests exist. Correct behavior, but it makes *my* release
   schedule depend on an external machine — every minute the Colab session is late is a
   minute the showcase can keep accruing parallel value in the paper spine and the
   clean-clone proof.
4. **mypy's 171 full-tree errors**: code-quality debt held at one remove by the
   non-blocking tier; it is the ratchet deliberately not crashing CI — de-drifted here in
   bounded steps (one module to the blocking allowlist at a time).
5. **Documentation as a bottleneck**: `portfolio/paper/` is all `% TODO`. Three of the
   four evidencable sections — Related Work, Methods, Superposition, Limitations — are
   writable today; writing them before the verdicts removes the only genuinely
   parallelizable artifact from the critical path.

## 2. Deep-dive study and research topics

1. **Zhang & Nanda, “Towards Best Practices of Activation Patching” (ICLR 2024)** —
   *before* the first real use of `run_path_patching_to_logits()`. This repository has
   committed that paper's site/metric errors twice on activation patching; path
   patching's first real run must not be the third. Extract §3–4 into a per-site audit
   table applied to our own `exp4` code — the table itself becomes paper Methods material.
2. **Olsson et al. 2022, the K-composition curriculum** — read with our numbers: which
   ingredient (d_model, seq_len, vocab, loss) most plausibly gates head formation at our
   scale, so that the “how far” figure (lane B) can be interrogated rather than merely
   rendered.
3. **Nanda et al., ICLR 2023 — re-read with weights in hand** — the P=113 recipe the way
   it should be read: weight decay as the Fourier-dial, the embedding-normalization detail
   I deviated from (named suspect #1 if P=113 fails), and the `Freq^k` sparsity of the
   progress measure as the thing to hand-verify once the model exists.
4. **Power et al. 2022, the hyperparameter landscape** — weight decay is the grokking dial;
   LR and optimizer support. Keep the landscape visible when interpreting a possible P=113
   negative, and keep the retry budget at one variable.
5. **Pineau et al., reproducibility checklist (JMLR 2021)** — evidence-ordered paper
   craft: Methods → strongest result → each manifest-backed rung; no sentence whose
   evidence is not already in `RESULTS.md`.
6. **The predictability-self-audit** — score my own MP-9/MP-10/MP-14 predictions against
   what actually happens once the verdicts land. A calibration drill before interpreting
   either outcome keeps the narrative honest when the numbers arrive.

## 3. Documentation requirements

- **Progress log**: one dated entry per session, including raw pass/fail before
  interpretation. MP-15's own missteps go to the `RESULTS.md` ledger, not into silence.
- **New notes**: a *figure supervision + watchdog* note under `06_production_ai/notes/`
  once the driver is real (standing pattern, not a one-off); a *Fourier progress measures*
  note once P=113 lands; a *W&B-lite experiment logging* note if the instrumented run
  wires it; the mypy de-drift record as a short `conventions` footnote (what got added to
  the blocking allowlist and why).
- **Updated notes**: `04_nlp_and_transformers/notes/induction-heads.md` gets whatever the
  verdict says — the lane always writes; `path-patching.md` gets its first real end-to-end
  numbers; the grokking note gets P=113 manifests or the honest negative.
- **Paper spine**: Sections 2 (Related Work), 4 (Methods/Setup), 9 (Superposition) and
  the refined Limitations become prose first — each paragraph cites a file in this repo,
  nothing dangling. Sections requiring verdicts (Grokking, Induction, Patching, SAE) are
  left gated on those lanes in Step 6.
- **Skill tree**: flips only with proofs and exercises, following the vault's law: a
  checked box without proof is a lie — including the negative outcomes, which get their
  own lines (an honest record writes a verdict of "headless at this scale" as a result,
  not a gap).
- **RESULTS.md**: reconciled with each new manifest; the ledger entry for this phase
  includes its own missteps; the Rung 2/5 numbers come from manifests, not prose.

## 4. Practical exercises and hands-on challenges

1. **Challenge — the R3 watchdog regeneration**: driver script (heartbeat +
   restart-on-abnormal-exit, `python -u`) around the full-scale `--geometry-check`
   regeneration; pentagon confirmed at the canonical budget; the silent-death class
   drilled with a deliberate abnormal exit mid-run.
2. **Challenge — the clean-clone dry run**: `scripts/clean_clone_check.sh` on a fresh
   temp clone, full transcript produced now; every manual step encountered is a failed
   gate — fix it now so the post-verdict real run is a formality, not an exercise.
3. **Exercise — the claims audit**: take three headline numbers from `RESULTS.md`
   (pentagon gaps 70.2–73.8°, fresh-batches 52.2%, real-activation 99.97% FVE) and
   re-derive each from its manifest + code by hand. The calibration drill for
   “what would my own gate catch”.
4. **Exercise — the Zhang–Nanda audit table**: map the paper's patch-site / metrics
   checklist onto our `exp4` implementation line by line; any deviation gets a named
   justification or an issue. The deliverable is the table, not agreement.
5. **Habit — figure provenance at commit time**: ask the three gate questions one commit
   earlier — figure on disk? tracked in git? bound to a manifest? That habit has cost the
   ledger more than any single fault class this phase fixes.
6. **Habit — prose-source discipline**: every sentence written in Step 4 carries a
   `(file:line)` source note in the markdown draft; no sentence survives into the TeX
   that didn't originate from an artifact.
7. **Pre-registration exercise — the “how far” estimate**: from the model hyperparameters,
   write down the K-composition threshold expected and the figure I'd accept as
   evidence — before any verdict exists. Post-verdict, score it (topic 6, above).
8. **Challenge — the mypy de-drift**: pay down the 171→≤150 full-tree errors and move one
   module (candidate: `src/experiments/exp3_superposition.py` — the strongest result's
   own module) onto the blocking allowlist, with its errors-at-move count recorded.

## 5. Strategic tips and architectural best practices

- **Parallelize the critical path, and the non-critical path**: the verdicts own the
  critical path; the paper spine, the watchdog, and the clean-clone transcript are the
  parallelizable artifacts that keep the phase producing while compute cooks.
- **Pre-commit the branches before the numbers**: lane A vs lane B differs only in
  interpretation, never in whether a deliverable exists — the fallback figure is
  implemented before its verdict.
- **A named negative is a contribution**: “no induction head forms at scale X under
  fresh batches, causally verified” is a paper-quality negative when declared as such and
  accompanied by the “how far” K-composition figure.
- **The release gate stays mechanical**: `verify-claims` is the last word — a merge that
  carries a dangling number is not a release, it's a regression.
- **Never trust an unattended long job that hasn't survived a real death**: the watchdog
  gets drilled against an abnormal exit in this phase, on the machine, before any real
  run leans on it.
- **The paper is the last artifact, not the first**: prose is written from manifests; the
  scaffold I keep turning real is exactly that order.
- **One variable per retry, one ledger per verdict**: if P=113 fails, the retry dials
  (weight decay; embedding-normalization; LR scheduling) are changed *one at a time*,
  with a pre-set budget, and every failure lands in the ledger.

## 6. Step-by-step execution roadmap

All steps through Step 5 need nothing but this machine. Step 6 onwards consumes MP-14's
verdicts through the three lanes, each pre-registered with its own deliverable.

```
Step 0: Pre-flight (this note, ~15 min) — CI mirror green locally (≥185 tests, blocking
        mypy, ruff), ledger + home wired, pushed on dev, GitHub CI green.
Step 1: R3 watchdog regeneration (infra that survives a real death, ~2–3 h CPU)
Step 2: Clean-clone dry run — transcript, fix every manual step found
Step 3: Mypy de-drift 171 → ≤150; move ONE module onto the blocking allowlist
Step 4: Paper spine — Related Work, Methods, Superposition, Limitations sections as
      prose, every paragraph citing a file; the claims audit (Exercises 3–4)
Step 5: Pre-verdict gates — verify-claims stands at ≤2 expected problems; every
      artifact tracked; ledger note updated with the phase's own missteps
      ┌──────────────────────────────┬──────────────────────────────┐
      ▼ (verdicts land, in-flight MP14)                              ▼
Step 6a (head): R1 --standard manifest, R4 E2E on the real head,
      R5 re-test on the head-bearing checkpoint, path-patching numbers
      → paper sections 5-7, MODEL-CARD update, skill flips
Step 6b (headless): K-composition “how far” figure + writeup, R4 sensitivity
      bound published as the honest negative, paper sections 5-7 framed
      as a declared bound, skill tree records the negative
Step 6c (grokked): exp2 manifest, Fourier figures, hand-verified frequency
      product (Exercise 7), Fourier note; if not grokked on sweep #1:
      1-variable retry dials (weight decay / embedding normalization)
      with the pre-set budget
Step 7: Showcase & release — paper full draft v0.1, RESULTS.md reconciled
      with every manifest, verify-claims zero unexpected, clean-clone real
      transcript, model-card and portfolio README refresh, home wired,
      ledger final entry; PR dev→main on green CI; merge; cleanup;
      archive this roadmap with its deviations noted
```

## 7. Gate criteria

1. Step 0 green: ≥185 tests, ruff clean, blocking mypy clean, markdownlint clean, GitHub
   CI green on `dev` — nothing below is attempted on a red floor.
2. Step 1: watchdog survives a *real* abnormal exit and regenerates the canonical
   pentagon figure at the full-scale budget — recorded in the durability proof.
3. Step 2: clean-clone dry-run transcript with zero required manual steps; each found
   step is a fixed failure, not a waiver.
4. Step 3: full-tree mypy ≤ 150 and one more module added to the blocking allowlist with
   its count recorded at move time.
5. Step 4: four paper sections written in evidence order; every paragraph carries a
   file citation; the audit table committed.
6. Step 5: pre-flight gates — `verify-claims` at its expected 2 problems maximum, every
   artifact tracked, ledger entry written.
7. Verdict lanes: whichever verdict lands, a public artifact exists within the phase —
   head → path-patching numbers; headless → “how far” figure; grokked → exp2 manifest +
   Fourier write-up; not-grokked → named suspects + budgeted retry protocol.
8. Step 7 release: `verify-claims` at zero unexpected problems, real clean-clone
   transcript, `RESULTS.md` reconciled, model-card genuine (no templated claims), CI
   green on the PR, merge, tree clean, roadmap archived with its deviations.

## Links

- [[13_micro-phase-14-the-verdicts]] — the launch phase this synthesis consumes; its
  Step 0 is verified, steps 1–7 are the verdict sources.
- [[12_micro-phase-13-flagships-landed]] — the evidence base (12 figures, gates, kill
  drill) this phase builds its infrastructure on.
- [[portfolio/RESULTS]] — the ledger this phase must change; the source of every paper
  number.
- [[portfolio/README]] — the showcase surface this phase's release pass refreshes.
- [[06_production_ai/proofs/reproducible-from-clean-clone]] — the Phase 6 gate proof
  whose real transcript Steps 2 and 7 produce.
- [[04_nlp_and_transformers/notes/induction-heads]] and
  [[04_nlp_and_transformers/notes/path-patching]] — the working notes that absorb this
  phase's verdicts.