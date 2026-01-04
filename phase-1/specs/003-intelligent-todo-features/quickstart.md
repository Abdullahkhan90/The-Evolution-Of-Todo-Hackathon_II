# Quickstart Guide: CLI Todo App - Intelligent Features

## Prerequisites
- Python 3.13+
- UV package manager
- dateparser library (install with: `uv add dateparser`)

## Setup
1. Clone the repository
2. Navigate to the project directory
3. Install dependencies: `uv sync` (or `pip install dateparser`)
4. Run the application: `python src/main.py`

## Basic Usage
The application provides a command-line interface for managing your todo tasks with intelligent automation features.

### Available Commands
- `add "title" ["description"] [--priority high|medium|low] [--tags tag1,tag2] [--due "natural date"] [--recurring daily|weekly|monthly|...]`
  - Add a new task (all fields optional)
  - Natural date examples: "tomorrow at 3pm", "next Monday", "in 2 days", "December 31st", "2025-12-31 15:00"
  - Recurrence examples: "daily", "weekly", "monthly", "every 3 days", "every 2 weeks"

- `list` - View all tasks (shows priority, tags, due date/time, recurrence if set)

- `complete <task_id>` - Mark task as complete (automatically creates next instance if recurring)

- `update <task_id> [--title "new title"] [--description "new description"] [--priority high|medium|low] [--tags tag1,tag2] [--due "natural date"] [--recurring pattern]`
  - Update task details

- `delete <task_id>` - Delete a task

- `search <keyword>` - Search tasks by keyword in title/description/tags

- `filter [status=complete|incomplete] [priority=high|medium|low] [tags=tag1,tag2] [due=before:YYYY-MM-DD|after:YYYY-MM-DD|on:YYYY-MM-DD]`
  - Filter tasks by criteria

- `sort priority|due|alpha`
  - Sort tasks by specified criterion

- `help` - Show available commands

- `quit/exit` - Exit the application

### Example Workflow
1. Add a recurring task: `add "Team meeting" "Weekly sync with team" --due "next Friday at 10am" --recurring weekly`
2. Add a task with natural language date: `add "Submit report" --due "in 3 days at 5pm" --priority high`
3. View tasks: `list`
4. Mark a task as complete: `complete 1` (if recurring, next instance will be auto-created)
5. Search for tasks: `search "meeting"`
6. Filter tasks: `filter priority=high`
7. Sort tasks: `sort due`

## Intelligent Features
- **Natural Language Dates**: Use phrases like "tomorrow at 3pm", "next Monday", "in 2 days" instead of rigid date formats
- **Recurring Tasks**: Set tasks to repeat daily, weekly, monthly, or custom intervals
- **Automatic Rescheduling**: When completing a recurring task, the next instance is automatically created
- **Smart Reminders**: On app startup, see upcoming and overdue tasks

## Development
To run tests: `python -m pytest tests/`
To run the application in development mode: `python src/main.py`

## Architecture
The application follows a clean architecture pattern:
- Models: Task definition with recurrence and datetime support
- Services: TaskManager with intelligent automation logic
- UI: CLI interface with natural language processing
- Utils: Helper functions (ID generation, validation, date parsing)