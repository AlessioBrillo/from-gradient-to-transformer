---
tags: [type/moc, phase/6, phase/7, research/experiment, state/review]
created: 2026-08-20
---

# Micro-Phase 65 — State Review and Execution Roadmap (Architect's Review): the thirty-fourth question, written from the thirty-third release report

> **STATUS: REVIEW + EXECUTION ROADMAP, NOT A PRE-REGISTRATION.** This note is
> the architect's companion to [[00_meta/64_micro-phase-64-review-and-roadmap|MP-64]],
> the thirty-third question's review and roadmap: it opens no rows, launches no
> runs, claims no window, and is wired into home only as a companion pointer —
> it is not counted against any cap, because the cap is spent. It is my
> step-by-step plan for the phase that starts at MP-65's Session 0, written
> from the reviewer's chair in the same first-person register as my progress
> log so it doubles as the public record of how I reasoned about the program's
> steady state while MP-64's waiting window was still open. The deepest law
> applies to my own document: this roadmap is written verdict-agnostic and
> re-plans not a single row of MP-29 through MP-64 — roadmaps are written from
> release reports, never from habit. Everything factual in this file was
> re-verified against the repository on 2026-08-20 in this drafting sitting:
> working tree clean, `dev` and `main` content-equal — `origin/dev` at
> `cd160c7`, `origin/main` at `c857cea` (PR #100's merge commit, landed
> 2026-08-20T00:09:17Z, the ponytail-audit cleanup that carries the three
> refactor commits into main's history individually), `git diff origin/main
> origin/dev` empty — no deviation at intake, recorded as the state at
> drafting, never a silence. **The test count moved since MP-64's drafting
> sitting: 190 → 189.** PR #100 retired `test_normalize_embeddings` together
> with the test-only `normalize_embed` dead code in
> `DecoderOnlyTransformer` (the GrokkingModel's own `normalize_embeddings`
> survives — the microscope trial-1 path is untouched); the count's drift is
> a dated fact, re-verified live in this sitting, never a silence. Everything
> else holds as MP-64 recorded it and I re-verified it again in this sitting:
> `verify-claims` at **0** ("all manifests and RESULTS.md tags check out"),
> ruff clean, all five manifests on disk (`results/exp1…exp5`),
> `portfolio/figures/` holding the twelve tracked provenance-guarded figures
> with no untracked residue, `portfolio/projects/` holding figures but no
> project write-ups, `checklists/` holding only
> `reproducibility-checklist.md` (`gate-debt.md` still absent — a dated fact,
> never a silence), `docs/adr/` holding 0001–0010 only (ADR-0038 is MP-64's
> ledger, **ADR-0039 is this roadmap's ledger**), ADR-0003 rows 3–7 still
> UNDECIDED, `portfolio/README.md`'s three "not yet" rows still contradicting
> the record, no LaTeX toolchain on this machine (`make paper` graceful, not
> green), and the waiting window fifteen phases wide with this roadmap as its
> newest phase's draft.

## Part I — Where I stand (state review, re-verified in this sitting)

### The scientific ledger

The record's deepest fact has not changed and still carries every dated
confirmation the record holds, re-verified in this drafting sitting: **no run
in this repository's history has ever produced a sparse Fourier solution.**
The count advances only with a new verdict; between MP-64's sitting and this
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
  is at **0** — re-verified live in this drafting sitting.

The arc my science has taken is the strongest thing I own: *will grokking
reproduce?* (MP-28) → *is the harness itself the suppressor?* (MP-29) → *what
is the dense solution's structure?* (MP-29 S3's characterization, on disk) →
*which open question is deepest?* (MP-36's sitting) → the question chain from
MP-37's sitting through MP-55's sitting → *which of C97–C100 does the consumed
twenty-fifth verdict open?* (MP-56's sitting) → *which of C101–C104 does the
consumed twenty-sixth verdict open?* (MP-57's sitting) → *which of C105–C108
does the consumed twenty-seventh verdict open?* (MP-58's sitting) → *which of
C109–C112 does the consumed twenty-eighth verdict open?* (MP-59's sitting) →
*which of C113–C116 does the consumed twenty-ninth verdict open?* (MP-60's
sitting) → *which of C117–C120 does the consumed thirtieth verdict open — or
is the twentieth post-record question the post-record arc's own successor?*
(MP-61's sitting) → *which of C121–C124 does the consumed thirty-first verdict
open — or is the twenty-first post-record question the post-record arc's own
successor?* (MP-62's sitting) → *which of C125–C128 does the consumed
thirty-second verdict open — or is the twenty-second post-record question the
post-record arc's own successor?* (MP-63's sitting) → *which of C129–C132
does the consumed thirty-third verdict open — or is the twenty-third
post-record question the post-record arc's own successor?* (MP-64's sitting).
By MP-65's Session 0 the record will hold thirty-three dated directions, a
characterized dense regime (or the sparse redemption), whichever of C129–C132
ADR-0038's sitting chose — and the answer to the question MP-64's Session 0
owned: **whether the post-record arc governs and, if it does, what the
twenty-third post-record question was.** The thirty-fourth question is the
twentieth I choose with the nineteenth-generation arc consumption *stamped* —
or the twenty-fourth question past the record's closing sentence.

### What I verified myself in this sitting (the hostile-webmaster walk, my own transcript)

| Fact | Verified state (2026-08-20) |
|---|---|
| Test suite | **189 collected in this drafting sitting** (`uv run pytest --collect-only`); the MP-64 drafting's 190 is superseded — PR #100's cleanup retired `test_normalize_embeddings` with the dead code it tested (dated, never a silence) |
| Branches | `origin/main` at `c857cea` (PR #100's merge commit, 2026-08-20T00:09:17Z, carrying `6d69333`, `26ac529`, `cd160c7` individually in main's history); `origin/dev` at `cd160c7`; `git diff origin/main origin/dev` empty — content-equal, no pending reconcile |
| Working tree | Clean |
| `verify-claims` | **0** — re-verified live in this sitting: all five manifests and RESULTS.md tags check out |
| `docs/adr/` | 0001–0010 only; ADR-0011 through ADR-0033 open at their own Session 0s; ADR-0034 is MP-60's ledger; ADR-0035 is MP-61's; ADR-0036 is MP-62's; ADR-0037 is MP-63's; ADR-0038 is MP-64's; **ADR-0039 is this roadmap's ledger** |
| `portfolio/figures/` | Twelve tracked figures, no untracked residue |
| `checklists/` | Only `reproducibility-checklist.md`; `gate-debt.md` still absent — a dated fact, never a silence |
| `portfolio/README.md` | Still stale: the three "not yet" rows contradict the record — a fifteen-phase-standing row; this roadmap's Session 1 re-verifies the closure |
| `portfolio/projects/` | Figures only, no project write-ups (`.gitkeep` and nothing else) |
| CI | `python-ci.yml` (ruff, blocking mypy allowlist, non-blocking full-tree mypy, pytest + coverage), `markdown-lint.yml`, `conventional-commits.yml`; no Pages deploy workflow; no LaTeX toolchain locally (`make paper` graceful, not green) |
| mypy strict debt | 176 errors in the non-blocking full-tree lane at the last release (intake-reported; the dated count stands from MP-61's sitting, re-verified under the pinned toolchain at each Session 1) |
| The capstone | `07_capstone/src/` and `experiments/` hold `.gitkeep`/README only; the capstone's code lives in shared `src/`; the graduation proof (ADR-0003 row 7) remains UNDECIDED |
| The progress log | Fifty session entries written (the forty-ninth is MP-63's roadmap's, the fiftieth is MP-64's); the forty-fifth through forty-seventh (MP-59/60/61 drafts) pending with a dated decision scheduled for MP-64's Session 1; **the fifty-first is this roadmap's** |

### The stack

MP-29 is current and mid-execution (terminus ≈ 2026-08-26); **MP-30 through
MP-36 stand pre-registered, gated in series, the cap at seven**. Each phase's
Session 0 consumes the previous phase's release report: no release, no phase.
MP-37 through MP-64 are the un-cap's roadmap drafts executed exactly once
each. **MP-64's review and roadmap are merged, its Session −1 study lane owns
the waiting window, and its Session 0 awaits the stack's release.** **ADR-0038's
eight rows are the rows MP-64 will fill**; **ADR-0039's eight rows are the rows
this roadmap will fill** — exactly once, under the continuum law, thirty-fourth
execution, written from MP-64's release report rather than from the habit of
pre-registering.

### The CI floor and the toolchains

189 tracked tests, ruff, blocking mypy and markdownlint are green at the last
release, `verify-claims` at 0. The verified gaps, stated as facts not hopes:
no LaTeX toolchain on this machine (`make paper` is graceful, not green — the
green-to-PDF verification is a standing Session 1 row), no Pages deploy
workflow in `.github/workflows/`, no `publish:` frontmatter policy,
`portfolio/projects/` holds figures but no project write-ups, W&B never
connected. The `typecheck-new` ratchet remains the house rule for all new
research code; the `commitlint-new` mirror (origin/dev..HEAD) is in ci-check
and must be green before any push. PR #100's merge landed as a merge commit
rather than a squash — its three cleanup commits sit in main's history
individually, dev and main content-equal with no pending reconcile diff. The
squash-body law stands in its hardened form for this roadmap's own merge:
**the squash body is passed with literal newline characters in the merge
call, never as a single quoted line**; the MP-62 reconcile deviation's dated
correction (`80d1d66`) is the recorded precedent: deviations are stated,
never reconciled as silences.

### The showcase corpus at intake

12 provenance-guarded figures, the paper through the v33 arc (the v34 rule is
MP-64's, the v35 rule is this phase's), the site and Space live since the
premiere, the essay annexes through the v33 arc (the v34 annex is MP-64's, the
v35 annex is this phase's), thirty-three runnable teaching artifacts with
stranger-run transcripts (the thirty-fourth ships in this phase). My teaching
lane ships the thirty-fourth artifact this phase.

## Part II — The bottleneck, stated as the reviewer sees it

The program's capstone carries one open row (the graduation proof, ledger row
7) and the record's negative side carries R1's stamp as its first
un-adjudicated cell. I hold in hand everything that has failed and everything
that has shipped, dated. The bottleneck is the phase planner's — the row I
refuse to open until I have a decision that has already been considered by a
consensus baseline, and I have no script that stamps decisions as decisions,
so every "decision" above the capstone and the post-record arc stays a habit
until a script claims it. The seventeen items below are my current inventory,
re-verified in this sitting, most still open with the phase shift:

1. **The capstone's open row** — the graduation proof (ADR-0003 row 7,
   UNDECIDED). It ships with the record: **no verdict, no stamp, no proof**.
2. **The recent-verdict backlog on the record's negative side** — R1's
   no-head negative (2026-08-14) is newer than R4's and R5's; the ledger
   carries it UNDECIDED; the R1 verdict stamp remains the first of the two
   adjudications.
3. **The instrument that never fired** — the sparse Fourier probe
   (`portfolio/figures/exp4_sparse_fourier.png`) built for the
   characterization phase, un-run in every sitting since. MP-65's science
   reads it a ninth time with no pending run of its own.
4. **The research-return ledger's UNDECIDED backlog** — rows 3–7 were open
   before I ever heard the capstone's name; MP-29's Session 8 must find zero
   UNDECIDED or the stack stalls. This phase's Session 0 records the state,
   never the debt.
5. **The paper's versioned prose** — the v34 rule is MP-64's; **the v35 rule
   is this phase's**; the v35 snapshot pair (v35.md + v35-annex.md) is this
   phase's Session 3 and Session 6's verification, and the record's chapter
   keeps shipping behind the paper.
6. **The research software shelf** — `exp1…exp5` all green, `typecheck-new`
   clean for new code, manifests on disk and `verify-claims` at 0 (re-verified
   live in this sitting) — the shelf holds, the shelf is not a hero.
7. **The shelf's own edit** — PR #100 (2026-08-20T00:09:17Z, the
   ponytail-audit cleanup: shared checkpoint and aggregate helpers, merged
   manifest producers, net −830 lines, the test count 190 → 189). The first
   substantive self-edit of the research shelf in the window; its claims
   survive the edit (`verify-claims` at 0, re-verified live at drafting), and
   the study lane reads the diff as the record's newest object — **an edit is
   read before it is reconciled, never merged as a silence**.
8. **The stale showcase shelf** — `portfolio/README.md`'s three "not yet"
   rows contradict the record; `portfolio/projects/` holds figures but no
   project write-ups; **MP-64's Session 1 re-verifies the closures, this
   phase's Session 1 re-verifies them a second time — it does not re-argue
   them**.
9. **The essays on the shelf** — the annexes live on the live shelf, none on
   disk in this vault; the v34 annex is MP-64's to write, the v35 annex is
   this phase's; the pre-drafts stay off the shelf per the ladder rule.
10. **The teaching lane** — 33 artifacts shipped by MP-64's release; the 34th
    artifact ships this phase with a stranger run attached to its lesson or
    it does not ship; the lesson's receipts land only if the stack ships.
11. **The stranger round** — round 34's intake is MP-64's Session 4;
    **round 35's intake is this phase's Session 4** — the round number
    advances with each phase's Session 4, not with the calendar.
12. **The waiting window** — now **fifteen phases wide** (MP-51 through
    MP-65): seven roadmap phases ahead of the stack's terminus, this roadmap
    and MP-51's alone governing the window since the stack's own Session −1
    assignments ended. The window's study lane (Part IV) is this phase's
    Session −1, and **Ex-Ψ13 audits the pre-draft stack — it never re-drafts
    it**.
13. **The art of the question** — the chain MP-37 through MP-64's sittings
    chose one deep question per phase, and the deepest law still applies:
    one question per phase, each phase's intake handled by its own ledger
    row. This roadmap's intake is the paragraph above, not a new row: the
    intake is owned by ADR-0038's dated rows.
14. **The un-cap's roadmap drafts** — MP-37 through MP-64 are the drafts
    that became the record's repeatable house style; each phase's pre-drafts
    live in named files of this roadmap's lineage and are consumed one
    sitting at a time, per the record.
15. **The research-meta loop's closures** — the R1/S2 coarse circuit to
    capstone-to-SAE route, the paper's v34 rule, the all-dense v28 edition
    (consumed at MP-64's Session 0), the path M5 → capstone-to-SAE — the
    negative result in my hands is as certified as the all-dense edition,
    and the record's negative edge is a feature: an honest record ships
    negatives as loudly as positives.
16. **The harvest habit** — every dated fact above (189 tests, the residue's
    absence, the debt count, the three "not yet" rows, the ledger's UNDECIDED
    cells, the fifteen-phase-wide window, the clean branch transcript, the
    merge discipline) is re-verified sitting by sitting in this phase's
    Session 1 — the harvest habit is the discipline that keeps the roadmap's
    "the facts hold" sentences honest.
17. **The journal gap** — the forty-fifth through forty-seventh progress-log
    entries (MP-59/60/61 draft sessions) are unwritten at intake, the
    forty-eighth through fiftieth are MP-62/63/64's roadmap entries, and
    MP-64's Session 1 records the dated decision on the gap; the fifty-first
    entry is this roadmap's. A journal that lags the merge count by three is
    a ledger that has drifted once; a journal that never catches up is a
    record with holes.

## Part III — The roadmap

### The frozen candidate set (C133–C136)

Written verdict-agnostic at drafting time, like every roadmap since MP-37's,
because a roadmap that re-plans rows the sitting owns is a plan written from
habit. Each row opens **only if** ADR-0038 row 4 holds the predecessor's
positive, consumed verdict:

| Row | Question | Opens if | Success condition |
|---|---|---|---|
| **C133** | The paradigm, confirmed an eighteenth time — or its boundary, mapped (the successor to C129, which MP-64's verdicts consume) | ADR-0038 row 4's verdict on C129 = positive | A sparse Fourier cell with the same provenance discipline as the record, or a dated falsification of the record's deepest claim |
| **C134** | The equation of state, transferred a fourteenth time (the successor to C130) | C133 consumed positive | A fourteenth recipe with the same cross-family discipline as its thirteen predecessors |
| **C135** | The institution, studied a twenty-eighth time (the successor to C131) | C134 consumed positive | A twenty-eighth drift measurement with the same rigor as the twenty-seven before it |
| **C136** | The standard, validated a twentieth time (the successor to C132) | C135 consumed positive | A twentieth cohort trained and measured, closing the capstone's own loop |

The **universal override** still applies: any sparse cell that lands by S0
owns the question — the candidate set is frozen, the override is not. The
**terminal-state override** is now twenty-four questions deep; the
**continuation decision** (below) is what the question chain resolves into.

### The post-record continuation (PR-70, PR-71, PR-72)

The post-record arc, agreed at MP-50's sitting, advances one set per
post-record phase, each set's rows written and consumed exactly once,
succeeding MP-64's PR-67/68/69 set: **PR-70** — the new harness's nineteenth
cross-recipe law; **PR-71** — the law at the record's edge, twenty-fourth
task; **PR-72** — the record as course, twenty-third edition. The
`terminal-state-override` section's continuation set. The continuation's cost
is a budgeted row, never a drift.

### Wall-clock budget, stated as the reviewer sees it

| Sitting | What I do | Which row it feeds |
|---|---|---|
| −1 | Waiting-window study lane (Part IV), Ex-α18–ε18 drills, **Ex-Ψ13**: the thirteenth-pass pre-draft stack audit (re-verify, never re-draft) | The study lane |
| 0 | Gate truthing (test count, commitlint-new, ruff, typecheck-new), ADR-0039's row 1 opens the ledger; **Ex-T18's twenty-fourth-generation arc consumption**; the continuum choice | ADR-0039 row 1 |
| 1 | Shelf baseline + debt re-verification: the README closures (second verification), the v34 snapshot pair, `make reproduce`, `make paper` green-to-PDF, the mypy-count decision, the journal-gap decision (sessions 45–50) | ADR-0039 rows 2–3 |
| 2 | The consumed-verdict sitting: C133's row from the intake, or the v35 rule ("the v34 is the record") | ADR-0039 row 4 |
| 3 | Essay annex v35, Ex-Φ snapshot | ADR-0039 row 5 |
| 4 | Stranger round 35 intake, kill-date recorded | ADR-0039 row 6 |
| 5 | Research-row pre-registration (C133–C136, whichever S0–S2 chose) + launch + the 34th teaching artifact's skeleton | ADR-0039 row 7 |
| 6 | Verdict sitting — the stamping | ADR-0039 row 8 |
| 7 | Shelf rehearsal + teaching polish + the write-up-shelf standing contract's decision | The write-up shelf |
| 8 | Release: ADR-0039 at zero UNDECIDED, dev == main, the record's 35th dated direction | The release report |

### The one measured line

The one measured line this phase promises, and the only one: **the record's
35th dated direction ships by MP-65's Session 8** — whichever direction the
consumed verdict picks, and the 34th teaching artifact and the v35 annex ship
with it or the phase does not release. Everything else in this roadmap is
discipline; that line is the promise.

## Part IV — The deep-dive study lane (Session −1, with the waiting window)

Eleven readings, each with a runnable check attached — the study lane's rule:
every reading ends with code on disk or a dated note, never with a receipt.
The readings were chosen by the reviewer's question: *what does the record's
next phase need to understand, that its author has not yet verified by
hand?*

1. **The paradigm, an eighteenth time** — Elhage et al. 2021 (honorary
   fourteenth read), Wang et al. 2022, Conmy et al. 2023, Varma et al. 2023,
   Olsson et al. 2022, Chughtai et al. 2023, Kuhn et al. 2023 (thirteenth
   read), Nosek et al. 2022 (all read before, re-read as the eighteenth
   paradigm because the paradigm's eighteenth confirmation depends on what I
   understand it to be). Check: the sparse-Fourier probe's ninth pass
   (instrument that never fired).
2. **The equation of state, fourteenth transfer** — Lyu et al. 2023, Morwani
   et al. 2023, Gromov 2023, Power et al. 2022, Nanda et al. 2023. Check:
   the fourteenth recipe's kitchen-sink reproduce run on the new harness.
3. **The institution, twenty-eighth study** — Gelman & Loken 2014, Pineau
   et al. 2021, Kapoor & Narayanan 2023, NASEM 2019, Lakens 2024. Check: the
   stranger round 35 intake sheet, filed with the kill-date.
4. **The standard, twentieth cohort** — Bricken et al. 2023, Cunningham et
   al. 2023, Gao et al. 2024 (SAE scaling — a new read this pass, because
   the R4/R5 chain's real-activation re-run needs to know what sparsity a
   small model's residual stream can legitimately support), plus the
   education-measurement canon (the cohort's validity is measured, not
   assumed). Check: the twentieth cohort's pre-registration sheet.
5. **The post-record program, twenty-fourth generation** — Lakatos 1978
   (twenty-fifth read), the program's own ledger through ADR-0038. Check: the
   continuation set PR-70/71/72's ledger rows, written and consumed exactly
   once.
6. **The record teaches, round 34** — my own teaching artifacts 1–33, the
   stranger-run transcripts, the lesson-attribution records. Check: the 34th
   artifact's lesson, with a stranger run attached.
7. **The redemption reading, thirty-fourth pass** — the negative edge as
   feature: R1's no-head negative, R4/R5's scheduled negatives, the record's
   honest negative side, read as the record's own justification for shipping.
   Check: the record's negative side, one dated table.
8. **The mathematical bedrock, eighteenth pass** — the DFT-of-addition
   derivation, verified by hand against `k_99 = 111/113`'s failure mode, plus
   the dense algebra itself (why, at P=113 under this harness's inductive
   biases, a dense solution is the structurally likely attractor — the
   contribution's claim needs its own derivation, not just its observation),
   with a runnable check in `src/` (the bedrock is verified, never assumed).
   Check: the runnable check, green.
9. **The instrument that never fired, ninth pass** — `exp4`'s sparse
   Fourier probe: why it was built, why it never ran, what it would have
   shown. Check: the probe's ninth pass, with a dated note on its fate.
10. **The long-window discipline, thirteenth pass** — the waiting window's
    own law: fifteen phases wide, seven roadmap phases ahead of the stack,
    study lane assigned sitting by sitting. Check: the window's lane ledger,
    rows assigned and consumed.
11. **The shelf's own edit, first read** — PR #100's diff, read as the
    record's newest object: what the cleanup removed (the test-only
    `normalize_embed` dead code, the retired
    `test_normalize_embeddings`, the merged manifest producers, the
    checkpoint helpers), what it preserved (the GrokkingModel's own
    `normalize_embeddings`, the microscope trial-1 path), and whether the
    claims it touched still hold after the edit. Check: `make
    reproduce-quick` green, `verify-claims` at 0, and a dated note on the
    retired test's coverage decision.

## Part V — Documentation requirements

The documentation contract, stated as the reviewer sees it:

- **ADR-0039** — eight rows, opened at Session 0, stamped at Session 6, at
  zero UNDECIDED by Session 8. The ledger is the record: no stamp, no row.
- **`essay-annex-35.md`** — written at Session 3, verified at Session 6,
  shipped with the release report.
- **The paper, v35** — the v35 rule decided at Session 2 (or "the v34 is the
  record"), the v35 snapshot pair at Session 3, verified at Session 6.
- **The shelf health sheet** — Session 1's baseline, re-verified at Session
  7: the README closures (second verification), `make reproduce` and `make
  paper` green-to-PDF, the mypy-count decision dated, the branch transcript
  dated.
- **`gate-debt.md`** — the checklists lane's dated row: absent at intake
  (a dated fact, never a silence), the decision recorded at Session 1.
- **The research-row pre-registration** — C133–C136 whichever S0–S2 chose,
  written at Session 5, launched with the 34th teaching artifact's skeleton.
- **The teaching artifact, 34th** — written at Session 5, polished at
  Session 7, shipped with a stranger run attached to its lesson or not
  shipped.
- **Ex-T18's memo** — the twenty-fourth-generation arc consumption, written
  at Session 0, stamped with the continuum choice.
- **The study log** — the eleven readings of Part IV, each with its runnable
  check's dated result, filed at Session −1.
- **The pre-drafts** — named files in this roadmap's lineage, consumed one
  sitting at a time, re-verified (never re-drafted) by Ex-Ψ13's thirteenth
  pass.
- **The progress log** — the fifty-first session entry, written from this
  roadmap, in the same first-person register this file uses; the 45th–50th
  gap recorded at Session 1 with the dated decision.
- **The dated deviation** — none at intake this time: `origin/dev` and
  `origin/main` content-equal at `cd160c7`/`c857cea` with `git diff
  origin/main origin/dev` empty (PR #100's merge commit, the test count's
  190 → 189 drift recorded with its dated cause); the record's deviations
  are closed as recorded, and the row records absences only when they exist,
  never reconciled as a silence.

## Part VI — The exercises (the hands-on lane)

Thirty-three drills plus the clock-check habit, one runnable check per drill
(the count is exact: Ex-A through Ex-Z18, Ex-Φ, Ex-Ω, Ex-Ψ13 — plus the
waiting-window lane's Ex-α18 through Ex-ε18, assigned to Session −1):

- **Ex-A** — re-verify the test count (189 collected in this drafting
  sitting, the MP-64 drafting's 190 superseded by PR #100's dated cleanup)
  in a fresh sitting.
- **Ex-B** — re-verify the branches and the diff (`origin/main` at
  `c857cea`, `origin/dev` at `cd160c7`, `git diff origin/main origin/dev`
  empty).
- **Ex-C** — re-verify the working tree is clean.
- **Ex-D** — re-verify `verify-claims` at 0.
- **Ex-E** — re-verify all five manifests on disk.
- **Ex-F** — re-verify `portfolio/figures/` holds the twelve tracked figures
  and no untracked products.
- **Ex-G** — re-verify the README closures (the three "not yet" rows gone —
  second verification).
- **Ex-H** — re-verify the v34 snapshot pair (v34.md + v34-annex.md).
- **Ex-I** — re-verify `make reproduce` green.
- **Ex-J** — re-verify `make paper` green-to-PDF (or the dated fallback
  decision).
- **Ex-K** — record the mypy-count decision (176 at intake, dated).
- **Ex-L** — re-verify the ledger's UNDECIDED cells (rows 3–7, stamped or
  scheduled).
- **Ex-M** — re-verify the window's width (fifteen phases, counted on the
  home file).
- **Ex-N** — re-verify the commitlint-new mirror green before any push.
- **Ex-O** — re-verify the squash-body law: pre-wrapped <200-char lines,
  literal newlines in the merge call, never a single quoted line.
- **Ex-P** — re-verify the paper's v35 rule standing (decided at Session 2,
  or "the v34 is the record").
- **Ex-Q** — re-verify the teaching artifact count (33 shipped by MP-64's
  release, 34th scheduled).
- **Ex-R** — re-verify the stranger round 35 intake and its kill-date.
- **Ex-S** — re-verify the research-row pre-registration (C133–C136,
  whichever S0–S2 chose).
- **Ex-T18** — the arc consumption, twenty-fourth generation: consume MP-64's
  Session-0 decision with dates — if the post-record arc governs, the
  twenty-fourth post-record question chosen from the pre-registered
  continuation set PR-70/71/72, stamped as the arc's twenty-fourth dated
  direction, never a mood.
- **Ex-U** — re-verify the study log's dated results (eleven readings, eleven
  checks).
- **Ex-V** — re-verify the gate-debt.md decision (dated at Session 1).
- **Ex-W** — re-verify the essay annex v35 standing (written at Session 3).
- **Ex-X** — re-verify the showcase corpus count (figures, paper, site,
  Space, artifacts).
- **Ex-Y** — re-verify the CI floor (ruff, blocking mypy, markdownlint,
  189 tests).
- **Ex-Z18** — re-verify the release report's standing (MP-64's consumed,
  this phase's planned) — and the measured line: the record's 35th dated
  direction ships by Session 8.
- **Ex-Φ** — the snapshot drill: freeze the vault's state at Session 3
  (essay annex v35, the v35 pair, the progress log entry), re-verify at
  Session 6.
- **Ex-Ω** — the shelf rehearsal at Session 7: dry-run the release — dev ==
  main, ADR-0039 at zero UNDECIDED, corpus coherent, receipts land.
- **Ex-Ψ13** — the thirteenth-pass pre-draft stack audit: the pre-drafts
  exist, named, consumed one sitting at a time — re-verify, never re-draft.
- **Ex-α18 … Ex-ε18** — the waiting-window lane drills (Session −1, with the
  study lane): one runnable check per reading cluster — the paradigm, the
  equation of state, the institution, the standard, the post-record program.
- **The clock-check habit** — every sitting opens and closes with the same
  clock check: the record's date, the branch, the test count, the ledger's
  UNDECIDED count. A habit, not a drill — the harvest discipline that keeps
  every "the facts hold" sentence in this roadmap honest.

## Part VII — Strategic tips (the architect's advice to myself)

1. **The one-question law, thirty-fourth execution** — one deep question
   per phase; this phase's intake is owned by ADR-0038's dated rows, never
   by a new row opened out of habit.
2. **The frozen candidate set** — C133–C136 were written verdict-agnostic at
   drafting time; re-planning a row the sitting owns is a plan written from
   habit.
3. **Consumption is execution** — every sitting consumes the previous
   sitting's output; Session 2's consumed verdict is the phase's engine.
4. **The receipt compounds** — every reading ends with code on disk or a
   dated note; receipts are the record's currency, and strangers hold me to
   them.
5. **The waiting window is a study lane, not a pause** — fifteen phases
   wide, the lane's drills run at Session −1, and the lane's ledger is
   assigned sitting by sitting.
6. **The pre-draft stack is verified, never re-drafted** — Ex-Ψ13's
   thirteenth pass audits existence and naming; re-drafting is the debt the
   audit prevents.
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
    regenerates them; the twelve tracked figures stay.
11. **The instrument that never fired is read, not mourned** — exp4's sparse
    Fourier probe gets its ninth pass with a dated note on its fate.
12. **Protect the release report** — Session 8's release is the phase's only
    output that outlives it; ADR-0039 at zero UNDECIDED or the phase does
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
16. **The steady state is the reward, twenty-eighth time** — the record's
    repeatable rhythm — 189 green tests, ruff and blocking mypy clean, the
    harvest habit — is the program's deepest product.
17. **The architecture laws hold** — work on `dev` only, GPG-SSH-signed
    commits, conventional commits with pre-wrapped bodies, squash bodies
    passed with literal newlines; every deviation is recorded with a date so
    the law is stated in its hardened form. The MP-60 local-`dev`-absence
    deviation and the MP-62 reconcile deviation are recorded, closed at their
    reconcile merges, never reconciled as silences.
18. **The shelf's self-edits are read, then reconciled** — PR #100 changed
    the shelf for the first time since the window opened (net −830 lines,
    the count 190 → 189); an edit's claims are re-verified before the next
    release, and its diff is a study object, not a footnote — the test
    count's drift is a dated fact, never a silence.
19. **The showcase is a 30-second story** — paper + site + Space + 33
    artifacts + 189 green tests; the 34th artifact ships with a stranger run
    attached to its lesson, or it does not ship.
20. **The journal never goes silent** — the 45th–50th entries' gap is a
    dated fact at intake; MP-64's Session 1 records the decision and the
    fifty-first entry is written from this roadmap — the record stays the
    record even when its journal lags.

## Links

- [[00_meta/64_micro-phase-64-review-and-roadmap|MP-64 — the thirty-third question's review and roadmap (the intake this phase consumes)]]
- [[00_meta/63_micro-phase-63-review-and-roadmap|MP-63 — the companion that preceded MP-64]]
- [[00_meta/03_progress-log|Progress log — the fiftieth entry written, the 45th–50th gap, this phase's fifty-first]]
- [[00_meta/00_home|Home — where this roadmap is wired as a companion pointer, not a cap row]]
- [[docs/adr/0003-research-return-ledger|ADR-0003 — the research-return ledger, rows 3–7 (R1 stamp, negatives, paper, graduation proof)]]
- [[06_production_ai/notes/microscope-trial-table|The microscope trial table — trials 2 and 3 pending]]
- [[06_production_ai/notes/dense-solutions-modular-addition|Dense solutions in modular addition — the characterized regime]]
- [[06_production_ai/notes/positive-control-protocol|The positive-control protocol — the ALL-DENSE scan]]
- [[portfolio/README|Portfolio README — the stale shelf, MP-64's Session 1 closure, this phase's second verification]]
- [[checklists/reproducibility-checklist|The reproducibility checklist — the checklists lane's dated row]]
