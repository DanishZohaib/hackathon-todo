# Quickstart: Todo System Phase I

## Setup
1. Ensure Python 3.11+ is installed on your system
2. Clone or access the project directory
3. Navigate to the project root directory

## Running the Application
```bash
python src/cli/main.py --help
```

## Basic Usage Examples

### Add a new task
```bash
python src/cli/main.py add "Buy groceries"
```

### List all tasks
```bash
python src/cli/main.py list
```

### Complete a task
```bash
python src/cli/main.py complete 1
```

### Delete a task
```bash
python src/cli/main.py delete 1
```

## Validation
- All commands should execute in under 100ms
- The application should handle invalid inputs gracefully
- Task IDs should be unique and automatically assigned
- Tasks should maintain their completion status correctly