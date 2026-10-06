import os
import tempfile
from pathlib import Path


def test_validate_file_path_accepts_real_file(tmp_path):
    file_path = tmp_path / "sample.txt"
    file_path.write_text("hello world", encoding="utf-8")

    ok, result = __import__("spectra.spectra", fromlist=["validate_file_path"]).validate_file_path(str(file_path))

    assert ok is True
    assert Path(result) == file_path.resolve()


def test_validate_file_path_rejects_missing_file(tmp_path):
    missing = tmp_path / "missing.txt"

    ok, result = __import__("spectra.spectra", fromlist=["validate_file_path"]).validate_file_path(str(missing))

    assert ok is False
    assert "does not exist" in result.lower()


def test_validate_file_path_rejects_directory(tmp_path):
    directory = tmp_path / "folder"
    directory.mkdir()

    ok, result = __import__("spectra.spectra", fromlist=["validate_file_path"]).validate_file_path(str(directory))

    assert ok is False
    assert "not a file" in result.lower()


def test_validate_sha256_hash_accepts_valid_hash():
    valid = "a" * 64
    assert __import__("spectra.spectra", fromlist=["validate_sha256_hash"]).validate_sha256_hash(valid) is True


def test_validate_sha256_hash_rejects_invalid_hash():
    invalid = "abc123"
    assert __import__("spectra.spectra", fromlist=["validate_sha256_hash"]).validate_sha256_hash(invalid) is False


def test_analyze_text_file_rejects_large_file(tmp_path):
    large_file = tmp_path / "large.txt"
    large_file.write_bytes(b"A" * (51 * 1024 * 1024))

    try:
        __import__("spectra.analyzer", fromlist=["analyze_text_file"]).analyze_text_file(str(large_file))
        assert False, "Expected ValueError for oversized text file"
    except ValueError as exc:
        assert "safe analysis limit" in str(exc).lower()
