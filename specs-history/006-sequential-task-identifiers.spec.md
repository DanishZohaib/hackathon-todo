# Spec 006: Sequential Task Identifiers

## Purpose
Replace UUID-based task identifiers with sequential integer IDs to improve CLI usability and user experience in Phase I. Sequential IDs are easier to type, remember, and reference when managing tasks from the command line.

## Functional Requirements
1. Task IDs must be sequential integers starting from 1
2. New tasks must receive the next available sequential ID
3. IDs must reset to 1 when the application restarts (in-memory behavior preserved)
4. All CLI commands that accept task IDs must work with integer IDs
5. The list command must display the sequential ID alongside task information
6. Error messages must reference the sequential ID when identifying tasks

## Acceptance Criteria
1. When adding a task, the system assigns it the next sequential integer ID
2. The first task receives ID 1, second task receives ID 2, etc.
3. When listing tasks, integer IDs are displayed in a dedicated column
4. Complete and delete commands work with integer IDs (e.g., `python -m src.cli.main complete 1`)
5. Error messages reference the integer ID when a task is not found
6. IDs reset to 1 when the application restarts (new process)

## Non-Goals
1. Persisting sequential IDs across application restarts
2. Maintaining ID consistency with existing UUID-based implementations
3. Supporting both UUID and integer ID systems simultaneously
4. Implementing ID reuse after task deletion
5. Introducing database or file-based persistence for IDs