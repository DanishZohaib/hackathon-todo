# Quickstart Guide: Phase II – Frontend UI Enhancement (Dark + Pakistan Theme)

## Prerequisites
- Node.js 18.x or higher
- npm or yarn package manager
- Access to the existing backend API
- Git for version control

## Setup Instructions

### 1. Clone and Navigate
```bash
git clone <repository-url>
cd <project-directory>
```

### 2. Install Dependencies
```bash
npm install
# or
yarn install
```

### 3. Environment Configuration
Create a `.env` file in the root directory:
```
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_THEME_DEFAULT=dark
REACT_APP_PRIMARY_COLOR=#006600
```

### 4. Start Development Server
```bash
npm start
# or
yarn start
```

The application will be available at http://localhost:3000

## Key Components

### Theme System
- The application defaults to dark theme
- Pakistan green (#006600) is used as the primary accent color
- Themes are managed via ThemeProvider component

### Authentication Flow
1. Navigate to `/login` or `/signup`
2. Complete the respective forms
3. User is redirected to dashboard upon successful authentication
4. Session persists until explicit signout

### Todo Management
1. On the dashboard, use the "Add Todo" form to create new tasks
2. Toggle checkboxes to mark tasks as complete/incomplete
3. Click the trash icon to delete tasks
4. Cards display with appropriate visual feedback

## Running Tests
```bash
# Unit tests
npm run test
# or
yarn test

# End-to-end tests
npm run test:e2e
# or
yarn test:e2e
```

## Building for Production
```bash
npm run build
# or
yarn build
```

The optimized build will be available in the `build/` directory.