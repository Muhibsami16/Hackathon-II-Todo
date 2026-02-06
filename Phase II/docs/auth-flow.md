# Authentication Flow Documentation

## Overview
This document describes the JWT-based authentication flow implemented in the Todo application using Better Auth on the frontend and shared-secret JWT verification in FastAPI.

## Architecture
- **Frontend**: Next.js application using Better Auth with JWT plugin
- **Backend**: FastAPI application with JWT verification using shared secret
- **Secret**: BETTER_AUTH_SECRET used by both frontend and backend for token validation

## Authentication Flow

### 1. User Registration
1. User submits registration form with email and password
2. Better Auth processes registration request
3. User account is created in the database
4. Response includes user information

### 2. User Login
1. User submits login form with email and password
2. Better Auth verifies credentials
3. If valid, Better Auth generates a signed JWT token
4. JWT token contains user_id and email claims
5. Token is returned to frontend with "bearer" token type

### 3. JWT Token Structure
The JWT token contains the following claims:
- `user_id`: Integer identifying the authenticated user
- `email`: User's email address for identification
- `exp`: Expiration timestamp in Unix time
- `iat`: Issued-at timestamp in Unix time

### 4. Protected API Requests
1. Frontend API client automatically attaches JWT to requests
2. Authorization header format: `Authorization: Bearer {token}`
3. Backend receives request and extracts JWT from header
4. Backend verifies JWT signature using BETTER_AUTH_SECRET
5. Backend validates token expiration
6. Backend extracts user identity from token claims
7. Request is processed with user-specific data filtering

### 5. User Data Isolation
1. All protected endpoints require valid JWT token
2. Backend extracts authenticated user ID from JWT
3. All data queries are filtered by authenticated user ID
4. Users can only access their own data
5. Attempts to access other users' data return 404 (not 403) to prevent enumeration

## Security Measures
- JWT tokens are signed with shared secret (BETTER_AUTH_SECRET)
- Tokens expire after 30 minutes (configurable)
- All protected endpoints validate JWT signature and expiration
- User identity is extracted from JWT claims, not URL parameters
- User-specific data filtering prevents unauthorized access
- 401 responses for invalid/missing tokens
- 404 responses for unauthorized resource access (to prevent enumeration)

## Error Handling
- **401 Unauthorized**: Invalid, expired, or missing JWT token
- **404 Not Found**: Attempt to access resource owned by another user
- **400 Bad Request**: Invalid registration data (e.g., duplicate email)
- **200 OK**: Successful authentication and valid requests
- **500 Internal Server Error**: Unexpected server errors

## Configuration
Environment variables required:
- `BETTER_AUTH_SECRET`: Shared secret for JWT signing/verification
- `JWT_ALGORITHM`: Algorithm used for signing (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time (default: 30 minutes)