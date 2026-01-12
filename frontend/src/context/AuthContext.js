import React, { createContext, useContext, useEffect, useState } from 'react';
import { getAuthToken, removeAuthToken, storeAuthToken } from '../utils/auth';
import { authService } from '../services/authService';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if user is authenticated on initial load
    const token = getAuthToken();
    if (token) {
      // In a real implementation, you might want to validate the token
      // by fetching user info from the API
      setIsAuthenticated(true);
      // You could also fetch user profile here:
      // fetchUserProfile();
    }
    setLoading(false);
  }, []);

  const login = async (credentials) => {
    try {
      const response = await authService.login(credentials);
      const { token, user } = response;

      storeAuthToken(token);
      setUser(user);
      setIsAuthenticated(true);

      return { success: true, user };
    } catch (error) {
      return { success: false, error: error.message };
    }
  };

  const register = async (userData) => {
    try {
      const response = await authService.register(userData);
      const { token, user } = response;

      storeAuthToken(token);
      setUser(user);
      setIsAuthenticated(true);

      return { success: true, user };
    } catch (error) {
      return { success: false, error: error.message };
    }
  };

  const logout = async () => {
    try {
      await authService.logout();
      removeAuthToken();
      setUser(null);
      setIsAuthenticated(false);
      return { success: true };
    } catch (error) {
      return { success: false, error: error.message };
    }
  };

  const value = {
    user,
    isAuthenticated,
    loading,
    login,
    register,
    logout,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};