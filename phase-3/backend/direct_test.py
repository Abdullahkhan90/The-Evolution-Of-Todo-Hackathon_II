#!/usr/bin/env python3
"""
Direct test of the chat endpoint to see errors
"""
import sys
import os
import uuid
from app.routers.chat import chat_endpoint, ChatRequest

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_chat_endpoint():
    print("Testing chat endpoint directly...")
    
    # Create a test request
    test_request = ChatRequest(
        user_id="123e4567-e89b-12d3-a456-426614174000",
        message="Hello, can you help me add a task?",
        conversation_id=None
    )
    
    try:
        print("Calling chat endpoint...")
        result = chat_endpoint(test_request)
        print(f"Success! Result: {result}")
    except Exception as e:
        print(f"Error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_chat_endpoint()