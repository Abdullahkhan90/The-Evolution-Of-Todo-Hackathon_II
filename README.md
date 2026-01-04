# CLI Todo Application

A simple command-line interface todo application with in-memory storage, built as part of The Evolution of Todo Project.

## Features

- Add, view, update, delete, and mark tasks as complete
- In-memory storage (no persistent data)
- Simple CLI interface
- User-friendly error messages

## Prerequisites

- Python 3.13+
- UV package manager or pip

## Dependencies

This project requires the following external dependencies:

- `dateparser` - for natural language date parsing (e.g., "tomorrow at 3pm", "next Monday")

Install dependencies with:
```bash
pip install -r requirements.txt
```

## Installation

1. Clone the repository
2. Navigate to the project directory
3. Install dependencies: `uv sync`
4. Run the application: `uv run python src/main.py`

## Usage

The application provides a command-line interface for managing your todo tasks:

- `add "task title" ["optional description"]` - Add a new task
- `list` - View all tasks
- `complete <task_id>` - Mark a task as complete
- `update <task_id> "new title" ["new description"]` - Update task details
- `delete <task_id>` - Delete a task
- `help` - Show available commands
- `quit` or `exit` - Exit the application

## Natural Language Date Support

The application supports natural language date parsing for due dates using the `--due` flag:

- `add "Meeting" "Team sync" --due "tomorrow at 3pm"`
- `add "Grocery" "Buy milk" --due "in 2 days"`
- `add "Review" "Project review" --due "next Monday"`

All date-related functionality is powered by the dateparser library.

## Development

This project was developed using spec-driven development with AI assistance. The implementation follows clean code principles and is designed with future evolution in mind.

### Architecture

The application follows a clean architecture pattern:
- Models: Task definition
- Services: TaskManager with business logic
- UI: CLI interface
- Utils: Helper functions

## Project Structure

```
src/
├── main.py              # Main entry point with CLI loop
├── models/
│   └── task.py          # Task class definition
├── services/
│   └── task_manager.py  # CRUD operations for tasks
├── ui/
│   └── cli.py           # CLI interface functions
└── utils/
    └── helpers.py       # Utility functions (ID generation, validation)
```

## Testing

Run tests with: `python -m pytest tests/`

## Contributing

This project is part of a spec-driven development experiment. All features derive from specifications, and code is generated with AI assistance.

## Running the Application

To start the CLI Todo Application, run:

```bash
python src/main.py
```

The application will start and display a welcome message. You can then enter commands to manage your tasks.