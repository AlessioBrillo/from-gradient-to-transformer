---
tags: [type/moc, phase/6, phase/7, research/experiment, state/review]
created: 2026-08-10
---

# Micro-Phase 26 — The Continuation: the shelf writes the next book

Written as a personal learning log and a public record, like every roadmap before it.

Every phase since MP-18 enacted the same law: a promise can be re-planned forever, but a
dated row is answered. MP-23 answers the science, MP-24 writes the answers down, MP-25
gives the answers an address. This phase is the first in which the record has a shelf and
the shelf must decide what the next book is: the horizon lanes the premiere executed (the
ACDC pilot, the scaled-up R1) return as verdicts to be consumed into artifacts, the
standing gate debt of six phases gets its final dated treatment, and exactly one new
research question — the first of the post-capstone program — opens as a pre-registered
row under its own ledger. The capstone stops being a project and becomes a practice.

The record's deepest pattern is now complete, and this phase extends it: pre-registration
was once the disease, and the ledger became the cure. The premiere's own law — *launch =
artifact merged + URL stamped, in the same sitting* — is this phase's inheritance, applied
to science and shelf alike. A paper that shipped gets its v2 diff; a site that shipped gets
its health rows; a pilot that ran gets its writeup. Nothing here re-plans a single verdict
of the three phases before it.

## Design decisions

- **The starting artifact is MP-25's release state, row by row.** Step 0 is a truthing
  pass over the premiere ledger's eight stamped rows, the five live URLs (or their dated
  reasons), the executed horizon verdicts, the stranger's round-2 notes and the CI floor —
  the intake discipline MP-21 applied to MP-20, walked up through MP-25, applied for the
  first time to a finished capstone. **Hard gate: this phase's Session 0 does not open
  until the premiere ledger shows zero `UNDECIDED` rows and the site has a live address.**
  Three predecessors were already one pre-registration too many; a fourth unexecuted one
  would be drift in the ledger's own terms (ADR-0003's consequence clause), and this gate
  is the mechanical refusal of it.
- **The executed horizon lanes are consumed into artifacts, never re-opened.** Whatever
  the ACDC pilot and the scaled-up R1 decided, this phase converts each verdict into its
  first-class deliverable: a Rung-6 section for paper v2 or the scheduled-negative trial
  table; a scaled-R1 result paragraph or the no-head negative from MP-23's verdict. The
  intake table (row → artifact → section) is written in Session 0, before any prose.
- **One new question per phase — the continuum law.** ADR-0006 opens with exactly one new
  research row, chosen at Session 0 from a pre-registered candidate set; each candidate
  carries a window, a kill-date and a "what would falsify this" column written before the
  choice (Gelman & Loken applied at the source, as always). The unchosen candidates close
  with one dated reason each, in the same sitting. Three open questions is drift by
  another name.
- **The shelf is maintained as rows, never as mood.** The site's health, the Space's
  health, the essay's annex and the paper's v2 diff each become a dated row with a window
  and a heartbeat; maintenance stops being "keeping it alive" and becomes a ledger state.
- **Verdict-agnostic prose for the negatives first.** The scheduled negatives (no-head R1,
  no-grok P=113) are drafted in full before the phase reads its intake — the MP-23
  inheritance, now load-bearing: the negative is a contribution, printed with the same
  polish as the win.
- **The continuum is bounded by the clock, not by ambition.** The first new research
  question is scoped to this machine's CPU budget and one 14-day window; a question that
  needs a GPU or a month is a candidate that closes with a dated reason, and the record's
  next phase can reopen it as a NEW row.
- **The terminus is stamped at Step 0**: release = this roadmap's merge + 14 calendar
  days. On that date the phase ships everything the rows decided — the residue is a dated
  list, never a silence (inherited, still true).

## Where this phase starts (state review, verified against the repo 2026-08-10)

I checked the tree, the manifests, the ledger rows, the CI floor and the gate states
before writing a single claim here.

- **Tree state**: working tree clean on `dev`; MP-23 current with ADR-0003's seven rows
  all UNDECIDED; MP-24 (ADR-0004, five rows) and MP-25 (ADR-0005, eight rows)
  pre-registered; no session of any of the three has started. The intake chain
  MP-23 → MP-24 → MP-25 → this phase is unbroken and this roadmap is written
  verdict-agnostic: nothing here waits for data it cannot name, exactly as its three
  predecessors were.
