#!/usr/bin/env python3
"""
Cairo0 Rustlings

A tool to help you learn Cairo0 by working through small exercises.
"""

import argparse
import os
import platform
import signal
import subprocess
import sys
import time
from enum import Enum
from pathlib import Path
from typing import Optional

import toml
from tabulate import tabulate


# ANSI color codes for terminal output
class Colors:
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


# Exercise status
class ExerciseStatus(Enum):
    PENDING = "pending"
    DONE = "done"


# Global state
EXERCISE_ORDER = []
EXERCISE_HINTS = {}
CURRENT_EXERCISE_INDEX = 0
EXERCISE_STATUS = {}
WATCH_MODE = True
MANUAL_RUN = False


def clear_screen():
    """Clear the terminal screen based on OS"""
    os.system("cls" if platform.system() == "Windows" else "clear")


def print_header():
    """Print the Cairo0 Rustlings header"""
    clear_screen()
    print(f"{Colors.BOLD}{Colors.BLUE}Cairo0 Rustlings{Colors.ENDC}")
    print(f"{Colors.CYAN}Learn Cairo0 by solving exercises!{Colors.ENDC}")
    print("-----------------------------------------------")


def load_exercise_data():
    """Load exercise order and hints from TOML file"""
    global EXERCISE_ORDER, EXERCISE_HINTS, EXERCISE_STATUS

    # Load order and hints from TOML file
    try:
        data = toml.load("exercise_order.toml")
        EXERCISE_ORDER = data.get("exercises", {}).get("order", [])
        EXERCISE_HINTS = data.get("hints", {})
    except Exception as e:
        print(f"{Colors.RED}Error loading exercise order: {e}{Colors.ENDC}")
        sys.exit(1)

    # Initialize exercise status
    for exercise in EXERCISE_ORDER:
        EXERCISE_STATUS[exercise] = ExerciseStatus.PENDING


def is_exercise_done(exercise_path: str) -> bool:
    """Check if the I AM NOT DONE marker is removed from the file"""
    cairo_file = Path("exercises") / f"{exercise_path}.cairo"

    if not cairo_file.exists():
        return False

    content = cairo_file.read_text()
    return "I AM NOT DONE" not in content


def update_exercise_status():
    """Update the status of all exercises"""
    global EXERCISE_STATUS

    for exercise in EXERCISE_ORDER:
        if is_exercise_done(exercise):
            EXERCISE_STATUS[exercise] = ExerciseStatus.DONE
        else:
            EXERCISE_STATUS[exercise] = ExerciseStatus.PENDING


def get_next_pending_exercise() -> Optional[str]:
    """Get the next pending exercise in the list"""
    for exercise in EXERCISE_ORDER:
        if EXERCISE_STATUS[exercise] == ExerciseStatus.PENDING:
            return exercise
    return None


def run_exercise_test(exercise_path: str) -> bool:
    """Run the test for a specific exercise using pytest"""
    test_path = Path("exercises") / f"{exercise_path}.py"

    if not test_path.exists():
        print(f"{Colors.RED}Error: Test file not found: {test_path}{Colors.ENDC}")
        return False

    print(f"{Colors.BLUE}Running test for {exercise_path}...{Colors.ENDC}")

    try:
        # Run pytest with uv
        result = subprocess.run(
            ["uv", "run", "pytest", str(test_path), "-v"],
            capture_output=True,
            text=True,
        )

        # Print the output
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr)

        # Check if the test passed
        return result.returncode == 0
    except Exception as e:
        print(f"{Colors.RED}Error running test: {e}{Colors.ENDC}")
        return False


def get_exercise_hint(exercise_path: str) -> str:
    """Get hint for the current exercise"""
    exercise_name = exercise_path.split("/")[-1]
    hint = EXERCISE_HINTS.get(exercise_name, "No hint available for this exercise.")
    return hint


