import os

from hash_engine import calculate_sha256
from metadata import get_file_metadata
from analyzer import (
    analyze_text_file,
    verify_integrity,
    detect_file_signature
)
from report import create_report


# ============================================================
# SPECTRA CONFIGURATION
# ============================================================

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


# ============================================================
# TERMINAL COLORS
# ============================================================

GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
WHITE = "\033[97m"
GRAY = "\033[90m"
RESET = "\033[0m"
BOLD = "\033[1m"


# ============================================================
# TERMINAL FUNCTIONS
# ============================================================

def clear_screen():
    print("\033[2J\033[H", end="")


def print_line():
    print(
        f"{GRAY}"
        "────────────────────────────────────────────────────────────"
        f"{RESET}"
    )


def success(message):
    print(f"{GREEN}[+] {message}{RESET}")


def complete(message):
    print(f"{GREEN}[✓] {message}{RESET}")


def warning(message):
    print(f"{YELLOW}[!] {message}{RESET}")


def error(message):
    print(f"{RED}[-] {message}{RESET}")


def info(message):
    print(f"{CYAN}[*] {message}{RESET}")


# ============================================================
# SPECTRA BANNER
# ============================================================

def show_banner():
    print(
        f"{GREEN}{BOLD}"
        r"""
 ███████╗██████╗ ███████╗ ██████╗████████╗██████╗  █████╗
 ██╔════╝██╔══██╗██╔════╝██╔════╝╚══██╔══╝██╔══██╗██╔══██╗
 ███████╗██████╔╝█████╗  ██║        ██║   ██████╔╝███████║
 ╚════██║██╔═══╝ ██╔══╝  ██║        ██║   ██╔══██╗██╔══██║
 ███████║██║     ███████╗╚██████╗   ██║   ██║  ██║██║  ██║
 ╚══════╝╚═╝     ╚══════╝ ╚═════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝
"""
        f"{RESET}"
    )

    print(
        f"{GREEN}"
        f"                 DIGITAL EVIDENCE ANALYZER"
        f"{RESET}"
    )

    print(
        f"{GRAY}"
        f"                         VERSION {VERSION}"
        f"{RESET}"
    )

    print()


# ============================================================
# STATUS PANEL
# ============================================================

def show_status():
    print(
        f"{GRAY}"
        "┌──────────────────────────────────────────────────────────┐"
        f"{RESET}"
    )

    print(
        f"{GRAY}│{RESET} "
        f"{GREEN}SYSTEM{RESET} : SPECTRA"
        f"        {GRAY}│{RESET} "
        f"{GREEN}MODE{RESET} : READ-ONLY"
    )

    print(
        f"{GRAY}│{RESET} "
        f"{GREEN}ENGINE{RESET} : Evidence Analysis"
        f"  {GRAY}│{RESET} "
        f"{GREEN}STATUS{RESET} : READY"
    )

    print(
        f"{GRAY}"
        "└──────────────────────────────────────────────────────────┘"
        f"{RESET}"
    )

    print()


# ============================================================
# ANALYZE EVIDENCE
# ============================================================

