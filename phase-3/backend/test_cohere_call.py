import os
import uuid
from uuid import UUID
import cohere

# Test the exact Cohere call that happens in the endpoint
try:
    cohere_api_key = os.getenv("COHERE_API_KEY", "xYsk4MnkGERx7vIWJle10gIaZXDbX9uuYa16VrFa")
    co = cohere.Client(cohere_api_key)
    
    # Define the system prompt
    system_prompt = """
    You are a helpful AI assistant that manages tasks for users.
    You can add, list, complete, delete, and update tasks.
    Always respond in a friendly, helpful manner.
    """

    # Prepare messages for the Cohere API
    # Combine system prompt with formatted messages
    chat_history = []
    # Add system prompt as the first message
    chat_history.append({"role": "SYSTEM", "message": system_prompt})
    # Add a sample user message
    chat_history.append({"role": "USER", "message": "Hello"})
    
    print("Making Cohere API call...")
    print(f"Chat history: {chat_history}")
    
    # Call the Cohere API
    response = co.chat(
        message="Hello",
        chat_history=chat_history,
        temperature=0.7
    )

    print(f"Response received: {response.text}")
    print("Cohere API call successful!")
    
except Exception as e:
    print(f"Error calling Cohere API: {e}")
    import traceback
    traceback.print_exc()