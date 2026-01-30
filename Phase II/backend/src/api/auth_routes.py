from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import Annotated
from src.database import get_session
from src.models.user import UserCreate, UserLogin, UserRead
from src.services.auth import register_user, authenticate_user
from src.api.deps import security
from fastapi.security import HTTPBearer

router = APIRouter()
security = HTTPBearer()


@router.post("/register", response_model=UserRead)
def register(user: UserCreate, session: Session = Depends(get_session)):
    """
    Register a new user account.
    """
    try:
        db_user = register_user(user=user, session=session)
        return db_user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/login")
def login(user_login: UserLogin, session: Session = Depends(get_session)):
    """
    Authenticate user and return JWT token.
    """
    user = authenticate_user(
        email=user_login.email,
        password=user_login.password,
        session=session
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    from src.utils.jwt import create_access_token
    from datetime import timedelta

    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"user_id": user.id, "email": user.email},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}