def analyze_file():

    clear_screen()

    print_line()

    print(
        f"{BOLD}{CYAN}"
        "                    EVIDENCE ANALYSIS"
        f"{RESET}"
    )

    print_line()
    print()

    filename = input(
        f"{GREEN}spectra > {RESET}"
        "Enter evidence file path: "
    ).strip()

    if not filename:
        error("No file path entered.")
        input("\nPress Enter to return...")
        return

    try:

        print()

        info("Reading evidence file...")

        file_hash = calculate_sha256(filename)

        complete("SHA-256 calculated.")

        metadata = get_file_metadata(filename)

        complete("Metadata collected.")

        file_type = detect_file_signature(filename)

        complete("File signature detected.")

        analysis = None

        if filename.lower().endswith(TEXT_EXTENSIONS):

            info("Running text analysis...")

            analysis = analyze_text_file(filename)

            complete("Text analysis completed.")

        print()

        print_line()

        print(
            f"{BOLD}{WHITE}"
            "                    ANALYSIS RESULT"
            f"{RESET}"
        )

        print_line()

        print()

        print(
            f"{CYAN}File       :{RESET} "
            f"{metadata['name']}"
        )

        print(
            f"{CYAN}Size       :{RESET} "
            f"{metadata['size']} bytes"
        )

        print(
            f"{CYAN}Type       :{RESET} "
            f"{file_type}"
        )

        print(
            f"{CYAN}Modified   :{RESET} "
            f"{metadata['modified']}"
        )

        print()

        print(
            f"{BOLD}{CYAN}"
            "--- SHA-256 ---"
            f"{RESET}"
        )

        print(file_hash)

        if analysis:

            print()

            print(
                f"{BOLD}{CYAN}"
                "--- TEXT ANALYSIS ---"
                f"{RESET}"
            )

            print(
                f"Lines       : {analysis['lines']}"
            )

            print(
                f"Words       : {analysis['words']}"
            )

            print(
                f"Characters  : {analysis['characters']}"
            )

            print(
                f"Empty lines : {analysis['empty_lines']}"
            )

        print()

        print_line()

        known_hash = input(
            f"{GREEN}spectra > {RESET}"
            "Known SHA-256 hash "
            "(press Enter to skip): "
        ).strip()

        if known_hash:

            print()

            if verify_integrity(
                file_hash,
                known_hash
            ):

                complete("INTEGRITY MATCH")

            else:

                warning("HASH MISMATCH")

        print()

        report_file = create_report(
            filename,
            file_hash,
            metadata,
            file_type,
            analysis
        )

        complete(
            f"Report created: {report_file}"
        )

        print()

        print_line()

    except FileNotFoundError:

        error("Evidence file not found.")

    except PermissionError:

        error("Permission denied.")

    except UnicodeDecodeError:

        error("File could not be read as text.")

    except OSError as err:

        error(f"Error accessing file: {err}")

    except Exception as err:

        error(f"Unexpected error: {err}")

    input("\nPress Enter to return...")


# ============================================================
# VERIFY INTEGRITY
# ============================================================

def verify_file_integrity():

    clear_screen()

    print_line()

    print(
        f"{BOLD}{CYAN}"
        "                  INTEGRITY VERIFICATION"
        f"{RESET}"
    )

    print_line()
    print()

    filename = input(
        f"{GREEN}spectra > {RESET}"
        "Evidence file path: "
    ).strip()

    if not filename:

        error("No file path entered.")
        input("\nPress Enter to return...")
        return

    known_hash = input(
        f"{GREEN}spectra > {RESET}"
        "Known SHA-256 hash: "
    ).strip()

    if not known_hash:

        error("No hash entered.")
        input("\nPress Enter to return...")
        return

    try:

        print()

        info("Calculating current SHA-256...")

        current_hash = calculate_sha256(filename)

        complete("Hash calculated.")

        print()

        print_line()

        print(
            f"{BOLD}{WHITE}"
            "                  INTEGRITY RESULT"
            f"{RESET}"
        )

        print_line()

        print()

        print(
            f"{CYAN}Current SHA-256:{RESET}"
        )

        print(current_hash)

        print()

        print(
            f"{CYAN}Known SHA-256:{RESET}"
        )

        print(known_hash)

        print()

        if verify_integrity(
            current_hash,
            known_hash
        ):

            complete("INTEGRITY MATCH")

        else:

            warning("HASH MISMATCH")

        print()

        print_line()

    except FileNotFoundError:

        error("Evidence file not found.")

    except PermissionError:

        error("Permission denied.")

    except OSError as err:

        error(f"Error accessing file: {err}")

    input("\nPress Enter to return...")


# ============================================================
# VIEW REPORTS
# ============================================================

