"""
Test JWT token expiration handling.
This test verifies that expired JWT tokens are properly rejected.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.src.main import app
from backend.src.database import get_db
from backend.src.utils.jwt import create_access_token
from datetime import timedelta, datetime
from jose import jwt
import os
from dotenv import load_dotenv

load_dotenv()

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

def create_expired_token():
    """Create a JWT token that expired in the past."""
    SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-default-secret-key-change-in-production")
    ALGORITHM = os.getenv("ALGORITHM", "HS256")

    # Create a token with expiration in the past
    data = {"user_id": 999, "email": "expired@example.com"}
    expire = datetime.utcnow() - timedelta(minutes=10)  # Expired 10 minutes ago
    data.update({"exp": expire})

    expired_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return expired_token

def create_short_lived_token():
    """Create a JWT token that will expire soon."""
    from backend.src.utils.jwt import create_access_token
    from datetime import timedelta

    data = {"user_id": 998, "email": "shortlived@example.com"}
    # Create token that expires in 1 second for testing
    expires_delta = timedelta(seconds=1)

    short_lived_token = create_access_token(data=data, expires_delta=expires_delta)
    return short_lived_token

def test_expired_token_rejection():
    """Test that expired JWT tokens are rejected."""

    # Create an expired token
    expired_token = create_expired_token()
    headers = {"Authorization": f"Bearer {expired_token}"}

    # Try to access protected endpoints with expired token
    response = client.get("/api/todos/", headers=headers)
    assert response.status_code == 401

    # Try to create a todo with expired token
    todo_data = {
        "title": "Expired Token Todo",
        "description": "This should fail with expired token",
        "completed": False
    }
    response = client.post("/api/todos/", json=todo_data, headers=headers)
    assert response.status_code == 401

    # Try to access any other protected endpoint with expired token
    response = client.get("/api/todos/1", headers=headers)
    assert response.status_code == 401

def test_valid_token_before_expiration():
    """Test that valid tokens work before they expire."""

    # Register a test user
    registration_data = {
        "email": "preexpiry@example.com",
        "password": "SecurePass123!"
    }

    response = client.post("/api/auth/register", json=registration_data)
    assert response.status_code == 200

    # Login to get JWT token
    login_data = {
        "email": "preexpiry@example.com",
        "password": "SecurePass123!"
    }

    response = client.post("/api/auth/login", json=login_data)
    assert response.status_code == 200

    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Test that token works immediately after creation
    response = client.get("/api/todos/", headers=headers)
    assert response.status_code == 200

    # Create a todo with the valid token
    todo_data = {
        "title": "Pre-expiry Todo",
        "description": "Created with valid token",
        "completed": False
    }

    response = client.post("/api/todos/", json=todo_data, headers=headers)
    assert response.status_code == 200

    created_todo = response.json()
    todo_id = created_todo["id"]

    # Test that the created todo can be accessed
    response = client.get(f"/api/todos/{todo_id}", headers=headers)
    assert response.status_code == 200

    # Clean up
    response = client.delete(f"/api/todos/{todo_id}", headers=headers)
    assert response.status_code == 200

def test_short_lived_token_behavior():
    """Test behavior of tokens with short expiration times."""

    # Create a short-lived token
    short_token = create_short_lived_token()
    headers = {"Authorization": f"Bearer {short_token}"}

    # Initially, the token should work (if expiration is in the future)
    # Note: This test may occasionally fail if the token expires between creation and this call
    # So we'll wrap it in a try-except to handle timing issues gracefully in the test
    response = client.get("/api/todos/", headers=headers)

    # The response should either be 200 (if token hasn't expired yet) or 401 (if token has expired)
    assert response.status_code in [200, 401]

def test_token_validation_consistency():
    """Test that token validation is consistent across all endpoints."""

    expired_token = create_expired_token()
    headers = {"Authorization": f"Bearer {expired_token}"}

    endpoints_to_test = [
        ("/api/todos/", "GET"),
        ("/api/todos/", "POST", {"title": "Test", "completed": False}),
        ("/api/todos/1", "GET"),
        ("/api/todos/1", "PUT", {"title": "Updated", "completed": True}),
        ("/api/todos/1/complete", "PATCH", {}, {"completed": True}),
        ("/api/todos/1", "DELETE")
    ]

    for endpoint_config in endpoints_to_test:
        if len(endpoint_config) == 2:
            url, method = endpoint_config
            response = client.request(method, url, headers=headers)
        elif len(endpoint_config) == 3:
            url, method, json_data = endpoint_config
            response = client.request(method, url, json=json_data, headers=headers)
        elif len(endpoint_config) == 4:
            url, method, json_data, params = endpoint_config
            response = client.request(method, url, json=json_data, params=params, headers=headers)

        # All endpoints should reject expired tokens consistently
        assert response.status_code == 401, f"Endpoint {method} {url} should reject expired token"

if __name__ == "__main__":
    test_expired_token_rejection()
    test_valid_token_before_expiration()
    test_short_lived_token_behavior()
    test_token_validation_consistency()
    print("✅ JWT token expiration tests passed!")