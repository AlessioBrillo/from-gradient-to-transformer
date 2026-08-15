---
tags: [type/moc, phase/6, phase/7, research/experiment, state/review]
created: 2026-08-15
---

# Micro-Phase 37 — State Review and Roadmap: the sixth question, written from the release report

> **STATUS: REVIEW + ROADMAP, NOT A PRE-REGISTRATION.** This note is the
> companion review to [[00_meta/36_micro-phase-37-the-sixth-question]], the
> binding conditional draft: it opens no rows, launches no runs, claims no
> window, and is wired into home only as a companion pointer — it is not a
> pre-registration and is not counted against the cap. It is my personal
> state review and my
> step-by-step plan for the phase that starts at MP-37's Session 0, written
> in the same first-person register as my progress log so it doubles as the
> public record of how I reasoned about the bottleneck before I executed
> through it. Everything factual in this file was re-verified against the
> repository on 2026-08-15.

## Part I — Where I stand (state review, verified against the repo)

### The scientific ledger

The record's deepest fact has not changed and now has six dated confirmations
behind it: **no run in this repository's history has ever produced a sparse
Fourier solution.**

- P=59 drills dense 59/59; P=113's three-seed verdict is NO-GROK (val 1.0,
  k_99 = 111/113); the positive-control scan stamped **ALL-DENSE** at
  P=59/67/97 (harness-level negative, val 0.0000–0.0006, gen −1) — small P
  does not even reach the dense-generalizing regime.
- Microscope trial 1 **FALSIFIED** (embedding re-normalization is not the
  suppressor: k_99 = 112/113, val 0.7176). Trials 2 (`--schedule constant`,
  enabler landed TDD-first) and 3 (wd 1.5×) are pending in ADR-0003's budget.
- The R1 standard-scale ×3-seed run COMPLETED 2026-08-14 04:07 local: the
  scheduled no-head negative is now the verdict — 0/8 heads, peak diag+1
  mass 0.075 at epoch 499, peak val accuracy 0.5083 near epoch 1950,
  K-composition max 0.056; row 3's analysis and stamping are pending.
- `verify-claims` at **0**, re-verified in the MP-37 drafting sitting; exp2
  and exp5 manifests clean on disk.

