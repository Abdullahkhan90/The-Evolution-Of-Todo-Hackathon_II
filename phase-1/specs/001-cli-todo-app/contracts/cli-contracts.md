# CLI Todo Application - Command Contracts

## Command Interface Specification

This document specifies the command interface contracts for the CLI Todo Application.

### Add Task Command
- **Command**: `add "title" ["description"]`
- **Input**: 
  - title: string (required, 1-200 characters)
  - description: string (optional, 0-1000 characters)
- **Output**: 
  - Success: "Task added with ID: {id}"
  - Error: "Error: {error_message}"
- **Behavior**: Creates a new task with a unique ID and 'incomplete' status

### List Tasks Command
- **Command**: `list`
- **Input**: None
- **Output**: 
  - Success: Formatted list of all tasks with ID, title, description, and status
  - Empty: "No tasks found."
  - Error: "Error: {error_message}"
- **Behavior**: Displays all tasks with clear status indicators

### Complete Task Command
- **Command**: `complete <task_id>`
- **Input**: 
  - task_id: integer (positive)
- **Output**: 
  - Success: "Task {id} marked as complete"
  - Error: "Error: {error_message}"
- **Behavior**: Updates task status to 'complete'

### Update Task Command
- **Command**: `update <task_id> "new_title" ["new_description"]`
- **Input**: 
  - task_id: integer (positive)
  - new_title: string (optional, 1-200 characters)
  - new_description: string (optional, 0-1000 characters)
- **Output**: 
  - Success: "Task {id} updated successfully"
  - Error: "Error: {error_message}"
- **Behavior**: Updates specified task details

### Delete Task Command
- **Command**: `delete <task_id>`
- **Input**: 
  - task_id: integer (positive)
- **Output**: 
  - Success: "Task {id} deleted"
  - Error: "Error: {error_message}"
- **Behavior**: Removes task from the list

### Help Command
- **Command**: `help`
- **Input**: None
- **Output**: List of available commands with brief descriptions
- **Behavior**: Displays help information

### Quit Command
- **Command**: `quit` or `exit`
- **Input**: None
- **Output**: Exits the application
- **Behavior**: Terminates the application gracefully

## Error Handling Contracts

### Invalid Command
- **Input**: Unrecognized command
- **Output**: "Unknown command: {command}. Type 'help' for available commands."

### Invalid Task ID
- **Input**: Command with non-existent task ID
- **Output**: "Error: Task with ID {id} not found."

### Invalid Input Format
- **Input**: Command with incorrect arguments
- **Output**: "Error: Invalid command format. {help_text}"

### Empty Title
- **Input**: Add command with empty title
- **Output**: "Error: Task title cannot be empty."