# SPECTRA

### Digital Evidence Analyzer

SPECTRA is a Python-based, read-only digital evidence analysis toolkit designed for educational and forensic-learning use.

It analyzes files without modifying the original evidence and generates structured analysis reports. The current project focuses on a lightweight terminal-based workflow for hashing, metadata collection, signature detection, and basic text analysis.

## Features

- SHA-256 file hashing
- File metadata collection
- File signature detection
- Text analysis for supported text-based files
- Integrity verification using known hashes
- Structured report generation
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
├── reports/
└── requirements.txt
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
SPECTRA calculates the SHA-256 hash of the selected file.

### Metadata Collection
It reads basic file information such as:
- filename
- file path
- file size
- modified time
- created time
- accessed time
- file extension

### File Signature Detection
It detects common file types based on known magic numbers, including:
- PNG
- JPEG
- PDF
- ZIP

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

Generated reports are saved in the `reports/` directory as text files.

## Known Limitations

- The project currently uses a terminal interface only
- Deep analysis is focused on text-like files
- Binary files are identified by signature, but not deeply parsed
- Large files are limited for safety during text analysis

## Roadmap

Planned enhancements for future versions of SPECTRA include:

- multi-hash integrity checks
- file type mismatch detection
- printable string extraction
- entropy analysis
- JSON report export improvements
- stronger forensic classification for binary containers

## License

SPECTRA is open source and licensed under the MIT License.

See the [LICENSE](LICENSE) file for the full text.

## Future Improvements

Possible improvements include:
- GUI or web interface
- richer file classification
- better binary analysis
- export to HTML
- automated tests for more analysis scenarios
