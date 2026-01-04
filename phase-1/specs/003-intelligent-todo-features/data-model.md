# Data Model: CLI Todo App - Intelligent Features

## Task Entity

### Attributes
- **id**: `int` - Unique identifier for the task (auto-incrementing integer)
- **title**: `str` - Required title of the task (non-empty string, 1-200 characters)
- **description**: `str | None` - Optional description of the task (nullable string, max 1000 characters)
- **completed**: `bool` - Status indicating if the task is completed (default: False)
- **priority**: `str | None` - Priority level of the task (values: "high"/"medium"/"low", default: None)
- **tags**: `List[str]` - List of tags/categories for the task (default: empty list)
- **due_date**: `datetime.datetime | None` - Due date and time for the task (default: None, format: YYYY-MM-DD HH:MM)
- **recurrence**: `str | None` - Recurrence pattern for the task (values: "daily", "weekly", "monthly", "every N days", default: None)

### Validation Rules
- `id` must be a positive integer
- `title` must be a non-empty string (1-200 characters)
- `description` can be None or a string up to 1000 characters
- `completed` must be a boolean value
- `priority` must be one of "high", "medium", "low" (case-insensitive) or None
- `tags` must be a list of strings where each tag is 1-50 characters (alphanumeric + hyphens/underscores)
- `due_date` must be a valid datetime or None
- `recurrence` must be one of the supported patterns or None

### State Transitions
- New task: `completed = False`, `priority = None`, `tags = []`, `due_date = None`, `recurrence = None` (default)
- Mark complete: `completed = True`
- Mark incomplete: `completed = False`
- Update priority: `priority = "high"/"medium"/"low"`
- Update tags: `tags = [new_list_of_tags]`
- Update due date: `due_date = datetime_object`
- Update recurrence: `recurrence = "pattern"`

### Recurrence Patterns
- **daily**: Recurs every day
- **weekly**: Recurs every week on the same day of the week
- **monthly**: Recurs every month on the same day of the month
- **every N days**: Recurs every N days (e.g., "every 3 days")
- **every N weeks**: Recurs every N weeks (e.g., "every 2 weeks")
- **every N months**: Recurs every N months (e.g., "every 6 months")

## TaskManager Service Interface

### Core Operations
- `add_task(title: str, description: str = None, priority: str = None, tags: List[str] = None, due_date: str = None, recurrence: str = None) -> int` - Creates a new task and returns its ID
- `get_task(task_id: int) -> Task | None` - Retrieves a task by ID
- `get_all_tasks() -> List[Task]` - Returns all tasks, applying current sort order if set
- `update_task(task_id: int, title: str = None, description: str = None, priority: str = None, tags: List[str] = None, due_date: str = None, recurrence: str = None) -> bool` - Updates task details
- `delete_task(task_id: int) -> bool` - Deletes a task by ID
- `mark_task_complete(task_id: int) -> bool` - Marks a task as complete; if recurring, creates next instance
- `mark_task_incomplete(task_id: int) -> bool` - Marks a task as incomplete

### Intelligent Operations
- `search_tasks(keyword: str) -> List[Task]` - Searches tasks by keyword in title, description, and tags
- `filter_tasks(filters: dict) -> List[Task]` - Filters tasks by various criteria (status, priority, tags, due date)
- `sort_tasks(criterion: str) -> bool` - Sets the sort order for task display (priority, due, alpha)
- `get_upcoming_tasks(hours_ahead: int = 24) -> List[Task]` - Gets tasks due within specified hours
- `get_overdue_tasks() -> List[Task]` - Gets tasks past their due date
- `process_completed_recurring_task(task_id: int) -> bool` - Creates next instance of recurring task after completion

### Error Conditions
- Invalid task ID: Returns appropriate error or None
- Empty inputs: Validated and rejected with clear error messages
- Invalid priority value: Raises validation error
- Invalid date format: Raises validation error
- Invalid recurrence pattern: Raises validation error
- Natural language date parsing failure: Raises validation error with suggestions