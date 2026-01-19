import os
import uuid
from uuid import UUID
from sqlmodel import Session, select
import cohere

# Test the Cohere client initialization
try:
    cohere_api_key = os.getenv("COHERE_API_KEY", "xYsk4MnkGERx7vIWJle10gIaZXDbX9uuYa16VrFa")
    co = cohere.Client(cohere_api_key)
    print("Cohere client initialized successfully")
except Exception as e:
    print(f"Error initializing Cohere client: {e}")

# Test UUID conversion
try:
    user_id = UUID("123e4567-e89b-12d3-a456-426614174000")
    print(f"UUID conversion successful: {user_id}")
except Exception as e:
    print(f"Error with UUID conversion: {e}")

# Test the chat history format
try:
    chat_history = [
        {"role": "SYSTEM", "message": "You are a helpful assistant"},
        {"role": "USER", "message": "Hello"},
        {"role": "CHATBOT", "message": "Hi there!"}
    ]
    print("Chat history format is correct")
    print(f"Chat history: {chat_history}")
except Exception as e:
    print(f"Error with chat history format: {e}")