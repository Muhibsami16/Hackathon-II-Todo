"""
Test that unauthorized API calls return 401 status codes.
This test verifies that protected endpoints properly reject requests without valid JWT tokens.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.src.main import app
from backend.src.database import get_db

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_unauthorized_api_calls():
    """Test that unauthorized API calls return 401 status codes."""

    # Test GET /api/todos/ without token
    response = client.get("/api/todos/")
    assert response.status_code == 401

    # Test GET /api/todos/{id} without token
    response = client.get("/api/todos/1")
    assert response.status_code == 401

    # Test POST /api/todos/ without token
    todo_data = {
        "title": "Unauthorized Todo",
        "description": "This should fail without auth",
        "completed": False
    }
    response = client.post("/api/todos/", json=todo_data)
    assert response.status_code == 401

    # Test PUT /api/todos/{id} without token
    update_data = {
        "title": "Updated Unauthorized Todo",
        "completed": True
    }
    response = client.put("/api/todos/1", json=update_data)
    assert response.status_code == 401

    # Test PATCH /api/todos/{id}/complete without token
    response = client.patch("/api/todos/1/complete", params={"completed": True})
    assert response.status_code == 401

    # Test DELETE /api/todos/{id} without token
    response = client.delete("/api/todos/1")
    assert response.status_code == 401

def test_invalid_token_handling():
    """Test that invalid JWT tokens are properly rejected."""

    # Create various invalid token scenarios
    invalid_headers_list = [
        {"Authorization": "Bearer"},  # Token missing
        {"Authorization": "Bearer invalid-token"},  # Invalid token format
        {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.invalid.invalid"},  # Malformed JWT
        {"Authorization": "Basic dXNlcjpwYXNzd29yZA=="},  # Wrong auth scheme
    ]

    for headers in invalid_headers_list:
        # Test GET /api/todos/ with invalid token
        response = client.get("/api/todos/", headers=headers)
        # Should return 401 for invalid tokens
        assert response.status_code == 401, f"Failed for headers: {headers}"

        # Test POST /api/todos/ with invalid token
        todo_data = {
            "title": "Unauthorized Todo",
            "description": "This should fail with invalid token",
            "completed": False
        }
        response = client.post("/api/todos/", json=todo_data, headers=headers)
        assert response.status_code == 401, f"Failed for headers: {headers}"

def test_valid_token_still_works():
    """Test that valid tokens continue to work properly."""

    # Register a test user
    registration_data = {
        "email": "validtoken@example.com",
        "password": "SecurePass123!"
    }

    response = client.post("/api/auth/register", json=registration_data)
    assert response.status_code == 200

    # Login to get JWT token
    login_data = {
        "email": "validtoken@example.com",
        "password": "SecurePass123!"
    }

    response = client.post("/api/auth/login", json=login_data)
    assert response.status_code == 200

    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Test that valid token allows access to protected endpoints
    response = client.get("/api/todos/", headers=headers)
    # Should return 200 (empty list) instead of 401
    assert response.status_code == 200

    # Create a todo with valid token
    todo_data = {
        "title": "Valid Token Todo",
        "description": "Created with valid token",
        "completed": False
    }

    response = client.post("/api/todos/", json=todo_data, headers=headers)
    assert response.status_code == 200

    # Get the created todo
    created_todo = response.json()
    todo_id = created_todo["id"]

    response = client.get(f"/api/todos/{todo_id}", headers=headers)
    assert response.status_code == 200

    # Clean up
    response = client.delete(f"/api/todos/{todo_id}", headers=headers)
    assert response.status_code == 200

if __name__ == "__main__":
    test_unauthorized_api_calls()
    test_invalid_token_handling()
    test_valid_token_still_works()
    print("✅ Unauthorized API access tests passed!")