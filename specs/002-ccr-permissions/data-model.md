# Data Model: CCR Permissions

## Entities

### Permission Pattern
- **Name**: Permission Pattern
- **Description**: Rules that govern access to tools and commands
- **Fields**:
  - type: String (e.g., "Bash", "Read", "Edit", "Write")
  - pattern: String (e.g., "ls:*", "git:*", "python:*")
  - validation_rules: List of validation rules
- **Validation Rules**:
  - Must use `:*` prefix matching syntax
  - No standalone `*` wildcards allowed
  - No nested quotes in permission strings
  - Must follow CCR validation requirements

### CCR Configuration
- **Name**: CCR Configuration
- **Description**: Settings that define tool permissions
- **Fields**:
  - permissions: Object containing allow/deny lists
  - allow: Array of Permission Pattern objects
  - validation_status: String (e.g., "valid", "invalid", "pending")
- **Relationships**:
  - Contains multiple Permission Pattern entities
  - Associated with specific tool access requests

### Tool Access Request
- **Name**: Tool Access Request
- **Description**: Runtime validation of permission grants
- **Fields**:
  - tool_type: String (e.g., "Bash", "Read", "Edit")
  - command: String (the specific command requested)
  - granted: Boolean (whether access was granted)
  - timestamp: DateTime (when the request was made)
- **Relationships**:
  - Associated with CCR Configuration for validation
  - References specific Permission Pattern for access rules

### Validation Engine
- **Name**: Validation Engine
- **Description**: System component that verifies permission syntax
- **Fields**:
  - validation_rules: Array of validation rule strings
  - validation_result: Object containing validation status
  - error_messages: Array of validation error messages
- **Relationships**:
  - Validates CCR Configuration entities
  - Processes Tool Access Request entities
  - Enforces Permission Pattern rules

## State Transitions

### CCR Configuration States
- **Pending**: Configuration created but not validated
- **Valid**: Configuration passes all validation rules
- **Invalid**: Configuration fails validation checks
- **Applied**: Configuration is active and in use

### Permission Validation Flow
1. CCR Configuration enters "Pending" state
2. Validation Engine processes configuration
3. If valid, state changes to "Valid"
4. If invalid, state changes to "Invalid" with error details
5. Valid configurations can transition to "Applied" state

## Relationships

- CCR Configuration **contains** multiple Permission Pattern entities
- Validation Engine **validates** CCR Configuration entities
- Tool Access Request **references** Permission Pattern rules for access decisions
- Permission Pattern **defines** access rules for Tool Access Request entities