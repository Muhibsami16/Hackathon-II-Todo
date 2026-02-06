"""
End-to-end test of the complete user workflow.
This test simulates a complete user journey: registration, authentication,
todo operations, and data isolation.
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

def test_complete_user_workflow():
    """
    Test the complete user workflow:
    1. User registers for an account
    2. User logs in and receives a JWT token
    3. User creates multiple todos
    4. User views their todos
    5. User updates a todo
    6. User marks a todo as complete
    7. User deletes a todo
    8. User verifies data isolation from other users
    """

    print("🧪 Starting end-to-end workflow test...")

    # Step 1: User registers for an account
    print("Step 1: Registering user...")
    registration_data = {
        "email": "e2e-test-user@example.com",
        "password": "SecurePass123!"
    }

    response = client.post("/api/auth/register", json=registration_data)
    assert response.status_code == 200, f"Registration failed: {response.text}"

    registration_result = response.json()
    assert "id" in registration_result
    assert registration_result["email"] == "e2e-test-user@example.com"
    print("✅ User registration successful")

    # Step 2: User logs in and receives a JWT token
    print("Step 2: Logging in user...")
    login_data = {
        "email": "e2e-test-user@example.com",
        "password": "SecurePass123!"
    }

    response = client.post("/api/auth/login", json=login_data)
    assert response.status_code == 200, f"Login failed: {response.text}"

    login_result = response.json()
    assert "access_token" in login_result
    assert login_result["token_type"] == "bearer"

    user1_token = login_result["access_token"]
    user1_headers = {"Authorization": f"Bearer {user1_token}"}
    print("✅ User login successful, JWT token received")

    # Step 3: User creates multiple todos
    print("Step 3: Creating multiple todos...")
    todos_to_create = [
        {
            "title": "Buy groceries",
            "description": "Milk, eggs, bread, fruits",
            "completed": False
        },
        {
            "title": "Complete project",
            "description": "Finish the todo application",
            "completed": False
        },
        {
            "title": "Call dentist",
            "description": "Schedule appointment",
            "completed": False
        }
    ]

    created_todo_ids = []
    for i, todo_data in enumerate(todos_to_create):
        response = client.post("/api/todos/", json=todo_data, headers=user1_headers)
        assert response.status_code == 200, f"Failed to create todo {i+1}: {response.text}"

        created_todo = response.json()
        assert created_todo["title"] == todo_data["title"]
        assert created_todo["description"] == todo_data["description"]
        assert created_todo["completed"] == todo_data["completed"]

        created_todo_ids.append(created_todo["id"])
        print(f"✅ Todo '{todo_data['title']}' created with ID {created_todo['id']}")

    # Step 4: User views their todos
    print("Step 4: Viewing user's todos...")
    response = client.get("/api/todos/", headers=user1_headers)
    assert response.status_code == 200, f"Failed to get todos: {response.text}"

    todos_list = response.json()
    assert len(todos_list) == 3, f"Expected 3 todos, got {len(todos_list)}"

    retrieved_todo_ids = [todo["id"] for todo in todos_list]
    for todo_id in created_todo_ids:
        assert todo_id in retrieved_todo_ids, f"Todo ID {todo_id} not found in retrieved list"

    print("✅ User can view all their todos")

    # Step 5: User updates a todo
    print("Step 5: Updating a todo...")
    todo_id_to_update = created_todo_ids[0]
    update_data = {
        "title": "Buy groceries (updated)",
        "description": "Milk, eggs, bread, fruits, vegetables",
        "completed": True
    }

    response = client.put(f"/api/todos/{todo_id_to_update}", json=update_data, headers=user1_headers)
    assert response.status_code == 200, f"Failed to update todo: {response.text}"

    updated_todo = response.json()
    assert updated_todo["title"] == update_data["title"]
    assert updated_todo["description"] == update_data["description"]
    assert updated_todo["completed"] == update_data["completed"]

    print("✅ Todo updated successfully")

    # Step 6: User marks another todo as complete (using PATCH)
    print("Step 6: Marking todo as complete...")
    todo_id_to_complete = created_todo_ids[1]

    response = client.patch(f"/api/todos/{todo_id_to_complete}/complete",
                           params={"completed": True}, headers=user1_headers)
    assert response.status_code == 200, f"Failed to complete todo: {response.text}"

    completed_todo = response.json()
    assert completed_todo["id"] == todo_id_to_complete
    assert completed_todo["completed"] is True

    print("✅ Todo marked as complete successfully")

    # Step 7: User deletes a todo
    print("Step 7: Deleting a todo...")
    todo_id_to_delete = created_todo_ids[2]

    response = client.delete(f"/api/todos/{todo_id_to_delete}", headers=user1_headers)
    assert response.status_code == 200, f"Failed to delete todo: {response.text}"

    delete_result = response.json()
    assert "message" in delete_result
    assert delete_result["message"] == "Todo deleted successfully"

    print("✅ Todo deleted successfully")

    # Verify the deleted todo is gone
    response = client.get(f"/api/todos/{todo_id_to_delete}", headers=user1_headers)
    assert response.status_code == 404, "Deleted todo should not be accessible"

    print("✅ Deleted todo is no longer accessible")

    # Step 8: User verifies data isolation from other users
    print("Step 8: Testing data isolation...")

    # Create a second user
    registration_data2 = {
        "email": "e2e-test-user2@example.com",
        "password": "SecurePass123!"
    }

    response = client.post("/api/auth/register", json=registration_data2)
    assert response.status_code == 200, f"Second user registration failed: {response.text}"

    # Login as second user
    login_data2 = {
        "email": "e2e-test-user2@example.com",
        "password": "SecurePass123!"
    }

    response = client.post("/api/auth/login", json=login_data2)
    assert response.status_code == 200, f"Second user login failed: {response.text}"

    user2_token = response.json()["access_token"]
    user2_headers = {"Authorization": f"Bearer {user2_token}"}

    # Second user creates a todo
    second_user_todo = {
        "title": "Second user's todo",
        "description": "This belongs to user 2",
        "completed": False
    }

    response = client.post("/api/todos/", json=second_user_todo, headers=user2_headers)
    assert response.status_code == 200, f"Second user todo creation failed: {response.text}"

    user2_todo = response.json()
    user2_todo_id = user2_todo["id"]
    print(f"✅ Second user created todo with ID {user2_todo_id}")

    # Verify first user cannot access second user's todo
    response = client.get(f"/api/todos/{user2_todo_id}", headers=user1_headers)
    assert response.status_code == 404, "User 1 should not be able to access User 2's todo"

    print("✅ Data isolation works - User 1 cannot access User 2's todo")

    # Verify second user cannot access first user's remaining todos
    for todo_id in created_todo_ids[:2]:  # Check remaining todos of user 1
        response = client.get(f"/api/todos/{todo_id}", headers=user2_headers)
        assert response.status_code == 404, f"User 2 should not be able to access User 1's todo {todo_id}"

    print("✅ Data isolation works - User 2 cannot access User 1's remaining todos")

    # Clean up: Delete remaining todos for both users
    remaining_user1_todos = [created_todo_ids[0], created_todo_ids[1]]  # First 2 todos (3rd was deleted)
    for todo_id in remaining_user1_todos:
        response = client.delete(f"/api/todos/{todo_id}", headers=user1_headers)
        assert response.status_code in [200, 404]  # Could be 404 if already deleted

    response = client.delete(f"/api/todos/{user2_todo_id}", headers=user2_headers)
    assert response.status_code in [200, 404]  # Could be 404 if already deleted

    print("✅ Cleanup completed")

    print("🎉 End-to-end workflow test completed successfully!")
    print("✅ All steps passed: registration, authentication, todo operations, data isolation")


if __name__ == "__main__":
    test_complete_user_workflow()
    print("\n🚀 All end-to-end tests passed! The complete user workflow is working correctly.")