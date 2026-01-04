# CLI Todo Application - Command Contracts

## Command Interface Specification

This document specifies the command interface contracts for the CLI Todo Application with organizational enhancements.

### Add Task Command
- **Command**: `add "title" ["description"] [--priority high|medium|low] [--tags tag1,tag2,...] [--due YYYY-MM-DD]`
- **Input**: 
  - title: string (required, 1-200 characters)
  - description: string (optional, 0-1000 characters)
  - priority: string (optional, values: high/medium/low)
  - tags: string (optional, comma-separated list of tags)
  - due: string (optional, date in YYYY-MM-DD format)
- **Output**: 
  - Success: "Task added with ID: {id}"
  - Error: "Error: {error_message}"
- **Behavior**: Creates a new task with a unique ID and 'incomplete' status, with optional organizational fields

### List Tasks Command
- **Command**: `list`
- **Input**: None
- **Output**: 
  - Success: Formatted list of all tasks with ID, title, description, status, priority (if set), tags (if set), due date (if set)
  - Empty: "No tasks found."
  - Error: "Error: {error_message}"
- **Behavior**: Displays all tasks with clear status indicators and optional organizational fields when present

### Complete Task Command
- **Command**: `complete <task_id>`
- **Input**: 
  - task_id: integer (positive)
- **Output**: 
  - Success: "Task {id} marked as complete"
  - Error: "Error: {error_message}"
- **Behavior**: Updates task status to 'complete'

### Update Task Command
- **Command**: `update <task_id> ["new_title"] ["new_description"] [--priority high|medium|low] [--tags tag1,tag2,...] [--due YYYY-MM-DD]`
- **Input**: 
  - task_id: integer (positive)
  - new_title: string (optional, 1-200 characters)
  - new_description: string (optional, 0-1000 characters)
  - priority: string (optional, values: high/medium/low)
  - tags: string (optional, comma-separated list of tags)
  - due: string (optional, date in YYYY-MM-DD format)
- **Output**: 
  - Success: "Task {id} updated successfully"
  - Error: "Error: {error_message}"
- **Behavior**: Updates specified task details including optional organizational fields

### Delete Task Command
- **Command**: `delete <task_id>`
- **Input**: 
  - task_id: integer (positive)
- **Output**: 
  - Success: "Task {id} deleted"
  - Error: "Error: {error_message}"
- **Behavior**: Removes task from the list

### Search Task Command
- **Command**: `search <keyword>`
- **Input**: 
  - keyword: string (to search in title, description, and tags)
- **Output**: 
  - Success: Formatted list of matching tasks
  - No matches: "No tasks found matching '{keyword}'."
  - Error: "Error: {error_message}"
- **Behavior**: Searches tasks by keyword across title, description, and tags

### Filter Task Command
- **Command**: `filter [status=complete|incomplete] [priority=high|medium|low] [tags=tag1,tag2,...] [due=before:YYYY-MM-DD|after:YYYY-MM-DD|on:YYYY-MM-DD]`
- **Input**: 
  - status: string (optional, values: complete/incomplete)
  - priority: string (optional, values: high/medium/low)
  - tags: string (optional, comma-separated list of tags to match)
  - due: string (optional, date filter with before/after/on prefix)
- **Output**: 
  - Success: Formatted list of filtered tasks
  - No matches: "No tasks found matching the filters."
  - Error: "Error: {error_message}"
- **Behavior**: Filters tasks by specified criteria

### Sort Task Command
- **Command**: `sort [priority|due|alpha]`
- **Input**: 
  - criterion: string (values: priority/due/alpha)
- **Output**: 
  - Success: "Tasks sorted by {criterion}."
  - Error: "Error: {error_message}"
- **Behavior**: Sorts tasks by specified criterion (priority high→low, due soonest first, alpha A-Z)

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

### Invalid Priority Value
- **Input**: Command with invalid priority value
- **Output**: "Error: Priority must be one of: high, medium, low."

### Invalid Date Format
- **Input**: Command with invalid date format
- **Output**: "Error: Date must be in YYYY-MM-DD format."