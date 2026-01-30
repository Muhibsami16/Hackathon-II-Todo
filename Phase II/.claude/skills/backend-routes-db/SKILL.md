---
name: backend-routes-db
description: Build backend functionality by generating routes, handling requests/responses, and connecting to databases. Use for API and server-side development.
---

# Backend Skill – Routes, Requests & Database

## Instructions

1. **Routing**
   - Define RESTful routes (GET, POST, PUT, DELETE)
   - Organize routes by feature/module
   - Use proper URL naming conventions

2. **Request & Response Handling**
   - Parse request body, params, and query
   - Validate incoming data
   - Send structured JSON responses
   - Handle errors with proper HTTP status codes

3. **Database Connection**
   - Connect to database (SQL or NoSQL)
   - Use environment variables for credentials
   - Perform CRUD operations
   - Handle connection errors safely

## Best Practices
- Follow REST API standards
- Use async/await for database operations
- Separate routes, controllers, and services
- Never expose sensitive data in responses
- Use middleware for validation and auth

## Example Structure
```js
// routes/userRoutes.js
import express from "express";
import { getUsers, createUser } from "../controllers/userController.js";

const router = express.Router();

router.get("/users", getUsers);
router.post("/users", createUser);

export default router;
