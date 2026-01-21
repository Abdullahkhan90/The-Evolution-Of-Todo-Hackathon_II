"""MCP Tool for listing tasks for the logged-in user."""

from typing import Dict, Any, List, Optional
from sqlmodel import Session, select
from pydantic import BaseModel, Field
from ..models.task import Task
from ..database.database import get_session, engine
from uuid import UUID


class ListTasksInput(BaseModel):
    """Input schema for the list_tasks tool."""

    user_id: str = Field(..., description="The ID of the user whose tasks to retrieve")
    status: Optional[str] = Field(None, description="Filter tasks by status: 'all', 'pending', or 'completed'")


def list_tasks(input_data: ListTasksInput) -> List[Dict[str, Any]]:
    """
    Retrieve user's tasks with optional status filter.

    Args:
        input_data: Contains user_id and optional status filter

    Returns:
        Array of task objects with id, title, completed status, and other properties
    """
    # Get database session
    with Session(engine) as session:
        # Build query with user_id filter
        query = select(Task).where(Task.user_id == UUID(input_data.user_id))

        # Apply status filter if provided
        if input_data.status:
            status = input_data.status.lower()
            if status == "pending":
                query = query.where(Task.completed == False)
            elif status == "completed":
                query = query.where(Task.completed == True)
            # If status is "all" or any other value, no additional filter is applied

        # Execute query
        result = session.execute(query)
        tasks = result.scalars().all()

        # Convert tasks to dictionary format
        tasks_list = []
        for task in tasks:
            task_dict = {
                "id": str(task.id),
                "title": task.title,
                "completed": task.completed,
                "description": task.description,
                "created_at": task.created_at.isoformat() if task.created_at else None,
                "updated_at": task.updated_at.isoformat() if task.updated_at else None
            }
            tasks_list.append(task_dict)

        return tasks_list