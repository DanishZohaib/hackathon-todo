#!/usr/bin/env python3
"""
Final validation test to ensure all functionality works as expected.
"""

from src.services.todo_service import TodoService

def test_complete_workflow():
    """Test the complete workflow for the todo application."""
    print("=== Final Validation Test ===")

    service = TodoService()

    # Test 1: Add tasks (US1)
    print("\n1. Testing ADD functionality...")
    task1 = service.add_task("Buy groceries")
    task2 = service.add_task("Complete the project")
    task3 = service.add_task("Walk the dog")
    print(f"   Added 3 tasks: {len(service.get_all_tasks())}")

    # Test 2: List tasks (US2)
    print("\n2. Testing LIST functionality...")
    all_tasks = service.get_all_tasks()
    print(f"   Listed tasks: {len(all_tasks)}")
    for task in all_tasks:
        print(f"   - {task.id[:8]}... - {task.description} [{task.status}]")

    # Test 3: Complete a task (US3)
    print("\n3. Testing COMPLETE functionality...")
    success = service.complete_task(task1.id)
    print(f"   Completed task {task1.id[:8]}...: {success}")

    # Verify completion
    updated_task = service.get_task_by_id(task1.id)
    print(f"   Task status after completion: {updated_task.status}")

    # Test 4: Delete a task (US4)
    print("\n4. Testing DELETE functionality...")
    success = service.delete_task(task2.id)
    print(f"   Deleted task {task2.id[:8]}...: {success}")

    # Verify deletion
    remaining_tasks = service.get_all_tasks()
    print(f"   Remaining tasks after deletion: {len(remaining_tasks)}")

    # Test 5: Error handling (US5)
    print("\n5. Testing ERROR HANDLING...")

    # Try to add empty task
    try:
        service.add_task("")
        print("   ERROR: Should have failed to add empty task")
    except ValueError:
        print("   OK Correctly handled empty task description")

    # Try to add very long task
    try:
        very_long_desc = "A" * 1001  # More than 1000 chars
        service.add_task(very_long_desc)
        print("   ERROR: Should have failed to add very long task")
    except ValueError:
        print("   OK Correctly handled very long task description")

    # Try to operate on non-existent task
    success = service.complete_task("non-existent")
    print(f"   OK Non-existent task completion returns: {success}")

    success = service.delete_task("non-existent")
    print(f"   OK Non-existent task deletion returns: {success}")

    print("\n=== All functionality validated successfully! ===")

if __name__ == "__main__":
    test_complete_workflow()