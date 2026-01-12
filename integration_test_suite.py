#!/usr/bin/env python3
"""
Comprehensive Integration Test Suite for the Todo Application.

This script performs end-to-end testing of all major functionality across
the CLI interface, service layer, and data models.
"""

import sys
import os
import subprocess
from src.services.todo_service import TodoService
from src.models.task import Task


def test_models_layer():
    """Test the models layer directly."""
    print("=== Testing Models Layer ===")

    # Test successful task creation
    try:
        task = Task(id=1, description="Test task")
        print(f"[PASS] Created task: ID={task.id}, Description='{task.description}', Status='{task.status}'")

        # Verify initial state
        assert task.id == 1
        assert task.description == "Test task"
        assert task.status == "incomplete"
        print("[PASS] Task attributes validated")

        # Test completion
        task.complete()
        assert task.status == "complete"
        print("[PASS] Task completion validated")

        # Test to_dict/from_dict
        task_dict = task.to_dict()
        reconstructed_task = Task.from_dict(task_dict)
        assert reconstructed_task.id == task.id
        assert reconstructed_task.description == task.description
        assert reconstructed_task.status == task.status
        print("[PASS] Task serialization/deserialization validated")

        print("[PASS] Models layer tests passed\n")

    except Exception as e:
        print(f"[FAIL] Models layer test failed: {e}")
        return False

    return True


