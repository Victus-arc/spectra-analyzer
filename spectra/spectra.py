import os
import re

from hash_engine import calculate_hashes, calculate_sha256
from metadata import get_file_metadata
from analyzer import (
    analyze_text_file,
    calculate_entropy,
    detect_file_signature,
    detect_file_type_mismatch,
    extract_strings,
    verify_integrity,
)
from report import create_report


VERSION = "1.0"

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

GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
WHITE = "\033[97m"
GRAY = "\033[90m"
RESET = "\033[0m"
BOLD = "\033[1m"


def validate_file_path(filename):
    if not filename:
        return False, "No file path entered."
    if "\x00" in filename:
        return False, "File path contains invalid null bytes."

    safe_path = os.path.abspath(os.path.expanduser(filename))
    try:
        real_path = os.path.realpath(safe_path)
    except Exception:
        return False, "Invalid file path."

    if not os.path.exists(real_path):
        return False, "File does not exist."
    if not os.path.isfile(real_path):
        return False, "Path is not a file (it may be a directory or special file)."
    if not os.access(real_path, os.R_OK):
        return False, "File is not readable."

    return True, real_path


def validate_sha256_hash(hash_string):
    return bool(re.fullmatch(r"[A-Fa-f0-9]{64}", hash_string))


def clear_screen():
    print("\033[2J\033[H", end="")


def print_line():
    print(f"{GRAY}────────────────────────────────────────────────────────────{RESET}")


def complete(message):
    print(f"{GREEN}[✓] {message}{RESET}")


def warning(message):
    print(f"{YELLOW}[!] {message}{RESET}")


def error(message):
    print(f"{RED}[-] {message}{RESET}")


def info(message):
    print(f"{CYAN}[*] {message}{RESET}")


def show_banner():
    print(f"{GREEN}{BOLD}" + r"""
  ███████╗██████╗ ███████╗ ██████╗████████╗██████╗  █████╗
  ██╔════╝██╔══██╗██╔════╝██╔════╝╚══██╔══╝██╔══██╗██╔══██╗
  ███████╗██████╔╝█████╗  ██║        ██║   ██████╔╝███████║
  ╚════██║██╔═══╝ ██╔══╝  ██║        ██║   ██╔══██╗██╔══██║
  ███████║██║     ███████╗╚██████╗   ██║   ██║  ██║██║  ██║
  ╚══════╝╚═╝     ╚══════╝ ╚═════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝
  """ + f"{RESET}")
    print(f"{GREEN}                 DIGITAL EVIDENCE ANALYZER{RESET}")
    print(f"{GRAY}                         VERSION {VERSION}{RESET}")
    print()


def show_status():
    print(f"{GRAY}┌──────────────────────────────────────────────────────────┐{RESET}")
    print(f"{GRAY}│{RESET} {GREEN}SYSTEM{RESET} : SPECTRA        {GRAY}│{RESET} {GREEN}MODE{RESET} : READ-ONLY")
    print(f"{GRAY}│{RESET} {GREEN}ENGINE{RESET} : Evidence Analysis  {GRAY}│{RESET} {GREEN}STATUS{RESET} : READY")
    print(f"{GRAY}└──────────────────────────────────────────────────────────┘{RESET}")
    print()


