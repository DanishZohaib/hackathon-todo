#!/usr/bin/env python3
"""
Complete test to verify all TodoService functionality works correctly.
"""

from src.services.todo_service import TodoService

def test_full_functionality():
    """Test all functionality."""
    service = TodoService()

    print("=== Testing ADD functionality ===")
    # Add tasks
    task1 = service.add_task("Buy groceries")
    print(f"Added task: {task1.id} - {task1.description} [{task1.status}]")

    task2 = service.add_task("Complete project")
    print(f"Added task: {task2.id} - {task2.description} [{task2.status}]")

    print("\n=== Testing LIST functionality ===")
    all_tasks = service.get_all_tasks()
    print(f"Total tasks: {len(all_tasks)}")
    for task in all_tasks:
        print(f"  - {task.id} - {task.description} [{task.status}]")

    print("\n=== Testing COMPLETE functionality ===")
    # Complete the first task
    success = service.complete_task(task1.id)
    print(f"Completed task {task1.id}: {success}")

    # Check status after completion
    all_tasks = service.get_all_tasks()
    for task in all_tasks:
        print(f"  - {task.id} - {task.description} [{task.status}]")

    print("\n=== Testing DELETE functionality ===")
    # Delete the second task
    success = service.delete_task(task2.id)
    print(f"Deleted task {task2.id}: {success}")

    # Check remaining tasks
    all_tasks = service.get_all_tasks()
    print(f"Remaining tasks: {len(all_tasks)}")
    for task in all_tasks:
        print(f"  - {task.id} - {task.description} [{task.status}]")

    print("\n=== Testing edge cases ===")
    # Try to complete already completed task
    success = service.complete_task(task1.id)
    print(f"Try to complete already completed task: {success}")

    # Try to delete non-existent task
    success = service.delete_task("non-existent-id")
    print(f"Try to delete non-existent task: {success}")

    # Try to complete non-existent task
    success = service.complete_task("non-existent-id")
    print(f"Try to complete non-existent task: {success}")

if __name__ == "__main__":
    test_full_functionality()