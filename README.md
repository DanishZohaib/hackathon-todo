# Hackathon Todo Application - Phase III: AI Chatbot Integration

This is a full-stack todo application with AI chatbot integration built as part of a hackathon project. The application consists of a React frontend and a FastAPI backend with PostgreSQL database.

## Project Structure

- `backend/` - FastAPI backend with authentication, todo management, and AI chatbot
- `frontend/` - React TypeScript frontend with Tailwind CSS
- `specs/` - Specification documents for the various features
- `history/` - Prompt history records and development artifacts

## Phase 3: AI Chatbot Integration

The application is currently in Phase 3, which integrates an AI chatbot using Model Context Protocol (MCP) to interact with the todo system using natural language.

## Getting Started

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables by copying the sample:
   ```bash
   cp .env.example .env  # if available
   ```

   Make sure to set a strong SECRET_KEY in the .env file:
   ```bash
   SECRET_KEY=your_very_long_secret_key_here_at_least_32_characters
   ```

4. Start the backend server:
   ```bash
   python run_server.py
   # or alternatively:
   python -m uvicorn src.main:app --reload --port 8000
   ```

   The backend will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

   The frontend will be available at `http://localhost:3000`

## API Endpoints

- `GET /health` - Health check endpoint
- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /redoc` - Alternative API documentation (ReDoc)

### Authentication Endpoints
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `POST /auth/logout` - User logout

### Todo Endpoints
- `GET /todos` - Get all user's todos
- `POST /todos` - Create a new todo
- `PUT /todos/{id}` - Update a todo
- `DELETE /todos/{id}` - Delete a todo
- `PATCH /todos/{id}/complete` - Mark a todo as complete/incomplete

### Chat Endpoints
- `POST /chat/{user_id}/chat` - AI chatbot endpoint for natural language todo management

## Features

1. **User Authentication** - Secure user registration and login
2. **Todo Management** - Full CRUD operations for todo items
3. **AI Chatbot Integration** - Natural language interaction for todo management
4. **Rate Limiting** - Protection against API abuse
5. **CORS Support** - Cross-origin resource sharing for frontend integration
6. **Database Persistence** - PostgreSQL with SQLAlchemy/SQLModel ORM

## Development

The application follows a spec-driven development approach with comprehensive documentation in the `specs/` directory.

## Technologies Used

### Backend
- FastAPI
- PostgreSQL
- SQLAlchemy/SQLModel
- JWT Authentication
- OpenAI/MCP Integration

### Frontend
- React 18
- TypeScript
- Tailwind CSS
- React Router
- Axios

## Phase Progression

- **Phase 1**: In-memory CLI Todo Application
- **Phase 2**: Full-stack web application with authentication
- **Phase 3**: AI Chatbot integration with natural language processing