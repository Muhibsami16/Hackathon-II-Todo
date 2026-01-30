from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.auth_routes import router as auth_router
from src.api.todo_routes import router as todo_router
from sqlmodel import SQLModel
from src.database import engine
import os
from dotenv import load_dotenv

load_dotenv()

# Create the FastAPI app
app = FastAPI(
    title="Todo API",
    description="A secure todo application API with JWT authentication",
    version="1.0.0"
)

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