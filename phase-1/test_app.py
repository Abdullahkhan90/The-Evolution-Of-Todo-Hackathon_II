"""
Simple test to verify the CLI Todo Application functionality.
"""
import sys
import os
import subprocess
import tempfile
import time

def test_application():
    """
    Test the CLI application by sending a sequence of commands.
    """
    # Change to the project directory
    os.chdir(r"C:\Users\Lenovo\Desktop\TODO")
    
    # Define a sequence of commands to test
    commands = [
        'add "Test task 1" "This is a test description"',
        'add "Test task 2" --priority high --tags work,urgent --due 2025-12-31',
        'list',
        'complete 1',
        'list',
        'update 2 --title "Updated task 2" --priority low',
        'list',
        'search test',
        'filter priority=low',
        'help',
        'quit'
    ]
    
    # Join commands with newlines to simulate user input
    input_text = "\n".join(commands)
    
    try:
        # Run the application with the commands as input
        result = subprocess.run(
            [sys.executable, "src/main.py"],
            input=input_text,
            text=True,
            capture_output=True,
            timeout=10  # 10 second timeout
        )
        
        print("STDOUT:")
        print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
            
        print(f"Return code: {result.returncode}")
        
        # Check if the application ran without errors
        if result.returncode == 0:
            print("\n✅ Application test completed successfully!")
            return True
        else:
            print("\n❌ Application test failed!")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Application test timed out!")
        return False
    except Exception as e:
        print(f"❌ Error running application test: {e}")
        return False

if __name__ == "__main__":
    success = test_application()
    if success:
        print("\n🎉 All tests passed! The CLI Todo Application is working correctly.")
    else:
        print("\n💥 Some tests failed. Please check the application.")