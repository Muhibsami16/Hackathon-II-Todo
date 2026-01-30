from sqlmodel import Session, select
from src.models.user import User, UserCreate
from src.utils.jwt import get_password_hash, verify_password
from typing import Optional


def register_user(user: UserCreate, session: Session) -> User:
    """
    Register a new user.

    Args:
        user: UserCreate object with email and password
        session: Database session

    Returns:
        User: The created user object

    Raises:
        ValueError: If email already exists
    """
    # Check if user already exists
    existing_user = session.exec(select(User).where(User.email == user.email)).first()
    if existing_user:
        raise ValueError("Email already registered")

    # Create new user
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        hashed_password=hashed_password
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


def authenticate_user(email: str, password: str, session: Session) -> Optional[User]:
    """
    Authenticate a user by email and password.

    Args:
        email: User's email
        password: User's password
        session: Database session

    Returns:
        User: The authenticated user object, or None if authentication fails
    """
    user = session.exec(select(User).where(User.email == email)).first()

    if not user or not verify_password(password, user.hashed_password):
        return None

    return user