---
tags: [type/moc, phase/5, phase/6, phase/7, research/experiment, state/review]
created: 2026-08-02
---

# Micro-Phase 10 — Consolidation & Paper (Roadmap)

A roadmap written before the work, deliberately — the same register as
[[08_micro-phase-09-the-flagship-runs]]. Micro-Phase 8 taught me that the most useful
discipline I have is writing down what I expect *before* I measure; Micro-Phase 9 made
that discipline the plan itself. This note is the plan for the micro-phase that follows
the flagship runs: the one in which the evidence — whatever it turns out to be — becomes
a paper, two phase gates go green, and the vault stops contradicting itself.

The contract of this micro-phase is that it is **outcome-agnostic**. The mini-paper gets
written whether Run A groks at P=113 or is recorded as a genuine negative; the Honesty
Ledger entry gets appended either way; gate 6 gets proven either way. What changes
between outcomes is the headline, not the work. The decision tree in this note is the
mechanism: it is the only place Micro-Phase 9's run outcomes land, and the branch
actually taken is recorded in my postscript *before* any prose is polished.

Four consolidation targets, stated plainly:

1. **A paper** — every writable section of `portfolio/paper/main.tex`, with every number
   backed by a manifest and zero silent gaps.
2. **Green phase gates 5 and 6** — the two gates my checklists still owe, proven by the
   gate proofs, not by assertion.
3. **A coherent vault** — READMEs, MOCs, tags, and claims that all agree with
   [[portfolio/RESULTS]].
4. **Technical debt paid down** — the exp5 seed harness, the mypy ratchet, and figures
   regenerated from committed code.

## Where this micro-phase starts

State at 2026-08-02, after [[08_micro-phase-09-the-flagship-runs]] was committed:

- **Micro-Phase 9 is pre-registered, not executed.** The P=113 grokking run and the
  standard-scale induction-head run need a GPU I do not have in this environment. Both
  entry states are handled here: the runs may have happened by the time this phase
  starts, or they may not — the tree below takes either branch.
- **Rung 3 (superposition)** is the only fully verified headline: the phase transition
  10/20 → 20/20 features represented as sparsity drops, multi-seed, root cause
  documented.
- **Rung 2 (grokking)** has exactly one data point: the P=29 quick test, a genuine
  dense-Fourier negative (val acc 0.0017, 29/29 frequencies).
- **No induction head has ever been detected** (0/8 across all seeds); path patching is
  validated only by its unit tests; the SAE's real-activation run (99.97% FVE, 53% L0)
  is honestly read as a wide, dense autoencoder.
- All three committed manifests were recorded against a dirty tree and a stale SHA
  (`6a5a54f`); every on-disk figure predates the 2026-08-01/02 fixes; and `figures/` is
  gitignored even though [[04_conventions]] says figures are committed — a contradiction
  this phase settles.
- Phase gates 5 and 6 are unpassed. Phase 6's checklist has zero checked items and its
  MOC is a placeholder; Phase 5's gate depends on nnsight and on an AtP naming
  contradiction the skill tree has already half-resolved.
- The mini-paper is a scaffold: every section a `% TODO`, prose gated on
  `results/exp2_grokking.json` existing.

What this micro-phase leaves behind, regardless of which branch the tree takes: a paper
with prose, a green gate 6 and a reconciled gate 5, a graph that agrees with itself, and
a ledger entry written in the same register whether the flagship runs succeeded, failed,
or never happened.

## Decision Tree — Inheriting Micro-Phase 9's Outcomes

Micro-Phase 9's seven exercises are **inherited, not duplicated**:

- Frequency-ablation confirmation (its Exercise 3)
- Path patching end-to-end (its Exercise 4)
- SAE re-run on the grokked checkpoint (its Exercise 5)
- Pentagon Gram-matrix geometry check (its Exercise 6)
- The two written proofs — modular-addition Fourier algorithm, induction-head formation
  dynamics (its Exercise 7)

Each inherited outcome has exactly two fates in this phase: *done* → quoted as evidence
in the paper and in [[portfolio/RESULTS]]; *not done* → its absence is stated in the
paper's Limitations and its deferral is named here, with a date. There is no third fate,
and nothing in this micro-phase re-runs them.

