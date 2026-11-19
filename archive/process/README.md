# Process archive

Frozen history. Nothing in this directory is a current claim.

Between 2026-08 and 2026-10 this project was run through "micro-phase"
roadmaps, each with a ledger ADR that pre-stamped rows for a later session to
close. [ADR-0031](../../docs/adr/0031-closure.md) closed that process on
2026-10-08: it had started to cost more than it returned, and the remaining
work moved to GitHub Issues. The documents were moved here on 2026-11-16 so
that a reader of the repository meets the results first and the process second.

They are kept, not deleted, because the record of how a conclusion was reached
(including the plans that were wrong) is part of the evidence.

| Directory | Contents |
|---|---|
| `micro-phases/` | The micro-phase roadmaps and release reports (formerly `00_meta/07_*` to `94_*`) |
| `adr/` | Ledger ADRs 0001 to 0030 (formerly `docs/adr/`). Numbers 0011 to 0022 and 0026 were never written |
| `capstone-notes/` | Session notes named after a micro-phase (formerly `07_capstone/notes/mp-*`) |
| `portfolio/` | Launch drafts and the premiere ledger (formerly under `portfolio/`) |
| `gate-debt.md` | The gate-debt checklist (formerly `checklists/gate-debt.md`) |

## How to read these files

- Statuses and sentences describe the state **on the date they were written**.
  Several were later reversed; for example, the P=113 NO-GROK verdict was
  retracted on 2026-10-14.
- The authority on what is true is
  [`portfolio/RESULTS.md`](../../portfolio/RESULTS.md).
- Paths inside these files are the paths of their time. Wikilinks still resolve
  by note name in Obsidian; relative Markdown links may not.
- Links inside the archive are reported by `make vault-check` but not enforced.
