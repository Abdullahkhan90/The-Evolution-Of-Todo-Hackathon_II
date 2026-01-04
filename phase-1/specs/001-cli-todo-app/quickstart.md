# Quickstart Guide: CLI Todo Application

## Prerequisites
- Python 3.13+
- UV package manager

## Setup
1. Clone the repository
2. Navigate to the project directory
3. Install dependencies: `uv sync` (if any dependencies are added later)
4. Run the application: `python src/main.py`

## Basic Usage
The application provides a command-line interface for managing your todo tasks.

### Available Commands
- `add "task title" ["optional description"]` - Add a new task
- `list` - View all tasks
- `complete <task_id>` - Mark a task as complete
- `update <task_id> "new title" ["new description"]` - Update task details
- `delete <task_id>` - Delete a task
- `help` - Show available commands
- `quit` or `exit` - Exit the application

### Example Workflow
1. Add a task: `add "Buy groceries" "Milk, bread, eggs"`
2. View tasks: `list`
3. Mark task as complete: `complete 1`
4. Update a task: `update 1 "Buy groceries" "Milk, bread, eggs, fruits"`
5. Delete a task: `delete 1`

## Features
- Add tasks with titles and optional descriptions
- View all tasks with clear completion status indicators
- Mark tasks as complete/incomplete
- Update task details
- Delete tasks
- Error handling for invalid inputs

## Development
To run tests: `python -m pytest tests/`
To run the application in development mode: `python src/main.py`

## Architecture
The application follows a clean architecture pattern:
- Models: Task definition
- Services: TaskManager with business logic
- UI: CLI interface
- Utils: Helper functions