**Branch variables.** Run A (grokking, P=113): A1 grokked (≥ 1 seed, targets met),
A2 partial (1 of 3 seeds or missed targets), A3 genuine negative (0 of 3 within the
fixed budget), A4 never ran. Run B (induction heads): B1 head found, B2 no head,
B3 never ran. Twelve combinations collapse into five paper outcomes:

| Branch | Paper flagship section | RESULTS.md headline | Skill-tree boxes | Ledger entry |
|---|---|---|---|---|
| A1/B1 | Grokking section written in full; induction section with a real head | Grokking: reproduced; induction: confirmed | Grokking `[x]`; SAE per re-run | #4: both runs land, numbers as recorded |
| A1/B2 | Grokking in full; induction written as a repeated negative at standard scale — a finding about task design | Grokking: reproduced; induction: honest negative | Grokking `[x]`; induction stays `[~]`, negative documented | #4: mixed outcome, both recorded |
| A2 or A3, any B | Grokking becomes "A Pre-Registered Negative at Scale": protocol, P=29 and P=113 together, what the pair licenses | Headline falls back to Rung 3 superposition | Grokking stays `[~]`, reason next to the box | #4: the negative is the result |
| A4, any B | Grokking section is a marked placeholder ("Not yet run — protocol pre-registered, notebook ready"), never a silence | Headline = Rung 3, Rung 1 fresh-vs-fixed as secondary | No box flips without a manifest | #4: runs still pending, stated plainly |
| Any A, B3 | Induction section written from the fresh-vs-fixed finding; path-patching claims stay "unit-tests-only" | As above, with "no standard-scale run yet" | No box flips without a manifest | #4 records the deferral |

A4/B3 is not a failure of this micro-phase. The tree's only binding rule is that the
branch actually taken is recorded in my postscript *before* the prose is polished — a
later outcome may not quietly rewrite an earlier branch.

## 1. Deep-Dive Study and Research Topics

Study is mapped to the exact artifact it informs, as in Micro-Phase 9. Five topics, all
CPU-only:

1. **Pre-registration and research integrity.** Nosek et al. (2018) on pre-registration
   and the tradition behind it — the frame for the paper's Methods/Reproducibility
   section and for the claim that this project's differentiator is its honesty
   infrastructure (three audit entries, pre-registered predictions). I want to be able
   to cite the practice correctly, not just practice it.
