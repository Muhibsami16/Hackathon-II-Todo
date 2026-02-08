# Quickstart Guide: Frontend Application for Secure Todo Web Platform

## Setup Instructions

### Prerequisites
- Node.js 18+
- npm or yarn package manager
- Access to the backend API endpoint

### Environment Variables
Create a `.env.local` file in the frontend root directory:

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
```

### Installation
1. Navigate to the frontend directory: `cd frontend`
2. Install dependencies: `npm install`
3. Start the development server: `npm run dev`
4. Visit `http://localhost:3000` to access the application

### Configuration
1. Configure Better Auth with your settings in `src/lib/auth.ts`
2. Set up the API client in `src/services/api-client.ts` with proper JWT handling
3. Implement protected route components to handle authentication state

## Development Workflow

1. Start the frontend development server on port 3000
2. Ensure the backend API is running on the configured endpoint
3. Register a new user account or sign in with existing credentials
4. Access the dashboard to manage tasks
5. All API calls will automatically include the JWT token

## Testing the Integration
1. Complete the authentication flow (sign up or sign in)
2. Verify JWT token is stored and attached to API requests
3. Test all 5 task operations (create, read, update, delete, complete)
4. Verify responsive layout on different screen sizes
5. Test navigation between pages while maintaining authentication state