def analyze_file():
    clear_screen()
    print_line()
    print(f"{BOLD}{CYAN}                    EVIDENCE ANALYSIS{RESET}")
    print_line(); print()

    filename = input(f"{GREEN}spectra > {RESET}Enter evidence file path: ").strip()
    is_valid, validated_path = validate_file_path(filename)
    if not is_valid:
        error(validated_path)
        input("\nPress Enter to return...")
        return
    filename = validated_path

    try:
        print(); info("Reading evidence file...")

        file_hash = calculate_sha256(filename)
        file_hashes = calculate_hashes(filename)
        complete("SHA-256 and multi-hash checks calculated.")

        metadata = get_file_metadata(filename)
        complete("Metadata collected.")

        file_type = detect_file_signature(filename)
        complete("File signature detected.")

        mismatch_detected, mismatch_reason = detect_file_type_mismatch(filename)
        if mismatch_detected:
            warning(f"Possible file type mismatch: {mismatch_reason}")

        analysis = None
        if filename.lower().endswith(TEXT_EXTENSIONS):
            info("Running text analysis...")
            analysis = analyze_text_file(filename)
            complete("Text analysis completed.")

        print(); print_line()
        print(f"{BOLD}{WHITE}                    ANALYSIS RESULT{RESET}")
        print_line(); print()

        print(f"{CYAN}File       :{RESET} {metadata['name']}")
        print(f"{CYAN}Size       :{RESET} {metadata['size']} bytes")
        print(f"{CYAN}Type       :{RESET} {file_type}")
        print(f"{CYAN}Modified   :{RESET} {metadata['modified']}")
        print()

        print(f"{BOLD}{CYAN}--- SHA-256 ---{RESET}")
        print(file_hash)

        print(); print(f"{BOLD}{CYAN}--- MULTI-HASH INTEGRITY ---{RESET}")
        print(f"MD5      : {file_hashes['MD5']}")
        print(f"SHA-1    : {file_hashes['SHA-1']}")
        print(f"SHA-256  : {file_hashes['SHA-256']}")
        print(f"BLAKE2b  : {file_hashes['BLAKE2b']}")

        if analysis:
            print(); print(f"{BOLD}{CYAN}--- TEXT ANALYSIS ---{RESET}")
            print(f"Lines       : {analysis['lines']}")
            print(f"Words       : {analysis['words']}")
            print(f"Characters  : {analysis['characters']}")
            print(f"Empty lines : {analysis['empty_lines']}")

        entropy_value = calculate_entropy(filename)
        printable_strings = extract_strings(filename, min_length=4, max_strings=25)

        print(); print(f"{BOLD}{CYAN}--- FORENSIC SIGNALS ---{RESET}")
        print(f"Entropy    : {entropy_value:.4f}")
        print(f"String hits: {len(printable_strings)} printable strings found")

        print(); print_line()

        known_hash = input(f"{GREEN}spectra > {RESET}Known SHA-256 hash (press Enter to skip): ").strip()
        if known_hash:
            if not validate_sha256_hash(known_hash):
                error("Invalid SHA-256 hash format (must be 64 hex characters).")
            else:
                print()
                if verify_integrity(file_hash, known_hash):
                    complete("INTEGRITY MATCH")
                else:
                    warning("HASH MISMATCH")

        print()
        report_file = create_report(filename, file_hash, metadata, file_type, analysis)
        complete(f"Report created: {report_file}")
        print(); print_line()

    except FileNotFoundError:
        error("Evidence file not found.")
    except PermissionError:
        error("Permission denied.")
    except UnicodeDecodeError:
        error("File could not be read as text.")
    except ValueError as err:
        error(str(err))
    except OSError as err:
        error(f"Error accessing file: {err}")
    except Exception as err:
        error(f"Unexpected error: {err}")

    input("\nPress Enter to return...")


def verify_file_integrity():
    clear_screen(); print_line(); print(f"{BOLD}{CYAN}                  INTEGRITY VERIFICATION{RESET}"); print_line(); print()

    filename = input(f"{GREEN}spectra > {RESET}Evidence file path: ").strip()
    is_valid, validated_path = validate_file_path(filename)
    if not is_valid:
        error(validated_path); input("\nPress Enter to return..."); return
    filename = validated_path

    known_hash = input(f"{GREEN}spectra > {RESET}Known SHA-256 hash: ").strip()
    if not known_hash:
        error("No hash entered."); input("\nPress Enter to return..."); return
    if not validate_sha256_hash(known_hash):
        error("Invalid SHA-256 hash format (must be 64 hex characters).")
        input("\nPress Enter to return..."); return

    try:
        print(); info("Calculating current SHA-256...")
        current_hash = calculate_sha256(filename)
        complete("Hash calculated.")

        print(); print_line(); print(f"{BOLD}{WHITE}                  INTEGRITY RESULT{RESET}"); print_line(); print()
        print(f"{CYAN}Current SHA-256:{RESET}"); print(current_hash)
        print(); print(f"{CYAN}Known SHA-256:{RESET}"); print(known_hash)
        print()

        if verify_integrity(current_hash, known_hash):
            complete("INTEGRITY MATCH")
        else:
            warning("HASH MISMATCH")

        hashes = calculate_hashes(filename)
        print(); print(f"{BOLD}{CYAN}MULTI-HASH CHECKS{RESET}")
        print(f"MD5     : {hashes['MD5']}")
        print(f"SHA-1   : {hashes['SHA-1']}")
        print(f"SHA-256 : {hashes['SHA-256']}")
        print(f"BLAKE2b : {hashes['BLAKE2b']}")

        print(); print_line()
    except FileNotFoundError:
        error("Evidence file not found.")
    except PermissionError:
        error("Permission denied.")
    except OSError as err:
        error(f"Error accessing file: {err}")

    input("\nPress Enter to return...")


