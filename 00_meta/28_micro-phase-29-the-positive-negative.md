---
tags: [type/moc, phase/6, phase/7, research/experiment, state/review]
created: 2026-08-12
---

# Micro-Phase 29 — The Positive-Negative: the verdict earns its proof

Written as a personal learning log and a public record, like every roadmap before it.

MP-28 executed the unblock: the exp2 port landed with falsification tests first,
the P=113 lane ran three seeds to 5000/5000 epochs under the frozen protocol,
and the verdict is in — **NO-GROK, a positive-negative**. Val accuracy reached
1.0 across all three seeds, but the Fourier representation stayed dense
(k_99 = 111/113): the model solved modular addition at P=113 *without* forming
the sparse circuit the protocol defines as grokking. The machine, the pipeline
and the checkpoint machinery all worked; the phenomenon did not appear.

That verdict is the center of gravity of this phase, and it re-orders the
science. Before any claim about grokking can be made, one question dominates
every other: **does this harness ever produce a sparse solution at all?** The
record already holds the deepest clue — the P=59 probe drills from MP-27 were
dense too (59/59 frequencies). A codebase that has never seen k_99 < P/2 in
any run, at any P, cannot attribute its negatives to the phenomenon; the
harness itself is the prime suspect until it is cleared. This phase therefore
opens with a **positive control**, runs the microscope lane to its dated
terminus, and then — whatever the control says — turns the dense solution
itself into the contribution: a full characterization of the algorithm the
model actually computed, with the same polish as the sparse story would have
had.

## Where this phase starts (state review, verified against the repo 2026-08-12)

I checked the tree, the manifests, the ledger rows and the CI floor before
writing a single claim here.

- **Tree state**: `dev` clean at the MP-28 verdict merge; MP-28 current with
  Sessions 0–2 done (port, drill, launch) and Sessions 4–8 open — its own
  residue rows (R1 verdict, R4/R5 chain, paper prose, release) are this
  phase's intake, per the record's law that a session is not over while a row
  it owns is undated.
- **ADR-0003**: row 1 stamped (LAUNCHED 2026-08-11, NO-GROK, val 1.0, Fourier
  dense, k_99 = 111/113, gen epochs 1250/1048/1326); row 2 in flight (trial 1
  `--no-normalize-embeddings`); rows 3–7 UNDECIDED.
- **The manifests**: `results/exp2_grokking.json` exists but carries
  `git_dirty: true` (`git_sha d48f9ad`) — the manifest was produced mid-phase
  against an uncommitted tree, and `make verify-claims` correctly refuses it.
  `results/exp1_induction_heads.json` is the old sub-standard run
  (epochs=150, d_model=24, final acc ≈ 0.004) — the standard-scale multi-seed
  manifest does NOT exist. `results/exp5_sae_dashboard.json` does not exist.
- **The CI floor**: `make verify-claims` at **3 problems** (dirty-tree exp2
  manifest; Rung 2 section tag missing; Rung 5 section tag missing) — not the
  2 designed ones: the dirty-tree row is this phase's first cleanup. The
  tracked 185 tests, ruff, blocking mypy and markdownlint baselines were all
  green at MP-28's release and nothing has changed under them since.
- **The scientific ledger across all runs to date**: no run in this
  repository's history has ever produced a sparse Fourier solution — P=59
  drills (dense 59/59), P=113 × 3 seeds (k_99 = 111/113). This is the fact
  the positive control exists to explain.

## Design decisions