The arc my science has taken is the strongest thing I own: *will grokking
reproduce?* (MP-28) → *is the harness itself the suppressor?* (MP-29) → *what
is the dense solution's structure?* (MP-29 S3's characterization, on disk) →
*which open question is deepest?* (C17/C18, MP-36's sitting) → *what does my
own phase map say about the boundary?* (C21–C24, this phase's sitting). A
negative that became a map, a map that became a characterization — the sixth
question is the first one I choose with a characterization already on the
record.

### The stack

MP-29 is current and mid-execution; **MP-30 through MP-36 stand
pre-registered, gated in series, the cap at seven**. Each phase's Session 0
consumes the previous phase's release report: no release, no phase. The
ledgers run ADR-0003 (MP-29, rows 3–7 in its window) through ADR-0010 (MP-36,
eight rows UNDECIDED). **ADR-0011's eight rows are the rows this roadmap will
fill** — exactly once, under the continuum law, sixth execution.

### The CI floor and the toolchains

190+ tracked tests, ruff, blocking mypy and markdownlint are green at the
last release. The verified gaps, stated as facts not hopes: no LaTeX
toolchain on this machine (`make paper` is graceful, not green), no Pages
deploy workflow in `.github/workflows/`, no `publish:` frontmatter policy,
`portfolio/projects/` empty, W&B never connected. Each is a dated row owned
by MP-30/31/34/35/36 — their residue, never my re-planning.

### The showcase corpus at intake

12+ provenance-guarded figures, the paper at v5/v6, the site and Space live
since the premiere, the essay annex at v5/v6, four runnable teaching
artifacts with stranger-run transcripts. My teaching lane ships the fifth
artifact this phase.

## Part II — The bottleneck analysis (what I must not let drift)

1. **The serialized stack is the critical path.** MP-29's release (terminus
   ≈ 2026-08-26) feeds MP-30's Session 0, which feeds MP-31's, and so on to
   MP-36. A slip at any link slides six phases; seven stacked phases was the
   exact drift the record named since MP-18, and the cap at seven is the
   mechanical refusal of it. **My highest-leverage act is protecting MP-29's
   window** — its release report is the artifact everything downstream
   consumes. Nothing in this phase may borrow a minute from it.
2. **The paper's compile gate is the hardest artifact in the stack.** No
   TeX on this machine; MP-31's own canon applies early: *toolchains are
   pinned in Session 0, never discovered at Session 7.* The paper v7 rule
   ("opens only for new numbers, else the v6 is the record") is my
   insurance — a dated sentence, never a silence.
3. **The standing debt is undated by design and must not survive the
   stack.** exp5 1000-epoch ×3-seed (~15 h), clean-clone proof, graduation
   proof, `reproduce-multiseed`, W&B, the gate-debt transcript — each owned
   by a named row in MP-30–MP-36. A pending item cannot outlive a ledger;
   row 8 of this phase re-verifies the closures with transcripts.
4. **The science's next fork is already visible.** MP-29 S3's dense
   characterization decides whether C18's reading has data; the R1 head
   verdict and microscope trials 2–3 decide which of C21/C22 survives. My
   candidate set is frozen precisely so this fork is adjudicated at Session
   0, never improvised.
5. **The showcase's receipts are still future.** Four stranger-run
   transcripts exist only if MP-33–MP-36 ship; C23 (the measured
   reproducibility rate) is conditioned on ≥ 4 transcripts on disk. The
   receipt compounds only if the lanes execute.
6. **The un-cap is the reward, not the norm.** This phase is the first
   roadmap written from a release report rather than from the habit of
   pre-registering. Its discipline — a DRAFT that opens no rows until
   Session 0 promotes it from MP-36's release report — is the cap's intended
   end state, executed exactly once.

## Part III — The roadmap, step by step (the continuum law, sixth execution)

### The frozen candidate set (chosen at Session 0, never improvised)

| # | Candidate | Opens only if | Why it would close |
|---|---|---|---|
| C21 | **The dense algorithm's computation** — read the P=113 solution as code: per-head Fourier dictionaries, norm structure vs the ideal full-support DFT expansion, frequency ablation, progress measures along the dense trajectory | MP-29 S3's dense characterization note on disk with manifest-tagged numbers (its checkpoints exist: `exp2_checkpoint_seed{0,1,2}.pt`) | A sparse cell exists anywhere → C17's successor owns the reading |
| C22 | **Finite-size scaling of the dense→memorized boundary** — boundary width and critical wd vs P, sharpening-with-P written before the analysis, the Morwani edge-of-stability check; analysis-only on the diagram's data plus one bounded confirmatory slice | ADR-0010 row 3 = C18 with monotone order-parameter curves on disk | C18 never opened, or its curves not monotone |
| C23 | **The stranger-run reproducibility rate, measured** — per-step pass/fail across the register's ≥ 4 transcripts; the verdict is a dated reproducibility report with a rate | ≥ 4 stranger-run transcripts on disk at S0 | Fewer than 4 → the receipt system hasn't earned a study |
| C24 | **The regime-resolved SAE map** — L0/FVE/dead-features as a function of solution regime, converting "SAEs struggle exactly where the circuit is dense" into a regime-labeled map | An SAE-on-dense evidence lane exists AND the diagram's checkpoints exist | A sparse regime exists → C21's successor owns it |

The likely survivor: **C21** — the record's signature arc completed (negative
→ map → characterization → mechanism), always CPU-runnable on checkpoints
that exist today, independent of every fork except the redemption. C22 is the
scientific successor if C18 delivered monotone order parameters; C23 is the
always-runnable fallback; C24 is the evidence lane.

### The nine sessions

1. **Session 0 (~1 h) — the gate truthing + the continuum choice.** Consume
   MP-36's release report row by row: ADR-0010 at zero UNDECIDED rows, the
   live URL re-clicked in the sitting, `verify-claims` at its actual count,
   the fourth teaching transcript on disk, `dev == main`. Commit the intake
   table before a single continuum row opens. Then the C21–C24 adjudication:
   each candidate's opening-or-closure memo in three sentences with a
   falsifier; exactly one opens as row 3; the unchosen close with one dated
   reason each, stamped in the same sitting. Open ADR-0011 with its eight
   rows, windows and kill-dates; declare the terminus (release = merge + 14
   calendar days); promote this draft into the roadmap, deviations recorded
   as dated ledger notes. *Exit: intake signed; row 3 chosen; ledger open.*