2. **Grokking, consolidation pass.** Power et al. (2022), Nanda et al. (2023), Liu et al.
   (2022, Omnigrok), Varma et al. (2023) — read not to learn grokking (that was
   Micro-Phase 9's study list) but to write the paper's comparison paragraph: what
   reproduced, what differed, where my numbers sit in the literature. Under branch A3/A4
   this topic morphs into "what a scaled negative requires" — controls, budgets, and
   what the P=29 + P=113 pair jointly license — for the negative-result subsection.
3. **Patching best practices and their limits.** Zhang & Nanda (2024), Wang et al.
   (2023), Makelov et al. (2023) on layernorm denominator effects and
   subspace-projection illusions. This is what the Limitations section's patching
   entries are written *from* — understanding, not the scaffold's pre-seeded bullets.
4. **SAE evaluation literacy.** Bricken et al. (2023) and Cunningham et al. (2024) on
   FVE, L0, dead-feature rates, and what "sparse" means on genuinely sparse features —
   the benchmark for reading the 99.97% FVE / 53% L0 real-activation run as the dense
   autoencoder it is, and for whatever the re-run returns.
5. **Academic writing craft, minimal.** One short practical guide on abstract and
   conclusion discipline, to keep the paper tight. Time-boxed: skipped-with-note if the
   phase is running long.

## 2. Documentation Requirements

Every artifact this phase must produce, and where it lands:

1. **Commit between exercises.** Provenance is the gate: a manifest can only record
   `git_dirty: false` on a committed tree. This is the same rule Micro-Phase 9 ran on;
   it is repeated here because Exercises 2–4 depend on it.
2. **`results/` re-verified** — all four manifests (exp1, exp3, exp4, and the new exp5)
   recorded on a clean tree with `git_sha` = HEAD, plus the exp5 manifest that does not
   exist yet.
3. **`portfolio/RESULTS.md`** — final per-rung tables with manifest tags on every
   headline number, figure lists that match the disk, and the Honesty Ledger entry
   (entry #4, or #5 if Micro-Phase 9's runs produced one). The ledger stays append-only.
4. **Skill tree** — boxes flipped only with proof: reproducibility harness `[x]` after
   the gate run; grokking and SAE boxes per the taken branch; mini-paper `[x]` after
   prose lands.
5. **Progress log** — one dated entry per working session, following the journal
   convention.
6. **`00_meta/00_home.md`** — the link line for this note, mirroring how Micro-Phase 9's
   creation commit touched home.
7. **Micro-Phase 9 postscript** — if the runs happened, the MP9 note gets its promised
   postscript and this note links it; if not, my postscript says "still pending" in one
   line.
8. **Paper, figures, manifests** — the tracked artifacts: `portfolio/paper/main.tex`,
   `figures/*.png` (regenerated), `results/*.json` (re-verified).

## 3. Practical Exercises and Hands-On Challenges

Ordered by dependency; each has a defined "done" condition and a time bound. All are
CPU-runnable; nothing here waits on a GPU. The dependency chain runs code (2) →
manifests (3) → gate (4) → claims (8) → paper (9), with figures (1), gate 5 (5), graph
(6), and tags (7) in parallel lanes.

1. **Figures and artifact truth** (3–5 h). Regenerate every figure from committed code at
   the configuration that produced each reported number — quick scale where the number
   was quick, full scale where full. Delete `figures/exp6_automated_vs_manual.png` and
   the stale `src/experiments/__pycache__/exp6_automated_circuit*.pyc` (`make clean`).
   Settle the `figures/` gitignore contradiction: either un-ignore and commit the
   regenerated set (the convention's stated rule) or amend [[04_conventions]] to
   "generated-only, deterministic scripts are the source of truth" — one decision,
   written down. Reconcile RESULTS.md's figure lists with the disk: three names are
   claimed that do not exist (`exp4_head_ablation.png`, `exp5_sparsity_tradeoff_real.png`,
   `exp5_feature_histogram_real.png`) — regenerate or strike, with the figure scale
   declared next to each. *Done when* every figure named in RESULTS.md exists on disk and
   came from a committed script, `exp6*` is gone everywhere, and the gitignore decision
   is recorded in [[04_conventions]].
2. **exp5 `--seeds`, manifest wiring, and the mypy ratchet** (1.5–3 h). Add `--seeds` to
   `src/experiments/exp5_sae_dashboard.py` using the `runner.py` pattern from
   Micro-Phase 8 — reuse, not rewrite. Run a 3-seed quick manifest; add
   `<!-- manifest: results/exp5_sae_dashboard.json -->` to Rung 5 in RESULTS.md; extend
   `make reproduce-multiseed` to include exp5. Then extend the `typecheck-new` allowlist
   with exp5 and fix its strict-mode errors — the ratchet moves, not the big bang.
   *Done when* `results/exp5_sae_dashboard.json` exists with 3 seeds, `make verify-claims`
   passes with the new tag, and `make typecheck-new` still exits 0 with exp5 in scope.
3. **Manifests re-verified on a clean tree** (1–2 h). After Exercises 1–2 are committed,
   re-run exp1/exp3/exp4 `--quick --seeds 0,1,2` plus the exp5 run. *Done when* all four
   manifests record `git_dirty: false` and `git_sha` = HEAD, and every manifest tag in
   RESULTS.md matches its manifest's seed count.
4. **Phase 6 gate — the clean-clone run** (2–3 h). Execute the gate proof's own commands
   verbatim from a fresh clone of pushed `dev`: `uv sync`, `make reproduce-quick`,
   `make reproduce-multiseed`, `make verify-claims`. Update
   `06_production_ai/proofs/reproducible-from-clean-clone.md` to Outcome: Passed, flip
   the 06 checklist gate line, and flip the skill tree's reproducibility-harness box.
   *Done when* the proof's outcome is `[x] Passed` and the 06 checklist's "Phase gate"
   line is `[x]` with the proof linked.
5. **Phase 5 gate reconciliation — nnsight and the AtP naming** (1.5–4 h). The checklist
   marks Attribution Patching `[x]` while the skill tree says it is "genuinely not
   implemented", and nnsight sits unchecked under a gate that names it. Read the 05
   checklist, the skill tree, `mi-tooling.md`, and `proofs/activation-patching.md`;
   write down precisely what each checked box claims versus what exists. Then either
   (a) implement a small nnsight exercise with a proof note, or (b) mark nnsight and AtP
   deliberately out-of-scope with a dated justification in both checklist and skill tree
   — and qualify the phase-5 proof title so "Activation Patching" (implemented, exp4) is
   never readable as "AtP" (not implemented). *Done when* the 05 checklist has no
   checked box without an existing proof and no unchecked box without a stated reason,
   and the gate line is `[x]` with proof or `[~]` with the justification linked.
6. **Graph repair — MOCs and orphans** (1.5–2.5 h). The 04 MOC gains
   `notes/superposition-and-feature-capacity.md`; the 05 MOC gains the two audit proofs
   (`intervention-validity.md`, `superposition-setup-validity.md` — the most important
   artifacts in the vault and currently unindexed); the 06 MOC's placeholders become
   real links. Reconnect `references/` with inbound links so the "no orphan notes" rule
   holds, and rewrite `07_capstone/src/README.md` to point at the real `src/` layout
   instead of five modules that were never created there. *Done when* a grep for inbound
   links to `references/` finds them, each phase MOC lists every artifact in its folder,
   and `07_capstone/src/README.md` names no non-existent module.
7. **State/tag consolidation sweep** (1.5–3 h). The vault mixes frontmatter styles
   (`state: review` key vs `state/review` tag) and 17 notes still sit in review — all of
   Phase 4's load-bearing MI notes and three in a gate-complete Phase 2. Pick one
   canonical style; go note by note; consolidate to `state/consolidated` where the
   content is settled, or keep open deliberately with a dated reason and a live
   `#question`. *Done when* the postscript lists every note and its decision, and zero
   `state: review` notes remain in gate-complete phases without a recorded reason.
8. **Claim reconciliation sweep** (2–3 h). The root README and [[portfolio/README]] still
   say induction heads are "the strongest verified result" — no head has ever been
   detected; Rung 3 is the only fully verified headline. Fix both to the branch's actual
   headline; correct the stale `portfolio/mini-paper/` path to `portfolio/paper/`; amend
   the model card's aspirational "mean ± std over ≥3 seeds where applicable" to true
   coverage ("exp1/3/4/5 quick multiseed; exp2 pending GPU"); delete the dead
   "no seed-loop harness" sentence in [[04_conventions]]; and reconcile the test-count
   drift (158 vs 145) with a fresh `pytest --collect-only`, writing one canonical number
   into the Micro-Phase 8 note, the gate proof, and my postscript. *Done when* a grep for
   each stale phrase finds zero hits and one canonical test count appears in all three
   places.
9. **Mini-paper prose and `make paper`** (6–10 h, the largest item). Write every section
   of `portfolio/paper/main.tex` the tree says is writable: Introduction, Related Work,
   the tree-designated flagship section, Superposition, Patching, SAE, Limitations
   (expanded from the scaffold), Conclusion. Remove `% TODO` markers except the single
   deferred one the tree names — under A4, grokking is an explicit "deferred" paragraph,
   never a silence. Update the abstract per branch; add the missing `make paper`
   Makefile target (the checklist already claims it); and decide the relationship of
   `07_capstone/writeup.md` — outline becomes the paper's narrative companion, or a
   pointer. *Done when* `make paper` compiles, `main.tex` has zero unmarked TODOs, and
   every number in the prose matches a manifest-backed RESULTS.md row.

## 4. Strategic Tips and Architectural Best Practices

1. **The paper is a ledger, not a brochure.** Every sentence must survive the Honesty
   Ledger. When a number is absent, the prose says so — "not yet run" is a sentence;
   silence is a defect.
2. **Commit between exercises.** Manifests, the gate proof, and `verify-claims` all
   presuppose a clean committed tree. No exercise in this phase should finish inside a
   dirty worktree.
3. **The Decision Tree is binding.** Record the taken branch in the postscript before
   polishing prose. A later outcome may extend a branch; it may not rewrite it.
4. **Declare figure scale.** A regenerated figure is only honest if its scale is declared
   next to it: exp2's figures come from the P=29 quick test — full P=113 is ~5.5 h of
   CPU and is not the figure source. Quick where the number was quick.
5. **One grep, one sweep, one canonical count.** State/tag style, test counts, and
   phantom filenames each get one consolidated pass — five micro-fixes to the same thing
   are how drift comes back.
6. **Defer cleanly, name the deferral.** W&B tracking (tooling, not evidence — the paper
   cites manifests), the HF Spaces dashboard (needs a confirmed-head checkpoint first),
   FlashAttention/KV cache and RAG/LoRA (breadth items, no artifact in this phase's
   chain), ML system design (a capstone deliverable), automated circuit discovery
   (descoped 2026-08-01 — needs a real implementation project), and a thesis-scale paper
   (the mini-paper is the deliverable). Each is written down with a date so this roadmap
   does not quietly grow, extending Micro-Phase 9's deferral register.
7. **CI discipline.** markdownlint (MD013, line length 400), commitlint (header ≤ 121),
   ruff, pytest, and `make ci-check` must pass before anything reaches `dev → main`;
   conventional, GPG-signed commits throughout.

## Risks and Bottlenecks

- **Micro-Phase 9 never executes (no GPU).** Branch A4/B3 is taken; the grokking section
  is a marked placeholder; the paper is written around Rung 3 with Rung 1's
  fresh-vs-fixed finding as secondary. The tree is honored, not rewritten.
- **Figure regeneration wall-clock on CPU.** Mitigated by regenerating at
  reported-number scale and declaring the scale. Full-scale reruns are not the figure
  source.
- **The clean-clone gate surfaces a real defect.** Then the fix lands in the repo, not
  in the log — that is the gate proof's own rule. My honest prior: P(first-attempt
  green) ≈ 0.5, written down here so a failure is not a surprise.
- **Scope creep into Micro-Phase 9's runs.** The temptation, mid-consolidation, will be
  to re-trigger the GPU run or to "help" it with hyperparameters. The budget is fixed,
  the fallback ladder is fixed, and the tree is the contract.
- **LaTeX toolchain absent locally.** `make paper` either compiles or fails loudly. The
  prose is the deliverable and the PDF a bonus; whichever way it goes, it is recorded.
- **Count and claim drift reappearing.** The sweep's canonical counts are written into
  the postscript so the next micro-phase can diff against them.

## Predicted Outcomes (Pre-Registration)

Written 2026-08-02, before any work of this micro-phase:

- **Micro-Phase 9's runs:** I expect them not to have executed — no GPU in this
  environment. My honest prior: P(runs done before this phase's postscript) ≈ 0.2,
  which makes A4/B3 the most likely branch and Rung 3 the likely headline.
- **Phase 6 gate:** I expect the clean-clone run to take more than one attempt, with any
  failure being a genuine defect fixed in the repo. P(green on first attempt) ≈ 0.5.
- **exp5 seed harness:** the pattern is proven twice over (exp1/3/4); wiring exp5 into
  it is mechanical. P(3-seed manifest clean on first run) ≈ 0.8.
- **Phase 5 gate:** I expect to resolve the nnsight/AtP question as deliberate
  out-of-scope with a dated justification rather than implement nnsight, because the
  reframed phase focus is instrumentation that produced evidence. P(out-of-scope) ≈ 0.7.
- **The paper:** under A4/B3, every writable section has a manifest behind it and
  `make paper` compiles. P(zero unmarked TODOs) ≈ 0.9.
- **Success definition:** every Done-when met or its deferral named with a date; gate 6
  green; paper prose matching the branch actually taken; ledger entry appended. The
  micro-phase succeeds *even if Run A remains a placeholder* — that is the
  outcome-agnostic contract.

## Links

- [[portfolio/RESULTS]] — the evidence authority every exercise reconciles against
- [[08_micro-phase-09-the-flagship-runs]] — the runs this phase inherits through the tree
- [[07_micro-phase-08-evidence-pass]] — the pass that built the harness and the honesty infrastructure
- [[02_skill-tree]] — the boxes this phase earns the right to check
- [[03_progress-log]] — the dated journal this phase will enter
- [[01_roadmap]] — where this micro-phase sits in the full path
- [[06_production_ai/notes/results-manifests-and-provenance]] — the harness this phase runs on
- [[06_production_ai/proofs/reproducible-from-clean-clone]] — the gate-6 proof this phase passes
- [[07_capstone/research-plan]] — the capstone thesis this phase's paper serves
