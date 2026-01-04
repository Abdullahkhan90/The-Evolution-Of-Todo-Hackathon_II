"""
Simple test runner for the CLI Todo Application.
"""
import sys
import os
# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import modules directly since we're adding src to path
from models.task import Task
from services.task_manager import TaskManager


def run_task_tests():
    """Run tests for the Task model."""
    print("Running Task model tests...")

    # Test 1: Task creation
    task = Task(id=1, title="Test task", description="Test description", completed=False)
    assert task.id == 1
    assert task.title == "Test task"
    assert task.description == "Test description"
    assert task.completed is False
    print("[PASS] Task creation test passed")

    # Test 2: Task creation with defaults
    task = Task(id=2, title="Test task 2")
    assert task.id == 2
    assert task.title == "Test task 2"
    assert task.description is None
    assert task.completed is False
    print("[PASS] Task creation with defaults test passed")

    # Test 3: Task title validation
    try:
        Task(id=3, title="", description="Test description")
        assert False, "Should raise ValueError for empty title"
    except ValueError:
        print("[PASS] Task title validation test passed")

    try:
        Task(id=4, title="a" * 201, description="Test description")
        assert False, "Should raise ValueError for title too long"
    except ValueError:
        print("[PASS] Task title length validation test passed")


def run_task_manager_tests():
    """Run tests for the TaskManager service."""
    print("\nRunning TaskManager tests...")

    tm = TaskManager()

    # Test 1: Add task
    task_id = tm.add_task("Test task", "Test description")
    assert task_id == 1
    print("[PASS] Add task test passed")

    # Test 2: Get task
    task = tm.get_task(1)
    assert task is not None
    assert task.title == "Test task"
    print("[PASS] Get task test passed")

    # Test 3: Get all tasks
    tm.add_task("Second task", "Second description")
    tasks = tm.get_all_tasks()
    assert len(tasks) == 2
    print("[PASS] Get all tasks test passed")

    # Test 4: Update task
    result = tm.update_task(1, "Updated task", "Updated description")
    assert result is True
    updated_task = tm.get_task(1)
    assert updated_task.title == "Updated task"
    print("[PASS] Update task test passed")

    # Test 5: Mark task complete
    result = tm.mark_task_complete(1)
    assert result is True
    task = tm.get_task(1)
    assert task.completed is True
    print("[PASS] Mark task complete test passed")

    # Test 6: Delete task
    result = tm.delete_task(2)
    assert result is True
    task = tm.get_task(2)
    assert task is None
    print("[PASS] Delete task test passed")


def main():
    """Run all tests."""
    print("Running tests for CLI Todo Application...")

    try:
        run_task_tests()
        run_task_manager_tests()
        print("\n[SUCCESS] All tests passed! The CLI Todo Application is working correctly.")
    except Exception as e:
        print(f"\n[ERROR] Test failed with error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())