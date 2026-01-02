"""
Main CLI interface for the Todo application.
Handles command-line arguments and delegates to the appropriate service methods.
"""

import argparse
import sys
import os
import inspect
from typing import NoReturn

# Add the src directory to the path to import modules
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from src.services.todo_service import TodoService


class TodoCLI:
    """
    Command-line interface for the Todo application.
    Handles user input and output for all todo operations.
    """

    def __init__(self):
        """Initialize the CLI with a TodoService instance."""
        self.service = TodoService()

    def run(self) -> int:
        """
        Run the CLI application.

        Returns:
            Exit code (0 for success, non-zero for errors)
        """
        parser = argparse.ArgumentParser(
            description="Todo CLI Application - Manage your tasks from the command line"
        )
        subparsers = parser.add_subparsers(dest="command", help="Available commands")

        # Add command
        add_parser = subparsers.add_parser("add", help="Add a new task")
        add_parser.add_argument("description", nargs="*", help="Task description")

        # List command
        list_parser = subparsers.add_parser("list", help="List all tasks")

        # Complete command
        complete_parser = subparsers.add_parser("complete", help="Mark a task as complete")
        complete_parser.add_argument("task_id", help="ID of the task to complete")

        # Delete command
        delete_parser = subparsers.add_parser("delete", help="Delete a task")
        delete_parser.add_argument("task_id", help="ID of the task to delete")

        # Parse arguments
        args = parser.parse_args()

        # Handle commands
        try:
            if args.command == "add":
                return self.handle_add(args)
            elif args.command == "list":
                return self.handle_list()
            elif args.command == "complete":
                return self.handle_complete(args)
            elif args.command == "delete":
                return self.handle_delete(args)
            else:
                parser.print_help()
                return 1
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.", file=sys.stderr)
            return 1
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1

    def handle_add(self, args) -> int:
        """
        Handle the add command.

        Args:
            args: Parsed command-line arguments

        Returns:
            Exit code
        """
        if not args.description:
            print("Error: Task description cannot be empty", file=sys.stderr)
            return 1

        description = " ".join(args.description)
        try:
            task = self.service.add_task(description)
            print(f"Task added successfully with ID: {task.id}")
            return 0
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1

    def handle_list(self) -> int:
        """
        Handle the list command.

        Returns:
            Exit code
        """
        tasks = self.service.get_all_tasks()

        if not tasks:
            print("No tasks found")
            return 0

        print(f"{'ID':<36} {'Status':<10} {'Description'}")
        print("-" * 80)
        for task in tasks:
            status = "COMPLETED" if task.status == "complete" else "PENDING"
            print(f"{task.id:<36} {status:<10} {task.description}")
        return 0

    def handle_complete(self, args) -> int:
        """
        Handle the complete command.

        Args:
            args: Parsed command-line arguments

        Returns:
            Exit code
        """
        success = self.service.complete_task(args.task_id)
        if success:
            print(f"Task {args.task_id} marked as complete")
            return 0
        else:
            print(f"Error: Task with ID {args.task_id} not found", file=sys.stderr)
            return 1

    def handle_delete(self, args) -> int:
        """
        Handle the delete command.

        Args:
            args: Parsed command-line arguments

        Returns:
            Exit code
        """
        success = self.service.delete_task(args.task_id)
        if success:
            print(f"Task {args.task_id} deleted successfully")
            return 0
        else:
            print(f"Error: Task with ID {args.task_id} not found", file=sys.stderr)
            return 1


def main() -> NoReturn:
    """
    Main entry point for the application.
    """
    cli = TodoCLI()
    exit_code = cli.run()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()