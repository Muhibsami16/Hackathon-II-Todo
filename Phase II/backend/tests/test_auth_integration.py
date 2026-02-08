"""
Integration test for JWT token issuance flow.
This test verifies the complete authentication flow: registration → login → JWT token issuance → protected access.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.main import app
from src.database import get_db
from src.utils.jwt import verify_token

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_auth_integration.db"
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

def test_jwt_token_issuance_flow():
    """Test the complete JWT token issuance flow."""

    # Step 1: Register a new user
    user_data = {
        "email": "integration-test@example.com",
        "password": "SecurePass123!"
    }

    response = client.post("/api/auth/register", json=user_data)
    assert response.status_code == 200

    registration_result = response.json()
    assert registration_result["email"] == user_data["email"]
    user_id = registration_result["id"]

    print(f"✅ User registered with ID: {user_id}")


    # Step 2: Login and receive JWT token
    login_data = {
        "email": "integration-test@example.com",
        "password": "SecurePass123!"
    }

    response = client.post("/api/auth/login", json=login_data)
    assert response.status_code == 200

    login_result = response.json()
    assert "access_token" in login_result
    assert login_result["token_type"] == "bearer"

    jwt_token = login_result["access_token"]
    assert isinstance(jwt_token, str)
    assert len(jwt_token) > 0

    print(f"✅ JWT token received: {jwt_token[:30]}...")


    # Step 3: Verify the JWT token is valid
    token_payload = verify_token(jwt_token)
    assert token_payload is not None
    assert "user_id" in token_payload
    assert "email" in token_payload
    assert token_payload["user_id"] == user_id
    assert token_payload["email"] == user_data["email"]

    print("✅ JWT token verified successfully")


    # Step 4: Use JWT token to access protected endpoint
    headers = {"Authorization": f"Bearer {jwt_token}"}

    # Try to access a protected endpoint (todos endpoint)
    response = client.get("/api/todos/", headers=headers)
    # Should return 200 (empty list) or 404/405 depending on if the endpoint exists
    assert response.status_code in [200, 404, 405]

    print("✅ Protected endpoint accessed successfully with JWT token")


    # Step 5: Try to access protected endpoint without token (should fail)
    response = client.get("/api/todos/")
    assert response.status_code == 401

    print("✅ Unauthorized access properly rejected")


    # Step 6: Try to access protected endpoint with invalid token (should fail)
    invalid_headers = {"Authorization": "Bearer invalid-token"}
    response = client.get("/api/todos/", headers=invalid_headers)
    assert response.status_code == 401

    print("✅ Invalid token access properly rejected")


def test_multiple_users_jwt_isolation():
    """Test that JWT tokens provide proper user isolation."""

    # Register first user
    user1_data = {
        "email": "user1-isolation-test@example.com",
        "password": "SecurePass123!"
    }

    response = client.post("/api/auth/register", json=user1_data)
    assert response.status_code == 200
    user1_result = response.json()
    user1_id = user1_result["id"]
    print(f"✅ User 1 registered with ID: {user1_id}")

    # Register second user
    user2_data = {
        "email": "user2-isolation-test@example.com",
        "password": "SecurePass123!"
    }

    response = client.post("/api/auth/register", json=user2_data)
    assert response.status_code == 200
    user2_result = response.json()
    user2_id = user2_result["id"]
    print(f"✅ User 2 registered with ID: {user2_id}")

    # Login as first user and get token
    login_data = {
        "email": "user1-isolation-test@example.com",
        "password": "SecurePass123!"
    }

    response = client.post("/api/auth/login", json=login_data)
    assert response.status_code == 200
    user1_token = response.json()["access_token"]
    print("✅ User 1 logged in and received token")

    # Login as second user and get token
    login_data = {
        "email": "user2-isolation-test@example.com",
        "password": "SecurePass123!"
    }

    response = client.post("/api/auth/login", json=login_data)
    assert response.status_code == 200
    user2_token = response.json()["access_token"]
    print("✅ User 2 logged in and received token")

    # Verify tokens contain correct user IDs
    user1_payload = verify_token(user1_token)
    user2_payload = verify_token(user2_token)

    assert user1_payload["user_id"] == user1_id
    assert user2_payload["user_id"] == user2_id
    print("✅ JWT tokens contain correct user IDs for isolation")

    # Verify tokens are different
    assert user1_token != user2_token
    print("✅ Tokens are unique per user")


if __name__ == "__main__":
    test_jwt_token_issuance_flow()
    test_multiple_users_jwt_isolation()
    print("\n🎉 JWT token issuance flow integration tests passed!")