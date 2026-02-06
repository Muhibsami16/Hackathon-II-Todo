"""
Integration test for JWT expiration handling.
This test verifies that expired tokens are properly rejected.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.main import app
from src.database import get_db
from src.utils.jwt import create_access_token
from datetime import timedelta, datetime
from jose import jwt
import os
from dotenv import load_dotenv

load_dotenv()

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_jwt_expiration_integration.db"
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
    SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", os.getenv("JWT_SECRET_KEY", "fallback-secret"))
    ALGORITHM = os.getenv("ALGORITHM", "HS256")

    # Create a token with expiration in the past
    data = {"user_id": 999, "email": "expired@example.com"}
    expire = datetime.utcnow() - timedelta(minutes=10)  # Expired 10 minutes ago
    data.update({"exp": expire})

    expired_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return expired_token


def test_expired_token_rejection():
    """Test that expired JWT tokens are rejected."""

    # Create an expired token
    expired_token = create_expired_token()
    headers = {"Authorization": f"Bearer {expired_token}"}

    # Try to access protected endpoints with expired token
    endpoints_to_test = [
        "/api/todos/",
        "/api/todos/1",
    ]

    for endpoint in endpoints_to_test:
        response = client.get(endpoint, headers=headers)
        assert response.status_code == 401, f"Expired token should be rejected for endpoint {endpoint}"

        response_data = response.json()
        assert "detail" in response_data


def test_valid_token_acceptance():
    """Test that valid tokens are accepted."""

    # Register a test user
    user_data = {
        "email": "valid-token-test@example.com",
        "password": "SecurePass123!"
    }

    response = client.post("/api/auth/register", json=user_data)
    assert response.status_code == 200

    # Login to get a valid token
    login_data = {
        "email": "valid-token-test@example.com",
        "password": "SecurePass123!"
    }

    response = client.post("/api/auth/login", json=login_data)
    assert response.status_code == 200

    valid_token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {valid_token}"}

    # Valid token should work for protected endpoints
    response = client.get("/api/todos/", headers=headers)
    assert response.status_code in [200, 404, 405], "Valid token should be accepted"


def test_malformed_token_rejection():
    """Test that malformed tokens are rejected."""

    malformed_headers_list = [
        {"Authorization": "Bearer"},  # Token missing
        {"Authorization": "Bearer invalid-token"},  # Invalid token format
        {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.invalid.invalid"},  # Malformed JWT
        {"Authorization": "Basic dXNlcjpwYXNzd29yZA=="},  # Wrong auth scheme
    ]

    for headers in malformed_headers_list:
        # Test with a protected endpoint
        response = client.get("/api/todos/", headers=headers)
        # Should return 401 for invalid/malformed tokens
        assert response.status_code == 401, f"Malformed token should be rejected: {headers}"


if __name__ == "__main__":
    test_expired_token_rejection()
    test_valid_token_acceptance()
    test_malformed_token_rejection()
    print("✅ JWT expiration handling integration tests passed!")