# study-session

Structured workflow for a complete study session: from researching a topic through creating notes, exercises, proofs, and committing.

## When to load

User says: "I want to study X", "Let's study Y", "Help me learn Z"

## Workflow

### Step 1 — Identify

Ask the user:
- What concept to study?
- Which phase (01-07)?
- What to create: note only? note + exercise? note + exercise + proof?

### Step 2 — Research

Search the web for authoritative resources:
- 3Blue1Brown, Karpathy, StatQuest for visual intuition
- ArXiv papers for formal references
- Alammar, Lil'Log, Chip Huyen for blog-style explanations
- Official docs (PyTorch, Hugging Face, scikit-learn)

Read and understand before writing. Do not copy — rewrite in your own words.

### Step 3 — Create Note

```bash
bash scripts/new_note.sh <phase> notes "<Concept>"
```

Compile every section:

- **tags:** add correct `#phase/N` and `#type/lesson`
- **state:** leave as `review` initially
- **What it is:** one clear sentence defining the concept
- **Why it exists:** what problem does it solve? What gap does it fill?
- **How it works:** explanation with concrete example, diagram
  (ASCII or description), or minimal code
- **Links:** at least 2 wikilinks to existing notes (use `_MOC.md` files
  as starting points). Link to related phases.
- **Open questions:** add `#question` for anything unclear

### Step 4 — Create Exercise (if requested)

```bash
bash scripts/new_note.sh <phase> exercises "<Concept>"
```

Compile:

- **Goal / skill it demonstrates** — be specific
- **Solution** — working code or step-by-step reasoning
- **What I learned** — key takeaways from doing it
- **Linked skill** — `[[00_meta/02_skill-tree]] -> item: ...`

### Step 5 — Create Proof (if requested)

```bash
bash scripts/new_note.sh <phase> proofs "<Concept>"
```

The proof is done FROM MEMORY — no notes, no looking back.

Compile:

- **What I needed to demonstrate**
- **What I produced from memory**
- **Outcome:** [ ] Passed or [ ] Retry needed

### Step 6 — Update Skill Tree (if proof passed)

Read `00_meta/02_skill-tree.md` and find the matching skill for this proof.
Change `[ ]` -> `[x]` and append `— proof: [[<path/to/proof>]]`.

### Step 7 — Commit

One commit per file. If multiple files, one commit per logical unit:

```bash
git add <file>
git commit -m "feat(phaseN): add <concept> note"
git push
```

CI runs automatically on push to dev. If a check fails:
- Check which check failed and why
- Fix the issue
- Commit and push again
- Never push a broken commit to dev without fixing

## Rules

- Never copy-paste from sources. Rewrite everything in your own words.
- If you can't explain "why it exists", you haven't understood it yet — research more.
- Keep code minimal and runnable in the exercise files.
- CI must be green before any merge to main.
