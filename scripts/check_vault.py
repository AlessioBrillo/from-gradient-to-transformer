#!/usr/bin/env python3
"""Vault gate: enforce the note rules CLAUDE.md declares.

CLAUDE.md has always said "Every note links at least 2 other notes. No orphan
notes." and specified the tag schema `#phase/N`, `#type/lesson|exercise|proof|
moc`, `#state/review|consolidated`. Neither rule was enforced by anything, so
20 of 124 notes were in violation (12 with zero outbound links, 8 with one) and
only 54% of files carried all three required tags. `06_production_ai/_MOC.md`
was a placeholder indexing none of its 17 notes.

This script checks, for every markdown file under `01_*` .. `07_*`:

1. **Link degree** — at least 2 outbound `[[wikilinks]]`. MOCs and READMEs are
   index files and are exempt from the first rule but must exist.
2. **Frontmatter present** with a `tags:` list.
3. **Tag schema** — exactly one `phase/N`, exactly one `type/<kind>` from the
   allowed set, and at least one `state/<value>`.
4. **MOC coverage** — every note, exercise and proof must be listed in its
   phase's `_MOC.md`. A note nobody can navigate to is functionally an orphan.

Run: `make vault-check` (also a CI step, and part of `make ci-check`).
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

PHASES = [
    "01_foundations",
    "02_classical_ml",
    "03_deep_learning",
    "04_nlp_and_transformers",
    "05_llm_engineering",
    "06_production_ai",
    "07_capstone",
]

# Directories whose files are real content, plus the per-phase index files.
CONTENT_DIRS = ("notes", "exercises", "proofs")
INDEX_FILES = ("_MOC.md", "README.md", "checklist.md")

# Files exempt from the link-degree rule: they are indexes or administrative,
# and their job is to point at other files rather than be pointed at from them.
LINK_EXEMPT_BASENAMES = set(INDEX_FILES)

ALLOWED_TYPES = {"lesson", "exercise", "proof", "moc", "note"}
ALLOWED_STATES = {"review", "consolidated", "roadmap", "transition"}

# `07_capstone` predates the vault conventions and uses its own frontmatter
# keys (capstone, research/experiment, execution/log). It is checked for links
# and frontmatter, not for the phase/type/state schema.
SCHEMA_EXEMPT_DIRS = {"07_capstone"}

WIKILINK = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]")


def _frontmatter(text: str) -> tuple[dict, str]:
    """Split a markdown file into (frontmatter dict, body). Minimal YAML subset:
    only the flat `key: value` and `key: [a, b]` forms this vault uses.
    """
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end < 0:
        return {}, text
    raw = text[3:end].strip()
    body = text[end + 4 :]
    fm: dict[str, str] = {}
    for line in raw.split("\n"):
        if ":" not in line or line.lstrip().startswith("#"):
            continue
        key, _, value = line.partition(":")
        fm[key.strip()] = value.strip().strip("{}")
    return fm, body


def _tags(fm: dict) -> list[str]:
    raw = fm.get("tags", "")
    raw = raw.strip()
    if raw.startswith("[") and raw.endswith("]"):
        raw = raw[1:-1]
    return [t.strip().strip("'\"") for t in raw.split(",") if t.strip()]


def _outbound_links(body: str) -> set[str]:
    """Every distinct wikilink target in the body, normalised."""
    names = set()
    for m in WIKILINK.finditer(body):
        target = m.group(1).strip()
        if target:
            names.add(target)
    return names


def _note_stem(path: Path, phases_root: Path) -> str:
    """The bare note name used inside wikilinks, e.g. `induction-heads`."""
    return path.stem


def _phase_of(path: Path) -> str:
    """The `0N_name` directory this file lives in, e.g. `06_production_ai`."""
    for part in path.parts:
        if re.match(r"^0[1-7]_", part):
            return part
    return ""


def check_link_degree(
    files: list[Path], problems: list[str], *, fix: bool = False
) -> None:
    """Flag notes with fewer than 2 outbound wikilinks."""
    for path in files:
        text = path.read_text(encoding="utf-8")
        _, body = _frontmatter(text)
        links = _outbound_links(body)
        if len(links) >= 2:
            continue
        if path.name in LINK_EXEMPT_BASENAMES:
            continue
        # A note may legitimately link only into its own _MOC and be linked
        # *from* it; that still leaves the reader a dead end. Report the count.
        problems.append(
            f"{path.relative_to(REPO_ROOT).as_posix()}: {len(links)} outbound "
            "wikilink(s) — CLAUDE.md requires at least 2."
        )


def check_schema(files: list[Path], problems: list[str]) -> None:
    """Flag missing frontmatter and non-conforming tag values."""
    for path in files:
        text = path.read_text(encoding="utf-8")
        fm, _ = _frontmatter(text)
        rel = path.relative_to(REPO_ROOT).as_posix()
        phase = _phase_of(path)

        if not fm:
            if path.name not in LINK_EXEMPT_BASENAMES:
                problems.append(f"{rel}: no frontmatter.")
            continue
        if "tags" not in fm:
            problems.append(f"{rel}: frontmatter has no `tags:` field.")
            continue

        tags = _tags(fm)
        phases = [t for t in tags if t.startswith("phase/")]
        if len(phases) != 1:
            problems.append(
                f"{rel}: expected exactly one `phase/N` tag, got {phases or 'none'}."
            )
        elif phase:
            # The tag must match the directory the file lives in. `07_capstone`
            # notes carry `phase/7` and that is correct, so the rule is simply
            # "tag == directory", computed from the directory prefix — the
            # earlier `or phase/7` escape hatch let a phase-6 note be tagged
            # phase/7, which is how five capstone-research notes ended up
            # misfiled in 06_production_ai/notes/ in the first place.
            expected = f"phase/{int(phase[:2])}"
            if phases[0] != expected:
                problems.append(
                    f"{rel}: tagged {phases[0]} but lives in {phase}/ — "
                    f"expected {expected}. Mis-filed, or the tag is wrong."
                )

        if phase in SCHEMA_EXEMPT_DIRS:
            continue

        types = [t for t in tags if t.startswith("type/")]
        if len(types) != 1:
            problems.append(
                f"{rel}: expected exactly one `type/<kind>` tag, got "
                f"{[t[5:] for t in types] or 'none'}."
            )
        else:
            kind = types[0][5:]
            if kind not in ALLOWED_TYPES:
                problems.append(
                    f"{rel}: `type/{kind}` is not one of {sorted(ALLOWED_TYPES)}."
                )
            elif path.name in LINK_EXEMPT_BASENAMES and kind != "moc":
                problems.append(
                    f"{rel}: index file should be `type/moc`, got `type/{kind}`."
                )

        states = [t for t in tags if t.startswith("state/")]
        if not states:
            problems.append(f"{rel}: no `state/<value>` tag.")
        else:
            for s in states:
                if s[6:] not in ALLOWED_STATES:
                    problems.append(
                        f"{rel}: `{s}` is not one of {sorted(ALLOWED_STATES)}."
                    )


def check_moc_coverage(files: list[Path], problems: list[str]) -> None:
    """Every note/exercise/proof must be reachable from its phase's _MOC.md."""
    by_phase: dict[str, list[Path]] = {}
    for path in files:
        phase = _phase_of(path)
        if phase:
            by_phase.setdefault(phase, []).append(path)

    for phase, phase_files in by_phase.items():
        moc = REPO_ROOT / phase / "_MOC.md"
        if not moc.exists():
            problems.append(f"{phase}/_MOC.md: missing.")
            continue
        _, body = _frontmatter(moc.read_text(encoding="utf-8"))
        # MOCs link by vault path (`[[01_foundations/notes/foo|Foo]]`) while some
        # use a bare stem. Compare on the stem so both forms count.
        indexed = {Path(t).stem for t in _outbound_links(body)}
        indexed |= {Path(p).stem for p in _plain_paths(body)}
        missing = []
        for path in phase_files:
            if path.name in LINK_EXEMPT_BASENAMES:
                continue
            if path.stem in indexed:
                continue
            missing.append(path.relative_to(REPO_ROOT).as_posix())
        if missing:
            problems.append(
                f"{phase}/_MOC.md does not index {len(missing)} file(s): "
                + ", ".join(sorted(missing))
            )


