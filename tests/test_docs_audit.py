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

import json
from pathlib import Path

from scripts.docs_audit import (
    REQUIRED_MANIFESTS,
    STALE_CLAIMS,
    _is_gitignored,
    check_audit_count,
    check_numbers_against_manifests,
    check_referenced_manifests_exist,
    check_required_manifests,
    check_results_index,
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

    def test_public_documents_agree_on_the_audit_count(self) -> None:
        problems = check_audit_count()
        assert problems == [], "\n".join(problems)

    def test_the_numbers_in_the_tables_match_their_manifests(self) -> None:
        problems = check_numbers_against_manifests()
        assert problems == [], "\n".join(problems)

    def test_every_tracked_manifest_is_indexed(self) -> None:
        problems = check_results_index()
        assert problems == [], "\n".join(problems)

    def test_every_manifest_a_document_names_exists(self) -> None:
        problems = check_referenced_manifests_exist()
        assert problems == [], "\n".join(problems)


class TestTheAuditFires:
    def test_a_retracted_statement_coming_back_is_caught(self, tmp_path: Path) -> None:
        """The ratchet has to fire on the real file, not on a copy.

        The file is restored **byte for byte**: writing back the decoded
        text would rewrite the line endings, and a test run that leaves the
        tree dirty makes every manifest written afterwards claim
        `git_dirty: true` for a tree nobody changed.
        """
        target = REPO_ROOT / STALE_CLAIMS[0][0]
        original = target.read_bytes()
        text = original.decode("utf-8")
        sentence = STALE_CLAIMS[0][1]
        assert sentence not in text  # the tree is clean
        try:
            target.write_bytes((text + "\n" + sentence + "\n").encode("utf-8"))
            problems = check_stale_claims()
            assert any(STALE_CLAIMS[0][1] in p for p in problems)
        finally:
            target.write_bytes(original)
        assert check_stale_claims() == []

    def test_a_stale_audit_count_is_caught(self) -> None:
        """The ledger said ten while README/writeup/checklist said nine."""
        target = REPO_ROOT / "README.md"
        original = target.read_bytes()
        text = original.decode("utf-8")
        assert "twelve audits" in text
        try:
            target.write_bytes(
                text.replace("twelve audits", "nine audits", 1).encode("utf-8")
            )
            problems = check_audit_count()
            assert any("README.md" in p and "nine" in p for p in problems), problems
        finally:
            target.write_bytes(original)
        assert check_audit_count() == []

    def test_a_number_that_contradicts_its_manifest_is_caught(self) -> None:
        """The 2026-11-11 drift: a table carried the right tag and the wrong
        numbers. A tag proves that evidence exists; it does not prove that
        the number next to it is that evidence."""
        target = REPO_ROOT / "portfolio/RESULTS.md"
        original = target.read_bytes()
        text = original.decode("utf-8")
        # The Rung 2 section cites results/grokking_nanda_p113.json, whose
        # final validation accuracy is 0.9999 to four decimals.
        assert "| **0.9999 ± 0.0002** |" in text
        try:
            target.write_bytes(
                text.replace("| **0.9999 ± 0.0002** |", "| **0.9989 ± 0.0002** |", 1).encode(
                    "utf-8"
                )
            )
            problems = check_numbers_against_manifests()
            assert any("RESULTS.md" in p for p in problems), problems
        finally:
            target.write_bytes(original)
        assert check_numbers_against_manifests() == []

    def test_a_manifest_missing_from_the_index_is_caught(self) -> None:
        target = REPO_ROOT / "results/INDEX.md"
        original = target.read_bytes()
        text = original.decode("utf-8")
        assert "results/exp4_content.json" in text
        try:
            target.write_bytes(
                text.replace(
                    "| `results/exp4_content.json` |",
                    "| `results/exp4_content_removed.json` |",
                    1,
                ).encode("utf-8")
            )
            problems = check_results_index()
            assert any("exp4_content.json" in p for p in problems), problems
        finally:
            target.write_bytes(original)
        assert check_results_index() == []

    def test_a_document_naming_a_manifest_that_does_not_exist_is_caught(self) -> None:
        """The paper described the cells of a sweep that has never run, and
        named manifests that do not exist."""
        target = REPO_ROOT / "portfolio/RESULTS.md"
        original = target.read_bytes()
        text = original.decode("utf-8")
        try:
            target.write_bytes(
                (
                    text
                    + "\n<!-- manifest: results/phase_diagram_p113_nanda_wd10.json -->\n"
                ).encode("utf-8")
            )
            problems = check_referenced_manifests_exist()
            assert any("phase_diagram_p113_nanda_wd10.json" in p for p in problems), problems
        finally:
            target.write_bytes(original)
        assert check_referenced_manifests_exist() == []

    def test_naming_a_gitignored_derived_artifact_is_not_an_error(self) -> None:
        """The content-task verdict is deliberately gitignored: it is derived
        from the manifests, not evidence, and it is absent from a clean
        clone. A document that names it is describing the workflow, not
        claiming a manifest exists — and the audit must not fail a clean
        clone over it.

        (Found by the Docker gate on 2026-11-13: the check treated every
        `results/*.json` prose mention as a manifest, so the audit failed
        on any clone that had not run `make content-verdict`.)
        """
        # The exemption must come from .gitignore, not from the artifact
        # happening to be on this machine's disk.
        assert _is_gitignored("results/content_verdict.json"), (
            "the derived verdict is expected to be gitignored; if that "
            "changed, this exemption needs re-deciding"
        )
        problems = check_referenced_manifests_exist()
        assert not any("content_verdict.json" in p for p in problems), problems

    def test_a_document_that_stops_naming_its_manifest_is_caught(
        self, tmp_path: Path
    ) -> None:
        target = REPO_ROOT / "CONTEXT.md"
        original = target.read_bytes()
        try:
            # Drop one required tag and the audit has to notice.
            target.write_bytes(
                original.decode("utf-8")
                .replace("<!-- manifest: results/exp4_standard.json -->", "", 1)
                .encode("utf-8"),
            )
            problems = check_required_manifests()
            assert any("exp4_standard.json" in p for p in problems)
        finally:
            target.write_bytes(original)
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


class TestTheRung3TableIsManifestBacked:
    """Rung 3's phase-transition table was the one public table in the
    ledger with no manifest behind it (2026-11-11). The sweep now writes
    `results/exp3_superposition_sweep.json`, so the table is that
    manifest's numbers -- and the ratchet must police it."""

    def _rung3_section(self) -> str:
        text = (REPO_ROOT / "portfolio" / "RESULTS.md").read_text(encoding="utf-8")
        start = text.index("## Rung 3")
        return text[start : text.index("## Rung 4", start)]

    def test_the_section_cites_the_sweep_manifest(self) -> None:
        assert (
            "<!-- manifest: results/exp3_superposition_sweep.json -->"
            in self._rung3_section()
        ), "the Rung 3 table must name the manifest that produced it"

    def test_the_table_does_not_claim_to_have_no_manifest(self) -> None:
        """The 2026-11-11 exemption said 'no tracked manifest'. Now that one
        exists the declaration is false, and it would make the number check
        skip the very table it was written for."""
        assert "no tracked manifest" not in self._rung3_section(), (
            "the Rung 3 table still declares itself unbacked; the sweep "
            "manifest now exists, so the exemption is false and the number "
            "check is skipping this table"
        )

    def test_the_published_counts_are_the_manifests_counts(self) -> None:
        """The table must state the manifest's mean +- std per sparsity."""
        manifest = json.loads(
            (REPO_ROOT / "results" / "exp3_superposition_sweep.json").read_text(
                encoding="utf-8"
            )
        )
        section = self._rung3_section()
        for sparsity in (0.5, 0.2, 0.1, 0.05, 0.02, 0.01, 0.005, 0.002, 0.001):
            key = f"sparsity_{sparsity:g}".replace(".", "_")
            stats = manifest["aggregate"][f"{key}_n_represented"]
            row = f"| {sparsity:.3f} | {stats['mean']:.2f} ± {stats['std']:.2f} |"
            assert row in section, (
                f"the Rung 3 table does not carry the manifest's numbers for "
                f"sparsity {sparsity} (expected the row {row!r})"
            )

    def test_a_number_the_manifest_does_not_carry_is_caught(self) -> None:
        """The ratchet has to fire on the real file, not on a copy.

        The corrupted value is a non-integer on purpose: the audit's
        allowlist treats a bare integer as a *count* (3 seeds, 20 features)
        and skips it, so only a fractional value is actually compared
        against the manifest.

        The file is restored **byte for byte**: writing back the decoded
        text would rewrite the line endings, and a test run that leaves the
        tree dirty makes every manifest written afterwards claim
        `git_dirty: true` for a tree nobody changed.
        """
        target = REPO_ROOT / "portfolio" / "RESULTS.md"
        original = target.read_bytes()
        text = original.decode("utf-8")
        assert "| 0.100 | 17.67 ± 1.25 |" in text
        try:
            target.write_bytes(
                text.replace(
                    "| 0.100 | 17.67 ± 1.25 |", "| 0.100 | 11.67 ± 1.25 |", 1
                ).encode("utf-8")
            )
            problems = check_numbers_against_manifests()
            assert any("RESULTS.md" in p for p in problems), problems
        finally:
            target.write_bytes(original)
        assert check_numbers_against_manifests() == []


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
