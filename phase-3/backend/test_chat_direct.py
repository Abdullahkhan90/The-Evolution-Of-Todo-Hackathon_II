import requests
import json

# Test the chat endpoint directly
url = "http://127.0.0.1:8000/api/chat/conversation"

payload = {
    "user_id": "123e4567-e89b-12d3-a456-426614174000",
    "message": "Hello"
}

headers = {
    "Content-Type": "application/json"
}

try:
    print("Making request to:", url)
    print("Payload:", json.dumps(payload, indent=2))
    
    response = requests.post(url, json=payload, headers=headers)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code != 200:
        print("Headers received:", dict(response.headers))
        print("Response content:", response.text)
        
except requests.exceptions.ConnectionError:
    print("Connection error - server may not be running on port 8000")
except Exception as e:
    print(f"Error: {e}")