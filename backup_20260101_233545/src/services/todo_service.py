"""
Todo service for managing tasks in memory.
Implements CRUD operations for tasks with in-memory storage.
"""

import uuid
from typing import List, Optional, Dict, Any
from src.models.task import Task


class TodoService:
    """
    Service class for managing todo tasks in memory.
    Provides CRUD operations and maintains the in-memory task store.
    """

    def __init__(self):
        """Initialize the in-memory task store."""
        self._tasks: Dict[str, Task] = {}

    def add_task(self, description: str) -> Task:
        """
        Add a new task with the given description.

        Args:
            description: The task description

        Returns:
            The created Task object with a unique ID

        Raises:
            ValueError: If description is empty or too long
        """
        if not description or not description.strip():
            raise ValueError("Task description cannot be empty")

        # Validate description length (max 1000 characters as per data model)
        if len(description) > 1000:
            raise ValueError("Task description exceeds maximum length of 1000 characters")

        # Generate a unique ID for the task
        task_id = str(uuid.uuid4())

        # Create and store the new task
        task = Task(id=task_id, description=description.strip())
        self._tasks[task_id] = task

        return task

    def get_all_tasks(self) -> List[Task]:
        """
        Get all tasks in the system.

        Returns:
            List of all tasks
        """
        return list(self._tasks.values())

    def get_task_by_id(self, task_id: str) -> Optional[Task]:
        """
        Get a specific task by its ID.

        Args:
            task_id: The ID of the task to retrieve

        Returns:
            The task if found, None otherwise
        """
        return self._tasks.get(task_id)

    def complete_task(self, task_id: str) -> bool:
        """
        Mark a task as complete.

        Args:
            task_id: The ID of the task to complete

        Returns:
            True if the task was found and updated, False otherwise
        """
        task = self._tasks.get(task_id)
        if task:
            task.complete()
            return True
        return False

    def delete_task(self, task_id: str) -> bool:
        """
        Delete a task by its ID.

        Args:
            task_id: The ID of the task to delete

        Returns:
            True if the task was found and deleted, False otherwise
        """
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def update_task_description(self, task_id: str, description: str) -> bool:
        """
        Update the description of an existing task.

        Args:
            task_id: The ID of the task to update
            description: The new description for the task

        Returns:
            True if the task was found and updated, False otherwise
        """
        task = self._tasks.get(task_id)
        if task and description and description.strip():
            # Validate description length (max 1000 characters as per data model)
            if len(description) > 1000:
                raise ValueError("Task description exceeds maximum length of 1000 characters")
            task.description = description.strip()
            return True
        return False