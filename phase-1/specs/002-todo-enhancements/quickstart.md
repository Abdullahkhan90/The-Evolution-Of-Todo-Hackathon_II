# Quickstart Guide: CLI Todo App - Organization & Usability Enhancements

## Prerequisites
- Python 3.13+
- UV package manager

## Setup
1. Clone the repository
2. Navigate to the project directory
3. Install dependencies: `uv sync` (if any dependencies are added later)
4. Run the application: `python src/main.py`

## Basic Usage
The application provides a command-line interface for managing your todo tasks with enhanced organizational features.

### Available Commands
- `add "task title" ["optional description"]` - Add a new task (old syntax, backward compatible)
- `add "task title" ["optional description"] --priority high --tags work,urgent --due 2025-12-30` - Add a new task with organizational features
- `list` - View all tasks (enhanced to show priority, tags, due date when present)
- `complete <task_id>` - Mark a task as complete
- `update <task_id> "new title" ["new description"]` - Update task details (old syntax, backward compatible)
- `update <task_id> --priority medium --tags personal --due 2025-12-31` - Update task with new fields
- `delete <task_id>` - Delete a task
- `search <keyword>` - Search tasks by keyword in title, description, and tags
- `filter [status=complete] [priority=high] [tags=work] [due=after:2025-12-25]` - Filter tasks by criteria
- `sort [priority|due|alpha]` - Sort tasks by specified criterion
- `help` - Show available commands
- `quit` or `exit` - Exit the application

### Example Workflow
1. Add a task with organizational features: `add "Prepare presentation" "Slides for team meeting" --priority high --tags work --due 2025-12-30`
2. View tasks: `list` (shows priority indicator, tags, and due date)
3. Search for tasks: `search presentation`
4. Filter tasks: `filter priority=high`
5. Sort tasks: `sort due`
6. Update a task: `update 1 --priority medium`
7. Mark task as complete: `complete 1`

## Enhanced Features
- **Priority**: Assign high/medium/low priority to tasks
- **Tags**: Categorize tasks with multiple tags
- **Due Dates**: Set deadlines in YYYY-MM-DD format
- **Search**: Find tasks by keyword across title, description, and tags
- **Filter**: Narrow down tasks by various criteria
- **Sort**: Organize tasks by priority, due date, or alphabetically

## Backward Compatibility
All original Basic Level commands continue to work exactly as before:
- `add "title" ["description"]`
- `list`
- `complete <id>`
- `update <id> "title" ["description"]`
- `delete <id>`

The new features are completely optional and additive.

## Development
To run tests: `python -m pytest tests/`
To run the application in development mode: `python src/main.py`

## Architecture
The application follows a clean architecture pattern:
- Models: Task definition with new organizational fields
- Services: TaskManager with enhanced business logic
- UI: CLI interface with flexible command parsing
- Utils: Helper functions for validation and formatting