"""
TaskManager service for managing tasks in memory with organizational features.
"""
import sys
import os
from typing import List, Optional, Dict, Any
from datetime import datetime

# Add the project root to the path to allow imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.models.task import Task
from src.utils.helpers import get_next_id


class TaskManager:
    """
    Manages tasks in memory with CRUD operations and organizational features.
    """
    def __init__(self):
        self._tasks: List[Task] = []
        self._id_map: dict = {}  # Maps ID to task index for O(1) lookup
        self._current_sort_order: str = "insertion"  # Default sort order

    def add_task(self, title: str, description: Optional[str] = None, priority: Optional[str] = None, tags: Optional[List[str]] = None, due_date: Optional[datetime] = None, recurrence: Optional[str] = None) -> int:
        """
        Create a new task and return its ID.
        """
        if not title or not title.strip():
            raise ValueError("Task title cannot be empty")

        task_id = get_next_id()
        task = Task(
            id=task_id,
            title=title,
            description=description,
            completed=False,
            priority=priority,
            tags=tags if tags is not None else [],
            due_date=due_date,
            recurrence=recurrence
        )

        self._tasks.append(task)
        self._id_map[task_id] = len(self._tasks) - 1

        return task_id

    def get_task(self, task_id: int) -> Optional[Task]:
        """
        Retrieve a task by ID.
        """
        if task_id in self._id_map:
            index = self._id_map[task_id]
            return self._tasks[index]
        return None

    def get_all_tasks(self) -> List[Task]:
        """
        Return all tasks, applying current sort order if set.
        """
        tasks = self._tasks.copy()
        
        if self._current_sort_order == "priority":
            # Sort by priority: high, medium, low, then by insertion order
            priority_order = {"high": 0, "medium": 1, "low": 2}
            tasks.sort(key=lambda t: (priority_order.get(t.priority, 3), self._tasks.index(t)))
        elif self._current_sort_order == "due":
            # Sort by due date: soonest first, then by insertion order
            def sort_key(task):
                if task.due_date:
                    # task.due_date is a datetime object, extract year, month, day
                    return (task.due_date.year, task.due_date.month, task.due_date.day, task.due_date.hour, task.due_date.minute, task.due_date.second)
                else:
                    # Tasks without due dates come last
                    return (float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), float('inf'))
            tasks.sort(key=sort_key)
        elif self._current_sort_order == "alpha":
            # Sort alphabetically by title
            tasks.sort(key=lambda t: t.title.lower())
        
        return tasks

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None, priority: Optional[str] = None, tags: Optional[List[str]] = None, due_date: Optional[datetime] = None, recurrence: Optional[str] = None) -> bool:
        """
        Update task details by ID.
        """
        if task_id not in self._id_map:
            return False

        index = self._id_map[task_id]
        task = self._tasks[index]

        if title is not None:
            if not title or not title.strip():
                raise ValueError("Task title cannot be empty")
            task.title = title

        if description is not None:
            task.description = description

        if priority is not None:
            task.priority = priority

        if tags is not None:
            task.tags = tags

        if due_date is not None:
            task.due_date = due_date

        if recurrence is not None:
            task.recurrence = recurrence

        return True

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by ID.
        """
        if task_id not in self._id_map:
            return False

        index = self._id_map[task_id]
        del self._tasks[index]
        
        # Update the id_map for indices after the deleted task
        for task_id_key, task_index in self._id_map.items():
            if task_index > index:
                self._id_map[task_id_key] = task_index - 1

        # Remove the deleted task's ID from the map
        del self._id_map[task_id]
        
        return True

    def mark_task_complete(self, task_id: int) -> bool:
        """
        Mark a task as complete by ID.
        If the task is recurring, create a new instance with updated due date.
        """
        if task_id not in self._id_map:
            return False

        index = self._id_map[task_id]
        task = self._tasks[index]

        # If the task is recurring, create a new instance before marking as complete
        if task.recurrence:
            self._create_next_instance(task)

        task.completed = True
        return True

    def _create_next_instance(self, task: Task) -> int:
        """
        Create the next instance of a recurring task with updated due date.
        """
        # Calculate the next due date based on recurrence pattern
        next_due_date = self._calculate_next_due_date(task.due_date, task.recurrence)

        # Create a new task with the same properties but updated due date
        new_task_id = get_next_id()
        new_task = Task(
            id=new_task_id,
            title=task.title,
            description=task.description,
            completed=False,
            priority=task.priority,
            tags=task.tags,
            due_date=next_due_date,
            recurrence=task.recurrence
        )

        self._tasks.append(new_task)
        self._id_map[new_task_id] = len(self._tasks) - 1

        return new_task_id

    def _calculate_next_due_date(self, current_due_date: Optional[datetime], recurrence_pattern: str) -> Optional[datetime]:
        """
        Calculate the next due date based on the recurrence pattern.
        """
        if not current_due_date:
            return None

        from datetime import timedelta

        # Parse the recurrence pattern
        if recurrence_pattern == "daily" or recurrence_pattern == "every day":
            return current_due_date + timedelta(days=1)
        elif recurrence_pattern == "weekly" or recurrence_pattern == "every week":
            return current_due_date + timedelta(days=7)
        elif recurrence_pattern == "monthly" or recurrence_pattern == "every month":
            # For monthly recurrence, we'll add approximately 30 days
            # For more accurate month-to-month calculation, we'd need a more complex algorithm
            return current_due_date + timedelta(days=30)
        elif recurrence_pattern.startswith("every"):
            # Handle patterns like "every N days/weeks/months"
            parts = recurrence_pattern.split()
            if len(parts) == 3 and parts[2] in ["days", "weeks", "months"]:
                count = int(parts[1])
                unit = parts[2][:-1] if parts[2][-1] == 's' else parts[2]  # Remove plural 's'

                if unit == "day":
                    return current_due_date + timedelta(days=count)
                elif unit == "week":
                    return current_due_date + timedelta(weeks=count)
                elif unit == "month":
                    # For month intervals, we'll use 30 days * count as approximation
                    return current_due_date + timedelta(days=30*count)

        # If pattern not recognized, return None
        return None

    def mark_task_incomplete(self, task_id: int) -> bool:
        """
        Mark a task as incomplete by ID.
        """
        if task_id not in self._id_map:
            return False

        index = self._id_map[task_id]
        self._tasks[index].completed = False
        return True

    def get_upcoming_tasks(self, hours_ahead: int = 24) -> List[Task]:
        """
        Get tasks that are due within the specified number of hours.
        """
        from datetime import datetime, timedelta

        now = datetime.now()
        future_time = now + timedelta(hours=hours_ahead)

        upcoming_tasks = []
        for task in self._tasks:
            if not task.completed and task.due_date and task.due_date <= future_time and task.due_date >= now:
                upcoming_tasks.append(task)

        return upcoming_tasks

    def get_overdue_tasks(self) -> List[Task]:
        """
        Get tasks that are past their due date and not yet completed.
        """
        from datetime import datetime

        now = datetime.now()
        overdue_tasks = []

        for task in self._tasks:
            if not task.completed and task.due_date and task.due_date < now:
                overdue_tasks.append(task)

        return overdue_tasks

    def search_tasks(self, keyword: str) -> List[Task]:
        """
        Search tasks by keyword in title, description, and tags.
        """
        keyword_lower = keyword.lower()
        matching_tasks = []
        
        for task in self._tasks:
            # Check if keyword is in title
            if keyword_lower in task.title.lower():
                matching_tasks.append(task)
                continue
            
            # Check if keyword is in description
            if task.description and keyword_lower in task.description.lower():
                matching_tasks.append(task)
                continue
            
            # Check if keyword is in tags
            for tag in task.tags:
                if keyword_lower in tag.lower():
                    matching_tasks.append(task)
                    break
        
        return matching_tasks

    def filter_tasks(self, filters: Dict[str, Any]) -> List[Task]:
        """
        Filter tasks by various criteria.
        Supported filters: status, priority, tags, due_date
        """
        filtered_tasks = []
        
        for task in self._tasks:
            match = True
            
            # Filter by status (completed/incomplete)
            if 'status' in filters:
                if filters['status'] == 'complete' and not task.completed:
                    match = False
                elif filters['status'] == 'incomplete' and task.completed:
                    match = False
            
            # Filter by priority
            if 'priority' in filters:
                if task.priority != filters['priority']:
                    match = False
            
            # Filter by tags (any of the specified tags)
            if 'tags' in filters and match:
                filter_tags = filters['tags'] if isinstance(filters['tags'], list) else [filters['tags']]
                task_has_any_tag = any(tag in task.tags for tag in filter_tags)
                if not task_has_any_tag:
                    match = False
            
            # Filter by due date (before/after/on)
            if 'due' in filters and match:
                filter_due = filters['due']
                if task.due_date:
                    # task.due_date is a datetime object, extract year, month, day
                    task_date = [task.due_date.year, task.due_date.month, task.due_date.day]
                    if filter_due.startswith('before:'):
                        filter_date = [int(x) for x in filter_due[7:].split('-')]  # Remove 'before:' prefix
                        if task_date >= filter_date:
                            match = False
                    elif filter_due.startswith('after:'):
                        filter_date = [int(x) for x in filter_due[6:].split('-')]  # Remove 'after:' prefix
                        if task_date <= filter_date:
                            match = False
                    elif filter_due.startswith('on:'):
                        filter_date = [int(x) for x in filter_due[3:].split('-')]  # Remove 'on:' prefix
                        if task_date != filter_date:
                            match = False
                else:
                    # Task has no due date but filter expects one
                    match = False
            
            if match:
                filtered_tasks.append(task)
        
        return filtered_tasks

    def sort_tasks(self, criterion: str, reverse: bool = False) -> bool:
        """
        Sort tasks by specified criterion.
        Criterion options: 'priority', 'due', 'alpha'
        """
        if criterion not in ['priority', 'due', 'alpha', 'insertion']:
            return False
        
        self._current_sort_order = criterion
        return True