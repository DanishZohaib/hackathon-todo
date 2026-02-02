# Data Model: Phase II – Frontend UI Enhancement (Dark + Pakistan Theme)

## Overview
Data models for the UI enhancement feature, focusing on frontend representation of backend entities.

## User Entity
**Representation**: Frontend user object for authentication and UI personalization
- id: string | Unique identifier for the user
- username: string | User's display name
- email: string | User's email address
- createdAt: string | Account creation timestamp
- isAuthenticated: boolean | Authentication status flag

**Relationships**: Owns multiple Todo entities

## Todo Entity
**Representation**: Individual task with state and metadata
- id: string | Unique identifier for the todo
- title: string | Title of the task (max 255 chars)
- completed: boolean | Completion status
- createdAt: string | Creation timestamp
- updatedAt: string | Last update timestamp
- userId: string | Owner of this todo

**State Transitions**:
- New → Active (on creation)
- Active ↔ Completed (toggle via checkbox)
- Any state → Deleted (on deletion)

**Validation Rules**:
- Title must be 1-255 characters
- UserId must be a valid user reference
- Creation and update timestamps are auto-generated

## Theme Entity
**Representation**: Theme settings for UI customization
- mode: 'light' | 'dark' | Current theme mode (default: 'dark')
- primaryColor: string | Primary accent color (default: '#006600' for Pakistan green)
- fontSize: 'small' | 'normal' | 'large' | Font size preference
- animationsEnabled: boolean | Whether UI animations are enabled

## UI State Entity
**Representation**: Temporary UI state not persisted to backend
- isLoading: boolean | Global loading state
- errorMessage: string | Error messages for user feedback
- successMessage: string | Success messages for user feedback
- currentPage: string | Currently active page/route

## Session Entity
**Representation**: Authentication session state
- token: string | JWT or session token
- expiresAt: string | Token expiration timestamp
- user: User | Associated user object