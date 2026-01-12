# Todo App Frontend

This is the frontend for the Todo application built with React and integrated with a FastAPI backend.

## Features

- User authentication (signup/login)
- Todo management (create, read, update, delete, mark complete)
- Responsive design using Tailwind CSS
- Secure API communication with token-based authentication

## Architecture

- **Components**: UI components organized in `src/components/`
- **Pages**: Application pages in `src/pages/`
- **Services**: API communication in `src/services/`
- **Context**: Authentication state management in `src/context/`
- **Utils**: Utility functions in `src/utils/`
- **Router**: Navigation and routing in `src/router/`

## Services

- `api.js`: Axios-based API service with authentication interceptors
- `authService.js`: Authentication API operations
- `taskService.js`: Todo management API operations

## Security

- Token-based authentication using localStorage
- Automatic token inclusion in API requests
- Automatic logout on 401 responses
- Secure token removal on logout

## Getting Started

1. Install dependencies: `npm install`
2. Set environment variables (REACT_APP_API_URL)
3. Start the development server: `npm start`

## Environment Variables

- `REACT_APP_API_URL`: Backend API URL (default: http://localhost:8000)