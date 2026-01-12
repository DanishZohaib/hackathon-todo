# API Contract for Phase II Todo Application

## Authentication Endpoints

### POST /auth/signup
**Purpose**: Register a new user account
- **Request Body**:
  ```json
  {
    "email": "string (required, valid email format)",
    "password": "string (required, minimum 8 characters)",
    "name": "string (optional)"
  }
  ```
- **Success Response**: 201 Created
  ```json
  {
    "user_id": "UUID",
    "email": "string",
    "name": "string",
    "created_at": "ISO 8601 datetime"
  }
  ```
- **Error Responses**:
  - 400: Invalid input data
  - 409: Email already exists

### POST /auth/signin
**Purpose**: Authenticate user and return session token
- **Request Body**:
  ```json
  {
    "email": "string (required)",
    "password": "string (required)"
  }
  ```
- **Success Response**: 200 OK
  ```json
  {
    "token": "string (JWT or session token)",
    "user": {
      "user_id": "UUID",
      "email": "string",
      "name": "string"
    }
  }
  ```
- **Error Responses**:
  - 400: Invalid input data
  - 401: Invalid credentials

### POST /auth/signout
**Purpose**: Terminate user session
- **Headers**: Authorization: Bearer {token}
- **Success Response**: 200 OK
  ```json
  {
    "message": "Successfully signed out"
  }
  ```
- **Error Responses**:
  - 401: Invalid or expired token

## Task Management Endpoints

### GET /todos
**Purpose**: Retrieve authenticated user's tasks with optional filtering
- **Headers**: Authorization: Bearer {token}
- **Query Parameters**:
  - status: string (optional, values: "all", "completed", "pending", default: "all")
  - limit: integer (optional, default: 20, max: 100)
  - offset: integer (optional, default: 0)
  - sort: string (optional, values: "created", "due_date", "priority", default: "created")
- **Success Response**: 200 OK
  ```json
  {
    "tasks": [
      {
        "id": "UUID",
        "title": "string",
        "description": "string (optional)",
        "is_completed": "boolean",
        "due_date": "ISO 8601 datetime (optional)",
        "priority": "string (low|medium|high)",
        "created_at": "ISO 8601 datetime",
        "updated_at": "ISO 8601 datetime",
        "user_id": "UUID"
      }
    ],
    "total_count": "integer",
    "limit": "integer",
    "offset": "integer"
  }
  ```
- **Error Responses**:
  - 401: Invalid or expired token

### POST /todos
**Purpose**: Create a new task for the authenticated user
- **Headers**: Authorization: Bearer {token}
- **Request Body**:
  ```json
  {
    "title": "string (required)",
    "description": "string (optional)",
    "due_date": "ISO 8601 datetime (optional)",
    "priority": "string (optional, low|medium|high, default: medium)"
  }
  ```
- **Success Response**: 201 Created
  ```json
  {
    "id": "UUID",
    "title": "string",
    "description": "string (optional)",
    "is_completed": "boolean (false)",
    "due_date": "ISO 8601 datetime (optional)",
    "priority": "string",
    "created_at": "ISO 8601 datetime",
    "updated_at": "ISO 8601 datetime",
    "user_id": "UUID"
  }
  ```
- **Error Responses**:
  - 400: Invalid input data
  - 401: Invalid or expired token

### GET /todos/{id}
**Purpose**: Retrieve a specific task by ID
- **Headers**: Authorization: Bearer {token}
- **Path Parameter**: id (UUID of the task)
- **Success Response**: 200 OK
  ```json
  {
    "id": "UUID",
    "title": "string",
    "description": "string (optional)",
    "is_completed": "boolean",
    "due_date": "ISO 8601 datetime (optional)",
    "priority": "string",
    "created_at": "ISO 8601 datetime",
    "updated_at": "ISO 8601 datetime",
    "user_id": "UUID"
  }
  ```
- **Error Responses**:
  - 401: Invalid or expired token
  - 403: Task does not belong to user
  - 404: Task not found

### PUT /todos/{id}
**Purpose**: Update a specific task by ID
- **Headers**: Authorization: Bearer {token}
- **Path Parameter**: id (UUID of the task)
- **Request Body**:
  ```json
  {
    "title": "string (optional)",
    "description": "string (optional)",
    "due_date": "ISO 8601 datetime (optional)",
    "priority": "string (optional, low|medium|high)",
    "is_completed": "boolean (optional)"
  }
  ```
- **Success Response**: 200 OK
  ```json
  {
    "id": "UUID",
    "title": "string",
    "description": "string (optional)",
    "is_completed": "boolean",
    "due_date": "ISO 8601 datetime (optional)",
    "priority": "string",
    "created_at": "ISO 8601 datetime",
    "updated_at": "ISO 8601 datetime",
    "user_id": "UUID"
  }
  ```
- **Error Responses**:
  - 400: Invalid input data
  - 401: Invalid or expired token
  - 403: Task does not belong to user
  - 404: Task not found

### PATCH /todos/{id}/complete
**Purpose**: Toggle task completion status
- **Headers**: Authorization: Bearer {token}
- **Path Parameter**: id (UUID of the task)
- **Request Body**:
  ```json
  {
    "is_completed": "boolean (required)"
  }
  ```
- **Success Response**: 200 OK
  ```json
  {
    "id": "UUID",
    "is_completed": "boolean",
    "updated_at": "ISO 8601 datetime"
  }
  ```
- **Error Responses**:
  - 400: Invalid input data
  - 401: Invalid or expired token
  - 403: Task does not belong to user
  - 404: Task not found

### DELETE /todos/{id}
**Purpose**: Delete a specific task by ID
- **Headers**: Authorization: Bearer {token}
- **Path Parameter**: id (UUID of the task)
- **Success Response**: 204 No Content
- **Error Responses**:
  - 401: Invalid or expired token
  - 403: Task does not belong to user
  - 404: Task not found

## Common Error Response Format
```json
{
  "error": {
    "code": "string (error identifier)",
    "message": "string (human-readable error message)",
    "details": "object (optional, specific error details)"
  }
}
```

## Authentication Requirements
- All task-related endpoints require valid authentication token
- Authentication tokens must be included in Authorization header as Bearer token
- Invalid or expired tokens result in 401 Unauthorized responses
- Users can only access their own tasks (enforced by user_id checks)