def view_reports():

    clear_screen()

    print_line()

    print(
        f"{BOLD}{CYAN}"
        "                     SPECTRA REPORTS"
        f"{RESET}"
    )

    print_line()
    print()

    reports_folder = "reports"

    if not os.path.exists(reports_folder):

        warning("No reports folder found.")
        input("\nPress Enter to return...")
        return

    reports = [
        file
        for file in os.listdir(reports_folder)
        if file.endswith(".txt")
    ]

    if not reports:

        warning("No reports available.")
        input("\nPress Enter to return...")
        return

    reports.sort()

    for number, report in enumerate(
        reports,
        start=1
    ):

        print(
            f"{GREEN}[{number}]{RESET} "
            f"{report}"
        )

    print()

    choice = input(
        f"{GREEN}spectra > {RESET}"
        "Select report number "
        "(Enter to return): "
    ).strip()

    if not choice:
        return

    try:

        selected = reports[
            int(choice) - 1
        ]

    except (ValueError, IndexError):

        error("Invalid report selection.")
        input("\nPress Enter to return...")
        return

    report_path = os.path.join(
        reports_folder,
        selected
    )

    try:

        clear_screen()

        print_line()

        print(
            f"{BOLD}{CYAN}"
            "                         REPORT"
            f"{RESET}"
        )

        print_line()
        print()

        with open(
            report_path,
            "r",
            encoding="utf-8"
        ) as file:

            print(file.read())

    except OSError as err:

        error(f"Error reading report: {err}")

    input("\nPress Enter to return...")


# ============================================================
# MAIN MENU
# ============================================================

def show_menu():

    print_line()

    print(
        f"{BOLD}{WHITE}"
        "                     SPECTRA MENU"
        f"{RESET}"
    )

    print_line()

    print()

    print(
        f"{GREEN}[1]{RESET} "
        "Analyze Evidence"
    )

    print(
        f"{GREEN}[2]{RESET} "
        "Verify Integrity"
    )

    print(
        f"{GREEN}[3]{RESET} "
        "View Reports"
    )

    print(
        f"{GREEN}[4]{RESET} "
        "About SPECTRA"
    )

    print(
        f"{RED}[Q]{RESET} "
        "Exit"
    )

    print()


# ============================================================
# ABOUT SPECTRA
# ============================================================

def show_about():

    clear_screen()

    print_line()

    print(
        f"{BOLD}{CYAN}"
        "                      ABOUT SPECTRA"
        f"{RESET}"
    )

    print_line()

    print()

    print(
        "SPECTRA is a Python-based, "
        "read-only digital evidence"
    )

    print(
        "analysis toolkit designed for "
        "educational purposes."
    )

    print()

    print(
        f"{CYAN}Version      :{RESET} {VERSION}"
    )

    print(
        f"{CYAN}Language     :{RESET} Python"
    )

    print(
        f"{CYAN}Hashing      :{RESET} SHA-256"
    )

    print(
        f"{CYAN}Mode         :{RESET} Read-only"
    )

    print(
        f"{CYAN}Interface    :{RESET} Terminal"
    )

    print()

    print(
        f"{GREEN}[✓] No original evidence is modified."
        f"{RESET}"
    )

    print()

    print_line()

    input("\nPress Enter to return...")


# ============================================================
# MAIN PROGRAM
# ============================================================

def main():

    while True:

        clear_screen()

        # Banner is displayed ONLY here.
        show_banner()

        show_status()

        show_menu()

        choice = input(
            f"{GREEN}spectra > {RESET}"
        ).strip().lower()

        if choice == "1":

            analyze_file()

        elif choice == "2":

            verify_file_integrity()

        elif choice == "3":

            view_reports()

        elif choice == "4":

            show_about()

        elif choice == "q":

            clear_screen()

            show_banner()

            print(
                f"{GREEN}"
                "[+] SPECTRA shutting down."
                f"{RESET}"
            )

            print()

            break

        else:

            warning(
                "Invalid option. "
                "Select 1-4 or Q."
            )

            input("\nPress Enter to continue...")


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()
    