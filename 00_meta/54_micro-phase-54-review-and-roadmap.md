---
tags: [type/moc, phase/6, phase/7, research/experiment, state/review]
created: 2026-08-18
---

# Micro-Phase 54 — State Review and Execution Roadmap (Architect's Review): the twenty-third question, written from the twenty-second release report

> **STATUS: REVIEW + EXECUTION ROADMAP, NOT A PRE-REGISTRATION.** This note is
> the architect's companion to [[00_meta/53_micro-phase-53-review-and-roadmap]],
> the twenty-second question's review and roadmap: it opens no rows, launches no
> runs, claims no window, and is wired into home only as a companion pointer —
> it is not counted against any cap, because the cap is spent. It is my
> step-by-step plan for the phase that starts at MP-54's Session 0, written
> from the reviewer's chair in the same first-person register as my progress
> log so it doubles as the public record of how I reasoned about the program's
> steady state while MP-53's waiting window was still open. The deepest law
> applies to my own document: this roadmap is written verdict-agnostic and
> re-plans not a single row of MP-29 through MP-53 — roadmaps are written from
> release reports, never from habit. Everything factual in this file was
> re-verified against the repository on 2026-08-18 in this drafting sitting:
> working tree clean, local `dev` at `6acd48d` (one ci-commit ahead of main —
> the scoped pardon for the MP-53 squash, which MP-53's Session 8 folds in),
> local `main` at `ae867d5` (the MP-53 squash, PR #88), **190 tests collected
> in this drafting sitting**, ruff clean at the last release, blocking mypy
> clean at the last release, `verify-claims` at 0.

## Part I — Where I stand (state review, re-verified in this sitting)

### The scientific ledger

The record's deepest fact has not changed and still has twelve dated
confirmations behind it, re-verified in this drafting sitting: **no run in
this repository's history has ever produced a sparse Fourier solution.** The
count advances only with a new verdict; between MP-53's sitting and this one,
no new Fourier cell landed — the microscope's trials 2 and 3 remain pending in
ADR-0003's budget.

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
*which open question is deepest?* (MP-36's sitting) → *what does my own phase
map say about the boundary?* (MP-37's sitting) → *which of the causal,
circuit, law, rate and instrument questions does each consumed verdict open?*
(MP-38 through MP-50's sittings) → *which of C77–C80 does the consumed
twentieth verdict open?* (MP-51's sitting) → *which of C81–C84 does the
consumed twenty-first verdict open?* (MP-52's sitting) → *which of C85–C88
does the consumed twenty-second verdict open — or is the twelfth post-record
question the post-record arc's own successor?* (MP-53's sitting). By MP-54's
Session 0 the record will hold twenty-two dated directions, a characterized
dense regime (or the sparse redemption), whichever of C85–C88 ADR-0027's
sitting chose — and the answer to the question MP-53's Session 0 owns more
deeply than any phase before it: **whether the post-record arc governs and,
if it does, what the twelfth post-record question was.** The twenty-third
question is the thirteenth-generation consumption of the terminal-state
decision — or the thirteenth question past the record's closing sentence.

### What I verified myself in this sitting (the hostile-webmaster walk, my own transcript)

| Fact | Verified state (2026-08-18) |
|---|---|
| Test suite | 190 collected via `pytest --collect-only` (2.60 s) — green in this drafting sitting; the full suite passed at the last release in 64.48 s |
| Branches | `dev` at `6acd48d`; `main` at `ae867d5` (the MP-53 squash, PR #88); `git diff main dev` holds exactly the scoped CI pardon (`commitlint.config.mjs` +12), which MP-53's Session 8 release merge folds in — recorded here honestly, never as a reconciled silence |
| Working tree | Clean |
| `docs/adr/` | 0001–0010 only; ADR-0011 through ADR-0026 open at their own Session 0s; ADR-0027's eight rows are the rows MP-53 will fill; **ADR-0028 is this roadmap's ledger** |
| `figures/` | Zero tracked files (gitignored build product, provenanced by the manifests, never by git); `portfolio/figures/` holds the twelve tracked figures |
| Rung 6 residue | Confirmed still on disk: `figures/exp6_automated_vs_manual.png` + `src/experiments/__pycache__/exp6_automated_circuit.cpython-312.pyc` — MP-51's Session 1 owns the removal; this roadmap's Session 1 re-verifies the absence |
| `checklists/` | Only `reproducibility-checklist.md`; `gate-debt.md` still absent — a dated fact, never a silence |
| `portfolio/README.md` | Still stale: the three "not yet" rows contradict the record (paper through the v22 arc, site and Space live since the premiere, manifest machinery since Micro-Phase 8) — MP-51's Session 1 owns the dated fix; every Session 1 since re-verifies it; this roadmap's Session 1 re-verifies the closure |
| `portfolio/projects/` | Figures only, no project write-ups (`.gitkeep` and nothing else) |
| Annexes | No `essay-annex-*.md` on disk — they live on the live shelf; the v23 snapshot pair is MP-53's; this roadmap verifies the v23 pair and writes the v24 pair |
| CI | `python-ci.yml` (ruff, blocking mypy allowlist, non-blocking full-tree mypy, pytest + coverage), `markdown-lint.yml` (markdownlint-cli2 over the whole vault), `conventional-commits.yml` (commitlint — with the `commitlint-new` mirror in ci-check since the MP-52 incident); no Pages deploy workflow; no LaTeX toolchain locally (`make paper` graceful, not green — the green-to-PDF verification is a standing Session 1 row) |
| Ledger | ADR-0003 rows 3–7 still carry UNDECIDED cells — the R1 verdict stamp, the R4/R5 scheduled negatives, the paper prose and the graduation proof must be dated before MP-29's Session 8, or the entire stack stalls; the pre-draft prose exists on disk from the prior waiting windows (Ex-Ψ2 verifies, never re-drafts) |

### The stack

MP-29 is current and mid-execution (terminus ≈ 2026-08-26); **MP-30 through
MP-36 stand pre-registered, gated in series, the cap at seven**. Each phase's
Session 0 consumes the previous phase's release report: no release, no phase.
MP-37 through MP-53 are the un-cap's roadmap drafts executed exactly once
each. **MP-53's review and roadmap are merged, its Session −1 study lane owns
the waiting window, and its Session 0 awaits the stack's release.**
**ADR-0027's eight rows are the rows MP-53 will fill**; **ADR-0028's eight
rows are the rows this roadmap will fill** — exactly once, under the continuum
law, twenty-third execution, written from MP-53's release report rather than
from the habit of pre-registering.

### The CI floor and the toolchains

190 tracked tests, ruff, blocking mypy and markdownlint are green at the last
release — and the test suite was re-verified collected-green **in this
drafting sitting** (190 in 2.60 s), `verify-claims` at 0. The verified gaps,
stated as facts not hopes: no LaTeX toolchain on this machine (`make paper` is
graceful, not green — the green-to-PDF verification is a standing Session 1
row, re-verified by this phase's Session 1), no Pages deploy workflow in
`.github/workflows/`, no `publish:` frontmatter policy, `portfolio/projects/`
holds figures but no project write-ups, W&B never connected. Each is a dated
row owned by named rows of earlier phases — their residue, never my
re-planning. The `typecheck-new` ratchet remains the house rule for all new
research code — a module that touches the manifest machinery lands in the
strict allowlist (`src/results.py`, `src/experiments/runner.py`) or it stays
out of the blocking gate with its error count recorded. The `commitlint-new`
mirror (origin/dev..HEAD) is in ci-check since the MP-52 footer-line incident
and must be green before any push.

### The showcase corpus at intake

12+ provenance-guarded figures (the count grows with whatever MP-53's science
adds), the paper through the v22 arc (the v23 rule is MP-53's, **the v24 rule
is this phase's**), the site and Space live since the premiere, the essay
annexes through the v22 arc (the v23 annex is MP-53's to write and this
phase's to verify; the v24 annex is this phase's), twenty-two runnable
teaching artifacts with stranger-run transcripts (the receipts land only if
the stack ships: the twenty-second ships in MP-53, **the twenty-third in this
phase**). My teaching lane ships the twenty-third artifact this phase.

## Part II — The bottleneck analysis (what I must not let drift)

1. **The intake is a consumption thirteen generations deep.** MP-54's Session
   0 must **consume MP-53's Session-0 decision with dates** — the single most
   dangerous drift is re-litigating a decision already consumed twelve times:
   re-opening candidates the twenty-second question already closed with dated
   reasons, or treating "the post-record arc governs" as a mood instead of as
   a stamped verdict. The decision chain is now thirteen generations deep; a
   sitting stamps, it never re-decides.
2. **The stacked execution is still the critical path — and its head is still
   MP-29.** MP-54's Session 0 consumes MP-53's release report, which awaits
   the stack. A slip at any link slides the whole chain; **my highest-
   leverage act is unchanged: protect MP-29's window** — its release report is
   the artifact everything downstream consumes. Nothing in this phase may
   borrow a minute from it, and this draft is written verdict-agnostic by law:
   it re-plans not a single row of MP-29 through MP-53.
3. **ADR-0003 still carries UNDECIDED rows, and the ledger is the schedule.**
   The R1 run *completed* 2026-08-14, but rows 3–5 have not been stamped with
   their verdicts (the no-head negative for row 3; the scheduled negatives
   for rows 4–5), and rows 6–7 (paper prose, graduation proof) remain
   undated. MP-29's Session 8 requires zero UNDECIDED rows; a slip here
   stalls the entire stack. I do not re-plan those rows — and the pre-draft
   prose of the scheduled negatives exists on disk from the prior waiting
   windows (Ex-Ψ2 re-verifies it with a date, never re-drafts it), so the
   stamping sitting is a stamping, never a discovery.
4. **The microscope budget is one failure away from exhaustion — and its
   verdicts will likely land long before this phase's Session 0.** Trial 2's
   verdict forces trial 3's choice (the ledger's "my own third"); three
   failures close row 2 and make the dense characterization the phase's
   headline. Verdict-agnostic readiness means: **trial 3's pre-registration,
   drafted in prior waiting windows, is re-verified with its falsifier column
   filled (Ex-Ψ2)** — so no sitting ever chooses an improvised third trial,
   and no phase ever re-drafts what a lane already owns.
5. **The CPU wall is the science's binding constraint — and the budget now
   runs on observed rates, never estimates.** Every pending run (trial 2,
   trial 3, the characterization's per-head dictionaries and ablations)
   shares one CPU and overnight windows. The observed rates MP-29's runs
   produce (~2.5 s/epoch × 5000 epochs ≈ 3.5 h wall per trial, the
   characterization at ~1–2 h, the SAE re-run at ~1 h) become the budget's
   ground truth; anything this phase launches gets a budget row at launch,
   never at Session 7 — heartbeat, checkpoint-every-500, scheduled negative
   drafted while the run is live.
6. **The steady state must not become ceremony — and at generation
   twenty-three the roadmap machinery itself is the risk.** MP-54 will be the
   seventeenth roadmap written from an *executed* roadmap's release report —
   the program's normal, confirmed sixteen times. The pre-draft stack has
   been re-drafted in every waiting window since MP-48; the countermeasure is
   concrete: **Ex-Ψ2, the pre-draft stack audit** — every artifact a prior
   lane already owns is verified on disk with its date and updated in place,
   never re-drafted from scratch — and every session's exit names at least
   one artifact changed on disk, and every row is dated in the sitting that
   owns it. A stamped row with no science behind it is ceremony by another
   name.
7. **The paper's compile gate is executable — which makes its drift subtler.**
   By this phase's Session 0, the toolchain will be pinned and the
   green-to-PDF verification a standing Session 1 row. The new risk is not a
   missing toolchain but a *ceremonial* one: the gate "passes" because
   `make paper` is graceful-by-design, and the v24 rule ("opens only for new
   numbers, else the v23 is the record") becomes a way to never compile. The
   countermeasure: Session 1 verifies `make paper` green on this machine
   **and** in the CI mirror with a dated transcript — a compile that produces
   a PDF, not a message.
8. **Stop-and-publish is a row, not a threat — and the post-record criterion
   is now thirteen questions deep.** ADR-0004's row 5 stays open as the
   program's honest exit: a phase is worth doing only if its candidate set
   can earn a paragraph the record does not already have. If MP-53's Session
   0 continued the post-record arc, the deepest candidate this phase can
   choose earns the post-record arc's *twelfth new paragraph* — the record's
   closing sentence consumed thirteen times, never repeated. The deepest form
   of laziness is building what the record has already said.
9. **Path patching may still be validated only by unit tests.** The R1
   no-head negative means the R4/R5 chain closes with scheduled negatives;
   head ablation and path patching remain unvalidated end-to-end until a
   confirmed head exists anywhere on the record. If C85 opened in MP-53, its
   patching verdicts were the first chance to close this gap — the intake
   tells me which. If the gap persists, C89's/C90's patching verdicts are the
   next chance; the protocol note must state explicitly which patching
   machinery is being validated for the first time, so the verdict doubles
   as an instrument validation or a dated instrument negative.
10. **The annexes live only on the live shelf — the snapshot rule is now a
    standing row.** MP-52's Ex-Φ made the record's first defense against a
    hosting-side loss a dated, read-only repo mirror written in the annex's
    own writing session. This phase: Session 1 re-verifies the v23 pair
    (shelf copy hash vs. repo snapshot, `verify-claims` checking the pair),
    Session 3 writes the v24 pair — the rule is a row, never a gesture.
11. **Figure provenance is silently re-derivable, never re-derived — the
    audit is now a standing row.** MP-52's Ex-Ω made `make reproduce` against
    the frozen configs a dated audit. This phase re-runs it against the grown
    corpus: a figure that no longer regenerates from the committed config is
    a silent lie wearing a manifest tag, struck with one dated reason.
12. **The waiting window is now four phases wide (new this sitting).**
    MP-51's, MP-52's, MP-53's and MP-54's Session −1 lanes share the same
    weeks before the stack's release. The collision risk is real: four lanes
    drafting the same trial-3 pre-registration, four intake checklists, four
    memo skeletons. The countermeasure is separation: each phase's pre-drafts
    live in named files of their own beside the lanes, never inside them, and
    MP-54's lane *verifies* the stack in place (Ex-Ψ2) instead of adding a
    fourth draft.

## Part III — The roadmap, step by step (the continuum law, twenty-third execution)

### The frozen candidate set (chosen at Session 0, never improvised)

| # | Candidate | Opens only if | Why it would close |
|---|---|---|---|
| C89 | **The paradigm confirmed a seventh time, or its boundary mapped** (C85's successor) — the failure-cell theory *predicted a seventh time*: the per-head mechanism at the eighth unseen task family's and the seventh architecture family's failure cells written as falsifiable predictions before any number is read, causally verified by patching, the theory's domain statement extended from "predicts unseen cells six times" to "predicts unseen cells seven times" — a paradigm that survives a seventh prediction is a theory with a confirmed domain; a paradigm that breaks on its seventh round is a boundary with a map, and the map is the result | ADR-0027 row 3 = C85 with a positive verdict (the sixth prediction on disk) | C85 closed negative, or the post-record arc governs → the theory's seventh round belongs to the post-record arc |
| C90 | **The equation of state's third transfer** (C86's successor) — the full P×wd×recipe×architecture space *used a third time*: the root-cause map closed at six recipes now asked a third time what it can do — the seventh recipe's failure cells *predicted from the map before the recipe runs*, each prediction ablated or mapped, the equation of state earning its name by transfer, not by accumulation — a boundary that predicts three unseen recipes is an equation of state with a two-transfer record; a boundary that re-measures is a phase diagram, and the diagram is the result | ADR-0027 row 3 = C86 with the sixth-recipe closure on disk | C86 never opened, or its verdict was negative → no equation of state to transfer |
| C91 | **The institution, seventeenth study** (C87's successor) — the twelfth drift measurement after the eleventh dated fix, the rate function's parameters re-estimated from the receipt system's history, the next measurement's schedule *predicted before it happens* a sixth time and the policy *enforced* across the stack's own execution window a sixth time — an institution that survived six enforcement windows is a constitution that keeps its own schedule; a discipline that predicted five times and kept its date is an institution, and the institution is the result | ADR-0027 row 3 = C87 with the eleventh measurement and attribution on disk AND ≥ 23 stranger-run transcripts at S0 | Fewer than 23 transcripts, or C87 never opened → the receipt system hasn't earned a seventeenth study |
| C92 | **The standard, ninth cohort** (C88's successor) — the eighth-edition course *validated a ninth time by the uninvited* under the rubric *already released as a standalone artifact others can run*: the scoring rule's seventh prediction round checked against the ninth cohort's friction, the feedback-to-fixes matrix's seventh prediction round executed — an instrument validated eight times by the uninvited is the standard others cite; an instrument validated seven times is a standard with a track record | ADR-0027 row 3 = C88 with the eighth cohort's measured outcome on disk | C88 never opened, or a sparse regime exists → the sparse reading owns the question |

The universal override stands: **if any sparse cell (k_99 < P/2 sustained ≥
3 checkpoints) exists anywhere on the record by Session 0, the sparse-regime
mechanism — the Nanda-style per-frequency reading on the first sparse
solution this harness ever produced — owns the question and all four
candidates close with that verdict.**

The terminal-state override stands, now thirteen generations deep: **if MP-53's
Session 0 consumed MP-52's decision with dates and the post-record arc
governs, then MP-54's Session 0 consumes the twelfth post-record question's
verdict from ADR-0027 row 3 and continues the post-record arc, choosing the
thirteenth post-record question from the pre-registered continuation set
below.** The rule is executed with dates at Session 0; it is never improvised
and never re-negotiated in the sitting that consumes it.

### The post-record continuation set (chosen only if MP-53 continued the post-record arc)

| # | Candidate | Why it would open | Why it would close |
|---|---|---|---|
| PR-37 | **The new harness's eighth cross-recipe law** (PR-34's successor) — the *tenth* recipe at the new address replicated across seeds and compared to the first nine under the record's laws: ten recipes compared across seeds is the harness's eighth law datum; nine recipes compared once is a seventh datum, and the datum is the result | The post-record arc continued at MP-53 with PR-34's verdict on disk | The record never closed, or the redemption fired first → the sparse question belongs to the old arc |
| PR-38 | **The law at the record's edge, thirteenth task** (PR-35's successor) — the frozen-checkpoint predictions tested at the thirteenth unseen task family: a law that predicts thirteen times is a law with a predictive record; a law that breaks is a boundary with a map | The post-record arc continued at MP-53 with PR-35's verdict on disk | The record never closed → the law's successors are C89's, not the post-record arc's |
| PR-39 | **The record as a course, twelfth edition** (PR-36's successor) — the eleventh edition revised from its tenth intake: the feedback-to-fixes matrix executed with dates, the twenty-three runnable artifacts assembled, the twelfth edition measured as a learning instrument with eleven cohorts — a course revised from its receipts eleven times is a curriculum; a course re-shown is a poster | The post-record arc continued at MP-53 with PR-36's verdict on disk | The record never closed → the teaching lane continues as the continuum's row 8 |

The likely survivor, written as a condition chain, never a prediction: if
MP-53's Session 0 continued the post-record arc → **the post-record
continuation** — the thirteenth question past the record, chosen in the
consuming sitting from PR-37/PR-38/PR-39; else if C85 landed positive →
**C89** — the paradigm's seventh prediction, always CPU-runnable on
checkpoints that exist today; else if C86's sixth-recipe closure landed →
**C90**; else **C91** (always-runnable, the showcase's own science, receipts
now twenty-three deep); C92 is the evidence lane and the teaching lane's
anchor.

### The pending-run wall-clock budget (verified against observed rates)

The runs the stack still owns, budgeted from observed wall-clock rates so no
launch is ever a discovery — and re-read by this phase as the ground truth
for whatever it launches:

| Run | Observed rate | Budget | Window discipline |
|---|---|---|---|
| Microscope trial 2 (`--schedule constant`, P=113, seed 0) | ~2.5 s/epoch (micro1) | ~3.5 h for 5000 epochs | Launch at window open; heartbeat; checkpoint-every-500 |
| Microscope trial 3 (wd 1.5×, P=113, seed 0) | same | ~3.5 h | Pre-registered in prior waiting windows (Ex-Ψ2 re-verifies); verdict forces the choice, never the schedule |
| Dense characterization (per-head dictionaries, ablations on frozen checkpoints) | reads only | ~1–2 h | Session 3, reads from disk, no training |
| SAE re-run on a confirmed-head checkpoint (ADR-0003 row 5) | exp5 rates | ~1 h | Only if a head exists; else the scheduled negative is the result |

### The sessions

1. **Session −1 (~1 h/day, now → the stack's release) — the waiting-window
   study lane.** The days before MP-53's Session 0 are owned, not idle — and
   the window is now four phases wide: MP-51's, MP-52's, MP-53's and MP-54's
   lanes share the same weeks. Each day: one study block from Part IV
   (reading → prediction written *before* the reading → one-page memo filed
   in the study log — each memo linking at least two notes, per the vault's
   orphan law), the clock-check habit, and one waiting-window exercise
   (Ex-α7 through Ex-ε7). Deliverables: **Ex-Ψ2, the pre-draft stack audit** —
   trial 3's pre-registration, the R4/R5 scheduled-negative prose, the S0
   intake checklist, the C89–C92 opening-or-closure memo skeletons, the Ex-T7
   execution-memo skeleton and the annex-snapshot one-pager each verified on
   disk with its date from the prior lanes, updated in place, anything
   missing drafted once with a dated reason. All saved beside MP-51's,
   MP-52's and MP-53's lanes, never inside them. *Exit: the study log has
   one dated entry per day; the audit table dated; no row of MP-29 through
   MP-53 was touched.*
2. **Session 0 (~1 h) — the gate truthing + the thirteen-generations-deep
   arc + the continuum choice.** Consume MP-53's release report row by row:
   ADR-0027 at zero UNDECIDED rows, the live URL re-clicked in the sitting,
   `verify-claims` at its actual count, the twenty-second teaching transcript
   on disk, `dev == main` (branch list as the transcript). Commit the intake
   table before a single continuum row opens. Then **Ex-T7: consume MP-53's
   Session-0 decision with dates** — the thirteenth-generation consumption:
   if the post-record arc continued, the twelfth post-record question's
   verdict is read from ADR-0027 row 3 and the thirteenth post-record
   question chosen from the pre-registered continuation set (PR-37/PR-38/
   PR-39), each opening-or-closure memo in three sentences with a falsifier;
   if not, the C89–C92 adjudication: exactly one opens as row 3, the
   unchosen close with one dated reason each, stamped in the same sitting.
   Open ADR-0028 with its eight rows, windows and kill-dates; declare the
   terminus (release = merge plus 14 calendar days); promote this roadmap
   from MP-53's release report, deviations recorded as dated ledger notes.
   **The toolchain decision is ratified here** — pinned by MP-51's Session 0,
   verified to a PDF in every Session 1 since; this sitting re-checks the pin
   survives contact with the record and re-checks `make paper` in the CI
   mirror. *Exit: intake signed; the thirteen-generations-deep arc stamped;
   row 3 chosen (or the post-record continuation row opened); ledger open.*
3. **Session 1 (~1 h) — the shelf baseline + the debt re-verification.**
   Row 5: hostile-webmaster walk of the live site + Space at zero (links,
   assets, a11y, orphans) — extended to the repo's own shelf: local `main`
   re-verified reconciled to `origin/main` (branch list as the transcript),
   `portfolio/README.md`'s staleness verified closed (MP-51's Session 1 owned
   the first fix; every Session 1 since verified it; this sitting re-verifies
   the file is current), the exp6 residue verified absent with a transcript,
   the annexes' location verified **and the v23 snapshot pair re-verified
   (Ex-Φ)**, the tracked figures re-derived from `make reproduce` (Ex-Ω,
   against the grown corpus). Row 8: MP-53's stamped closures re-verified
   (W&B, clean-clone proof, graduation proof, `reproduce-multiseed`
   exp2/exp5, the exp5 1000-epoch resolution, the README fix, the residue
   removal, the toolchain decision — **now executed, so `make paper` is
   verified green to a PDF, not graceful**) — each cell
   LAUNCHED-with-transcript or CLOSED-with-one-reason; a claimed closure
   without its transcript stays open and blocks Session 8; `gate-debt.md`'s
   absence, if still absent, recorded with a date. *Exit: rows 5 and 8
   stamped.*
4. **Session 2 (~1–2 h) — the consumed-verdict sitting (rows 1, 2).** Row 1:
   the twenty-second research question's verdict (ADR-0027 row 3) becomes the
   paper-v24 section, the annex table, or the results-page row — every number
   manifest-tagged, consumed in the sitting that owns it; if the post-record
   arc governs, the post-record statement is framed from MP-53's release,
   never rewritten. Row 2: v24 opens only if row 1 lands new numbers; else
   "the v23 is the record" is the dated reason and `make paper` is
   re-verified against v23 — **green, with the PDF on disk**. Row 6's
   substitute filed from the visitor's chair, before the window opens (Ex-G);
   the fork drill (Ex-H) and the arc consumption (Ex-N through Ex-T7) land
   here. *Exit: rows 1 and 2 dated; substitute filed; Ex-T7's execution memo
   on disk.*
5. **Session 3 (~2–3 h) — the essay annex v24.**
   `portfolio/essay-annex-24.md` (its home on the live shelf, dated, **with
   the repo-side snapshot written in the same sitting per Ex-Φ**): the
   twenty-second question's verdict set and the teaching lane's twenty-second
   receipt distilled into one dated annex; the reverse claims audit at zero
   (prose → manifest → command); each claim's "what would falsify this"
   column filled at writing time. The annex is amended, never rewritten.
   *Exit: row 4 dated; audit at zero; snapshot pair on disk.*
6. **Session 4 (~1 h) — the stranger round 24 intake.** Row 6's window opens
   (intake S4, kill-date S5); the feedback-to-fixes matrix pre-stamped:
   friction point → cause → dated fix → re-check row. The recruitment plan
   for the uninvited cohort is executed with dates — the channels that
   produced the first twenty-three transcripts are re-used and one new
   channel is added (a public post on the showcase's own shelf), so the
   "uninvited" property is re-earned, never assumed. *Exit: window open,
   kill-date declared.*
7. **Session 5 (~2–3 h) — the research row pre-registration + launch + the
   teaching kickoff.** Row 3: the chosen candidate's protocol written before
   the first pass (site, metric, negative control, kill-date, falsifier
   column) and the run launched under a heartbeat — or, if the post-record
   arc governs, the continuation row's protocol opened under the same
   discipline. If C89: the failure cells at the eighth unseen task family
   and the seventh architecture family, and the expected per-head mechanism
   written as falsifiable predictions before a single number is read (Ex-C,
   Ex-I7, Ex-J7, Ex-S7, Ex-U7, Ex-W7) — and the patching-validity note
   appended (Part II, item 9), so the run doubles as the instrument's
   end-to-end validation or its dated negative. If C90: the seventh recipe's
   failure cells *predicted from the completed map* (Ex-X7). The scheduled
   negative is drafted *while the run is live* (Ex-D), so the S6 verdict
   sitting is a stamping, not a discovery. Row 6's kill-date honored
   (feedback → matrix drafted; silence → substitute closes it). Row 7: the
   twenty-third teaching artifact's skeleton drafted — walkthrough v23,
   10-minute talk v23, or Colab grokking notebook v21 — with its ship-date.
   *Exit: row 3 pre-registered and launched (or the post-record protocol
   opened); row 6 dated either way; row 7's skeleton drafted.*
8. **Session 6 (~1–2 h) — the research verdict sitting.** Row 3's verdict
   read from the manifest: completed and dated, or window closed and the
   scheduled negative is the result — drafted while the run was live (Ex-D),
   so this sitting is a stamping, not a discovery. *Exit: row 3 dated either
   way.*
9. **Session 7 (~2–3 h) — the shelf rehearsal + the re-check row + the
   teaching polish.** Row 5: the hostile-webmaster walk at zero beside the
   browser, every public number clicked back to disk; the repo-shelf findings
   re-checked (local `main` reconciled, README current, residue gone, annexes'
   home verified, v23 + v24 snapshot pairs current, figures re-derived).
   Row 6's re-check row dated. Row 7: the twenty-third artifact runs end to
   end on a stranger's machine (fresh clone / Colab session); the run
   transcript is the receipt; the teaching distillation (Ex-F) lands here.
   *Exit: rows 5, 6, 7 dated; the artifact shipped with its transcript.*
10. **Session 8 (~1 h) — the release.** ADR-0028 at zero UNDECIDED rows; the
    merge green locally and on GitHub; `dev == main`; home wired — this
    roadmap's companion status retired; the roadmap archived with its
    deviations, every deviation a dated ledger note. If the post-record arc
    governs, this sitting stamps the post-record arc's thirteenth dated
    direction — the record's closing sentence consumed thirteen times, never
    repeated. *Exit: the merge; the program's twenty-third dated direction —
    or the post-record arc's thirteenth.*

### The one measured line

ADR-0028 at **zero UNDECIDED rows** on release day, with exactly one LAUNCHED
research row (or the post-record continuation row) whose verdict (or
scheduled negative) re-derives from a manifest; `verify-claims` at 0 with
every public number re-derivable from one command line; the hostile-webmaster
walk at zero on the live shelf and on the repo's own shelf (local `main`
reconciled, README current, residue removed, the debt ledger present or
absent-with-date, the annex snapshot pairs current, the figures re-derived);
**the paper compiled to a PDF on this machine and in the CI mirror, or the
dated v24 rule recorded**; the twenty-third teaching artifact shipped with a
stranger-runnable transcript; `dev == main` and the program's twenty-third
dated direction — or, if the post-record arc governs, its thirteenth dated
direction.

## Part IV — Deep-dive study and research topics

The study I will do between now and the verdict sitting — each reading with
the paper, the one question it must answer, the prediction I write before a
single number is read, and the primary source on disk. Filed as one dated
memo each in the study log (Session −1).

1. **The paradigm confirmed a seventh time, or its boundary (the C89
   reading).** Elhage et al., *A Mathematical Framework for Transformer
   Circuits* (2021) for the QK/OV machinery the causal claim is made over;
   Wang et al., *Interpretability in the Wild* (2022) for activation-patching
   methodology at per-head resolution; Conmy et al., *Towards Automated
   Circuit Discovery* (2023) for turning a hand-traced mechanism into a
   scalable, testable procedure (read, never re-implemented — ACDC stays
   descoped); Varma et al., *Explaining grokking through circuit efficiency*
   (2023) for why circuits grow sharp and where that sharpness is measurable;
   Olsson et al., *In-context Learning and Induction Heads* (2022) for what
   transfers across task families; Chughtai et al., *A Toy Model of
   Universality* (2023) for why the eighth unseen task family's and the
   seventh architecture family's failure cells fail the way they do — now
   read at the *seventh-prediction* axis: what a theory earns by predicting
   unseen cells seven times, where six-round paradigms overreach on their
   seventh round, and what Popperian corroboration and Lakatosian
   progressivity say about a law whose seventh out-of-sample round lands.
   Nosek et al., *The Preregistration Revolution* (2022) — for
   pre-registration as the seventh trial's own instrument: what a theory that
   pre-registered its seventh prediction can claim that one that predicted
   after the fact cannot. My C85 verdict and its measured theory frame the
   reading. **Prediction to write**: which per-head role's failure mechanism
   is the boundary's root cause at the eighth unseen task's structure and at
   the seventh architecture family's, and what the patching at those cells
   reveals; the null hypothesis every measured fingerprint is compared
   against. **Primary sources**: the frozen checkpoints, C85's theory table,
   the S3 note.
2. **The equation of state's third transfer (the C90 reading).** Lyu et al.,
   *Understanding the training dynamics of transformers on modular
   arithmetic* (2024) for the loss-landscape structure of grokking and its
   phase transitions; Morwani et al. (2024) on the edge-of-numerical-
   stability regime; Gromov, *Grokking: A Memory Perspective* (2023); Power
   et al. (2022); Nanda et al. (2023) — now read at the *transfer* axis, a
   third pass: what a full-cell root-cause map that has already transferred
   twice *predicts* about a recipe it has never seen a third time, and where
   "the driver" is really an optimization artifact that does not survive its
   third out-of-map recipe. **Prediction**: the seventh recipe's failure
   cells written before the analysis; C86's completed equation of state and
   C89's second transfer are this reading's admission tickets.
3. **The institution, seventeenth study (the C91 reading).** Gelman & Loken,
   *The Garden of Forking Paths*; Pineau et al. (2021); Kapoor & Narayanan,
   *Reproducibility in Machine Learning: A Systematic Literature Review*
   (2023); the ML reproducibility line (NASEM's five pillars); Lakens,
   *The Value of Preregistration for Psychological Science* — now read at the
   *constitution* axis: what a policy gains when its next measurement is
   predicted *before* it happens a sixth time and kept on its own schedule,
   and what a discipline can honestly claim that a model cannot. My
   twenty-three stranger-run transcripts are the data; the sixteenth study
   defined the twelfth drift, I must decide what counts as the seventeenth
   measurement before I measure any.
4. **The standard, ninth cohort (the C92 reading).** Bricken et al. (2023);
   Cunningham et al. (2024); the dictionary-circuit and feature-universality
   line — plus the education-measurement line (rubric validity, inter-rater
   reliability, external assessment, instrument release norms) for what a
   *ninth, uninvited cohort* under a *released standard others can run*
   claims that an eighth's does not. My Rung-5 datum (99.97% FVE, L0 =
   136/256, 0% dead features) and C88's ninth-cohort outcome are the record's
   first data points.
5. **The post-record program, thirteenth generation (new, deepest).**
   Lakatos, *The Methodology of Scientific Research Programmes* (1978) — read
   a fourteenth time, now for the *thirteenth* question past a completed
   program: progressive vs. degenerating problem shifts when the *twelfth*
   post-record verdict lands, Kuhn's normal science as the post-record arc's
   axioms, and the honest criterion for the thirteenth post-record question —
   a question that must earn the post-record arc's twelfth *new* paragraph.
   This reading feeds Ex-T7 and the Session-0 question MP-54 owns more deeply
   than any phase before it: *what does the record's twelfth post-record
   verdict open?* The answer can be the post-record arc's thirteenth dated
   row — Lakatos' point is that the decision is made on the record, never as
   a mood.
6. **The record teaches, round twenty-three.** The twenty-third verdict in
   four registers — the paper's sentence, the annex's sentence, the 30-second
   spoken claim, and the 5-minute teaching explanation with a worked toy a
   stranger can run; the gap between the last two is where my teaching
   leaks, and I will measure it deliberately by writing all four registers
   for the same verdict (Ex-F). **Waiting-window rehearsal**: run the four
   registers on the R1 no-head negative — a stamped verdict, safe to
   practice on.
7. **The redemption reading, or negative results as maps, the twenty-third
   pass.** If a sparse cell exists by S0: Nanda et al.'s full per-frequency
   reading on the first sparse solution this harness ever produced. If not:
   how the *completed* law is reported honestly — the law's domain closed
   with its measured boundaries and its failure cells explained or mapped,
   the driver a principle or a case study with a dated exception map, the
   drift numbers twelve deep, the negative as a contribution — and how the
   post-record harness (if PR-37 governs) would be designed from the dated
   negatives instead of from hope. Either way, the paper's hardest paragraph
   is the one that claims the dense solution *computes something*; I will
   draft it against this reading and let the manifest referee it.
8. **The mathematical bedrock, seventh pass (new).** The DFT-of-addition
   derivation I hand-rolled in the waiting windows extended to the *seventh
   architecture family's* geometry: what changes in the embedding's spectral
   support, the QK/OV factorization and the convolution theorem when the
   family changes a sixth time — the derivation that makes every
   seventh-family fingerprint interpretable rather than decorative.
   **Primary sources**: Nanda et al. (2023) and its appendix; my own
   `01_foundations` linear-algebra proofs; the exp2 Fourier instrument on
   disk. **One runnable check**: the hand derivation reproduced in a one-file
   script whose DFT output matches `results/exp2_grokking.json`'s k_99 =
   111/113 at P=113, then re-run at the seventh family's geometry.
9. **The paradigm's sociology, third pass (new).** Kuhn, *The Structure of
   Scientific Revolutions* read against my own record a third time: when a
   paradigm claim that has predicted *seven* times still requires a community
   rather than a track record, what normal science looks like for a
   one-person program at its seventh confirmation, and how the paper should
   say "paradigm" without overclaiming the collective — the reading that
   keeps C89's victory honest in its own terms, and the threshold at which
   the record's "theory" line stops being a research programme and becomes a
   paradigm others must engage.
10. **The long-window discipline, second pass (new).** Pacing a
    four-phases-wide waiting window: how the study lane stays a lane rather
    than becoming a ceremony factory — the spacing-effect line (Ebbinghaus
    and the modern replication of the spacing effect) for why one dated memo
    per day outlearns a crammed weekend, the daily-habit mechanics my own
    study log has proven across three phases, and Ex-Ψ2 as the lane's own
    gate. The waiting window is the program's longest since the premiere; a
    window with no dated entry is a row without a date.

## Part V — Documentation requirements (the contract)

Everything this phase claims re-derives from a manifest and a command. The
documentation I will write, and where:

- **This roadmap**, promoted from the companion review at Session 0,
  rewritten from MP-53's release report, deviations recorded as dated ledger
  notes.
- **ADR-0028**, the twenty-third continuum ledger — eight rows pre-stamped
  with windows and kill-dates; rows 1–2 consumed from ADR-0027's verdicts;
  row 3 the twenty-third research question with its protocol note and
  heartbeat (or the post-record continuation row's protocol); rows 4–8 the
  continuum's decisions.
- **`portfolio/essay-annex-24.md`** — the v24 annex, manifest-tagged,
  amended never rewritten; the annexes' home (the live shelf) recorded with
  a date **and the repo-side snapshot written in the same sitting (Ex-Φ)**;
  the v23 snapshot pair re-verified at Session 1.
- **The paper v24 diff** (`portfolio/paper/main.tex` v24 + diff log) or the
  dated "the v23 is the record" memo; **`make paper` verified green to a PDF
  on this machine and in the CI mirror**, with the toolchain pin ratified at
  Session 0 (MiKTeX + TeX Live CI action per MP-51's pin, verified in every
  Session 1 since and re-verified here).
- **The shelf health sheet + hostile-webmaster transcript** (site + Space at
  zero), extended to the repo's own shelf: local `main` reconciled to
  `origin/main`, `portfolio/README.md` current, the exp6 residue removed, the
  annexes' location verified, the v23 snapshot pair current, **the figures
  re-derived (`make reproduce` transcript attached, Ex-Ω)**; the claims gate
  re-run on every merge.
- **`checklists/gate-debt.md`** — each cell's transcript or one-line reason,
  dated in Session 1; the file's absence, if still absent, recorded with a
  date.
- **The research row's pre-registration note** (site, metric, negative
  control, kill-date) in `06_production_ai/notes/` + the heartbeat artifact;
  if C89: the seventh-prediction figure spec written before the analysis,
  the figure itself manifest-tagged after, and the patching-validity
  appendix (Part II, item 9). If C90: the seventh recipe's predicted
  failure-cell table (Ex-X7) committed before the analysis. If the post-
  record arc governs: the continuation row's protocol note instead.
- **The twenty-third teaching artifact + its stranger-run transcript**
  (fresh-clone or Colab session receipt).
- **Ex-T7's execution memo** — MP-53's arc decision run with dates, written
  verdict-agnostic and executed at Session 0.
- **The study log** (now a standing lane, its fifth phase): one dated memo
  per reading, each linking at least two notes — the vault's orphan law
  applied to the study lane itself.
- **The waiting-window pre-drafts** (alongside MP-51's, MP-52's and MP-53's
  Session −1 lanes): the S0 intake checklist pre-built with empty date cells,
  the C89–C92 opening-or-closure memo skeletons, the Ex-T7 execution-memo
  skeleton, the annex-snapshot one-pager — each verified in place from the
  prior lanes' drafts (Ex-Ψ2), updated with dates, never re-drafted from
  scratch.
- **`00_meta/03-progress-log`** — one dated entry per session; home wired at
  release; the continuum ledger's rows cited by the skill tree's publication
  flips.

## Part VI — Practical exercises and hands-on challenges

1. **Ex-A · The C89–C92 adjudication drill (S0):** each candidate's
   opening-or-closure memo in three sentences with a falsifier; exactly one
   opens; the unchosen close with one dated reason, stamped in the same
   sitting — preceded by the arc consumption (Ex-N through Ex-T7), which may
   close the whole set with the post-record verdict.
2. **Ex-B · The consumed-verdict reverse audit (S2):** every number from
   ADR-0027's row-3 verdict traced to its manifest and its command; the rest
   struck with a reason — the hostile-webmaster test of my own prose,
   twenty-third run.
3. **Ex-C · The falsifiable-prediction sprint (S5):** if C89 or C90 opens,
   the question's predictions written as falsifiable statements before the
   analysis — the failure cells and the expected per-head mechanism at the
   eighth unseen task's structure and the seventh architecture family's
   (C89), or the seventh recipe's predicted failure cells from the completed
   map (C90) — the "what would falsify this" column filled at writing time.
4. **Ex-D · The scheduled negative drafted before the run ends (S5):** the
   negative written while the run is live, so the S6 verdict sitting is a
   stamping, not a discovery.
5. **Ex-E · The hostile-webmaster walk v24 (S7):** the live site + Space at
   zero — links, assets, a11y, orphans, dead figures — walked as a complete
   transcript, with the repo's own shelf added: branches reconciled, README
   current, residue removed, snapshot pairs current, figures re-derived.
6. **Ex-F · The teaching distillation, round twenty-three (S7):** the
   twenty-third question's verdict in four registers — the paper's sentence,
   the annex's sentence, the 30-second spoken claim, the 5-minute teaching
   explanation with a worked toy a stranger can run; the gap between the
   last two is where my teaching leaks.
7. **Ex-G · The stranger substitute from the visitor's chair (S2):** the
   self-review written from the chair a stranger would occupy — friction
   points → fixes → re-check row — filed before S4, so the S5 kill-date can
   never close the row with a skip.
8. **Ex-H · The fork drill, deepest form (S2, verdict-agnostic):** the
   continuing state (C89–C92) vs. the post-record state (PR-37/PR-38/PR-39)
   written as two one-page paths — what each verdict changes downstream,
   including the C89-vs-C90 choice and the post-record continuation choice —
   so next phase's S0 decision is a stamping, not a discovery.
9. **Ex-I7 · The boundary hand-roll, round twelve (S5, C89 only, before any
   number is read):** the expected per-head mechanism at the eighth unseen
   task's and the seventh architecture family's failure cells written by
   hand from C85's theory table — which per-head roles must transfer
   unchanged, which may re-tune, which should fail first, and what patching
   at those cells should reveal — the null hypothesis every measured
   fingerprint is compared against. One runnable check: the hand-rolled
   fingerprints printed and saved next to Ex-J7's observed ones, so the S6
   comparison is a diff, not a memory.
10. **Ex-J7 · The transfer reader, round twelve (S5, C89 only):** the script
    that loads the frozen checkpoints at every P (including the eighth
    unseen task's and the seventh family's), runs the per-head extraction
    and patching machinery, and emits the failure-cell table as a
    manifest-tagged JSON — with the patching-validity appendix of Part II,
    item 9 attached, so the run's verdict doubles as the instrument's
    end-to-end validation or its dated negative. One runnable check: the
    reader runs on the frozen checkpoints and its output is committed before
    the verdict paragraph is drafted.
11. **Ex-K7 · The sparse-recovery toy, revisited a seventeenth time (my
    foundation challenge, seventh-family pass):** the one-file toy that
    recovers the addition table's DFT coefficients under L2 vs L1 penalties,
    now extended to the completion question: *does the sharpening ablation
    signature survive across seven architecture families and seven recipes,
    and where does it break?* One runnable check: the toy prints both
    reconstructions' sparsity and error plus the ablation table on a fixed
    seed, across seven architectures. This is the micro-scale intuition
    C90's verdict must not contradict.
12. **Ex-L7 · The "what does the dense solution compute?" sprint, round
    seventeen (S5, C89 only):** the paper's hardest paragraph drafted at S5,
    then audited against the mechanism reading at S6 — prose that must
    survive contact with the manifest, the "computes something" claim earned
    or struck with one reason.
13. **Ex-M7 · The stranger-run drill on my own receipt (S1):** I execute
    MP-53's shipped artifact (the twenty-second) on a fresh clone as if I
    were the stranger — the transcript becomes the baseline against which
    the twenty-third artifact's transcript is compared. One runnable check:
    the baseline transcript saved beside the new one.
14. **Ex-N · The arc consumption, second generation (S0):** MP-40's Ex-N
    defined the terminal state; MP-41 executed it; MP-42 through MP-53
    consumed it twelve times. This drill executes that second-generation
    consumption exactly as MP-53's memo stamped it.
15. **Ex-O · The arc consumption, third generation (S0):** MP-52's Ex-O
    defined the third-generation drill; MP-53 executed it; this drill
    consumes MP-53's Session-0 decision with dates, the criteria cited from
    the release it consumes. One runnable check: the execution memo exists,
    names the decision rule, cites the criteria from MP-53's release report.
16. **Ex-P … Ex-S7, Ex-T7 · The arc consumption, generations 4–13 (S0):**
    the consumption chain's deepest runs as MP-53 stamped them — each memo
    cites the criteria from the release report it consumes. One runnable
    check per drill: the execution memo exists and cites the criteria from
    the release report.
17. **Ex-T7 · The arc consumption, thirteenth generation (S0, new,
    verdict-agnostic):** the consumption chain's deepest run — MP-53's
    Session-0 decision consumed with dates as MP-54's intake, the
    twelfth-generation post-record verdict read from ADR-0027 row 3 if the
    arc governs, the criteria cited, the release that follows (the thirteenth
    post-record question, or the C89–C92 adjudication), and what each of
    ADR-0027's possible verdicts changes in that execution. One runnable
    check: the execution memo exists, names the decision rule that closes or
    continues the program's science, and cites the criteria from MP-53's
    release report — the chain now thirteen generations deep, a sitting
    stamps, it never re-decides.
18. **Ex-S7 · The out-of-sample sprint, round twelve (S5, C89 only):** the
    mechanism's predictions at the eighth unseen task family written as a
    dated table before any number is read — task family, expected failing
    head role, expected order of failure, expected patching signature — with
    the falsifier column filled at writing time; the observed table compared
    at S6 as a diff, not a memory.
19. **Ex-U7 · The architecture-family sprint, round twelve (S5, C89 only):**
    the law's predictions at the seventh architecture family written as a
    dated table before any number is read — family, expected per-head role
    transfer or re-tuning, expected failure order, expected patching
    signature — with the falsifier column filled at writing time; the
    observed table compared at S6 as a diff, not a memory.
20. **Ex-V7 · The drift-attribution drill, round nine (S5, C91 only):**
    the rate function's parameters re-estimated from the twenty-three
    transcripts before any fix, the twelfth drift's components attributed —
    harness change vs. protocol drift vs. codebase aging — each component's
    contribution re-estimated, the top root-cause's fix dated in the same
    sitting. One runnable check: the re-estimated parameter table saved
    beside the drift numbers, so the S6 verdict is a diff, not a memory.
21. **Ex-W7 · The theory's falsifier column, round seven (S5, C89 only):**
    each seventh-round failure-cell explanation written with its own
    falsifier — the single observation that would refute the explanation of
    why this cell fails — filled at writing time, before the analysis; the
    S6 verdict is a diff between prediction and observation, never a memory.
22. **Ex-X7 · The equation-of-state prediction table, round seven (S5, C90
    only, new):** the seventh recipe's failure cells *predicted from the
    completed map* before any number is read — cell, predicted root cause,
    predicted ablation signature, predicted failure order — with the
    falsifier column filled at writing time; the observed map compared at S6
    as a diff, not a memory. This is the moment the phase diagram stops
    being a description and becomes a law with a two-transfer record.
23. **Ex-Y7 · The policy allocation drill, round seven (S5, C91 only):**
    the seventeenth measurement's schedule derived from the rate model
    before the run — the next measurement, its budget, its predicted
    outcome, its falsifier — so the S6 verdict compares the schedule against
    what the receipt system actually did, as a diff, not a memory.
24. **Ex-Z7 · The public rubric draft, round seven (S5, C92 only, new):**
    the ninth cohort's rubric written as a public artifact — scoring rule,
    evidence requirements, adjudication procedure, release license — before
    recruitment, so the ninth measurement is taken under the published rule,
    never after it.
25. **Ex-Φ · The annex snapshot (S3, standing since MP-52):** the v24 annex
    written on the live shelf *and* mirrored into the repo as a dated,
    read-only copy in the same sitting; the v23 pair re-verified at Session 1
    (shelf copy hash vs. repo snapshot); the snapshot's own manifest tag, so
    `verify-claims` can check the pair. One runnable check: the repo
    snapshot's hash matches the shelf's dated copy at S7.
26. **Ex-Ω · The figure-regeneration audit (S1, standing since MP-52):**
    `make reproduce` run against the frozen configs and every tracked figure
    in `portfolio/figures/` re-derived — the corpus has grown by whatever
    MP-53's science added, so the audit re-runs against the grown set; a
    figure that cannot be re-derived from the committed command is struck
    from the showcase with one dated reason. One runnable check: the
    re-derived figures' manifest tags match the committed ones.
27. **Ex-Ψ2 · The pre-draft stack audit, second pass (Session −1, new, the
    anti-ceremony gate):** every pre-drafted artifact the prior lanes own —
    trial 3's pre-registration, the R4/R5 scheduled-negative prose, the S0
    intake checklist, the C89–C92 memo skeletons, the annex-snapshot
    one-pager — verified on disk with its date; anything present is updated
    in place with a dated delta, anything missing is drafted once with a
    dated reason. The audit table is the transcript that keeps the waiting
    window a lane instead of a factory. One runnable check: the audit table
    names each artifact, its date, and its delta or its drafted-once reason.
28. **The waiting-window drills (Session −1):** Ex-α7 the DFT hand-roll,
    seventh pass (the derivation extended to the seventh family's geometry);
    Ex-β7 the four-registers rehearsal on the R1 no-head negative; Ex-γ7 the
    scheduled-negative drafting drill — now a re-verification drill: the
    ADR-0003 rows 4–5 prose and trial 3's pre-registration exist from prior
    lanes (Ex-Ψ2), this pass re-verifies the falsifier columns and updates
    in place; Ex-δ7 the stranger-run drill on the twenty-second artifact once
    it ships (the transcript becomes the twenty-third's baseline); Ex-ε7 the
    trial-3 falsifier decision tree re-verified before trial 2's verdict is
    read.
29. **Habit · The clock check (every session):** ADR-0028's undated rows, the
    open PR's CI status line, the shelf's health — all three before any new
    prose.

## Part VII — Strategic tips and architectural best practices

- **The one-question law, twenty-third execution.** A phase that opens two
  research questions is drift by another name; the unchosen candidates close
  in the same sitting as the choice — and the arc consumption may close all
  of them with the post-record verdict. The continuum law is the mechanical
  refusal of this drift — proven executable twenty-two times, it must simply
  be executed again.
- **The candidate set is frozen before S0, never improvised at it.** C89–C92
  are conditions, not predictions; a sitting decides, it never invents — and
  the terminal-state object is the hardest frozen object on the record:
  written by MP-40, executed by MP-41, consumed twelve more times since —
  *consumed a thirteenth time* by MP-54, never re-negotiated in the consuming
  sitting.
- **Consumption is execution.** A verdict consumed into an artifact in the
  same sitting is a result; consumed into a paragraph written later it is a
  memory. Row 1 consumes ADR-0027's row-3 verdict in the sitting that owns
  it — or the post-record statement, if the arc governs.
- **The receipt compounds.** The twenty-third runnable artifact is only
  worth shipping because the first twenty-two transcripts proved the format —
  and if C91 opens, the receipts are a drift-of-drift-of-drift-of-drift-of-
  drift-of-drift-of-drift-of-drift-of-drift-of-drift-of-drift-of-drift number
  measured twelve times in a row, tested by people I did not choose, across
  an aging codebase. My showcase's story is now "read it, run it, watch me
  be wrong on the record," twenty-three receipts deep.
- **The waiting window is a lane, not a gap — and it is now four phases
  wide.** MP-51's, MP-52's, MP-53's and MP-54's Session −1 lanes share the
  same weeks; each phase's pre-drafts live in named files of their own, and
  MP-54's lane verifies (Ex-Ψ2) instead of re-drafting. A day with no dated
  entry is a row without a date.
- **The pre-draft stack is verified, never re-drafted (second pass).** The
  trial-3 pre-registration and the scheduled-negative prose have been drafted
  in every waiting window since MP-48; at generation twenty-three, drafting
  them again is ceremony, and verifying them with a date is discipline. Ex-Ψ2
  is the gate, and the study log itself follows the vault's orphan law: a
  memo that links nothing is a note that proves nothing was understood.
- **Budget the wall-clock at launch, never at Session 7 — and from observed
  rates, never estimates.** The CPU is the binding constraint; the rates
  MP-29's runs produce become the budget's ground truth; every run gets a
  budget row, a heartbeat, a checkpoint-every-500, and a scheduled negative
  drafted while it is live. This is the architecture law that protects the
  release date.
- **A pinned toolchain is a promise; a compiled PDF is a receipt.** The
  toolchain pin landed in MP-51's Session 0 and is verified to a PDF in
  every Session 1 since; this phase re-verifies `make paper` green on this
  machine and in the CI mirror. Graceful failure was the bridge; green is
  the destination. The v24 rule ("opens only for new numbers") remains the
  insurance either way.
- **The record must survive its own shelf.** The Ex-Φ snapshot rule is now a
  standing row: verify the v23 pair, write the v24 pair, and let
  `verify-claims` check both — the record's first defense against a
  hosting-side loss, cheap enough to be a habit and strict enough to be a
  row.
- **Figures must be re-derivable, not just provenance-tagged.** A manifest
  tag on a stale figure is a silent lie; the figure-regeneration audit
  (Ex-Ω) makes "the showcase regenerates" a verified sentence instead of an
  assumption — and it re-runs as the corpus grows.
- **Protect the release report.** The serialized stack means MP-29's release
  is still the artifact everything downstream consumes; a slip at any link
  slides the whole chain. A promise can be re-planned forever, but a dated
  row is answered.
- **The S0 gate is a checklist with receipts.** ADR-0027 at zero, the live
  URL, `verify-claims` at 0, the twenty-second teaching transcript on disk —
  a condition with artifacts, not a paragraph.
- **The negative stays the signature.** The row that closes with one reason
  is stamped like the row that launched; the R1 no-head negative — 0/8
  heads, stamped 2026-08-14 — is the record's newest dated signature. The
  strongest form of the signature is the chain: negative → map →
  characterization → mechanism → causal verdict → circuit → law → theory →
  second prediction → third prediction → fourth prediction → fifth
  prediction → sixth prediction → *seventh prediction* — or a record that
  knew when to end.
- **The steady state is the reward, not the ceremony.** MP-54 will be the
  seventeenth roadmap written from an *executed* roadmap's release report —
  the program at its normal, confirmed sixteen times. The machinery is the
  guardrail, never the goal: rows are dated in the sitting that owns them, or
  they are not rows. The pre-draft stack audit (Ex-Ψ2) is this phase's
  concrete refusal of the ceremony.
- **Architecture laws unchanged.** `dev` only, GPG-signed, Conventional
  Commits with `(meta)`, `(portfolio)`, `(ci)` scopes; CI green before any
  merge; the floor re-verified locally before every push (including the
  `commitlint-new` mirror); zero UNDECIDED rows at Session 8; release =
  merge plus 14 calendar days.
- **The showcase 30-second story:** *the program's twenty-third dated
  direction was written from its own release report — the cap honored, the
  stack executed, the steady state kept honest seventeen times, the record
  taught twenty-three times in runnable artifacts, every public number still
  re-derives from one command line, the paper compiled to a PDF on the
  record, and the record consumed — thirteen times, with dates — its own
  terminal-state decision, and answered it in a release.* Every artifact
  this phase launches is written to that standard.

## Links

- [[00_meta/53_micro-phase-53-review-and-roadmap]] — the twenty-second
  question's review and roadmap; this roadmap's intake is ADR-0027's release
  report and MP-53's Session-0 decision, which Session 0 consumes again.
- [[00_meta/52_micro-phase-52-review-and-roadmap]] — the twenty-first
  question's review and roadmap, the intake chain's previous link.
- [[docs/adr/0004-horizon-ledger]] — the horizon rows, including row 5
  (stop-and-publish), the honest exit every candidate must beat — and the row
  the terminal state executes.
- [[06_production_ai/notes/dense-solutions-modular-addition]] ·
  [[06_production_ai/notes/microscope-trial-table]] ·
  [[06_production_ai/notes/positive-control-protocol]] — the science C89–C92
  adjudicate over, whose pending verdicts are the intake.
- [[06_production_ai/notes/results-manifests-and-provenance]] — the manifest
  machinery every public number cites.
- [[06_production_ai/notes/checkpoint-resume-durability]] ·
  [[06_production_ai/notes/scheduled-negatives-mp28]] — the CPU-budget canon
  the phase's runs are specified against.
- [[00_meta/03-progress-log]] — the dated journal this review will be
  answered in, session by session.
