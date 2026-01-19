# Test script to check for import and model errors
import sys
import traceback

try:
    print("Testing imports...")
    from app.models.task import User, Task, Conversation, Message
    print("[OK] Models imported successfully")

    from app.routers import chat
    print("[OK] Chat router imported successfully")

    from app.main import app
    print("[OK] Main app imported successfully")

    print("\nTesting database session...")
    from app.database.database import engine
    from sqlmodel import Session
    with Session(engine) as session:
        print("[OK] Database session works")

    print("\nTesting UUID conversion...")
    from uuid import UUID
    user_id = UUID("123e4567-e89b-12d3-a456-426614174000")
    print(f"[OK] UUID conversion works: {user_id}")

    print("\nTesting Cohere client initialization...")
    import os
    import cohere
    cohere_api_key = os.getenv("COHERE_API_KEY", "xYsk4MnkGERx7vIWJle10gIaZXDbX9uuYa16VrFa")
    co = cohere.Client(cohere_api_key)
    print("[OK] Cohere client initializes")

    print("\nAll tests passed! No obvious import or initialization errors.")
    
except Exception as e:
    print(f"Error: {e}")
    traceback.print_exc()