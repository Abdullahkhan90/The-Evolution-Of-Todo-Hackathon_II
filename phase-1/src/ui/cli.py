"""
CLI interface for the Todo Application with organizational features.
"""
import re
import shlex
import sys
import os
from typing import Optional, List, Dict, Any

# Add the project root to the path to allow imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.services.task_manager import TaskManager
from src.models.task import Task
from src.utils.helpers import validate_priority, validate_due_date, validate_tags


class CLIInterface:
    """
    Handles command-line interface interactions with improved formatting and command parsing.
    """
    def __init__(self, task_manager: TaskManager):
        self.task_manager = task_manager

    def add_task(self, title: str, description: Optional[str] = None, priority: Optional[str] = None, tags: Optional[List[str]] = None, due_date: Optional[str] = None, recurrence: Optional[str] = None) -> str:
        """
        Add a new task with optional organizational features.
        """
        try:
            # Validate inputs
            if priority:
                validate_priority(priority)
            if due_date:
                # Parse natural language date if needed
                from dateparser import parse
                import re

                # Try to handle "next [day] at [time]" format by splitting it
                parsed_date = None
                if "next" in due_date.lower() and "at" in due_date.lower():
                    # Try to parse by replacing "next" with just the day
                    day_time_match = re.search(r'next\s+(\w+)\s+at\s+(.+)', due_date.lower())
                    if day_time_match:
                        day = day_time_match.group(1)
                        time = day_time_match.group(2)
                        # Try parsing "[day] at [time]"
                        parsed_date = parse(f"{day} at {time}")

                # If the above didn't work, try the original string
                if not parsed_date:
                    parsed_date = parse(due_date)

                if not parsed_date:
                    return f"Error: Unable to parse date '{due_date}'. Please use formats like 'tomorrow', 'next Monday', or 'YYYY-MM-DD'."
                # Update due_date to be the parsed datetime object
                due_date = parsed_date
            if recurrence:
                # Validate recurrence pattern
                valid_patterns = [
                    "daily", "weekly", "monthly",
                    "every day", "every week", "every month",
                    "every 2 days", "every 3 days", "every 4 days", "every 5 days", "every 6 days", "every 7 days",
                    "every 2 weeks", "every 3 weeks", "every 4 weeks",
                    "every 2 months", "every 3 months", "every 6 months"
                ]
                if recurrence not in valid_patterns and not (
                    recurrence.startswith("every ") and
                    ("days" in recurrence or "weeks" in recurrence or "months" in recurrence)
                ):
                    return f"Error: Invalid recurrence pattern '{recurrence}'. Valid patterns: {', '.join(valid_patterns)}"

            task_id = self.task_manager.add_task(title, description, priority, tags, due_date, recurrence)
            return f"Task added with ID: {task_id}"
        except ValueError as e:
            return f"Error: {str(e)}"

    def list_tasks(self) -> str:
        """
        List all tasks with clean, table-like display of organizational features.
        """
        tasks = self.task_manager.get_all_tasks()
        if not tasks:
            return "No tasks found."

        # Define column widths
        id_width = 4
        status_width = 8
        priority_width = 10
        title_width = 25
        tags_width = 15
        due_width = 12
        recurrence_width = 12

        # Create header
        header = (
            f"{'ID':<{id_width}} {'Status':<{status_width}} {'Priority':<{priority_width}} "
            f"{'Title':<{title_width}} {'Tags':<{tags_width}} {'Due Date':<{due_width}} {'Recurs':<{recurrence_width}}"
        )

        result = [header]

        # Separator line
        separator = "-" * len(header)
        result.append(separator)

        for task in tasks:
            status = "[X]" if task.completed else "[ ]"

            # Format priority display
            priority_display = "-"
            if task.priority:
                # Map priority to uppercase
                priority_map = {
                    "high": "HIGH", "h": "HIGH", "1": "HIGH",
                    "medium": "MEDIUM", "m": "MEDIUM", "2": "MEDIUM",
                    "low": "LOW", "l": "LOW", "3": "LOW"
                }
                priority_display = priority_map.get(task.priority.lower(), "-")

            # Format tags display
            tags_display = "-"
            if task.tags:
                tags_display = ",".join(task.tags)

            # Format due date display (without microseconds)
            due_date_display = "-"
            if task.due_date:
                # Format datetime to remove microseconds for cleaner display
                due_date_display = task.due_date.strftime("%Y-%m-%d %H:%M:%S") if hasattr(task.due_date, 'strftime') else str(task.due_date)

            # Format recurrence display
            recurrence_display = task.recurrence if task.recurrence else "-"

            # Format title (truncate if too long)
            title_display = task.title
            if len(task.title) > title_width-3:
                title_display = task.title[:title_width-3] + "..."

            # Add task row
            row = (
                f"{task.id:<{id_width}} {status:<{status_width}} {priority_display:<{priority_width}} "
                f"{title_display:<{title_width}} {tags_display:<{tags_width}} {due_date_display:<{due_width}} {recurrence_display:<{recurrence_width}}"
            )
            result.append(row)

        return "\n".join(result)

    def complete_task(self, task_id: int) -> str:
        """
        Mark a task as complete.
        """
        if self.task_manager.mark_task_complete(task_id):
            return f"Task {task_id} marked as complete"
        else:
            return f"Error: Task with ID {task_id} not found."

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None, priority: Optional[str] = None, tags: Optional[List[str]] = None, due_date: Optional[str] = None, recurrence: Optional[str] = None) -> str:
        """
        Update a task with optional organizational features.
        """
        # Parse due date if provided
        if due_date:
            from dateparser import parse
            import re

            # Try to handle "next [day] at [time]" format by splitting it
            parsed_date = None
            if "next" in due_date.lower() and "at" in due_date.lower():
                # Try to parse by replacing "next" with just the day
                day_time_match = re.search(r'next\s+(\w+)\s+at\s+(.+)', due_date.lower())
                if day_time_match:
                    day = day_time_match.group(1)
                    time = day_time_match.group(2)
                    # Try parsing "[day] at [time]"
                    parsed_date = parse(f"{day} at {time}")

            # If the above didn't work, try the original string
            if not parsed_date:
                parsed_date = parse(due_date)

            if not parsed_date:
                return f"Error: Unable to parse date '{due_date}'. Please use formats like 'tomorrow', 'next Monday', or 'YYYY-MM-DD'."
            # Update due_date to be the parsed datetime object
            due_date = parsed_date

        if self.task_manager.update_task(task_id, title, description, priority, tags, due_date, recurrence):
            return f"Task {task_id} updated successfully"
        else:
            return f"Error: Task with ID {task_id} not found."

    def delete_task(self, task_id: int) -> str:
        """
        Delete a task.
        """
        if self.task_manager.delete_task(task_id):
            return f"Task {task_id} deleted"
        else:
            return f"Error: Task with ID {task_id} not found."

    def search_tasks(self, keyword: str) -> str:
        """
        Search tasks by keyword in title, description, and tags.
        """
        tasks = self.task_manager.search_tasks(keyword)
        if not tasks:
            return f"No tasks found matching '{keyword}'."

        # Define column widths
        id_width = 4
        status_width = 8
        priority_width = 10
        title_width = 25
        tags_width = 20
        due_width = 12

        # Create header
        header = (
            f"{'ID':<{id_width}} {'Status':<{status_width}} {'Priority':<{priority_width}} "
            f"{'Title':<{title_width}} {'Tags':<{tags_width}} {'Due Date':<{due_width}}"
        )

        result = [f"Search results for '{keyword}':", header]

        # Separator line
        separator = "-" * len(header)
        result.append(separator)

        for task in tasks:
            status = "[X]" if task.completed else "[ ]"

            # Format priority display
            priority_display = "-"
            if task.priority:
                # Map priority to uppercase
                priority_map = {
                    "high": "HIGH", "h": "HIGH", "1": "HIGH",
                    "medium": "MEDIUM", "m": "MEDIUM", "2": "MEDIUM", 
                    "low": "LOW", "l": "LOW", "3": "LOW"
                }
                priority_display = priority_map.get(task.priority.lower(), "-")

            # Format tags display
            tags_display = "-"
            if task.tags:
                tags_display = ",".join(task.tags)

            # Format due date display (without microseconds)
            due_date_display = "-"
            if task.due_date:
                # Format datetime to remove microseconds for cleaner display
                due_date_display = task.due_date.strftime("%Y-%m-%d %H:%M:%S") if hasattr(task.due_date, 'strftime') else str(task.due_date)

            # Format title (truncate if too long)
            title_display = task.title
            if len(task.title) > title_width-3:
                title_display = task.title[:title_width-3] + "..."

            # Add task row
            row = (
                f"{task.id:<{id_width}} {status:<{status_width}} {priority_display:<{priority_width}} "
                f"{title_display:<{title_width}} {tags_display:<{tags_width}} {due_date_display:<{due_width}}"
            )
            result.append(row)

        return "\n".join(result)

    def filter_tasks(self, filters: Dict[str, Any]) -> str:
        """
        Filter tasks by various criteria.
        """
        tasks = self.task_manager.filter_tasks(filters)
        if not tasks:
            filter_desc = []
            for key, value in filters.items():
                if key == 'status':
                    filter_desc.append(f"status={value}")
                elif key == 'priority':
                    filter_desc.append(f"priority={value}")
                elif key == 'tags':
                    if isinstance(value, list):
                        filter_desc.append(f"tags={','.join(value)}")
                    else:
                        filter_desc.append(f"tags={value}")
                elif key == 'due':
                    filter_desc.append(f"due={value}")
            filter_str = ", ".join(filter_desc)
            return f"No tasks found matching the filters: {filter_str}."

        # Define column widths
        id_width = 4
        status_width = 8
        priority_width = 10
        title_width = 25
        tags_width = 20
        due_width = 12

        # Create header
        header = (
            f"{'ID':<{id_width}} {'Status':<{status_width}} {'Priority':<{priority_width}} "
            f"{'Title':<{title_width}} {'Tags':<{tags_width}} {'Due Date':<{due_width}}"
        )

        result = ["Filtered tasks:", header]

        # Separator line
        separator = "-" * len(header)
        result.append(separator)

        for task in tasks:
            status = "[X]" if task.completed else "[ ]"

            # Format priority display
            priority_display = "-"
            if task.priority:
                # Map priority to uppercase
                priority_map = {
                    "high": "HIGH", "h": "HIGH", "1": "HIGH",
                    "medium": "MEDIUM", "m": "MEDIUM", "2": "MEDIUM", 
                    "low": "LOW", "l": "LOW", "3": "LOW"
                }
                priority_display = priority_map.get(task.priority.lower(), "-")

            # Format tags display
            tags_display = "-"
            if task.tags:
                tags_display = ",".join(task.tags)

            # Format due date display (without microseconds)
            due_date_display = "-"
            if task.due_date:
                # Format datetime to remove microseconds for cleaner display
                due_date_display = task.due_date.strftime("%Y-%m-%d %H:%M:%S") if hasattr(task.due_date, 'strftime') else str(task.due_date)

            # Format title (truncate if too long)
            title_display = task.title
            if len(task.title) > title_width-3:
                title_display = task.title[:title_width-3] + "..."

            # Add task row
            row = (
                f"{task.id:<{id_width}} {status:<{status_width}} {priority_display:<{priority_width}} "
                f"{title_display:<{title_width}} {tags_display:<{tags_width}} {due_date_display:<{due_width}}"
            )
            result.append(row)

        return "\n".join(result)

    def sort_tasks(self, criterion: str) -> str:
        """
        Sort tasks by specified criterion.
        """
        if self.task_manager.sort_tasks(criterion):
            return f"Tasks sorted by {criterion}."
        else:
            return f"Error: Invalid sort criterion. Use 'priority', 'due', or 'alpha'."

    def parse_command(self, command: str) -> tuple:
        """
        Parse a command string into base command, arguments, and flags using shlex for proper quote handling.
        Returns a tuple of (base_command, args, flags_dict)
        """
        try:
            # Use shlex to properly handle quoted strings
            parts = shlex.split(command.strip())
        except ValueError:
            # If there's an issue with quotes, fall back to simple split
            parts = command.strip().split()

        if not parts:
            return None, [], {}

        base_cmd = parts[0].lower()
        args = []
        flags = {}

        i = 1
        while i < len(parts):
            part = parts[i]
            if part.startswith('--'):
                # This is a flag
                flag_name = part[2:]  # Remove '--' prefix
                if i + 1 < len(parts) and not parts[i + 1].startswith('--'):
                    # Next part is the flag value
                    flags[flag_name] = parts[i + 1]
                    i += 2  # Skip both flag and its value
                else:
                    # Flag without value (like a boolean flag)
                    flags[flag_name] = True
                    i += 1
            else:
                # Regular argument
                args.append(part)
                i += 1

        return base_cmd, args, flags

    def execute_command(self, command: str) -> str:
        """
        Execute a command and return the result.
        """
        base_cmd, args, flags = self.parse_command(command)

        if base_cmd == "add":
            if len(args) < 1:
                return "Error: Invalid command format. Usage: add \"title\" [\"description\"] [--priority high|medium|low] [--tags tag1,tag2] [--due \"natural date\"] [--recurring pattern]"

            title = args[0]
            description = args[1] if len(args) > 1 else None

            # Extract optional flags
            priority = flags.get('priority')
            tags_str = flags.get('tags')
            due_date = flags.get('due')
            recurrence = flags.get('recurring')

            # Validate and parse tags if provided
            tags = None
            if tags_str:
                try:
                    tags = validate_tags(tags_str)
                except ValueError as e:
                    return f"Error: {str(e)}"

            return self.add_task(title, description, priority, tags, due_date, recurrence)

        elif base_cmd == "list":
            return self.list_tasks()

        elif base_cmd == "complete":
            if len(args) != 1:
                return "Error: Invalid command format. Usage: complete <task_id>"
            try:
                task_id = int(args[0])
                return self.complete_task(task_id)
            except ValueError:
                return "Error: Invalid task ID. Task ID must be a number."

        elif base_cmd == "update":
            if len(args) < 1:
                return "Error: Invalid command format. Usage: update <task_id> [--title \"new title\"] [--description \"new description\"] [--priority high|medium|low] [--tags tag1,tag2] [--due \"natural date\"] [--recurring pattern]"

            try:
                task_id = int(args[0])

                # Extract all possible flags
                title = flags.get('title')
                description = flags.get('description')
                priority = flags.get('priority')
                tags_str = flags.get('tags')
                due_date = flags.get('due')
                recurrence = flags.get('recurring')

                # Validate and parse tags if provided
                tags = None
                if tags_str:
                    try:
                        tags = validate_tags(tags_str)
                    except ValueError as e:
                        return f"Error: {str(e)}"

                return self.update_task(task_id, title, description, priority, tags, due_date, recurrence)
            except ValueError:
                return "Error: Invalid task ID. Task ID must be a number."

        elif base_cmd == "delete":
            if len(args) != 1:
                return "Error: Invalid command format. Usage: delete <task_id>"
            try:
                task_id = int(args[0])
                return self.delete_task(task_id)
            except ValueError:
                return "Error: Invalid task ID. Task ID must be a number."

        elif base_cmd == "search":
            if len(args) != 1:
                return "Error: Invalid command format. Usage: search <keyword>"
            keyword = args[0]
            return self.search_tasks(keyword)

        elif base_cmd == "filter":
            if not flags and len(args) == 0:
                return "Error: Invalid command format. Usage: filter [status=complete|incomplete] [priority=high|medium|low] [tags=tag1,tag2] [due=before:YYYY-MM-DD|after:YYYY-MM-DD|on:YYYY-MM-DD]"

            # Parse filter arguments
            filters = {}
            for key, value in flags.items():
                if key in ['status', 'priority']:
                    filters[key] = value
                elif key == 'tags':
                    try:
                        filters['tags'] = validate_tags(value)
                    except ValueError as e:
                        return f"Error: {str(e)}"
                elif key == 'due':
                    # Validate date format for due date filters
                    if value.startswith('before:') or value.startswith('after:') or value.startswith('on:'):
                        date_part = value.split(':', 1)[1]
                        try:
                            validate_due_date(date_part)
                            filters['due'] = value
                        except ValueError as e:
                            return f"Error: {str(e)}"
                    else:
                        return f"Error: Invalid due date filter format. Use before:YYYY-MM-DD, after:YYYY-MM-DD, or on:YYYY-MM-DD"

            return self.filter_tasks(filters)

        elif base_cmd == "sort":
            if len(args) != 1:
                return "Error: Invalid command format. Usage: sort priority|due|alpha"
            criterion = args[0]
            if criterion not in ['priority', 'due', 'alpha']:
                return "Error: Invalid sort criterion. Use 'priority', 'due', or 'alpha'."
            return self.sort_tasks(criterion)

        elif base_cmd == "reminders":
            return self.show_reminders()

        elif base_cmd == "help":
            help_text = """
Available commands:

  add "title" ["description"] [--priority high|medium|low] [--tags tag1,tag2] [--due "natural date"] [--recurring pattern]
      - Add a new task (description, priority, tags, due, recurring are optional)

  list
      - View all tasks (shows priority, tags, due date, recurrence if set)

  complete <task_id>
      - Mark task as complete (auto-creates next instance if recurring)

  update <task_id> [--title "new title"] [--description "new description"] [--priority high|medium|low] [--tags tag1,tag2] [--due "natural date"] [--recurring pattern]
      - Update task details

  delete <task_id>
      - Delete a task

  search <keyword>
      - Search tasks by keyword in title/description/tags

  filter [status=complete|incomplete] [priority=high|medium|low] [tags=tag1,tag2] [due=before:YYYY-MM-DD|after:YYYY-MM-DD|on:YYYY-MM-DD]
      - Filter tasks by criteria

  sort priority|due|alpha
      - Sort tasks by specified criterion

  reminders
      - Show upcoming and overdue tasks

  help
      - Show this help message

  quit/exit
      - Exit the application
            """.strip()
            return help_text

        elif base_cmd in ["quit", "exit"]:
            return "quit"

        elif base_cmd == "reminders":
            return self.show_reminders()

        else:
            return f"Unknown command: {base_cmd}. Type 'help' for available commands."

    def show_reminders(self) -> str:
        """
        Show upcoming and overdue tasks.
        """
        from datetime import datetime, timedelta

        # Get upcoming tasks (due within 24 hours)
        upcoming_tasks = self.task_manager.get_upcoming_tasks(hours_ahead=24)

        # Get overdue tasks
        overdue_tasks = self.task_manager.get_overdue_tasks()

        result = []

        if overdue_tasks:
            result.append("[WARNING] OVERDUE TASKS:")
            for task in overdue_tasks:
                due_date_str = task.due_date.strftime("%Y-%m-%d %H:%M:%S") if hasattr(task.due_date, 'strftime') else str(task.due_date)
                result.append(f"  - {task.id}. {task.title} (due: {due_date_str})")
            result.append("")  # Empty line for spacing

        if upcoming_tasks:
            result.append("[INFO] UPCOMING TASKS (due in next 24 hours):")
            for task in upcoming_tasks:
                due_date_str = task.due_date.strftime("%Y-%m-%d %H:%M:%S") if hasattr(task.due_date, 'strftime') else str(task.due_date)
                result.append(f"  - {task.id}. {task.title} (due: {due_date_str})")
            result.append("")  # Empty line for spacing

        if not overdue_tasks and not upcoming_tasks:
            result.append("[OK] No upcoming or overdue tasks.")

        return "\n".join(result)
