# Quickstart Guide for Phase II Todo Application

## Development Setup

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL (or access to Neon PostgreSQL instance)
- Git

### Backend Setup
1. Navigate to backend directory: `cd backend`
2. Create virtual environment: `python -m venv venv`
3. Activate virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix/Mac: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Set up environment variables (see `.env.example`)
6. Run database migrations: `python -m src.database.migrations`
7. Start the server: `python -m src.main`

### Frontend Setup
1. Navigate to frontend directory: `cd frontend`
2. Install dependencies: `npm install`
3. Set up environment variables (see `.env.example`)
4. Start development server: `npm run dev`

## API Endpoints

### Authentication
- Register: `POST /auth/signup`
- Login: `POST /auth/signin`
- Logout: `POST /auth/signout`

### Tasks
- List tasks: `GET /todos`
- Create task: `POST /todos`
- Get task: `GET /todos/{id}`
- Update task: `PUT /todos/{id}`
- Complete task: `PATCH /todos/{id}/complete`
- Delete task: `DELETE /todos/{id}`

## Database Schema

### Users Table
- id (UUID, Primary Key)
- email (VARCHAR, Unique, Not Null)
- password_hash (VARCHAR, Not Null)
- name (VARCHAR)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)
- is_active (BOOLEAN, Default: true)

### Tasks Table
- id (UUID, Primary Key)
- title (VARCHAR, Not Null)
- description (TEXT)
- is_completed (BOOLEAN, Default: false)
- due_date (TIMESTAMP)
- priority (VARCHAR, Default: 'medium')
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)
- user_id (UUID, Foreign Key to users.id)

## Environment Variables

### Backend (.env)
```
DATABASE_URL=postgresql://user:password@localhost:5432/todo_app
SECRET_KEY=your-super-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Frontend (.env)
```
REACT_APP_API_URL=http://localhost:8000
REACT_APP_AUTH_DOMAIN=your-auth-domain
```

## Running Tests

### Backend Tests
```bash
# Run all tests
python -m pytest

# Run unit tests
python -m pytest tests/unit/

# Run integration tests
python -m pytest tests/integration/
```

### Frontend Tests
```bash
# Run all tests
npm test

# Run unit tests
npm run test:unit

# Run integration tests
npm run test:integration
```

## Docker Setup (Optional)
```bash
# Build and run with Docker Compose
docker-compose up --build

# Run tests in Docker
docker-compose run backend pytest
docker-compose run frontend npm test
```