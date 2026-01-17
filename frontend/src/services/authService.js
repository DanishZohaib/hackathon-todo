import api from './api';

export const authService = {
  // User registration
  async register(userData) {
    try {
      const response = await api.post('/auth/signup', userData);
      return response.data;
    } catch (error) {
      console.error('Error during registration:', error);
      throw error;
    }
  },

  // User login
  async login(credentials) {
    try {
      const response = await api.post('/auth/signin', credentials);
      return response.data;
    } catch (error) {
      console.error('Error during login:', error);
      throw error;
    }
  },

  // User logout
  async logout() {
    try {
      // Call the backend logout endpoint
      await api.post('/auth/signout');
      // Remove the token from local storage
      localStorage.removeItem('token');
      return { success: true };
    } catch (error) {
      // Even if the backend call fails, still remove the local token
      localStorage.removeItem('token');
      console.error('Error during logout:', error);
      return { success: true };
    }
  },

  // Get current user profile (if needed)
  async getProfile() {
    try {
      const response = await api.get('/auth/profile');
      return response.data;
    } catch (error) {
      console.error('Error fetching profile:', error);
      throw error;
    }
  }
};