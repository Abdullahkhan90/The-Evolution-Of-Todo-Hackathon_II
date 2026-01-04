"""
Unit tests for the Task model.
"""
import pytest
from src.models.task import Task


def test_task_creation():
    """Test creating a task with valid parameters."""
    task = Task(id=1, title="Test task", description="Test description", completed=False)
    assert task.id == 1
    assert task.title == "Test task"
    assert task.description == "Test description"
    assert task.completed is False


def test_task_creation_defaults():
    """Test creating a task with default parameters."""
    task = Task(id=1, title="Test task")
    assert task.id == 1
    assert task.title == "Test task"
    assert task.description is None
    assert task.completed is False


def test_task_title_validation():
    """Test task title validation."""
    # Test empty title
    try:
        Task(id=1, title="", description="Test description")
        assert False, "Should raise ValueError for empty title"
    except ValueError:
        pass
    
    # Test title too long
    try:
        Task(id=1, title="a" * 201, description="Test description")
        assert False, "Should raise ValueError for title too long"
    except ValueError:
        pass


def test_task_completion_toggle():
    """Test toggling task completion status."""
    task = Task(id=1, title="Test task", completed=False)
    assert task.completed is False
    
    task.completed = True
    assert task.completed is True