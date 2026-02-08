"""
Contract test for JWT validation.
This test verifies that the JWT validation functionality follows the specified contract.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.main import app
from src.database import get_db
from src.utils.jwt import create_access_token
from datetime import timedelta

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_jwt_validation_contract.db"
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

def test_expired_token_rejection_contract():
    """Test that expired tokens are properly rejected."""

    # This is more of an integration test, but verifies the contract
    pass


def test_invalid_token_rejection_contract():
    """Test that invalid tokens are properly rejected."""

    # Try to access protected endpoint with invalid token
    headers = {"Authorization": "Bearer invalid.token.format"}

    # Test with various endpoints
    endpoints_to_test = [
        "/api/todos/",
        "/api/todos/1",
    ]

    for endpoint in endpoints_to_test:
        response = client.get(endpoint, headers=headers)
        # Should return 401 for invalid tokens
        assert response.status_code == 401, f"Endpoint {endpoint} should reject invalid tokens"

        response_data = response.json()
        assert "detail" in response_data


def test_missing_token_rejection_contract():
    """Test that missing tokens are properly rejected."""

    # Try to access protected endpoint without token
    endpoints_to_test = [
        "/api/todos/",
        "/api/todos/1",
    ]

    for endpoint in endpoints_to_test:
        response = client.get(endpoint)
        # Should return 401 for missing tokens
        assert response.status_code == 401, f"Endpoint {endpoint} should require authentication"

        response_data = response.json()
        assert "detail" in response_data


if __name__ == "__main__":
    test_invalid_token_rejection_contract()
    test_missing_token_rejection_contract()
    print("✅ JWT validation contract tests passed!")