# Data Model: CLI Todo App - Organization & Usability Enhancements

## Task Entity

### Attributes
- **id**: `int` - Unique identifier for the task (auto-incrementing integer)
- **title**: `str` - Required title of the task (non-empty string)
- **description**: `str | None` - Optional description of the task (nullable string)
- **completed**: `bool` - Status indicating if the task is completed (default: False)
- **priority**: `str | None` - Priority level of the task (values: "high"/"medium"/"low", default: None)
- **tags**: `List[str]` - List of tags/categories for the task (default: empty list)
- **due_date**: `str | None` - Due date for the task in YYYY-MM-DD format (default: None)

### Validation Rules
- `id` must be a positive integer
- `title` must be a non-empty string (1-200 characters)
- `description` can be None or a string up to 1000 characters
- `completed` must be a boolean value
- `priority` must be one of "high", "medium", "low" (case-insensitive) or None
- `tags` must be a list of strings where each tag is 1-50 characters (alphanumeric + hyphens/underscores)
- `due_date` must be in YYYY-MM-DD format or None

### State Transitions
- New task: `completed = False`, `priority = None`, `tags = []`, `due_date = None` (default)
- Mark complete: `completed = True`
- Mark incomplete: `completed = False` (if supporting this operation)
- Update priority: `priority = "high"/"medium"/"low"`
- Update tags: `tags = [new_list_of_tags]`
- Update due date: `due_date = "YYYY-MM-DD"`

## TaskManager Service Interface

### Core Operations
- `add_task(title: str, description: str = None, priority: str = None, tags: List[str] = None, due_date: str = None) -> int` - Creates a new task and returns its ID
- `get_task(task_id: int) -> Task | None` - Retrieves a task by ID
- `get_all_tasks() -> List[Task]` - Returns all tasks
- `update_task(task_id: int, title: str = None, description: str = None, priority: str = None, tags: List[str] = None, due_date: str = None) -> bool` - Updates task details
- `delete_task(task_id: int) -> bool` - Deletes a task by ID
- `mark_task_complete(task_id: int) -> bool` - Marks a task as complete
- `mark_task_incomplete(task_id: int) -> bool` - Marks a task as incomplete

### New Operations for Phase II
- `search_tasks(keyword: str) -> List[Task]` - Searches tasks by keyword in title, description, and tags
- `filter_tasks(filters: dict) -> List[Task]` - Filters tasks by various criteria (status, priority, tags, due date)
- `sort_tasks(criterion: str, reverse: bool = False) -> List[Task]` - Sorts tasks by specified criterion

### Error Conditions
- Invalid task ID: Returns appropriate error or None
- Duplicate operations: Handled gracefully
- Empty inputs: Validated and rejected with clear error messages
- Invalid priority value: Raises validation error
- Invalid date format: Raises validation error
- Invalid tag format: Raises validation error