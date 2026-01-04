# Data Model: CLI Todo Application

## Task Entity

### Attributes
- **id**: `int` - Unique identifier for the task (auto-incrementing integer)
- **title**: `str` - Required title of the task (non-empty string)
- **description**: `str | None` - Optional description of the task (nullable string)
- **completed**: `bool` - Status indicating if the task is completed (default: False)

### Validation Rules
- `id` must be a positive integer
- `title` must be a non-empty string (1-200 characters)
- `description` can be None or a string up to 1000 characters
- `completed` must be a boolean value

### State Transitions
- New task: `completed = False` (default)
- Mark complete: `completed = True`
- Mark incomplete: `completed = False` (if supporting this operation)

## TaskManager Service Interface

### Core Operations
- `add_task(title: str, description: str = None) -> int` - Creates a new task and returns its ID
- `get_task(task_id: int) -> Task | None` - Retrieves a task by ID
- `get_all_tasks() -> List[Task]` - Returns all tasks
- `update_task(task_id: int, title: str = None, description: str = None) -> bool` - Updates task details
- `delete_task(task_id: int) -> bool` - Deletes a task by ID
- `mark_task_complete(task_id: int) -> bool` - Marks a task as complete
- `mark_task_incomplete(task_id: int) -> bool` - Marks a task as incomplete

### Error Conditions
- Invalid task ID: Returns appropriate error or None
- Duplicate operations: Handled gracefully
- Empty inputs: Validated and rejected with clear error messages