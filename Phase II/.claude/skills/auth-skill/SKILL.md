---
name: auth-skill
description: Implement secure authentication systems including signup, signin, password hashing, JWT tokens, and Better Auth integration.
---

# Authentication Skill

## Instructions

1. **User Signup**
   - Collect user credentials (email, username, password)
   - Validate input (email format, password strength)
   - Hash password before storing in database
   - Prevent duplicate accounts

2. **User Signin**
   - Verify user credentials
   - Compare hashed passwords securely
   - Handle invalid login attempts
   - Return authentication token on success

3. **Password Hashing**
   - Use strong hashing algorithms (bcrypt, argon2)
   - Add salt for extra security
   - Never store plain text passwords
   - Support password updates securely

4. **JWT Tokens**
   - Generate JWT on successful login
   - Include user ID and roles in payload
   - Set token expiration time
   - Verify JWT on protected routes

5. **Better Auth Integration**
   - Configure Better Auth provider
   - Use built-in session management
   - Enable OAuth / social login if required
   - Handle refresh tokens and logout

## Best Practices
- Always hash passwords
- Use HTTPS for all auth routes
- Set short-lived access tokens
- Store JWT securely (HTTP-only cookies)
- Implement proper error handling
- Rate-limit auth endpoints

## Example Flow

```text
User Signup
   ↓
Validate Input
   ↓
Hash Password
   ↓
Save User to Database
   ↓
Signin Request
   ↓
Verify Password
   ↓
Generate JWT
   ↓
Access Protected Routes
