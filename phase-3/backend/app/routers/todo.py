from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select
from typing import List, Optional
from uuid import UUID
from app.models.task import Task, User, TaskBase, TaskCreate
from app.schemas.task import Task as TaskSchema, TaskCreate as TaskCreateSchema, TaskUpdate
from app.database.database import get_session
from app.core.auth import get_current_user

router = APIRouter(prefix="/todos", tags=["todos"])

@router.post("/", response_model=TaskSchema)
def create_todo(
    todo_create: TaskCreateSchema,
    current_user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Create a new todo item for the authenticated user.
    """
    # Verify that the user_id in the request matches the authenticated user
    if str(current_user_id) != str(todo_create.user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create todos for this user"
        )

    # Check if user exists
    user = session.get(User, todo_create.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Create task instance
    todo = Task(
        title=todo_create.title,
        description=todo_create.description,
        completed=todo_create.completed,
        priority=todo_create.priority,
        tags=todo_create.tags,
        due_date=todo_create.due_date,
        recurrence=todo_create.recurrence,
        user_id=todo_create.user_id
    )

    session.add(todo)
    session.commit()
    session.refresh(todo)

    return todo


@router.get("/", response_model=List[TaskSchema])
def read_todos(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    completed: Optional[bool] = Query(None, description="Filter by completion status"),
    priority: Optional[str] = Query(None, description="Filter by priority level"),
    current_user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Retrieve todos for the authenticated user with optional pagination and filtering.
    """
    # Build query with user_id filter
    query = select(Task).where(Task.user_id == UUID(str(current_user_id)))

    # Apply filters if provided
    if completed is not None:
        query = query.where(Task.completed == completed)
    if priority is not None:
        query = query.where(Task.priority == priority)

    # Apply pagination
    query = query.offset(skip).limit(limit)

    todos = session.exec(query).all()
    return todos


@router.get("/{todo_id}", response_model=TaskSchema)
def read_todo(
    todo_id: UUID,
    current_user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get a specific todo by ID.
    """
    todo = session.get(Task, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    # Check if todo belongs to the authenticated user
    if str(todo.user_id) != str(current_user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this todo"
        )

    return todo


@router.put("/{todo_id}", response_model=TaskSchema)
def update_todo(
    todo_id: UUID,
    todo_update: TaskUpdate,
    current_user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Update a specific todo by ID.
    """
    todo = session.get(Task, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    # Check if todo belongs to the authenticated user
    if str(todo.user_id) != str(current_user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this todo"
        )

    # Update todo fields if provided
    for field, value in todo_update.dict(exclude_unset=True).items():
        setattr(todo, field, value)

    session.add(todo)
    session.commit()
    session.refresh(todo)

    return todo


@router.delete("/{todo_id}")
def delete_todo(
    todo_id: UUID,
    current_user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Delete a specific todo by ID.
    """
    todo = session.get(Task, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    # Check if todo belongs to the authenticated user
    if str(todo.user_id) != str(current_user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this todo"
        )

    session.delete(todo)
    session.commit()

    return {"message": "Todo deleted successfully"}