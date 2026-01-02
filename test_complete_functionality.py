#!/usr/bin/env python3
"""
Test to verify the complete task functionality works correctly.
"""

from src.services.todo_service import TodoService

def test_complete_functionality():
    """Test complete functionality."""
    service = TodoService()

    # Add a task
    task = service.add_task("Buy groceries")
    print(f"Original task: {task.id} - {task.description} [{task.status}]")

    # Complete the task
    success = service.complete_task(task.id)
    print(f"Complete task result: {success}")

    # Check the task status after completion
    updated_task = service.get_task_by_id(task.id)
    print(f"Updated task: {updated_task.id} - {updated_task.description} [{updated_task.status}]")

    # Try to complete an already completed task
    success = service.complete_task(task.id)
    print(f"Complete already completed task result: {success}")

    # Try to complete a non-existent task
    success = service.complete_task("non-existent-id")
    print(f"Complete non-existent task result: {success}")

if __name__ == "__main__":
    test_complete_functionality()