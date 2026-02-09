"""MCP Tool for updating a task's title or description."""

from typing import Dict, Any, Optional
from sqlmodel import Session, select
from pydantic import BaseModel, Field
from ..models.task import Task
from ..database.database import get_session, engine
from uuid import UUID


class UpdateTaskInput(BaseModel):
    """Input schema for the update_task tool."""

    user_id: str = Field(..., description="The ID of the user who owns the task")
    task_id: str = Field(..., description="The ID of the task to update")
    title: Optional[str] = Field(None, description="New title for the task (optional)")
    description: Optional[str] = Field(None, description="New description for the task (optional)")


def update_task(input_data: UpdateTaskInput) -> Dict[str, Any]:
    """
    Modify task title or description.

    Args:
        input_data: Contains user_id, task_id, and optional title/description updates

    Returns:
        Dictionary with task_id, status, and title of the updated task

    Raises:
        ValueError: If the task is not found or doesn't belong to the user
    """
    # Get database session
    with Session(engine) as session:
        # Find the task by id and user_id
        query = select(Task).where(Task.id == UUID(input_data.task_id)).where(Task.user_id == UUID(input_data.user_id))
        result = session.execute(query)
        task = result.scalar_one_or_none()

        # Raise error if task not found
        if not task:
            raise ValueError(f"Task with id {input_data.task_id} not found for user {input_data.user_id}")

        # Update fields if provided
        if input_data.title is not None:
            task.title = input_data.title.strip()
        if input_data.description is not None:
            task.description = input_data.description.strip()

        # Save the updated task
        session.add(task)
        session.commit()
        session.refresh(task)

        # Return success response
        return {
            "task_id": str(task.id),
            "status": "updated",
            "title": task.title
        }