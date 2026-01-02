#!/usr/bin/env python3
"""
Demo script to show the complete functionality of the Todo CLI application.
"""

from src.services.todo_service import TodoService

def demo_functionality():
    """Demonstrate all the functionality of the Todo application."""
    print("=== Todo CLI Application - Phase I Demo ===\n")

    # Create a service instance
    service = TodoService()

    print("1. ADDING TASKS:")
    print("-" * 20)
    task1 = service.add_task("Buy groceries")
    print(f"OK Added: {task1.description} (ID: {task1.id})")

    task2 = service.add_task("Complete the project")
    print(f"OK Added: {task2.description} (ID: {task2.id})")

    task3 = service.add_task("Walk the dog")
    print(f"OK Added: {task3.description} (ID: {task3.id})")

    print(f"\nTotal tasks added: {len(service.get_all_tasks())}")

    print("\n2. LISTING ALL TASKS:")
    print("-" * 25)
    all_tasks = service.get_all_tasks()
    print(f"{'ID':<10} {'Status':<10} {'Description'}")
    print("-" * 50)
    for task in all_tasks:
        status = "PENDING" if task.status == "incomplete" else "COMPLETED"
        print(f"{task.id:<10} {status:<10} {task.description}")

    print("\n3. COMPLETING A TASK:")
    print("-" * 25)
    success = service.complete_task(task1.id)
    print(f"OK Completed task {task1.id}: {success}")

    # Show updated status
    updated_task = service.get_task_by_id(task1.id)
    status = "PENDING" if updated_task.status == "incomplete" else "COMPLETED"
    print(f"OK Updated status: {status}")

    print("\n4. LISTING TASKS AFTER COMPLETION:")
    print("-" * 35)
    print(f"{'ID':<10} {'Status':<10} {'Description'}")
    print("-" * 50)
    for task in service.get_all_tasks():
        status = "PENDING" if task.status == "incomplete" else "COMPLETED"
        print(f"{task.id:<10} {status:<10} {task.description}")

    print("\n5. DELETING A TASK:")
    print("-" * 20)
    success = service.delete_task(task2.id)
    print(f"OK Deleted task {task2.id}: {success}")

    print("\n6. LISTING TASKS AFTER DELETION:")
    print("-" * 35)
    remaining_tasks = service.get_all_tasks()
    if remaining_tasks:
        print(f"{'ID':<10} {'Status':<10} {'Description'}")
        print("-" * 50)
        for task in remaining_tasks:
            status = "PENDING" if task.status == "incomplete" else "COMPLETED"
            print(f"{task.id:<10} {status:<10} {task.description}")
    else:
        print("No tasks found")

    print(f"\nRemaining tasks: {len(remaining_tasks)}")

    print("\n7. ERROR HANDLING:")
    print("-" * 20)

    # Test error handling for empty description
    try:
        service.add_task("")
    except ValueError as e:
        print(f"OK Empty description error: {e}")

    # Test error handling for non-existent task
    success = service.complete_task(999)  # Use a high integer that doesn't exist
    print(f"OK Non-existent task completion: {success}")

    success = service.delete_task(999)  # Use a high integer that doesn't exist
    print(f"OK Non-existent task deletion: {success}")

    print("\n=== Demo completed successfully! ===")
    print("\nThis demonstrates the complete functionality of the Todo CLI application:")
    print("- Add tasks with unique IDs")
    print("- List all tasks with status")
    print("- Complete tasks")
    print("- Delete tasks")
    print("- Comprehensive error handling")

if __name__ == "__main__":
    demo_functionality()