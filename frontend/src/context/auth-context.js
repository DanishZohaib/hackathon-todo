import React, { createContext, useContext, useReducer } from 'react';
import { authService } from '../services/auth';

const AuthContext = createContext();

const authReducer = (state, action) => {
  switch (action.type) {
    case 'LOGIN_START':
      return { ...state, loading: true, error: null };
    case 'LOGIN_SUCCESS':
      return { ...state, loading: false, authenticated: true, user: action.payload };
    case 'LOGIN_FAILURE':
      return { ...state, loading: false, authenticated: false, error: action.payload };
    case 'LOGOUT':
      return { ...state, authenticated: false, user: null };
    case 'SET_USER':
      return { ...state, authenticated: true, user: action.payload };
    default:
      return state;
  }
};

export const AuthProvider = ({ children }) => {
  const [state, dispatch] = useReducer(authReducer, {
    authenticated: authService.isAuthenticated(),
    user: null,
    loading: false,
    error: null
  });

  const login = async (credentials) => {
    try {
      dispatch({ type: 'LOGIN_START' });
      const data = await authService.login(credentials);
      dispatch({ type: 'LOGIN_SUCCESS', payload: data.user });
      return data;
    } catch (error) {
      dispatch({ type: 'LOGIN_FAILURE', payload: error.message });
      throw error;
    }
  };

  const logout = () => {
    authService.logout();
    dispatch({ type: 'LOGOUT' });
  };

  const value = {
    ...state,
    login,
    logout
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};