import os

from hash_engine import calculate_sha256
from metadata import get_file_metadata
from analyzer import (
    analyze_text_file,
    verify_integrity,
    detect_file_signature
)
from report import create_report


TEXT_EXTENSIONS = (
    ".txt",
    ".log",
    ".py",
    ".c",
    ".cpp",
    ".h",
    ".html",
    ".css",
    ".js",
    ".json",
)


def analyze_file():
    filename = input("\nEnter evidence file path: ").strip()

    if not filename:
        print("\nError: No file path entered.")
        return

    try:
        print("\nAnalyzing evidence...")

        file_hash = calculate_sha256(filename)
        metadata = get_file_metadata(filename)
        file_type = detect_file_signature(filename)

        analysis = None

        if filename.lower().endswith(TEXT_EXTENSIONS):
            analysis = analyze_text_file(filename)

        print("\n================================")
        print("       ANALYSIS RESULT")
        print("================================")

        print(f"File: {metadata['name']}")
        print(f"Size: {metadata['size']} bytes")
        print(f"Type: {file_type}")
        print(f"SHA-256: {file_hash}")

        if analysis:
            print("\n--- TEXT ANALYSIS ---")
            print(f"Lines: {analysis['lines']}")
            print(f"Words: {analysis['words']}")
            print(f"Characters: {analysis['characters']}")
            print(f"Empty lines: {analysis['empty_lines']}")

        known_hash = input(
            "\nEnter known SHA-256 hash "
            "(or press Enter to skip): "
        ).strip()

        if known_hash:
            if verify_integrity(file_hash, known_hash):
                print("\n INTEGRITY MATCH")
            else:
                print("\n HASH MISMATCH")

        report_file = create_report(
            filename,
            file_hash,
            metadata,
            file_type,
            analysis
        )

        print(f"\n✓ Report created: {report_file}")

    except FileNotFoundError:
        print("\nError: Evidence file not found.")

    except PermissionError:
        print("\nError: Permission denied.")

    except UnicodeDecodeError:
        print("\nError: File could not be read as text.")

    except OSError as error:
        print(f"\nError accessing file: {error}")

    except Exception as error:
        print(f"\nUnexpected error: {error}")


def verify_file_integrity():
    filename = input("\nEnter evidence file path: ").strip()

    if not filename:
        print("\nError: No file path entered.")
        return

    known_hash = input("Enter known SHA-256 hash: ").strip()

    if not known_hash:
        print("\nError: No hash entered.")
        return

    try:
        current_hash = calculate_sha256(filename)

        print("\n================================")
        print("      INTEGRITY VERIFICATION")
        print("================================")

        print(f"\nCurrent SHA-256:\n{current_hash}")
        print(f"\nKnown SHA-256:\n{known_hash}")

        if verify_integrity(current_hash, known_hash):
            print("\n INTEGRITY MATCH")
            print("The calculated hash matches the known hash.")
        else:
            print("\n HASH MISMATCH")
            print("The calculated hash does not match the known hash.")

    except FileNotFoundError:
        print("\nError: Evidence file not found.")

    except PermissionError:
        print("\nError: Permission denied.")

    except OSError as error:
        print(f"\nError accessing file: {error}")


def view_reports():
    reports_folder = "reports"

    if not os.path.exists(reports_folder):
        print("\nNo reports folder found.")
        return

    reports = [
        file
        for file in os.listdir(reports_folder)
        if file.endswith(".txt")
    ]

    if not reports:
        print("\nNo reports available.")
        return

    reports.sort()

    print("\n================================")
    print("        SPECTRA REPORTS")
    print("================================")

    for number, report in enumerate(reports, start=1):
        print(f"[{number}] {report}")

    choice = input(
        "\nEnter report number "
        "(or press Enter to return): "
    ).strip()

    if not choice:
        return

    try:
        selected = reports[int(choice) - 1]

    except (ValueError, IndexError):
        print("\nInvalid report selection.")
        return

    report_path = os.path.join(reports_folder, selected)

    try:
        print("\n================================")
        print("             REPORT")
        print("================================\n")

        with open(report_path, "r", encoding="utf-8") as file:
            print(file.read())

    except OSError as error:
        print(f"\nError reading report: {error}")


def show_banner():
    print("\n")
    print("╔══════════════════════════════════════╗")
    print("║             SPECTRA v1.0             ║")
    print("║        DIGITAL EVIDENCE ANALYZER     ║")
    print("╚══════════════════════════════════════╝")


def main():
    while True:
        show_banner()

        print("\n[1] Analyze Evidence")
        print("[2] Verify Integrity")
        print("[3] View Reports")
        print("[4] Exit")

        choice = input("\nSelect option: ").strip()

        if choice == "1":
            analyze_file()

        elif choice == "2":
            verify_file_integrity()

        elif choice == "3":
            view_reports()

        elif choice == "4":
            print("\nSPECTRA shutting down.")
            break

        else:
            print("\nInvalid option. Please select 1-4.")


if __name__ == "__main__":
    main()