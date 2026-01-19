"""MCP Tool for marking a task as completed."""

from typing import Dict, Any, Optional
from sqlmodel import Session, select
from pydantic import BaseModel, Field
from ..models.task import Task
from ..database.database import get_session, engine
from uuid import UUID
import re


class CompleteTaskInput(BaseModel):
    """Input schema for the complete_task tool."""

    user_id: str = Field(..., description="The ID of the user who owns the task")
    task_id: Optional[str] = Field(None, description="The ID of the task to mark as completed (optional if using title)")
    title: Optional[str] = Field(None, description="The title of the task to mark as completed (partial/fuzzy matching allowed)")


def complete_task(input_data: CompleteTaskInput) -> Dict[str, Any]:
    """
    Mark a task as completed by ID or title.

    Args:
        input_data: Contains user_id and either task_id or title

    Returns:
        Dictionary with task_id, status, and title of the completed task

    Raises:
        ValueError: If the task is not found or doesn't belong to the user
    """
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

            # Debug: print all user tasks
            print(f"DEBUG: All user tasks for matching: {[{'id': str(t.id), 'title': t.title, 'completed': t.completed, 'created_at': str(t.created_at)} for t in all_user_tasks]}")

            # Find all matching tasks with high similarity scores
            matches = []
            threshold = 0.3  # Minimum similarity threshold

            for task_item in all_user_tasks:
                score = calculate_title_similarity(input_data.title.lower(), task_item.title.lower())
                print(f"DEBUG: Comparing '{input_data.title}' with '{task_item.title}', score: {score}")

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

        # Raise error if task not found
        if not task:
            # Get all user tasks to return in error message
            query = select(Task).where(Task.user_id == UUID(input_data.user_id))
            result = session.execute(query)
            all_user_tasks = result.scalars().all()

            all_tasks_titles = [t.title for t in all_user_tasks]
            raise ValueError(f"Could not find a task matching '{input_data.title or input_data.task_id}'. Here are your tasks: {all_tasks_titles}")

        # Update task to completed
        task.completed = True
        session.add(task)
        session.commit()
        session.refresh(task)

        # Return success response
        return {
            "task_id": str(task.id),
            "status": "completed",
            "title": task.title
        }


def calculate_title_similarity(title1: str, title2: str) -> float:
    """
    Calculate similarity between two titles using a simple algorithm.
    Returns a score between 0 and 1 where 1 is perfect match.
    """
    # Clean titles by removing common words and punctuation
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