# SPECTRA
### Digital Evidence Analyzer

SPECTRA is a Python-based digital forensics and file analysis toolkit designed for educational and forensic-learning purposes.

It provides a lightweight, read-only workflow for examining files, collecting metadata, detecting file signatures, calculating cryptographic hashes, and generating structured analysis reports.

## Features

- **SHA-256 Hashing** — Calculate cryptographic hashes for file integrity checks.
- **Metadata Collection** — Extract basic file information, including size, timestamps, filename, and extension.
- **File Signature Detection** — Identify common file types using file signatures (magic numbers).
- **Text Analysis** — Analyze supported text files for lines, words, characters, and empty lines.
- **Integrity Verification** — Compare calculated hashes against known values.
- **Report Generation** — Generate structured text-based analysis reports.
- **Read-Only Workflow** — Analyze original evidence without intentionally modifying its contents.

## Technology Stack

- Python
- Standard Python libraries
- Git and GitHub

## Installation

Clone the repository:

```bash
git clone https://github.com/Victus-arc/spectra-analyzer.git
cd spectra-analyzer
```

Check your Python installation:

```bash
python --version
```

## Usage

Run SPECTRA from the project root:

```bash
python spectra/spectra.py
```

Follow the terminal menu to access the available options:

1. Analyze Evidence
2. Verify Integrity
3. View Reports
4. About SPECTRA

## Analysis Capabilities

### 1. File Hashing
Calculates SHA-256 hashes to support file integrity verification.

### 2. Metadata Collection
Collects basic file attributes, including:
- Filename
- File path
- File size
- Modified time
- Created time
- Accessed time
- File extension

### 3. File Signature Detection
Identifies supported file types using known signatures, including PNG, JPEG, PDF, and ZIP.

### 4. Text Analysis
Provides basic statistics for supported text-based files:
- Total lines
- Total words
- Total characters
- Empty line count

### 5. Integrity Verification
Compares a file's current SHA-256 hash against a known-good hash.

## Safety Considerations

SPECTRA is designed around a read-only analysis workflow.

Current validation includes:
- Rejecting invalid file paths.
- Rejecting directory paths where a file is expected.
- Handling unreadable files.
- Validating SHA-256 input.
- Applying size limits to text analysis.

Always work with authorized files and preserve original evidence.

## Known Limitations

- Currently uses a command-line interface.
- Deep analysis is focused on supported text-based files.
- Binary files are identified by signature but are not deeply parsed.
- Large text files are subject to analysis limits.

## Roadmap

Potential future development includes:

- Multi-hash integrity verification.
- File type mismatch detection.
- Printable string extraction.
- Entropy analysis.
- Improved JSON and HTML report exports.
- Stronger binary file classification.
- Expanded automated test coverage.
- GUI interface.

## Testing

SPECTRA includes automated tests.

Run the test suite from the project root:

```bash
python -m pytest
```

*Note: Install pytest separately if it is not already available.*

## License

SPECTRA is distributed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Author

Developed as an independent learning project focused on Python programming and digital forensics.
