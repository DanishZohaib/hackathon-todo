# Task Persistence Schema Specification

## Purpose
Define the database schema for persisting todo tasks with user ownership. This specification ensures tasks are stored reliably, can be retrieved efficiently, and maintain proper user isolation.

## Functional Requirements

### Task Entity
- **FR-001**: System MUST store task ID, title, description, completion status, creation timestamp, and update timestamp
- **FR-002**: System MUST store user ID to establish ownership relationship
- **FR-003**: System MUST support optional due dates for tasks
- **FR-004**: System MUST support optional priority levels (low, medium, high)
- **FR-005**: System MUST support optional category/tags for tasks

### Data Relationships
- **FR-006**: System MUST ensure every task is associated with exactly one user
- **FR-007**: System MUST prevent orphaned task records without valid user references
- **FR-008**: System MUST maintain referential integrity between tasks and users

### Data Operations
- **FR-009**: System MUST support CRUD operations (Create, Read, Update, Delete) for tasks
- **FR-010**: System MUST support querying tasks by user ID
- **FR-011**: System MUST support querying tasks by completion status
- **FR-012**: System MUST support querying tasks by due date range
- **FR-013**: System MUST support sorting tasks by creation date, due date, or priority

### Data Integrity
- **FR-014**: System MUST ensure task titles are not empty or null
- **FR-015**: System MUST validate that timestamps are in correct format
- **FR-016**: System MUST ensure data consistency during concurrent operations

## Acceptance Criteria

### Task Creation
1. **Given** an authenticated user with valid task data, **When** they create a new task, **Then** the task is stored with correct ownership and all required fields
2. **Given** an authenticated user with invalid task data (empty title), **When** they attempt to create a task, **Then** an appropriate error is returned and no record is created

### Task Retrieval
1. **Given** a user with multiple tasks, **When** they request their tasks, **Then** only their tasks are returned with all relevant details
2. **Given** a user with tasks of different statuses, **When** they filter by completion status, **Then** only matching tasks are returned
3. **Given** a user with tasks with due dates, **When** they request tasks in date range, **Then** only tasks within that range are returned

### Task Updates
1. **Given** a user with an existing task, **When** they update task details, **Then** only their own task is modified with updated timestamp
2. **Given** a user attempting to update another user's task, **When** they submit update request, **Then** the operation is rejected with appropriate error

### Task Deletion
1. **Given** a user with an existing task, **When** they delete the task, **Then** only their own task is removed from the database
2. **Given** a user attempting to delete another user's task, **When** they submit delete request, **Then** the operation is rejected with appropriate error

## Out of Scope

- Task sharing between users
- Task collaboration features
- Advanced reporting or analytics
- Task history/versioning
- File attachments to tasks
- Recurring task patterns
- Complex task dependencies