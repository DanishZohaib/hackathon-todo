# Todo Application - Phase II

A full-stack web application with persistent storage, authentication, and RESTful API built as Phase II of a multi-phase system. This phase extends the Phase I CLI application to include multi-user access, persistent storage, web interface, and authentication.

## Features

### Phase I Features (In-Memory CLI)
- Add new tasks with descriptions
- List all tasks with their status
- Mark tasks as complete
- Delete tasks
- Robust error handling
- Interactive and command-line interfaces

### Phase II Features (Web App with Persistence)
- Multi-user access with registration and authentication
- Persistent storage using PostgreSQL
- Task management (create, read, update, delete)
- Task completion tracking
- Task priority management (low, medium, high)
- Task filtering and search
- Responsive web interface
- RESTful API with JWT authentication

## Tech Stack

### Backend
- Python 3.11
- FastAPI
- PostgreSQL (via Neon)
- SQLAlchemy/SQLModel
- JWT-based authentication
- Pydantic for data validation

### Frontend
- React
- React Router
- Tailwind CSS
- Axios for API communication

## Requirements

### Backend
- Python 3.11 or higher
- PostgreSQL database

### Frontend
- Node.js 18 or higher
- npm or yarn

## Setup

### Backend

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables in `.env`:
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

5. Run the application:
   ```bash
   uvicorn src.main:app --reload --port 8000
   ```

### Frontend

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Set up environment variables in `.env`:
   ```bash
   cp .env.example .env
   # Edit .env with your backend API URL
   ```

4. Run the development server:
   ```bash
   npm start
   ```

## API Documentation

The API documentation is available at `http://localhost:8000/docs` when the backend is running.

## Project Structure

```
backend/
├── src/
│   ├── models/      # Data models (User, Task)
│   ├── services/    # Business logic (AuthService, TaskService, UserService)
│   ├── api/         # API routes (auth_router, task_router)
│   ├── database/    # Database connection and migrations
│   ├── config/      # Configuration settings
│   └── utils/       # Utility functions
└── tests/           # Test files

frontend/
├── src/
│   ├── components/  # React components (task list, form, toggle)
│   ├── pages/       # Page components (signup, signin, dashboard)
│   ├── services/    # API services (auth, task)
│   ├── context/     # React context (auth context)
│   ├── utils/       # Utility functions
│   └── public/      # Static assets
```

## Design Principles

- **Spec-Driven Development**: All functionality based on written specifications
- **Separation of Concerns**: Clear boundaries between models, services, and API layers
- **API-First Design**: All business operations exposed via RESTful APIs
- **Persistence with Discipline**: PostgreSQL is single source of truth
- **Authentication Boundary**: Every task belongs to exactly one user
- **Stateless Backend**: Backend services are stateless
- **Forward Compatibility**: Architecture supports evolution to AI integration and cloud deployment

## Phase II Completion

This Phase II implementation:
- Delivers a multi-user web application with persistent storage
- Implements secure authentication and user isolation
- Provides a responsive web interface for task management
- Follows RESTful API design principles
- Maintains the clean architecture established in Phase I
- Sets foundation for future phases with AI and cloud capabilities

Future phases will add AI features, chatbot integration, and cloud deployment capabilities.