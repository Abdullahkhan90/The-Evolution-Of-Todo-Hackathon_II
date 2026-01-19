import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session
from sqlmodel.pool import StaticPool
from app.main import app
from app.database.database import get_session
from app.models.task import User, Task, Conversation, Message
from app.core.auth import create_access_token
from uuid import uuid4


@pytest.fixture(name="client")
def fixture_client():
    """Create a test client with an in-memory database."""
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


def test_chat_endpoint_exists(client):
    """Test that the chat endpoint exists and returns proper status."""
    # Register a user first
    user_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    response = client.post("/api/users/register", json=user_data)
    assert response.status_code == 200
    user = response.json()
    user_id = user["id"]
    
    # Test the chat endpoint
    chat_data = {
        "user_id": user_id,
        "message": "Add a task to buy groceries",
        "conversation_id": None
    }
    
    response = client.post(
        "/api/chat/conversation",
        json=chat_data
    )
    
    # Should return 401 because we didn't provide authentication
    assert response.status_code == 401


def test_database_models_exist():
    """Test that all required database models exist."""
    # Check that all required models are defined
    assert hasattr(User, 'id')
    assert hasattr(User, 'email')
    assert hasattr(User, 'password')
    
    assert hasattr(Task, 'id')
    assert hasattr(Task, 'title')
    assert hasattr(Task, 'completed')
    assert hasattr(Task, 'user_id')
    
    assert hasattr(Conversation, 'id')
    assert hasattr(Conversation, 'user_id')
    
    assert hasattr(Message, 'id')
    assert hasattr(Message, 'user_id')
    assert hasattr(Message, 'conversation_id')
    assert hasattr(Message, 'role')
    assert hasattr(Message, 'content')


def test_mcp_tools_exist():
    """Test that MCP tools are properly defined."""
    from app.mcp_tools.mcp_server import server
    
    # Check that all required tools are registered
    tool_names = [tool.name for tool in server.tools]
    required_tools = ["add_task", "list_tasks", "complete_task", "delete_task", "update_task"]
    
    for tool in required_tools:
        assert tool in tool_names, f"Missing MCP tool: {tool}"