---
id: 5
title: Phase II Specs
stage: spec
date: 2026-01-04
surface: agent
model: Claude Sonnet 4.5
feature: phase-ii-specs
branch: 001-phase-ii-specs
user: user
command: sp.specify
labels: [spec, phase-ii, todo-app, authentication, persistence, api]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - specs/001-phase-ii-specs/009_user_model_and_auth.md
 - specs/001-phase-ii-specs/010_task_persistence_schema.md
 - specs/001-phase-ii-specs/011_rest_api_contract.md
 - specs/001-phase-ii-specs/012_frontend_pages_and_flows.md
 - specs/001-phase-ii-specs/013_api_frontend_integration.md
tests: []
---

## Prompt

```
### Prompt

You are now specifying **Phase II only** of the Todo project.

## Scope
You MUST define specifications for:
1. Database schema
2. REST API
3. Authentication
4. Frontend UI
5. User-scoped task behavior

## Mandatory Phase II Specs

Create the following specs (DO NOT IMPLEMENT YET):

### Backend
- 009_user_model_and_auth.md
- 010_task_persistence_schema.md
- 011_rest_api_contract.md

### Frontend
- 012_frontend_pages_and_flows.md
- 013_api_frontend_integration.md

## Spec Rules
- Describe WHAT, never HOW
- APIs must be RESTful
- Authentication must be explicit
- Each spec must list:
  - Purpose
  - Functional Requirements
  - Acceptance Criteria
  - Out of Scope

Stop after Phase II specs are complete.
📄 EXAMPLE HIGH-IMPACT SPEC (JUDGES LOVE THIS)
011_rest_api_contract.md
Purpose
Define RESTful endpoints for managing user-specific todo tasks.

Endpoints

Method    Endpoint    Description
POST    /auth/signup    Register user
POST    /auth/signin    Authenticate user
GET    /todos    List user's tasks
POST    /todos    Creat### Prompt

You are now specifying **Phase II only** of the Todo project.

## Scope
You MUST define specifications for:
1. Database schema
2. REST API
3. Authentication
4. Frontend UI
5. User-scoped task behavior

## Mandatory Phase II Specs

Create the following specs (DO NOT IMPLEMENT YET):

### Backend
- 009_user_model_and_auth.md
- 010_task_persistence_schema.md
- 011_rest_api_contract.md

### Frontend
- 012_frontend_pages_and_flows.md
- 013_api_frontend_integration.md

## Spec Rules
- Describe WHAT, never HOW
- APIs must be RESTful
- Authentication must be explicit
- Each spec must list:
  - Purpose
  - Functional Requirements
  - Acceptance Criteria
  - Out of Scope

Stop after Phase II specs are complete.
📄 EXAMPLE HIGH-IMPACT SPEC (JUDGES LOVE THIS)
011_rest_api_contract.md
Purpose
Define RESTful endpoints for managing user-specific todo tasks.

Endpoints

Method    Endpoint    Description
POST    /auth/signup    Register user
POST    /auth/signin    Authenticate user
GET    /todos    List user's tasks
POST    /todos    Creat
```

## Response snapshot

Created all five required Phase II specifications for the Todo project:

1. **009_user_model_and_auth.md**: Defines user data model and authentication system with secure registration, login, and session management
2. **010_task_persistence_schema.md**: Specifies database schema for user-specific task storage with proper relationships and data integrity
3. **011_rest_api_contract.md**: Details RESTful API endpoints for user authentication and task management with proper HTTP standards
4. **012_frontend_pages_and_flows.md**: Outlines frontend UI pages and user navigation flows for the web-based todo application
5. **013_api_frontend_integration.md**: Defines how the frontend integrates with the backend API for data flow and error handling

Each specification follows the required format with Purpose, Functional Requirements, Acceptance Criteria, and Out of Scope sections. All specifications focus on WHAT the system should do rather than HOW to implement it, with explicit authentication requirements and RESTful API design.

## Outcome

- ✅ Impact: Created comprehensive Phase II specifications covering all required areas (authentication, persistence, API, frontend)
- 🧪 Tests: No tests required for documentation specifications
- 📁 Files: Created 5 specification files in specs/001-phase-ii-specs/ directory
- 🔁 Next prompts: Ready for Phase II planning and implementation
- 🧠 Reflection: Specifications provide clear requirements for Phase II development while maintaining consistency with Phase I constitution

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A for documentation creation
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin Phase II implementation following these specifications