#!/usr/bin/env python3
"""
Direct test of the chat endpoint to see errors - with user creation
"""
import sys
import os
import uuid
from app.routers.chat import chat_endpoint, ChatRequest
from app.models.task import User
from app.database.database import engine
from sqlmodel import Session

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_chat_endpoint():
    print("Testing chat endpoint directly...")
    
    # Create a test user first
    user_id = uuid.UUID("123e4567-e89b-12d3-a456-426614174000")
    
    with Session(engine) as session:
        # Check if user already exists
        existing_user = session.get(User, user_id)
        if not existing_user:
            # Create a test user
            test_user = User(
                id=user_id,
                email="test@example.com",
                password="hashed_password_placeholder"
            )
            session.add(test_user)
            session.commit()
            print(f"Created test user with ID: {user_id}")
        else:
            print(f"Using existing test user with ID: {user_id}")
    
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