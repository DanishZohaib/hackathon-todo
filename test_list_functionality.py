#!/usr/bin/env python3
"""
Test to verify the list functionality works correctly.
"""

from src.services.todo_service import TodoService

def test_list_functionality():
    """Test list functionality."""
    service = TodoService()

    # Add some tasks
    task1 = service.add_task("Buy groceries")
    task2 = service.add_task("Complete project")
    service.complete_task(task1.id)  # Complete one task

    print("=== Testing LIST functionality ===")
    all_tasks = service.get_all_tasks()
    print(f"Total tasks: {len(all_tasks)}")

    if not all_tasks:
        print("No tasks found")
    else:
        print(f"{'ID':<36} {'Status':<10} {'Description'}")
        print("-" * 80)
        for task in all_tasks:
            status = "COMPLETED" if task.status == "complete" else "PENDING"
            print(f"{task.id:<36} {status:<10} {task.description}")

    print("\n=== Testing with no tasks ===")
    # Create a new service with no tasks
    empty_service = TodoService()
    empty_tasks = empty_service.get_all_tasks()
    if not empty_tasks:
        print("No tasks found")

if __name__ == "__main__":
    test_list_functionality()