- **The CI floor (the recorded baseline; no `src/` change has landed since)**: 185 tests
  green; ruff clean on `src/ tests/`; blocking mypy clean (`src/results.py`,
  `src/experiments/runner.py`); full-tree mypy at the tracked 171 ratchet (non-blocking,
  at most one module this phase); `make verify-claims` at its designed 2 problems —
  `results/exp2_grokking.json` and `results/exp5_sae_dashboard.json` have never existed,
  and those lanes decide at MP-23: they arrive here either as manifests to cite or as
  struck notes to print; markdownlint 0 on changed notes.
- **The science intake is the executed horizon verdicts.** ADR-0005 rows 7–8 carry the
  ACDC pilot and the scaled-up R1 into this phase LAUNCHED-with-verdict or
  CLOSED-with-reason; the standing gate debt — W&B, the clean-clone reproducible proof,
  the graduation proof, the `reproduce-multiseed` coverage for exp2/exp5 — is consumed as
  its own dated rows. None of it is re-negotiated here.
- **The public shelf exists as of MP-25 or this phase does not open.** The essay, the site
  and the Space carry the verdicts this phase writes into prose; the hard gate keeps the
  gate honest.
- **A verified gap this review adds to the record**: `exp2_grokking.py` exposes only
  `--save-model` (its `main()` parser), while the full stateful checkpoint/resume
  system — atomic `save_training_checkpoint`, RNG-state capture, `--resume`,
  `--checkpoint-every` — exists only in `exp1_induction_heads.py`. The P=113 lane's
  disconnect-recovery promise ("heartbeat: checkpoint-every-500 + resume") is therefore
  not mechanically real until that machinery is ported to exp2. The port decision belongs
  to MP-23's Session 0, not to this roadmap; the finding is recorded here regardless of
  which way it goes.

### Bottleneck analysis (ranked by what blocks what)

1. **MP-25's release report — everything consumes it.** The premiere ledger's stamps, the
   five URLs (or reasons), the executed horizon verdicts: this phase cannot open a single
   row without them. The treatment is the hard Session-0 gate and the intake table written
   before any planning prose — the discipline every phase since MP-21 inherited, applied
   to the first phase past the finish line.
2. **The first-new-question choice.** A research program that opens three lanes at once is
   a mood with dates; the treatment is the continuum law — one row opens, the rest close
   with reasons, and the choice itself is a Session-0 sitting, never a committee.
3. **The consumed-verdict dependency.** If the ACDC pilot closed with a scheduled
   negative, the Rung-6 artifact is the trial table, not a section; the negative path is
   drafted in full before Session 0 so that the closure is never a silence.
4. **The shelf's recurring cost.** The site, the Space and the claims gate are now
   permanent infrastructure — a build that rots on a Sunday is gone by Monday. The
   treatment is the maintenance row with its own window and heartbeat, bounded and dated,
   never the phase's critical path.
5. **The strangers remain a pipeline.** Round-2 feedback from the launched thread, the
   live site and the Space's visitors is data with a kill-date on intake; feedback
   absorbed silently is feedback lost (inherited, now with an audience).
6. **The mypy ratchet (171)** — scheduled, non-blocking, at most one module in this
   phase; it must never be chased while a launch or a revision is pending.

<!-- MP26-SECTION-2 -->

## 1. Deep-dive study and research topics (bound to a session — no topic without a deliverable)

| Topic | Session | The deliverable that proves the reading |
|---|---|---|
| Conmy et al., *Towards Automated Circuit Discovery (ACDC)* (NeurIPS 2023) — re-read against the verdict my pilot actually produced | S2 | The Rung-6 artifact: the paper-v2 section, or the trial table that closes the lane with its reason |
| Zhang & Nanda, *Best Practices of Activation Patching* — the second re-read, now against the real-head matrix if the head exists | S4 | The R4 prose-revision memo: what I did differently from the authors' named failure modes, filed before the stranger sees it |
| Nanda et al., *Progress Measures for Grokking* — re-read against my own Fourier counts if grokked · else Power et al., re-read as a compression study | S2 | The grokking section's final prose, or the one-page honest-negative compression addendum |
| Olsson et al., *In-context Learning and Induction Heads* — the scaling section, as the consumed scaled-R1 verdict's warrant | S5 | The scaled-R1 result paragraph or its no-head negative, written from my log, not from the paper's curves |
| Bricken et al., *Towards Monosemanticity* — the SAE continuation line, if R5's delta from MP-23/25 warrants it | S6 | The SAE verdict memo: retry, or the dated reason the lane stays closed |
| The stranger's round-2 notes (thread replies, site feedback, Space visitors) — studied as data, not as feedback | S4 | The feedback-to-fixes matrix: friction point → cause → dated fix → re-check row |
| Quartz v4 documentation + the GitHub Pages Actions workflow — the pipeline that now runs in production | S1 | The site-maintenance memo: one page from clone to filter to build to deploy, with the claims gate inserted |
| One primary source chosen by the opened ADR-0006 row (e.g., Elhage et al. Toy Models ch. 2–3 if a superposition question opens) | S5 | The new-question pre-registration: site, metric, negative control, kill-date — written before the first pass |

