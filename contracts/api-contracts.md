# API Contracts: CLI Usability Improvements

## Overview
This document defines the API contracts for the CLI usability improvements, focusing on the changes to task ID handling and CLI output formatting.

## CLI Command Contracts

### Add Command
```
Command: python -m src.cli.main add "Task description"
```

**Input**:
- Command: `add`
- Argument: `description` (string, required)

**Output**:
- Success: "Task added successfully with ID: {integer_id}"
- Error: "Error: {error_message}" (to stderr)

**Behavior**:
- Creates new task with sequential integer ID
- ID starts at 1 and increments for each new task
- Validates description is not empty
- Returns exit code 0 on success, 1 on error

### List Command
```
Command: python -m src.cli.main list
```

**Input**:
- Command: `list`

**Output**:
- Success: ASCII table with columns [ID, Status, Description]
- Empty: "No tasks found"
- Format:
```
+----+------------+------------------------------------------+
| ID | Status     | Description                              |
+----+------------+------------------------------------------+
| 1  | PENDING    | Buy groceries                            |
| 2  | COMPLETED  | Pay electricity bill                     |
+----+------------+------------------------------------------+
```

**Behavior**:
- Displays all tasks in ASCII table format
- ID column: 4 characters wide, right-aligned integer
- Status column: 12 characters wide
- Description column: remaining width
- Returns exit code 0

### Complete Command
```
Command: python -m src.cli.main complete {task_id}
```

**Input**:
- Command: `complete`
- Argument: `task_id` (positive integer)

**Output**:
- Success: "Task {task_id} marked as complete"
- Error: "Error: Task with ID {task_id} not found" (to stderr)

**Behavior**:
- Validates task_id is a positive integer
- Marks task as complete if found
- Returns exit code 0 on success, 1 on error

### Delete Command
```
Command: python -m src.cli.main delete {task_id}
```

**Input**:
- Command: `delete`
- Argument: `task_id` (positive integer)

**Output**:
- Success: "Task {task_id} deleted successfully"
- Error: "Error: Task with ID {task_id} not found" (to stderr)

**Behavior**:
- Validates task_id is a positive integer
- Deletes task if found
- Returns exit code 0 on success, 1 on error

## Service Layer Contracts

### TodoService.add_task(description: str) -> Task
```
Input: description (string, 1-1000 characters, non-empty)
Output: Task object with sequential integer ID
```

**Behavior**:
- Generates next sequential integer ID
- Creates Task with new ID and provided description
- Sets status to "incomplete" by default
- Raises ValueError for invalid input

### TodoService.get_all_tasks() -> List[Task]
```
Input: None
Output: List of all Task objects
```

**Behavior**:
- Returns all tasks in storage
- Maintains order of creation (ascending ID order)

### TodoService.get_task_by_id(task_id: int) -> Optional[Task]
```
Input: task_id (positive integer)
Output: Task object if found, None otherwise
```

**Behavior**:
- Looks up task by integer ID
- Returns None if not found

### TodoService.complete_task(task_id: int) -> bool
```
Input: task_id (positive integer)
Output: boolean (True if completed, False if not found)
```

**Behavior**:
- Changes task status to "complete"
- Returns True if task existed and was updated
- Returns False if task not found

### TodoService.delete_task(task_id: int) -> bool
```
Input: task_id (positive integer)
Output: boolean (True if deleted, False if not found)
```

**Behavior**:
- Removes task from storage
- Returns True if task existed and was removed
- Returns False if task not found

### TodoService.update_task_description(task_id: int, description: str) -> bool
```
Input: task_id (positive integer), description (string, 1-1000 characters)
Output: boolean (True if updated, False if not found or invalid)
```

**Behavior**:
- Updates description of existing task
- Returns True if task existed and description was valid
- Returns False if task not found or description invalid

## Data Model Contracts

### Task Data Structure
```
{
  "id": integer,           # Sequential positive integer
  "description": string,   # Task description (1-1000 chars)
  "status": string        # "incomplete" or "complete"
}
```

## Error Handling Contracts

### Validation Errors
- Invalid integer ID: "Error: Task ID must be a positive integer"
- Empty description: "Error: Task description cannot be empty"
- Description too long: "Error: Task description exceeds maximum length of 1000 characters"
- Task not found: "Error: Task with ID {task_id} not found"

### Exit Codes
- 0: Success
- 1: Error (validation, not found, etc.)

## Terminal Display Contracts

### Table Formatting
- Border characters: `|`, `-`, `+`
- Column alignment: ID right-aligned, Status and Description left-aligned
- Minimum terminal width support: 80 characters
- Proper spacing between columns
- Header row clearly separated from data rows