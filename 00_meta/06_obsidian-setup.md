---
tags: [meta, obsidian]
---

# Obsidian Setup

## Opening
Obsidian → *Open folder as vault* → select the project folder. Entry point: [[00_home]].

## Core plugins to activate
- **Graph view** — visualize the link graph (the real value of this method).
- **Backlinks** / **Outgoing links** — see what points to what.
- **Templates** (core) or **Templater** (community) — to use files in `/templates`.
- **Tag pane** — navigate by `#phase/N`, `#question`, `#state/...`.

## Recommended community plugins

| Plugin | Why |
|--------|-----|
| **Dataview** | Auto-queries: "all open `#question` notes", phase progress dashboard, "recent exercises" |
| **Templater** | Inline scripting for auto-frontmatter (more powerful than core Templates) |
| **Excalidraw** | Hand-drawn diagrams: computation graphs, attention mechanisms, Transformer blocks |
| **Git** | Commit/push from inside Obsidian — the vault becomes a living repo |
| **Kanban** | Visual skill tree for each phase |
| **Calendar** | Navigate daily progress log entries |
| **Periodic Notes** | Weekly review notes for consolidation |
| **Admonition / Callouts** | Better formatting for exercises, questions, warnings in notes |

## Philosophy (à la Karpathy)
Treat the vault as a *knowledge codebase* that composes over time: each new lesson does not just add a note, but updates and links existing ones. The growing graph **is** the proof that you are understanding, not just accumulating.

## Example Dataview query (open questions dashboard)
````markdown
```dataview
LIST FROM #question WHERE !completed SORT file.mtime DESC
```
````

## Example Dataview query (phase progress)
````markdown
```dataview
TABLE phase, completed AS "Done" FROM "02_skill-tree" FLATTEN file.tags AS phase
```
````
