---
tags: [type/moc, phase/6, phase/7, research/experiment, state/review]
created: 2026-08-12
---

# Micro-Phase 31 — The Premiere: the record gets an address

Written as a personal learning log and a public record, like every roadmap before it.

MP-29 decides the science, MP-30 consumes the decision into the finished
artifact — the paper in prose and PDF, RESULTS v-final, the horizon decided as
dated rows, the record's address earned on a clean clone. This phase is where
the written answer must survive a stranger's eyes: nothing in this repository
is publicly addressable yet. MP-22 pre-registered the public arc (essay,
thread, site, Space, walkthrough) and its ledger sits entirely UNDECIDED — the
record has manifests, verified results, a paper, a talk script and a
clean-clone transcript, but no URL. This phase is the premiere: the release of
the finished capstone onto surfaces a stranger can open, the revision cycle
that the first reader's notes force, and the execution — or honest closure —
of the horizon lanes MP-30 decided. Whatever MP-30's release says, this phase
consumes it row by row; nothing here re-plans a single verdict.

The record's deepest pattern is the one this phase completes: public artifacts
were pre-registered in prose but never launched, exactly as the experimental
rows were. The treatment is the same mechanical one the science already
absorbed — a row with a launch clock, a URL as its receipt, and a same-sitting
rule that makes "planning it" an illegal final state. The premiere is where
the notebook becomes a shelf.

## Where this phase starts (state review, verified against the repo 2026-08-12)

The intake is MP-30's release report; below is what the record stands at the
moment of pre-registration, so this roadmap's claims are auditable from day
one. MP-30's Session 8 updates every line; nothing here re-plans a single row
of it.

- **Tree state**: `dev` clean at the MP-30 pre-registration merge (PR #62
  squashed, dev reconciled with main); nothing of MP-29 or MP-30 has executed
  yet — both stand pre-registered, and their residue rows (the R1 verdict, the
  paper prose, the stranger review, the PDF) are this phase's intake, per the
  record's law that a session is not over while a row it owns is undated.