2. **Session 1 (~1 h) — the shelf baseline + the debt re-verification.**
   Row 5: hostile-webmaster walk of the live site + Space at zero (links,
   assets, a11y, orphans) — year five begins with a baseline. Row 8:
   W&B, clean-clone proof, graduation proof, `reproduce-multiseed` exp2/exp5,
   and the exp5 1000-epoch resolution — each cell LAUNCHED-with-transcript or
   CLOSED-with-one-reason; a claimed closure without its transcript stays
   open and blocks Session 8. *Exit: rows 5 and 8 stamped.*
3. **Session 2 (~1–2 h) — the consumed-verdict sitting (rows 1, 2).** Row 1:
   the fifth research question's verdict (ADR-0010 row 3) becomes the
   paper-v7 section, the annex table, or the results-page row — every number
   manifest-tagged, consumed in the sitting that owns it. Row 2: v7 opens
   only if row 1 lands new numbers; else "the v6 is the record" is the dated
   reason and `make paper` is re-verified against v6. Row 6's substitute
   filed from the visitor's chair, before the window opens (Ex-G). *Exit:
   rows 1 and 2 dated; substitute filed.*
4. **Session 3 (~2–3 h) — the essay annex v7.** `portfolio/essay-annex-7.md`:
   the fifth question's verdict set and the teaching lane's fourth receipt
   distilled into one dated annex; the reverse claims audit at zero (prose →
   manifest → command); each claim's "what would falsify this" column filled
   at writing time. The annex is amended, never rewritten. *Exit: row 4
   dated; audit at zero.*
5. **Session 4 (~1 h) — the stranger round 7 intake.** Row 6's window opens
   (intake S4, kill-date S5); the feedback-to-fixes matrix pre-stamped:
   friction point → cause → dated fix → re-check row. *Exit: window open,
   kill-date declared.*
6. **Session 5 (~2–3 h) — the research row pre-registration + launch + the
   teaching kickoff.** Row 3: the chosen candidate's protocol written before
   the first pass (site, metric, negative control, kill-date, falsifier
   column) and the run launched under a heartbeat. If C21: the per-head
   dictionary's support, the norm split vs the ideal expansion, and the
   ablation effect profile all written as falsifiable predictions before a
   single number is read (Ex-C, Ex-I, Ex-J). Row 6's kill-date honored
   (feedback → matrix drafted; silence → substitute closes it). Row 7: the
   fifth teaching artifact's skeleton drafted — walkthrough v5, 10-minute
   talk v5, or Colab grokking notebook v3 — with its ship-date. *Exit:
   row 3 pre-registered and launched; row 6 dated either way; row 7's
   skeleton drafted.*
7. **Session 6 (~1–2 h) — the research verdict sitting.** Row 3's verdict
   read from the manifest: completed and dated, or window closed and the
   scheduled negative is the result — drafted while the run was live (Ex-D),
   so this sitting is a stamping, not a discovery. *Exit: row 3 dated either
   way.*
8. **Session 7 (~2–3 h) — the shelf rehearsal + the re-check row + the
   teaching polish.** Row 5: the hostile-webmaster walk at zero beside the
   browser, every public number clicked back to disk. Row 6's re-check row
   dated. Row 7: the fifth artifact runs end to end on a stranger's machine
   (fresh clone / Colab session); the run transcript is the receipt; the
   teaching distillation (Ex-F) lands here. *Exit: rows 5, 6, 7 dated; the
   artifact shipped with its transcript.*
9. **Session 8 (~1 h) — the release.** ADR-0011 at zero UNDECIDED rows; the
   merge green locally and on GitHub; `dev == main`; home wired — this
   roadmap's draft status retired; the roadmap archived with its deviations,
   every deviation a dated ledger note. *Exit: the merge; the program's
   sixth dated direction, stamped in the same sitting.*

### The one measured line

ADR-0011 at **zero UNDECIDED rows** on release day, with exactly one LAUNCHED
research row whose verdict (or scheduled negative) re-derives from a
manifest; `verify-claims` at 0 with every public number re-derivable from one
command line; the hostile-webmaster walk at zero on the live shelf, year
five; the fifth teaching artifact shipped with a stranger-runnable
transcript; `dev == main` and the program's sixth dated direction.

