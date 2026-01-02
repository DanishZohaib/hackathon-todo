# Research Findings: Phase I CLI Usability Revision

## Sequential ID Generation Strategy

### Decision: In-Memory Sequential Counter
**Rationale**: To maintain the in-memory behavior while providing sequential integer IDs, implement a class-level counter in the TodoService.
**Implementation**:
- Add `_next_id` instance variable initialized to 1
- Increment counter after successful task creation
- Counter resets naturally when service instance is recreated (application restart)
- No persistence required, matches Phase I in-memory requirements

### Alternatives Considered:
1. **Global module-level counter**: Would work but harder to test and maintain
2. **Static class variable**: Could cause issues with multiple service instances
3. **External ID generator**: Adds unnecessary complexity for Phase I

## Task Model ID Type Change

### Decision: Update Task ID Type to Integer
**Rationale**: Change ID type from string to integer to support sequential integer IDs while maintaining data model simplicity.
**Implementation**:
- Update Task dataclass to accept `id: int` instead of `id: str`
- Update validation to ensure integer type
- Update serialization methods (`to_dict`, `from_dict`) to handle integer IDs
- Maintain all other functionality unchanged

### Alternatives Considered:
1. **Keep string type with integer values**: Would work but doesn't reflect actual type
2. **Generic type that accepts both**: Adds complexity without benefit for Phase I

## CLI Table Rendering Implementation

### Decision: ASCII Table with Fixed-Width Columns
**Rationale**: Implement clean ASCII table rendering using standard characters that works well in most terminal environments.
**Implementation**:
- Use `+`, `-`, `|` characters for table borders
- Fixed column widths: ID (4 chars), Status (12 chars), Description (remaining width)
- Calculate terminal width or use standard 80-char width
- Handle text wrapping for long descriptions

### Table Format Example:
```
+----+------------+------------------------------------------+
| ID | Status     | Description                              |
+----+------------+------------------------------------------+
| 1  | PENDING    | Buy groceries                            |
| 2  | COMPLETED  | Pay electricity bill                     |
+----+------------+------------------------------------------+
```

### Alternatives Considered:
1. **Third-party table libraries**: Violates constraint of no third-party UI libraries
2. **Simple aligned columns**: Less visual clarity than full table
3. **Dynamic column sizing**: More complex but potentially better for various terminal sizes

## Error Handling and Validation

### Decision: Strict Integer ID Validation
**Rationale**: Ensure CLI commands only accept valid integer IDs to maintain data integrity.
**Implementation**:
- Add validation in CLI layer to check if input is a valid integer
- Provide clear error messages for invalid ID formats
- Update service methods to handle integer IDs appropriately
- Maintain all existing error handling for non-existent tasks

## Integration Approach

### Decision: Non-Breaking Evolution
**Rationale**: Maintain all existing CLI commands and functionality while updating ID format and display.
**Implementation**:
- Keep same command structure (`add`, `list`, `complete`, `delete`)
- Update only the ID generation and display layers
- Preserve all existing error messages and success messages (with updated ID format)
- Ensure backward compatibility in service layer API