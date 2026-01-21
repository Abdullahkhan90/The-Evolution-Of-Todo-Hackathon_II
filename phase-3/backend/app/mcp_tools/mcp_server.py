from mcp import Server
from mcp.types import Tool, ArgumentsSchema, Result
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from sqlmodel import Session, select
from uuid import UUID
import asyncio

from ..models.task import Task, User, Conversation, Message
from ..database.database import engine


# Define the MCP server
server = Server("todo-mcp-server")


# Define tool input schemas
class AddTaskInput(BaseModel):
    user_id: str = Field(..., description="The ID of the user creating the task")
    title: str = Field(..., description="The title of the task")
    description: str = Field("", description="The description of the task (optional)")


class ListTasksInput(BaseModel):
    user_id: str = Field(..., description="The ID of the user whose tasks to retrieve")
    status: Optional[str] = Field(None, description="Filter tasks by status: 'all', 'pending', or 'completed'")


class CompleteTaskInput(BaseModel):
    user_id: str = Field(..., description="The ID of the user who owns the task")
    task_id: Optional[str] = Field(None, description="The ID of the task to mark as completed (optional if using title)")
    title: Optional[str] = Field(None, description="The title of the task to mark as completed (partial/fuzzy matching allowed)")


class DeleteTaskInput(BaseModel):
    user_id: str = Field(..., description="The ID of the user who owns the task")
    task_id: Optional[str] = Field(None, description="The ID of the task to delete (optional if using title)")
    title: Optional[str] = Field(None, description="The title of the task to delete (partial/fuzzy matching allowed)")


class UpdateTaskInput(BaseModel):
    user_id: str = Field(..., description="The ID of the user who owns the task")
    task_id: str = Field(..., description="The ID of the task to update")
    title: Optional[str] = Field(None, description="New title for the task (optional)")
    description: Optional[str] = Field(None, description="New description for the task (optional)")


# Add task tool
@server.tool(
    "add_task",
    description="Create a new task for the logged-in user",
    input_schema=AddTaskInput.model_json_schema(),
)
def handle_add_task(context, params: Dict[str, Any]) -> Result:
    """Handle the add_task tool call."""
    input_data = AddTaskInput(**params)
    
    # Validate input
    if not input_data.title.strip():
        return Result(error="Title cannot be empty")
    
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
        return Result(content=str({
            "task_id": str(new_task.id),
            "status": "created",
            "title": new_task.title
        }))


# List tasks tool
@server.tool(
    "list_tasks",
    description="Retrieve user's tasks with optional status filter",
    input_schema=ListTasksInput.model_json_schema(),
)
def handle_list_tasks(context, params: Dict[str, Any]) -> Result:
    """Handle the list_tasks tool call."""
    input_data = ListTasksInput(**params)
    
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

        return Result(content=str(tasks_list))


# Complete task tool
@server.tool(
    "complete_task",
    description="Mark a task as completed",
    input_schema=CompleteTaskInput.model_json_schema(),
)
def handle_complete_task(context, params: Dict[str, Any]) -> Result:
    """Handle the complete_task tool call."""
    input_data = CompleteTaskInput(**params)

    # Get database session
    with Session(engine) as session:
        task = None

        # If task_id is provided, find by ID
        if input_data.task_id:
            try:
                query = select(Task).where(Task.id == UUID(input_data.task_id)).where(Task.user_id == UUID(input_data.user_id))
                result = session.execute(query)
                task = result.scalar_one_or_none()
            except ValueError:
                # If task_id is not a valid UUID, treat it as a title
                input_data.title = input_data.task_id
                input_data.task_id = None

        # If no task_id or invalid ID, find by title using fuzzy matching
        if not task and input_data.title:
            # Get all tasks for the user
            query = select(Task).where(Task.user_id == UUID(input_data.user_id)).order_by(Task.created_at.desc())  # Order by most recent first
            result = session.execute(query)
            all_user_tasks = result.scalars().all()

            # Find all matching tasks with high similarity scores
            matches = []
            threshold = 0.3  # Minimum similarity threshold

            for task_item in all_user_tasks:
                score = calculate_title_similarity(input_data.title.lower(), task_item.title.lower())

                if score >= threshold:
                    matches.append((task_item, score))

            # Sort matches by similarity score (descending) and then by creation date (most recent first)
            matches.sort(key=lambda x: (-x[1], x[0].created_at.timestamp() if x[0].created_at else 0))

            if matches:
                # Select the best match (highest score, most recent if tied)
                task = matches[0][0]
            else:
                # Also try simple substring matching as a fallback
                substring_matches = []
                for task_item in all_user_tasks:
                    if input_data.title.lower() in task_item.title.lower() or task_item.title.lower() in input_data.title.lower():
                        substring_matches.append(task_item)

                if substring_matches:
                    # Select the most recent match
                    most_recent = max(substring_matches, key=lambda t: t.created_at.timestamp() if t.created_at else 0)
                    task = most_recent

        # Return error if task not found
        if not task:
            # Get all user tasks to return in error message
            query = select(Task).where(Task.user_id == UUID(input_data.user_id))
            result = session.execute(query)
            all_user_tasks = result.scalars().all()

            all_tasks_titles = [t.title for t in all_user_tasks]
            return Result(error=f"Could not find a task matching '{input_data.title or input_data.task_id}'. Here are your tasks: {all_tasks_titles}")

        # Update task to completed
        task.completed = True
        session.add(task)
        session.commit()
        session.refresh(task)

        # Return success response
        return Result(content=str({
            "task_id": str(task.id),
            "status": "completed",
            "title": task.title
        }))


