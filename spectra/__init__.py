"""SPECTRA package."""

from .analyzer import analyze_text_file, calculate_entropy, calculate_entropy_from_bytes, detect_file_signature, detect_file_type_mismatch, extract_strings, verify_integrity
from .hash_engine import calculate_blake2b, calculate_hashes, calculate_md5, calculate_sha1, calculate_sha256
from .metadata import get_file_metadata
from .report import create_json_report, create_report

__all__ = [
    "analyze_text_file",
    "calculate_entropy",
    "calculate_entropy_from_bytes",
    "detect_file_signature",
    "detect_file_type_mismatch",
    "extract_strings",
    "verify_integrity",
    "calculate_blake2b",
    "calculate_hashes",
    "calculate_md5",
    "calculate_sha1",
    "calculate_sha256",
    "get_file_metadata",
    "create_json_report",
    "create_report",
]
