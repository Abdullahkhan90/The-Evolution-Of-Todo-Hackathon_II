import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from sqlmodel import SQLModel, create_engine, Session
from app.models.task import Task, User, Conversation, Message
from uuid import UUID

# Test database operations
try:
    # Create an in-memory database for testing
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(bind=engine)
    
    print("Database models created successfully")
    
    # Test creating a conversation
    with Session(engine) as session:
        user_id = UUID("123e4567-e89b-12d3-a456-426614174000")
        
        # Create a conversation
        conversation = Conversation(user_id=user_id)
        session.add(conversation)
        session.commit()
        session.refresh(conversation)
        
        print(f"Conversation created with ID: {conversation.id}")
        
        # Create a message
        user_msg = Message(
            user_id=user_id,
            conversation_id=conversation.id,
            role="user",
            content="Hello"
        )
        session.add(user_msg)
        session.commit()
        
        print("Message added successfully")
        
        # Test fetching messages
        from sqlmodel import select
        history_query = select(Message).where(
            Message.conversation_id == conversation.id
        )
        history_result = session.execute(history_query)
        messages = history_result.scalars().all()
        
        print(f"Fetched {len(messages)} messages")
        
        for msg in messages:
            print(f"Message: {msg.role} - {msg.content}")
        
    print("Database operations test successful!")
    
except Exception as e:
    print(f"Error with database operations: {e}")
    import traceback
    traceback.print_exc()