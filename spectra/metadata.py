import math
import os
import re
from collections import Counter

MAX_TEXT_FILE_SIZE = 50 * 1024 * 1024  # 50 MB safety cap for text analysis


def analyze_text_file(filename):
    """Analyze a text file without loading the full file into memory."""
    file_size = os.path.getsize(filename)

    if file_size > MAX_TEXT_FILE_SIZE:
        raise ValueError(
            f"File exceeds the safe analysis limit of {MAX_TEXT_FILE_SIZE / (1024 * 1024):.0f} MB."
        )

    lines = 0
    words = 0
    characters = 0
    empty_lines = 0

    with open(filename, "r", encoding="utf-8", errors="replace") as file:
        for raw_line in file:
            lines += 1
            characters += len(raw_line)

            if not raw_line.strip():
                empty_lines += 1

            words += len(raw_line.split())

    return {
        "lines": lines,
        "words": words,
        "characters": characters,
        "empty_lines": empty_lines,
    }


def verify_integrity(current_hash, known_hash):
    return current_hash.lower() == known_hash.lower()


def detect_file_signature(filename):
    with open(filename, "rb") as file:
        header = file.read(16)

    signatures = {
        b"\x89PNG\r\n\x1a\n": "PNG image",
        b"\xff\xd8\xff": "JPEG image",
        b"%PDF": "PDF document",
        b"PK\x03\x04": "ZIP archive",
    }

    for signature, file_type in signatures.items():
        if header.startswith(signature):
            return file_type

    return "Unknown / plain-text file"


def detect_file_type_mismatch(filename):
    """Compare the file extension against the detected file signature."""
    _, extension = os.path.splitext(filename)
    extension = extension.lower()
    actual_type = detect_file_signature(filename)

    extension_map = {
        ".png": "PNG image",
        ".jpg": "JPEG image",
        ".jpeg": "JPEG image",
        ".pdf": "PDF document",
        ".zip": "ZIP archive",
        ".txt": "Unknown / plain-text file",
        ".md": "Unknown / plain-text file",
        ".log": "Unknown / plain-text file",
        ".py": "Unknown / plain-text file",
        ".json": "Unknown / plain-text file",
        ".csv": "Unknown / plain-text file",
        ".xml": "Unknown / plain-text file",
        ".html": "Unknown / plain-text file",
        ".css": "Unknown / plain-text file",
        ".js": "Unknown / plain-text file",
        ".c": "Unknown / plain-text file",
        ".cpp": "Unknown / plain-text file",
        ".h": "Unknown / plain-text file",
    }

    expected_type = extension_map.get(extension)

    if expected_type is None:
        return False, "No known extension mapping is available for this file type."

    if expected_type != actual_type:
        return (
            True,
            f"Extension '{extension}' suggests '{expected_type}', but the file signature identifies '{actual_type}'.",
        )

    return False, "No mismatch detected."


def extract_strings(filename, min_length=4, max_strings=None):
    """Extract printable ASCII strings from a file."""
    with open(filename, "rb") as file:
        data = file.read()

    if not data:
        return []

    pattern = rb"[\x20-\x7E]{%d,}" % min_length
    matches = re.findall(pattern, data)
    strings = [match.decode("ascii", "ignore") for match in matches]

    if max_strings is not None:
        strings = strings[:max_strings]

    return strings


def calculate_entropy_from_bytes(data):
    """Compute Shannon entropy for a byte string."""
    if not data:
        return 0.0

    counts = Counter(data)
    length = len(data)
    entropy = 0.0

    for count in counts.values():
        probability = count / length
        entropy -= probability * math.log2(probability)

    return entropy


def calculate_entropy(filename):
    """Return the entropy score for the contents of a file."""
    with open(filename, "rb") as file:
        return calculate_entropy_from_bytes(file.read())
