# CLI Command Contracts: Todo System Phase I

## Add Task Command
- **Command**: `python src/cli/main.py add [description]`
- **Input**: Task description as a string argument
- **Output**: Success message with assigned task ID
- **Error Cases**:
  - Empty description → Error message: "Task description cannot be empty"
  - Invalid arguments → Help message displayed

## List Tasks Command
- **Command**: `python src/cli/main.py list`
- **Input**: No arguments required
- **Output**: Formatted list of all tasks with ID, description, and status
- **Error Cases**:
  - No tasks exist → Message: "No tasks found"

## Complete Task Command
- **Command**: `python src/cli/main.py complete [task_id]`
- **Input**: Task ID as integer argument
- **Output**: Success message confirming task completion
- **Error Cases**:
  - Invalid task ID → Error message: "Task not found"
  - Already completed task → Success message (no change)

## Delete Task Command
- **Command**: `python src/cli/main.py delete [task_id]`
- **Input**: Task ID as integer argument
- **Output**: Success message confirming task deletion
- **Error Cases**:
  - Invalid task ID → Error message: "Task not found"