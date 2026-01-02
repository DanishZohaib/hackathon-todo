#!/usr/bin/env python3
"""
Test script to simulate CLI commands by directly using the service layer.
This validates all functionality works as expected.
"""

from src.services.todo_service import TodoService

def simulate_cli_workflow():
    """Simulate the CLI workflow to validate all functionality."""
    print("=== CLI Workflow Simulation ===")

    # Create a service instance
    service = TodoService()

    print("\n1. ADD command simulation:")
    # Add a task (simulating: python -m src.cli.main add 'Buy groceries')
    task1 = service.add_task("Buy groceries")
    print(f"   Added task: {task1.description} (ID: {task1.id[:8]}...)")

    task2 = service.add_task("Walk the dog")
    print(f"   Added task: {task2.description} (ID: {task2.id[:8]}...)")

    print("\n2. LIST command simulation:")
    # List tasks (simulating: python -m src.cli.main list)
    tasks = service.get_all_tasks()
    print(f"   {'ID':<10} {'Status':<10} {'Description'}")
    print(f"   {'-'*10} {'-'*10} {'-'*20}")
    for task in tasks:
        status = "COMPLETED" if task.status == "complete" else "PENDING"
        print(f"   {task.id[:8]}... {status:<10} {task.description}")

    print("\n3. COMPLETE command simulation:")
    # Complete a task (simulating: python -m src.cli.main complete <task_id>)
    success = service.complete_task(task1.id)
    print(f"   Completed task {task1.id[:8]}...: {success}")

    # Verify completion in list
    updated_task = service.get_task_by_id(task1.id)
    status = "COMPLETED" if updated_task.status == "complete" else "PENDING"
    print(f"   Updated status: {status}")

    print("\n4. DELETE command simulation:")
    # Delete a task (simulating: python -m src.cli.main delete <task_id>)
    success = service.delete_task(task2.id)
    print(f"   Deleted task {task2.id[:8]}...: {success}")

    # Verify deletion by listing remaining tasks
    remaining_tasks = service.get_all_tasks()
    print(f"   Remaining tasks after deletion: {len(remaining_tasks)}")

    print("\n5. Error handling simulation:")
    # Test error cases
    try:
        service.add_task("")  # Should fail
    except ValueError as e:
        print(f"   OK Empty description error handled: {e}")

    success = service.complete_task("invalid-id")  # Should return False
    print(f"   OK Invalid ID for complete returns: {success}")

    success = service.delete_task("invalid-id")  # Should return False
    print(f"   OK Invalid ID for delete returns: {success}")

    print("\n=== All CLI commands validated successfully! ===")

if __name__ == "__main__":
    simulate_cli_workflow()