"""
Main entry point for the CLI Todo Application with organizational features.
"""
import sys
import os
# Add the project root directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.services.task_manager import TaskManager
from src.ui.cli import CLIInterface


def main():
    """
    Main application loop with enhanced organizational features.
    """
    print("Welcome to the CLI Todo Application!")
    print("Enhanced with organizational features: priority, tags, due dates")
    print("Type 'help' for available commands or 'quit'/'exit' to exit.")

    task_manager = TaskManager()
    cli = CLIInterface(task_manager)

    # Show reminders on startup
    reminders_result = cli.show_reminders()
    if reminders_result and reminders_result != "✅ No upcoming or overdue tasks.":
        print("\n" + reminders_result)

    while True:
        try:
            command = input("\n> ").strip()
            if not command:
                continue

            result = cli.execute_command(command)

            if result == "quit":
                print("Goodbye!")
                break

            print(result)

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except EOFError:
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    main()