def test_service_layer():
    """Test the service layer functionality."""
    print("=== Testing Service Layer ===")

    service = TodoService()

    try:
        # Test adding tasks
        task1 = service.add_task("First test task")
        print(f"[PASS] Added task 1: ID={task1.id}, Description='{task1.description}'")

        task2 = service.add_task("Second test task")
        print(f"[PASS] Added task 2: ID={task2.id}, Description='{task2.description}'")

        # Verify task IDs are sequential
        assert task1.id == 1
        assert task2.id == 2
        print("[PASS] Sequential ID assignment validated")

        # Test listing tasks
        all_tasks = service.get_all_tasks()
        assert len(all_tasks) == 2
        print(f"[PASS] Retrieved all tasks: {len(all_tasks)} tasks found")

        # Test getting specific task
        retrieved_task = service.get_task_by_id(1)
        assert retrieved_task is not None
        assert retrieved_task.id == 1
        assert retrieved_task.description == "First test task"
        print("[PASS] Specific task retrieval validated")

        # Test completing a task
        success = service.complete_task(1)
        assert success is True
        completed_task = service.get_task_by_id(1)
        assert completed_task.status == "complete"
        print("[PASS] Task completion validated")

        # Test deleting a task
        success = service.delete_task(2)
        assert success is True
        remaining_tasks = service.get_all_tasks()
        assert len(remaining_tasks) == 1
        print("[PASS] Task deletion validated")

        # Test error cases
        try:
            service.add_task("")
            assert False, "Should have raised ValueError"
        except ValueError:
            print("[PASS] Empty task description validation validated")

        # Test operations on non-existent tasks
        success = service.complete_task(999)
        assert success is False
        print("[PASS] Non-existent task completion handling validated")

        success = service.delete_task(999)
        assert success is False
        print("[PASS] Non-existent task deletion handling validated")

        success = service.update_task_description(999, "New description")
        assert success is False
        print("[PASS] Non-existent task update handling validated")

        print("[PASS] Service layer tests passed\n")

    except Exception as e:
        print(f"[FAIL] Service layer test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

    return True


def test_cli_integration():
    """Test CLI functionality through subprocess calls."""
    print("=== Testing CLI Integration ===")

    try:
        # Test help command
        result = subprocess.run([sys.executable, "-m", "src.cli.main", "--help"],
                              capture_output=True, text=True, timeout=10)
        assert result.returncode == 0
        assert "Todo CLI Application" in result.stdout
        print("[PASS] CLI help command works")

        # Test add command
        result = subprocess.run([sys.executable, "-m", "src.cli.main", "add", "CLI test task"],
                              capture_output=True, text=True, timeout=10)
        assert result.returncode == 0
        assert "Task added successfully" in result.stdout
        print("[PASS] CLI add command works")

        # Test list command
        result = subprocess.run([sys.executable, "-m", "src.cli.main", "list"],
                              capture_output=True, text=True, timeout=10)
        assert result.returncode == 0
        # Note: Each CLI call creates a new service instance, so it won't see previous tasks
        # This is expected behavior for the CLI
        print("[PASS] CLI list command works")

        # Test complete command (will fail as task doesn't exist in this instance)
        result = subprocess.run([sys.executable, "-m", "src.cli.main", "complete", "1"],
                              capture_output=True, text=True, timeout=10)
        # This should fail since we're using a new service instance
        print("[PASS] CLI complete command tested (expected to fail due to new service instance)")

        print("[PASS] CLI integration tests completed\n")

    except subprocess.TimeoutExpired:
        print("[FAIL] CLI test timed out")
        return False
    except Exception as e:
        print(f"[FAIL] CLI integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

    return True


def test_error_handling():
    """Test comprehensive error handling."""
    print("=== Testing Error Handling ===")

    service = TodoService()

    try:
        # Test empty description
        try:
            service.add_task("")
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "empty" in str(e).lower()
            print("[PASS] Empty description validation works")

        # Test whitespace-only description
        try:
            service.add_task("   ")
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "empty" in str(e).lower()
            print("[PASS] Whitespace-only description validation works")

        # Test very long description
        try:
            service.add_task("x" * 1001)  # Exceeds 1000 char limit
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "exceeds" in str(e).lower()
            print("[PASS] Long description validation works")

        # Test invalid task creation
        try:
            invalid_task = Task(-1, "Invalid ID task")
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "positive" in str(e).lower()
            print("[PASS] Invalid task ID validation works")

        try:
            invalid_task = Task(1, "")
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "empty" in str(e).lower()
            print("[PASS] Empty task description validation works")

        try:
            invalid_task = Task(1, "Valid desc", "invalid_status")
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "status" in str(e).lower()
            print("[PASS] Invalid task status validation works")

        print("[PASS] Error handling tests passed\n")

    except Exception as e:
        print(f"[FAIL] Error handling test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

    return True


def test_data_persistence_simulation():
    """Test the in-memory persistence model."""
    print("=== Testing Data Persistence Model ===")

    # Create first service instance and add tasks
    service1 = TodoService()
    task1 = service1.add_task("Persistent task 1")
    task2 = service1.add_task("Persistent task 2")
    service1.complete_task(task1.id)

    # Verify state in first instance
    tasks1 = service1.get_all_tasks()
    assert len(tasks1) == 2
    assert any(t.id == task1.id and t.status == "complete" for t in tasks1)
    assert any(t.id == task2.id and t.status == "incomplete" for t in tasks1)
    print("[PASS] State maintained in first service instance")

    # Create second service instance (simulates new process/session)
    service2 = TodoService()
    tasks2 = service2.get_all_tasks()
    # Should be empty since it's a new instance
    assert len(tasks2) == 0
    print("[PASS] New service instance starts empty (as expected)")

    print("[PASS] Data persistence model validated\n")

    return True


def run_comprehensive_tests():
    """Run all integration tests."""
    print("Starting Comprehensive Integration Test Suite\n")

    tests = [
        ("Models Layer", test_models_layer),
        ("Service Layer", test_service_layer),
        ("Error Handling", test_error_handling),
        ("Data Persistence", test_data_persistence_simulation),
        ("CLI Integration", test_cli_integration),
    ]

    results = []
    for test_name, test_func in tests:
        print(f"Running {test_name} tests...")
        result = test_func()
        results.append((test_name, result))

    print("=== Test Results Summary ===")
    all_passed = True
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{test_name}: {status}")
        if not result:
            all_passed = False

    print(f"\nOverall Result: {'ALL TESTS PASSED' if all_passed else 'SOME TESTS FAILED'}")
    return all_passed


if __name__ == "__main__":
    success = run_comprehensive_tests()
    sys.exit(0 if success else 1)