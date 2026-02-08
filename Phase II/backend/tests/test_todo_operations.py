"""
Test all 5 todo operations (create, read, update, delete, complete) for authenticated users.
This test verifies that authenticated users can perform all todo operations on their own todos.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.src.main import app
from backend.src.database import get_db
from backend.src.models.user import User
from backend.src.utils.jwt import create_access_token
from datetime import timedelta
import json

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

def create_test_user():
    """Helper to create a test user and return their JWT token."""
    # Register a test user
    registration_data = {
        "email": "testuser@example.com",
        "password": "SecurePass123!"
    }

    response = client.post("/api/auth/register", json=registration_data)
    assert response.status_code == 200

    # Login to get JWT token
    login_data = {
        "email": "testuser@example.com",
        "password": "SecurePass123!"
    }

    response = client.post("/api/auth/login", json=login_data)
    assert response.status_code == 200

    token = response.json()["access_token"]
    return token

def test_todo_operations():
    """Test all 5 todo operations: create, read, update, delete, complete."""
    # Get JWT token for authenticated user
    token = create_test_user()
    headers = {"Authorization": f"Bearer {token}"}

    # 1. CREATE: Create a new todo
    todo_data = {
        "title": "Test Todo",
        "description": "This is a test todo item",
        "completed": False
    }

    response = client.post("/api/todos/", json=todo_data, headers=headers)
    assert response.status_code == 200

    created_todo = response.json()
    assert created_todo["title"] == "Test Todo"
    assert created_todo["description"] == "This is a test todo item"
    assert created_todo["completed"] is False
    todo_id = created_todo["id"]

    # 2. READ: Get the created todo
    response = client.get(f"/api/todos/{todo_id}", headers=headers)
    assert response.status_code == 200

    retrieved_todo = response.json()
    assert retrieved_todo["id"] == todo_id
    assert retrieved_todo["title"] == "Test Todo"

    # 3. READ: Get all todos for the user
    response = client.get("/api/todos/", headers=headers)
    assert response.status_code == 200

    todos_list = response.json()
    assert len(todos_list) >= 1
    assert any(todo["id"] == todo_id for todo in todos_list)

    # 4. UPDATE: Modify the todo
    update_data = {
        "title": "Updated Test Todo",
        "description": "This is an updated test todo item",
        "completed": True
    }

    response = client.put(f"/api/todos/{todo_id}", json=update_data, headers=headers)
    assert response.status_code == 200

    updated_todo = response.json()
    assert updated_todo["title"] == "Updated Test Todo"
    assert updated_todo["completed"] is True

    # 5. COMPLETE: Toggle completion status (PATCH operation)
    # First, mark as incomplete
    patch_response = client.patch(f"/api/todos/{todo_id}/complete", params={"completed": False}, headers=headers)
    assert patch_response.status_code == 200

    toggled_todo = patch_response.json()
    assert toggled_todo["completed"] is False

    # Then mark as complete again
    patch_response = client.patch(f"/api/todos/{todo_id}/complete", params={"completed": True}, headers=headers)
    assert patch_response.status_code == 200

    toggled_todo = patch_response.json()
    assert toggled_todo["completed"] is True

    # Verify final state
    response = client.get(f"/api/todos/{todo_id}", headers=headers)
    assert response.status_code == 200

    final_todo = response.json()
    assert final_todo["title"] == "Updated Test Todo"
    assert final_todo["completed"] is True

    # 6. DELETE: Remove the todo
    response = client.delete(f"/api/todos/{todo_id}", headers=headers)
    assert response.status_code == 200

    # Verify the todo is deleted
    response = client.get(f"/api/todos/{todo_id}", headers=headers)
    assert response.status_code == 404

if __name__ == "__main__":
    test_todo_operations()
    print("✅ All 5 todo operations test passed!")