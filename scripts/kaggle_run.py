#!/usr/bin/env python3
"""Run a GPU experiment on Kaggle (or stage the identical run for Colab).

The repo's GPU work was blocked on hardware; the free tiers of Kaggle
(30 GPU-hours/week, ~9h sessions) and Colab (T4, variable sessions) cover
every remaining job, but only through one disciplined contract:

    run remotely -> manifests written by the experiment's own --seeds path
    -> download -> `pin_remote_run.py` validates and installs them
    -> verify-claims green -> a HUMAN commits

This script owns the remote half: it renders a Kaggle kernel from a
notebook (substituting the pinned git ref), pushes it, polls it, and
downloads the produced manifests. It never touches `results/` and never
commits — `scripts/pin_remote_run.py` does the installing, with
validation that fails closed.

Colab has no free programmatic run API, so Colab runs stay manual: the
same notebook opens from GitHub with one click, and the same pin command
ingests the downloaded manifests. One contract, two runtimes.

Usage:
    python scripts/kaggle_run.py --notebook notebooks/kaggle_grokking_p113.ipynb \\
        --branch main --dry-run
    python scripts/kaggle_run.py --notebook notebooks/kaggle_grokking_p113.ipynb \\
        --branch main --user <kaggle-username> [--poll] [--download]
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

logger = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_STAGING = Path("results/remote")
BRANCH_LINE_RE = re.compile(r'^BRANCH\s*=\s*["\']([^"\']*)["\']', re.MULTILINE)
MODULE_RE = re.compile(r"python -m (src\.experiments\.[a-z0-9_]+)")
FLAG_RE = re.compile(r"--[a-z0-9][a-z0-9-]*")


class NotebookError(ValueError):
    """The notebook violates the remote-run contract."""


# ---------------------------------------------------------------------------
# Notebook loading / rendering
# ---------------------------------------------------------------------------

def load_notebook(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as e:
        raise NotebookError(f"notebook not found: {path}") from e
    except json.JSONDecodeError as e:
        raise NotebookError(f"notebook is not valid JSON: {e}") from e


def _sources(cell: dict[str, Any]) -> str:
    return "".join(cell.get("source", []))


def set_branch(nb: dict[str, Any], ref: str) -> dict[str, Any]:
    """Point every `BRANCH = "..."` assignment at `ref`.

    The driver, not the author, decides the pinned ref: a run is only
    reproducible if the manifest's git_sha names a commit that exists.
    """
    rendered = 0
    for cell in nb.get("cells", []):
        if cell.get("cell_type") != "code":
            continue
        src = _sources(cell)
        new, n = BRANCH_LINE_RE.subn(f'BRANCH = "{ref}"', src)
        if n:
            cell["source"] = new.splitlines(keepends=True)
            rendered += n
    if not rendered:
        raise NotebookError(
            'notebook has no `BRANCH = "..."` assignment; the remote run '
            "must clone a pinned ref so its manifest names a real commit"
        )
    return nb


def code_cells(nb: dict[str, Any]) -> list[str]:
    return [_sources(c) for c in nb.get("cells", []) if c.get("cell_type") == "code"]


# ---------------------------------------------------------------------------
# Validation (shared with tests/test_remote_notebooks.py — CI runs the same
# rules on every notebooks/kaggle_*.ipynb, because the teaching artifact
# v22 rotted exactly this way: a notebook nobody checks is a notebook that
# lies about what the code can do)
# ---------------------------------------------------------------------------

def _module_flags(module: str) -> set[str]:
    """The flags `python -m <module> --help` accepts."""
    proc = subprocess.run(
        [sys.executable, "-m", module, "--help"],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
        timeout=300,
    )
    return set(FLAG_RE.findall(proc.stdout + proc.stderr))


def validate_notebook(nb: dict[str, Any], check_flags: bool = True) -> list[str]:
    """Every way a remote notebook can silently rot, as a problem list."""
    problems: list[str] = []
    cells = code_cells(nb)
    text = "\n".join(cells)

    if not any(BRANCH_LINE_RE.search(c) for c in cells):
        problems.append("no `BRANCH = ...` assignment")

    modules = sorted(set(MODULE_RE.findall(text)))
    if not modules:
        problems.append("no `python -m src.experiments.*` invocation to run")
    # Flags are validated per invocation line, so a flag used by one module
    # is checked against THAT module's parser.
    lines = [line for cell in cells for line in cell.splitlines()]
    for module in modules:
        try:
            __import__(module)
        except Exception as e:  # noqa: BLE001 - report, don't crash the lint
            problems.append(f"{module} does not import: {e}")
            continue
        if not check_flags:
            continue
        try:
            flags = _module_flags(module)
        except Exception as e:  # noqa: BLE001
            problems.append(f"{module} --help failed: {e}")
            continue
        for line in lines:
            if f"python -m {module}" not in line:
                continue
            for flag in FLAG_RE.findall(line):
                if flag not in flags:
                    problems.append(f"{module}: flag {flag} does not exist")

    for line in text.splitlines():
        for match in re.finditer(r"--manifest-path\s+(\S+)", line):
            target = match.group(1).strip("\"'")
            if not target.startswith("results/"):
                problems.append(f"--manifest-path {target} is not under results/")

    # The download cell must serve both runtimes: files.download on Colab,
    # /kaggle/working output on Kaggle. A Colab-only cell strands Kaggle
    # results and vice versa.
    if "google.colab" not in text:
        problems.append("no google.colab handling in the download cell")

    for cell in cells:
        if re.search(r"[A-Z]:\\|/Users/|/home/", cell):
            problems.append("absolute host path in a code cell (runs remotely!)")
            break

    if "cuda.is_available" not in text:
        problems.append("no GPU assertion — a CPU run wastes the session")

    return problems


def normalize_slug(raw: str) -> str:
    """Kaggle's slug rules: lowercase, no underscores.

    A kernel's public id is derived from its *title*, and Kaggle's
    slugifier turns underscores into hyphens — so `grokking_p113` becomes
    `grokking-p113` and every subsequent `kernels status/output` call by the
    underscore spelling fails with a permission error that reads like an
    auth problem. Normalizing here (and setting the metadata title to the
    same slug) keeps the id the driver prints and the id Kaggle assigns
    bit-identical.
    """
    return raw.strip().lower().replace("_", "-")


def kernel_dir_for(
    nb: dict[str, Any], nb_path: Path, ref: str, user: str, slug: str, out_dir: Path
) -> Path:
    """Render a Kaggle kernel directory: metadata + ref-pinned notebook."""
    slug = normalize_slug(slug)
    out_dir.mkdir(parents=True, exist_ok=True)
    metadata = {
        "id": f"{user}/{slug}",
        "title": slug,  # the title MUST slugify to the id — hence the same string
        "code_file": nb_path.name,
        "language": "python",
        "kernel_type": "notebook",
        "is_private": True,
        "enable_gpu": True,
        "enable_internet": True,
        "dataset_sources": [],
        "competition_sources": [],
        "kernel_sources": [],
    }
    (out_dir / "kernel-metadata.json").write_text(
        json.dumps(metadata, indent=2), encoding="utf-8"
    )
    shutil.copy(nb_path, out_dir / nb_path.name)
    # The rendered copy carries the pinned ref; the tracked notebook keeps
    # its placeholder so the repo stays ref-agnostic.
    (out_dir / nb_path.name).write_text(
        json.dumps(set_branch(nb, ref), indent=1), encoding="utf-8"
    )
    return out_dir


# ---------------------------------------------------------------------------
# Kaggle CLI plumbing
#
# The CLI is invoked as `sys.executable -m kaggle`, not as the `kaggle`
# executable: the module lives in the project venv, and a PATH lookup
# fails whenever the driver is run outside an activated venv — which is
# exactly how a `python scripts/kaggle_run.py ...` invocation happens.
# ---------------------------------------------------------------------------

def _kaggle(args: list[str], timeout: int = 120) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-m", "kaggle", *args], capture_output=True, text=True, timeout=timeout
    )


def kaggle_preflight() -> list[str]:
    """Is the kaggle CLI importable, with credentials?

    Kaggle's current auth is the KGAT API token — either the
    `KAGGLE_API_TOKEN` environment variable or the `~/.kaggle/access_token`
    file the CLI reads automatically. The legacy username/key pair
    (`~/.kaggle/kaggle.json`, or KAGGLE_USERNAME/KAGGLE_KEY) still works and
    is accepted too.
    """
    problems: list[str] = []
    kaggle_dir = Path.home() / ".kaggle"
    has_token = bool(os.environ.get("KAGGLE_API_TOKEN")) or (
        kaggle_dir / "access_token"
    ).exists()
    has_legacy = (kaggle_dir / "kaggle.json").exists() or (
        bool(os.environ.get("KAGGLE_USERNAME")) and bool(os.environ.get("KAGGLE_KEY"))
    )
    if not has_token and not has_legacy:
        problems.append(
            "no Kaggle credentials: save the KGAT token to "
            "~/.kaggle/access_token (Windows: C:\\Users\\<you>\\.kaggle\\access_token) "
            "or set KAGGLE_API_TOKEN — kaggle.com -> Settings -> Account -> "
            "Create New Token. Legacy ~/.kaggle/kaggle.json is also accepted."
        )
        return problems
    proc = _kaggle(["kernels", "list", "--mine"])
    if proc.returncode != 0:
        problems.append(
            f"kaggle credentials rejected: {(proc.stdout + proc.stderr).strip()[:200]}"
        )
    return problems


def push_kernel(kernel_dir: Path) -> None:
    proc = _kaggle(["kernels", "push", "-p", str(kernel_dir)], timeout=120)
    if proc.returncode != 0:
        raise RuntimeError(f"kaggle kernels push failed:\n{proc.stdout}\n{proc.stderr}")
    logger.info("pushed kernel: %s", proc.stdout.strip())


def poll_kernel(slug: str, user: str, timeout_s: int, interval_s: int = 60) -> str:
    """Poll until the kernel is complete or errors; returns the final state.

    A single status call is allowed to be slow (the Kaggle API occasionally
    hangs for minutes); a timeout is "unknown", not "dead" — the loop keeps
    polling until the overall budget expires.
    """
    ref = f"{user}/{normalize_slug(slug)}"
    deadline = time.monotonic() + timeout_s
    while True:
        try:
            proc = _kaggle(["kernels", "status", ref], timeout=300)
            state = (proc.stdout + proc.stderr).lower()
        except subprocess.TimeoutExpired:
            state = "status call timed out — still polling"
        logger.info("kaggle kernels status %s -> %s", ref, state.strip())
        if "complete" in state:
            return "complete"
        # A wrong slug surfaces as a permission error; anything else with
        # "error"/"cancel" is a genuine kernel failure.
        if ("error" in state or "cancel" in state) and "still polling" not in state:
            return "error"
        if time.monotonic() > deadline:
            return "timeout"
        time.sleep(interval_s)


def download_output(slug: str, user: str, out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    ref = f"{user}/{normalize_slug(slug)}"
    proc = _kaggle(["kernels", "output", ref, "-p", str(out_dir)], timeout=600)
    if proc.returncode != 0:
        raise RuntimeError(f"kaggle kernels output failed:\n{proc.stdout}\n{proc.stderr}")
    logger.info("downloaded kernel output into %s", out_dir)
    return out_dir


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--notebook", type=str, required=True, help="Path to notebooks/kaggle_*.ipynb"
    )
    parser.add_argument(
        "--branch", type=str, required=True,
        help="Pushed branch, tag or commit sha the remote run clones",
    )
    parser.add_argument(
        "--user", type=str, default=None, help="Kaggle username (kernel owner)"
    )
    parser.add_argument(
        "--slug", type=str, default=None, help="Kernel slug (default: notebook stem)"
    )
    parser.add_argument(
        "--staging-dir", type=str, default=str(DEFAULT_STAGING),
        help="Where the kernel dir and downloaded output land",
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Validate everything, push nothing"
    )
    parser.add_argument("--push", action="store_true", help="Push the kernel (default action)")
    parser.add_argument(
        "--poll-only",
        action="store_true",
        help=(
            "Do not push: attach to the already-pushed kernel with this slug "
            "and poll/download it. Recovers a run whose push succeeded but "
            "whose driver invocation died (the kernel keeps running on "
            "Kaggle regardless)."
        ),
    )
    parser.add_argument("--poll", action="store_true", help="Poll the kernel until it finishes")
    parser.add_argument(
        "--poll-timeout", type=int, default=9 * 3600,
        help="Poll budget in seconds (Kaggle sessions are ~9h)",
    )
    parser.add_argument("--download", action="store_true", help="Download the kernel output")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

    nb_path = Path(args.notebook)
    if not nb_path.is_absolute():
        nb_path = REPO_ROOT / nb_path
    nb = load_notebook(nb_path)
    ref = args.branch
    slug = normalize_slug(args.slug or nb_path.stem.removeprefix("kaggle_"))
    staging = REPO_ROOT / args.staging_dir / slug

    # --- validation (always, even on a real run: a broken notebook pushed
    # to Kaggle burns GPU hours to discover a typo) ---
    problems = validate_notebook(nb)
    if problems:
        print("notebook failed the remote-run contract:", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        raise SystemExit(1)

    remote_ref = subprocess.run(
        ["git", "ls-remote", "origin", ref], capture_output=True, text=True, cwd=REPO_ROOT
    ).stdout.strip()
    if not remote_ref:
        print(f"ref {ref!r} does not exist on origin — push it first", file=sys.stderr)
        raise SystemExit(1)
    logger.info("pinned ref %s -> %s", ref, remote_ref.split()[0][:8])

    kernel_dir = kernel_dir_for(
        nb, nb_path, ref, args.user or "<kaggle-user>", slug, staging / "kernel"
    )
    logger.info("kernel rendered at %s", kernel_dir)

    if args.dry_run:
        print(f"DRY RUN OK: {nb_path.name} is runnable at ref {ref}.")
        print(f"  kernel dir: {kernel_dir}")
        print(f"  to push:    python scripts/kaggle_run.py --notebook {args.notebook} "
              f"--branch {ref} --user <you> --poll --download")
        print(f"  Colab:      https://colab.research.google.com/github/AlessioBrillo/"
              f"from-gradient-to-transformer/blob/{ref}/{args.notebook}")
        return

    user = args.user
    if not user:
        print("--user is required to push (your Kaggle username)", file=sys.stderr)
        raise SystemExit(1)

    preflight = kaggle_preflight()
    if preflight:
        for p in preflight:
            print(f"  - {p}", file=sys.stderr)
        raise SystemExit(1)

    if not args.poll_only:
        push_kernel(kernel_dir_for(nb, nb_path, ref, user, slug, staging / "kernel"))
    else:
        logger.info("poll-only: attaching to the already-pushed kernel %s/%s", user, slug)

    if args.poll:
        state = poll_kernel(slug, user, args.poll_timeout)
        logger.info("kernel finished in state: %s", state)
        if state != "complete":
            raise SystemExit(f"kernel did not complete: {state}")

    if args.download:
        out_dir = download_output(slug, user, staging / "output")
        print("download the manifests back with:")
        print(f"  python scripts/pin_remote_run.py --from {out_dir}")


if __name__ == "__main__":
    main()
