# Data Model: Phase I – In-Memory Python Console Todo App

## Todo Item Entity

**Name**: Todo
**Description**: Represents a single task with an ID, description text, and completion status

### Fields
- `id` (int): Unique identifier for the todo item (auto-generated, sequential)
- `title` (str): The description/text of the todo item (required, non-empty)
- `completed` (bool): Completion status of the todo item (default: False)

### Validation Rules
- `id` must be a positive integer
- `title` must be a non-empty string (no whitespace-only titles)
- `completed` must be a boolean value

### State Transitions
- `incomplete` → `completed`: When user marks item as complete
- `completed` → `incomplete`: When user marks item as incomplete

## Todo List Collection

**Name**: TodoList
**Description**: In-memory collection of Todo items

### Operations
- Add: Add a new Todo item to the collection
- Get: Retrieve a Todo item by ID
- Update: Modify a Todo item's properties
- Delete: Remove a Todo item from the collection
- List: Get all Todo items in the collection

### Validation Rules
- IDs must be unique within the collection
- No duplicate IDs allowed
- Operations must target existing items