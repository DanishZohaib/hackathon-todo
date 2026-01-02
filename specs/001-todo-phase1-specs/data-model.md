# Data Model: Todo System Phase I

## Task Entity

### Fields
- **id** (string/integer): Unique identifier for the task, automatically assigned when created
- **description** (string): The text description of what needs to be done
- **status** (string): The completion status of the task, either "incomplete" or "complete"

### Relationships
- The Task entity is independent and does not have relationships with other entities in Phase I

### Validation Rules
- **id**: Must be unique within the system, automatically generated
- **description**: Must not be empty or null, maximum length of 1000 characters
- **status**: Must be either "incomplete" or "complete", case-sensitive

### State Transitions
- **incomplete** → **complete**: When a user marks a task as completed
- **complete** → **complete**: No change when user attempts to complete an already completed task

## In-Memory Storage Structure
- Tasks will be stored in a Python dictionary where the key is the task ID and the value is the task object
- The dictionary will be maintained in application memory during execution
- No persistence outside of the application lifecycle