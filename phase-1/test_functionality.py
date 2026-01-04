"""
Test script to verify all functionality of the CLI Todo Application.
"""
import sys
import os
# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.services.task_manager import TaskManager
from src.ui.cli import CLIInterface


def test_all_functionality():
    """
    Test all functionality of the CLI Todo Application.
    """
    print("Testing CLI Todo Application functionality...")
    
    # Initialize components
    task_manager = TaskManager()
    cli = CLIInterface(task_manager)
    
    # Test 1: Add a task
    result = cli.execute_command('add "Test task 1" "This is a test description"')
    print(f"Add task result: {result}")
    assert "Task added with ID:" in result
    
    # Test 2: Add another task
    result = cli.execute_command('add "Test task 2"')
    print(f"Add second task result: {result}")
    assert "Task added with ID:" in result
    
    # Test 3: List tasks
    result = cli.execute_command('list')
    print(f"List tasks result:\n{result}")
    assert "Test task 1" in result
    assert "Test task 2" in result
    
    # Test 4: Complete a task (assuming the first task got ID 1)
    result = cli.execute_command('complete 1')
    print(f"Complete task result: {result}")
    assert "Task 1 marked as complete" in result
    
    # Test 5: List tasks again to see the completed status
    result = cli.execute_command('list')
    print(f"List tasks after completion:\n{result}")
    assert "[X]" in result  # Should show completed task
    
    # Test 6: Update a task
    result = cli.execute_command('update 2 "Updated task 2" "Updated description"')
    print(f"Update task result: {result}")
    assert "Task 2 updated successfully" in result
    
    # Test 7: List tasks to verify update
    result = cli.execute_command('list')
    print(f"List tasks after update:\n{result}")
    assert "Updated task 2" in result
    
    # Test 8: Delete a task
    result = cli.execute_command('delete 2')
    print(f"Delete task result: {result}")
    assert "Task 2 deleted" in result
    
    # Test 9: List tasks to verify deletion
    result = cli.execute_command('list')
    print(f"List tasks after deletion:\n{result}")
    assert "Updated task 2" not in result  # Should not show the deleted task
    assert "Test task 1" in result  # Should still show the completed task
    
    # Test 10: Try to delete a non-existent task
    result = cli.execute_command('delete 999')
    print(f"Delete non-existent task result: {result}")
    assert "Error: Task with ID 999 not found." in result
    
    # Test 11: Show help
    result = cli.execute_command('help')
    print(f"Help result:\n{result}")
    assert "Available commands:" in result
    
    print("\nAll tests passed! The CLI Todo Application is working correctly.")


if __name__ == "__main__":
    test_all_functionality()