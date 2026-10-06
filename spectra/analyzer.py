import os

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
