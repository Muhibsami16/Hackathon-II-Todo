# Data Model: Authentication and Security Integration for Todo Web Application

## Entities

### JWT Token
Represents a secure authentication credential containing user identity claims and expiration information, used for stateless authentication between frontend and backend.

**Claims**:
- user_id: Integer (required, identifies the authenticated user)
- email: String (required, user's email address for identification)
- exp: Integer (required, expiration timestamp in Unix time)
- iat: Integer (optional, issued-at timestamp in Unix time)
- sub: String (optional, subject identifier)

**Characteristics**:
- Signed with shared secret (HS256 algorithm)
- Short-lived (typically 15-30 minutes)
- Stateless (no server-side session storage required)

### User Identity
Represents the authenticated user's information extracted from JWT token claims, used for access control and data isolation.

**Attributes**:
- id: Integer (extracted from JWT user_id claim)
- email: String (extracted from JWT email claim)
- authenticated: Boolean (whether user identity has been verified)

**Validation rules**:
- User ID must match the user_id claim in the JWT
- Token must not be expired at time of validation
- Token signature must be valid against shared secret

### Shared Secret
Represents the cryptographic key used for signing and verifying JWT tokens, ensuring token authenticity and integrity.

**Attributes**:
- value: String (the actual secret key, stored securely in environment)
- algorithm: String (the signing algorithm, typically HS256)
- length: Integer (recommended minimum 256 bits)

**Security requirements**:
- Must be stored in environment variables
- Should be randomly generated with sufficient entropy
- Must be identical between frontend and backend for validation