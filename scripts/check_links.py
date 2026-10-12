#!/usr/bin/env python3
"""Check that every vault wikilink resolves to a real file.

`check_vault.py` checks link *degree*, tags and MOC coverage — it does not check
that a link's target exists. Moving five notes out of `06_production_ai/notes/`
on 2026-10-11 rewrote ~130 references, and a missed one would leave a dead link
that nothing else catches. This script is that safety net.

Scope: the **live** vault (01..07), `portfolio/`, `docs/` and the root
documents. `00_meta/` is the dated historical archive that ADR-0031 freezes —
it is excluded by default and reported separately, because it carries real
pre-existing dead links (`[[04_nlp_and_transformers/notes/attribution-patching]]
points at a note that was never written, `[[03-progress-log]]` uses hyphens
where the file uses underscores, and `04_conventions.md` uses `[[links]]` and
`[[wikilink]]` as literal examples). Fixing those is a separate, dated piece of
work; silently ignoring them is not, so the count is printed either way.

Run: `make check-links` (also a CI step), or `--archive` to fold the archive
into the failure set.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

PHASES = (
    "01_foundations",
    "02_classical_ml",
    "03_deep_learning",
    "04_nlp_and_transformers",
    "05_llm_engineering",
    "06_production_ai",
    "07_capstone",
)

LIVE_TOP = PHASES + ("portfolio", "docs", "references", "templates", "configs", "scripts", "src")
LIVE_ROOT_DOCS = ("README.md", "CLAUDE.md", "CONTEXT.md")
ARCHIVE_DIR = "00_meta"

SKIP_DIRS = {".venv", ".git", ".obsidian", "_site", "node_modules", "__pycache__", ".pytest_cache"}
WIKILINK = re.compile(r"\[\[([^\]|#]+?)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]")


def _collect(root: Path) -> tuple[list[Path], set[str]]:
    """Markdown files plus every resolvable link target name."""
    md_files: list[Path] = []
    known: set[str] = set()
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        rel = path.relative_to(root)
        known.add(rel.with_suffix("").as_posix())
        known.add(path.stem)
        if path.suffix == ".md":
            md_files.append(path)
    return md_files, known


def _resolve(target: str, known: set[str]) -> bool:
    if target in known:
        return True
    # Obsidian resolves a bare stem anywhere in the vault.
    return Path(target).stem in known


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--archive",
        action="store_true",
        help="Also fail on dead links inside the frozen 00_meta/ archive.",
    )
    args = parser.parse_args(argv)

    md_files, known = _collect(REPO_ROOT)

    def in_scope(path: Path) -> bool:
        rel = path.relative_to(REPO_ROOT)
        if args.archive:
            return True
        if len(rel.parts) == 1:
            return rel.name in LIVE_ROOT_DOCS
        if rel.parts[0] not in LIVE_TOP:
            return False
        return True

    broken: list[str] = []
    archive_broken: list[str] = []
    total = 0
    for md in sorted(md_files):
        text = md.read_text(encoding="utf-8", errors="replace")
        for m in WIKILINK.finditer(text):
            target = m.group(1).strip()
            if not target:
                continue
            total += 1
            if _resolve(target, known):
                continue
            entry = f"{md.relative_to(REPO_ROOT).as_posix()}: [[{target}]]"
            if in_scope(md):
                broken.append(entry)
            else:
                archive_broken.append(entry)

    if archive_broken:
        print(
            f"check-links: {len(archive_broken)} dead link(s) in the frozen "
            f"{ARCHIVE_DIR}/ archive (reported, not enforced).\n"
        )

    if broken:
        print(f"check-links: {len(broken)} broken wikilink(s) of {total} total\n")
        for b in broken:
            print(f"  - {b}")
        return 1

    print(f"check-links: {total} wikilink(s) checked — all resolve.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
