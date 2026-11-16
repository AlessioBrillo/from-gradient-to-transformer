---
tags: [type/moc, phase/6, phase/7, research/experiment, state/review]
created: 2026-08-10
---

# Micro-Phase 25 — The Premiere: the capstone ends, the record begins

Written as a personal learning log and a public record, like every roadmap before it.

Every phase since MP-18 enacted the same law: a promise can be re-planned forever, but a
dated row is answered. MP-23 answers the science, MP-24 writes the answers down in prose.
This phase is where the written answer must survive a stranger's eyes — because nothing in
this repository is publicly addressable yet. MP-22 pre-registered the public arc (essay,
thread, site, Space, walkthrough) and its ledger sits entirely UNDECIDED: the record has
manifests, verified results, a paper in prose and a talk script, but no URL. This phase is
the premiere: the release of the finished capstone onto surfaces a stranger can open,
followed by the first scientific continuation the horizon decides — a real ACDC pilot, a
scaled-up Rung 1, or a deliberate stop-and-publish. Whatever MP-24's release decided, this
phase consumes it row by row; nothing here re-plans a single verdict.

The record's deepest pattern is the one this phase completes: public artifacts were
pre-registered in prose but never launched, exactly as the experimental rows were. The
treatment is the same mechanical one the science already absorbed — a row with a launch
clock, a URL as its receipt, and a same-sitting rule that makes "planning it" an illegal
final state. The premiere is where the notebook becomes a shelf.

## Design decisions

- **The starting artifact is MP-24's release state, row by row.** Step 0 is a truthing pass
  over the paper's PDF on disk, RESULTS v-final, the model card, the talk script and the
  ADR-0004 horizon rows — the same intake discipline MP-24 applied to MP-23, applied to the
  finished capstone. **Hard gate: this phase's Session 0 does not open until the paper's
  PDF exists on disk.** A fourth unexecuted pre-registration would be drift in the ledger's
  own terms (ADR-0003's consequence clause), and this gate is the mechanical refusal of it.
- **The public arc reopens as NEW rows, only where a manifest exists.** ADR-0002's five
  surfaces reopen as this phase's rows under its own dates, windows and kill-dates ("rows
  reopen from ADR-0001/0002 only under new dates and new windows, this phase's own" — the
  inherited rule, applied to publication). A surface opens only if the artifact behind it
  exists on disk: the essay needs the paper, the thread needs the essay, the site needs the
  paper's figures, the Space needs the superposition engine. The URL is the receipt:
  *launch = artifact merged + address stamped, in the same sitting.*
