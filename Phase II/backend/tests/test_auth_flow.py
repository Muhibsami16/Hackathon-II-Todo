"""
Test user authentication and JWT token exchange flow.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.main import app
from src.database import get_db

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_auth_flow.db"
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

def test_user_authentication_and_jwt_token_exchange():
    """Test the complete user authentication and JWT token exchange flow."""

    # Register a user
    user_data = {
        "email": "flow-test@example.com",
        "password": "SecurePass123!"
    }

    response = client.post("/api/auth/register", json=user_data)
    assert response.status_code == 200

    # Login to get JWT token
    login_data = {
        "email": "flow-test@example.com",
        "password": "SecurePass123!"
    }

    response = client.post("/api/auth/login", json=login_data)
    assert response.status_code == 200

    result = response.json()
    assert "access_token" in result
    assert result["token_type"] == "bearer"

    print("✅ User authentication and JWT token exchange flow works correctly!")


if __name__ == "__main__":
    test_user_authentication_and_jwt_token_exchange()