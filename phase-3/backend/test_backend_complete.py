import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

import requests
import json
import time

print("Testing backend functionality...")

# First, let's register a test user
email = f"test_{int(time.time())}@example.com"
password = "password123"
register_data = {
    "email": email,
    "password": password
}

print(f"Registering test user: {email}...")
try:
    register_response = requests.post(
        "http://127.0.0.1:8000/api/users/register",
        json=register_data,
        headers={"Content-Type": "application/json"}
    )
    print(f"Register Response Status: {register_response.status_code}")

    if register_response.status_code == 200:
        print("Registration successful")
        print(f"Register Response: {register_response.text}")
    else:
        print(f"Registration failed: {register_response.text}")
        # Continue anyway in case user already exists
        if register_response.status_code == 400:
            print("User might already exist, proceeding to login...")

    # Now login to get the token
    login_data = {
        "email": email,
        "password": password
    }

    login_response = requests.post(
        "http://127.0.0.1:8000/api/users/login",
        json=login_data,
        headers={"Content-Type": "application/json"}
    )

    print(f"Login Response Status: {login_response.status_code}")
    if login_response.status_code == 200:
        login_response_json = login_response.json()
        print(f"Login Response: {json.dumps(login_response_json, indent=2)}")
        token = login_response_json.get("access_token")
    else:
        print(f"Login failed: {login_response.text}")
        token = None

    if token:
        print("Successfully obtained token")

        # Now test the chat endpoint
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        # Prepare the chat request
        chat_data = {
            "user_id": "ignored_due_to_jwt",  # This will be ignored since we use JWT
            "message": "Hello, how can I add a task?",
            "conversation_id": None
        }

        print("Testing chat endpoint...")
        response = requests.post(
            "http://127.0.0.1:8000/api/chat/conversation",
            json=chat_data,
            headers=headers
        )

        print(f"Chat Response Status: {response.status_code}")
        print(f"Chat Response Body: {response.text}")

        if response.status_code == 200:
            print("SUCCESS: Chat endpoint returned 200 OK!")
        elif response.status_code == 500:
            print("Got 500 error - this might be due to OpenAI API configuration, but authentication is working.")
        else:
            print(f"Got {response.status_code} - this indicates an issue with the endpoint.")
    else:
        print("Failed to obtain token for chat endpoint test")

except requests.exceptions.ConnectionError:
    print("FAILED: Could not connect to server. Is it running?")
except Exception as e:
    print(f"FAILED: Error occurred: {str(e)}")