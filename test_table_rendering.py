#!/usr/bin/env python3
"""
Test script to demonstrate the ASCII table rendering in CLI.
"""
from src.services.todo_service import TodoService
from src.cli.main import TodoCLI

def test_cli_table_rendering():
    """Test the CLI table rendering functionality."""
    print("Testing CLI ASCII Table Rendering...")
    print()

    # Create a service instance
    service = TodoService()

    # Add some test tasks
    task1 = service.add_task("Buy groceries")
    task2 = service.add_task("Complete the project")
    task3 = service.add_task("Walk the really long description that might need truncation")

    print("Tasks added successfully!")
    print(f"Task 1 ID: {task1.id}")
    print(f"Task 2 ID: {task2.id}")
    print(f"Task 3 ID: {task3.id}")
    print()

    # Create CLI instance with our service
    cli = TodoCLI()
    # Replace the CLI's service with our populated service
    cli.service = service

    print("Table rendering output:")
    print("-" * 50)
    cli._render_task_table(service.get_all_tasks())
    print("-" * 50)

    # Test completing a task
    print()
    print("Completing task 1...")
    service.complete_task(1)

    print("Updated table rendering:")
    print("-" * 50)
    cli._render_task_table(service.get_all_tasks())
    print("-" * 50)

if __name__ == "__main__":
    test_cli_table_rendering()