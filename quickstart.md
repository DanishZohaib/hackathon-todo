# Quickstart Guide: CLI Usability Improvements

## Overview
This guide provides instructions for implementing the CLI usability improvements, including sequential integer IDs and ASCII table rendering.

## Changes to Implement

### 1. Update Task Model
- Change Task ID type from `str` to `int` in `src/models/task.py`
- Update validation to ensure integer type
- Update serialization methods to handle integer IDs

### 2. Update Todo Service
- Add sequential ID counter to `TodoService`
- Replace UUID generation with sequential integer generation
- Update all methods to work with integer IDs

### 3. Update CLI Layer
- Implement ASCII table rendering for task listing
- Add integer ID validation for commands
- Update error messages to reference integer IDs

## Implementation Steps

### Step 1: Update Task Model
1. Edit `src/models/task.py`
2. Change `id: str` to `id: int` in the Task dataclass
3. Update validation in `__post_init__` to check for positive integer
4. Ensure `from_dict` method properly handles integer conversion

### Step 2: Update Todo Service
1. Edit `src/services/todo_service.py`
2. Add `_next_id` instance variable initialized to 1 in `__init__`
3. Replace `str(uuid.uuid4())` with sequential integer in `add_task`
4. Update `_tasks` dictionary to use integer keys
5. Update all methods to accept and use integer IDs

### Step 3: Update CLI Layer
1. Edit `src/cli/main.py`
2. Add integer validation for task_id arguments
3. Create ASCII table rendering function
4. Update `handle_list` method to use table rendering
5. Update success and error messages to show integer IDs

## Testing Commands

After implementation, test these commands:

```bash
# Add tasks (should show integer IDs)
python -m src.cli.main add "First task"
python -m src.cli.main add "Second task"

# List tasks (should show ASCII table)
python -m src.cli.main list

# Complete task (should accept integer ID)
python -m src.cli.main complete 1

# Delete task (should accept integer ID)
python -m src.cli.main delete 2
```

## Expected Output Format

### List Command Output
```
+----+------------+------------------------------------------+
| ID | Status     | Description                              |
+----+------------+------------------------------------------+
| 1  | COMPLETED  | First task                               |
| 2  | PENDING    | Second task                              |
+----+------------+------------------------------------------+
```

## Validation Requirements

- All CLI commands must accept only integer IDs
- Sequential IDs must start from 1 and increment by 1
- IDs must reset to 1 on application restart
- Table rendering must use ASCII characters only
- Error messages must reference integer IDs appropriately

## Rollback Plan

If issues occur:
1. Revert changes to `src/models/task.py`
2. Revert changes to `src/services/todo_service.py`
3. Revert changes to `src/cli/main.py`
4. Restore original UUID-based functionality