def display_exercise_status(exercise_path: str):
    """Display the current status of the exercise"""
    cairo_file = Path("exercises") / f"{exercise_path}.cairo"
    test_file = Path("exercises") / f"{exercise_path}.py"

    print(f"\n{Colors.BOLD}Current exercise: {Colors.BLUE}{exercise_path}{Colors.ENDC}")

    if not cairo_file.exists():
        print(f"{Colors.RED}Error: Cairo file not found: {cairo_file}{Colors.ENDC}")
        return

    if not test_file.exists():
        print(f"{Colors.RED}Error: Test file not found: {test_file}{Colors.ENDC}")
        return

    # Show file status
    status = EXERCISE_STATUS[exercise_path]
    status_color = Colors.GREEN if status == ExerciseStatus.DONE else Colors.YELLOW
    print(f"Status: {status_color}{status.value}{Colors.ENDC}")

    # Run the test if the file is marked as done
    if status == ExerciseStatus.DONE:
        if run_exercise_test(exercise_path):
            print(f"{Colors.GREEN}Exercise completed successfully!{Colors.ENDC}")
        else:
            print(f"{Colors.RED}Exercise test failed.{Colors.ENDC}")
    else:
        # Display the exercise content
        content = cairo_file.read_text()
        print("\nExercise file content:")
        print(f"{Colors.CYAN}{'=' * 50}{Colors.ENDC}")
        print(content)
        print(f"{Colors.CYAN}{'=' * 50}{Colors.ENDC}")

        # Show hint
        print(f"\n{Colors.BOLD}Hint:{Colors.ENDC} {get_exercise_hint(exercise_path)}")


def watch_exercise_file(exercise_path: str):
    """Watch for changes in the exercise file"""
    global MANUAL_RUN
    cairo_file = Path("exercises") / f"{exercise_path}.cairo"
    last_modified = cairo_file.stat().st_mtime if cairo_file.exists() else 0

    while WATCH_MODE:
        if not cairo_file.exists():
            print(f"{Colors.RED}Error: File not found: {cairo_file}{Colors.ENDC}")
            time.sleep(1)
            continue

        current_modified = cairo_file.stat().st_mtime

        if current_modified > last_modified or MANUAL_RUN:
            clear_screen()
            print_header()

            # Check if the exercise is now marked as done
            if is_exercise_done(exercise_path):
                EXERCISE_STATUS[exercise_path] = ExerciseStatus.DONE

            display_exercise_status(exercise_path)

            if EXERCISE_STATUS[exercise_path] == ExerciseStatus.DONE:
                # If this exercise is done and all tests pass, check if there are more exercises
                if run_exercise_test(exercise_path):
                    next_exercise = get_next_pending_exercise()
                    if next_exercise:
                        print(
                            f"\n{Colors.GREEN}Great job! Moving to the next exercise: {next_exercise}{Colors.ENDC}"
                        )
                        time.sleep(2)
                        return next_exercise
                    else:
                        print(
                            f"\n{Colors.GREEN}Congratulations! You've completed all exercises!{Colors.ENDC}"
                        )
                        return None

            last_modified = current_modified
            if MANUAL_RUN:
                MANUAL_RUN = False

        # Process keyboard commands
        if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            cmd = sys.stdin.readline().strip()
            if cmd == "q":
                return None  # Exit watch mode
            elif cmd == "h":
                print(
                    f"\n{Colors.BOLD}Hint:{Colors.ENDC} {get_exercise_hint(exercise_path)}"
                )
            elif cmd == "r":
                MANUAL_RUN = True
            elif cmd == "l":
                show_exercise_list()

        time.sleep(0.5)

    return None


