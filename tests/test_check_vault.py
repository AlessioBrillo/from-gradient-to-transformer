"""Tests for the vault gate (scripts/check_vault.py).

CLAUDE.md has always declared "Every note links at least 2 other notes. No
orphan notes" and the tag schema `#phase/N`, `#type/lesson|exercise|proof|moc`,
`#state/review|consolidated`. Nothing enforced either rule, so 20 of 124 notes
were in violation and only 54% of files carried all three tags. The gate now
runs in CI; these tests pin its behaviour on synthetic trees so a checker bug
cannot silently disable the rule.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"

_spec = importlib.util.spec_from_file_location("check_vault", SCRIPTS / "check_vault.py")
check_vault = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(check_vault)


def _note(path: Path, body: str, fm: str | None = None) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = f"---\n{fm}\n---\n\n{body}" if fm is not None else body
    path.write_text(text, encoding="utf-8")
    return path


@pytest.fixture
def vault(tmp_path: Path) -> Path:
    """A minimal but complete two-phase vault."""
    (tmp_path / "01_foundations" / "notes").mkdir(parents=True)
    (tmp_path / "01_foundations" / "exercises").mkdir(parents=True)
    (tmp_path / "01_foundations" / "proofs").mkdir(parents=True)
    (tmp_path / "06_production_ai" / "notes").mkdir(parents=True)
    return tmp_path


def _run(root: Path) -> list[str]:
    problems: list[str] = []
    files = sorted(p for p in root.glob("0[1-7]_*/*/*.md"))
    # Reuse the real file discovery against this synthetic root.
    files = []
    for phase in check_vault.PHASES:
        base = root / phase
        if not base.is_dir():
            continue
        for sub in check_vault.CONTENT_DIRS:
            d = base / sub
            if d.is_dir():
                files.extend(sorted(d.glob("*.md")))
        for name in check_vault.INDEX_FILES:
            f = base / name
            if f.is_file():
                files.append(f)
    # Patch REPO_ROOT so _phase_of / relative paths resolve inside the tmp tree.
    original = check_vault.REPO_ROOT
    check_vault.REPO_ROOT = root
    try:
        check_vault.check_link_degree(files, problems)
        check_vault.check_schema(files, problems)
        check_vault.check_moc_coverage(files, problems)
    finally:
        check_vault.REPO_ROOT = original
    return problems


def test_clean_vault_has_no_problems(vault: Path) -> None:
    _note(
        vault / "01_foundations" / "notes" / "a.md",
        "See [[01_foundations/notes/b|B]] and [[01_foundations/notes/c|C]].",
        fm="tags: [type/lesson, phase/1, state/consolidated]",
    )
    _note(
        vault / "01_foundations" / "notes" / "b.md",
        "See [[01_foundations/notes/a|A]] and [[01_foundations/notes/c|C]].",
        fm="tags: [type/lesson, phase/1, state/consolidated]",
    )
    _note(
        vault / "01_foundations" / "notes" / "c.md",
        "See [[01_foundations/notes/a|A]] and [[01_foundations/notes/b|B]].",
        fm="tags: [type/lesson, phase/1, state/consolidated]",
    )
    moc = "---\ntags: [type/moc, phase/1, state/consolidated]\n---\n\n" + (
        "- [[01_foundations/notes/a|A]]\n"
        "- [[01_foundations/notes/b|B]]\n"
        "- [[01_foundations/notes/c|C]]\n"
    )
    (vault / "01_foundations" / "_MOC.md").write_text(moc, encoding="utf-8")

    assert _run(vault) == []


def test_note_with_too_few_links_is_flagged(vault: Path) -> None:
    _note(
        vault / "01_foundations" / "notes" / "orphan.md",
        "Only one link: [[01_foundations/notes/other|Other]].",
        fm="tags: [type/lesson, phase/1, state/consolidated]",
    )
    problems = _run(vault)
    assert any("orphan.md" in p and "outbound wikilink" in p for p in problems)


def test_index_files_are_exempt_from_link_degree(vault: Path) -> None:
    """A MOC points at notes; it is not required to be pointed at from them."""
    _note(
        vault / "01_foundations" / "_MOC.md",
        "No links at all.",
        fm="tags: [type/moc, phase/1, state/consolidated]",
    )
    problems = _run(vault)
    assert not any("_MOC.md" in p and "outbound wikilink" in p for p in problems)


def test_missing_state_tag_is_flagged(vault: Path) -> None:
    _note(
        vault / "01_foundations" / "notes" / "stateless.md",
        "Links [[01_foundations/notes/x|X]] and [[01_foundations/notes/y|Y]].",
        fm="tags: [type/lesson, phase/1]",
    )
    problems = _run(vault)
    assert any("stateless.md" in p and "state/" in p for p in problems)


def test_bare_type_tag_is_flagged(vault: Path) -> None:
    """`note` / `moc` / `proof` bare tags are not the canonical `type/*` form."""
    _note(
        vault / "01_foundations" / "notes" / "bare.md",
        "Links [[01_foundations/notes/x|X]] and [[01_foundations/notes/y|Y]].",
        fm="tags: [note, phase/1, state/consolidated]",
    )
    problems = _run(vault)
    assert any("bare.md" in p and "type/" in p for p in problems)


def test_phase_tag_mismatch_is_flagged(vault: Path) -> None:
    _note(
        vault / "06_production_ai" / "notes" / "misfiled.md",
        "Links [[06_production_ai/notes/x|X]] and [[06_production_ai/notes/y|Y]].",
        fm="tags: [type/lesson, phase/7, state/review]",
    )
    problems = _run(vault)
    assert any("misfiled.md" in p and "Mis-filed" in p for p in problems)


def test_phase_seven_tag_is_accepted_in_capstone(vault: Path) -> None:
    """07_capstone notes legitimately carry phase/7."""
    cap = vault / "07_capstone" / "notes"
    cap.mkdir(parents=True, exist_ok=True)
    _note(
        cap / "ok.md",
        "Links [[07_capstone/notes/x|X]] and [[07_capstone/notes/y|Y]].",
        fm="tags: [type/lesson, phase/7, state/review]",
    )
    problems = _run(vault)
    assert not any("ok.md" in p and "mis-filed" in p for p in problems)


def test_unindexed_note_is_flagged(vault: Path) -> None:
    _note(
        vault / "01_foundations" / "notes" / "hidden.md",
        "Links [[01_foundations/notes/a|A]] and [[01_foundations/notes/b|B]].",
        fm="tags: [type/lesson, phase/1, state/consolidated]",
    )
    (vault / "01_foundations" / "_MOC.md").write_text(
        "---\ntags: [type/moc, phase/1, state/consolidated]\n---\n\nNothing indexed.\n",
        encoding="utf-8",
    )
    problems = _run(vault)
    assert any("_MOC.md" in p and "hidden.md" in p for p in problems)


def test_moc_accepts_both_wikilink_and_plain_path_forms(vault: Path) -> None:
    _note(
        vault / "01_foundations" / "notes" / "bylink.md",
        "Links [[01_foundations/notes/bypath|ByPath]] and [[01_foundations/notes/c|C]].",
        fm="tags: [type/lesson, phase/1, state/consolidated]",
    )
    _note(
        vault / "01_foundations" / "notes" / "bypath.md",
        "Links [[01_foundations/notes/bylink|ByLink]] and [[01_foundations/notes/c|C]].",
        fm="tags: [type/lesson, phase/1, state/consolidated]",
    )
    (vault / "01_foundations" / "_MOC.md").write_text(
        "---\ntags: [type/moc, phase/1, state/consolidated]\n---\n\n"
        "- [[01_foundations/notes/bylink|By Link]]\n"
        "- notes/bypath.md\n",
        encoding="utf-8",
    )
    problems = _run(vault)
    assert not any("bylink.md" in p or "bypath.md" in p for p in problems)


def test_missing_frontmatter_is_flagged(vault: Path) -> None:
    _note(vault / "01_foundations" / "notes" / "bare_file.md", "Links [[a|A]] and [[b|B]].")
    problems = _run(vault)
    assert any("bare_file.md" in p and "frontmatter" in p for p in problems)
