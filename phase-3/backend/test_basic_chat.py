from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

# Test the chat endpoint
print("Testing the AI Chatbot functionality...")

# First, register a user
import uuid
unique_email = f"test_{uuid.uuid4()}@example.com"
user_data = {
    "email": unique_email,
    "password": "testpassword123"
}

response = client.post("/api/users/register", json=user_data)
print(f"User registration status: {response.status_code}")
if response.status_code == 200:
    user = response.json()
    user_id = user["id"]
    print(f"Registered user with ID: {user_id}")
    
    # Get JWT token for the user
    login_data = {
        "email": unique_email,
        "password": "testpassword123"
    }
    login_response = client.post("/api/users/login", json=login_data)
    if login_response.status_code == 200:
        token_data = login_response.json()
        token = token_data["access_token"]
        print("Successfully obtained JWT token")
        
        # Test adding a task via the chatbot
        chat_data = {
            "user_id": user_id,
            "message": "Add a task to buy groceries",
            "conversation_id": "test_conv_1"
        }
        
        chat_response = client.post(
            "/api/chat/conversation",
            json=chat_data,
            headers={"Authorization": f"Bearer {token}"}
        )
        
        print(f"Chat endpoint status: {chat_response.status_code}")
        if chat_response.status_code == 200:
            result = chat_response.json()
            print(f"Chat response: {result['response']}")
            print("[SUCCESS] AI Chatbot is working correctly!")
        else:
            print(f"[ERROR] Chat endpoint failed with status: {chat_response.status_code}")
            print(f"Error: {chat_response.text}")
    else:
        print(f"[ERROR] Login failed with status: {login_response.status_code}")
else:
    print(f"[ERROR] Registration failed with status: {response.status_code}")