def show_exercise_list():
    """Show an interactive list of all exercises"""
    global CURRENT_EXERCISE_INDEX

    update_exercise_status()

    while True:
        clear_screen()
        print_header()

        # Create a table of exercises
        table_data = []
        for i, exercise in enumerate(EXERCISE_ORDER):
            status = EXERCISE_STATUS[exercise]
            status_str = "✓" if status == ExerciseStatus.DONE else " "
            current = ">" if i == CURRENT_EXERCISE_INDEX else " "
            table_data.append([current, f"{i+1}", status_str, exercise])

        # Print the table
        print(
            tabulate(
                table_data, headers=["", "#", "Done", "Exercise"], tablefmt="simple"
            )
        )

        print("\nCommands:")
        print("  c: Continue selected exercise")
        print("  p/n: Previous/Next exercise")
        print("  r: Reset exercise status")
        print("  q: Return to watch mode")

        # Get user input
        key = input("\nEnter command: ").strip().lower()

        if key == "c":
            return EXERCISE_ORDER[CURRENT_EXERCISE_INDEX]
        elif key == "p" and CURRENT_EXERCISE_INDEX > 0:
            CURRENT_EXERCISE_INDEX -= 1
        elif key == "n" and CURRENT_EXERCISE_INDEX < len(EXERCISE_ORDER) - 1:
            CURRENT_EXERCISE_INDEX += 1
        elif key == "r":
            # Reset the selected exercise
            exercise = EXERCISE_ORDER[CURRENT_EXERCISE_INDEX]
            cairo_file = Path("exercises") / f"{exercise}.cairo"

            if cairo_file.exists():
                content = cairo_file.read_text()
                if "I AM NOT DONE" not in content:
                    # Find the comment line index
                    lines = content.split("\n")
                    for i, line in enumerate(lines):
                        if line.strip().startswith(
                            "//"
                        ) and not line.strip().startswith("// I AM NOT DONE"):
                            lines.insert(i, "// I AM NOT DONE")
                            break

                    # Write the modified content back
                    cairo_file.write_text("\n".join(lines))
                    EXERCISE_STATUS[exercise] = ExerciseStatus.PENDING
        elif key == "q":
            break

    return EXERCISE_ORDER[CURRENT_EXERCISE_INDEX]


def run_watch_mode():
    """Run the watch mode, monitoring files and running tests"""
    global CURRENT_EXERCISE_INDEX, WATCH_MODE

    print_header()
    print(f"{Colors.CYAN}Watch mode enabled. Press Ctrl+C to exit.{Colors.ENDC}")
    print("Commands: h (hint), r (run test), l (list exercises), q (quit)")

    # Set up signal handler for Ctrl+C
    def signal_handler(sig, frame):
        global WATCH_MODE
        WATCH_MODE = False
        print(f"\n{Colors.YELLOW}Exiting watch mode...{Colors.ENDC}")
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    # Find the first pending exercise
    current_exercise = get_next_pending_exercise()
    if not current_exercise:
        print(f"{Colors.GREEN}All exercises are completed!{Colors.ENDC}")
        return

    # Set the current exercise index
    CURRENT_EXERCISE_INDEX = EXERCISE_ORDER.index(current_exercise)

    # Start watching for changes
    while WATCH_MODE and current_exercise:
        display_exercise_status(current_exercise)
        next_exercise = watch_exercise_file(current_exercise)

        if next_exercise:
            current_exercise = next_exercise
            CURRENT_EXERCISE_INDEX = EXERCISE_ORDER.index(current_exercise)
        else:
            break


def init_command():
    """Initialize the environment by creating necessary files"""
    # Create exercise_order.toml if it doesn't exist
    if not Path("exercise_order.toml").exists():
        print(f"{Colors.YELLOW}Creating exercise_order.toml...{Colors.ENDC}")
        # We've already created this in our script, so we'll just print a message here

    print(f"{Colors.GREEN}Cairo0 Rustlings initialized successfully!{Colors.ENDC}")
    print(
        f"Run '{Colors.BOLD}uv run python cairo0_rustlings.py{Colors.ENDC}' to start the exercises."
    )


def main():
    """Main entry point"""
    global WATCH_MODE, MANUAL_RUN

    parser = argparse.ArgumentParser(
        description="Cairo0 Rustlings - Learn Cairo by solving exercises"
    )
    parser.add_argument(
        "command",
        nargs="?",
        default="watch",
        choices=["watch", "init", "list"],
        help="Command to run (watch, init, list)",
    )
    parser.add_argument(
        "--manual-run",
        action="store_true",
        help="Manually run tests (don't watch for file changes)",
    )

    args = parser.parse_args()

    # Import select only if we're in watch mode
    if args.command == "watch":
        global select
        import select

    if args.manual_run:
        MANUAL_RUN = True

    if args.command == "init":
        init_command()
        return

    # Load exercise data
    load_exercise_data()
    update_exercise_status()

    if args.command == "list":
        show_exercise_list()
        return

    # Run watch mode
    run_watch_mode()


if __name__ == "__main__":
    main()
