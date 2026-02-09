from fastapi.testclient import TestClient
from app.main import app
from app.database.database import engine
from sqlmodel import SQLModel
from app.models.task import User, Task
from app.core.auth import create_access_token
from uuid import uuid4
import pytest

client = TestClient(app)

@pytest.fixture
def setup_db():
    """Set up test database"""
    SQLModel.metadata.create_all(engine)
    yield
    SQLModel.metadata.drop_all(engine)

def test_create_todo(setup_db):
    """Test creating a new todo"""
    # Create a test user first
    user_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    response = client.post("/api/users/register", json=user_data)
    assert response.status_code == 200
    user = response.json()
    user_id = user["id"]

    # Create a todo
    todo_data = {
        "title": "Test Todo",
        "description": "Test Description",
        "completed": False,
        "priority": "medium",
        "tags": "test,important",
        "due_date": "2024-12-31T10:00:00",
        "recurrence": "none",
        "user_id": user_id
    }

    # Get JWT token for authentication
    token = create_access_token(data={"sub": str(user_id)})

    response = client.post(
        "/api/todos/",
        json=todo_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Todo"
    assert data["description"] == "Test Description"
    assert data["completed"] is False
    assert data["user_id"] == user_id


def test_read_todos(setup_db):
    """Test reading todos with pagination and filtering"""
    # Create a test user first
    user_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    response = client.post("/api/users/register", json=user_data)
    assert response.status_code == 200
    user = response.json()
    user_id = user["id"]

    # Get JWT token for authentication
    token = create_access_token(data={"sub": str(user_id)})

    # Create a todo
    todo_data = {
        "title": "Test Todo",
        "description": "Test Description",
        "completed": False,
        "priority": "medium",
        "tags": "test",
        "due_date": "2024-12-31T10:00:00",
        "recurrence": "none",
        "user_id": user_id
    }

    response = client.post(
        "/api/todos/",
        json=todo_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200

    # Read todos with pagination
    response = client.get(
        "/api/todos/?skip=0&limit=10",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["title"] == "Test Todo"


def test_read_todo_by_id(setup_db):
    """Test reading a specific todo by ID"""
    # Create a test user first
    user_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    response = client.post("/api/users/register", json=user_data)
    assert response.status_code == 200
    user = response.json()
    user_id = user["id"]

    # Get JWT token for authentication
    token = create_access_token(data={"sub": str(user_id)})

    # Create a todo
    todo_data = {
        "title": "Test Todo",
        "description": "Test Description",
        "completed": False,
        "priority": "medium",
        "tags": "test",
        "due_date": "2024-12-31T10:00:00",
        "recurrence": "none",
        "user_id": user_id
    }

    response = client.post(
        "/api/todos/",
        json=todo_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    created_todo = response.json()
    todo_id = created_todo["id"]

    # Read the specific todo
    response = client.get(
        f"/api/todos/{todo_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Todo"
    assert data["id"] == todo_id


def test_update_todo(setup_db):
    """Test updating a todo"""
    # Create a test user first
    user_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    response = client.post("/api/users/register", json=user_data)
    assert response.status_code == 200
    user = response.json()
    user_id = user["id"]

    # Get JWT token for authentication
    token = create_access_token(data={"sub": str(user_id)})

    # Create a todo
    todo_data = {
        "title": "Test Todo",
        "description": "Test Description",
        "completed": False,
        "priority": "medium",
        "tags": "test",
        "due_date": "2024-12-31T10:00:00",
        "recurrence": "none",
        "user_id": user_id
    }

    response = client.post(
        "/api/todos/",
        json=todo_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    created_todo = response.json()
    todo_id = created_todo["id"]

    # Update the todo
    update_data = {
        "title": "Updated Todo",
        "completed": True
    }

    response = client.put(
        f"/api/todos/{todo_id}",
        json=update_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Todo"
    assert data["completed"] is True


def test_delete_todo(setup_db):
    """Test deleting a todo"""
    # Create a test user first
    user_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    response = client.post("/api/users/register", json=user_data)
    assert response.status_code == 200
    user = response.json()
    user_id = user["id"]

    # Get JWT token for authentication
    token = create_access_token(data={"sub": str(user_id)})

    # Create a todo
    todo_data = {
        "title": "Test Todo",
        "description": "Test Description",
        "completed": False,
        "priority": "medium",
        "tags": "test",
        "due_date": "2024-12-31T10:00:00",
        "recurrence": "none",
        "user_id": user_id
    }

    response = client.post(
        "/api/todos/",
        json=todo_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    created_todo = response.json()
    todo_id = created_todo["id"]

    # Delete the todo
    response = client.delete(
        f"/api/todos/{todo_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200

    # Verify the todo is deleted by trying to get it
    response = client.get(
        f"/api/todos/{todo_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 404


def test_todo_authorization(setup_db):
    """Test that users can only access their own todos"""
    # Create first user
    user1_data = {
        "email": "user1@example.com",
        "username": "user1",
        "password": "password123"
    }
    response = client.post("/api/users/register", json=user1_data)
    assert response.status_code == 200
    user1 = response.json()
    user1_id = user1["id"]
    user1_token = create_access_token(data={"sub": str(user1_id)})

    # Create second user
    user2_data = {
        "email": "user2@example.com",
        "username": "user2",
        "password": "password123"
    }
    response = client.post("/api/users/register", json=user2_data)
    assert response.status_code == 200
    user2 = response.json()
    user2_id = user2["id"]
    user2_token = create_access_token(data={"sub": str(user2_id)})

    # Create a todo for user1
    todo_data = {
        "title": "User1 Todo",
        "description": "Test Description",
        "completed": False,
        "priority": "medium",
        "tags": "test",
        "due_date": "2024-12-31T10:00:00",
        "recurrence": "none",
        "user_id": user1_id
    }

    response = client.post(
        "/api/todos/",
        json=todo_data,
        headers={"Authorization": f"Bearer {user1_token}"}
    )
    assert response.status_code == 200
    created_todo = response.json()
    todo_id = created_todo["id"]

    # Try to access user1's todo with user2's token (should fail)
    response = client.get(
        f"/api/todos/{todo_id}",
        headers={"Authorization": f"Bearer {user2_token}"}
    )
    assert response.status_code == 403  # Forbidden

    # Try to update user1's todo with user2's token (should fail)
    update_data = {"title": "Hacked Todo"}
    response = client.put(
        f"/api/todos/{todo_id}",
        json=update_data,
        headers={"Authorization": f"Bearer {user2_token}"}
    )
    assert response.status_code == 403  # Forbidden

    # Try to delete user1's todo with user2's token (should fail)
    response = client.delete(
        f"/api/todos/{todo_id}",
        headers={"Authorization": f"Bearer {user2_token}"}
    )
    assert response.status_code == 403  # Forbidden