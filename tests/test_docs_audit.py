"""Tests for the record audit (`scripts/docs_audit.py`).

The audit is a ratchet, and a ratchet is only worth something if it
*fires*. These tests check both halves of that:

1. the audit passes on the current tree — a ratchet that fails on the
   repository it guards is worse than no ratchet;
2. the audit actually fails when a known-false statement comes back, and
   when a current-facing document stops naming its manifest.

The second half is the one that matters: on 2026-10-20 the paper's
limitations, the writeup, the skill tree and the README all stated claims
their own manifests had already falsified, and `make verify-claims` was
green throughout, because the stale sentences carried no manifest tag.
"""

from __future__ import annotations

from pathlib import Path

from scripts.docs_audit import (
    REQUIRED_MANIFESTS,
    STALE_CLAIMS,
    check_required_manifests,
    check_stale_claims,
)

REPO_ROOT = Path(__file__).resolve().parents[1]


class TestTheAuditPassesOnTheCurrentTree:
    def test_no_stale_claim_is_back(self) -> None:
        problems = check_stale_claims()
        assert problems == [], "\n".join(problems)

    def test_every_current_facing_document_names_its_manifests(self) -> None:
        problems = check_required_manifests()
        assert problems == [], "\n".join(problems)


class TestTheAuditFires:
    def test_a_retracted_statement_coming_back_is_caught(self, tmp_path: Path) -> None:
        """The ratchet has to fire on the real file, not on a copy."""
        target = REPO_ROOT / STALE_CLAIMS[0][0]
        original = target.read_text(encoding="utf-8")
        sentence = STALE_CLAIMS[0][1]
        assert sentence not in original  # the tree is clean
        try:
            target.write_text(
                original + "\n" + sentence + "\n", encoding="utf-8"
            )
            problems = check_stale_claims()
            assert any(STALE_CLAIMS[0][1] in p for p in problems)
        finally:
            target.write_text(original, encoding="utf-8")
        assert check_stale_claims() == []

    def test_a_document_that_stops_naming_its_manifest_is_caught(
        self, tmp_path: Path
    ) -> None:
        target = REPO_ROOT / "CONTEXT.md"
        original = target.read_text(encoding="utf-8")
        try:
            # Drop one required tag and the audit has to notice.
            target.write_text(
                original.replace(
                    "<!-- manifest: results/exp4_standard.json -->", "", 1
                ),
                encoding="utf-8",
            )
            problems = check_required_manifests()
            assert any("exp4_standard.json" in p for p in problems)
        finally:
            target.write_text(original, encoding="utf-8")
        assert check_required_manifests() == []


class TestTheAuditListIsSane:
    def test_every_entry_names_a_file_that_exists(self) -> None:
        for rel, _sentence, _replacement, _when in STALE_CLAIMS:
            assert (REPO_ROOT / rel).is_file(), rel

    def test_every_entry_is_a_distinct_claim(self) -> None:
        keys = [(rel, sentence) for rel, sentence, _r, _w in STALE_CLAIMS]
        assert len(set(keys)) == len(keys)

    def test_every_required_document_exists(self) -> None:
        for rel in REQUIRED_MANIFESTS:
            assert (REPO_ROOT / rel).is_file(), rel

    def test_every_required_manifest_exists_and_is_tracked(self) -> None:
        import subprocess

        for manifests in REQUIRED_MANIFESTS.values():
            for manifest in manifests:
                path = REPO_ROOT / manifest
                assert path.is_file(), manifest
                tracked = subprocess.run(
                    ["git", "ls-files", "--error-unmatch", manifest],
                    cwd=REPO_ROOT,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                assert tracked.returncode == 0, f"{manifest} is not tracked"


def test_the_audit_script_runs_as_a_program() -> None:
    """`make docs-audit` must exit 0 on a clean tree."""
    import subprocess

    out = subprocess.run(
        ["uv", "run", "python", "scripts/docs_audit.py"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert out.returncode == 0, out.stdout + out.stderr
    assert "docs-audit: OK" in out.stdout
