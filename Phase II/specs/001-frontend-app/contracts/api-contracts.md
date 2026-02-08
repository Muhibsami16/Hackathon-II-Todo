# API Contracts: Frontend Application for Secure Todo Web Platform

## Authentication Endpoints

### POST /api/auth/register
Register a new user account.

**Request**:
```json
{
  "email": "user@example.com",
  "password": "secure_password"
}
```

**Response (200)**:
```json
{
  "id": 1,
  "email": "user@example.com",
  "created_at": "2026-02-04T10:00:00Z"
}
```

**Response (400)**:
```json
{
  "detail": "Email already exists"
}
```

### POST /api/auth/login
Authenticate user and return JWT token.

**Request**:
```json
{
  "email": "user@example.com",
  "password": "secure_password"
}
```

**Response (200)**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Response (401)**:
```json
{
  "detail": "Incorrect email or password"
}
```

## Todo Endpoints

### GET /api/todos
Retrieve all todos for the authenticated user.

**Headers**:
```
Authorization: Bearer {jwt_token}
```

**Response (200)**:
```json
[
  {
    "id": 1,
    "title": "Sample todo",
    "description": "Sample description",
    "completed": false,
    "user_id": 1,
    "created_at": "2026-02-04T10:00:00Z",
    "updated_at": "2026-02-04T10:00:00Z"
  }
]
```

**Response (401)**:
```json
{
  "detail": "Could not validate credentials"
}
```

### POST /api/todos
Create a new todo for the authenticated user.

**Headers**:
```
Authorization: Bearer {jwt_token}
```

**Request**:
```json
{
  "title": "New todo",
  "description": "Todo description",
  "completed": false
}
```

**Response (201)**:
```json
{
  "id": 2,
  "title": "New todo",
  "description": "Todo description",
  "completed": false,
  "user_id": 1,
  "created_at": "2026-02-04T11:00:00Z",
  "updated_at": "2026-02-04T11:00:00Z"
}
```

**Response (401)**:
```json
{
  "detail": "Could not validate credentials"
}
```

### GET /api/todos/{id}
Retrieve a specific todo for the authenticated user.

**Headers**:
```
Authorization: Bearer {jwt_token}
```

**Response (200)**:
```json
{
  "id": 1,
  "title": "Sample todo",
  "description": "Sample description",
  "completed": false,
  "user_id": 1,
  "created_at": "2026-02-04T10:00:00Z",
  "updated_at": "2026-02-04T10:00:00Z"
}
```

**Response (401)**:
```json
{
  "detail": "Could not validate credentials"
}
```

**Response (404)**:
```json
{
  "detail": "Todo not found"
}
```

### PUT /api/todos/{id}
Update an existing todo for the authenticated user.

**Headers**:
```
Authorization: Bearer {jwt_token}
```

**Request**:
```json
{
  "title": "Updated todo",
  "description": "Updated description",
  "completed": true
}
```

**Response (200)**:
```json
{
  "id": 1,
  "title": "Updated todo",
  "description": "Updated description",
  "completed": true,
  "user_id": 1,
  "created_at": "2026-02-04T10:00:00Z",
  "updated_at": "2026-02-04T12:00:00Z"
}
```

**Response (401)**:
```json
{
  "detail": "Could not validate credentials"
}
```

**Response (404)**:
```json
{
  "detail": "Todo not found"
}
```

### PATCH /api/todos/{id}/complete
Toggle the completion status of a todo for the authenticated user.

**Headers**:
```
Authorization: Bearer {jwt_token}
```

**Query Parameters**:
- `completed`: boolean value (true/false)

**Response (200)**:
```json
{
  "id": 1,
  "title": "Sample todo",
  "description": "Sample description",
  "completed": true,
  "user_id": 1,
  "created_at": "2026-02-04T10:00:00Z",
  "updated_at": "2026-02-04T13:00:00Z"
}
```

**Response (401)**:
```json
{
  "detail": "Could not validate credentials"
}
```

**Response (404)**:
```json
{
  "detail": "Todo not found"
}
```

### DELETE /api/todos/{id}
Delete a specific todo for the authenticated user.

**Headers**:
```
Authorization: Bearer {jwt_token}
```

**Response (200)**:
```json
{
  "message": "Todo deleted successfully"
}
```

**Response (401)**:
```json
{
  "detail": "Could not validate credentials"
}
```

**Response (404)**:
```json
{
  "detail": "Todo not found"
}
```

## Security Requirements

All protected endpoints require valid JWT token in Authorization header:
- Token must be properly formatted as "Bearer {token}"
- Token signature must be valid against shared secret
- Token must not be expired
- User identity must be extracted from token claims
- Resource access must be validated against authenticated user ID

## Error Handling

- 401: Unauthorized for invalid/missing JWT tokens
- 404: Not found for resources owned by other users (to prevent user enumeration)
- 422: Unprocessable Entity for invalid request data
- 500: Internal server error for unexpected issues