# phase-release

Complete a learning phase: verify everything is done, create a tagged release, and reset the dev branch. CI checks are mandatory before any merge.

## When to load
User says: "Phase N is complete", "Release Phase N", "Let's ship Phase N"

## Workflow

### Step 1 — Verify Phase Checklist
Read `<phase>/checklist.md`. Confirm every item is checked `[x]`.
If items are incomplete, list them for the user and ask whether to proceed or finish them first.

### Step 2 — Verify Skill Tree Proofs
Read `00_meta/02_skill-tree.md`. Check that every skill for `Phase N` has a linked proof file.
Missing proofs are gaps — flag them to the user.

### Step 3 — Update Progress Log
Append to `00_meta/03_progress-log.md`:

```markdown
## YYYY-MM-DD
- Completed Phase N: <phase name>
- Proofs verified: <count>/<total> skills have linked proofs
- Tag: v0.N.0
```

### Step 4 — Commit Changes on Dev
```bash
git add 00_meta/03_progress-log.md
git commit -m "docs(meta): mark Phase N as complete in progress log"
git push
```

### Step 5 — Create Pull Request
```bash
gh pr create \
  --base main \
  --head dev \
  --title "chore(release): Phase N complete" \
  --body "Phase N: <phase name>\n- All checklist items verified\n- Skill tree proofs linked\n\nSee [[00_meta/03_progress-log]] for details."
```

### Step 6 — Wait for CI (CRITICAL)
Before merging, all CI checks must be green:
```bash
gh pr checks <num> --watch
```
Wait until ALL checks pass:
- Markdown Lint / lint
- Conventional Commits / lint-commits
- Python Tests / test

If any check fails:
1. Identify the failure (check the workflow run URL)
2. Fix the issue on dev
3. Push the fix — the PR updates automatically
4. Wait for CI to re-run
5. Only merge when all checks show green

### Step 7 — Merge PR
```bash
gh pr merge <num> --squash --subject "chore(release): Phase N complete"
```

### Step 8 — Tag Release
```bash
git checkout main
git pull
git tag -a v0.N.0 -m "v0.N.0 — Phase N complete"
git push origin --tags
```

### Step 9 — Recreate Dev Branch
```bash
git branch -D dev
git checkout -b dev
git push -u origin dev --force
```

### Step 10 — Notify
Report to the user:
- v0.N.0 tagged and pushed
- Dev branch reset from main
- Phase N+1 is ready to start

## Notes
- The `--force` on dev push is safe because dev is a throwaway integration branch.
- Tags are the permanent record of progress. Each tag corresponds to one completed phase.
- Never merge without green CI. A red CI means something is broken — fix first.
