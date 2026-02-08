# Todo API Documentation

## Base URL
All API endpoints are prefixed with `/api`.

## Authentication
Most endpoints require authentication using JWT tokens. Include the token in the Authorization header:
```
Authorization: Bearer <your-jwt-token>
```

## Endpoints

### Authentication

#### POST /api/auth/register
Register a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

**Response (200):**
```json
{
  "id": 1,
  "email": "user@example.com",
  "created_at": "2026-01-30T10:00:00Z",
  "updated_at": "2026-01-30T10:00:00Z"
}
```

**Response (400):**
```json
{
  "detail": "Email already exists"
}
```

#### POST /api/auth/login
Authenticate user and return JWT token.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

**Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Response (401):**
```json
{
  "detail": "Incorrect email or password"
}
```

### Todo Operations

#### GET /api/todos/
Retrieve all todos for the authenticated user.

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Response (200):**
```json
[
  {
    "id": 1,
    "title": "Complete project",
    "description": "Finish the todo application",
    "completed": false,
    "user_id": 1,
    "created_at": "2026-01-30T10:00:00Z",
    "updated_at": "2026-01-30T10:00:00Z"
  }
]
```

#### POST /api/todos/
Create a new todo for the authenticated user.

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Request Body:**
```json
{
  "title": "New task",
  "description": "Task description",
  "completed": false
}
```

**Response (200):**
```json
{
  "id": 2,
  "title": "New task",
  "description": "Task description",
  "completed": false,
  "user_id": 1,
  "created_at": "2026-01-30T11:00:00Z",
  "updated_at": "2026-01-30T11:00:00Z"
}
```

#### GET /api/todos/{id}
Retrieve a specific todo for the authenticated user.

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Response (200):**
```json
{
  "id": 1,
  "title": "Complete project",
  "description": "Finish the todo application",
  "completed": false,
  "user_id": 1,
  "created_at": "2026-01-30T10:00:00Z",
  "updated_at": "2026-01-30T10:00:00Z"
}
```

**Response (404):**
```json
{
  "detail": "Todo not found"
}
```

#### PUT /api/todos/{id}
Update an existing todo for the authenticated user.

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Request Body:**
```json
{
  "title": "Updated task",
  "description": "Updated description",
  "completed": true
}
```

**Response (200):**
```json
{
  "id": 1,
  "title": "Updated task",
  "description": "Updated description",
  "completed": true,
  "user_id": 1,
  "created_at": "2026-01-30T10:00:00Z",
  "updated_at": "2026-01-30T12:00:00Z"
}
```

#### PATCH /api/todos/{id}/complete
Toggle the completion status of a todo for the authenticated user.

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Query Parameters:**
- `completed`: boolean value (true/false)

**Response (200):**
```json
{
  "id": 1,
  "title": "Complete project",
  "description": "Finish the todo application",
  "completed": true,
  "user_id": 1,
  "created_at": "2026-01-30T10:00:00Z",
  "updated_at": "2026-01-30T13:00:00Z"
}
```

#### DELETE /api/todos/{id}
Delete a specific todo for the authenticated user.

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Response (200):**
```json
{
  "message": "Todo deleted successfully"
}
```

**Response (404):**
```json
{
  "detail": "Todo not found"
}
```

## Error Responses

All error responses follow this format:
```json
{
  "detail": "Error message describing what went wrong"
}
```

## Status Codes

- `200`: Success for GET, PUT, PATCH requests
- `201`: Created for POST requests
- `204`: No content for DELETE requests
- `400`: Bad request for validation errors
- `401`: Unauthorized for invalid/missing JWT
- `404`: Not found for missing resources
- `500`: Internal server error for unexpected issues

## Security

- All todo endpoints require valid JWT token in Authorization header
- JWT tokens must be verified using shared secret
- User ID must be extracted from JWT claims and validated against requested resources
- Users can only access their own todos
- Passwords are hashed using bcrypt before storage