- **The web inherits the manifest law.** Every number that reaches a public surface
  re-derives from `results/*.json` via `make verify-claims`; the site build runs the claims
  gate in the local CI mirror, so a public page can no more cite an unreproducible number
  than the paper can. The paper rots loudly or not at all (MP-24's design); the site does
  the same.
- **The horizon rows consume ADR-0004 exactly as MP-24 decided them.** The real-ACDC pilot,
  the scaled-up R1 and the 10-minute talk enter this phase LAUNCHED-with-verdict or
  CLOSED-with-reason from MP-24 and get their *execution* here, never their re-negotiation.
- **The stranger is a pipeline, not an event.** MP-24's stranger review produces three
  dated friction points; this phase carries the revision cycle as a first-class row — the
  fixes, the re-read, and the lesson written into the essay. If the reviewed paper is not
  re-read, the row closes with one reason; the feedback is never absorbed silently.
- **Toolchains are pinned in Step 0, never discovered at Session 7.** Quartz v4 + GitHub
  Pages, the LaTeX toolchain from MP-24, the Gradio CPU Space: each is decided and
  smoke-tested in Session 0 — the MiKTeX and `make` lessons (MP-21/24), applied before the
  premiere.
- **The terminus is stamped at Step 0**: release = this roadmap's merge + 14 calendar days.
  On that date the phase ships everything the rows decided — the residue is a dated list,
  never a silence (inherited, still true).

## Where this phase starts (state review, verified against the repo 2026-08-10)

I checked the tree, the manifests, the ledger rows and the gate states before writing a
single claim here.

- **Tree state**: working tree clean on `dev`; MP-23 current with ADR-0003's seven rows
  UNDECIDED; MP-24 pre-registered with ADR-0004's five rows UNDECIDED; no sessions of
  either have started. MP-23's release report feeds MP-24; MP-24's release report feeds
  this phase — the intake chain is unbroken.
- **The CI floor (the recorded baseline; no `src/` change has landed since)**: 185 tests
  green; ruff clean on `src/ tests/`; blocking mypy clean (`src/results.py`,
  `src/experiments/runner.py`); full-tree mypy at the tracked 171 ratchet (non-blocking, at
  most one module this phase); `make verify-claims` at its designed 2 problems —
  `results/exp2_grokking.json` and `results/exp5_sae_dashboard.json` have never existed;
  markdownlint 0 on changed notes.
- **The public arc is pre-registered, not executed**: ADR-0002's five rows are all
  UNDECIDED; there is no essay, no thread, no site, no Space, no walkthrough anywhere on
  disk. `portfolio/` holds RESULTS.md, the model card and the paper scaffold;
  `portfolio/projects/` is an empty `.gitkeep`. This is not a defect to fix and not a
  failure to confess — it is the backlog this phase exists to clear, and the ledger already
  has the machinery for it: closed-then-reopened is a NEW row.
- **The paper (MP-24's flagship output) is a scaffold today**: `main.tex` carries its
  section skeleton and the `% TODO` gates, including the standing rule that the Grokking
  section opens only when `results/exp2_grokking.json` exists. Whatever MP-23's rows
  decide, `make paper` is in the CI mirror by MP-24's Step 0; this phase's Step 0 consumes
  the compiled PDF, clause by clause.
- **The horizon (ADR-0004) is written, not decided**: five rows with windows and
  kill-dates — real ACDC pilot, stranger review, scaled-up R1, 10-minute talk,
  stop-and-publish. Its Session-8 rule — zero undated rows — is what turns the capstone's
  end into a dated decision set, which is this phase's intake.

### Bottleneck analysis (ranked by what blocks what)

1. **MP-24's release report — everything consumes it.** The paper's PDF, the horizon
   stamps, the stranger's notes: this phase cannot open a single row without them. The
   treatment is the hard Session-0 gate (no PDF, no phase) and the intake table written
   before any planning prose — the discipline every phase since MP-21 has inherited,
   applied to the finale.
2. **The publication launch reflex.** The record's second mechanical failure mode once the
   science lands: a publishable artifact with no dated row stays a private file. ADR-0002
   proved a whole phase can pre-register publication and execute none of it; this phase's
   treatment is the *same-sitting rule* — a row enters LAUNCHED only with its artifact
   merged and its URL stamped, never with a plan.
3. **The ACDC pilot's dependency chain (if the horizon row opened).** Real circuit
   discovery needs a real head (MP-23's R1 verdict), a working EAP attribution backend, and
   a CPU budget that a threaded attribution run can exhaust. The treatment is the
   pre-registration-first rule: sites, metric, negative control and kill-date written
   before the first EAP forward pass — and a scheduled negative as a first-class result
   (inherited from MP-23's R4/R5 design).
4. **The site toolchain.** Quartz v4, GitHub Pages Actions and the vault's
   `publish: true/false` frontmatter policy are a new build pipeline on a new platform; the
   class of risk is exactly MP-21's missing `make`. The treatment is the Session-0 pin and
   the clean-clone-to-live-URL drill run twice — once as rehearsal, once as launch.
5. **The stranger and the revision cycle are human dependencies.** Dated windows with
   kill-dates on both sides: the review (inherited from MP-24) and the re-read of my fixes.
   If either dies in silence, the row closes with one named reason and the recorded
   self-review substitute — never a silent skip.
6. **The mypy ratchet (171)** — scheduled, non-blocking, at most one module in this phase;
   it must never be chased while a launch or a revision is pending.

## 1. Deep-dive study and research topics (bound to a session — no topic without a deliverable)

| Topic | Session | The deliverable that proves the reading |
|---|---|---|
| Conmy et al., *Towards Automated Circuit Discovery (ACDC)* (NeurIPS 2023) — read against my own hand-rolled implementation | S2 | The ACDC pilot's pre-registration: edge set, metric, negative control, kill-date — written before the first pass |
| Hanna et al., *Efficient Attribution Patching (EAP)* (2024) and Syed et al., *Attribution Patching Outputs (APO)* — the attribution-vs-intervention line | S2 | The EAP-on-real-head memo: my metric choices justified against the authors' named failure modes |
| Olsson et al., *In-context Learning and Induction Heads* (2022) — the scaling section: layers, context and head count as the design knobs | S5 | The scaled-up R1 pre-registration (if the horizon row opened): budget, seeds, detection threshold — or its scheduled negative |
| The 10-minute talk anatomy — my own MP-24 script, studied as a stranger would hear it: hook, claim, evidence, limit, next | S4 | The talk outline v2: timed sections, one sentence per slide, the two rewritten minutes |
| Quartz v4 documentation + the GitHub Pages Actions workflow + the vault's own `publish:` policy | S1 | The site-build book: one page — clone to filter to build to deploy, with the claims gate inserted |
| Anthropic, *Sparse Autoencoders Find Highly Interpretable Features* (April Update) — the SAE continuation line, if R5's delta warrants | S6 | The SAE verdict memo for the site's SAE page — retry, or the dated reason it stays closed |
| Writing for strangers: the paper-to-essay distillation — what survives a lost reader's first pass | S3 | The essay's reverse claims audit: every essay number walked back to its manifest, the rest struck |
| The stranger's own notes (MP-24's review) — studied as data, not as feedback | S3 | The revision matrix: friction point to cause to dated fix to re-read check |

Each reading produces a deliverable — the vault's golden rule, extended to the phase that
goes public.

## 2. Documentation requirements

- **The premiere ledger (ADR-0005)** — *new*: one row per public surface reopened under
  this phase's dates (essay, thread, site, Space, walkthrough), plus the revision cycle and
  the executed horizon rows (ACDC pilot, scaled R1) — each with a window, a heartbeat where
  a run exists, and a kill-date, under the ADR-0001 rules. Rows end LAUNCHED-with-URL or
  CLOSED-with-one-reason; zero UNDECIDED at Session 8.
- **The public essay** — `portfolio/essay.md`: the record's first public prose, distilled
  from the paper, every number manifest-tagged; the essay is never rewritten afterwards,
  only amended via dated annexes (the MP-23/24 inheritance).
- **The site** — the Quartz vault subset with the `publish: true/false` frontmatter policy,
  the paper's figures as the provenance-guarded asset set, and the claims gate in the
  build.
- **The thread** — six-post arc drafted from the essay, each post citing its manifest,
  scheduled and launched on a date.
- **The Space** — the CPU Superposition Explorer (Gradio): the verified Rung 3 engine
  behind a live demo, with its own engine health check.
- **The walkthrough transcript** — clean clone to `uv sync` to full suite to
  `verify-claims` to paper build to site live: one command line for a stranger to
  reproduce the premiere.
- **RESULTS v-release** — the versioned final sheet: what to trust, in order, with the
  public URLs beside the rows that shipped.
- **New notes (Obsidian, atomic, each linked ≥ 2 others)**: the ACDC-hand-roll note, the
  EAP attributions note, the premiere checklist note, the publish-policy note, the
  stranger-revision method note.
- **Skill tree** — flips only with a dated manifest or a stamped ledger row: ACDC [~] →
  [x] or closed with its reason; the publication rows end LAUNCHED or CLOSED with dates.
- **Progress log** — one dated entry per session; raw pass/fail before interpretation; a
  launch row is logged even if it fails — the failure is the note (the MP-12 lesson,
  applied to URLs).

## 3. Practical exercises and hands-on challenges

1. **The truthing pass (S0)**: read MP-24's release row by row — the PDF, the horizon
   stamps, the stranger's notes; the one-page scope: what the record can now claim
   publicly, in trust order. Exit: zero unsupported claims in the scope sheet.
2. **The premiere drill (S1)**: bare clone to `uv sync` to full suite to `verify-claims`
   to `make paper` to Quartz build to live URL, in one sitting, on a branch. The launch
   becomes boring before it is real (the MP-20 lesson, upgraded to the web).
3. **The ACDC hand-roll (S2)**: implement the algorithm from the paper on the real R1
   circuit (if the head exists) — expected: the discovered subgraph matches my hand-found
   circuit; the scheduled negative is a first-class result either way.
4. **The stranger-revision loop (S3)**: the three friction points from MP-24's review →
   three dated fixes → the re-read row, stamped in the same sitting as the fixes.
5. **The talk rehearsal on a live clock (S4)**: the scripted talk timed at 10 minutes; the
   from-memory draft is the real one (inherited); one dry run against a stopwatch, one
   against the site's pages.
6. **The site walk (S5)**: every public number clicked back to its manifest — the
   re-derivation game for the web, `verify-claims` open beside the browser.
7. **The EAP attribution run (S5, if the ACDC row opened)**: EAP score the real circuit's
   edges; compare the attribution ranking against the intervention ground truth from
   MP-23's R4 matrix.
8. **The three-draft thread (S6)**: the six-post arc drafted once from the essay, once
   from memory, once after a 24-hour pause — the second and third drafts are the real ones.
9. **The hostile-webmaster pass (S7)**: broken links, unbuilt pages, dead figures, missing
   accessibility basics, orphan pages — the site audit checklist walked as a complete
   transcript.
10. **Habit — the clock check (every session)**: the ledger's undated rows, the open PR's
    CI status line, the site's build status — all three before any new prose.

## 4. Strategic tips and architectural best practices

- **The URL is the proof.** A public surface that is not a LAUNCHED row with a date and an
  address does not exist. Plans are documents; the ledger row is the artifact a stranger
  opens.
- **Manifest-first on the web, too.** The site inherits the paper's law: a page cannot
  cite a number the claims gate cannot re-derive; the build fails loudly, never silently.
- **Toolchains are Step-0 decisions.** Quartz, MiKTeX, Gradio — each pinned and
  smoke-tested before the phase's first launch, never discovered at the release (the
  `make`-missing incident is the permanent precedent).
- **One sitting, one launch.** An artifact merged and a URL stamped in the same sitting is
  a launch; anything else is a plan with a date, which is a promise by another name.
- **The stranger's eyes are the cheapest validation the record can buy** — and they are a
  pipeline: review rows, revision rows, re-read rows, each with kill-dates; feedback
  absorbed silently is feedback lost.
- **The negative is the contribution** (inherited, now load-bearing): the premiere
  publishes the honest negatives with the same polish as the wins — the page that says
  "not reproduced" is a feature, not a gap.
- **Small surface, honest depth.** Publish only what the record proves; a site with five
  pages whose every number re-derives beats thirty pages of prose whose numbers don't.
- **Rehearse the release until it is boring.** Two clean-clone-to-live drills (S1 and S7)
  mean release day is a formality, not an adventure — the MP-17/20 rehearsal doctrine,
  applied to the public premiere.
- **Every hypothesis row carries its falsification and its kill-date** (Gelman & Loken,
  via ADR-0003): the ACDC pilot and scaled R1 open with their "what would falsify this"
  columns already written.
- **Session clocks beat mood clocks** (inherited, still true): every step has a wall clock
  and an exit gate.

## 5. Step-by-step execution roadmap

```
WEEK 1

SESSION 0 — THE PRE-FLIGHT (~30-60 min)
  Hard gate: MP-24's release report read row by row — the paper's PDF on
  disk, the horizon rows stamped, the stranger's notes filed. CI green
  locally AND on GitHub (the tracked 185, ruff, blocking mypy, markdownlint,
  `make paper` in the mirror). ADR-0005 opened with its rows and windows;
  the Quartz toolchain pinned and a smoke build pushed to a preview branch;
  this roadmap wired into home; pushed to dev; a green GitHub floor.
  Exit: the terminus is declared (release = this merge + 14 calendar days);
  the premiere drill is scheduled.

SESSION 1 — THE PREMIERE DRILL (~3 h)
  The clean-clone-to-live-URL drill on a branch: bare checkout → uv sync →
  full suite → verify-claims → paper build → Quartz build → pages deploy.
  The first rehearsal makes the launch boring. Exit: the drill transcript
  exists; the site branch builds green from the vault filter.

SESSION 2 — THE ACDC PRE-REGISTRATION (~3 h)
  The horizon rows consumed as decided: if the ACDC pilot opened — the
  hand-roll implementation and the pilot's pre-registration (edge set,
  metric, negative control, kill-date, scheduled negative) written before
  any EAP pass. The EAP/APO study's deliverable lands with it.
  Exit: the ACDC row is LAUNCHED-with-protocol or CLOSED-with-one-reason.

SESSION 3 — THE REVISION CYCLE (~2-3 h)
  The stranger's three friction points → three dated fixes → the re-read
  row stamped; the essay's reverse claims audit walks every draft sentence
  back to its manifest. Exit: the revision row is dated; the essay draft
  cites only disk.

WEEK 2

SESSION 4 — THE TALK + THE ESSAY (~3 h)
  The 10-minute talk rehearsed on a live clock (two drafts, the from-memory
  one counting); the essay's final prose pass with the hostile-reader ear.
  Exit: the talk script and the essay are revision-complete.

SESSION 5 — THE SCIENTIFIC EXECUTION (~3 h)
  The ACDC run (or its scheduled negative); the scaled-up R1 row decided
  with its budget and threshold, or closed with the no-head reason from
  MP-23's verdict; the site walk: every public number clicked back to its
  manifest. Exit: every executed horizon row is dated with a verdict.

SESSION 6 — THE THREAD + THE SPACE (~3 h)
  The six-post arc drafted three times and scheduled; the CPU
  Superposition Explorer rebuilt behind the Rung 3 engine with its health
  check; the SAE verdict memo filed. Exit: all five public rows exist on a
  branch with their dates and their artifacts.

SESSION 7 — THE HOSTILE-WEBMASTER + THE REHEARSAL (~3 h)
  The site audit walked as a transcript (links, assets, a11y, orphans);
  the full premiere rehearsal from a bare clone with the live deploy; mypy
  drift at most one module if the budget allows. Exit: the landing plan
  has been walked on a branch, twice.

SESSION 8 — THE RELEASE (the fixed terminus date)
  Merge on green; the essay, thread, site, Space and walkthrough rows
  LAUNCHED with their URLs; the horizon executed rows CLOSED or LAUNCHED
  under dates; home wired; this roadmap archived with its deviations —
  every deviation a dated ledger note. Exit: tree clean, `dev == main`,
  the ledger is the phase's after-the-fact truth, and the repository has
  an address.
```

## 6. Gate criteria

1. Session 0: MP-24's release report consumed row by row — the paper's PDF on disk; the CI
   floor green locally AND on GitHub; `make paper` in the mirror; the Quartz pin
   smoke-tested.
2. Session 1: the premiere drill transcript exists; the site builds green from the vault
   filter.
3. Session 2: the ACDC row is LAUNCHED-with-protocol (pre-registration on disk) or
   CLOSED-with-one-reason — zero undated rows at session end.
4. Session 3: the stranger's three friction points fixed with dates and re-read; the essay
   cites only manifests on disk.
5. Sessions 4-6: the talk and the essay are revision-complete; every public number
   re-derivable from a walked command; all five public rows carry artifacts and dates.
6. Session 7: the site audit transcript has zero unfixed issues; the premiere rehearsal has
   been walked twice on a branch.
7. Session 8: the merge is green; every ledger row is LAUNCHED-with-URL or
   CLOSED-with-one-reason; the progress log closes the loop.
8. The record-sanity gate: nothing on any public surface exceeds the record — every
   sentence survives `verify-claims` or is struck with a date.

## 7. Showcase note (for the portfolio reader)

The journey's public shape is now complete: I built a transformer from nothing, asked it
the smallest honest questions, caught real bugs in my own causal claims three times and
published the catches, answered the two flagship questions under pre-registered clocks,
wrote the answers in the order the evidence allowed — and then, in this phase, gave the
finished record an address. A stranger can open the paper, walk the site, run the demo,
replay the walkthrough transcript from a bare clone, and read the revision notes my first
reviewer forced me to write. Nine phases planned two runs; this is the phase that stopped
planning and started publishing — every number file-cited, every negative printed as a
contribution, every promise landed as a URL.

> "The phase where the notebook became a shelf: the paper had a reader, the results had
> links, the demo had a visitor, and the journey was finally legible to someone who never
> saw the vault."

## Links

- [[00_meta/23_micro-phase-24-the-synthesis]] — the roadmap this phase consumes; its
  release report and ADR-0004 stamps are Session 0's starting artifact.
- [[docs/adr/0004-horizon-ledger]] — the intake: the horizon rows this phase executes or
  closes, exactly as decided.
- [[docs/adr/0005-premiere-ledger]] — this phase's new ledger: the public surfaces, the
  revision cycle and the executed horizon rows.
- [[docs/adr/0002-public-arc-ledger]] · [[docs/adr/0003-research-return-ledger]] — the
  machines whose rows reopen here as NEW rows under this phase's dates.
- [[portfolio/RESULTS]] · [[portfolio/README]] — the results sheet this phase publishes in
  v-release; the shelf the URLs land on.
- [[portfolio/paper/main]] · [[portfolio/model-card]] — the paper the premiere hosts; the
  card that states the record's limits, once, dated.
- [[00_meta/03-progress-log]] — the dated record of every session, including the rows that
  closed (per the premiere ledger), the launches that failed (per the MP-12 lesson), and
  the first stranger's verdict (per MP-24's design).