Each reading produces a deliverable — the vault's golden rule, extended to the phase where
the shelf exists.

## 2. Documentation requirements

- **The continuum ledger (ADR-0006)** — *new*: one row per post-premiere decision — the
  consumed horizon artifacts, the first new research question, the maintenance rows (site
  health, Space health, essay annex v2, paper v2 diff), the stranger round 2 and the
  standing gate debt — each with a window, a heartbeat where a run exists, and a
  kill-date, under the ADR-0001 rules. Rows end LAUNCHED-with-artifact or
  CLOSED-with-one-reason; zero UNDECIDED at Session 8.
- **The essay annex v2** — `portfolio/essay-annex-2.md`: what the premiere's verdicts
  changed, distilled from the consumed rows, every number manifest-tagged; the essay
  itself is never rewritten, only amended (the MP-23/24/25 inheritance).
- **The paper v2 diff** — sections opened only for manifests that exist on disk: the
  Rung-6 section if the pilot recovered its subgraph, the scaled-R1 paragraph if the head
  existed, the struck notes otherwise; `make paper` still compiles in the CI mirror, and
  the paper still rots loudly or not at all.
- **RESULTS v-release-2** — the trust order updated with the premiere-verdict rows and
  the first new-question manifest, the public URLs beside the rows that shipped.
- **The site-maintenance memo + health transcript** — the recurring build's walk: one
  page that makes a stranger's clone → build → deploy boring twice over.
- **New notes (Obsidian, atomic, each linked ≥ 2 others)**: the ACDC-after-the-pilot note
  (or its negative), the stranger-round-2-as-data note, the site-maintenance note, the
  post-premiere-program note, one note per opened study.
- **Skill tree** — flips only with a dated manifest or a stamped ledger row: mini-paper
  [~] → [x] with the paper v2 PDF; ACDC [~] → [x] or closed with its reason; the
  continuum row ends LAUNCHED or CLOSED with dates.
- **Progress log** — one dated entry per session; raw pass/fail before interpretation; a
  launch row is logged even if it fails — the failure is the note (the MP-12 lesson,
  applied to the shelf).

## 3. Practical exercises and hands-on challenges

1. **The consumption truthing (S0)**: read MP-25's release row by row — the premiere
   ledger, the five URLs (or reasons), the horizon verdicts; the one-page scope: what the
   record can now claim publicly, in trust order. Exit: zero unsupported claims in the
   scope sheet.
2. **The shelf health walk (S1)**: every public number clicked back to its manifest — the
   re-derivation game played against the live site, `verify-claims` open beside the
   browser; dead links, unbuilt pages, orphan pages, missing a11y basics, walked as a
   complete transcript.
3. **The consumed-verdict sprint (S2)**: the ACDC pilot's verdict becomes the Rung-6
   artifact in one sitting — a section written from my log, or the trial table that closes
   the lane; the study slot's deliverable lands with it.
4. **The three-hostile-reviewers pass (S3)**: the essay annex v2 read as an
   experimentalist, a theorist and a skeptic; five attack sentences fixed per page, then
   the negative-first prose checked to carry the same polish as the wins.
5. **The feedback-to-fixes loop (S4)**: the stranger's round-2 friction points → dated
   fixes → the re-check row stamped in the same sitting; feedback absorbed silently is
   feedback lost.
6. **The first-question pre-registration (S5)**: the opened ADR-0006 row's protocol —
   site, metric, negative control, kill-date, scheduled negative — written before the
   first forward pass; the run supervised with a heartbeat.
7. **The re-derivation game v2 (S6)**: every headline number on the live site → command →
   manifest → figure, walked as a checklist; the claims gate is the immune system, and
   the game proves it daily.
8. **The maintenance rehearsal (S7)**: bare clone → `uv sync` → full suite →
   `verify-claims` → `make paper` → site build → live deploy, one transcript, one
   sitting — the premiere's drill, now a recurring habit.
9. **The one-new-question analysis (S6)**: the opened row's verdict written from its
   manifest; the falsification column answered line by line, the scheduled negative
   printed as a contribution if it came.
