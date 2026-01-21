"""MCP Tool for adding a new task for the logged-in user."""

from typing import Dict, Any, Union
from sqlmodel import Session, select
from pydantic import BaseModel, Field
from ..models.task import Task
from ..database.database import get_session, engine
from uuid import UUID


class AddTaskInput(BaseModel):
    """Input schema for the add_task tool."""

    user_id: str = Field(..., description="The ID of the user creating the task")
    title: str = Field(..., description="The title of the task")
    description: str = Field("", description="The description of the task (optional)")


def add_task(input_data: AddTaskInput) -> Dict[str, Any]:
    """
    Create a new task for the logged-in user.

    Args:
        input_data: Contains user_id, title, and optional description

    Returns:
        Dictionary with task_id, status, and title of the created task
    """
    # Validate input
    if not input_data.title.strip():
        raise ValueError("Title cannot be empty")

    # Get database session
    with Session(engine) as session:
        # Create new task instance
        new_task = Task(
            user_id=UUID(input_data.user_id),
            title=input_data.title.strip(),
            description=input_data.description.strip() if input_data.description else ""
        )

        # Add to database
        session.add(new_task)
        session.commit()
        session.refresh(new_task)

        # Return success response
        return {
            "task_id": str(new_task.id),
            "status": "created",
            "title": new_task.title
        }