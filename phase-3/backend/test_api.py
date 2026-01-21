"""
Basic test file to verify the API structure works correctly.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Todo API"}

def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_api_docs():
    """Test that API docs are available"""
    response = client.get("/docs")
    assert response.status_code == 200

def test_api_redoc():
    """Test that ReDoc is available"""
    response = client.get("/redoc")
    assert response.status_code == 200

if __name__ == "__main__":
    pytest.main([__file__])