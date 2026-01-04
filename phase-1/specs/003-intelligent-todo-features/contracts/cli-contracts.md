# CLI Todo Application - Intelligent Command Contracts

## Command Interface Specification

This document specifies the command interface contracts for the CLI Todo Application with intelligent features.

### Add Task Command with Intelligence
- **Command**: `add "title" ["description"] [--priority high|medium|low] [--tags tag1,tag2] [--due "natural language date"] [--recurring daily|weekly|monthly|every N days]`
- **Input**: 
  - title: string (required, 1-200 characters)
  - description: string (optional, 0-1000 characters)
  - priority: string (optional, values: high/medium/low)
  - tags: string (optional, comma-separated list of tags)
  - due: string (optional, natural language date/time like "tomorrow at 3pm", "next Monday")
  - recurring: string (optional, recurrence pattern)
- **Output**: 
  - Success: "Task added with ID: {id}"
  - Error: "Error: {error_message}"
- **Behavior**: Creates a new task with a unique ID and 'incomplete' status, with optional intelligent fields

### Complete Task Command with Auto-Rescheduling
- **Command**: `complete <task_id>`
- **Input**: 
  - task_id: integer (positive)
- **Output**: 
  - Success: "Task {id} marked as complete"
  - If recurring: "Task {id} marked as complete. Next instance scheduled for {date}"
  - Error: "Error: {error_message}"
- **Behavior**: Updates task status to 'complete'; if task is recurring, automatically creates next instance with updated due date

### List Tasks Command with Enhanced Display
- **Command**: `list`
- **Input**: None
- **Output**: 
  - Success: Formatted list of all tasks with ID, status, priority, title, tags, due date/time, recurrence pattern
  - Empty: "No tasks found."
  - Error: "Error: {error_message}"
- **Behavior**: Displays all tasks with enhanced information when present (priority, tags, due date/time, recurrence)

### Search Task Command
- **Command**: `search <keyword>`
- **Input**: 
  - keyword: string (to search in title, description, and tags)
- **Output**: 
  - Success: Formatted list of matching tasks
  - No matches: "No tasks found matching '{keyword}'."
  - Error: "Error: {error_message}"
- **Behavior**: Searches tasks by keyword across title, description, and tags

### Filter Task Command with Intelligent Criteria
- **Command**: `filter [status=complete|incomplete] [priority=high|medium|low] [tags=tag1,tag2] [due=before:YYYY-MM-DD|after:YYYY-MM-DD|on:YYYY-MM-DD|upcoming:N_hours|overdue] [recurs=pattern]`
- **Input**: 
  - status: string (optional, filter by completion status)
  - priority: string (optional, filter by priority level)
  - tags: string (optional, comma-separated list of tags to match)
  - due: string (optional, date filter with before/after/on/upcoming/overdue prefixes)
  - recurs: string (optional, recurrence pattern filter)
- **Output**: 
  - Success: Formatted list of filtered tasks
  - No matches: "No tasks found matching the filters."
  - Error: "Error: {error_message}"
- **Behavior**: Filters tasks by multiple criteria with AND logic

### Sort Task Command with Intelligent Options
- **Command**: `sort [priority|due|alpha|recurrence]`
- **Input**: 
  - criterion: string (sort by priority, due date, alphabetical, or recurrence)
- **Output**: 
  - Success: "Tasks sorted by {criterion}."
  - Error: "Error: {error_message}"
- **Behavior**: Sorts tasks by specified criterion

### Update Task Command with Intelligent Fields
- **Command**: `update <task_id> [--title "new title"] [--description "new description"] [--priority high|medium|low] [--tags tag1,tag2] [--due "natural language date"] [--recurring pattern]`
- **Input**: 
  - task_id: integer (positive)
  - title: string (optional, 1-200 characters)
  - description: string (optional, 0-1000 characters)
  - priority: string (optional, values: high/medium/low)
  - tags: string (optional, comma-separated list of tags)
  - due: string (optional, natural language date/time)
  - recurring: string (optional, recurrence pattern)
- **Output**: 
  - Success: "Task {id} updated successfully"
  - Error: "Error: {error_message}"
- **Behavior**: Updates specified task fields, including intelligent fields

## Intelligent Automation Behaviors

### Recurring Task Processing
- When a recurring task is marked as complete, the system automatically creates a new instance with the next occurrence date
- The new instance inherits all properties from the original task
- The recurrence pattern determines the interval for the next occurrence

### Natural Language Date Parsing
- The system uses dateparser library to interpret natural language dates
- Supports relative dates ("tomorrow", "in 2 days", "next week")
- Supports absolute dates ("December 31st", "2025-12-31")
- Supports time specifications ("at 3pm", "at 15:00", "in the morning")

### Reminder Notifications
- On application startup, the system checks for upcoming and overdue tasks
- Displays notifications for tasks due soon (e.g., "Upcoming: Meeting in 30 min")
- Displays notifications for overdue tasks (e.g., "Overdue: Grocery shopping")

## Error Handling Contracts

### Invalid Natural Language Date
- **Input**: Command with unparseable natural language date
- **Output**: "Error: Unable to parse date '{input}'. Please use formats like 'tomorrow at 3pm', 'next Monday', or 'YYYY-MM-DD'."

### Invalid Recurrence Pattern
- **Input**: Command with unsupported recurrence pattern
- **Output**: "Error: Invalid recurrence pattern '{pattern}'. Use 'daily', 'weekly', 'monthly', or 'every N days/weeks'."

### Invalid Task ID
- **Input**: Command with non-existent task ID
- **Output**: "Error: Task with ID {id} not found."

### Empty Title
- **Input**: Add command with empty title
- **Output**: "Error: Task title cannot be empty."