def calculate_title_similarity(title1: str, title2: str) -> float:
    """
    Calculate similarity between two titles using a simple algorithm.
    Returns a score between 0 and 1 where 1 is perfect match.
    """
    # Clean titles by removing common words and punctuation
    import re
    title1_clean = re.sub(r'[^\w\s]', ' ', title1.lower()).strip()
    title2_clean = re.sub(r'[^\w\s]', ' ', title2.lower()).strip()

    # Split into words
    words1 = set(title1_clean.split())
    words2 = set(title2_clean.split())

    # Calculate Jaccard similarity
    intersection = len(words1.intersection(words2))
    union = len(words1.union(words2))

    if union == 0:
        return 0.0

    jaccard_similarity = intersection / union

    # Also check for substring matches
    max_len = max(len(title1), len(title2))
    if max_len > 0:
        if title1 in title2 or title2 in title1:
            # Boost score for substring matches
            return min(1.0, jaccard_similarity + 0.3)

    return jaccard_similarity


# Delete task tool
@server.tool(
    "delete_task",
    description="Remove a task",
    input_schema=DeleteTaskInput.model_json_schema(),
)
def handle_delete_task(context, params: Dict[str, Any]) -> Result:
    """Handle the delete_task tool call."""
    input_data = DeleteTaskInput(**params)

    # Get database session
    with Session(engine) as session:
        task = None

        # If task_id is provided, find by ID
        if input_data.task_id:
            try:
                query = select(Task).where(Task.id == UUID(input_data.task_id)).where(Task.user_id == UUID(input_data.user_id))
                result = session.execute(query)
                task = result.scalar_one_or_none()
            except ValueError:
                # If task_id is not a valid UUID, treat it as a title
                input_data.title = input_data.task_id
                input_data.task_id = None

        # If no task_id or invalid ID, find by title using fuzzy matching
        if not task and input_data.title:
            # Get all tasks for the user
            query = select(Task).where(Task.user_id == UUID(input_data.user_id)).order_by(Task.created_at.desc())  # Order by most recent first
            result = session.execute(query)
            all_user_tasks = result.scalars().all()

            # Find all matching tasks with high similarity scores
            matches = []
            threshold = 0.3  # Minimum similarity threshold

            for task_item in all_user_tasks:
                score = calculate_title_similarity(input_data.title.lower(), task_item.title.lower())

                if score >= threshold:
                    matches.append((task_item, score))

            # Sort matches by similarity score (descending) and then by creation date (most recent first)
            matches.sort(key=lambda x: (-x[1], x[0].created_at.timestamp() if x[0].created_at else 0))

            if matches:
                # Select the best match (highest score, most recent if tied)
                task = matches[0][0]
            else:
                # Also try simple substring matching as a fallback
                substring_matches = []
                for task_item in all_user_tasks:
                    if input_data.title.lower() in task_item.title.lower() or task_item.title.lower() in input_data.title.lower():
                        substring_matches.append(task_item)

                if substring_matches:
                    # Select the most recent match
                    most_recent = max(substring_matches, key=lambda t: t.created_at.timestamp() if t.created_at else 0)
                    task = most_recent

        # Return error if task not found
        if not task:
            # Get all user tasks to return in error message
            query = select(Task).where(Task.user_id == UUID(input_data.user_id))
            result = session.execute(query)
            all_user_tasks = result.scalars().all()

            all_tasks_titles = [t.title for t in all_user_tasks]
            return Result(error=f"Could not find a task matching '{input_data.title or input_data.task_id}'. Here are your tasks: {all_tasks_titles}")

        # Delete the task
        session.delete(task)
        session.commit()

        # Return success response
        return Result(content=str({
            "task_id": str(task.id),
            "status": "deleted",
            "title": task.title
        }))


# Update task tool
@server.tool(
    "update_task",
    description="Modify task title or description",
    input_schema=UpdateTaskInput.model_json_schema(),
)
def handle_update_task(context, params: Dict[str, Any]) -> Result:
    """Handle the update_task tool call."""
    input_data = UpdateTaskInput(**params)
    
    # Get database session
    with Session(engine) as session:
        # Find the task by id and user_id
        query = select(Task).where(Task.id == UUID(input_data.task_id)).where(Task.user_id == UUID(input_data.user_id))
        result = session.execute(query)
        task = result.scalar_one_or_none()

        # Return error if task not found
        if not task:
            return Result(error=f"Task with id {input_data.task_id} not found for user {input_data.user_id}")

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
        return Result(content=str({
            "task_id": str(task.id),
            "status": "updated",
            "title": task.title
        }))