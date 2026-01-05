# Quickstart: Phase I – In-Memory Python Console Todo App

## Prerequisites
- Python 3.13+ installed
- No additional dependencies required

## Setup
1. Clone the repository
2. Navigate to the project directory
3. Run the application directly with Python

## Running the Application
```bash
python src/todo_app/main.py
```

## Available Commands
- `add "task description"` - Add a new todo item
- `list` - View all todo items
- `update <id> "new description"` - Update a todo item
- `complete <id>` - Mark a todo item as complete
- `delete <id>` - Delete a todo item
- `help` - Show available commands
- `quit` - Exit the application

## Example Usage
```
> add "Buy groceries"
Added todo: "Buy groceries" (ID: 1)

> add "Walk the dog"
Added todo: "Walk the dog" (ID: 2)

> list
1. [ ] Buy groceries
2. [ ] Walk the dog

> complete 1
Marked todo 1 as complete

> list
1. [x] Buy groceries
2. [ ] Walk the dog

> update 2 "Walk the cat"
Updated todo 2: "Walk the cat"

> delete 2

> list
1. [x] Buy groceries
```