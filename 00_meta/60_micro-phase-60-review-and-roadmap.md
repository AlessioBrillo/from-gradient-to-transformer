---
tags: [type/moc, phase/6, phase/7, research/experiment, state/review]
created: 2026-08-19
---

# Micro-Phase 60 — State Review and Execution Roadmap (Architect's Review): the twenty-ninth question, written from the twenty-eighth release report

> **STATUS: REVIEW + EXECUTION ROADMAP, NOT A PRE-REGISTRATION.** This note is
> the architect's companion to [[00_meta/59_micro-phase-59-review-and-roadmap|MP-59]],
> the twenty-eighth question's review and roadmap: it opens no rows, launches no
> runs, claims no window, and is wired into home only as a companion pointer —
> it is not counted against any cap, because the cap is spent. It is my
> step-by-step plan for the phase that starts at MP-60's Session 0, written
> from the reviewer's chair in the same first-person register as my progress
> log so it doubles as the public record of how I reasoned about the program's
> steady state while MP-59's waiting window was still open. The deepest law
> applies to my own document: this roadmap is written verdict-agnostic and
> re-plans not a single row of MP-29 through MP-59 — roadmaps are written from
> release reports, never from habit. Everything factual in this file was
> re-verified against the repository on 2026-08-19 in this drafting sitting:
> working tree clean, `main` at `f53ff47` (the MP-59 squash merge, PR #94),
> `origin/dev` at `e0f7995` (the reconcile merge, remote-only at intake — a
> dated deviation from the record's "local dev" sentences, recorded here
> honestly, never as a reconciled silence), **190 tests PASSED in this
> drafting sitting (402 s)**, ruff clean, blocking mypy clean, `verify-claims`
> at 0, markdownlint at 0 issues on 237 tracked files, full-tree mypy at the
> dated 176-error count (re-verified under the pinned toolchain, no crash),
> `figures/` holding no untracked residue, `docs/adr/` holding 0001–0010,
> ADR-0003 rows 3–7 still UNDECIDED, `portfolio/README.md`'s three "not yet"
> rows still contradicting the record.

## Part I — Where I stand (state review, re-verified in this sitting)

### The scientific ledger

The record's deepest fact has not changed and still carries every dated
confirmation the record holds, re-verified in this drafting sitting: **no run
in this repository's history has ever produced a sparse Fourier solution.**
The count advances only with a new verdict; between MP-59's sitting and this
one, no new Fourier cell landed — the microscope's trials 2 and 3 remain
pending in ADR-0003's budget, and the dense characterization remains the
phase's headline unless one of them rescues the run.

- P=59 drills dense 59/59; P=113's three-seed verdict is NO-GROK (val 1.0,
  k_99 = 111/113); the positive-control scan stamped **ALL-DENSE** at
  P=59/67/97 (harness-level negative, val 0.0000–0.0006, gen −1); microscope
  trial 1 **FALSIFIED** (embedding re-normalization is not the suppressor:
  k_99 = 112/113, val 0.7176); trials 2 (`--schedule constant`) and 3
  (wd 1.5×) pending in ADR-0003's budget; and the R1 standard-scale ×3-seed
  run COMPLETED 2026-08-14 with the scheduled no-head negative as its verdict
  (0/8 heads, peak diag+1 mass 0.075 at epoch 499, peak val accuracy 0.5083
  near epoch 1950, K-composition max 0.056). The R1 verdict remains the
  newest dated fact on the record's negative side.
- All five manifests are on disk (`results/exp1…exp5`), and `verify-claims`
  is at **0** — re-verified in this sitting.

