"""
Integration test for multi-user data access and isolation.
This test verifies that users can only access their own data.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.main import app
from src.database import get_db
from src.models.todo import TodoCreate

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_isolation_integration.db"
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

def test_multi_user_data_isolation():
    """Test that users can only access their own data."""

    # Register first user
    user1_data = {
        "email": "user1-isolation@example.com",
        "password": "SecurePass123!"
    }

    response = client.post("/api/auth/register", json=user1_data)
    assert response.status_code == 200
    user1_result = response.json()
    user1_id = user1_result["id"]
    print(f"✅ User 1 registered with ID: {user1_id}")

    # Login as first user to get token
    login_data = {
        "email": "user1-isolation@example.com",
        "password": "SecurePass123!"
    }

    response = client.post("/api/auth/login", json=login_data)
    assert response.status_code == 200
    user1_token = response.json()["access_token"]
    user1_headers = {"Authorization": f"Bearer {user1_token}"}
    print("✅ User 1 logged in and got token")

    # Register second user
    user2_data = {
        "email": "user2-isolation@example.com",
        "password": "SecurePass123!"
    }

    response = client.post("/api/auth/register", json=user2_data)
    assert response.status_code == 200
    user2_result = response.json()
    user2_id = user2_result["id"]
    print(f"✅ User 2 registered with ID: {user2_id}")

    # Login as second user to get token
    login_data = {
        "email": "user2-isolation@example.com",
        "password": "SecurePass123!"
    }

    response = client.post("/api/auth/login", json=login_data)
    assert response.status_code == 200
    user2_token = response.json()["access_token"]
    user2_headers = {"Authorization": f"Bearer {user2_token}"}
    print("✅ User 2 logged in and got token")

    # User 1 creates a todo
    todo1_data = {
        "title": "User 1's Todo",
        "description": "This belongs to user 1",
        "completed": False
    }

    response = client.post("/api/todos/", json=todo1_data, headers=user1_headers)
    assert response.status_code in [200, 201]  # May return 200 or 201 depending on implementation
    user1_todo = response.json()
    user1_todo_id = user1_todo["id"]
    print(f"✅ User 1 created todo with ID: {user1_todo_id}")

    # User 2 creates a todo
    todo2_data = {
        "title": "User 2's Todo",
        "description": "This belongs to user 2",
        "completed": False
    }

    response = client.post("/api/todos/", json=todo2_data, headers=user2_headers)
    assert response.status_code in [200, 201]
    user2_todo = response.json()
    user2_todo_id = user2_todo["id"]
    print(f"✅ User 2 created todo with ID: {user2_todo_id}")

    # Verify User 1 can access their own todo
    response = client.get(f"/api/todos/{user1_todo_id}", headers=user1_headers)
    assert response.status_code == 200
    print("✅ User 1 can access their own todo")

    # Verify User 2 can access their own todo
    response = client.get(f"/api/todos/{user2_todo_id}", headers=user2_headers)
    assert response.status_code == 200
    print("✅ User 2 can access their own todo")

    # Verify User 1 cannot access User 2's todo
    response = client.get(f"/api/todos/{user2_todo_id}", headers=user1_headers)
    assert response.status_code == 404  # Should return 404, not 403, to prevent user enumeration
    print("✅ User 1 cannot access User 2's todo (returns 404)")

    # Verify User 2 cannot access User 1's todo
    response = client.get(f"/api/todos/{user1_todo_id}", headers=user2_headers)
    assert response.status_code == 404  # Should return 404, not 403, to prevent user enumeration
    print("✅ User 2 cannot access User 1's todo (returns 404)")

    # Verify each user can only see their own todos in the list
    response = client.get("/api/todos/", headers=user1_headers)
    assert response.status_code == 200
    user1_todos = response.json()

    user1_todo_ids = [todo["id"] for todo in user1_todos]
    assert user1_todo_id in user1_todo_ids
    assert user2_todo_id not in user1_todo_ids
    print("✅ User 1 only sees their own todos in the list")

    response = client.get("/api/todos/", headers=user2_headers)
    assert response.status_code == 200
    user2_todos = response.json()

    user2_todo_ids = [todo["id"] for todo in user2_todos]
    assert user2_todo_id in user2_todo_ids
    assert user1_todo_id not in user2_todo_ids
    print("✅ User 2 only sees their own todos in the list")

    # Test update isolation - User 1 cannot update User 2's todo
    update_data = {
        "title": "Hacked Todo",
        "description": "User 1 tried to update User 2's todo",
        "completed": True
    }
    response = client.put(f"/api/todos/{user2_todo_id}", json=update_data, headers=user1_headers)
    assert response.status_code == 404  # Should return 404 to prevent enumeration
    print("✅ User 1 cannot update User 2's todo (returns 404)")

    # Test delete isolation - User 1 cannot delete User 2's todo
    response = client.delete(f"/api/todos/{user2_todo_id}", headers=user1_headers)
    assert response.status_code == 404  # Should return 404 to prevent enumeration
    print("✅ User 1 cannot delete User 2's todo (returns 404)")

    # Clean up: Both users delete their own todos
    response = client.delete(f"/api/todos/{user1_todo_id}", headers=user1_headers)
    assert response.status_code in [200, 204]

    response = client.delete(f"/api/todos/{user2_todo_id}", headers=user2_headers)
    assert response.status_code in [200, 204]

    print("✅ Multi-user data isolation verified successfully!")


if __name__ == "__main__":
    test_multi_user_data_isolation()
    print("\n🎉 Multi-user data access isolation tests passed!")