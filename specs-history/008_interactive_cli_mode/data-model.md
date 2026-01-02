# Data Model: Interactive CLI Mode

## Entities

### Task
**Description**: Represents a todo item with a description and completion status
**Fields**:
- id: int (sequential identifier, positive integer)
- description: str (task description, 1-1000 characters)
- status: str (task status, either "pending" or "complete")

**Validation rules**:
- id must be a positive integer
- description cannot be empty or whitespace-only
- description must not exceed 1000 characters
- status must be either "pending" or "complete"

**State transitions**:
- From "pending" to "complete" when task is completed

### Interactive Session
**Description**: Represents the state where the application is running in interactive mode
**Fields**:
- active: bool (indicates if interactive mode is active)
- menu_options: List[str] (available menu options)
- user_input: str (last input from user)

## Relationships

- TodoService manages multiple Task entities
- Interactive Session interacts with TodoService to perform operations on Tasks

## State Management

The interactive session maintains its own state separate from the task data:
- Displays menu options to user
- Processes user input
- Calls service methods based on user selections
- Maintains loop until user chooses to exit