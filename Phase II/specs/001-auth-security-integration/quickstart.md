# Quickstart Guide: Authentication and Security Integration

## Setup Instructions

### Prerequisites
- Node.js 18+ for frontend
- Python 3.11+ for backend
- Better Auth configured with JWT plugin
- Shared secret for JWT verification

### Environment Variables
Configure the shared secret for both frontend and backend:

**Backend (.env)**:
```
BETTER_AUTH_SECRET=your-super-secret-jwt-key-here-make-it-long-and-random
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=postgresql://...
```

**Frontend (.env.local)**:
```
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
BETTER_AUTH_SECRET=your-super-secret-jwt-key-here-make-it-long-and-random
```

### Backend Setup
1. Navigate to the backend directory: `cd backend`
2. Install Python dependencies: `pip install fastapi python-jose[cryptography] passlib[bcrypt] python-multipart python-dotenv`
3. Configure JWT utilities in `src/utils/jwt.py`
4. Set up authentication dependency in `src/api/deps.py`
5. Start the server: `uvicorn src.main:app --reload --port 8000`

### Frontend Setup
1. Navigate to the frontend directory: `cd frontend`
2. Install dependencies: `npm install better-auth @better-auth/react`
3. Configure Better Auth with JWT plugin in `src/lib/auth.js`
4. Set up API client with automatic JWT token attachment in `src/services/api-client.js`
5. Start the development server: `npm run dev`
6. Visit `http://localhost:3000` to access the application

## Authentication Flow

1. User registers or logs in via Better Auth
2. Better Auth issues a signed JWT token
3. Frontend stores the token securely
4. API client automatically adds `Authorization: Bearer {token}` to protected requests
5. Backend verifies JWT signature using shared secret
6. Backend extracts user identity from token claims
7. Backend validates user access to requested resources
8. Request is processed with user-specific data filtering

## Testing the Integration
1. Register a new user account
2. Login to receive JWT token
3. Make protected API calls - they should succeed
4. Try API calls without token - they should return 401
5. Try to access other users' data - should return 404