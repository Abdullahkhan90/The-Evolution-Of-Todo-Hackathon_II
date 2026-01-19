#!/usr/bin/env python3
"""
Test script to verify the chat backend functionality
"""
import requests
import uuid
from datetime import datetime, timedelta
from jose import jwt
import os
import sys
import time
import subprocess
import signal

# Add the parent directory to the path so we can import app modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

def create_test_user():
    """Create a test user for authentication"""
    # This would normally use the API to create a user
    # For testing, we'll create a fake user and generate a token
    from app.core.auth import SECRET_KEY, ALGORITHM
    from datetime import datetime, timedelta

    user_id = str(uuid.uuid4())
    payload = {
        "sub": user_id,
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return user_id, token

def test_chat_endpoint():
    """Test the chat endpoint"""
    base_url = "http://127.0.0.1:8000"

    # Wait a bit for the server to start
    time.sleep(2)

    # Create a test user and token
    user_id, token = create_test_user()

    # Test the chat endpoint
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Prepare the chat request
    chat_data = {
        "user_id": user_id,  # This will be ignored since we use JWT
        "message": "Hello, how can I add a task?",
        "conversation_id": None
    }

    try:
        print("Testing chat endpoint...")
        response = requests.post(
            f"{base_url}/api/chat/conversation",
            json=chat_data,
            headers=headers
        )

        print(f"Response Status: {response.status_code}")
        print(f"Response Body: {response.text}")

        if response.status_code == 200:
            print("✅ SUCCESS: Chat endpoint returned 200 OK!")
            return True
        else:
            print(f"❌ FAILED: Expected 200, got {response.status_code}")
            return False

    except requests.exceptions.ConnectionError:
        print("❌ FAILED: Could not connect to server. Is it running?")
        return False
    except Exception as e:
        print(f"❌ FAILED: Error occurred: {str(e)}")
        return False

if __name__ == "__main__":
    test_chat_endpoint()