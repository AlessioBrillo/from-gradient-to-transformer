#!/usr/bin/env bash
# gate_status: run the gate on the exact commit, then post the GitHub status `ci/local`.
#
# GitHub Actions is not the gate and no Woodpecker server reports to GitHub, so the merge
# protection of `main` requires the status `ci/local`, which only this script posts, and
# only after `ci-local` (the Woodpecker pipeline in .woodpecker/ci.yml) exits 0 on a clean
# tree. The status is a statement by the maintainer's machine, visible on the pull request;
# it is not an independent runner.
#
# Usage: scripts/gate_status.sh        (the commit must already be pushed)
set -euo pipefail

[ -z "$(git status --porcelain)" ] || { echo "gate_status: the tree is dirty; commit first" >&2; exit 2; }
sha=$(git rev-parse HEAD)
repo=$(git remote get-url origin | sed -E 's#.*github\.com[:/]##; s#\.git$##')
git fetch -q origin
git branch -r --contains "$sha" | grep -q . || {
  echo "gate_status: $sha is not on origin; push the branch first" >&2
  exit 2
}

ci-local   # set -e: a red gate stops here and no status is posted

gh api -X POST "repos/$repo/statuses/$sha" \
  -f state=success -f context=ci/local \
  -f description="ci-local green on the maintainer machine (.woodpecker/ci.yml)" >/dev/null
echo "gate_status: ci/local = success on $sha"
