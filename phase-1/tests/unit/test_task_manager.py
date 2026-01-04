"""
Unit tests for the TaskManager service.
"""
import pytest
from src.services.task_manager import TaskManager


def test_add_task():
    """Test adding a task."""
    tm = TaskManager()
    task_id = tm.add_task("Test task", "Test description")
    assert task_id == 1
    
    task = tm.get_task(1)
    assert task is not None
    assert task.title == "Test task"
    assert task.description == "Test description"
    assert task.completed is False


def test_get_all_tasks():
    """Test getting all tasks."""
    tm = TaskManager()
    tm.add_task("Task 1", "Description 1")
    tm.add_task("Task 2", "Description 2")
    
    tasks = tm.get_all_tasks()
    assert len(tasks) == 2


def test_update_task():
    """Test updating a task."""
    tm = TaskManager()
    task_id = tm.add_task("Original task", "Original description")
    
    result = tm.update_task(task_id, "Updated task", "Updated description")
    assert result is True
    
    updated_task = tm.get_task(task_id)
    assert updated_task.title == "Updated task"
    assert updated_task.description == "Updated description"


def test_delete_task():
    """Test deleting a task."""
    tm = TaskManager()
    task_id = tm.add_task("Task to delete", "Description")
    
    result = tm.delete_task(task_id)
    assert result is True
    
    task = tm.get_task(task_id)
    assert task is None


def test_mark_task_complete():
    """Test marking a task as complete."""
    tm = TaskManager()
    task_id = tm.add_task("Task to complete", "Description")
    
    result = tm.mark_task_complete(task_id)
    assert result is True
    
    task = tm.get_task(task_id)
    assert task.completed is True


def test_mark_task_incomplete():
    """Test marking a task as incomplete."""
    tm = TaskManager()
    task_id = tm.add_task("Task to mark incomplete", "Description")

    # First mark the task as complete
    result = tm.mark_task_complete(task_id)
    assert result is True

    # Then mark it as incomplete
    result = tm.mark_task_incomplete(task_id)
    assert result is True

    task = tm.get_task(task_id)
    assert task.completed is False