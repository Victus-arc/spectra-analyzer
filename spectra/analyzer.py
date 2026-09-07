def analyze_text_file(filename):
    with open(filename, "r", encoding="utf-8", errors="replace") as file:
        text = file.read()

    lines = text.splitlines()
    words = text.split()

    return {
        "lines": len(lines),
        "words": len(words),
        "characters": len(text),
        "empty_lines": sum(1 for line in lines if not line.strip()),
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