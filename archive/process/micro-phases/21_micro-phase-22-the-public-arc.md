---
tags: [type/moc, phase/6, phase/7, research/experiment, state/review]
created: 2026-08-09
---

# Micro-Phase 22 — The Public Arc: the Essay, the Thread, the Site, the Space, the Walkthrough

Written as a personal learning log and a public record, like every roadmap before it.
Micro-Phase 21 is the record's *proof of publication-readiness*: its release consumes
whatever the execution arc shipped and stamps the five gate rows (nnsight, W&B, HF
Spaces, clean-clone proof, graduation) as dated decisions — LAUNCHED or CLOSED, never
`[~]` again. This phase must not re-litigate that release; it must *translate* it. The
work is done. The record sits in the vault: manifests, figures, a compiling paper, a
verified superposition transition. What the record has never had is **an address** — a
page where a stranger can read the story honestly, a thread that tells it in six posts,
a slot that makes it hands-on, a site that renders the vault itself, and a walkthrough
that ends where the project actually stands. That is all this phase is: the public
arc. It adds no new scientific claims — it publishes the ones that survive contact
with a manifest, and it names the ones that didn't.

## Design decisions

- **The starting artifact is whatever MP-21 actually shipped.** Step 0 is a truthing
  pass over the release state — ledger rows, paper prose, gate stamps, clean-room
  transcript — and a *scope lock*: what the public arc can and cannot claim. Nothing in
  this roadmap re-plans MP-21; it consumes the release state, whichever way the rows
  decided.
- **The essay is the flagship public artifact.** One atomic file,
  `portfolio/essay.md` — the honest, readable account of the record — written under
  the same discipline as the paper: every paragraph that carries a number cites a
  manifest, a figure, or a ledger row on disk, and the headline numbers are re-derived
  from manifest + code, never from my own prose.
- **Every public channel ends LAUNCHED-with-a-date or CLOSED-with-one-reason.** The
  essay, the thread, the Space, the site — each is a row with a date. The no-news
  state that ends so many projects is this phase's institutional memory: the ledger
  discipline, applied to publication.
- **The toolchain is Quartz v4 on GitHub Pages.** The site (S4) renders the curated
  subset of the vault — wikilinks, embeds, tags, callouts — with the `publish:
  true/false` frontmatter policy as the single gate between vault and web. Local
  first (Quartz preview), then a `site/` branch + Pages, then the link lives in the
  essay, the card, the home MOC.
- **HF Spaces reopens as a *new* ledger row, scoped to CPU.** MP-21 may have closed
  the old "HF Spaces" box; this phase's row is a *new* decision with its own date:
  a CPU-only Superposition Explorer (a Gradio Space with the pentagon geometry slider)
  — the one result I can hand a random stranger. GPU-scoped rows stay closed.
- **The terminus is stamped at Step 0**: release = this roadmap's merge + 14 calendar
  days. On that date the phase ships: the essay, the site, the thread, the Space row
  — whichever rows are done, the honest residue is a dated list, not a silence.

## Where this phase starts (state review, verified against the repo)

I checked `git status`, the manifests, the ledger, the CI floor and the gate rows
before writing a single claim here.

- **Tree state**: `dev` and `main` are tree-identical (MP-21's release is in; the
  reconciling merge after the MP-20 squash is history-only). Working tree clean.
  No open PRs.
- **The CI floor, re-verified this session**: **185 tests passing**, ruff clean on
  `src/ tests/`, blocking mypy clean (`src/results.py`, `src/experiments/runner.py`),
  full-tree mypy at its tracked **171** (exit 1, the non-blocking ratchet),
  `make verify-claims` at exactly its designed 2 problems (Rung 2 and Rung 5
  manifestless by design), markdownlint 0 issues on the changed notes.
- **MP-21's gate stamps are this phase's starting sheet**: nnsight, W&B, HF Spaces,
  clean-clone proof, graduation — each ends LAUNCHED with a date or CLOSED with one
  reason inside MP-21's report. This phase reads the report; it does not re-plan.
  The only new row this phase opens over old names is the CPU-explicit HF Spaces row.
- **The essay's crown-jewel numbers** — the ones a random reader will check first —
  are the ones re-derived in S1's claims audit: Rung 3's phase transition (10/20 →
  20/20 represented as sparsity drops 0.5 → 0.01) and the pentagon geometry (gaps
  70.2–73.8°, std ≤ 1.4° vs the ideal 72°); the fresh-batches 52.2% val stabilization
  from the matched fixed-vs-fresh comparison; and whatever Rung 2's lane decided.
