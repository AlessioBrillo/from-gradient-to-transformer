#!/usr/bin/env python3
"""Pin manifests produced by a remote (Kaggle/Colab) GPU run into `results/`.

The remote runs write their own manifests through the experiments'
`--seeds --manifest-path` path, so the files coming back are complete
`ResultsManifest` JSON with provenance (git sha, dirty flag, device).
This tool validates and installs them — it never trusts them blindly:

    1. each file must load as a ResultsManifest with a non-empty aggregate;
    2. seeds must match per-seed records, aggregate n must match seeds
       (the structural contract `verify_claims` enforces locally);
    3. the recorded git_sha must resolve in THIS checkout — a manifest
       recorded against a commit that does not exist here is exactly the
       provenance drift the manifest system exists to prevent;
    4. a manifest recorded with a dirty tree is refused: remote runs clone
       a pinned ref, so a dirty flag means the provenance is wrong;
    5. no file is overwritten without --force, and nothing is installed if
       ANY file fails (fail-closed, atomicity by refusal).

After installing, it re-runs `verify-claims` and prints the exact
`<!-- manifest: ... -->` citation snippet for each installed manifest.

Usage:
    python scripts/pin_remote_run.py --from results/remote/<slug>/output
    python scripts/pin_remote_run.py --from <dir> --dry-run
    python scripts/pin_remote_run.py --from <dir> --force  # overwrite an existing file
"""

from __future__ import annotations

import argparse
import logging
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.results import ResultsManifest, verify_claims  # noqa: E402

logger = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = REPO_ROOT / "results"
CLAIMS_FILE = REPO_ROOT / "portfolio" / "RESULTS.md"


def _git_sha_exists(sha: str) -> bool:
    proc = subprocess.run(
        ["git", "cat-file", "-e", f"{sha}^{{commit}}"],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )
    return proc.returncode == 0


def validate_manifest(path: Path) -> list[str]:
    """Every check that must pass before a remote manifest can be cited."""
    problems: list[str] = []
    try:
        m = ResultsManifest.load(path)
    except Exception as e:  # noqa: BLE001 - report, don't crash
        return [f"{path.name}: not a ResultsManifest ({e})"]

    if not m.aggregate:
        problems.append(f"{path.name}: empty aggregate — nothing was measured")
    if len(m.seeds) != len(m.per_seed_metrics):
        problems.append(
            f"{path.name}: {len(m.seeds)} seeds but "
            f"{len(m.per_seed_metrics)} per-seed records"
        )
    for key, stats in m.aggregate.items():
        if int(stats.get("n", -1)) != len(m.seeds):
            problems.append(
                f"{path.name}: aggregate['{key}']['n']={stats.get('n')} != "
                f"{len(m.seeds)} seeds"
            )
    if m.git_dirty:
        problems.append(
            f"{path.name}: recorded with a dirty working tree — remote runs "
            "clone a pinned ref, so the provenance is wrong"
        )
    if not _git_sha_exists(m.git_sha):
        problems.append(
            f"{path.name}: git_sha {m.git_sha[:8]} does not exist in this "
            "checkout — fetch it (git fetch origin <ref>) before pinning"
        )
    return problems


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--from", dest="source", type=str, required=True,
                        help="Directory of downloaded manifests (or a single .json)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Validate and report, install nothing")
    parser.add_argument("--force", action="store_true",
                        help="Overwrite an existing file in results/")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

    source = Path(args.source)
    if not source.is_absolute():
        source = REPO_ROOT / source
    if source.is_file():
        candidates = [source]
    else:
        candidates = sorted(p for p in source.rglob("*.json") if p.is_file())
    if not candidates:
        print(f"no .json manifests found under {source}", file=sys.stderr)
        raise SystemExit(1)

    all_problems: list[str] = []
    for path in candidates:
        all_problems.extend(validate_manifest(path))
    if all_problems:
        print("remote manifests FAILED validation — nothing installed:", file=sys.stderr)
        for p in all_problems:
            print(f"  - {p}", file=sys.stderr)
        raise SystemExit(1)

    installed: list[Path] = []
    for path in candidates:
        target = RESULTS_DIR / path.name
        if target.exists() and not args.force:
            if target.read_bytes() == path.read_bytes():
                logger.info("%s already pinned and identical", target.name)
                continue
            print(
                f"refusing to overwrite tracked {target.name} "
                "(different content; pass --force deliberately)",
                file=sys.stderr,
            )
            raise SystemExit(1)
        if args.dry_run:
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(path, target)
        installed.append(target)
        logger.info("installed %s", target)

    if args.dry_run:
        print(f"DRY RUN OK: {len(candidates)} manifest(s) valid and ready to pin.")
        return

    # The gate: a new manifest in results/ that nothing cites fails
    # verify-claims until the author adds the tag — print exactly what to add.
    problems = verify_claims(RESULTS_DIR, CLAIMS_FILE)
    print()
    print("verify-claims after install:", "GREEN" if not problems else "RED")
    for p in problems:
        print(f"  - {p}")
    print()
    print("cite each manifest next to its headline number in portfolio/RESULTS.md:")
    for target in installed:
        print(f"  <!-- manifest: results/{target.name} -->")
    if problems:
        print(
            "\nverify-claims is RED because the new manifests are not cited "
            "yet — add the tags above, then re-run `make verify-claims`."
        )
        raise SystemExit(1)
    print("\nall green; commit results/*.json on a branch and open a PR.")


if __name__ == "__main__":
    main()
