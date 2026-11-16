"""Tests for the remote-run manifest pinner (fail-closed).

`pin_remote_run.py` is the gate between a GPU run's output and the repo's
cited record. It must refuse, not forgive: a manifest with a fabricated or
unverifiable provenance is worse than a missing one, because
`verify-claims` would treat it as evidence.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from scripts.pin_remote_run import validate_manifest

REPO_ROOT = Path(__file__).resolve().parents[1]


def _pinner_cmd(source: Path, results_dir: Path, *extra: str) -> list[str]:
    """The pinner's command line, always aimed at a throwaway results dir.

    Every test that shells out to the pinner installs into ``results_dir``
    (a tmp_path), never into the repository's own ``results/``. Two reasons:
    a test must never be able to overwrite the tracked record, and the
    pinner's refusal to overwrite a *different* file with the same name used
    to make the tests depend on what happens to be tracked in ``results/``
    (three of them failed on 2026-11-11, the day ``exp4_content.json``
    landed there).
    """
    return [
        sys.executable,
        str(REPO_ROOT / "scripts" / "pin_remote_run.py"),
        "--from",
        str(source),
        "--results-dir",
        str(results_dir),
        *extra,
    ]


def _head_sha() -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"], capture_output=True, text=True, cwd=REPO_ROOT
    ).stdout.strip()


def _write_manifest(path: Path, **overrides) -> Path:
    manifest = {
        "experiment": "induction_scale_large",
        "seeds": [0, 1, 2],
        "args": {"modulus": 113},
        "per_seed_metrics": [
            {"final_val_acc": 0.9},
            {"final_val_acc": 0.91},
            {"final_val_acc": 0.92},
        ],
        "aggregate": {
            "final_val_acc": {"mean": 0.91, "std": 0.01, "min": 0.9, "max": 0.92, "n": 3}
        },
        "wall_clock_seconds": 120.0,
        "git_sha": _head_sha(),
        "git_dirty": False,
        "device": "cuda",
        "torch_version": "2.x",
        "numpy_version": "2.x",
        "python_version": "3.12.x",
        "n_parameters": 1000,
        "created_at": "2026-10-13T00:00:00+00:00",
        "notes": None,
    }
    manifest.update(overrides)
    path.write_text(json.dumps(manifest), encoding="utf-8")
    return path


class TestValidateManifest:
    def test_valid_manifest_passes(self, tmp_path: Path) -> None:
        assert validate_manifest(_write_manifest(tmp_path / "ok.json")) == []

    def test_empty_aggregate_is_refused(self, tmp_path: Path) -> None:
        path = _write_manifest(tmp_path / "empty.json", aggregate={})
        problems = validate_manifest(path)
        assert any("empty aggregate" in p for p in problems)

    def test_seeds_must_match_per_seed_records(self, tmp_path: Path) -> None:
        path = _write_manifest(
            tmp_path / "mismatch.json",
            seeds=[0, 1, 2],
            per_seed_metrics=[{"final_val_acc": 0.9}],
        )
        problems = validate_manifest(path)
        assert any("per-seed records" in p for p in problems)

    def test_aggregate_n_must_match_seeds(self, tmp_path: Path) -> None:
        path = _write_manifest(
            tmp_path / "badn.json",
            aggregate={
                "final_val_acc": {"mean": 0.9, "std": 0.0, "min": 0.9, "max": 0.9, "n": 1}
            },
        )
        problems = validate_manifest(path)
        assert any("aggregate['final_val_acc']['n']=1" in p for p in problems)

    def test_dirty_tree_is_refused(self, tmp_path: Path) -> None:
        """A remote run clones a pinned ref, so git_dirty=true means the
        provenance is wrong — a local re-run stamped it, not the GPU run."""
        path = _write_manifest(tmp_path / "dirty.json", git_dirty=True)
        problems = validate_manifest(path)
        assert any("dirty working tree" in p for p in problems)

    def test_unknown_sha_is_refused(self, tmp_path: Path) -> None:
        path = _write_manifest(tmp_path / "ghost.json", git_sha="0" * 40)
        problems = validate_manifest(path)
        assert any("does not exist" in p for p in problems)

    def test_non_manifest_json_is_refused(self, tmp_path: Path) -> None:
        path = tmp_path / "garbage.json"
        path.write_text('{"hello": "world"}', encoding="utf-8")
        problems = validate_manifest(path)
        assert any("not a ResultsManifest" in p for p in problems)


class TestZipExpansion:
    """The notebooks ship manifests inside a zip (one archive for both
    runtimes), so a download directory usually holds no loose JSON at all."""

    def _zip_with_manifest(self, tmp_path: Path) -> Path:
        import zipfile

        src = tmp_path / "src"
        src.mkdir(parents=True, exist_ok=True)
        good = _write_manifest(src / "good.json")
        archive = tmp_path / "run.zip"
        with zipfile.ZipFile(archive, "w") as zf:
            zf.write(good, arcname="results/good.json")
        return archive

    def test_zip_is_expanded_and_validated(self, tmp_path: Path) -> None:
        from scripts.pin_remote_run import _expand_zips

        archive = self._zip_with_manifest(tmp_path)
        # The download directory holds the zip (and nothing else useful):
        # that is exactly what the driver's `kaggle kernels output` gives.
        candidates = _expand_zips(tmp_path)
        assert any(c.name == "good.json" for c in candidates)
        extracted = archive.with_suffix("") / "results" / "good.json"
        assert extracted.exists()
        assert validate_manifest(extracted) == []

    def test_dry_run_pins_from_a_zip(self, tmp_path: Path) -> None:
        self._zip_with_manifest(tmp_path)
        proc = subprocess.run(
            _pinner_cmd(tmp_path, tmp_path / "results", "--dry-run"),
            capture_output=True,
            text=True,
            cwd=REPO_ROOT,
            timeout=300,
        )
        assert proc.returncode == 0, proc.stdout + proc.stderr
        assert "DRY RUN OK" in proc.stdout
        assert not (REPO_ROOT / "results" / "good.json").exists()

    def test_dry_run_pins_from_the_zip_file_itself(self, tmp_path: Path) -> None:
        """`--from <path-to.zip>` is the natural thing an operator types after
        `kaggle kernels output` hands them one archive."""
        archive = self._zip_with_manifest(tmp_path)
        proc = subprocess.run(
            _pinner_cmd(archive, tmp_path / "results", "--dry-run"),
            capture_output=True,
            text=True,
            cwd=REPO_ROOT,
            timeout=300,
        )
        assert proc.returncode == 0, proc.stdout + proc.stderr
        assert "DRY RUN OK" in proc.stdout


class TestDryRunEntryPoint:
    def test_dry_run_installs_nothing(self, tmp_path: Path) -> None:
        src = _write_manifest(tmp_path / "good.json")
        proc = subprocess.run(
            _pinner_cmd(src, tmp_path / "results", "--dry-run"),
            capture_output=True,
            text=True,
            cwd=REPO_ROOT,
            timeout=300,
        )
        assert proc.returncode == 0, proc.stdout + proc.stderr
        assert "DRY RUN OK" in proc.stdout
        assert not (REPO_ROOT / "results" / "good.json").exists()

    def test_dry_run_reports_an_overwrite_instead_of_refusing(self, tmp_path: Path) -> None:
        """A rehearsal must not fail because the file it would install already
        exists with different content.

        The refusal to overwrite exists to protect the tracked record from a
        silent overwrite — and it is still the behaviour of a real install.
        But a dry run installs nothing, so refusing there made
        `make remote-pin --dry-run` unusable the moment a tracked manifest
        had the same name as the file being rehearsed (and it broke three
        tests of this suite on 2026-11-11, the day `exp4_content.json`
        landed in `results/`).
        """
        src = _write_manifest(tmp_path / "good.json")
        results = tmp_path / "results"
        results.mkdir()
        (results / "good.json").write_text('{"different": true}', encoding="utf-8")
        proc = subprocess.run(
            _pinner_cmd(src, results, "--dry-run"),
            capture_output=True,
            text=True,
            cwd=REPO_ROOT,
            timeout=300,
        )
        assert proc.returncode == 0, proc.stdout + proc.stderr
        assert "would overwrite good.json" in proc.stderr
        # …and nothing was installed.
        assert (results / "good.json").read_text(encoding="utf-8") == '{"different": true}'

    def test_a_real_install_refuses_to_overwrite(self, tmp_path: Path) -> None:
        """The refusal itself must survive the dry-run change."""
        src = _write_manifest(tmp_path / "good.json")
        results = tmp_path / "results"
        results.mkdir()
        (results / "good.json").write_text('{"different": true}', encoding="utf-8")
        proc = subprocess.run(
            _pinner_cmd(src, results),
            capture_output=True,
            text=True,
            cwd=REPO_ROOT,
            timeout=300,
        )
        assert proc.returncode != 0
        assert "refusing to overwrite" in proc.stderr

    def test_invalid_manifest_fails_closed(self, tmp_path: Path) -> None:
        bad = tmp_path / "bad.json"
        bad.write_text('{"nope": 1}', encoding="utf-8")
        proc = subprocess.run(
            [
                sys.executable,
                str(REPO_ROOT / "scripts" / "pin_remote_run.py"),
                "--from",
                str(bad),
                "--dry-run",
            ],
            capture_output=True,
            text=True,
            cwd=REPO_ROOT,
            timeout=300,
        )
        assert proc.returncode != 0
        assert "FAILED validation" in proc.stderr


class TestProfile:
    def _write_manifests(self, tmp_path: Path, names: list[str]) -> Path:
        src = tmp_path / "src"
        src.mkdir(parents=True)
        head = subprocess.run(
            ["git", "rev-parse", "HEAD"], capture_output=True, text=True, cwd=REPO_ROOT
        ).stdout.strip()
        for name in names:
            manifest = {
                "experiment": "induction_content",
                "seeds": [0, 1, 2],
                "args": {},
                "per_seed_metrics": [{"final_val_acc": 0.9}] * 3,
                "aggregate": {
                    "final_val_acc": {
                        "mean": 0.9,
                        "std": 0.0,
                        "min": 0.9,
                        "max": 0.9,
                        "n": 3,
                    }
                },
                "wall_clock_seconds": 120.0,
                "git_sha": head,
                "git_dirty": False,
                "device": "cuda",
                "torch_version": "2.x",
                "numpy_version": "2.x",
                "python_version": "3.12.x",
                "n_parameters": 1000,
                "created_at": "2026-10-13T00:00:00+00:00",
                "notes": None,
            }
            (src / name).write_text(
                json.dumps(manifest), encoding="utf-8"
            )
        return src

    def test_profile_pins_required_and_optional(self, tmp_path: Path) -> None:
        src = self._write_manifests(
            tmp_path, ["induction_content.json", "exp4_content.json", "exp5_content.json"]
        )
        proc = subprocess.run(
            _pinner_cmd(
                src, tmp_path / "results", "--profile", "induction-content", "--dry-run"
            ),
            capture_output=True,
            text=True,
            cwd=REPO_ROOT,
            timeout=300,
        )
        assert proc.returncode == 0, proc.stdout + proc.stderr
        assert "DRY RUN OK" in proc.stdout
        # Nothing installed in dry run.
        assert not (tmp_path / "results" / "induction_content.json").exists()

    def test_profile_induction_content_passes_with_exp1_only(self, tmp_path: Path) -> None:
        """exp4 è opzionale: un run negativo valido che salta exp4 è pinnabile."""
        src = self._write_manifests(
            tmp_path, ["induction_content.json"]  # exp4_content.json missing — OK
        )
        proc = subprocess.run(
            _pinner_cmd(
                src, tmp_path / "results", "--profile", "induction-content", "--dry-run"
            ),
            capture_output=True,
            text=True,
            cwd=REPO_ROOT,
            timeout=300,
        )
        assert proc.returncode == 0, proc.stdout + proc.stderr
        assert "DRY RUN OK" in proc.stdout
        assert "optional files not present, skipping" in proc.stderr
        assert "exp4_content.json" in proc.stderr
        assert "exp5_content.json" in proc.stderr

    def test_profile_skips_missing_optional(self, tmp_path: Path) -> None:
        src = self._write_manifests(
            tmp_path, ["induction_content.json", "exp4_content.json"]
        )  # exp5_content.json missing (optional)
        proc = subprocess.run(
            _pinner_cmd(
                src, tmp_path / "results", "--profile", "induction-content", "--dry-run"
            ),
            capture_output=True,
            text=True,
            cwd=REPO_ROOT,
            timeout=300,
        )
        assert proc.returncode == 0, proc.stdout + proc.stderr
        assert "optional files not present, skipping" in proc.stderr
        assert "exp5_content.json" in proc.stderr

    def test_profile_phase_diagram_requires_all_ten_cells(self, tmp_path: Path) -> None:
        """Il profilo phase-diagram richiede tutte e dieci le celle del sweep."""
        src = self._write_manifests(
            tmp_path,
            [
                "induction_content.json",  # estraneo al profilo: ignorato
            ]
            + [f"phase_diagram_{cid}.json" for cid in (
                "p113_nanda_wd10",
                "p113_minibatch_wd10",
                "p113_beta2_0999_wd10",
                "p113_cosine_wd10",
                "p113_renorm_wd10",
                "p113_layernorm_wd10",
                "p113_gradclip_1_wd10",
                "p113_nanda_wd01",
                "p113_nanda_wd05",
                # p113_nanda_wd20 mancante: deve fallire
            )],
        )
        proc = subprocess.run(
            _pinner_cmd(src, tmp_path / "results", "--profile", "phase-diagram", "--dry-run"),
            capture_output=True,
            text=True,
            cwd=REPO_ROOT,
            timeout=300,
        )
        assert proc.returncode != 0
        assert "required by --profile" in proc.stderr
        assert "phase_diagram_p113_nanda_wd20.json" in proc.stderr

    def test_profile_and_only_are_mutually_exclusive(self, tmp_path: Path) -> None:
        src = self._write_manifests(tmp_path, ["induction_content.json"])
        proc = subprocess.run(
            _pinner_cmd(
                src,
                tmp_path / "results",
                "--profile",
                "induction-content",
                "--only",
                "induction_content.json",
                "--dry-run",
            ),
            capture_output=True,
            text=True,
            cwd=REPO_ROOT,
            timeout=300,
        )
        assert proc.returncode != 0
        assert "mutually exclusive" in proc.stderr
