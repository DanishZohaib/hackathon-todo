// Auth token storage and management utilities

// Store auth token in local storage
export const storeAuthToken = (token) => {
  if (token) {
    localStorage.setItem('authToken', token);
  }
};

// Get auth token from local storage
export const getAuthToken = () => {
  return localStorage.getItem('authToken');
};

// Remove auth token from local storage (logout)
export const removeAuthToken = () => {
  localStorage.removeItem('authToken');
};

// Check if user is authenticated
export const isAuthenticated = () => {
  const token = getAuthToken();
  // In a real implementation, you might want to validate the token
  // For now, we just check if it exists
  return !!token;
};

// Set auth token in HTTP headers for future requests
export const setAuthHeader = (token) => {
  if (token) {
    // This is handled by the axios interceptor in api.js
    // but we can expose this function for consistency
    storeAuthToken(token);
  } else {
    removeAuthToken();
  }
};

// Clear all auth-related data
export const clearAuthData = () => {
  removeAuthToken();
  // Clear any other auth-related data if needed
  sessionStorage.removeItem('user');
};