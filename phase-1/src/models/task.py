"""
Task model representing a todo item with organizational features.
"""
import sys
import os
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List

# Add the project root to the path to allow imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))


@dataclass
class Task:
    """
    Represents a todo task with id, title, description, completion status, and organizational features.
    """
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False
    priority: Optional[str] = None  # high, medium, low
    tags: List[str] = None  # list of tags
    due_date: Optional[datetime] = None  # datetime object
    recurrence: Optional[str] = None  # recurrence pattern

    def __post_init__(self):
        """
        Validate the task attributes after initialization.
        """
        if not self.title or not self.title.strip():
            raise ValueError("Task title cannot be empty")
        if len(self.title) > 200:
            raise ValueError("Task title cannot exceed 200 characters")
        if self.description and len(self.description) > 1000:
            raise ValueError("Task description cannot exceed 1000 characters")
        if not isinstance(self.completed, bool):
            raise ValueError("Task completion status must be a boolean")

        # Validate priority if provided
        if self.priority is not None:
            self.priority = self.priority.lower()
            valid_priorities = ["high", "medium", "low", "h", "m", "l"]
            if self.priority not in valid_priorities:
                raise ValueError(f"Priority must be one of: {', '.join(valid_priorities)}")

        # Initialize tags as empty list if None
        if self.tags is None:
            self.tags = []

        # Validate tags
        for tag in self.tags:
            if not isinstance(tag, str) or len(tag) == 0:
                raise ValueError("Tags must be non-empty strings")

        # Validate recurrence pattern if provided
        if self.recurrence is not None:
            valid_recurrences = [
                "daily", "weekly", "monthly",
                "every day", "every week", "every month",
                "every 2 days", "every 3 days", "every 4 days", "every 5 days", "every 6 days", "every 7 days",
                "every 2 weeks", "every 3 weeks", "every 4 weeks",
                "every 2 months", "every 3 months", "every 6 months"
            ]
            # Check if it's a valid pattern (including "every N days/weeks/months")
            if not any(
                self.recurrence == pattern or
                (self.recurrence.startswith("every ") and
                 ("days" in self.recurrence or "weeks" in self.recurrence or "months" in self.recurrence))
                for pattern in valid_recurrences
            ):
                raise ValueError(f"Recurrence must be one of: {', '.join(valid_recurrences)}")