- **The record's honesty is the essay's spine, not its appendix**: the ledger's
  closed rows (Rung 6 — the deleted placeholder — and any lane that fired never
  again), the absent induction head, the never-reproduced grokking strip — each is
  published in the essay with its date, exactly like the positives.
- **`checkpoints/` still holds only the kill-drill artifacts** and the paper compiled
  its first draft under MP-21 — both enter the essay only through their manifests.

### Bottleneck analysis (ranked by what blocks what)

1. **The essay prose.** The single channel every other channel hangs off: the thread
   links the essay, the site frames it, the walkthrough walks it. Seated writing
   sessions with the file-citation rule are the only cure never fully tried — MP-21
   wrote them for the paper; this phase writes the essay.
2. **The claims audit.** Re-deriving the crown-jewel numbers from manifest + code
   (S1) decides which essay sentences survive. A number that cannot be re-derived is
   a struck sentence before drafts, not a footnote after.
3. **The Space row.** The only "new science-adjacent" artifact: a CPU-bound Gradio
   explorer with a live engine check. It has a kill-date like every row — scoped to
   CPU, clocked, honest.
4. **The site choreography.** Quartz renders wikilinks, but the curated subset is a
   policy decision (publish: true/false), not a build detail — a half-day of
   classification plus a deploy.
5. **The mypy ratchet (171)** — scheduled, not blocking: the same short-sittings
   mechanism as MP-21, at most one module in this phase.

## 1. Deep-dive study and research topics (bound to a session — no topic without a deliverable)

| Topic | Session | The deliverable that proves the reading |
|---|---|---|
| Pineau et al., "Improving Reproducibility in ML Research" (JMLR 2021) — re-read as the essay's methods section | S1 | The essay's reproducibility box: every number a command, every command a file — the claims audit table |
| Heath & Heath, *Made to Stick* (SUCCESs principles) | S2 | The essay's structure: the "public story" skeleton — what is Concrete, Credible, Emotional, Story-shaped in this record |
| Zinsser, *On Writing Well* (chapter: clutter) | S2 | The clutter pass list: the essay's sentences mapped against the six clutter rules, before the second draft |
| Fanelli, "Negative results in a high-profile journal" (2012) | S2 | The essay's honesty paragraph: why publishing negatives is the credibility move — written before the positives |
| Gelman & Loken, "The Garden of Forking Paths" (2013) — re-read | S3 | The essay's claims table's "what would falsify this" column — the honesty clause in the closing |
| Strunk &amp; White, *The Elements of Style* (plain words) | S3 | The rewrite pass: one hour, the essay read aloud, nothing survives that cannot be spoken |
| Elhage et al., "Toy Models of Superposition" (2022) — the canonical text behind the demo | S4 | The explorer's README: the article's story compressed into the one-visual explanation of the slider |
| Gradio docs + HF Spaces platform docs | S4 | The Space running on CPU (`space.yaml` + `app.py` in `scripts/spaces`) with a live engine check |
| Quartz v4 docs (content, publishing, hosting) | S5 | The site live on GitHub Pages with the publish: true/false subset chosen and buildable |
| Grokking progress measures (Nanda et al. 2023) — if the Rung 2 lane lives | S6 | The essay's grokking sentence written from the manifest the lane leaves — or the honest row |
| MP-21's clean-room transcript (the reproducible-from-clean-clone gate) | S7 | The walkthrough's final page: clone → sync → run → verify — the proof of the proof |
| The public-record craft: how explainers of results are written (Distill/Olah-style prefaces) | S7 | The walkthrough script with step numbers, timings and the honesty beats labeled |

The MP-20/21 reading lists are inherited wholesale — the study calendar is the same
calendar with this phase's slots bound to the essay, the demo, and the site.

## 2. Documentation requirements

- **Progress log**: one dated entry per session; raw pass/fail before interpretation;
  a publication row is logged even when the row never runs — the closure is the note.
- **The public-arc ledger (ADR-0002)** — *new*: one row per public surface (essay,
  thread, site, Space), each with date, window, kill-date, under the same rules as
  the closure ledger ADR-0001; closed-then-reopened is a NEW row, never a revision.
  The HF Spaces row reopens here with the CPU scope written in.
- **The essay** (`portfolio/essay.md`): the flagship artifact — every paragraph with
  a number carries its command/manifest citation; the negatives are date-stamped
  prose, not a footnote.
- **The thread** (`portfolio/thread.md`): six posts, each with the "proof beat" it
  lands — drafted with the honesty labels in place.
- **RESULTS.md / portfolio README / model card**: refreshed in S7 so the public
  addresses are the first claims a reader meets.