## Part IV — Deep-dive study and research topics

The study I will do between now and the verdict sitting — each reading with
the paper, the one question it must answer, the prediction I write before a
single number is read, and the primary source on disk.

1. **The dense algorithm's computation (the C21 reading).** Elhage et al.,
   *A Mathematical Framework for Transformer Circuits* (2021) — per-head
   QK/OV decomposition, virtual weights, the residual stream as a
   communication channel — and Nanda et al., *Progress Measures for
   Grokking via Mechanistic Interpretability* (2023) — the addition table's
   DFT expansion, per-frequency progress measures, weight-decay-driven
   circuit formation. My C13/C14 verdicts and MP-29's S3 characterization
   note frame the reading. **Prediction to write before the analysis**: the
   per-head dictionary's support; the norm split vs the ideal full-support
   expansion; the ablation effect profile. **Primary sources**:
   `exp2_checkpoint_seed{0,1,2}.pt`, the phase-diagram manifest, the S3 note.
2. **Why the optimizer picks dense over sparse (my foundation study).** The
   Fourier dictionary is the null hypothesis of the whole phase: the ideal
   full-support DFT expansion of the addition table is *exact* — so the
   question is never "can a sparse circuit exist" but "which solution does
   the loss landscape reward". I will study sparse-representation theory —
   Donoho & Elad (2003) on uniqueness of sparse representations, the L1/L0
   equivalence, ISTA/FISTA (Beck & Teboulle 2009) — to state precisely why
   weight decay drives solutions toward L2-minimal dense Fourier codes
   rather than L1-minimal sparse ones. **Prediction**: the per-head norm
   structure will track the ideal expansion's energy profile, compressed by
   the K-composition. **Hand-built before reading anything**: Ex-I's
   ideal-expansion hand-roll and Ex-K's sparse-recovery toy.
3. **Phase boundaries and finite-size scaling (the C22 reading).** Order
   parameters, critical lines, boundary width vs P. Morwani et al. (2024)
   on the edge-of-numerical-stability regime, Gromov, *Grokking: A Memory
   Perspective* (2023), Power et al. (2022) — studied as theory before the
   order-parameter analysis is fixed, exactly as I studied the diagram's
   axes before its sweep grid. **Prediction**: sharpening-with-P and
   monotonicity, written with falsifiers; C18's monotone curves on disk are
   this reading's admission ticket.
4. **Shortcut learning and universality.** Liu et al., *Transformers Learn
   Shortcuts to Automata* (2023); Chughtai et al., *A Toy Model of
   Universality* (2023) — the vocabulary to say *why* the dense solution is
   dense honestly: is it a shortcut, or the canonical algorithm computed by
   a low-weight solution? This is the sentence C21's verdict must earn.
5. **SAE failure modes where the circuit is dense (the C24 reading).**
   Bricken et al. (2023); Cunningham et al. (2024) — L0/FVE/dead-features
   as regime labels, not just diagnostics. My Rung-5 datum (99.97% FVE,
   L0 = 136/256, 0% dead features on the 32-dimensional residual stream) is
   the record's first data point: dense-but-reconstructable is not
   sparse-but-interpretable, and I will write down what distinguishes the
   two before the map is drawn.
6. **Reproducibility science (the C23 reading).** Gelman & Loken, *The
   Garden of Forking Paths* — how a study of receipts is designed:
   failure-rate baselines, per-step pass/fail definitions, what a
   reproducibility rate actually claims. My four stranger-run transcripts
   are the data; I must decide what counts as a "step" and a "pass" before
   I count any.
7. **Negative results as maps, deepened.** How a characterized boundary is
   reported honestly — critical lines, order parameters, falsified
   predictions, the mapped negative as a contribution. If C21 opens, the
   paper's hardest paragraph claims the dense solution *computes something*;
   I will draft it against this reading (Ex-L) and let the manifest referee
   it.

## Part V — Documentation requirements (the contract)

Everything this phase claims re-derives from a manifest and a command. The
documentation I will write, and where:

- **This roadmap**, promoted from the draft at Session 0, rewritten from
  MP-36's release report, deviations recorded as dated ledger notes.
