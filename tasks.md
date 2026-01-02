# Phase I – Revision A: CLI Usability Improvements

## Feature Overview
This revision implements CLI usability improvements by replacing UUID-based task identifiers with sequential integer IDs and implementing ASCII table rendering for improved visual clarity. The changes maintain architectural cleanliness and avoid breaking existing behavior.

## Implementation Strategy
- Implement sequential integer ID generation in the service layer
- Create ASCII table rendering for task listing
- Update error handling to provide friendly messages for invalid IDs
- Maintain all existing functionality while improving usability

---

## Phase 1: Setup Tasks
- [x] T001 Create backup of current source files before making changes
- [x] T002 Review current implementation in src/models/task.py, src/services/todo_service.py, and src/cli/main.py

## Phase 2: Foundational Tasks
- [x] T003 [P] Update Task model to use integer ID type in src/models/task.py
- [x] T004 [P] Add sequential ID counter to TodoService in src/services/todo_service.py
- [x] T005 [P] Create ASCII table rendering function in src/cli/main.py

---

## Phase 3: Sequential ID Implementation [US1]
### User Story Goal
Replace UUID-based task identifiers with sequential integer IDs starting from 1, with IDs resetting when the application restarts.

### Independent Test Criteria
- `python -m src.cli.main add "Test task"` assigns sequential integer ID starting from 1
- Adding multiple tasks results in incrementing IDs (1, 2, 3, etc.)
- Restarting the application resets IDs back to 1

### Implementation Tasks
- [x] T006 [US1] Update Task model validation to require positive integer ID in src/models/task.py
- [x] T007 [US1] Modify TodoService to initialize ID counter to 1 in src/services/todo_service.py
- [x] T008 [US1] Update TodoService.add_task to use sequential integer ID in src/services/todo_service.py
- [x] T009 [US1] Update all TodoService methods to accept integer IDs in src/services/todo_service.py
- [x] T010 [US1] Update Task serialization methods to handle integer IDs in src/models/task.py
- [x] T011 [US1] Test sequential ID generation with multiple tasks
- [x] T012 [US1] Verify IDs reset to 1 on application restart

---

## Phase 4: CLI Table Rendering [US2]
### User Story Goal
Implement ASCII table rendering for the list command to improve visual clarity with columns for ID, Status, and Description.

### Independent Test Criteria
- `python -m src.cli.main list` displays tasks in ASCII table format
- Table includes ID, Status, and Description columns with proper alignment
- Table has clear borders using ASCII characters (|, -, +)

### Implementation Tasks
- [x] T013 [US2] Create dedicated table rendering function in src/cli/main.py
- [x] T014 [US2] Implement ASCII table formatting with proper column alignment in src/cli/main.py
- [x] T015 [US2] Update handle_list method to use table rendering function in src/cli/main.py
- [x] T016 [US2] Handle empty task list case with appropriate message in src/cli/main.py
- [x] T017 [US2] Ensure table formatting works within 80+ character terminals in src/cli/main.py
- [x] T018 [US2] Test table rendering with various task descriptions
- [x] T019 [US2] Verify proper column alignment and borders

---

## Phase 5: Error Handling Update [US3]
### User Story Goal
Update error handling to provide friendly messages for invalid IDs and controlled errors for non-existent tasks.

### Independent Test Criteria
- `python -m src.cli.main delete "text"` fails safely with friendly error message
- `python -m src.cli.main delete 1` works when task exists
- Error messages reference integer IDs appropriately

### Implementation Tasks
- [x] T020 [US3] Add integer validation for task_id arguments in CLI commands in src/cli/main.py
- [x] T021 [US3] Update error messages to reference integer IDs in src/cli/main.py
- [x] T022 [US3] Implement validation for positive integer IDs in src/cli/main.py
- [x] T023 [US3] Test error handling with invalid ID formats
- [x] T024 [US3] Verify controlled errors for non-existent tasks
- [x] T025 [US3] Test success and error messages with integer IDs

---

## Phase 6: Validation & Testing
### Validation Checklist
- [x] `list` shows table with proper formatting
- [x] `delete 1` works for existing tasks
- [x] `delete "text"` fails safely with friendly error
- [x] App remains stable after all changes

### Implementation Tasks
- [x] T026 Test add command with sequential integer IDs
- [x] T027 Test list command with ASCII table rendering
- [x] T028 Test delete command with integer IDs
- [x] T029 Test complete command with integer IDs
- [x] T030 Test error handling for invalid ID formats
- [x] T031 Verify all existing functionality preserved
- [x] T032 Test application restart behavior for ID reset
- [x] T033 Run full integration test of all commands

---

## Dependencies
- T003 (Task model update) must complete before T004 (Service update)
- T004 (Service update) must complete before T007, T008, T009 (Service method updates)
- T013 (Table rendering function) must complete before T015 (handle_list update)

## Parallel Execution Examples
- T006, T010 can run in parallel (both in models)
- T007, T008, T009 can run in parallel (all in service layer)
- T013, T014, T015, T016, T017 can run in parallel (all in CLI layer)
- T020, T021, T022 can run in parallel (all CLI error handling)

## MVP Scope
The MVP includes the first user story (Sequential ID Implementation) which provides the core functionality of replacing UUIDs with sequential integers. This alone significantly improves CLI usability by making task IDs easier to type and remember.