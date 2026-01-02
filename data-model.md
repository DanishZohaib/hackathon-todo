# Data Model: Sequential Task IDs

## Task Entity

### Current State
```python
@dataclass
class Task:
    id: str                    # UUID string
    description: str          # Task description
    status: str = "incomplete" # Task status ("incomplete" or "complete")
```

### Target State
```python
@dataclass
class Task:
    id: int                   # Sequential integer ID
    description: str          # Task description
    status: str = "incomplete" # Task status ("incomplete" or "complete")
```

### Field Definitions

#### ID
- **Type**: `int`
- **Constraints**: Positive integer, unique during runtime
- **Generation**: Sequential, starting from 1, incrementing by 1
- **Behavior**: Resets to 1 when application restarts (in-memory preservation)
- **Validation**: Must be positive integer

#### Description
- **Type**: `str`
- **Constraints**: Cannot be empty, maximum 1000 characters
- **Validation**: Non-empty after stripping whitespace

#### Status
- **Type**: `str`
- **Values**: "incomplete" or "complete"
- **Default**: "incomplete"
- **Validation**: Only accepts allowed values

### Validation Rules

1. **ID Validation**:
   - Must be a positive integer (id > 0)
   - Required field, cannot be None or empty

2. **Description Validation**:
   - Cannot be empty or only whitespace
   - Maximum length of 1000 characters
   - Required field

3. **Status Validation**:
   - Must be either "incomplete" or "complete"
   - Case-sensitive validation
   - Defaults to "incomplete" if not provided

### State Transitions

#### Status Transitions
- Initial state: `status = "incomplete"`
- Transition to complete: `complete()` method changes status to "complete"
- No reverse transition (completed tasks remain completed)

### Serialization

#### to_dict() Method
```python
def to_dict(self) -> Dict[str, Any]:
    return {
        "id": self.id,              # Integer ID
        "description": self.description,
        "status": self.status
    }
```

#### from_dict() Method
```python
@classmethod
def from_dict(cls, data: Dict[str, Any]) -> 'Task':
    return cls(
        id=int(data["id"]),          # Convert to integer if needed
        description=data["description"],
        status=data.get("status", "incomplete")
    )
```

### Method Updates

#### complete() Method
- No changes required
- Maintains same functionality

## Service Layer Data Flow

### Task Creation Flow
1. TodoService receives description
2. Service increments internal ID counter
3. Service creates Task with new integer ID
4. Task stored in internal dictionary using integer ID as key

### Task Retrieval Flow
1. CLI receives integer ID as string argument
2. CLI converts string to integer for validation
3. Service uses integer ID to look up task
4. Service returns task if found

### Data Integrity
- Sequential ID generation ensures uniqueness during runtime
- Integer type ensures compatibility with CLI input validation
- In-memory storage maintains ID persistence within application lifecycle
- Application restart naturally resets ID sequence (preserves in-memory behavior)