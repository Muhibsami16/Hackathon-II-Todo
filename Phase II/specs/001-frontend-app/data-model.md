# Data Model: Frontend Application for Secure Todo Web Platform

## Entities

### User Session
Represents the authenticated state of a user in the application, including JWT token and user identity information.

**Attributes**:
- token: String (the JWT token received after authentication)
- user: Object (user information like id, email, etc.)
- isAuthenticated: Boolean (whether the user is currently authenticated)
- isLoading: Boolean (whether authentication state is being determined)

**State Transitions**:
- unauthenticated → authenticating (when login/register initiated)
- authenticating → authenticated (when login successful)
- authenticated → unauthenticated (when logout or token expires)

**Validation rules**:
- Token must be valid JWT format
- User object must contain required identity information
- Session must be validated against backend before use

### Task Item
Represents a single todo item with properties like title, description, completion status, and user association.

**Attributes**:
- id: String/Number (unique identifier for the task)
- title: String (the task title, required)
- description: String (optional description of the task)
- completed: Boolean (completion status, default: false)
- createdAt: Date (timestamp when task was created)
- updatedAt: Date (timestamp when task was last updated)

**State Transitions**:
- pending → completed (when user marks task as complete)
- completed → pending (when user unmarks task as complete)

**Validation rules**:
- Title must be provided and not empty
- Title must not exceed maximum character length
- Task must be associated with authenticated user
- Task can only be modified by its owner

### Navigation State
Represents the current page and routing context, maintaining proper authentication context across transitions.

**Attributes**:
- currentPage: String (the current route/path)
- previousPage: String (the previous route/path)
- isAuthenticated: Boolean (authentication state at navigation time)
- protectedRoute: Boolean (whether the route requires authentication)

**State Transitions**:
- public → protected (when navigating to authenticated area)
- protected → public (when logging out or session expires)

**Validation rules**:
- Protected routes require valid authentication state
- Navigation should preserve user context where appropriate
- Back navigation should respect authentication boundaries