import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from datetime import datetime, timedelta
from jose import jwt
from app.core.auth import SECRET_KEY, ALGORITHM
import uuid
import requests
import json

# Generate a test token
user_id = str(uuid.uuid4())
payload = {
    "sub": user_id,
    "exp": datetime.utcnow() + timedelta(hours=1)
}
token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

print(f"Generated test token for user: {user_id}")

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
        "http://127.0.0.1:8000/api/chat/conversation",
        json=chat_data,
        headers=headers
    )

    print(f"Response Status: {response.status_code}")
    print(f"Response Body: {response.text}")

    if response.status_code == 200:
        print("✅ SUCCESS: Chat endpoint returned 200 OK!")
    else:
        print(f"❌ FAILED: Expected 200, got {response.status_code}")
        print("This might be due to OpenAI API key not being set.")

except requests.exceptions.ConnectionError:
    print("❌ FAILED: Could not connect to server. Is it running?")
except Exception as e:
    print(f"❌ FAILED: Error occurred: {str(e)}")