10. **Habit — the clock check (every session)**: the ledger's undated rows, the open PR's
    CI status line, the site's build status — all three before any new prose.

## 4. Strategic tips and architectural best practices

- **The shelf is a job now.** A published record has recurring rows — site health, Space
  health, claims gate on every merge, essay annex per release; maintenance is a dated
  ledger state, never a mood.
- **One new number per phase.** The record compounds only when each phase ships one
  genuinely new manifest; the continuum law makes "three open questions" an illegal final
  state.
- **The negative is the contribution** (inherited, now the record's public signature): the
  scheduled negatives are drafted first, printed with the same polish as the wins — the
  page that says "not reproduced" is a feature, not a gap.
- **Pre-registration first, always** (inherited — Gelman & Loken, via ADR-0003): the
  opened question's falsification column exists before the first pass; the chosen row is
  the only one that opens.
- **The strangers are a pipeline, not an event** (inherited, now with an audience):
  review rows, revision rows, re-check rows, kill-dates on both ends; round-2 feedback is
  data with a date.
- **Verdict-agnostic writing** (inherited): the roadmap is written before the results
  exist; MP-23/24/25's data fills cells, never redraws the table.
- **Toolchains are Step-0 decisions** (inherited): Quartz, MiKTeX, Gradio — pinned and
  smoke-tested in Session 0, never discovered at a release; the `make`-missing incident
  remains the permanent precedent.
- **Micro-scale discipline.** The record's power is the honest micro-scale answer; a
  question that needs a GPU or a month is a candidate that closes with a dated reason and
  reopens later as a NEW row — it is never absorbed as a mood.
- **The claims gate is the immune system of the public record.** A page that cannot
  re-derive its numbers fails loudly in the build; the site inherits the paper's law, and
  the walk game keeps the law alive.
- **Session clocks beat mood clocks** (inherited, still true): every step has a wall clock
  and an exit gate.

<!-- MP26-SECTION-3 -->

## 5. Step-by-step execution roadmap

```
WEEK 1

SESSION 0 — THE PRE-FLIGHT (~30-60 min)
  Hard gate: MP-25's release report read row by row — the premiere
  ledger stamped, the site live, the horizon verdicts filed. CI green
  locally AND on GitHub (the tracked 185, ruff, blocking mypy,
  markdownlint, `make paper` in the mirror). ADR-0006 opened with its
  rows and windows; the intake table (row → artifact → section)
  written; the candidate set listed with one row chosen and the rest
  closed with dates; the Quartz toolchain re-verified against the live
  pipeline; this roadmap wired into home; pushed to dev; a green
  GitHub floor.
  Exit: the terminus is declared (release = this merge + 14 calendar
  days); the maintenance rehearsal is scheduled.

SESSION 1 — THE SHELF HEALTH BASELINE (~2-3 h)
  The site walk as a hostile webmaster: every public number clicked
  back to its manifest, dead links and orphans filed as dated fixes;
  the site-maintenance memo lands with the Quartz reading; the
  standing gate debt rows are stamped (W&B, clean-clone proof,
  graduation proof — each with a date or one reason).
  Exit: the maintenance row is LAUNCHED; the shelf's baseline is
  walked twice.

SESSION 2 — THE CONSUMED-VERDICTS SPRINT (~3 h)
  The horizon lanes consumed as decided: the ACDC verdict becomes the
  Rung-6 section or the trial table; the grokking prose is written
  from MY log per the raw verdict (grokked or not, the study slot's
  deliverable lands with it).
  Exit: the consumed rows are each LAUNCHED-with-artifact or
  CLOSED-with-one-reason.

SESSION 3 — THE NEGATIVE-FIRST PROSE + THE ANNEX DRAFT (~2-3 h)
  The scheduled negatives polished to the same standard as the wins;
  the essay annex v2 drafted from the consumed rows with every number
  manifest-tagged; the three-hostile-reviewers pass over both.
  Exit: the annex draft cites only disk; the hostile pass fixed five
  attack sentences per page.

WEEK 2

SESSION 4 — THE STRANGER ROUND 2 + THE PATCHING MEMO (~2-3 h)
  The round-2 feedback (thread, site, Space) read as data; the
  feedback-to-fixes matrix stamped; the Zhang & Nanda re-read's memo
  filed (if a real head exists).
  Exit: the stranger row is dated; feedback absorbed is fixed with
  dates.

SESSION 5 — THE FIRST NEW QUESTION (~3 h)
  The opened ADR-0006 row pre-registered in full (site, metric,
  negative control, kill-date) and launched on this machine with a
  heartbeat; the scaled-R1 verdict's paragraph written (or its
  no-head negative); the study source's deliverable lands with it.
  Exit: the continuum row is LAUNCHED-with-protocol; the run's
  heartbeat is live.

SESSION 6 — THE ANALYSIS + THE RE-DERIVATION (~3 h)
  The opened question's verdict written from its manifest; the SAE
  verdict memo filed per R5's delta; the re-derivation game v2 walked
  end to end against the live site; RESULTS v-release-2 and the skill
  tree flips stamped.
  Exit: every headline number re-derivable from a walked command.

SESSION 7 — THE REHEARSAL (~3 h)
  The maintenance rehearsal from a bare clone with the live deploy —
  the premiere's drill as a recurring habit; the paper v2 compiles
  clean in the mirror; mypy drift at most one module if the budget
  allows.
  Exit: the shelf's drill has been walked twice.

SESSION 8 — THE RELEASE (the fixed terminus date)
  Merge on green; the essay annex v2 lands with its date; the
  continuum rows LAUNCHED or CLOSED under dates; home wired; this
  roadmap archived with its deviations — every deviation a dated
  ledger note.
  Exit: tree clean, `dev == main`, the ledger is the phase's
  after-the-fact truth, and the program has its first post-capstone
  question answered or closed.
```

## 6. Gate criteria

1. Session 0: MP-25's release consumed row by row — the premiere ledger stamped, the site
   live; the CI floor green locally AND on GitHub; the intake table written; the
   continuum row chosen and the rest closed with dates.
2. Session 1: the maintenance row is LAUNCHED; the shelf baseline walked twice; the
   gate-debt rows carry dates or one reason each.
3. Sessions 2–3: the consumed verdicts each end LAUNCHED-with-artifact or
   CLOSED-with-one-reason; the annex cites only manifests on disk; the hostile pass fixed
   ≥ 5 attack sentences per page.
4. Session 4: the stranger round-2 row is dated; the feedback-to-fixes matrix is stamped.
5. Session 5: the continuum row is LAUNCHED-with-protocol — pre-registration on disk
   before the first pass — with its heartbeat live.
6. Session 6: the opened question's verdict is written from its manifest; every public
   number re-derivable from a walked command.
7. Session 7: the maintenance rehearsal walked twice on a branch; `make paper` compiles in
   the mirror.
8. Session 8: the merge is green; every ledger row is LAUNCHED-with-artifact or
   CLOSED-with-one-reason; the progress log closes the loop.
9. The record-sanity gate: nothing on any public surface exceeds the record — every
   sentence survives `verify-claims` or is struck with a date (inherited, now enforced by
   the site's build).

## 7. Showcase note (for the portfolio reader)

The journey's public shape is now a practice: I built a transformer from nothing, asked it
the smallest honest questions, caught real bugs in my own causal claims three times and
published the catches, answered the two flagship questions under pre-registered clocks,
wrote the answers down, gave the record an address — and then kept going, in the same
register: the first post-capstone phase consumed the premiere's verdicts into artifacts,
closed the standing debt with dates, and opened exactly one new question under its own
pre-registration. A stranger can now watch the discipline itself compound: the site's
numbers re-derive from disk, the negatives are printed as contributions, the ledger shows
zero undated rows at release, and the next question — one per phase — is chosen, never
drifted into.

> "The phase where the shelf began to write: the first post-premiere question was
> pre-registered, launched, answered or closed with a reason — and the notebook that
> became a shelf became a workshop."

## Links

- [[00_meta/24_micro-phase-25-the-premiere]] — the roadmap this phase consumes; its
  release report and ADR-0005 stamps are Session 0's starting artifact.
- [[docs/adr/0005-premiere-ledger]] — the intake: the eight rows this phase's consumption
  table maps to artifacts.
- [[docs/adr/0006-continuum-ledger]] — this phase's new ledger: the continuum row, the
  maintenance rows and the gate-debt closures.
- [[docs/adr/0003-research-return-ledger]] · [[docs/adr/0004-horizon-ledger]] — the
  machines whose verdicts arrive here consumed, never re-negotiated.
- [[portfolio/RESULTS]] · [[portfolio/README]] — the results sheet v2 this phase
  re-writes; the shelf the URLs land on.
- [[portfolio/paper/main]] — the paper whose v2 diff opens sections only for manifests on
  disk.
- [[00_meta/03-progress-log]] — the dated record of every session, including the rows
  that closed and the launches that failed (the failure is the note).