def _plain_paths(body: str) -> set[str]:
    """Bare `notes/foo.md` style paths, which some MOCs use instead of links."""
    return set(re.findall(r"[\w./-]+\.md", body))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=REPO_ROOT,
        help="Repository root (default: this file's parent).",
    )
    args = parser.parse_args(argv)

    root = args.root.resolve()
    files: list[Path] = []
    for phase in PHASES:
        base = root / phase
        if not base.is_dir():
            continue
        for sub in list(CONTENT_DIRS):
            d = base / sub
            if d.is_dir():
                files.extend(sorted(d.glob("*.md")))
        for name in INDEX_FILES:
            f = base / name
            if f.is_file():
                files.append(f)

    if not files:
        print("check-vault: no vault files found — nothing to check.")
        return 0

    problems: list[str] = []
    check_link_degree(files, problems)
    check_schema(files, problems)
    check_moc_coverage(files, problems)

    if problems:
        print(f"check-vault: {len(problems)} problem(s) found\n")
        for p in problems:
            print(f"  - {p}")
        print(
            "\nCLAUDE.md: 'Every note links at least 2 other notes. No orphan notes.'"
            "\nFix the notes, not this script."
        )
        return 1

    print(f"check-vault: {len(files)} files checked — links, tags and MOC coverage OK.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