The arc my science has taken is the strongest thing I own: *will grokking
reproduce?* (MP-28) → *is the harness itself the suppressor?* (MP-29) → *what
is the dense solution's structure?* (MP-29 S3's characterization, on disk) →
*which open question is deepest?* (MP-36's sitting) → the question chain from
MP-37's sitting through MP-54's sitting → *which of C93–C96 does the consumed
twenty-fourth verdict open?* (MP-55's sitting) → *which of C97–C100 does the
consumed twenty-fifth verdict open?* (MP-56's sitting) → *which of C101–C104
does the consumed twenty-sixth verdict open?* (MP-57's sitting) → *which of
C105–C108 does the consumed twenty-seventh verdict open?* (MP-58's sitting) →
*which of C109–C112 does the consumed twenty-eighth verdict open — or is the
eighteenth post-record question the post-record arc's own successor?* (MP-59's
sitting). By MP-60's Session 0 the record will hold twenty-eight dated
directions, a characterized dense regime (or the sparse redemption), whichever
of C109–C112 ADR-0033's sitting chose — and the answer to the question MP-59's
Session 0 owned more deeply than any phase before it: **whether the post-record
arc governs and, if it does, what the eighteenth post-record question was.**
The twenty-ninth question is the fifteenth I choose with the fourteenth-
generation arc consumption *stamped* — or the nineteenth question past the
record's closing sentence.

### What I verified myself in this sitting (the hostile-webmaster walk, my own transcript)

| Fact | Verified state (2026-08-19) |
|---|---|
| Test suite | **190 PASSED in this drafting sitting (402 s)**, green |
| Branches | `main` at `f53ff47` (the MP-59 squash merge, PR #94); `origin/dev` at `e0f7995` (the reconcile merge, remote-only at intake); `git diff main origin/dev` empty |
| Working tree | Clean |
| `docs/adr/` | 0001–0010 only; ADR-0011 through ADR-0030 open at their own Session 0s; ADR-0031 through ADR-0033 are MP-57/58/59's ledgers; **ADR-0034 is this roadmap's ledger** |
| `figures/` | **No untracked products** — the exp6 residue's absence, previously a scheduled row, is now a verified fact |
| `checklists/` | Only `reproducibility-checklist.md`; `gate-debt.md` still absent — a dated fact, never a silence |
| `portfolio/README.md` | Still stale: the three "not yet" rows contradict the record (paper through the v26 arc, site and Space live since the premiere, manifest machinery since Micro-Phase 8) — a ten-phase-standing row; this roadmap's Session 1 re-verifies the closure |
| `portfolio/projects/` | Figures only, no project write-ups (`.gitkeep` and nothing else) |
| CI | `python-ci.yml` (ruff, blocking mypy allowlist, non-blocking full-tree mypy, pytest + coverage), `markdown-lint.yml`, `conventional-commits.yml`; no Pages deploy workflow; no LaTeX toolchain locally (`make paper` graceful, not green) |
| mypy strict debt | **176 errors** in the non-blocking full-tree lane, re-verified identical in this sitting (no crash) — owned by no named row yet; this phase's Session 1 records the dated decision |
| The capstone | `07_capstone/src/` and `experiments/` hold `.gitkeep` only; the capstone's code lives in shared `src/`; the graduation proof (ADR-0003 row 7) remains UNDECIDED |

### The stack

MP-29 is current and mid-execution (terminus ≈ 2026-08-26); **MP-30 through
MP-36 stand pre-registered, gated in series, the cap at seven**. Each phase's
Session 0 consumes the previous phase's release report: no release, no phase.
MP-37 through MP-59 are the un-cap's roadmap drafts executed exactly once
each. **MP-59's review and roadmap are merged (PR #94), its Session −1 study
lane owns the waiting window, and its Session 0 awaits the stack's release.**
**ADR-0033's eight rows are the rows MP-59 will fill**; **ADR-0034's eight
rows are the rows this roadmap will fill** — exactly once, under the continuum
law, twenty-ninth execution, written from MP-59's release report rather than
from the habit of pre-registering.

### The CI floor and the toolchains

190 tracked tests, ruff, blocking mypy and markdownlint are green at the last
release, `verify-claims` at 0. The verified gaps, stated as facts not hopes:
no LaTeX toolchain on this machine (`make paper` is graceful, not green — the
green-to-PDF verification is a standing Session 1 row), no Pages deploy
workflow in `.github/workflows/`, no `publish:` frontmatter policy,
`portfolio/projects/` holds figures but no project write-ups, W&B never
connected. The `typecheck-new` ratchet remains the house rule for all new
research code; the `commitlint-new` mirror (origin/dev..HEAD) is in ci-check
and must be green before any push. The squash-body law stands in its hardened
form: **the squash body is passed with literal newline characters in the
merge call, never as a single quoted line**; this roadmap's own merge observes
it.

### The showcase corpus at intake

12+ provenance-guarded figures (the count grows with whatever MP-59's science
adds), the paper through the v26 arc (the v28 rule is MP-58's, the v29 rule is
MP-59's, **the v30 rule is this phase's**), the site and Space live since the
premiere, the essay annexes through the v26 arc (the v28 annex is MP-58's, the
v29 annex is MP-59's to write and this phase's to verify; **the v30 annex is
this phase's**), twenty-eight runnable teaching artifacts with stranger-run
transcripts (the receipts land only if the stack ships: the twenty-eighth
ships in MP-59, **the twenty-ninth in this phase**). My teaching lane ships
the twenty-ninth artifact this phase.

## Part II — The bottleneck, stated as the reviewer sees it

The program's capstone carries one open row (the graduation proof, ledger row
7) and the record's negative side carries R1's stamp as its first
un-adjudicated cell. I hold in hand everything that has failed and everything
that has shipped, dated. The bottleneck is the phase planner's — the row I
refuse to open until I have a decision that has already been considered by a
consensus baseline, and I have no script that stamps decisions as decisions,
so every "decision" above the capstone and the post-record arc stays a habit
until a script claims it. The fifteen items below are my current inventory,
re-verified in this sitting, most still open with the phase shift:

1. **The capstone's open row** — the graduation proof (ADR-0003 row 7,
   UNDECIDED). It ships with the record: **no verdict, no stamp, no proof**.
2. **The recent-verdict backlog on the record's negative side** — R1's
   no-head negative (2026-08-14) is newer than R4's and R5's; the ledger
   carries it UNDECIDED; the R1 verdict stamp remains the first of the two
   adjudications.
3. **The instrument that never fired** — the sparse Fourier probe
   (`figures/exp4_sparse_fourier.png`) built for the characterization phase,
   un-run in every sitting since. MP-60's science reads it a fourth time with
   no pending run of its own.
4. **The research-return ledger's UNDECIDED backlog** — rows 3–7 were open
   before I ever heard the capstone's name; MP-29's Session 8 must find zero
   UNDECIDED or the stack stalls. This phase's Session 0 records the state,
   never the debt.
5. **The paper's versioned prose** — the v29 rule is MP-59's; **the v30 rule
   is this phase's**; the v30 snapshot pair (v30.md + v30-annex.md) is this
   phase's Session 3 and Session 6's verification, and the record's chapter
   keeps shipping behind the paper.
6. **The research software shelf** — `exp1…exp5` all green, the exp6 residue
   gone (absence verified 2026-08-19), `typecheck-new` clean for new code,
   manifests on disk and `verify-claims` at 0 — the shelf holds, the shelf is
   not a hero.
7. **The stale showcase shelf** — `portfolio/README.md`'s three "not yet"
   rows contradict the record; `portfolio/projects/` holds figures but no
   project write-ups; **Session 1 of this phase re-verifies the closures,
   it does not re-argue them**.
8. **The essays on the shelf** — the annexes live on the live shelf, none on
   disk in this vault; the v29 annex is MP-59's to write, the v30 annex is
   this phase's; the pre-drafts stay off the shelf per the ladder rule.
9. **The teaching lane** — 28 artifacts shipped by MP-59's release, 28
   stranger-run transcripts; the 29th artifact ships this phase with a
   stranger run attached to its lesson or it does not ship; the lesson's
   receipts land only if the stack ships.
10. **The stranger round** — round 29 closes at MP-59's Session 4 with the
    intake in the progress log; **round 30's intake is this phase's Session
    4** — the round number advances with each phase's Session 4, not with
    the calendar.
11. **The waiting window** — now **ten phases wide** (MP-51 through MP-60):
    six roadmap phases ahead of the stack's terminus, this roadmap and
    MP-51's alone governing the window since the stack's own Session −1
    assignments ended. The window's study lane (Part IV) is this phase's
    Session −1, and **Ex-Ψ8 audits the pre-draft stack — it never re-drafts
    it**.
12. **The art of the question** — the chain MP-37 through MP-59's sittings
    chose one deep question per phase, and the deepest law still applies:
    one question per phase, each phase's intake handled by its own ledger
    row. This roadmap's intake is the paragraph above, not a new row: the
    intake is owned by ADR-0033's dated rows.
13. **The un-cap's roadmap drafts** — MP-37 through MP-59 are the drafts
    that became the record's repeatable house style; each phase's pre-drafts
    live in named files of this roadmap's lineage and are consumed one
    sitting at a time, per the record.
14. **The research-meta loop's closures** — the R1/S2 coarse circuit to
    capstone-to-SAE route, the paper's v29 rule, the all-dense v28 edition
    (to be consumed at this phase's Session 0), the path M5 → capstone-to-SAE
    — the negative result in my hands is as certified as the all-dense
    edition, and the record's negative edge is a feature: an honest record
    ships negatives as loudly as positives.
15. **The harvest habit** — every dated fact above (190 tests, the residue's
    absence, the debt count, the three "not yet" rows, the ledger's UNDECIDED
    cells, the ten-phase-wide window, the merge discipline) is re-verified
    sitting by sitting in this phase's Session 1 — the harvest habit is the
    discipline that keeps the roadmap's "the facts hold" sentences honest.

## Part III — The roadmap

### The frozen candidate set (C113–C116)

Written verdict-agnostic at drafting time, like every roadmap since MP-37's,
because a roadmap that re-plans rows the sitting owns is a plan written from
habit. Each row opens **only if** ADR-0033 row 3 holds the predecessor's
positive, consumed verdict:

| Row | Question | Opens if | Success condition |
|---|---|---|---|
| **C113** | The paradigm, confirmed a thirteenth time — or its boundary, mapped (the successor to C109, which R1's no-head negative and MP-59's verdicts consume) | ADR-0033 row 3's verdict on C109 = positive | A sparse Fourier cell with the same provenance discipline as the record, or a dated falsification of the record's deepest claim |
| **C114** | The equation of state, transferred a ninth time (the successor to C110) | C113 consumed positive | A ninth recipe with the same cross-family discipline as its eight predecessors |
| **C115** | The institution, studied a twenty-third time (the successor to C111) | C114 consumed positive | A twenty-third drift measurement with the same rigor as the twenty-two before it |
| **C116** | The standard, validated a fifteenth time (the successor to C112) | C115 consumed positive | A fifteenth cohort trained and measured, closing the capstone's own loop |

The **universal override** still applies: any sparse cell that lands by S0
owns the question — the candidate set is frozen, the override is not. The
**terminal-state override** is now nineteen questions deep; the
**continuation decision** (below) is what the question chain resolves into.

### The post-record continuation (PR-55, PR-56, PR-57)

The post-record arc, agreed at MP-50's sitting, advances one set per
post-record phase, each set's rows written and consumed exactly once: **PR-55**
— the new harness's fourteenth cross-recipe law; **PR-56** — the law at the
record's edge, nineteenth task; **PR-57** — the record as course, eighteenth
edition. The `terminal-state-override` section's continuation set. The
continuation's cost is a budgeted row, never a drift.

### Wall-clock budget, stated as the reviewer sees it

| Sitting | What I do | Which row it feeds |
|---|---|---|
| −1 | Waiting-window study lane (Part IV), Ex-α13–ε13 drills, **Ex-Ψ8**: the eighth-pass pre-draft stack audit (re-verify, never re-draft) | The study lane |
| 0 | Gate truthing (test count, commitlint-new, ruff, typecheck-new), ADR-0034's row 1 opens the ledger; **Ex-T13's nineteenth-generation arc consumption**; the continuum choice | ADR-0034 row 1 |
| 1 | Shelf baseline + debt re-verification: the README closures, the v29 snapshot pair, `make reproduce`, `make paper` green-to-PDF, the mypy-count decision | ADR-0034 rows 2–3 |
| 2 | The consumed-verdict sitting: C113's row from the intake, or the v30 rule ("the v29 is the record") | ADR-0034 row 4 |
| 3 | Essay annex v30, Ex-Φ snapshot | ADR-0034 row 5 |
| 4 | Stranger round 30 intake, kill-date recorded | ADR-0034 row 6 |
| 5 | Research-row pre-registration (C113–C116, whichever S0–S2 chose) + launch + the 29th teaching artifact's skeleton | ADR-0034 row 7 |
| 6 | Verdict sitting — the stamping | ADR-0034 row 8 |
| 7 | Shelf rehearsal + teaching polish + the write-up-shelf standing contract's decision | The write-up shelf |
| 8 | Release: ADR-0034 at zero UNDECIDED, dev == main, the record's 29th dated direction | The release report |

### The one measured line

The one measured line this phase promises, and the only one: **the record's
30th dated direction ships by MP-60's Session 8** — whichever direction the
consumed verdict picks, and the 29th teaching artifact and the v30 annex ship
with it or the phase does not release. Everything else in this roadmap is
discipline; that line is the promise.

## Part IV — The deep-dive study lane (Session −1, with the waiting window)

Ten readings, each with a runnable check attached — the study lane's rule:
every reading ends with code on disk or a dated note, never with a receipt.
The readings were chosen by the reviewer's question: *what does the record's
next phase need to understand, that its author has not yet verified by
hand?*

1. **The paradigm, a thirteenth time** — Elhage et al. 2021 (honorary tenth
   read), Wang et al. 2022, Conmy et al. 2023, Varma et al. 2023, Olsson et
   al. 2022, Chughtai et al. 2023, Kuhn et al. 2023 (ninth read), Nosek et
   al. 2022 (all read before, re-read as the thirteenth paradigm because the
   paradigm's thirteenth confirmation depends on what I understand it to be).
   Check: the sparse-Fourier probe's fourth pass (instrument that never
   fired).
2. **The equation of state, ninth transfer** — Lyu et al. 2023, Morwani
   et al. 2023, Gromov 2023, Power et al. 2022, Nanda et al. 2023. Check:
   the ninth recipe's kitchen-sink reproduce run on the new harness.
3. **The institution, twenty-third study** — Gelman & Loken 2014, Pineau
   et al. 2021, Kapoor & Narayanan 2023, NASEM 2019, Lakens 2024. Check: the
   stranger round 30 intake sheet, filed with the kill-date.
4. **The standard, fifteenth cohort** — Bricken et al. 2023, Cunningham et
   al. 2023, plus the education-measurement canon (the cohort's validity is
   measured, not assumed). Check: the fifteenth cohort's pre-registration
   sheet.
5. **The post-record program, nineteenth generation** — Lakatos 1978
   (twentieth read), the program's own ledger through ADR-0033. Check: the
   continuation set PR-55/56/57's ledger rows, written and consumed exactly
   once.
6. **The record teaches, round 29** — my own teaching artifacts 1–28, the
   stranger-run transcripts, the lesson-attribution records. Check: the 29th
   artifact's lesson, with a stranger run attached.
7. **The redemption reading, twenty-ninth pass** — the negative edge as
   feature: R1's no-head negative, R4/R5's scheduled negatives, the record's
   honest negative side, read as the record's own justification for shipping.
   Check: the record's negative side, one dated table.
8. **The mathematical bedrock, thirteenth pass** — the DFT-of-addition
   derivation, verified by hand against `k_99 = 111/113`'s failure mode, with
   a runnable check in `src/` (the bedrock is verified, never assumed).
   Check: the runnable check, green.
9. **The instrument that never fired, fourth pass** — `exp4`'s sparse
   Fourier probe: why it was built, why it never ran, what it would have
   shown. Check: the probe's fourth pass, with a dated note on its fate.
10. **The long-window discipline, eighth pass** — the waiting window's own
    law: ten phases wide, six roadmap phases ahead of the stack, study
    lane assigned sitting by sitting. Check: the window's lane ledger, rows
    assigned and consumed.

## Part V — Documentation requirements

The documentation contract, stated as the reviewer sees it:

- **ADR-0034** — eight rows, opened at Session 0, stamped at Session 6, at
  zero UNDECIDED by Session 8. The ledger is the record: no stamp, no row.
- **`essay-annex-30.md`** — written at Session 3, verified at Session 6,
  shipped with the release report.
- **The paper, v30** — the v30 rule decided at Session 2 (or "the v29 is the
  record"), the v30 snapshot pair at Session 3, verified at Session 6.
- **The shelf health sheet** — Session 1's baseline, re-verified at Session
  7: the README closures, `make reproduce` and `make paper` green-to-PDF,
  the mypy-count decision dated.
- **`gate-debt.md`** — the checklists lane's dated row: absent at intake
  (a dated fact, never a silence), the decision recorded at Session 1.
- **The research-row pre-registration** — C113–C116 whichever S0–S2 chose,
  written at Session 5, launched with the 29th teaching artifact's skeleton.
- **The teaching artifact, 29th** — written at Session 5, polished at
  Session 7, shipped with a stranger run attached to its lesson or not
  shipped.
- **Ex-T13's memo** — the nineteenth-generation arc consumption, written
  at Session 0, stamped with the continuum choice.
- **The study log** — the ten readings of Part IV, each with its runnable
  check's dated result, filed at Session −1.
- **The pre-drafts** — named files in this roadmap's lineage, consumed one
  sitting at a time, re-verified (never re-drafted) by Ex-Ψ8's eighth pass.
- **The progress log** — the forty-sixth session entry, written from this
  roadmap, in the same first-person register this file uses.
- **The dated deviation** — the local-`dev`-absence fact, recorded in the
  progress log at Session 0, never reconciled as a silence.

## Part VI — The exercises (the hands-on lane)

Thirty drills plus the clock-check habit, one runnable check per drill (the
count is exact: Ex-A through Ex-Z13, Ex-Φ, Ex-Ω, Ex-Ψ8 — plus the
waiting-window lane's Ex-α13 through Ex-ε13, assigned to Session −1):

- **Ex-A** — re-verify the test count (190 passed in this drafting sitting)
  in a fresh sitting.
- **Ex-B** — re-verify the branches and the diff (`main` at `f53ff47`,
  `origin/dev` at `e0f7995`, `git diff main origin/dev` holding what the
  release says it holds).
- **Ex-C** — re-verify the working tree is clean.
- **Ex-D** — re-verify `verify-claims` at 0.
- **Ex-E** — re-verify all five manifests on disk.
- **Ex-F** — re-verify `figures/` holds no untracked products (the exp6
  residue's absence is a verified fact, not a hope).
- **Ex-G** — re-verify the README closures (the three "not yet" rows gone).
- **Ex-H** — re-verify the v29 snapshot pair (v29.md + v29-annex.md).
- **Ex-I** — re-verify `make reproduce` green.
- **Ex-J** — re-verify `make paper` green-to-PDF (or the dated fallback
  decision).
- **Ex-K** — record the mypy-count decision (176 at intake, dated).
- **Ex-L** — re-verify the ledger's UNDECIDED cells (rows 3–7, stamped or
  scheduled).
- **Ex-M** — re-verify the window's width (ten phases, counted on the
  home file).
- **Ex-N** — re-verify the commitlint-new mirror green before any push.
- **Ex-O** — re-verify the squash-body law: pre-wrapped <200-char lines,
  literal newlines in the merge call, never a single quoted line.
- **Ex-P** — re-verify the paper's v30 rule standing (decided at Session 2,
  or "the v29 is the record").
- **Ex-Q** — re-verify the teaching artifact count (28 shipped, 29th
  scheduled).
- **Ex-R** — re-verify the stranger round 30 intake and its kill-date.
- **Ex-S** — re-verify the research-row pre-registration (C113–C116,
  whichever S0–S2 chose).
- **Ex-T** — re-verify the study log's dated results (ten readings, ten
  checks).
- **Ex-U** — re-verify the gate-debt.md decision (dated at Session 1).
- **Ex-V** — re-verify the essay annex v30 standing (written at Session 3).
- **Ex-W** — re-verify the showcase corpus count (figures, paper, site,
  Space, artifacts).
- **Ex-X** — re-verify the CI floor (ruff, blocking mypy, markdownlint,
  190 tests).
- **Ex-Y** — re-verify the release report's standing (MP-59's consumed,
  this phase's planned).
- **Ex-Z13** — re-verify the measured line: the record's 30th dated
  direction ships by Session 8.
- **Ex-Φ** — the snapshot drill: freeze the vault's state at Session 3
  (essay annex v30, the v30 pair, the progress log entry), re-verify at
  Session 6.
- **Ex-Ω** — the shelf rehearsal at Session 7: dry-run the release — dev ==
  main, ADR-0034 at zero UNDECIDED, corpus coherent, receipts land.
- **Ex-Ψ8** — the eighth-pass pre-draft stack audit: the pre-drafts exist,
  named, consumed one sitting at a time — re-verify, never re-draft.
- **Ex-α13 … Ex-ε13** — the waiting-window lane drills (Session −1, with the
  study lane): one runnable check per reading cluster — the paradigm, the
  equation of state, the institution, the standard, the post-record program.
- **The clock-check habit** — every sitting opens and closes with the same
  clock check: the record's date, the branch, the test count, the ledger's
  UNDECIDED count. A habit, not a drill — the harvest discipline that keeps
  every "the facts hold" sentence in this roadmap honest.

## Part VII — Strategic tips (the architect's advice to myself)

1. **The one-question law, twenty-ninth execution** — one deep question
   per phase; this phase's intake is owned by ADR-0033's dated rows, never
   by a new row opened out of habit.
2. **The frozen candidate set** — C113–C116 were written verdict-agnostic at
   drafting time; re-planning a row the sitting owns is a plan written from
   habit.
3. **Consumption is execution** — every sitting consumes the previous
   sitting's output; Session 2's consumed verdict is the phase's engine.
4. **The receipt compounds** — every reading ends with code on disk or a
   dated note; receipts are the record's currency, and strangers hold me to
   them.
5. **The waiting window is a study lane, not a pause** — ten phases wide,
   the lane's drills run at Session −1, and the lane's ledger is assigned
   sitting by sitting.
6. **The pre-draft stack is verified, never re-drafted** — Ex-Ψ8's eighth
   pass audits existence and naming; re-drafting is the debt the audit
   prevents.
7. **Budget by wall-clock at launch, not at release** — the sitting table in
   Part III is the budget; every sitting has a row, and a sitting without a
   row is a sitting that drifts.
8. **The toolchain is pinned, the receipt is a PDF** — `make paper`
   green-to-PDF is a standing row; no LaTeX toolchain on this machine means
   a dated decision, not a hope.
9. **The record survives its own shelf** — the paper, the site, the Space
   and the essays are the record's public face; the shelf's health is
   re-verified at Session 1 and Session 7, never assumed.
10. **The figures re-derive** — provenance-guarded, `make reproduce`
    regenerates them; the residue is gone, the twelve tracked figures stay.
11. **The instrument that never fired is read, not mourned** — exp4's sparse
    Fourier probe gets its fourth pass with a dated note on its fate.
12. **Protect the release report** — Session 8's release is the phase's only
    output that outlives it; ADR-0034 at zero UNDECIDED or the phase does
    not release.
13. **The S0 gate checklist is executed, not recited** — the test count,
    commitlint-new, ruff, typecheck-new; a gate that is recited is a gate
    that drifts.
14. **The negative stays a signature** — R1's no-head negative and R4/R5's
    scheduled negatives are the record's honest edge; a negative with a
    date is a fact.
15. **The mypy row is dated, never deleted** — 176 errors at intake, the
    decision recorded at Session 1, the count re-verified under the pinned
    toolchain.
16. **The steady state is the reward, twenty-third time** — the record's
    repeatable rhythm — 190 green tests, ruff and blocking mypy clean, the
    harvest habit — is the program's deepest product.
17. **The architecture laws hold** — work on `dev` only, GPG-SSH-signed
    commits, conventional commits with pre-wrapped bodies, squash bodies
    passed with literal newlines; every deviation is recorded with a date so
    the law is stated in its hardened form. The local-`dev`-absence is such
    a deviation: recorded, never reconciled as a silence.
18. **The showcase is a 30-second story** — paper + site + Space + 28
    artifacts + 190 green tests; the 29th artifact ships with a stranger run
    attached to its lesson, or it does not ship.

## Links

- [[00_meta/59_micro-phase-59-review-and-roadmap|MP-59 — the twenty-eighth question's review and roadmap (the intake this phase consumes)]]
- [[00_meta/58_micro-phase-58-review-and-roadmap|MP-58 — the companion that preceded MP-59]]
- [[00_meta/03_progress-log|Progress log — the forty-fifth entry (MP-59's draft) and this phase's forty-sixth]]
- [[00_meta/00_home|Home — where this roadmap is wired as a companion pointer, not a cap row]]
- [[docs/adr/0003-research-return-ledger|ADR-0003 — the research-return ledger, rows 3–7 (R1 stamp, negatives, paper, graduation proof)]]
- [[06_production_ai/notes/microscope-trial-table|The microscope trial table — trials 2 and 3 pending]]
- [[06_production_ai/notes/dense-solutions-modular-addition|Dense solutions in modular addition — the characterized regime]]
- [[06_production_ai/notes/positive-control-protocol|The positive-control protocol — the ALL-DENSE scan]]
- [[portfolio/README|Portfolio README — the stale shelf, Session 1's closure]]
- [[checklists/reproducibility-checklist|The reproducibility checklist — the checklists lane's dated row]]