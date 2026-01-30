from fastapi import Depends, HTTPException, status
from sqlmodel import Session
from typing import Generator
from src.database import get_session
from src.models.user import User
from src.utils.jwt import verify_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


security = HTTPBearer()


def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session)
) -> User:
    """Get the current authenticated user from the JWT token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = verify_token(token.credentials)
    if payload is None:
        raise credentials_exception

    user_id: int = payload.get("user_id")
    if user_id is None:
        raise credentials_exception

    # Get user from database
    user = session.get(User, user_id)
    if user is None:
        raise credentials_exception

    return user