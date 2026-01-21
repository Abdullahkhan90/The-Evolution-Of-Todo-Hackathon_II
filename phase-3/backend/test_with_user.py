#!/usr/bin/env python3
"""
Script to create a test user and then test the chat endpoint
"""
import requests
import uuid
import json

BASE_URL = "http://localhost:8001"

def create_test_user():
    """Create a test user for the chat endpoint"""
    user_data = {
        "email": "testuser@example.com",
        "password": "securepassword123"
    }
    
    response = requests.post(f"{BASE_URL}/api/users/register", json=user_data)
    print(f"User registration response: {response.status_code}")
    
    if response.status_code == 200:
        user_info = response.json()
        print(f"Created user: {user_info}")
        return user_info['id']
    else:
        print(f"Failed to create user: {response.text}")
        # Try to get user by logging in if already exists
        login_data = {
            "email": "testuser@example.com",
            "password": "securepassword123"
        }
        login_response = requests.post(f"{BASE_URL}/api/users/login", json=login_data)
        if login_response.status_code == 200:
            user_info = login_response.json()
            print(f"Existing user logged in: {user_info}")
            return user_info.get('user_id')  # Adjust based on actual response
        return None

def test_chat_endpoint(user_id):
    """Test the chat endpoint with the created user"""
    if not user_id:
        print("Cannot test chat endpoint without a valid user ID")
        return
    
    chat_data = {
        "user_id": user_id,
        "message": "Hello, can you help me add a task?",
        "conversation_id": None
    }
    
    print(f"Testing chat endpoint with user_id: {user_id}")
    response = requests.post(f"{BASE_URL}/api/chat/conversation", json=chat_data)
    print(f"Chat endpoint response: {response.status_code}")
    print(f"Response content: {response.text}")
    
    return response

if __name__ == "__main__":
    # First create a test user
    user_id = create_test_user()
    
    # Then test the chat endpoint
    if user_id:
        test_chat_endpoint(user_id)
    else:
        print("Could not get a valid user ID to test the chat endpoint")