#!/usr/bin/env python3
"""
Debug script to understand the task ID and storage behavior
"""

from src.services.todo_service import TodoService

def debug_storage():
    """Debug the storage behavior"""
    print("=== Debug: Single Service Instance ===")

    # Create a service instance
    service = TodoService()
    print(f"Initial next_id: {service._next_id}")

    # Add a task
    task1 = service.add_task("Test task 1")
    print(f"Added task with ID: {task1.id}")
    print(f"Current next_id: {service._next_id}")

    # Add another task
    task2 = service.add_task("Test task 2")
    print(f"Added task with ID: {task2.id}")
    print(f"Current next_id: {service._next_id}")

    # List all tasks
    all_tasks = service.get_all_tasks()
    print(f"Total tasks in service: {len(all_tasks)}")
    for task in all_tasks:
        print(f"  - ID: {task.id}, Description: {task.description}, Status: {task.status}")

    print("\n=== Creating NEW Service Instance ===")
    # Create a NEW service instance (simulating a new CLI command)
    new_service = TodoService()
    new_all_tasks = new_service.get_all_tasks()
    print(f"Total tasks in NEW service: {len(new_all_tasks)}")
    print("This shows why 'list' shows 'No tasks found' - it's a completely new in-memory store!")

if __name__ == "__main__":
    debug_storage()