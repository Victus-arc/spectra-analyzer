# SPECTRA

### Digital Evidence Analyzer

SPECTRA is a Python-based, read-only digital evidence analysis toolkit designed for educational and forensic-learning use.

It analyzes files without modifying the original evidence and generates structured analysis reports. The project currently uses a terminal-based CLI interface.

## Features

- SHA-256 file hashing
- Multi-hash integrity checks (MD5, SHA-1, SHA-256, BLAKE2b)
- File metadata collection
- File signature detection
- File type mismatch detection
- Text analysis for supported text-based files
- Printable string extraction
- Entropy analysis
- Integrity verification using known hashes
- Structured report generation
- JSON report export
- Read-only evidence workflow

## Requirements

- Python 3.x
- Git (optional, for cloning the repository)

## Project Structure

```text
spectra-analyzer/
├── spectra/
│   ├── analyzer.py
│   ├── hash_engine.py
│   ├── metadata.py
│   ├── report.py
│   ├── spectra.py
│   └── evidence.txt
├── tests/
│   └── test_safety.py
├── README.md
├── LICENSE
├── .gitignore
└── reports/
```

## Installation

Clone the repository:

```bash
git clone https://github.com/Victus-arc/spectra-analyzer.git
cd spectra-analyzer
```

## Usage

Run the CLI:

```bash
python spectra/spectra.py
```

From the menu, you can:

1. Analyze Evidence
2. Verify Integrity
3. View Reports
4. About SPECTRA

## What SPECTRA Checks

### File Hashing
SPECTRA calculates the SHA-256 hash of the selected file and can also generate MD5, SHA-1, and BLAKE2b values.

### Metadata Collection
It reads basic file information such as:
- filename
- file path
- file size
- created time
- modified time
- accessed time
- file extension

### File Signature Detection
It detects common file types based on known magic numbers, including:
- PNG
- JPEG
- PDF
- ZIP

### File Type Mismatch Detection
It compares the file extension against the detected file signature to flag suspicious mismatches.

### Strings Extraction
It extracts printable ASCII strings from the file to help identify embedded text or markers.

### Entropy Analysis
It measures file randomness to help identify compressed, encrypted, or highly structured data.

### Text Analysis
For supported text-based files, it calculates:
- total lines
- total words
- total characters
- empty line count

### Integrity Verification
You can compare a file's current SHA-256 value against a known-good hash.

## Safety Notes

This tool is designed to be read-only and safe by default. The code includes validation to help reduce common misuse:

- invalid file paths are rejected
- non-file paths are rejected
- unreadable files are rejected
- malformed SHA-256 values are rejected
- oversized text files are prevented from causing excessive memory usage

## Report Output

Generated reports are saved in the `reports/` directory as text or JSON files.

## Known Limitations

- The project currently uses a terminal interface only
- Deep analysis is focused on text-like files
- Binary files are identified by signature, but not deeply parsed
- Large files are limited for safety during text analysis

## License

SPECTRA is open source and licensed under the MIT License.

See the [LICENSE](LICENSE) file for the full text.

## Future Improvements

Planned or possible improvements include:
- GUI or web interface
- richer file classification
- better binary analysis
- export to HTML
- automated tests for more analysis scenarios
