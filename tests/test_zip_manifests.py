"""The manifest zip helper: the bug was a shell quoting one, so pin the fix.

The remote notebooks used ``!zip ... $manifests``. IPython expands the list to
its repr, so no archive was written and a Colab session lost its manifests.
These tests keep the replacement honest: basenames, no missing files, no
duplicate names, and append semantics that cannot shadow an earlier entry.
"""

from __future__ import annotations

import zipfile
from pathlib import Path

import pytest

from scripts.zip_manifests import (
    append_to_zip,
    main,
    write_manifest_zip,
)


def _manifest(tmp_path: Path, name: str, text: str = "{}") -> Path:
    path = tmp_path / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def test_writes_basenames_and_round_trips(tmp_path: Path) -> None:
    first = _manifest(tmp_path, "a.json", '{"a": 1}')
    second = _manifest(tmp_path, "b.json", '{"b": 2}')

    archive = write_manifest_zip([first, second], tmp_path / "out.zip")

    with zipfile.ZipFile(archive) as bundle:
        assert sorted(bundle.namelist()) == ["a.json", "b.json"]
        assert bundle.read("a.json") == b'{"a": 1}'


def test_rejects_an_empty_file_list(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="no files"):
        write_manifest_zip([], tmp_path / "out.zip")


def test_rejects_a_missing_file(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError, match="missing file"):
        write_manifest_zip([tmp_path / "absent.json"], tmp_path / "out.zip")


def test_rejects_duplicate_basenames(tmp_path: Path) -> None:
    first = _manifest(tmp_path / "one", "same.json")
    second = _manifest(tmp_path / "two", "same.json")
    with pytest.raises(ValueError, match="same basename"):
        write_manifest_zip([first, second], tmp_path / "out.zip")


def test_append_adds_without_shadowing(tmp_path: Path) -> None:
    first = _manifest(tmp_path, "a.json", "{}")
    verdict = _manifest(tmp_path, "content_verdict.json", '{"status": "OK"}')
    archive = write_manifest_zip([first], tmp_path / "out.zip")

    append_to_zip([verdict], archive)

    with zipfile.ZipFile(archive) as bundle:
        assert sorted(bundle.namelist()) == ["a.json", "content_verdict.json"]
        assert bundle.read("content_verdict.json") == b'{"status": "OK"}'


def test_append_refuses_a_name_already_in_the_archive(tmp_path: Path) -> None:
    first = _manifest(tmp_path, "a.json", "{}")
    archive = write_manifest_zip([first], tmp_path / "out.zip")
    with pytest.raises(ValueError, match="already in"):
        append_to_zip([first], archive)


def test_append_creates_the_archive_when_absent(tmp_path: Path) -> None:
    first = _manifest(tmp_path, "a.json", "{}")
    archive = append_to_zip([first], tmp_path / "new.zip")
    with zipfile.ZipFile(archive) as bundle:
        assert bundle.namelist() == ["a.json"]


def test_cli_writes_the_archive(tmp_path: Path) -> None:
    first = _manifest(tmp_path, "a.json", "{}")
    output = tmp_path / "cli.zip"
    assert main(["--output", str(output), str(first)]) == 0
    assert output.is_file()