def view_reports():
    clear_screen(); print_line(); print(f"{BOLD}{CYAN}                     SPECTRA REPORTS{RESET}"); print_line(); print()

    reports_folder = os.path.abspath("reports")
    if not os.path.exists(reports_folder):
        warning("No reports folder found.")
        input("\nPress Enter to return...")
        return

    reports = [file for file in os.listdir(reports_folder) if file.endswith(".txt")]
    if not reports:
        warning("No reports available.")
        input("\nPress Enter to return...")
        return

    reports.sort()
    for number, report in enumerate(reports, start=1):
        print(f"{GREEN}[{number}]{RESET} {report}")

    print()
    choice = input(f"{GREEN}spectra > {RESET}Select report number (Enter to return): ").strip()
    if not choice:
        return

    try:
        selected = reports[int(choice) - 1]
    except (ValueError, IndexError):
        error("Invalid report selection.")
        input("\nPress Enter to return...")
        return

    report_path = os.path.join(reports_folder, selected)
    try:
        clear_screen(); print_line(); print(f"{BOLD}{CYAN}                         REPORT{RESET}"); print_line(); print()
        with open(report_path, "r", encoding="utf-8") as file:
            print(file.read())
    except OSError as err:
        error(f"Error reading report: {err}")

    input("\nPress Enter to return...")


def show_menu():
    print_line(); print(f"{BOLD}{WHITE}                     SPECTRA MENU{RESET}"); print_line(); print()
    print(f"{GREEN}[1]{RESET} Analyze Evidence")
    print(f"{GREEN}[2]{RESET} Verify Integrity")
    print(f"{GREEN}[3]{RESET} View Reports")
    print(f"{GREEN}[4]{RESET} About SPECTRA")
    print(f"{RED}[Q]{RESET} Exit")
    print()


def show_about():
    clear_screen(); print_line(); print(f"{BOLD}{CYAN}                      ABOUT SPECTRA{RESET}"); print_line(); print()
    print("SPECTRA is a Python-based, read-only digital evidence")
    print("analysis toolkit designed for educational purposes.")
    print()
    print(f"{CYAN}Version      :{RESET} {VERSION}")
    print(f"{CYAN}Language     :{RESET} Python")
    print(f"{CYAN}Hashing      :{RESET} SHA-256 + multi-hash")
    print(f"{CYAN}Mode         :{RESET} Read-only")
    print(f"{CYAN}Interface    :{RESET} Terminal")
    print(); print(f"{GREEN}[✓] No original evidence is modified.{RESET}"); print(); print_line(); input("\nPress Enter to return...")


def main():
    while True:
        clear_screen(); show_banner(); show_status(); show_menu()
        choice = input(f"{GREEN}spectra > {RESET}").strip().lower()

        if choice == "1":
            analyze_file()
        elif choice == "2":
            verify_file_integrity()
        elif choice == "3":
            view_reports()
        elif choice == "4":
            show_about()
        elif choice == "q":
            clear_screen(); show_banner(); print(f"{GREEN}[+] SPECTRA shutting down.{RESET}"); print(); break
        else:
            warning("Invalid option. Select 1-4 or Q.")
            input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
