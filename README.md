# Todo CLI Application - Phase I

This is a command-line interface (CLI) todo application built as Phase I of a multi-phase system. It provides basic todo functionality with in-memory storage, demonstrating architectural discipline and clean separation of concerns.

## Features

- Add new tasks with descriptions
- List all tasks with their status
- Mark tasks as complete
- Delete tasks
- Robust error handling

## Requirements

- Python 3.11 or higher
- No external dependencies (uses only standard library)

## Installation

No installation required. The application can be run directly with Python.

## Usage

### Add a new task
```bash
python -m src.cli.main add "Task description here"
```

### List all tasks
```bash
python -m src.cli.main list
```

### Complete a task
```bash
python -m src.cli.main complete <task_id>
```

### Delete a task
```bash
python -m src.cli.main delete <task_id>
```

### Get help
```bash
python -m src.cli.main --help
```

## Architecture

The application follows a clean architecture with separation of concerns:

- **Models** (`src/models/`): Data structures only, no business logic
- **Services** (`src/services/`): Business logic and in-memory storage
- **CLI** (`src/cli/`): User interface and command parsing

## Design Principles

- **Spec-Driven Development**: All functionality based on written specifications
- **Separation of Concerns**: Clear boundaries between models, services, and CLI
- **Simplicity Over Prematurity**: No premature optimization beyond Phase I requirements
- **Forward Compatibility**: Architecture supports evolution to web app, AI integration, and cloud deployment

## Limitations

- In-memory storage only (tasks are lost when the application exits)
- Single-user, local execution
- No persistence to file or database

## Phase I Completion

This Phase I implementation:
- Delivers a robust, clean in-memory CLI Todo application
- Demonstrates architectural discipline
- Is easy to extend for future phases
- Is stable and predictable

Future phases will add persistence, web interfaces, AI features, and cloud deployment capabilities.