- **ADR-0011**, the sixth continuum ledger — eight rows pre-stamped with
  windows and kill-dates; rows 1–2 consumed from ADR-0010's verdicts; row 3
  the sixth research question with its protocol note and heartbeat; rows 4–8
  the continuum's decisions.
- **`portfolio/essay-annex-7.md`** — the v7 annex, manifest-tagged, amended
  never rewritten.
- **The paper v7 diff** (`portfolio/paper/main.tex` v7 + diff log) or the
  dated "the v6 is the record" memo; `make paper` re-verified in the CI
  mirror.
- **The shelf health sheet + hostile-webmaster transcript** (site + Space at
  zero, year five); the claims gate re-run on every merge.
- **`checklists/gate-debt.md`** — each cell's transcript or one-line reason,
  dated in Session 1, including the exp5 1000-epoch resolution's receipt.
- **The research row's pre-registration note** (site, metric, negative
  control, kill-date) in `06_production_ai/notes/` + the heartbeat artifact;
  if C21: the per-head dictionary figure spec written before the analysis,
  the figure itself manifest-tagged after.
- **The fifth teaching artifact + its stranger-run transcript** (fresh-clone
  or Colab session receipt).
- **`00_meta/03-progress-log`** — one dated entry per session; home wired at
  release; the continuum ledger's rows cited by the skill tree's publication
  flips.

## Part VI — Practical exercises and hands-on challenges

1. **Ex-A · The C21–C24 adjudication drill (S0):** each candidate's
   opening-or-closure memo in three sentences with a falsifier; exactly one
   opens; the unchosen close with one dated reason, stamped in the same
   sitting.
2. **Ex-B · The consumed-verdict reverse audit (S2):** every number from
   ADR-0010's row-3 verdict traced to its manifest and its command; the rest
   struck with a reason — the hostile-webmaster test of my own prose, fifth
   run.
3. **Ex-C · The falsifiable-prediction sprint (S5):** if C21 or C22 opens,
   the question's predictions written as falsifiable statements before the
   analysis — the dictionary's support, the norm split, sharpening with P —
   the "what would falsify this" column filled at writing time.
4. **Ex-D · The scheduled negative drafted before the run ends (S5):** the
   negative written while the run is live, so the S6 verdict sitting is a
   stamping, not a discovery.
5. **Ex-E · The hostile-webmaster walk v7 (S7):** the live site + Space at
   zero — links, assets, a11y, orphans, dead figures — walked as a complete
   transcript, year five.
6. **Ex-F · The teaching distillation, round five (S7):** the sixth
   question's verdict in four registers — the paper's sentence, the annex's
   sentence, the 30-second spoken claim, the 5-minute teaching explanation
   with a worked toy a stranger can run; the gap between the last two is
   where my teaching leaks.
7. **Ex-G · The stranger substitute from the visitor's chair (S2):** the
   self-review written from the chair a stranger would occupy — friction
   points → fixes → re-check row — filed before S4, so the S5 kill-date can
   never close the row with a skip.
8. **Ex-H · The fork drill (S2, verdict-agnostic):** the redemption (a
   sparse cell found) vs the all-dense future written as two one-page paths
   — what each verdict changes downstream, including the C21-vs-C22 choice —
   so next phase's S0 choice is a stamping, not a discovery.
9. **Ex-I · The ideal-expansion hand-roll (S5, before any number is read):**
   the ideal full-support DFT expansion of the addition table built by hand
   and script — its support, its norm structure, its per-frequency energy
   split — as the null hypothesis every checkpoint reading is measured
   against. One runnable check: the hand-rolled norm split printed and saved
   next to Ex-J's observed split, so the S6 comparison is a diff, not a
   memory.
10. **Ex-J · The per-head dictionary reader (S5, C21 only):** a small script
    that loads `exp2_checkpoint_seed{0,1,2}.pt`, composes each head's
    effective weight (embedding → attention → unembed), projects it onto the
    DFT basis, and emits per-head support, top frequencies and norms as a
    manifest-tagged JSON. One runnable check: the reader runs on the frozen
    checkpoint and its output is committed before the verdict paragraph is
    drafted.
