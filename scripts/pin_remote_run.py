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

# Declared record profiles per experiment. Naming the record set in one place
# prevents the silent-missing-file failure mode: a profile's `required` files
# must all be present, `optional` files are pinned when present, and nothing
# else is installed.
PROFILES: dict[str, dict[str, list[str]]] = {
    "induction-content": {
        "required": ["induction_content.json"],
        "optional": ["exp4_content.json", "exp5_content.json"],
    },
    "phase-diagram": {
        "required": [
            "phase_diagram_p113_nanda_wd10.json",
            "phase_diagram_p113_minibatch_wd10.json",
            "phase_diagram_p113_beta2_0999_wd10.json",
            "phase_diagram_p113_cosine_wd10.json",
            "phase_diagram_p113_renorm_wd10.json",
            "phase_diagram_p113_layernorm_wd10.json",
            "phase_diagram_p113_gradclip_1_wd10.json",
            "phase_diagram_p113_nanda_wd01.json",
            "phase_diagram_p113_nanda_wd05.json",
            "phase_diagram_p113_nanda_wd20.json",
        ],
        "optional": [],
    },
}


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
            f"{path.name}: {len(m.seeds)} seeds but {len(m.per_seed_metrics)} per-seed records"
        )
    for key, stats in m.aggregate.items():
        if int(stats.get("n", -1)) != len(m.seeds):
            problems.append(
                f"{path.name}: aggregate['{key}']['n']={stats.get('n')} != {len(m.seeds)} seeds"
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


def _expand_zips(source: Path) -> list[Path]:
    """Unzip any archives under `source`, returning the JSONs inside.

    The notebooks zip their manifests before download (one archive for both
    runtimes), so the download directory typically holds a .zip rather than
    loose .json files. Expanding here keeps the notebooks runtime-agnostic:
    Colab downloads the zip, Kaggle's kernel output carries the zip.
    """
    import zipfile

    candidates = sorted(source.rglob("*.json"))
    for archive in sorted(source.rglob("*.zip")):
        out_dir = archive.with_suffix("")
        out_dir.mkdir(parents=True, exist_ok=True)
        try:
            with zipfile.ZipFile(archive) as zf:
                zf.extractall(out_dir)
        except zipfile.BadZipFile as e:
            raise SystemExit(f"{archive.name} is not a readable zip: {e}")
        logger.info("expanded %s -> %s", archive.name, out_dir)
        candidates.extend(sorted(out_dir.rglob("*.json")))
    return candidates


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--from",
        dest="source",
        type=str,
        required=True,
        help="Directory of downloaded manifests (or a single .json)",
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Validate and report, install nothing"
    )
    parser.add_argument(
        "--force", action="store_true", help="Overwrite an existing file in results/"
    )
    parser.add_argument(
        "--results-dir",
        type=str,
        default=None,
        help=(
            "Where the validated manifests are installed (default: the "
            "repository's results/). A dry run against a directory that is not "
            "the repository's own is the supported way to rehearse a pinning "
            "without touching the tracked record — and it is what the test "
            "suite uses, so a test can never write into the repository."
        ),
    )
    parser.add_argument(
        "--only",
        default=None,
        help=(
            "Comma-separated file names to pin from the download directory "
            "(e.g. induction_content.json,exp4_content.json). Per-seed "
            "recovery manifests and the verdict JSON are valid JSON but are "
            "not the record; selecting the record explicitly is what keeps "
            "them out of results/."
        ),
    )
    parser.add_argument(
        "--profile",
        default=None,
        help=(
            "Named record set (e.g. induction-content). Implies --only with "
            "the profile's required + optional files; required files that are "
            "missing fail the run. Use --profile instead of --only for repeat"
            "able remote-run pinning."
        ),
    )
    args = parser.parse_args()

    # Resolve --profile into --only: required files must exist, optional ones
    # are pinned when present. --profile and --only are mutually exclusive.
    if args.profile and args.only:
        print("--profile and --only are mutually exclusive", file=sys.stderr)
        raise SystemExit(1)
    if args.profile:
        if args.profile not in PROFILES:
            print(
                f"--profile: unknown profile {args.profile!r}; "
                f"known: {', '.join(sorted(PROFILES))}",
                file=sys.stderr,
            )
            raise SystemExit(1)
        profile = PROFILES[args.profile]
        wanted = set(profile["required"]) | set(profile["optional"])
        args.only = ",".join(sorted(wanted))
        # Remember required set for the missing-file check below.
        args._profile_required = set(profile["required"])
    else:
        args._profile_required = set()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

    source = Path(args.source)
    if not source.is_absolute():
        source = REPO_ROOT / source
    if source.is_file() and source.suffix == ".zip":
        # A single downloaded archive: expand it, then validate the contents.
        candidates = _expand_zips(source.parent if source.parent != source else source.parent)
        candidates = [c for c in candidates if str(source.with_suffix("")) in str(c)]
    elif source.is_file():
        candidates = [source]
    else:
        candidates = _expand_zips(source)
    if not candidates:
        print(f"no .json manifests found under {source}", file=sys.stderr)
        raise SystemExit(1)

    if args.only:
        wanted = {name.strip() for name in args.only.split(",") if name.strip()}
        present = {c.name for c in candidates}
        missing = sorted(wanted - present)
        if missing:
            # With --profile, only required files are enforced; optional ones
            # that are missing are simply not pinned.
            required_missing = [
                m for m in missing if m in args._profile_required
            ]
            optional_missing = sorted(set(missing) - set(required_missing))
            if required_missing:
                print(
                    f"--only: {', '.join(required_missing)} not found under {source} "
                    "(required by --profile)",
                    file=sys.stderr,
                )
                raise SystemExit(1)
            if optional_missing:
                print(
                    f"--profile: optional files not present, skipping: "
                    f"{', '.join(optional_missing)}",
                    file=sys.stderr,
                )
            wanted = wanted - set(optional_missing)
        candidates = [c for c in candidates if c.name in wanted]

    all_problems: list[str] = []
    for path in candidates:
        all_problems.extend(validate_manifest(path))
    if all_problems:
        print("remote manifests FAILED validation — nothing installed:", file=sys.stderr)
        for p in all_problems:
            print(f"  - {p}", file=sys.stderr)
        raise SystemExit(1)

    installed: list[Path] = []
    results_dir = Path(args.results_dir) if args.results_dir else RESULTS_DIR
    if not results_dir.is_absolute():
        results_dir = REPO_ROOT / results_dir
    for path in candidates:
        target = results_dir / path.name
        if target.exists() and not args.force:
            if target.read_bytes() == path.read_bytes():
                logger.info("%s already pinned and identical", target.name)
                continue
            if args.dry_run:
                # A dry run installs nothing, so it must not refuse either:
                # the refusal exists to protect the tracked record from a
                # silent overwrite, and a rehearsal that cannot even report
                # "this would overwrite" is useless. The check that matters
                # for the rehearsal — provenance, seeds, aggregate — already
                # ran above. (The refusal *did* fire in --dry-run until
                # 2026-11-11, which made `make remote-pin` unusable as soon
                # as a tracked manifest had the same name as the file being
                # rehearsed, and broke three tests of the test suite.)
                print(
                    f"would overwrite {target.name} (different content; "
                    "pass --force to install it deliberately)",
                    file=sys.stderr,
                )
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

    # verify_claims checks that every citation in RESULTS.md resolves to an
    # existing, well-formed manifest. It does NOT check that every installed
    # manifest is cited — an uncited manifest is not a claim, it is just
    # data. So an uncited manifest cannot make verify-claims RED; print the
    # citation snippets as a reminder, not as a gate.
    problems = verify_claims(results_dir, CLAIMS_FILE)
    print()
    print("verify-claims after install:", "GREEN" if not problems else "RED")
    for p in problems:
        print(f"  - {p}")
    print()
    print("If any installed manifest backs a headline number in portfolio/RESULTS.md,")
    print("cite it next to that number with one of:")
    for target in installed:
        print(f"  <!-- manifest: results/{target.name} -->")
    print()
    print("verify-claims is GREEN when all cited manifests exist and are valid;")
    print("uncited manifests are data, not claims, and do not affect the gate.")
    if problems:
        raise SystemExit(1)
    print("all green; commit results/*.json on a branch and open a PR.")


if __name__ == "__main__":
    main()
