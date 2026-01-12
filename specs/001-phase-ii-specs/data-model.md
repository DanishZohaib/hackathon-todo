# Data Model for Phase II Todo Application

## User Entity

**Entity Name**: User
- **Fields**:
  - id: UUID (Primary Key, unique identifier)
  - email: String (Unique, required, valid email format)
  - password_hash: String (Required, securely hashed)
  - name: String (Optional, user display name)
  - created_at: DateTime (Required, timestamp of account creation)
  - updated_at: DateTime (Required, timestamp of last update)
  - is_active: Boolean (Default: true, indicates account status)

**Validation Rules**:
- Email must follow standard email format validation
- Email must be unique across all users
- Password must meet minimum security requirements (length, complexity)
- Name length must be within reasonable limits (e.g., 1-100 characters)

**Relationships**:
- One-to-Many: User has many Tasks
- Foreign Key: tasks.user_id references users.id

## Task Entity

**Entity Name**: Task
- **Fields**:
  - id: UUID (Primary Key, unique identifier)
  - title: String (Required, task description)
  - description: String (Optional, detailed task information)
  - is_completed: Boolean (Default: false, indicates completion status)
  - due_date: DateTime (Optional, deadline for task)
  - priority: String (Optional, values: 'low', 'medium', 'high', default: 'medium')
  - created_at: DateTime (Required, timestamp of task creation)
  - updated_at: DateTime (Required, timestamp of last update)
  - user_id: UUID (Foreign Key, references users.id, required)

**Validation Rules**:
- Title must not be empty or only whitespace
- Due date must be a valid future date if provided
- Priority must be one of the allowed values ('low', 'medium', 'high')
- User_id must reference an existing, active user

**Relationships**:
- Many-to-One: Task belongs to one User (user_id → users.id)
- Foreign Key Constraint: Enforce referential integrity

## State Transitions

### Task State Transitions
- **Creation**: New task created with is_completed = false
- **Completion**: is_completed transitions from false → true when task completed
- **Reopening**: is_completed transitions from true → false when task reopened
- **Update**: updated_at timestamp updates when any field changes
- **Deletion**: Task marked as deleted (soft delete) or removed from database

### User State Transitions
- **Registration**: New user created with is_active = true
- **Deactivation**: is_active transitions from true → false when account disabled
- **Reactivation**: is_active transitions from false → true when account re-enabled
- **Profile Update**: updated_at timestamp updates when profile data changes

## Constraints and Business Rules

1. **User Isolation**: Each task must belong to exactly one user (enforced by user_id foreign key)
2. **Data Integrity**: Referential integrity enforced between users and tasks tables
3. **Required Fields**: All required fields must be present for successful creation
4. **Unique Constraints**: Email uniqueness enforced at database level
5. **Timestamp Management**: created_at and updated_at automatically managed by application/database