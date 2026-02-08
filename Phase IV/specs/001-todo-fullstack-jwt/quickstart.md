# Quickstart Guide: Todo Full-Stack Web Application

## Setup Instructions

### Prerequisites
- Node.js 18+ for frontend
- Python 3.11+ for backend
- PostgreSQL-compatible database (Neon Serverless PostgreSQL)
- Better Auth configured with JWT plugin

### Environment Variables
Create `.env` files for both frontend and backend:

**Backend (.env)**:
```
DATABASE_URL=postgresql://username:password@localhost:5432/todo_app
JWT_SECRET_KEY=your-super-secret-jwt-key-here-make-it-long-and-random
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**Frontend (.env.local)**:
```
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
```

### Backend Setup
1. Navigate to the backend directory: `cd backend`
2. Install Python dependencies: `pip install fastapi sqlmodel python-jose[cryptography] passlib[bcrypt] python-multipart python-dotenv`
3. Initialize the database: `python -c "from src.main import create_db_and_tables; create_db_and_tables()"`
4. Start the server: `uvicorn src.main:app --reload --port 8000`

### Frontend Setup
1. Navigate to the frontend directory: `cd frontend`
2. Install dependencies: `npm install`
3. Start the development server: `npm run dev`
4. Visit `http://localhost:3000` to access the application

## Development Workflow

1. Start backend server on port 8000
2. Start frontend server on port 3000
3. Register a new user account
4. Log in to receive JWT token
5. Access todo functionality through the dashboard

## API Testing
- Backend API documentation available at `http://localhost:8000/docs`
- Use the API explorer to test endpoints with proper JWT authentication