- **Skill tree**: the publication rows (essay, site, thread, Space) end LAUNCHED with
  a date or CLOSED with one reason — the `[~]` count for publication is zero at
  terminus.
- **New notes** (Obsidian, atomic, each linked to at least two others): the
  essay-writing note (S2), the explorer-design note (S4), the Quartz-setup note (S5),
  the thread-card note (S6), the walkthrough-script note (S7).

## 3. Practical exercises and hands-on challenges

1. **The truthing pass (S0 — the phase's Step 0)**: read MP-21's release state —
   ledger rows, gate stamps, paper %, manifests — and write the one-page scope:
   what the essay can and cannot claim. Exit: zero unsupported claims left in the
   scope.
2. **The claims audit (S0)**: re-derive three headline numbers from manifest + code —
   pentagon gaps 70.2–73.8°; fresh-batches 52.2%; one number born this phase. Each
   lands in the essay with its command.
3. **The essay skeleton (S1)**: claims → evidence → warrants on paper first; every
   sentence the essay will carry is already the record's.
4. **The honesty paragraph (S2)**: the closed lanes' exact words drafted before the
   positives — the negative is a contribution, not a confession.
5. **The public/private split (S4)**: classify the vault's notes into
   publish: true/false; the site ships the subset, the policy is a committed table.
6. **The five-minute demo (S4)**: a stranger can open the Space, move the sparsity
   slider, and see pentagon → collapse in under five minutes without a README — else
   the README is the bug.
7. **The engine check (S4)**: the demo's rendered figure must match the committed
   manifest's geometry — the "live" check that keeps the slider honest.
8. **The thread drill (S6)**: the six-post skeleton written cold (hook, number,
   honesty, how-to, campus, close) in one sitting; then re-written with S1's scope.
9. **The adversarial reader pass (S7)**: the essay read as three hypothetical
   reviewers who want to disprove me; the five strongest attack sentences per major
   section are fixed before release.
10. **The walkthrough rehearsal (S7)**: the whole public tour (essay → site → Space →
    thread) walked end-to-end on a branch, exactly as the release will do it.
11. **The mypy de-drift (optional, S7)**: 171 → ≤165, one module onto the blocking
    allowlist with its errors-at-move count.
12. **The clean-clone check (S8)**: fresh clone → `uv sync` → full suite → essay +
    site rebuilt → `verify-claims` — one transcript from bare checkout.
13. **Habit — the publication clock check (every session)**: the public-arc ledger's
    undated rows, the essay's status, the CI status line — before any prose.

## 4. Strategic tips and architectural best practices

- **The essay is the product; everything else points at it.** Site links, thread
  posts, card URL — if the essay is not the destination, the address structure is
  wrong.
- **A claim with no file is torn out.** The claims audit sentence deletion is the
  same discipline as the paper's citation rule at essay scale. If it can't be
  re-derived, it's future flakiness, not prose.
- **Publish the negative lanes first.** The essay's honesty paragraph written in S2
  anchors everything later — the positives are then the news, not the defense.
- **The demo is the demo of a *result*, not of a notebook.** The Space exists
  because a geometry check is runnable by a stranger; the engine check keeps the
  widget from becoming a PowerPoint.
- **The one-row test**: at any moment the public-arc ledger must have zero rows
  without a date; "no decision" is a decision by the end of its window.
- **Session clocks beat re-clocks** (inherited): every step below has a wall-clock
  and an exit gate.
- **Deferral-with-a-kill-date is a decision; deferral without one is instinct**
  (inherited): applies to essay sections, not just ledger rows.
- **Rehearse the release once, then release once** (inherited): the complete publish
  sequence is rehearsed at S7, so release day is a formality.

## 5. Step-by-step execution roadmap

```
WEEK 1

SESSION 0 — the pre-flight (~15–20 min)
  CI green locally AND on GitHub (185 tests, ruff, blocking mypy, markdownlint);
  the public-arc ledger ADR-0002 opened with the rows (essay, thread, site,
  Spaces) and dates; this roadmap wired into home; pushed to dev; CI green on
  GitHub. Exit: a green floor. [The fixed terminus: release = this merge + 14
  calendar days.]

SESSION 1 — THE TRUTHING and the CLAIMS AUDIT (the phase's Step 1, ~2 h)
  Read MP-21's release state row-by-row: gate stamps, ledger, paper prose %,
  manifests. Write the one-page scope: what the essay can and cannot claim.
  Re-derive the three headline numbers from manifest + code. Exit: zero
  unsupported claims in scope; the three numbers exist with their commands
  (or are struck with a reason).

SESSION 2 — THE ESSAY, TURN 1 (two seated hours)
  The essay skeleton → prose: the story, the verified geometry, the open
  negatives. Every paragraph cites a file. The honesty paragraph stands first.
  Exit: first full prose draft of the essay's core.

SESSION 3 — THE ESSAY, TURN 2 (two seated hours)
  The comparison sections (the numbers as fresh story), the "how far is it real"
  craft, edits from reading aloud. Exit: essay v0.9, every claim file-cited.

SESSION 4 — THE SPACE (the demo, ~3 h; the site together on S5)
  The CPU Superposition Explorer: `scripts/spaces/` app built on the committed
  exp3 math, the engine check wired (slider → figure vs manifest), uploaded to
  the ledgered row (LAUNCHED with URL) or CLOSED with one reason. The Quartz
  scaffold started (publish: true/false table committed).

WEEK 2

SESSION 5 — THE SITE and the publish: policy (~3 h)
  Quartz on GitHub Pages with the curated subset; the home links to the essay;
  the essay linked from the card. Exit: the site serves the essay publicly
  (or the row CLOSED with one reason).

SESSION 6 — THE THREAD and the row-closing (~2–3 h)
  The six-post thread under the honesty rule; the portfolio README + model card
  refreshed with the public addresses; the public-arc ledger re-read row by
  row, undated rows stamped before the session ends or struck with reason.

SESSION 7 — THE REHEARSAL (~2–3 h)
  The complete publish sequence rehearsed on a branch: essay final pass, site
  build, Spaces check, thread copy ready, walkthrough scripted; the
  adversarial-reader pass fixes applied; the mypy drift if the budget allows.

SESSION 8 — THE RELEASE (the fixed terminus date)
  The essay ships (portfolio/essay.md v1.0); the site, thread, and Space rows
  end LAUNCHED-with-date or CLOSED-with-reason; the clean-clone transcript
  (essay + Space + verify-claims); RESULTS + README + card reconciled; home
  wired; PR on green CI; merge; cleanup; this roadmap archived with its
  deviations — every deviation a dated ledger note.
```

## 6. Gate criteria

1. Session 0: the CI floor is green locally AND on GitHub — before the phase evicts
   a step.
2. Session 1: the claims table has three re-derived numbers, each with its own
   command; zero unsupported claims in the scope sheet.
3. Session 3: the essay exists in prose with every number file-cited; the honesty
   paragraph is present and specific (the negatives named with dates).
4. Session 4: the Space row is LAUNCHED (URL) or CLOSED (one reason), and — if
   launched — passes its own engine check against the committed manifest.
5. Session 5: the site publishes the curated subset with the policy table committed
   and the essay reachable from the address claimed in the essay's links.
6. Session 6: the thread draft is honest-side (the negatives in), and the public-arc
   ledger has zero undated rows at the end of the session.
7. Session 8: whatever rows are left, the ledger names them LAUNCHED or CLOSED under
   a date; `verify-claims` at zero unexpected; the PR merges on green; the terminus
   is kept.
8. The record-sanity gate: nothing in the essay exceeds the record — every public
   sentence is either verified on disk (manifest/code/ledger) or struck.

## 7. Showcase note (for the portfolio reader)

The research's deepest reward is not the slide deck — it is the record, and the
record was made public: the essay a first-time reader can follow from "what does a
transformer's internals mean" to "here is what this one taught me", the live
Superposition Explorer that puts the pentagon geometry in anyone's hand, the thread
one scroll long, and the site that finally has an address. The showcase motto:

*"The record surfaced: an essay with proof, a demo with an engine check, a thread
honest to its negatives, and the whole release traceable from a fresh clone."*

## Links

- [[20_micro-phase-21-the-record-assembly]] — the roadmap this phase consumes; its
  release state, gate stamps, and ledger revisions are this phase's starting artifact.
- [[19_micro-phase-20-execution-arc]] — the execution whose results become the
  essay's story; the inherited terminus rule (merge + 14 days).
- [[docs/adr/0001-verdict-closure-ledger]] — the ledger machinery this phase's
  public-arc ledger reuses; the HF Space row reopens as a new row here.
- [[docs/adr/0002-public-arc-ledger]] — this phase's own gate artifact: one row per
  public surface, each ending LAUNCHED or CLOSED under a date.
- [[portfolio/RESULTS]] · [[portfolio/README]] — the results the essay reconciles; the
  shelf the public addresses land on.
- [[03-progress-log]] — the dated record of every session, including the rows that
  closed.
- [[06_production_ai/proofs/reproducible-from-clean-clone]] — the proof whose
  transcripts this phase re-runs into the walkthrough's final page.