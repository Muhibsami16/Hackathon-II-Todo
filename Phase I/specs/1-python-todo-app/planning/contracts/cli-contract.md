# CLI Contract: Phase I – In-Memory Python Console Todo App

## Command Interface

### Add Command
- **Command**: `add "description"`
- **Input**: Task description as string
- **Output**: Success message with assigned ID
- **Errors**:
  - Empty description: "Error: Task description cannot be empty"
  - Invalid format: "Error: Please provide a task description"

### List Command
- **Command**: `list`
- **Input**: None
- **Output**: Formatted list of all todos with ID, status, and description
- **Errors**: None (shows empty list if no items)

### Update Command
- **Command**: `update <id> "new description"`
- **Input**: Todo ID (integer) and new description (string)
- **Output**: Success confirmation message
- **Errors**:
  - Invalid ID: "Error: Todo with ID <id> does not exist"
  - Empty description: "Error: Task description cannot be empty"

### Complete Command
- **Command**: `complete <id>`
- **Input**: Todo ID (integer)
- **Output**: Success confirmation message
- **Errors**:
  - Invalid ID: "Error: Todo with ID <id> does not exist"

### Delete Command
- **Command**: `delete <id>`
- **Input**: Todo ID (integer)
- **Output**: Success confirmation message
- **Errors**:
  - Invalid ID: "Error: Todo with ID <id> does not exist"

### Help Command
- **Command**: `help`
- **Input**: None
- **Output**: List of available commands with descriptions

### Quit Command
- **Command**: `quit`
- **Input**: None
- **Output**: Exit message and application termination