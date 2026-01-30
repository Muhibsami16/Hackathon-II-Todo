from fastapi import Request, HTTPException, status
from src.utils.jwt import verify_token
from typing import Dict, Optional
from datetime import datetime


class JWTAuthMiddleware:
    """
    Middleware to handle JWT authentication.

    This middleware is primarily used to verify JWT tokens on protected routes.
    For FastAPI, authentication is typically handled via dependencies rather than middleware,
    but this class is available for more complex authentication scenarios.
    """

    def __init__(self):
        pass

    async def __call__(self, request: Request):
        # Skip authentication for public routes
        if request.url.path in ["/", "/health", "/api/auth/login", "/api/auth/register"]:
            return

        # Extract authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authorization header missing or invalid format",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Extract token
        token = auth_header.split(" ")[1]

        # Verify token
        payload = verify_token(token)
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Check if token has expired (double-checking the expiration)
        exp_timestamp = payload.get("exp")
        if exp_timestamp:
            current_time = datetime.utcnow().timestamp()
            if current_time > exp_timestamp:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token has expired",
                    headers={"WWW-Authenticate": "Bearer"},
                )

        # Add user info to request state
        request.state.user_id = payload.get("user_id")
        request.state.email = payload.get("email")