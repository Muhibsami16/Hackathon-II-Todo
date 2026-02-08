from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from src.api.auth_routes import router as auth_router
from src.api.todo_routes import router as todo_router
from sqlmodel import SQLModel
from src.database import engine
import os
from dotenv import load_dotenv


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Middleware to add security headers to all responses.
    """
    async def dispatch(self, request, call_next):
        response = await call_next(request)

        # Add security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = "default-src 'self'; frame-ancestors 'none'"

        return response

load_dotenv()

# Create the FastAPI app
app = FastAPI(
    title="Todo API",
    description="A secure todo application API with JWT authentication",
    version="1.0.0"
)

# Add security headers middleware first
app.add_middleware(SecurityHeadersMiddleware)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(todo_router, prefix="/api/todos", tags=["todos"])


@app.on_event("startup")
async def startup_event():
    """Initialize the database tables on startup."""
    print("Creating database tables...")
    SQLModel.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo API"}


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "todo-api"}