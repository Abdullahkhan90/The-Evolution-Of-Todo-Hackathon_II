from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from app.models.task import Task, User, TaskBase, TaskCreate
from app.schemas.task import Task as TaskSchema, TaskCreate as TaskCreateSchema, TaskUpdate
from app.database.database import get_session
from app.core.auth import get_current_user
import uuid

router = APIRouter()

@router.post("/{user_id}/tasks", response_model=TaskSchema)
def create_task(user_id: str, task_create: TaskCreateSchema, current_user_id: str = Depends(get_current_user), session: Session = Depends(get_session)):
    """
    Create a new task for the authenticated user.
    """
    # Verify that the user_id in the path matches the authenticated user
    if str(current_user_id) != str(user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create tasks for this user"
        )

    # Check if user exists
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Create task instance
    task = Task(
        title=task_create.title,
        description=task_create.description,
        completed=task_create.completed,
        priority=task_create.priority,
        tags=task_create.tags,
        due_date=task_create.due_date,
        recurrence=task_create.recurrence,
        user_id=user_id
    )

    session.add(task)
    session.commit()
    session.refresh(task)

    return task


@router.get("/{user_id}/tasks", response_model=List[TaskSchema])
def read_tasks(user_id: str, skip: int = 0, limit: int = 100, current_user_id: str = Depends(get_current_user), session: Session = Depends(get_session)):
    """
    Retrieve tasks for the authenticated user with optional pagination.
    """
    # Verify that the user_id in the path matches the authenticated user
    if str(current_user_id) != str(user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access tasks for this user"
        )

    # Only return tasks for the authenticated user
    statement = select(Task).where(Task.user_id == uuid.UUID(str(user_id))).offset(skip).limit(limit)
    tasks = session.exec(statement).all()
    return tasks


@router.get("/{user_id}/tasks/{task_id}", response_model=TaskSchema)
def read_task(user_id: str, task_id: uuid.UUID, current_user_id: str = Depends(get_current_user), session: Session = Depends(get_session)):
    """
    Get a specific task by ID.
    """
    # Verify that the user_id in the path matches the authenticated user
    if str(current_user_id) != str(user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access tasks for this user"
        )

    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Check if task belongs to the authenticated user
    if str(task.user_id) != str(user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this task"
        )

    return task


@router.put("/{user_id}/tasks/{task_id}", response_model=TaskSchema)
def update_task(user_id: str, task_id: uuid.UUID, task_update: TaskUpdate, current_user_id: str = Depends(get_current_user), session: Session = Depends(get_session)):
    """
    Update a specific task by ID.
    """
    # Verify that the user_id in the path matches the authenticated user
    if str(current_user_id) != str(user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update tasks for this user"
        )

    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Check if task belongs to the authenticated user
    if str(task.user_id) != str(user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this task"
        )

    # Update task fields if provided
    for field, value in task_update.dict(exclude_unset=True).items():
        setattr(task, field, value)

    session.add(task)
    session.commit()
    session.refresh(task)

    return task


@router.delete("/{user_id}/tasks/{task_id}")
def delete_task(user_id: str, task_id: uuid.UUID, current_user_id: str = Depends(get_current_user), session: Session = Depends(get_session)):
    """
    Delete a specific task by ID.
    """
    # Verify that the user_id in the path matches the authenticated user
    if str(current_user_id) != str(user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete tasks for this user"
        )

    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Check if task belongs to the authenticated user
    if str(task.user_id) != str(user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this task"
        )

    session.delete(task)
    session.commit()

    return {"message": "Task deleted successfully"}