- **The ledgers**: ADR-0003 rows 2–7 UNDECIDED (MP-29's rows); ADR-0004's five
  horizon rows UNDECIDED (MP-30 decides them in its Session 4); **ADR-0005's
  eight premiere rows UNDECIDED — this phase's rows**; ADR-0006's eight
  continuum rows and its candidate set frozen by law — not this phase's rows.
  ADR-0002's five public-arc rows never received a date; they reopen here as
  NEW rows under this phase's own dates, windows and kill-dates.
- **The CI floor**: `make verify-claims` at its current 3 problems (dirty-tree
  exp2 manifest; Rung 2 section tag; Rung 5 section tag) — MP-29 drives it to
  0, MP-30's release requires 0, and 0 is this phase's precondition, not its
  hope. The tracked 185+ tests, ruff, blocking mypy and markdownlint baselines
  were all green at MP-28's release and nothing has changed under them since.
- **The toolchains, verified today**: no LaTeX toolchain on this machine
  (`pdflatex`/`latexmk`/`tectonic` all absent — `make paper` is graceful, not
  green); no Pages deploy workflow in `.github/workflows/` (only
  conventional-commits, markdown-lint, python-ci); no `publish:` frontmatter
  policy anywhere in the vault; `portfolio/projects/` empty; the Space engine
  is `src/experiments/exp3_superposition.py` behind `results/exp3_*.json`
  (clean manifests exist for exp3/exp4; exp1 is sub-standard and exp5's
  manifest is absent until MP-29/MP-30's lanes produce them).
- **The showcase corpus**: 12 provenance-guarded figures in
  `portfolio/figures/`; the paper scaffold (`main.tex` + `references.bib`)
  that MP-30 finishes; `portfolio/RESULTS.md`, `README.md` and `model-card.md`
  that MP-30 brings to v-final; `gh` CLI v2.97.0 against
  `github.com/AlessioBrillo/from-gradient-to-transformer`.

## Design decisions

- **Session 0 is the hard gate: MP-30's release report, consumed row by row.**
  The paper's PDF exists on disk, ADR-0004's rows are stamped as decided (not
  re-negotiated), `verify-claims` reads 0, and the intake table is committed
  before a single public row opens. A fourth unexecuted pre-registration
  would be drift in the ledger's own terms; this gate is the mechanical
  refusal of it.
- **The public arc reopens as NEW rows under this phase's dates** (ADR-0002 →
  ADR-0005 rows 1–5): essay, thread, site, Space, walkthrough. A surface opens
  only if the artifact behind it exists on disk: the essay needs the paper,
  the thread needs the essay, the site needs the paper's figures, the Space
  needs the verified Rung 3 engine. The URL is the receipt: *launch = artifact
  merged + address stamped, in the same sitting.*
- **The web inherits the manifest law.** Every number that reaches a public
  surface re-derives from `results/*.json` via `make verify-claims`; the site
  build runs the claims gate in the local CI mirror, so a public page can no
  more cite an unreproducible number than the paper can. The paper rots
  loudly or not at all; the site does the same.
- **The revision cycle is a first-class row** (ADR-0005 row 6): the stranger's
  three friction points → three dated fixes → the re-read row stamped in the
  same sitting as the fixes. Feedback absorbed silently is feedback lost; if
  the re-read does not happen within the window, the row closes with one
  reason and the recorded self-review substitute — never a silent skip.
- **The horizon lanes get their execution, never their re-negotiation**
  (ADR-0005 rows 7–8): the ACDC pilot runs its pre-registered protocol —
  sites, metric, negative control, kill-date — or closes with its trial
  table; scaled-up R1 opens only on a head that MP-29's verdict allowed, with
  budget, seeds and threshold pre-registered, else the scheduled no-head
  negative is the result. Both were written by MP-30's Session 4, exactly as
  ADR-0004 decided them.
- **The continuum stays frozen** (ADR-0006): zero new research questions open
  this phase. MP-31 is the premiere; the continuation is the phase after it,
  seeded only from what actually happened here.
- **Toolchains are pinned in Session 0, never discovered at Session 7.**
  Quartz v4 + GitHub Pages, the LaTeX toolchain MP-30 decided, the Gradio CPU
  Space: each is decided and smoke-tested in Session 0 — the MiKTeX and
  `make` lessons, applied before the premiere.
- **The terminus is stamped at Step 0**: release = this roadmap's merge + 14
  calendar days. On that date the phase ships everything the rows decided —
  the residue is a dated list, never a silence (inherited, still true).

## Session 0 — the truthing pass + the toolchains (2026-08-12, ~1 h) — next

- MP-30's release consumed row by row into an intake table: the paper's PDF
  on disk, ADR-0004's rows as stamped (dates, verdicts, manifest tags),
  `make verify-claims` at its actual count (0 if MP-30 landed its line;
  otherwise the residue is listed with the row that owns it — intake, not
  re-planning).
- The three toolchains decided and proven: `make paper` on the finished
  scaffold produces the PDF or names the blocker with the install line;
  Quartz v4 pinned and a smoke build pushed to a preview branch; the Gradio
  engine health check run on CPU under a memory ceiling. Each pinned the day
  it is first used, never the day it is needed.
- The `publish:` frontmatter policy written (true/false per note, the vault
  subset defined) and the claims gate inserted into the site build plan —
  the web inherits the paper's law from the first page, not the last.
- The CI floor re-verified locally: tracked tests green, ruff clean, blocking
  mypy clean, markdownlint 0 on changed notes.
- **Exit**: the intake table signed; `make paper` green or dated; the Quartz
  preview URL exists; ADR-0005 opened with its rows and windows; the terminus
  declared.

## Session 1 — the premiere drill (~3 h)

- The clean-clone-to-live-URL drill on a branch: bare checkout → `uv sync` →
  full suite → `verify-claims` → `make paper` → Quartz build → Pages deploy —
  one sitting, every step logged with its output line. The first rehearsal
  makes the launch boring (the MP-17/20 doctrine, upgraded to the web).
- The walkthrough's command line is drafted from this drill — any step that
  needs a hidden hand is a claim that fails its audit.
- **Exit**: the drill transcript exists; the site branch builds green from
  the vault filter; ADR-0005 row 5's transcript is pre-seeded.

## Session 2 — the essay (~3 h)

- `portfolio/essay.md`: the paper distilled for a lost reader — the NO-GROK /
  dense-solution story as the honest centerpiece, every number
  manifest-tagged, each claim's "what would falsify this" column filled at
  writing time (Gelman & Loken, applied to stranger-facing prose).
- The essay is never rewritten afterwards, only amended via dated annexes
  (the MP-23/24 inheritance).
- **Exit**: the essay draft exists; the reverse claims audit (prose →
  manifest → command) at zero.

## Session 3 — the revision cycle (~2–3 h)

- The stranger's three friction points (or the recorded self-review
  substitute, if the window closed silent) → three dated fixes in the paper
  and the essay → the re-read row stamped in the same sitting.
