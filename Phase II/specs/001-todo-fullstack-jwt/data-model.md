# Data Model: Todo Full-Stack Web Application

## Entities

### User
Represents a registered user account with unique email, password hash, and account metadata.

**Fields**:
- id: Integer (primary key, auto-increment)
- email: String (unique, required, indexed)
- hashed_password: String (required)
- created_at: DateTime (default: current timestamp)
- updated_at: DateTime (default: current timestamp, auto-update)

**Relationships**:
- One-to-many with Todo (one user can have many todos)

**Validation rules**:
- Email must be valid email format
- Email must be unique across all users
- Password must be hashed before storage

### Todo
Represents a task item with title, description, completion status, creation timestamp, and association to a specific user.

**Fields**:
- id: Integer (primary key, auto-increment)
- title: String (required, max length 200)
- description: String (optional, nullable)
- completed: Boolean (default: false)
- user_id: Integer (foreign key to User.id, required)
- created_at: DateTime (default: current timestamp)
- updated_at: DateTime (default: current timestamp, auto-update)

**Relationships**:
- Many-to-one with User (many todos belong to one user)

**State transitions**:
- completed: false → true (when marking as complete)
- completed: true → false (when marking as incomplete)

**Validation rules**:
- Title must be provided and not empty
- Title must not exceed 200 characters
- Todo must belong to a valid user
- Only the owner can modify the todo