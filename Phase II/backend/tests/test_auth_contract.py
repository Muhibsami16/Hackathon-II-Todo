"""
Contract test for authentication endpoints.
This test verifies that the authentication API endpoints follow the specified contract.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.main import app
from src.database import get_db

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_auth_contract.db"
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

def test_auth_register_endpoint_contract():
    """Test that the register endpoint follows the specified contract."""

    # Test request structure
    user_data = {
        "email": "contract-test@example.com",
        "password": "SecurePass123!"
    }

    response = client.post("/api/auth/register", json=user_data)

    # Should return 200 on successful registration
    assert response.status_code in [200, 400]  # 400 if already exists, 200 if successful

    if response.status_code == 200:
        response_data = response.json()
        # Should return user object with id, email, and timestamps
        assert "id" in response_data
        assert "email" in response_data
        assert response_data["email"] == user_data["email"]
        assert "created_at" in response_data
        assert "updated_at" in response_data


def test_auth_login_endpoint_contract():
    """Test that the login endpoint follows the specified contract."""

    # First register a user
    user_data = {
        "email": "login-contract-test@example.com",
        "password": "SecurePass123!"
    }

    register_response = client.post("/api/auth/register", json=user_data)
    assert register_response.status_code == 200

    # Test login request structure
    login_data = {
        "email": "login-contract-test@example.com",
        "password": "SecurePass123!"
    }

    response = client.post("/api/auth/login", json=login_data)

    # Should return 200 on successful login
    assert response.status_code == 200

    response_data = response.json()
    # Should return access_token and token_type
    assert "access_token" in response_data
    assert "token_type" in response_data
    assert response_data["token_type"] == "bearer"
    assert isinstance(response_data["access_token"], str)


def test_auth_login_invalid_credentials_contract():
    """Test that login returns 401 for invalid credentials."""

    login_data = {
        "email": "nonexistent@example.com",
        "password": "wrongpassword"
    }

    response = client.post("/api/auth/login", json=login_data)

    # Should return 401 for invalid credentials
    assert response.status_code == 401

    response_data = response.json()
    assert "detail" in response_data


def test_auth_register_duplicate_email_contract():
    """Test that register returns 400 for duplicate email."""

    # Register first user
    user_data = {
        "email": "duplicate-test@example.com",
        "password": "SecurePass123!"
    }

    response1 = client.post("/api/auth/register", json=user_data)
    assert response1.status_code == 200

    # Try to register with same email
    response2 = client.post("/api/auth/register", json=user_data)

    # Should return 400 for duplicate email
    assert response2.status_code == 400

    response_data = response2.json()
    assert "detail" in response_data


if __name__ == "__main__":
    test_auth_register_endpoint_contract()
    test_auth_login_endpoint_contract()
    test_auth_login_invalid_credentials_contract()
    test_auth_register_duplicate_email_contract()
    print("✅ Authentication contract tests passed!")