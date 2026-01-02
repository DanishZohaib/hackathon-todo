# Quickstart: Interactive CLI Mode

## Running the Application

### Interactive Mode
To start the application in interactive mode:
```bash
python -m src.cli.main
```

This will display a menu with options to add, list, complete, delete tasks and exit.

### Command Mode (Backward Compatible)
To use the traditional command-line interface:
```bash
python -m src.cli.main add "Buy groceries"
python -m src.cli.main list
python -m src.cli.main complete 1
python -m src.cli.main delete 1
```

## Interactive Menu Options

1. **Add Task**: Prompts for task description and adds it to the list
2. **List Tasks**: Displays all tasks with their completion status in a table format
3. **Complete Task**: Prompts for task ID and marks the task as complete
4. **Delete Task**: Prompts for task ID and removes the task from the list
5. **Exit**: Exits the interactive mode and terminates the application

## Input Validation

- Task descriptions cannot be empty
- Task IDs must be positive integers
- Invalid menu selections will show an error message and prompt again
- Empty inputs will show appropriate error messages

## Development

The interactive mode is implemented in the `TodoCLI` class in `src/cli/main.py`. The main changes include:

1. Detection of no command-line arguments
2. Interactive menu loop implementation
3. Input processing and validation
4. Integration with existing service methods