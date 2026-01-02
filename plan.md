# Phase I Revision Plan: CLI Usability Improvements

## Technical Context

**Current State**: The application uses UUID-based task IDs and basic text output for task listing. The CLI currently uses long, hard-to-type UUIDs for task identification and displays tasks in a simple text format.

**Current Architecture**:
- `src/models/task.py`: Task data model with string ID field
- `src/services/todo_service.py`: Service layer with UUID generation using `uuid.uuid4()`
- `src/cli/main.py`: CLI layer with basic text output formatting

**Target State**: Replace UUID-based IDs with sequential integer IDs and implement ASCII table rendering for improved visual clarity.

**Unknowns/Dependencies**:
- Need to determine how to maintain sequential ID generation while preserving in-memory behavior
- Need to design ASCII table rendering that works well in standard terminal sizes

## Constitution Check

### Compliance Verification

✅ **Spec-Driven Development**: Following specifications 006 (Sequential Task Identifiers) and 007 (CLI Table Rendering)

✅ **Separation of Concerns**: Changes will maintain clear separation between models, services, and CLI layers

✅ **Simplicity Over Prematurity**: Implementing only what's needed for Phase I (in-memory, sequential IDs, ASCII tables)

✅ **Forward Compatibility**: Sequential ID approach maintains compatibility with future persistence layers

✅ **Test-First Development**: All changes will be testable and maintain existing functionality

✅ **Human-Friendly Identifiers**: Replacing UUIDs with sequential integers as required

✅ **CLI Usability**: Implementing ASCII table rendering for better visual clarity

## Phase 0: Research & Analysis

### Research Tasks

#### Decision: Sequential ID Generation Strategy
**Rationale**: Need to implement sequential ID generation that resets on application restart while maintaining uniqueness during runtime.
**Approach**:
- Add a class-level counter in the TodoService to track the next available ID
- Initialize counter to 1 when service is created
- Increment counter after each new task creation
- IDs will naturally reset when application restarts (new service instance)

#### Decision: Task Model ID Type Change
**Rationale**: Need to change ID type from string to integer to support sequential integer IDs.
**Approach**:
- Update Task model to accept integer IDs
- Modify validation to ensure integer type
- Maintain backward compatibility in service layer

#### Decision: CLI Table Rendering Implementation
**Rationale**: Need to implement ASCII table rendering for improved visual clarity.
**Approach**:
- Create a dedicated table rendering function in CLI layer
- Use standard ASCII characters for borders (|, -, +)
- Format columns for ID, Status, and Description with proper alignment
- Handle edge cases like long descriptions and empty task lists

## Phase 1: Design & Contracts

### Data Model Changes

#### Task Model Update
- Change ID field from `str` to `int` type
- Update validation to ensure integer values
- Preserve all other functionality (description, status)

### Service Layer Changes

#### TodoService Updates
- Replace UUID generation with sequential integer generation
- Add counter to track next available ID
- Update method signatures to accept integer IDs
- Maintain all existing functionality and error handling

### CLI Layer Changes

#### TodoCLI Updates
- Implement ASCII table rendering for task listing
- Update error messages to reference integer IDs
- Ensure all commands accept and validate integer IDs
- Maintain all existing command structure and functionality

## Implementation Strategy

### Step 1: ID Strategy Update
1. Modify Task model to support integer IDs
2. Update TodoService to generate sequential integer IDs
3. Add ID counter functionality to service
4. Update all service methods to work with integer IDs

### Step 2: Update Commands
1. Update CLI argument parsing to enforce integer-only IDs
2. Add validation for integer ID format
3. Improve error messages for invalid IDs
4. Update success messages to show integer IDs

### Step 3: CLI Table Renderer
1. Create dedicated table rendering function
2. Implement ASCII table formatting
3. Add proper column alignment and borders
4. Handle edge cases (empty lists, long text)

### Step 4: Validation
1. Test add functionality with sequential IDs
2. Test list functionality with table rendering
3. Test delete with numeric IDs
4. Test update with numeric IDs
5. Test complete/incomplete with numeric IDs

## Risk Analysis

### Risks and Mitigations
- **Risk**: Breaking existing functionality during ID type change
  - **Mitigation**: Maintain same service method signatures, only change internal implementation
- **Risk**: Incompatibility with existing tests
  - **Mitigation**: Update tests to expect integer IDs while preserving test coverage
- **Risk**: Terminal width issues with table rendering
  - **Mitigation**: Design table to work within standard 80+ character terminals

## Success Criteria

- Sequential integer IDs are generated starting from 1
- All CLI commands accept and work with integer IDs
- Task listing displays in ASCII table format
- Error messages reference integer IDs appropriately
- Application behavior remains unchanged except for ID format and display
- All existing functionality preserved