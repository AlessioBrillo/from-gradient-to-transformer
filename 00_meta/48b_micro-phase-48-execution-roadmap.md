---
tags: [type/moc, phase/6, phase/7, research/experiment, state/review]
created: 2026-08-18
---

# Micro-Phase 48 — Execution Roadmap (Architect's Review): the seventeenth question, from the reviewer's chair

> **STATUS: REVIEW + EXECUTION ROADMAP, NOT A PRE-REGISTRATION.** This note is
> the architect's companion to [[00_meta/48_micro-phase-48-review-and-roadmap]],
> the seventeenth question's review and roadmap: it opens no rows, launches no
> runs, claims no window, and is wired into home only as a companion pointer —
> it is not counted against any cap, because the cap is spent. It is my
> step-by-step execution plan for the phase that starts at MP-48's Session 0,
> written from the reviewer's chair in the same first-person register as my
> progress log so it doubles as the public record of how I reasoned about the
> program's steady state before I executed through it. The deepest law applies
> to my own document: this roadmap is written verdict-agnostic and re-plans not
> a single row of MP-29 through MP-47 — roadmaps are written from release
> reports, never from habit. Everything factual in this file was re-verified
> against the repository on 2026-08-18 in this drafting sitting: working tree
> clean, local `main` reconciled to `origin/main` at `2d3b238` (the MP-48
> squash, PR #82), `dev` at `426952e` (the reconcile merge), `git diff main
> dev` empty, 190 tracked tests collected, `verify-claims` at 0, ruff and
> blocking mypy green at the last release.

## Part I — Where I stand (state review, re-verified in this sitting)

### The record, in one breath

The record's deepest fact has not changed and still has ten dated
confirmations behind it, re-verified in this drafting sitting: **no run in
this repository's history has ever produced a sparse Fourier solution.** The
count advances only with a new verdict. The scientific ledger stands as
stamped: P=59 drills dense 59/59; P=113's three-seed verdict is NO-GROK (val
1.0, k_99 = 111/113); the positive-control scan stamped ALL-DENSE at
P=59/67/97; microscope trial 1 FALSIFIED (embedding re-normalization is not
the suppressor: k_99 = 112/113, val 0.7176); trials 2 (`--schedule constant`)
and 3 (wd 1.5×) remain pending in ADR-0003's budget; the R1 standard-scale
×3-seed run COMPLETED 2026-08-14 with the scheduled no-head negative as its
verdict (0/8 heads, peak diag+1 mass 0.075 at epoch 499, peak val accuracy
0.5083 near epoch 1950, K-composition max 0.056); the exp2 and exp5 manifests
are clean on disk and `verify-claims` is at **0**.

The arc my science has taken is the strongest thing I own: *will grokking
reproduce?* (MP-28) → *is the harness itself the suppressor?* (MP-29) → *what
is the dense solution's structure?* (MP-29 S3's characterization) → *which
open question is deepest?* → *what does my own phase map say about the
boundary?* → *which of the causal, circuit, law and rate questions does the
consumed verdict open?* — and by MP-48's Session 0 the record will hold
sixteen dated directions, a characterized dense regime, and the seventeenth
question: the fourth I choose with the fourth-generation arc consumption
stamped — or the seventh question past the record's closing sentence.

### What I verified myself in this sitting (the hostile-webmaster walk, my own transcript)

| Fact | Verified state (2026-08-18) |
|---|---|
| Test suite | 190 collected via `pytest --collect-only`; full suite green at the last release |
| Branches | `dev` current at `426952e`; `git diff main dev` empty; `origin/main` at `2d3b238` (the MP-48 squash, PR #82) |
| Working tree | Clean |
| `docs/adr/` | 0001–0010 only; ADR-0011 through ADR-0021 open at their own Session 0s; **ADR-0022 is this phase's ledger** |
| `figures/` | Zero tracked files (gitignored build product, provenanced by the manifests, never by git) |
| Rung 6 residue | Confirmed on disk: `figures/exp6_automated_vs_manual.png` + `src/experiments/__pycache__/exp6_automated_circuit.cpython-312.pyc` — MP-47's Session 1 owns the removal with a transcript; this phase re-verifies the absence |
| `checklists/` | Only `reproducibility-checklist.md`; `gate-debt.md` still absent — a dated fact, never a silence |
| `portfolio/README.md` | Still stale: the three "not yet" rows contradict the record (paper v8–v15 arc, site and Space live since the premiere, manifest machinery since Micro-Phase 8) |
| CI | `python-ci.yml` (ruff, blocking mypy allowlist, non-blocking full-tree mypy, pytest + coverage), `markdown-lint.yml`, `conventional-commits.yml`; no Pages deploy workflow; no LaTeX toolchain locally (`make paper` graceful, not green) |
| Ledger | ADR-0003 rows 3–7 still carry UNDECIDED cells — the R1 verdict stamp, the R4/R5 scheduled negatives, the paper prose and the graduation proof must be dated before MP-29's Session 8, or the entire stack stalls |

## Part II — The bottleneck analysis (what I must not let drift)

1. **The intake is a consumption eight generations deep.** MP-48's Session 0
   consumes MP-47's Session-0 decision with dates — never re-litigates it.
   The single most dangerous drift remains re-opening candidates a consumed
   decision already closed with dated reasons, or treating "the post-record
   arc governs" as a mood instead of as a stamped verdict. The decision chain
   is eight generations deep; a sitting stamps, it never re-decides.
2. **The stacked execution is still the critical path — and it is genuinely
   blocked.** MP-48's Session 0 awaits the stack (MP-29 → MP-30 through
   MP-47), and the stack awaits MP-29's release (terminus ≈ 2026-08-26). The
   highest-leverage act is unchanged: protect MP-29's window. The corollary I
   must not miss is that **the waiting window is mine to schedule** — the
   study lane (Session −1 below) is the honest answer to the week I cannot
   yet spend on Session 0, so no day between now and the stack's release is
   unowned.
3. **The ledger is the schedule, and ADR-0003 still carries UNDECIDED rows.**
   The R1 run *completed* 2026-08-14, but rows 3–5 have not been stamped with
   their verdicts (the no-head negative for row 3; the scheduled negatives
   for rows 4–5). MP-29's Session 8 requires zero UNDECIDED rows; a slip here
   slides the whole stack. I do not re-plan those rows — but the waiting
   window pre-drafts the *prose* of those scheduled negatives so the stamping
   sitting is a stamping, never a discovery.
4. **The microscope budget is one failure away from exhaustion.** Trial 2's
   verdict forces trial 3's choice (the ledger's "my own third"); three
   failures close row 2 and make the dense characterization the phase's
   headline. Verdict-agnostic readiness means: **trial 3's pre-registration
   is drafted now, in the waiting window, with its falsifier column already
   filled** — so no sitting ever chooses an improvised third trial.
5. **The CPU wall is the science's binding constraint.** Every pending run
   (trial 2, trial 3, the characterization's per-head dictionaries and
   ablations) shares one CPU and overnight windows. The characterization
   study is heavier than the trials; its wall-clock must be budgeted before
   it is launched, with a checkpoint/resume heartbeat, or the release date
   slips. Budget the wall-clock at launch, never at Session 7.
6. **The steady state must not become ceremony.** MP-48 is the eleventh
   roadmap written from an *executed* roadmap's release report — the
   program's normal, confirmed eleven times. The countermeasure is concrete:
   **every session's exit names at least one artifact changed on disk, and
   every row is dated in the sitting that owns it** — a stamped row with no
   science behind it is ceremony by another name.
7. **The paper's compile gate is the hardest artifact in the stack.** No TeX
   on this machine — verified again in this sitting. The v18 rule ("opens
   only for new numbers, else the v17 is the record") is my insurance; the
   toolchain decision (local MiKTeX/TeX Live vs. Overleaf) is pinned at
   Session 0, never discovered at Session 7.
8. **Stop-and-publish is a row, not a threat.** ADR-0004 row 5 stays open as
   the program's honest exit: a phase is worth doing only if its candidate
   set can earn a paragraph the record does not already have. If the
   post-record arc governs, the deepest candidate earns the post-record
   arc's *sixth new paragraph* — the record's closing sentence consumed seven
   times, never repeated. The deepest form of laziness is building what the
   record has already said.

## Part III — The roadmap, step by step

### The frozen candidate set (chosen at Session 0, never improvised)

| # | Candidate | Opens only if | Why it would close |
|---|---|---|---|
| C65 | **The law as a theory** — the boundary's failure cells *explained*, not merely mapped: the per-head mechanism at the fourth unseen task family's and the second architecture family's failure cells predicted in writing, causally verified by patching, the law's domain statement closed with its theory of failure — a law whose failure cells are explained is a theory | ADR-0021 row 3 = C61 with a positive verdict (the law with a measured domain on disk) | C61 closed negative, or the post-record arc governs |
| C66 | **The principle's exception map** — the driver's break-map cells *root-caused*: where the loss-landscape → weight-norm → sharpening chain fails, a dated mechanism for every cell of the full P×wd diagram and both architecture families, each exception ablated | ADR-0021 row 3 = C62 with the driver named and causally verified on disk | C62 never opened, or its verdict was negative |
| C67 | **The rate as a policy** — the eleventh reproducibility study: the sixth drift measurement after the dated root-cause fix, the rate function's parameters re-estimated from the receipt system's history, the next measurement's schedule *allocated from the model* | ADR-0021 row 3 = C63 with the fifth measurement and attribution on disk AND ≥ 17 stranger-run transcripts at S0 | Fewer than 17 transcripts, or C63 never opened |
| C68 | **The instrument as a standard** — the third-edition course *validated a third time by the uninvited under a public rubric*: the rubric pre-registered with its scoring rule, the feedback-to-fixes matrix's second prediction round checked against the third cohort's friction | ADR-0021 row 3 = C64 with the fourth cohort's measured outcome on disk | C64 never opened, or a sparse regime exists |

The universal override stands: **if any sparse cell (k_99 < P/2 sustained ≥ 3
checkpoints) exists anywhere on the record by Session 0, the sparse-regime
mechanism — the Nanda-style per-frequency reading on the first sparse
solution this harness ever produced — owns the question and all four
candidates close with that verdict.**

The terminal-state override stands, now eight generations deep: **if MP-47's
Session 0 consumed MP-46's decision with dates and the post-record arc
governs, then MP-48's Session 0 consumes the sixth post-record question's
verdict from ADR-0021 row 3 and continues the post-record arc, choosing the
seventh post-record question from the pre-registered continuation set
(PR-19 the new harness's second cross-recipe law; PR-20 the law at the
record's edge, seventh task; PR-21 the record as a course, sixth edition).**

The likely survivor, written as a condition chain, never a prediction: if
MP-47's Session 0 continued the post-record arc → **the post-record
continuation**; else if C61 landed positive → **C65** — the law as a theory,
always CPU-runnable on checkpoints that exist today; else if C62's driver
verdict landed → **C66**; else **C67** (always-runnable, the showcase's own
science, receipts now seventeen deep); C68 is the evidence lane and the
teaching lane's anchor.

### The ten sessions

1. **Session −1 (~1 h/day, now → MP-29's release) — the waiting-window study
   lane.** The days before the stack releases are owned, not idle. Each day:
   one study block from Part IV (reading → prediction written *before* the
   reading → one-page memo filed in the study log), the clock-check habit,
   and one waiting-window exercise (Part VI, Ex-α through Ex-ζ). Deliverables:
   the trial-3 pre-registration drafted verdict-agnostic with its falsifier
   column filled; the R4/R5 scheduled-negative prose pre-drafted; the S0
   intake checklist pre-built with empty date cells; the C65–C68
   opening-or-closure memo skeletons; the Ex-T execution-memo skeleton. All
   saved beside MP-29's lanes, never inside them. *Exit: the study log has
   one dated entry per day; the pre-drafts exist on disk; no row of MP-29
   through MP-47 was touched.*
2. **Session 0 (~1 h) — the gate truthing + the seven-generations-deep arc +
   the continuum choice.** Consume MP-47's release report row by row:
   ADR-0021 at zero UNDECIDED rows, the live URL re-clicked in the sitting,
   `verify-claims` at its actual count, the sixteenth teaching transcript on
   disk, `dev == main` (branch list as the transcript). Commit the intake
   table before a single continuum row opens. Then Ex-T: consume MP-47's
   Session-0 decision with dates — the seventh-generation consumption — and
   adjudicate C65–C68 (exactly one opens as row 3; the unchosen close with
   one dated reason each) or continue the post-record arc. Open ADR-0022 with
   its eight rows, windows and kill-dates; declare the terminus (release =
   merge + 14 calendar days); promote this roadmap from MP-47's release
   report, deviations recorded as dated ledger notes. **The toolchain
   decision is pinned here** (TeX choice; `make paper` re-verified in the CI
   mirror). *Exit: intake signed; row 3 chosen; ledger open.*
3. **Session 1 (~1 h) — the shelf baseline + the debt re-verification.** Row
   5: hostile-webmaster walk of the live site + Space at zero (links, assets,
   a11y, orphans) — extended to the repo's own shelf: local `main`
   re-verified reconciled to `origin/main` (branch list as the transcript),
   `portfolio/README.md`'s staleness verified closed (MP-47's Session 1 owned
   the first fix; this sitting verifies the file is current), the exp6
   residue removed with a transcript, the annexes' location verified. Row 8:
   MP-47's stamped closures re-verified (W&B, clean-clone proof, graduation
   proof, `reproduce-multiseed` exp2/exp5, the exp5 1000-epoch resolution, the
   README fix, the residue removal) — each cell LAUNCHED-with-transcript or
   CLOSED-with-one-reason; a claimed closure without its transcript stays
   open and blocks Session 8; `gate-debt.md`'s absence, if still absent,
   recorded with a date. *Exit: rows 5 and 8 stamped.*
4. **Session 2 (~1–2 h) — the consumed-verdict sitting (rows 1, 2).** Row 1:
   the sixteenth research question's verdict (ADR-0021 row 3) becomes the
   paper-v18 section, the annex table, or the results-page row — every number
   manifest-tagged, consumed in the sitting that owns it; if the post-record
   arc governs, the post-record statement is framed from MP-47's release,
   never rewritten. Row 2: v18 opens only if row 1 lands new numbers; else
   "the v17 is the record" is the dated reason and `make paper` is re-verified
   against v17. Row 6's substitute filed from the visitor's chair, before the
   window opens (Ex-G); the fork drill (Ex-H) and the arc consumption (Ex-N
   through Ex-T) land here. *Exit: rows 1 and 2 dated; substitute filed;
   Ex-T's execution memo on disk.*
5. **Session 3 (~2–3 h) — the essay annex v18.** `portfolio/essay-annex-18.md`
   (its home on the live shelf, dated): the sixteenth question's verdict set
   and the teaching lane's sixteenth receipt distilled into one dated annex;
   the reverse claims audit at zero (prose → manifest → command); each
   claim's "what would falsify this" column filled at writing time. The annex
   is amended, never rewritten. *Exit: row 4 dated; audit at zero.*
6. **Session 4 (~1 h) — the stranger round 18 intake.** Row 6's window opens
   (intake S4, kill-date S5); the feedback-to-fixes matrix pre-stamped:
   friction point → cause → dated fix → re-check row. *Exit: window open,
   kill-date declared.*
7. **Session 5 (~2–3 h) — the research row pre-registration + launch + the
   teaching kickoff.** Row 3: the chosen candidate's protocol written before
   the first pass (site, metric, negative control, kill-date, falsifier
   column) and the run launched under a heartbeat — or, if the post-record
   arc governs, the continuation row's protocol opened under the same
   discipline. If C65: the failure cells at the fourth unseen task family and
   the second architecture family, and the expected per-head mechanism
   written as falsifiable predictions before a single number is read (Ex-C,
   Ex-I, Ex-J, Ex-S, Ex-U, Ex-W). The scheduled negative is drafted *while
   the run is live* (Ex-D), so the S6 verdict sitting is a stamping, not a
   discovery. Row 6's kill-date honored (feedback → matrix drafted; silence →
   substitute closes it). Row 7: the seventeenth teaching artifact's skeleton
   drafted — walkthrough v17, 10-minute talk v17, or Colab grokking notebook
   v15 — with its ship-date. *Exit: row 3 pre-registered and launched (or the
   post-record protocol opened); row 6 dated either way; row 7's skeleton
   drafted.*
8. **Session 6 (~1–2 h) — the research verdict sitting.** Row 3's verdict
   read from the manifest: completed and dated, or window closed and the
   scheduled negative is the result. *Exit: row 3 dated either way.*
9. **Session 7 (~2–3 h) — the shelf rehearsal + the re-check row + the
   teaching polish.** Row 5: the hostile-webmaster walk at zero beside the
   browser, every public number clicked back to disk; the repo-shelf findings
   re-checked (local `main` reconciled, README current, residue gone, annexes'
   home verified). Row 6's re-check row dated. Row 7: the seventeenth artifact
   runs end to end on a stranger's machine (fresh clone / Colab session); the
   run transcript is the receipt; the teaching distillation (Ex-F) lands
   here. *Exit: rows 5, 6, 7 dated; the artifact shipped with its transcript.*
10. **Session 8 (~1 h) — the release.** ADR-0022 at zero UNDECIDED rows; the
    merge green locally and on GitHub; `dev == main`; home wired — this
    roadmap's companion status retired; the roadmap archived with its
    deviations, every deviation a dated ledger note. If the post-record arc
    governs, this sitting stamps the post-record arc's seventh dated
    direction — the record's closing sentence consumed seven times, never
    repeated. *Exit: the merge; the program's seventeenth dated direction —
    or the post-record arc's seventh.*

### The one measured line

ADR-0022 at **zero UNDECIDED rows** on release day, with exactly one LAUNCHED
research row (or the post-record continuation row) whose verdict (or
scheduled negative) re-derives from a manifest; `verify-claims` at 0 with
every public number re-derivable from one command line; the hostile-webmaster
walk at zero on the live shelf and on the repo's own shelf (local `main`
reconciled, README current, residue removed, the debt ledger present or
absent-with-date); the seventeenth teaching artifact shipped with a
stranger-runnable transcript; `dev == main` and the program's seventeenth
dated direction — or, if the post-record arc governs, its seventh dated
direction.

## Part IV — Deep-dive study and research topics

The study I will do between now and the verdict sitting — each reading with
the paper, the one question it must answer, the prediction I write before a
single number is read, and the primary source on disk. Filed as one dated
memo each in the study log (Session −1).

1. **The law as a theory (the C65 reading).** Elhage et al., *A Mathematical
   Framework for Transformer Circuits* (2021) for the QK/OV machinery the
   causal claim is made over; Wang et al., *Interpretability in the Wild*
   (2022) for activation-patching methodology at per-head resolution; Conmy
   et al., *Towards Automated Circuit Discovery* (2023) for turning a
   hand-traced mechanism into a scalable, testable procedure (read, never
   re-implemented — ACDC stays descoped); Varma et al., *Explaining grokking
   through circuit efficiency* (2023) for why circuits grow sharp and where
   that sharpness is measurable; Olsson et al., *In-context Learning and
   Induction Heads* (2022) for what transfers across task families; Chughtai
   et al., *A Toy Model of Universality* (2023) for why the fourth unseen
   task family's and the second architecture family's failure cells fail the
   way they do. **Prediction to write**: which per-head role's failure
   mechanism is the boundary's root cause at the fourth unseen task's
   structure and at the second architecture family's, and what the patching
   at those cells reveals; the null hypothesis every measured fingerprint is
   compared against. **Primary sources**: the frozen checkpoints, C61's
   law-domain table, the S3 note.
2. **The principle's exception map (the C66 reading).** Lyu et al.,
   *Understanding the training dynamics of transformers on modular
   arithmetic* (2024) for the loss-landscape structure of grokking and its
   phase transitions; Morwani et al. (2024) on the edge-of-numerical-
   stability regime; Gromov, *Grokking: A Memory Perspective* (2023); Power
   et al. (2022); Nanda et al. (2023) — now read at the *exception* axis:
   whether the loss-landscape → weight-norm → sharpening chain's ablation
   signature survives every cell of the full P×wd diagram and both
   architecture families, what a dated negative at any link means for the
   principle, and where "the driver" is really an optimization artifact that
   does not survive the second family. **Prediction**: the break-map cells'
   root causes written before the analysis; C62's named driver and its dated
   break-map are this reading's admission ticket.
3. **The rate as a policy (the C67 reading).** Gelman & Loken, *The Garden
   of Forking Paths*; Pineau et al. (2021); Kapoor & Narayanan,
   *Reproducibility in Machine Learning: A Systematic Literature Review*
   (2023); the ML reproducibility line (NASEM's five pillars) — now read at
   the *allocation* axis: what a sixth drift measurement after the dated fix
   validates about the rate function's parameters, how a schedule derived
   from a model differs from a schedule kept by habit, and what a policy can
   honestly claim that a model cannot. My seventeen stranger-run transcripts
   are the data; I must decide what counts as the eleventh measurement before
   I measure any.
4. **The instrument as a standard (the C68 reading).** Bricken et al.
   (2023); Cunningham et al. (2024); the dictionary-circuit and
   feature-universality line — plus the education-measurement line (rubric
   validity, test-retest reliability, external assessment) for what a *third,
   uninvited cohort's* outcome under a *public rubric* claims that a second's
   does not, and what a rubric must contain to be a public scoring rule
   rather than a private one. My Rung-5 datum (99.97% FVE, L0 = 136/256, 0%
   dead features) is the record's first data point.
5. **The post-record program, seventh generation (new, deepest).** Lakatos,
   *The Methodology of Scientific Research Programmes* (1978) — read an
   eighth time, now for the *seventh* question past a completed program:
   progressive vs. degenerating problem shifts when the *sixth* post-record
   verdict lands, Kuhn's normal science as the post-record arc's axioms, and
   the honest criterion for the seventh post-record question. This reading
   feeds Ex-T and the Session-0 question MP-48 owns more deeply than any
   phase before it.
6. **The record teaches, round seventeen.** The seventeenth verdict in four
   registers — the paper's sentence, the annex's sentence, the 30-second
   spoken claim, and the 5-minute teaching explanation with a worked toy a
   stranger can run (Ex-F). The gap between the last two is where my teaching
   leaks, and I will measure it deliberately by writing all four registers for
   the same verdict. **Waiting-window rehearsal**: run the four registers on
   the R1 no-head negative — a stamped verdict, safe to practice on.
7. **The redemption reading, or negative results as maps, the seventeenth
   pass.** If a sparse cell exists by S0: Nanda et al.'s full per-frequency
   reading on the first sparse solution this harness ever produced. If not:
   how the *completed* law is reported honestly — the law's domain closed
   with its measured boundaries and its failure cells explained or mapped,
   the driver a principle or a case study with a dated exception map, the
   negative as a contribution. Either way, the paper's hardest paragraph is
   the one that claims the dense solution *computes something*; I will draft
   it against this reading and let the manifest referee it.
8. **The mathematical bedrock (new).** Before any per-head analysis: derive
   by hand the DFT of the modular-addition table — why its support is full
   (all P frequencies), why Nanda et al.'s sparse solution reaches the same
   function with ~√P frequencies and specific phase structure, and what the
   convolution theorem implies about the dense regime's factorization. This
   is the one derivation that makes every later fingerprint interpretable
   rather than decorative. **Primary sources**: Nanda et al. (2023) and its
   appendix; my own `01_foundations` linear-algebra proofs; the exp2 Fourier
   instrument on disk. **One runnable check**: the hand derivation reproduced
   in a one-file script whose DFT output matches `results/exp2_grokking.json`'s
   k_99 = 111/113 at P=113.
9. **Experiment design under a CPU budget (new).** Re-read my own canon —
   `06_production_ai/notes/checkpoint-resume-durability`,
   `multi-seed-experiment-design`, `scheduled-negatives-mp28` and the
   kill-drill proof — as the specification for every run this phase launches:
   wall-clock budget at launch, heartbeat artifact, checkpoint-every-500,
   scheduled negative drafted while the run is live. A run without a budget
   row is drift by another name.
10. **The science of the negative (new).** The chain I am building toward is
    the strongest form of the signature: a negative that became a map, a map
    that became a characterization, a characterization that became a
    mechanism, a mechanism that earned its causal verdict, a circuit that
    earned its complete reading, a circuit that earned its law, a law that
    predicted an unseen point, **a law whose failure cells are explained — or
    a record that knew when to end.** Study how completed negative programs
    are reported at the frontier so the paper's hardest paragraph earns its
    claim or is struck with one reason.

## Part V — Documentation requirements (the contract)

Everything this phase claims re-derives from a manifest and a command. The
documentation I will write, and where:

- **The Session −1 study log** (new): one dated entry per study block —
  reading, prediction written before the reading, one-page memo, where it was
  filed. This is the record of the waiting window and the phase's first
  showcase artifact.
- **The trial-3 pre-registration draft + R4/R5 scheduled-negative prose**
  (new, verdict-agnostic): saved beside MP-29's lanes, never inside them;
  each with its falsifier column filled at writing time.
- **This roadmap**, promoted from the companion review at Session 0,
  rewritten from MP-47's release report, deviations recorded as dated ledger
  notes.
- **ADR-0022**, the seventeenth continuum ledger — eight rows pre-stamped
  with windows and kill-dates; rows 1–2 consumed from ADR-0021's verdicts;
  row 3 the seventeenth research question with its protocol note and
  heartbeat (or the post-record continuation row's protocol); rows 4–8 the
  continuum's decisions.
- **`portfolio/essay-annex-18.md`** — the v18 annex, manifest-tagged,
  amended never rewritten; the annexes' home (the live shelf) recorded with
  a date.
- **The paper v18 diff** (`portfolio/paper/main.tex` v18 + diff log) or the
  dated "the v17 is the record" memo; `make paper` re-verified in the CI
  mirror with the toolchain decision pinned at Session 0.
- **The shelf health sheet + hostile-webmaster transcript** (site + Space at
  zero), extended to the repo's own shelf: local `main` reconciled to
  `origin/main`, `portfolio/README.md` current, the exp6 residue removed, the
  annexes' location verified; the claims gate re-run on every merge.
- **`checklists/gate-debt.md`** — each cell's transcript or one-line reason,
  dated in Session 1; the file's absence, if still absent, recorded with a
  date.
- **The research row's pre-registration note** (site, metric, negative
  control, kill-date) in `06_production_ai/notes/` + the heartbeat artifact;
  if C65: the law-theory figure spec written before the analysis, the figure
  itself manifest-tagged after. If the post-record arc governs: the
  continuation row's protocol note instead.
- **The seventeenth teaching artifact + its stranger-run transcript**
  (fresh-clone or Colab session receipt).
- **Ex-T's execution memo** — MP-47's arc decision run with dates, written
  verdict-agnostic in Session 2 and executed at Session 0.
- **`00_meta/03-progress-log`** — one dated entry per session; home wired at
  release; the continuum ledger's rows cited by the skill tree's publication
  flips.

## Part VI — Practical exercises and hands-on challenges

### The waiting window (Session −1 — all safe on stamped verdicts and study, none touch MP-29's rows)

1. **Ex-α · The DFT-of-addition hand-roll (new).** Derive the addition
   table's DFT support by hand for P ∈ {5, 13, 59, 113}; reproduce Nanda et
   al.'s √P sparse-support claim; write the one-file script whose output must
   match the manifest's k_99 = 111/113 at P=113. This is the mathematical
   bedrock of every fingerprint C65–C68 will read.
2. **Ex-β · The four-registers rehearsal (new).** Take the R1 no-head
   negative (stamped 2026-08-14) and write it in four registers — the paper's
   sentence, the annex's sentence, the 30-second spoken claim, the 5-minute
   teaching explanation with a worked toy. Measure the gap; the phase's Ex-F
   repeats the drill on the seventeenth verdict.
3. **Ex-γ · The scheduled-negative drafting drill (new).** Draft the prose of
   ADR-0003 rows 4–5's scheduled negatives and trial 3's pre-registration —
   verdict-agnostic, falsifier column filled — so the stamping sittings are
   stampings, never discoveries.
4. **Ex-δ · The stranger-run drill on my own receipt (Ex-M's rehearsal).**
   Execute the most recent shipped teaching artifact on a fresh clone as if I
   were the stranger; the transcript becomes the baseline the seventeenth
   artifact's transcript is compared against.
5. **Ex-ε · The trial-3 falsifier table (new).** Before trial 2's verdict is
   read, write what each of trial 2's outcomes means for trial 3's choice —
   the decision tree is the drill; the ledger row is the outcome.
6. **Habit · The clock check (every session, from today).** ADR-0022's
   undated rows, the open PR's CI status line, the shelf's health — all three
   before any new prose.

### The phase's exercise contract (Sessions 0–8, from the companion draft, executed as pre-registered)

| # | Exercise | Session | Covers |
|---|---|---|---|
| Ex-A | The C65–C68 adjudication drill — exactly one opens, the unchosen close with one dated reason each | S0 | the continuum choice |
| Ex-B | The consumed-verdict reverse audit — every number traced to its manifest and its command, the rest struck with a reason | S2 | the hostile-webmaster test of my own prose |
| Ex-C | The falsifiable-prediction sprint — predictions written as falsifiable statements before the analysis, falsifier column filled at writing time | S5 (C65/66) | prediction discipline |
| Ex-D | The scheduled negative drafted before the run ends | S5 | stamping, not discovery |
| Ex-E | The hostile-webmaster walk v18 — site + Space + repo shelf at zero, as a complete transcript | S7 | the showcase's honesty |
| Ex-F | The teaching distillation, round seventeen — the verdict in four registers | S7 | the teaching lane |
| Ex-G | The stranger substitute from the visitor's chair — filed before S4, so the S5 kill-date can never close the row with a skip | S2 | the stranger lane |
| Ex-H | The fork drill, deepest form — continuing vs. post-record states as two one-page paths | S2 | verdict-agnostic planning |
| Ex-I / Ex-S / Ex-U | The boundary hand-roll, the out-of-sample sprint, the architecture-family sprint — dated prediction tables before any number is read | S5 (C65) | hand-rolled fingerprints, diffs not memories |
| Ex-J | The transfer reader — loads the frozen checkpoints, runs the per-head extraction and patching machinery, emits the failure-cell table as manifest-tagged JSON | S5 (C65) | the machinery |
| Ex-K | The sparse-recovery toy, eleventh pass — L2 vs L1 DFT recovery across two architecture families | S−1/S5 | micro-scale intuition C66 must not contradict |
| Ex-L | The "what does the dense solution compute?" sprint — the paper's hardest paragraph drafted at S5, audited at S6 | S5/6 (C65) | the earned claim |
| Ex-N … Ex-R, Ex-T | The arc consumption, generations 2–7 — the chain executes with dates, criteria cited, never re-decided | S0 | the terminal-state object |
| Ex-Q / Ex-V / Ex-Y | The drift-attribution drills and the policy allocation drill — components attributed before any fix, schedules derived from the model | S5 (C67) | the rate as a policy |
| Ex-W / Ex-X / Ex-Z | The theory's falsifier column, the exception-map hand-roll, the public rubric draft — each with its falsifier at writing time | S5 (C65/66/68) | the new drills |

## Part VII — Strategic tips and architectural best practices

- **The one-question law, seventeenth execution.** A phase that opens two
  research questions is drift by another name; the unchosen candidates close
  in the same sitting as the choice — and the arc consumption may close all
  of them with the post-record verdict. The continuum law is the mechanical
  refusal of this drift — proven executable sixteen times, it must simply be
  executed again.
- **The candidate set is frozen before S0, never improvised at it.** C65–C68
  are conditions, not predictions; a sitting decides, it never invents. The
  terminal-state object is the hardest frozen object on the record: written
  by MP-40, executed by MP-41, consumed six more times since — consumed a
  *seventh* time by MP-48, never re-negotiated in the consuming sitting.
- **Consumption is execution.** A verdict consumed into an artifact in the
  same sitting is a result; consumed into a paragraph written later it is a
  memory. Row 1 consumes ADR-0021's row-3 verdict in the sitting that owns it
  — or the post-record statement, if the arc governs.
- **The receipt compounds.** The seventeenth runnable artifact is only worth
  shipping because the first sixteen transcripts proved the format. My
  showcase's story is now "read it, run it, watch me be wrong on the record,"
  seventeen receipts deep.
- **The waiting window is a lane, not a gap.** The days between this draft
  and the stack's release are the study lane (Session −1) — readings with
  predictions, hand-derivations, pre-drafted scheduled negatives. A day with
  no dated entry is a row without a date.
- **Budget the wall-clock at launch, never at Session 7.** The CPU is the
  binding constraint; every run gets a budget row, a heartbeat, a
  checkpoint-every-500, and a scheduled negative drafted while it is live.
  This is the architecture law that protects the release date.
- **Toolchains are pinned in S0, never discovered at S7.** The paper's
  compile gate is the hardest artifact in the stack; the v18 rule is the
  insurance that makes a missing toolchain a dated reason, not a crisis.
- **Protect the release report.** The serialized stack means MP-29's release
  is the artifact everything downstream consumes; a slip at any link slides
  the whole chain. A promise can be re-planned forever, but a dated row is
  answered.
- **The S0 gate is a checklist with receipts.** ADR-0021 at zero, the live
  URL, `verify-claims` at 0, the sixteenth teaching transcript on disk — a
  condition with artifacts, not a paragraph.
- **The negative stays the signature.** The row that closes with one reason
  is stamped like the row that launched; the R1 no-head negative — 0/8
  heads, stamped 2026-08-14 — is the record's newest dated signature. The
  strongest form of the signature is the chain: negative → map →
  characterization → mechanism → causal verdict → circuit → law → theory —
  or a record that knew when to end.
- **The steady state is the reward, not the ceremony.** MP-48 is the
  eleventh roadmap written from an *executed* roadmap's release report — the
  program at its normal, confirmed eleven times. The machinery is the
  guardrail, never the goal: rows are dated in the sitting that owns them, or
  they are not rows.
- **Architecture laws unchanged.** `dev` only, GPG-signed, Conventional
  Commits with `(meta)`, `(portfolio)`, `(ci)` scopes; CI green before any
  merge; the floor re-verified locally before every push; zero UNDECIDED rows
  at Session 8; release = merge + 14 calendar days.
- **The showcase 30-second story:** *the program's seventeenth dated
  direction was written from its own release report — the cap honored, the
  stack executed, the steady state kept honest eleven times, the record
  taught seventeen times in runnable artifacts, every public number still
  re-derives from one command line, and the record consumed — seven times,
  with dates — its own terminal-state decision, and answered it in a
  release.* Every artifact this phase launches is written to that standard.

## Links

- [[00_meta/48_micro-phase-48-review-and-roadmap]] · [[00_meta/47_micro-phase-47-review-and-roadmap]] —
  the seventeenth question's review and roadmap; this roadmap's intake is
  ADR-0021's release report and MP-47's Session-0 decision, which Session 0
  consumes again.
- [[00_meta/46_micro-phase-46-review-and-roadmap]] · [[00_meta/45_micro-phase-45-review-and-roadmap]] —
  the fifteenth and fourteenth questions' reviews and roadmaps, the un-cap's
  steady state confirmed eleven times.
- [[docs/adr/0004-horizon-ledger]] — the horizon rows, including row 5
  (stop-and-publish), the honest exit every candidate must beat — and the row
  the terminal state executes.
- [[06_production_ai/notes/dense-solutions-modular-addition]] ·
  [[06_production_ai/notes/microscope-trial-table]] ·
  [[06_production_ai/notes/positive-control-protocol]] — the science C65–C68
  adjudicate over, whose pending verdicts are the intake.
- [[06_production_ai/notes/results-manifests-and-provenance]] — the manifest
  machinery every public number cites.
- [[06_production_ai/notes/checkpoint-resume-durability]] ·
  [[06_production_ai/notes/scheduled-negatives-mp28]] — the CPU-budget canon
  the phase's runs are specified against.
- [[00_meta/03-progress-log]] — the dated journal this review will be
  answered in, session by session.
