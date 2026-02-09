import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session
from sqlmodel.pool import StaticPool
from app.main import app
from app.database.database import get_session
from app.models.task import User, Task
from app.core.auth import create_access_token
from uuid import uuid4


@pytest.fixture(name="client")
def fixture_client():
    # Use in-memory SQLite for testing
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(bind=engine)

    def get_session_override():
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_chat_add_task(client):
    """Test adding a task via the chat endpoint"""
    # Register a user first
    user_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    response = client.post("/api/users/register", json=user_data)
    assert response.status_code == 200
    user = response.json()
    user_id = user["id"]
    
    # Create a JWT token for the user
    token = create_access_token(data={"sub": str(user_id)})
    
    # Test the chat endpoint to add a task
    chat_data = {
        "user_id": user_id,
        "message": "Add a task to buy groceries",
        "conversation_id": "test_conv_1"
    }
    
    response = client.post(
        "/api/chat/conversation",
        json=chat_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    chat_response = response.json()
    assert "buy groceries" in chat_response["response"]
    assert chat_response["conversation_id"] == "test_conv_1"


def test_chat_list_tasks(client):
    """Test listing tasks via the chat endpoint"""
    # Register a user first
    user_data = {
        "email": "test2@example.com",
        "password": "testpassword123"
    }
    
    response = client.post("/api/users/register", json=user_data)
    assert response.status_code == 200
    user = response.json()
    user_id = user["id"]
    
    # Create a JWT token for the user
    token = create_access_token(data={"sub": str(user_id)})
    
    # Add a task first
    chat_data = {
        "user_id": user_id,
        "message": "Add a task to complete project",
        "conversation_id": "test_conv_2"
    }
    
    response = client.post(
        "/api/chat/conversation",
        json=chat_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    
    # Now list the tasks
    chat_data = {
        "user_id": user_id,
        "message": "Show my tasks",
        "conversation_id": "test_conv_2"
    }
    
    response = client.post(
        "/api/chat/conversation",
        json=chat_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    chat_response = response.json()
    assert "complete project" in chat_response["response"]