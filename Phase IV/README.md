# Todo Full-Stack Web Application with JWT Authentication

A secure, multi-user todo web application built with Next.js, FastAPI, SQLModel, Neon PostgreSQL, and Better Auth with JWT.

## Features

- User registration and authentication with JWT tokens
- Secure todo management (create, read, update, delete, complete)
- Multi-user support with strict data isolation
- Responsive web interface
- RESTful API with proper error handling

## Tech Stack

- **Frontend**: Next.js 16+ with App Router
- **Backend**: Python FastAPI
- **ORM**: SQLModel
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: Better Auth with JWT

## Getting Started

### Prerequisites

- Node.js 18+
- Python 3.11+
- PostgreSQL-compatible database (Neon Serverless PostgreSQL)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Set up the backend:
```bash
cd backend
pip install -r requirements.txt
```

3. Set up the frontend:
```bash
cd frontend
npm install
```

4. Configure environment variables:
```bash
# In backend/.env
DATABASE_URL=postgresql://localhost:5432/todo_app
JWT_SECRET_KEY=your-super-secret-jwt-key-here-make-it-long-and-random
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

```bash
# In frontend/.env.local
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
```

### Running the Application

1. Start the backend server:
```bash
cd backend
uvicorn src.main:app --reload --port 8000
```

2. Start the frontend server:
```bash
cd frontend
npm run dev
```

3. Access the application at `http://localhost:3000`

## API Documentation

The backend API documentation is available at `http://localhost:8000/docs` when running in development.

## Architecture

The application follows a clear separation of concerns:
- **Frontend**: Next.js application with authentication and todo management UI
- **Backend**: FastAPI with SQLModel ORM and JWT authentication
- **Database**: Neon PostgreSQL for data persistence
- **Authentication**: JWT-based authentication with user isolation

## Security

- JWT-based authentication with token expiration
- User data isolation at the API level
- Password hashing using bcrypt
- Input validation on both frontend and backend