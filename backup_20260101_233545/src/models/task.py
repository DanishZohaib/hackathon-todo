"""
Task model for the Todo application.
Represents a single todo item with ID, description, and completion status.
"""

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class Task:
    """
    Represents a single task in the todo system.

    Attributes:
        id: Unique identifier for the task
        description: The text description of what needs to be done
        status: The completion status of the task ("incomplete" or "complete")
    """
    id: str
    description: str
    status: str = "incomplete"

    def __post_init__(self):
        """Validate the task after initialization."""
        if not self.id:
            raise ValueError("Task ID cannot be empty")
        if not self.description:
            raise ValueError("Task description cannot be empty")
        if self.status not in ["incomplete", "complete"]:
            raise ValueError(f"Task status must be 'incomplete' or 'complete', got '{self.status}'")

    def to_dict(self) -> Dict[str, Any]:
        """Convert the task to a dictionary representation."""
        return {
            "id": self.id,
            "description": self.description,
            "status": self.status
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Task':
        """Create a Task instance from a dictionary."""
        return cls(
            id=data["id"],
            description=data["description"],
            status=data.get("status", "incomplete")
        )

    def complete(self) -> None:
        """Mark the task as complete."""
        self.status = "complete"