- **Positive control first (the phase's spine).** Session 1 hunts for ANY
  configuration under which this codebase produces k_99 < P/2 — a small-P
  scan (P=59/67/97, one seed each, the frozen protocol minus one variable).
  If small P is also dense, the harness itself is the suspect and the phase
  pivots to root-cause diagnosis (the normalization/loss/schedule chain read
  as code, not as hope) — and no P=113 microscope trial is worth its wall
  time until that question is answered. The control's verdict is dated before
  the microscope spends its three-trial budget ([[06_production_ai/notes/positive-control-protocol]]).
- **The microscope runs to a terminus, not a schedule.** ADR-0003 row 2's
  ≤ 3 single-variable trials each carry a pre-registered prediction and a
  falsification column written before the run starts
  ([[06_production_ai/notes/microscope-trial-table]]); the third trial is
  chosen with a one-line justification when trials 1–2 land. The planned
  third: weight decay 1.5×, the norm-pressure hypothesis, pending what the
  control says. Three failed trials close the row with one reason — the dated
  negative is the result.
- **The dense solution is a contribution, not a footnote.** The phase's
  scientific output is the characterization of the dense-generalizing
  solution: per-head Fourier dictionary of the P=113 checkpoints, norm
  structure against Nanda et al.'s sparse solution, frequency ablation, and
  an SAE reading of the dense residual stream with an honest L0/FVE delta
  ([[06_production_ai/notes/dense-solutions-modular-addition]]). The public
  sentence the record ships is: *"grokking modular addition at P=113 was not
  reproduced under this protocol on this machine within this window; here is
  the algorithm the model found instead."*
- **Rows close the day they are decided (ADR-0003 law, executed).** A session
  is not over while a row it owns is undated; zero UNDECIDED rows at
  Session 8. MP-28's residue (rows 3–7) is this phase's intake, folded in
  exactly as MP-23 consumed MP-22's record.
- **The continuum law, applied again.** Zero new research questions open this
  phase. ADR-0006's candidate set stays frozen; the open questions of the
  dense reading either become dated rows or close with one named reason.
- **Negative-first, falsification-first (inherited, now load-bearing).** Every
  number this phase reports gets its "what would falsify this" column before
  the number exists — the microscope trials, the control scan, and the R1
  verdict all ship their negatives pre-drafted (MP-28's scheduled-negatives
  file is the template, and Negative 2 — "no head at standard scale" — is
  still live until row 3 is stamped).
- **The one measured line**: `make verify-claims` from its current **3**
  problems to **0** — the dirty-tree manifest re-derived on a clean tree
  first, then the Rung 2 and Rung 5 tags, then the standard-scale R1
  manifest. `verify-claims` at 0 is the proof, not the prose.
- **The terminus is stamped at Step 0**: release = this roadmap's merge +
  14 calendar days. MP-28's release (its merge + 14 days) is consumed first;
  the phase ships whatever the rows decided, and the residue is a dated list,
  never a silence.

## Session 0 — the disk truth (2026-08-12, ~1 h) — next

- The manifests re-read as data: exp2's dirty-tree flag explained and fixed —
  the manifest producer is deterministic given the checkpoints, but the
  rolling `checkpoints/` directory was cleaned after the verdict (verified
  absent 2026-08-12), so re-derivation now requires a re-run of the P=113
  × 3 seeds launch (~2 h on this machine's own CPU budget, the protocol that
  already ran once). S0 either launches that re-run as the dated option — it
  doubles as the positive-negative's reproducibility check, the strongest
  claim the record can ship — or records the 3-problem state as the line
  until the R1/R5 lanes produce their manifests. Re-derivation is allowed,
  editing is not.
- The R1 standard-scale checkpoint set located on disk: if the run's rolling
  checkpoints exist, the analysis queue is set; if the run died or never
  launched, it is resumed under checkpoint-every-250 or re-launched with a
  dated PID — either way the row gets its heartbeat before the session ends.
- The positive-control protocol pre-registered in full
  ([[06_production_ai/notes/positive-control-protocol]]): P set, budget,
  threshold (k_99 < P/2 sustained ≥ 3 checkpoints), the one-change rule, and
  the decision tree for a harness-level negative.
- The CI floor re-verified locally: tracked tests green, ruff clean, blocking
  mypy clean, markdownlint 0 on changed notes.
- **Exit**: audit sheet signed; the exp2 line either re-running (dated PID) or
  recorded as-is; the control is launched or dated.

## Session 0 executed — deviation log (2026-08-13)

- **Deviation 1 (disk truth)**: the P=113 final checkpoints were NOT cleaned —
  `checkpoints/exp2_checkpoint_seed{0,1,2}.pt` (2026-08-11 20:37) are on disk.
  S0's binary resolves as re-derivation, not re-run: the manifest producer is
  deterministic given the checkpoints, so `results/exp2_grokking.json` is
  re-derived on a clean tree (minutes) and the NO-GROK row keeps its
  reproducibility receipt without a ~2 h re-launch.
- **Deviation 2 (R1, checkpoint cadence)**: the 2026-08-11 R1 launch died at
  ~epoch 242 with NO checkpoint under checkpoint-every-250 (the first save
  would have been at 250) — the single worst-case outcome the cadence
  allowed, realized. Relaunched 2026-08-13 13:29 local at
  **checkpoint-every-100**, explicit standard-scale flags (NO `--standard`:
  it forces `save_manifest=True` and parallel seeds would race on one file),
  `--fresh-batches --resume`, OMP_NUM_THREADS=3 per seed (9/12 threads),
  workers PID 15100/15940/18212, logs `checkpoints/exp1_seed{0,1,2}.log/.err.log`.
  Observed ~27 s/epoch → ETA ~22 h wall (13:29 local Aug 13 → ~12:00 local
  Aug 14), inside the pre-registered 17–24 h window.
- **Trial 1 decided early**: the microscope trial-1 resume (P=113 seed 0,
  `--no-normalize-embeddings`, 5000 epochs) completed 14:30 local — val
  0.7176, gen epoch −1, k_99 = 112/113. Verdict stamped **FALSIFIED**
  (renormalization not the suppressor) in
  [[06_production_ai/notes/microscope-trial-table]] — the trial enters the
  table in the sitting that decided it, one sitting ahead of S2's schedule.
- **Trial 2 enabler landed**: `--schedule constant` via the
  `make_lr_scheduler` factory — falsification tests first
  (`test(grokking)` 82fb216, RED ImportError), implementation
  (`feat(grokking)` 1479c5d, all 20 grokking tests GREEN). Trial 2 can launch
  on the control's verdict.
- **Control scan launched** 14:37 local: P=59/67/97, seed 0 each, 2000
  epochs, `--no-normalize-embeddings`, checkpoint-every-200,
  `--resume`, dedicated dirs `checkpoints/control_p{59,67,97}/`, workers PID
  1840/5240/8372 (3 threads each), logs `checkpoints/control_p{P}.log/.err.log`.
  ~1 h wall expected; verdict dated in S1's sitting.
- **CI floor at session start**: `make verify-claims` 3 problems (unchanged);
  tracked tests, ruff, mypy, markdownlint green.

## Session 1 — the positive control (next)

- The small-P scan runs: P=59/67/97, one seed each, frozen protocol minus one
  variable, checkpoint-every-200, under the kill conditions signed in S0.
- Reading the scan: any k_99 < P/2 sustained is the harness cleared at small
  P; all-dense is the harness-level negative with the code-path root-cause
  reading (the renormalization/loss/schedule chain, read as code).
- **Exit**: the control verdict row dated, either way; the microscope's trial
  order re-confirmed or re-ordered with a one-line justification.

## Session 2 — the microscope to terminus (next)

- ADR-0003 row 2's three trials, each with its pre-registered prediction and
  falsification column: (1) `--no-normalize-embeddings` (the flag exists since
  MP-28; the trial's result table is what was missing); (2) constant LR — the
  small `--schedule constant` flag lands first as a recorded experiment-code
  change; (3) the third, chosen with one-line justification at trials 1–2.
- **Exit**: ADR-0003 row 2 stamped — the trial-results table, or the dated
  negative with the one sentence the record is entitled to: the named
  suspects were tested and did not rescue the run.

## Session 3 — the dense solution, characterized (next)

- The P=113 checkpoints read as the algorithm: per-head Fourier dictionary,
  frequency amplitudes against the ideal dense solution and Nanda's sparse
  one, norm structure per layer, the embedding-renormalization interaction.
- Frequency ablation on the dense circuit (the exp2 instrument already
  exists) and the SAE reading of the dense residual stream vs the synthetic
  baseline — the honest L0/FVE/dead-features delta, in the record's tone.
- **Exit**: the characterization note written with every number
  manifest-tagged; the "what would falsify this reading" column filled for
  each claim.

## Session 4 — the R1 verdict (next)

- The standard-scale fresh-batches analysis from disk: per-head diag+1 mass,
  sustained ≥ 5 checkpoints vs the 0.3 threshold; the fixed-vs-fresh context
  (52.2% vs 0.05% at matched 800 epochs) cited as the record's own baseline.
- **Exit**: ADR-0003 row 3 stamped with dates and the seed count — a head
  formed, or the no-head negative printed as the contribution it was drafted
  to be.

## Session 5 — the R4/R5 chain (next)

- Real head: activation + path patching with self-patch-exact-zero as the
  falsification (the unit tests are the harness), then the SAE re-run on the
  confirmed-head checkpoint with the honest delta vs the 53% baseline.
- No head: the scheduled negatives ARE the result — patching validated only
  by unit tests, the SAE re-run on the best-available checkpoint, honest
  delta reported either way.
- **Exit**: ADR-0003 rows 4–5 stamped.

## Session 6 — verify-claims 0 + the paper's first prose (next)

- `make verify-claims` at **0** — the phase's one measured line, on disk:
  exp2 re-derived clean, exp1 standard-scale multi-seed manifest,
  exp5 real-activations manifest, Rung 2 and Rung 5 tags in RESULTS.md.
- The paper's Grokking section written from disk — its gate (an exp2 manifest
  existing) is open, and the positive-negative is the section's honest spine;
  the Induction section follows as row 3 allows; the essay annex v1.1 cites
  only manifests.
- **Exit**: ADR-0003 row 6 stamped; paper sections cite only disk.

## Session 7 — the graduation proof (next)

- The capstone gate answered from the phase's own numbers: the Fourier +
  progress-measures + causal-ablation assembly, with the dense reading as the
  honest answer — or closed with its dated reason.
- **Exit**: ADR-0003 row 7 stamped.

## Session 8 — the release (the fixed terminus date)

- All ADR-0003 rows stamped; the merge green locally and on GitHub;
  ADR-0006's candidate set untouched — zero new research questions opened
  this phase; the residue is a dated list.
- **Exit**: the merge; this roadmap wired into home as the executed record.

## Gate criteria (pre-registered, from the sessions above)

1. S0: verify-claims at its 2 designed problems (dirty-tree fixed); R1
   heartbeat dated; control protocol signed — audit sheet committed.
2. S1: the control verdict dated, either way, with its decision tree applied.
3. S2: ADR-0003 row 2 stamped with the trial-results table or the dated
   negative.
4. S3: the dense-solution characterization note written, manifest-tagged,
   falsification columns filled.
5. S4: ADR-0003 row 3 stamped with dates, either way.
6. S5: ADR-0003 rows 4–5 stamped.
7. S6: `make verify-claims` at 0; paper prose cites only manifests.
8. S7: row 7 stamped; S8: zero UNDECIDED rows; the merge green; the phase
   wired into home.

## The one measured line (status)

`make verify-claims` — currently 3 problems (dirty-tree exp2 manifest, Rung 2
tag, Rung 5 tag). Line moved: 3 → 2 in S0 (the exp2 line, by re-run or by
recorded decision — the checkpoints needed for pure re-derivation were
cleaned, verified 2026-08-12), 2 → 0 by S6 (the R1 and R5 manifests land
from this phase's own runs).

Updated 2026-08-13 (S0 executed): 3 → 1 in this sitting — the exp2 manifest
re-derived on a clean tree (checkpoints found on disk, deviation 1) and the
Rung 2 rewrite carries its `<!-- manifest: exp2_grokking -->` tag; the Rung 5
tag lands with the exp5 manifest once its synthetic run completes (the
real-activation manifest remains a pending row — Session 5's R5 chain — and
the Rung 5 tag will back the synthetic numbers only, with the honest delta
noted, per the record's tone). Rung 1's standard-scale manifest remains
pending on R1's verdict (Session 4).

## Deep-dive study plan

1. **The Fourier theory of modular addition** (Nanda et al., *Progress
   Measures for Grokking via Mechanistic Interpretability*, 2023): the DFT of
   the embedding, k_99, the n₀ = (P−1)/2 frequency dictionary, why ~√P
   frequencies implement addition exactly — and why the ideal full-support
   (dense) solution also generalizes. The question at the center: which
   regime did my run land in, and what selects between them?
2. **Why dense wins here**: weight decay × cosine-schedule interplay (Gromov,
   *Grokking: A Memory Perspective*, 2023), the edge-of-numerical-stability
   regime (Morwani et al., 2024), and embedding renormalization as a
   *nonlinear* constraint on the sparse solution's norm structure — studied
   as theory before any code is touched.
3. **Shortcut learning vs canonical circuits** (Liu et al., *Transformers
   Learn Shortcuts to Automata*, 2023) and universality baselines (Chughtai
   et al., *A Toy Model of Universality*, 2023): is the dense solution a
   shortcut, or a legitimate alternative algorithm with its own
   structure worth mapping?
4. **Induction heads at scale** (Olsson et al., *In-Context Learning and
   Induction Heads*, 2022): diag+1 mass, prefix matching, fresh-batches
   dynamics, the reported d_model ≈ 128 formation floor — the R1 lane's
   reading list.
5. **Causal intervention methodology**: activation vs path patching (Wang et
   al., *Interpretability in the Wild*, 2022; Elhage et al., 2021), with
   self-patch-exact-zero as the falsification the unit tests already encode.
6. **SAEs on real activations** (Bricken et al., 2023; Cunningham et al.,
   2023): FVE, L0, dead features — and what a dense residual stream means
   for feature discovery. Prediction to test: sparse autoencoders struggle
   exactly where the circuit is dense.
7. **Epistemics**: Gelman & Loken's garden of forking paths (the record's
   standing countermeasure), positive-control-first methodology, and how
   negative results ship in MI literature — the phase's spine is also its
   study topic.

## Documentation contract

- This roadmap, pre-registered (the file you are reading).
- [[06_production_ai/notes/positive-control-protocol]] — the control-first
  methodology note, signed in S0.
- [[06_production_ai/notes/microscope-trial-table]] — the 3-trial A/B scaffold
  with predictions written before the trials.
- [[06_production_ai/notes/dense-solutions-modular-addition]] — the
  characterization study note (the phase's scientific center).
- ADR-0003 rows 2–7 stamped with dates and one-line reasons; ADR-0001/0002
  untouched; ADR-0006 frozen.
- `portfolio/RESULTS.md`: Rung 2 rewritten as the positive-negative with its
  manifest tag; Rung 1 and Rung 5 tags; the home page's headline line
  ("not yet reproduced") replaced by the dated verdict.
- `portfolio/paper/main.tex`: Grokking section prose (first), Induction as
  rows allow; every number manifest-tagged.
- `00_meta/03_progress-log`: one dated entry per session; this roadmap wired
  into home on release.

## Practical exercises and challenges

1. **Ex-A · Audit the auditor**: implement the DFT and k_99 computation
   independently and verify the verdict script's criterion against the raw
   checkpoints. The NO-GROK verdict must survive a second, hand-built
   instrument.
2. **Ex-B · Predict-the-knob A/B**: pre-registered predictions for all three
   microscope trials before they run; score yourself after. The
   falsification-first muscle, trained on my own work.
3. **Ex-C · The two-hour positive-control hunt**: find any config in this
   repository that produces k_99 < P/2 — or write the dated proof that none
   exists. The harness-level verdict is mine to produce, not to outsource.
4. **Ex-D · The dense reading**: SAE on dense-solution activations vs the
   synthetic baseline; the honest L0/FVE/dead-features delta paragraph, in
   the record's exact tone.
5. **Ex-E · Path-patching drill**: `test_self_patching_is_a_no_op` as the
   harness, then a manual single-head patch decomposing direct vs mediated
   effects.
6. **Ex-F · The verdict table**: the 5-column decision table — what single
   observation would flip the NO-GROK verdict, and what it changes
   downstream. The negative's falsification, pre-registered like its
   positive twin.

## Strategic tips and architectural best practices

- **The ladder of attribution: harness → protocol → phenomenon.** The P=113
  finding attributes nothing until S1's positive control clears the harness —
  the highest-value sentence in the phase, and the one that separates this
  record from a notebook.
- **The negative is the product.** "Not reproduced under this protocol; here
  is the algorithm the model found instead" is a stronger portfolio piece
  than a re-run — it demonstrates instrumentation, discipline and honest
  closure, and it is the public signature of this vault.
- **One measured line per phase.** Every session gate is a row stamp or a
  manifest, never prose. Numbers live in `results/*.json`, cited by
  `<!-- manifest: -->` tags; `verify-claims` is the referee.
- **Machine discipline.** Checkpoint everything, kill conditions signed
  before launch, heartbeats as data, no overnight launch without a resume
  plan (the exp2 port made that promise mechanical; the drill proved it).
- **Architecture laws, unchanged.** `dev` only, GPG-signed, Conventional
  Commits with `(grokking)`, `(meta)`, `(paper)` scopes; CI green before any
  merge; the CI floor is re-verified locally before every push; zero
  UNDECIDED rows at Session 8.
- **The showcase 30-second story**: *the pipeline worked perfectly and
  produced a genuine negative, then I characterized the alternative
  algorithm it found.* Every artifact this phase writes — the control verdict,
  the trial table, the dense reading, the paper section — is written to that
  standard.

## Links

- [[00_meta/27_micro-phase-28-the-execution]] — the roadmap this phase
  consumes; its sessions 4–8 residue is this phase's intake.
- [[docs/adr/0003-research-return-ledger]] — the rows this phase stamps;
  row 1's verdict is the intake.
- [[06_production_ai/notes/grokking-verdict-p113]] — the verdict note this
  phase's science extends.
- [[06_production_ai/notes/scheduled-negatives-mp28]] — the pre-drafted
  negatives, kept or struck by the R1 lane.
- [[06_production_ai/notes/positive-control-protocol]] ·
  [[06_production_ai/notes/microscope-trial-table]] ·
  [[06_production_ai/notes/dense-solutions-modular-addition]] — the phase's
  three support notes.
- [[06_production_ai/notes/results-manifests-and-provenance]] ·
  [[06_production_ai/notes/multi-seed-experiment-design]] — the manifest
  machinery every number cites.
- [[00_meta/03_progress-log]] — the dated journal entries per session.
- [[portfolio/RESULTS]] · [[portfolio/paper/main]] — the artifacts this
  phase's manifests unblock.