- **Exit**: ADR-0005 row 6 dated; the essay cites only disk.

## Session 4 — the talk + the Space (~3 h)

- The 10-minute talk: draft one is MP-30's; draft two is written from memory
  — the from-memory draft is the real one, timed once under 11 minutes, no
  code on the slide.
- The CPU Superposition Explorer rebuilt behind the verified Rung 3 engine
  (`src/experiments/exp3_superposition.py`, the exp3 manifest): boots on CPU,
  engine version pinned, its own health check run — the demo cannot outrun
  the engine the record verified.
- **Exit**: both talk drafts exist, timed; the Space runs on CPU; the SAE
  verdict memo filed (retry or the dated reason it stays closed).

## Session 5 — the scientific execution (~3 h)

- The ACDC pilot runs its pre-registered protocol (edge set, metric, negative
  control, kill-date) — subgraph recovered, or the scheduled negative as the
  first-class result; EAP attribution compared against the intervention
  ground truth if the head existed.
- Scaled-up R1: opened with its pre-registered budget and threshold, or
  closed with the no-head reason MP-29's verdict gave it.
- The site walk: every public number clicked back to its manifest with
  `verify-claims` open beside the browser — the re-derivation game for the
  web.
- **Exit**: ADR-0005 rows 7–8 dated either way; the site walk transcript at
  zero.

## Session 6 — the thread + the rehearsal (~3 h)

- The six-post arc drafted three times — once from the essay, once from
  memory, once after a 24-hour pause; the second and third drafts are the
  real ones; each post cites its manifest; scheduled and launched on dates.
- The full premiere rehearsal from a bare clone with the live deploy — the
  second walk of the command line, on the branch that will ship.
- **Exit**: all five public rows exist on a branch with artifacts and dates;
  the walkthrough transcript re-executed green.

## Session 7 — the hostile-webmaster pass (~3 h)

- The whole portfolio + site walked as a transcript: broken links, unbuilt
  pages, dead figures, missing accessibility basics, orphan pages; the
  claims gate re-run on the clean clone — at zero unfixed issues.
- The same-sitting launches rehearsed once more: each LAUNCHED row's artifact
  merged and URL stamped in the sitting that decides it.
- **Exit**: the hostile-webmaster transcript; zero undated premiere rows; the
  landing plan walked twice on a branch.

## Session 8 — the release (the fixed terminus date)

- ADR-0005 at zero UNDECIDED rows — each LAUNCHED-with-URL or
  CLOSED-with-one-reason; ADR-0006 untouched — this phase opened zero new
  research questions; the merge green locally and on GitHub; home wired;
  this roadmap archived with its deviations — every deviation a dated ledger
  note.
- **Exit**: the merge; `dev == main`; the ledger is the phase's after-the-fact
  truth; the repository has an address.

## Gate criteria (pre-registered, from the sessions above)

1. S0: intake table signed; `make paper` green or dated; Quartz preview URL
   exists; the `publish:` policy committed.
2. S1: the premiere drill transcript exists; the site builds green from the
   vault filter.
3. S2: the essay's reverse claims audit at zero; the essay cites only disk.
4. S3: ADR-0005 row 6 dated; the fixes re-read in the same sitting.
5. S4: the talk's draft two under 11 minutes; the Space health check green.
6. S5: ADR-0005 rows 7–8 stamped; the site walk at zero.
7. S6: the thread scheduled; the rehearsal walked twice on a branch.
8. S7: the hostile-webmaster pass at zero; S8: zero UNDECIDED rows; the merge
   green; `dev == main`; the record has an address.

