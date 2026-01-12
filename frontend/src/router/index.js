import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { isAuthenticated } from '../utils/auth';
import MainLayout from '../components/layout/MainLayout';
import Signup from '../pages/Signup';
import Signin from '../pages/Signin';
import TodoDashboard from '../pages/TodoDashboard';
import Home from '../pages/Home'; // We'll create this as well

// Protected route component
const ProtectedRoute = ({ children }) => {
  return isAuthenticated() ? children : <Navigate to="/signin" />;
};

// Public route component (redirects if already logged in)
const PublicRoute = ({ children }) => {
  return !isAuthenticated() ? children : <Navigate to="/dashboard" />;
};

const AppRouter = () => {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route
            path="/"
            element={
              <MainLayout>
                <Home />
              </MainLayout>
            }
          />

          <Route
            path="/signup"
            element={
              <MainLayout>
                <PublicRoute>
                  <Signup />
                </PublicRoute>
              </MainLayout>
            }
          />

          <Route
            path="/signin"
            element={
              <MainLayout>
                <PublicRoute>
                  <Signin />
                </PublicRoute>
              </MainLayout>
            }
          />

          <Route
            path="/dashboard"
            element={
              <MainLayout>
                <ProtectedRoute>
                  <TodoDashboard />
                </ProtectedRoute>
              </MainLayout>
            }
          />

          {/* Catch-all route */}
          <Route
            path="*"
            element={
              <MainLayout>
                <div className="text-center">
                  <h1 className="text-2xl font-bold">404 - Page Not Found</h1>
                  <p>The page you're looking for doesn't exist.</p>
                </div>
              </MainLayout>
            }
          />
        </Routes>
      </div>
    </Router>
  );
};

export default AppRouter;