#!/usr/bin/env python3
"""
Test to verify the delete task functionality works correctly.
"""

from src.services.todo_service import TodoService

def test_delete_functionality():
    """Test delete functionality."""
    service = TodoService()

    # Add tasks
    task1 = service.add_task("Buy groceries")
    task2 = service.add_task("Complete project")
    print(f"Added tasks: {task1.id}, {task2.id}")

    # List all tasks before deletion
    all_tasks = service.get_all_tasks()
    print(f"Tasks before deletion: {len(all_tasks)}")

    # Delete one task
    success = service.delete_task(task1.id)
    print(f"Delete task result: {success}")

    # Check remaining tasks
    remaining_tasks = service.get_all_tasks()
    print(f"Remaining tasks after deletion: {len(remaining_tasks)}")
    for task in remaining_tasks:
        print(f"  - {task.id} - {task.description} [{task.status}]")

    # Try to delete the same task again
    success = service.delete_task(task1.id)
    print(f"Delete already deleted task result: {success}")

    # Try to delete a non-existent task
    success = service.delete_task("non-existent-id")
    print(f"Delete non-existent task result: {success}")

if __name__ == "__main__":
    test_delete_functionality()