11. **Ex-K · The sparse-recovery toy (new this phase, my foundation
    challenge):** a one-file toy that recovers the addition table's DFT
    coefficients under L2 vs L1 penalties — seeing with my own eyes why the
    L2-minimal solution is dense while the L1-minimal one is sparse, on the
    exact function the whole program has been chasing. One runnable check:
    the toy prints both reconstructions' sparsity and error on a fixed seed.
    This is the micro-scale intuition C21's verdict must not contradict.
12. **Ex-L · The "what does the dense solution compute?" sprint (S5, C21
    only):** the paper's hardest paragraph drafted at S5, then audited
    against the mechanism reading at S6 — prose that must survive contact
    with the manifest, the "computes something" claim earned or struck with
    one reason.
13. **Habit · The clock check (every session):** ADR-0011's undated rows,
    the open PR's CI status line, the shelf's health — all three before any
    new prose.

## Part VII — Strategic tips and architectural best practices

- **The one-question law, sixth execution.** A phase that opens two research
  questions is drift by another name; the unchosen candidates close in the
  same sitting as the choice. The continuum law is the mechanical refusal of
  this drift — proven executable five times, it must simply be executed
  again.
- **The candidate set is frozen before S0, never improvised at it.** C21–C24
  are conditions, not predictions; a sitting decides, it never invents.
- **Consumption is execution.** A verdict consumed into an artifact in the
  same sitting is a result; consumed into a paragraph written later it is a
  memory. Row 1 consumes ADR-0010's row-3 verdict in the sitting that owns
  it.
- **The receipt compounds.** The fifth runnable artifact is only worth
  shipping because the first four transcripts proved the format — and if C23
  opens, the receipts stop being anecdotes and become a measured rate. My
  showcase's story is now "read it, run it, watch me be wrong on the
  record," five receipts deep.
- **Toolchains are pinned in S0, never discovered at S7.** The paper's
  compile gate is the hardest artifact in the stack; the v7 rule ("opens
  only for new numbers") is the insurance that makes a missing toolchain a
  dated reason, not a crisis.
- **Protect the release report.** The serialized stack means MP-29's release
  is the artifact everything downstream consumes; a slip at any link slides
  six phases. The deepest law still applies: a promise can be re-planned
  forever, but a dated row is answered.
- **The S0 gate is a checklist with receipts.** ADR-0010 at zero, the live
  URL, `verify-claims` at 0, the fourth teaching transcript on disk — a
  condition with artifacts, not a paragraph.
- **The negative stays the signature.** The row that closes with one reason
  is stamped like the row that launched; if C21 opens, the dense mechanism
  reading is the strongest form of the record's signature: a negative that
  became a map, a map that became a characterization, and a characterization
  that became a mechanism.
- **The debt row re-verifies; it never re-does.** A stamped closure is
  re-checked with its transcript; a genuinely new debt cell is a NEW row,
  never a revision. A pending item cannot outlive a ledger.
- **Architecture laws unchanged.** `dev` only, GPG-signed, Conventional
  Commits with `(meta)`, `(portfolio)`, `(ci)` scopes; CI green before any
  merge; the floor re-verified locally before every push; zero UNDECIDED
  rows at Session 8; release = merge + 14 calendar days.
- **The showcase 30-second story:** *the program's sixth dated direction was
  written from its own release report — the cap honored, the stack executed,
  the record taught five times in runnable artifacts, and every public
  number still re-derives from one command line.* Every artifact this phase
  launches is written to that standard.

## Links

- [[00_meta/36_micro-phase-37-the-sixth-question]] — the binding conditional
  draft this review accompanies; its candidate set and sessions are this
  roadmap's frozen law.
- [[00_meta/35_micro-phase-36-the-fifth-question]] · [[docs/adr/0010-
  continuum-ledger-5]] — the release report and the ledger Session 0
  consumes row by row.
- [[00_meta/28_micro-phase-29-the-positive-negative]] ·
  [[06_production_ai/notes/microscope-trial-table]] ·
  [[06_production_ai/notes/positive-control-protocol]] ·
  [[06_production_ai/notes/dense-solutions-modular-addition]] — the science
  C21–C24 adjudicate over, whose pending verdicts are the intake.
- [[00_meta/03-progress-log]] — the dated journal this review will be
  answered in, session by session.