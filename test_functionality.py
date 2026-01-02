#!/usr/bin/env python3
"""
Simple test to verify the TodoService functionality works correctly.
"""

from src.services.todo_service import TodoService

def test_add_tasks():
    """Test adding tasks functionality."""
    service = TodoService()

    # Test adding a task
    task1 = service.add_task("Buy groceries")
    print(f"Added task: {task1.id} - {task1.description} [{task1.status}]")

    # Test adding another task
    task2 = service.add_task("Complete project")
    print(f"Added task: {task2.id} - {task2.description} [{task2.status}]")

    # Verify both tasks exist
    all_tasks = service.get_all_tasks()
    print(f"Total tasks: {len(all_tasks)}")

    for task in all_tasks:
        print(f"  - {task.id} - {task.description} [{task.status}]")

if __name__ == "__main__":
    test_add_tasks()