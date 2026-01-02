# Interactive CLI API Contracts

## Menu Options

### Add Task
- **Input**: User selects option 1, then enters task description
- **Validation**: Description must not be empty
- **Output**: Confirmation message with task ID
- **Service Method**: `TodoService.add_task(description)`

### List Tasks
- **Input**: User selects option 2
- **Output**: ASCII table of all tasks with ID, status, and description
- **Service Method**: `TodoService.get_all_tasks()`

### Complete Task
- **Input**: User selects option 3, then enters task ID
- **Validation**: Task ID must be positive integer and exist
- **Output**: Confirmation message
- **Service Method**: `TodoService.complete_task(task_id)`

### Delete Task
- **Input**: User selects option 4, then enters task ID
- **Validation**: Task ID must be positive integer and exist
- **Output**: Confirmation message
- **Service Method**: `TodoService.delete_task(task_id)`

### Exit
- **Input**: User selects option 5
- **Output**: Application terminates gracefully
- **Service Method**: None (terminates application)

## Error Handling Contracts

- Invalid menu selection: Show error and prompt again
- Empty task description: Show error and prompt again
- Invalid task ID: Show error and prompt again
- Non-existent task ID: Show error and prompt again
- KeyboardInterrupt (Ctrl+C): Exit gracefully