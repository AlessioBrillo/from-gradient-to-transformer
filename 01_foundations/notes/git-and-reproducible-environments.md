---
tags: [type/lesson, phase/1]
state: review
created: 2026-06-18
---

## What it is
Git tracks changes to files over time; a reproducible environment captures exact software dependencies (Python version, package versions, OS-level tools) so that code runs identically on any machine.

## Why it exists / what problem it solves
Without version control, you cannot roll back experiments, compare changes, or collaborate. Without reproducible environments, "it works on my machine" destroys trust in results. Together, Git and environment management form the scaffolding that makes machine learning experiments reproducible.

## How it works

### Git — the practical subset

**Initializing and committing:**
```bash
git init                    # start tracking
git add <file>              # stage changes
git commit -m "message"    # snapshot
```

**Branching (essential for experiments):**
```bash
git branch <name>           # create branch
git checkout <name>         # switch to it
git checkout -b <name>      # create + switch
git merge <branch>          # merge into current
```

**Inspecting history:**
```bash
git status                  # what changed?
git log --oneline -5        # last 5 commits
git diff                    # unstaged changes
git diff --staged           # staged changes
```

**Undoing mistakes:**
```bash
git checkout -- <file>      # discard unstaged changes
git reset --soft HEAD~1     # undo last commit, keep changes staged
git reset --hard HEAD~1     # undo last commit, discard changes (careful!)
```

### The experiment tracking workflow

1. Create a branch for each experiment: `git checkout -b experiment/lr-sweep`
2. Make changes, commit frequently.
3. If the experiment works, merge to main. If it fails, delete the branch.
4. Never commit to main directly.

### Reproducible environments

**uv (recommended for Python projects):**
```bash
uv init                     # create pyproject.toml
uv add numpy pandas torch   # add dependencies
uv sync                     # install everything
```

**venv + pip (the classic approach):**
```bash
python -m venv .venv        # create virtual environment
.venv\Scripts\activate      # activate (Windows)
source .venv/bin/activate   # activate (macOS/Linux)
pip install -r requirements.txt  # install deps
```

**Requirements files (for sharing):**
```bash
pip freeze > requirements.txt       # export exact versions
pip install -r requirements.txt     # reproduce on another machine
```

### The one rule

> **Every ML project must be reproducible from `git clone && pip install -r requirements.txt`.**

If someone cannot run your code with two commands, it is not reproducible. This means:
1. All code in version control (no "config files" outside git).
2. All dependencies in `requirements.txt` or `pyproject.toml`.
3. No hard-coded absolute paths.
4. Random seeds set explicitly for reproducible results.

```python
import numpy as np
import torch

# Always set seeds at the top of training scripts
np.random.seed(42)
torch.manual_seed(42)
```

## Links
- [[01_foundations/notes/pandas-for-data-preparation|pandas for Data Preparation]]
- [[01_foundations/notes/sql-for-data-pipelines|SQL for Data Pipelines]]

## Insight
Git branch management is the closest analogue to the scientific method in software engineering: each branch is a hypothesis, each commit is a reproducible step, and merging (or discarding) is the conclusion. Combined with a `requirements.txt`, every commit is a fully specified experiment that you or anyone else can reproduce at any point in the future.