## The one measured line (status)

ADR-0005 at **zero UNDECIDED rows** on release day, with every public number
re-derivable — the site build runs `make verify-claims` in the CI mirror, and
the hostile-webmaster pass is the same audit the paper always had, pointed at
the web. The second half of the line: `dev == main` and the record's first
live URL, stamped in the same sitting as the merge.

## Deep-dive study plan

1. **Quartz v4 + GitHub Pages Actions + the vault's `publish:` policy** — the
   vault-to-site pipeline as a build system: what the filter keeps, what the
   claims gate guards, and how a public number gets re-derived before it is
   rendered. The site-build book is a deliverable, not a reading.
2. **Writing for strangers** — the paper-to-essay distillation: what survives
   a lost reader's first pass, the honest-negative canon (protocol, window,
   machine, criterion — the NO-GROK sentence MP-29 built, now public), and
   why the negative is the signature, not the gap.
3. **The talk that survives without code, public edition** — the MP-30
   script studied as a stranger hears it: hook, claim, evidence, limit, next;
   the from-memory draft is the real one, and the gap between drafts is the
   argument's weak joint.
4. **ACDC and the EAP lineage, read ahead of execution** — Conmy et al.
   2023, Hanna et al. 2024: edge sets, attribution metrics, negative
   controls, the failure modes EAP names; the pilot's protocol was
   pre-registered by MP-30, this phase executes it against the real circuit
   or prints the trial table.
5. **Induction-head scaling as design** — Olsson et al. 2022's scaling
   section: layers, context, head count as the knobs a scaled-up R1 would
   turn; the no-head negative from MP-29's verdict is the likely intake, and
   the reading is what makes the closure a decision, not a mood.
6. **Gradio CPU packaging** — Spaces' hardware constraints as a design
   constraint: memory ceilings, model load, health checks; a demo that dies
   on a visitor is a row that fails its audit.
7. **The stranger's chair, applied to the web** — the craft of self-review as
   first-reader, now multiplied by the hostile webmaster: links rot, pages
   break, numbers drift — the transcript is the defense, and the rehearsal
   until boring is the method.

## Documentation contract

- This roadmap, pre-registered (the file you are reading).
- ADR-0005's eight rows stamped with dates and URLs or one-line reasons —
  LAUNCHED or CLOSED, nothing "awaiting"; ADR-0004's rows consumed as
  decided; ADR-0006 untouched — zero new research questions opened.
- `portfolio/essay.md` — the public essay, manifest-tagged, never rewritten
  after release, only amended via dated annexes.
- The site — the Quartz vault subset, `publish:` policy, the claims gate in
  the build; the thread — six posts drafted thrice, scheduled, launched.
- The Space — the CPU Superposition Explorer with its engine health check.
- The walkthrough transcript — clone → sync → suite → verify-claims → paper →
  site-live, executed twice, logged.
- `portfolio/RESULTS.md` at v-release: the trust order with the public URLs
  beside the rows that shipped; `portfolio/README.md` reconciled to the
  ledger.
- `00_meta/03_progress-log`: one dated entry per session; this roadmap wired
  into home on release; the premiere ledger's rows cited by the skill tree's
  publication flips.

## Practical exercises and challenges

1. **Ex-A · The truthing pass (S0)**: MP-30's release read row by row — the
   PDF, the horizon stamps, the stranger's notes — into a one-page scope:
   what the record can now claim publicly, in trust order. Zero unsupported
   claims in the scope sheet.
2. **Ex-B · Three registers, one negative (S2)**: the NO-GROK/dense story as
   (1) the paper's paragraph, (2) the essay's sentence, (3) the 30-second
   spoken claim. Same facts, three audiences; the delta between them is
   where my understanding leaks.
3. **Ex-C · The premiere drill (S1)**: bare clone → suite → claims → paper →
   site-live in one sitting; the launch becomes boring before it is real.
4. **Ex-D · The essay's reverse audit (S2)**: every essay number traced to
   its manifest and its command; the rest struck with a reason — the
   hostile-webmaster test of my own prose.
