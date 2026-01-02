#!/usr/bin/env python3
"""
Test to verify the error handling functionality works correctly.
"""

import sys
import os
import inspect
from src.services.todo_service import TodoService

def test_error_handling():
    """Test error handling functionality."""
    service = TodoService()

    print("=== Testing validation for empty task descriptions ===")
    try:
        service.add_task("")
        print("ERROR: Should have raised ValueError for empty description")
    except ValueError as e:
        print(f"OK Correctly caught error: {e}")

    try:
        service.add_task("   ")  # Just spaces
        print("ERROR: Should have raised ValueError for whitespace-only description")
    except ValueError as e:
        print(f"OK Correctly caught error: {e}")

    print("\n=== Testing invalid task ID handling ===")
    # Try to complete a non-existent task
    success = service.complete_task("non-existent-id")
    print(f"OK Complete non-existent task returns: {success}")

    # Try to delete a non-existent task
    success = service.delete_task("non-existent-id")
    print(f"OK Delete non-existent task returns: {success}")

    print("\n=== Testing task validation ===")
    # Test creating a task with invalid status
    try:
        from src.models.task import Task
        invalid_task = Task("123", "Test task", "invalid_status")
        print("ERROR: Should have raised ValueError for invalid status")
    except ValueError as e:
        print(f"OK Correctly caught error: {e}")

    # Test creating a task with empty description
    try:
        invalid_task = Task("123", "")
        print("ERROR: Should have raised ValueError for empty description")
    except ValueError as e:
        print(f"OK Correctly caught error: {e}")

    # Test creating a task with empty ID
    try:
        invalid_task = Task("", "Test task")
        print("ERROR: Should have raised ValueError for empty ID")
    except ValueError as e:
        print(f"OK Correctly caught error: {e}")

if __name__ == "__main__":
    test_error_handling()