5. **Ex-E · The talk from memory (S4)**: draft two written with the
   repository closed, timed against a stopwatch.
6. **Ex-F · The site walk (S5)**: `verify-claims` open beside the browser;
   every public number clicked back to disk.
7. **Ex-G · The ACDC hand-roll (S5, if the pilot opened)**: implement the
   algorithm against the real R1 circuit — discovered subgraph vs my
   hand-found circuit; the scheduled negative is a result either way.
8. **Ex-H · The three-draft thread (S6)**: once from the essay, once from
   memory, once after 24 hours — the second and third drafts are the real
   ones.
9. **Ex-I · The hostile-webmaster pass (S7)**: links, assets, a11y, orphans,
   dead figures — walked as a complete transcript at zero.
10. **Habit · The clock check (every session)**: the ledger's undated rows,
    the open PR's CI status line, the site's build status — all three before
    any new prose.

## Strategic tips and architectural best practices

- **The URL is the proof.** A public surface that is not a LAUNCHED row with
  a date and an address does not exist. Plans are documents; the ledger row
  is the artifact a stranger opens.
- **Manifest-first on the web, too.** The site inherits the paper's law — a
  page cannot cite a number the claims gate cannot re-derive, and the build
  fails loudly, never silently.
- **Toolchains are Step-0 decisions.** Quartz, TeX, Gradio — each pinned and
  smoke-tested before the phase's first launch, never discovered at the
  release (the `make`-missing incident is the permanent precedent).
- **One sitting, one launch.** An artifact merged and a URL stamped in the
  same sitting is a launch; anything else is a plan with a date, which is a
  promise by another name.
- **The stranger's eyes are the cheapest validation the record can buy** —
  and they are a pipeline: review rows, revision rows, re-read rows, each
  with kill-dates; feedback absorbed silently is feedback lost.
- **The negative is the contribution, now in public.** The page that says
  "not reproduced under this protocol" is a feature, not a gap — it is the
  signature that separates this shelf from a notebook.
- **Small surface, honest depth.** Five pages whose every number re-derives
  beat thirty pages of prose whose numbers don't.
- **Rehearse the release until it is boring.** Two clean-clone-to-live drills
  (S1 and S7) mean release day is a formality, not an adventure.
- **Architecture laws, unchanged.** `dev` only, GPG-signed, Conventional
  Commits with `(meta)`, `(portfolio)`, `(ci)` scopes; CI green before any
  merge; the floor re-verified locally before every push; zero UNDECIDED
  rows at Session 8; release = merge + 14 calendar days.
- **The showcase 30-second story**: *the pipeline ran perfectly and produced
  a genuine negative; I characterized the algorithm it found instead; then I
  put the whole record where a stranger could check every number — the
  paper, the site, the demo, and one command line that rebuilds all of it.*
  Every artifact this phase launches is written to that standard.

## Links

- [[00_meta/29_micro-phase-30-the-consumption]] — the roadmap this phase
  consumes; its release report and ADR-0004 stamps are Session 0's starting
  artifact.
- [[00_meta/24_micro-phase-25-the-premiere]] — the premiere's original
  pre-registration, re-clocked to MP-30's release; its design decisions are
  inherited as written.
- [[docs/adr/0005-premiere-ledger]] — this phase's ledger: the eight rows it
  stamps LAUNCHED-with-URL or CLOSED-with-one-reason.
- [[docs/adr/0004-horizon-ledger]] · [[docs/adr/0002-public-arc-ledger]] —
  the intake and the machine whose rows reopen here as NEW rows under this
  phase's dates.
- [[docs/adr/0006-continuum-ledger]] — frozen by design; the continuation is
  the phase after this one.
- [[portfolio/RESULTS]] · [[portfolio/README]] · [[portfolio/model-card]] ·
  [[portfolio/paper/main]] — the artifacts this phase hosts and publishes.
- [[06_production_ai/notes/results-manifests-and-provenance]] — the manifest
  machinery every public number cites.
- [[07_capstone/research-plan]] — the research plan the paper and the essay
  distill.
- [[00_meta/03-progress-log]] — the dated journal entries per session,
  including the rows that closed and the launches that failed (the MP-12
  lesson, applied to URLs).
