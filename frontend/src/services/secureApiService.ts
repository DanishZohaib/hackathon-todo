import { apiClient } from './apiClient';
import { refreshToken as refreshAuthToken } from './authService';
import { isValidToken, isTokenAboutToExpire } from '../utils/tokenUtils';

// Flag to prevent multiple simultaneous refresh attempts
let isRefreshing = false;
// Queue of requests waiting for token refresh
let failedQueue: Array<{resolve: (value: any) => void, reject: (error: any) => void}> = [];

/**
 * Process the queue of failed requests after token refresh
 */
const processQueue = (error: any = null, token: string | null = null) => {
  failedQueue.forEach(prom => {
    if (error) {
      prom.reject(error);
    } else {
      prom.resolve(token);
    }
  });

  failedQueue = [];
};

/**
 * Secure API request wrapper that handles token refresh automatically
 */
export const secureApiRequest = {
  get: async <T>(url: string, config?: any): Promise<any> => {
    const token = localStorage.getItem("token");
    
    // Check if token exists and is valid
    if (!token || !isValidToken(token)) {
      // If token doesn't exist or is invalid, we can't make the request
      throw new Error("Authentication required");
    }
    
    // Check if token is about to expire and refresh proactively
    if (isTokenAboutToExpire(token)) {
      return handleTokenRefreshAndRetry(() => apiClient.get<T>(url, config));
    }
    
    try {
      return await apiClient.get<T>(url, config);
    } catch (error: any) {
      if (error.response?.status === 401 || error.response?.status === 403) {
        return handleTokenRefreshAndRetry(() => apiClient.get<T>(url, config));
      }
      throw error;
    }
  },

  post: async <T>(url: string, data?: any, config?: any): Promise<any> => {
    const token = localStorage.getItem("token");
    
    // Check if token exists and is valid
    if (!token || !isValidToken(token)) {
      // If token doesn't exist or is invalid, we can't make the request
      throw new Error("Authentication required");
    }
    
    // Check if token is about to expire and refresh proactively
    if (isTokenAboutToExpire(token)) {
      return handleTokenRefreshAndRetry(() => apiClient.post<T>(url, data, config));
    }
    
    try {
      return await apiClient.post<T>(url, data, config);
    } catch (error: any) {
      if (error.response?.status === 401 || error.response?.status === 403) {
        return handleTokenRefreshAndRetry(() => apiClient.post<T>(url, data, config));
      }
      throw error;
    }
  },

  put: async <T>(url: string, data?: any, config?: any): Promise<any> => {
    const token = localStorage.getItem("token");
    
    // Check if token exists and is valid
    if (!token || !isValidToken(token)) {
      // If token doesn't exist or is invalid, we can't make the request
      throw new Error("Authentication required");
    }
    
    // Check if token is about to expire and refresh proactively
    if (isTokenAboutToExpire(token)) {
      return handleTokenRefreshAndRetry(() => apiClient.put<T>(url, data, config));
    }
    
    try {
      return await apiClient.put<T>(url, data, config);
    } catch (error: any) {
      if (error.response?.status === 401 || error.response?.status === 403) {
        return handleTokenRefreshAndRetry(() => apiClient.put<T>(url, data, config));
      }
      throw error;
    }
  },

  delete: async <T>(url: string, config?: any): Promise<any> => {
    const token = localStorage.getItem("token");
    
    // Check if token exists and is valid
    if (!token || !isValidToken(token)) {
      // If token doesn't exist or is invalid, we can't make the request
      throw new Error("Authentication required");
    }
    
    // Check if token is about to expire and refresh proactively
    if (isTokenAboutToExpire(token)) {
      return handleTokenRefreshAndRetry(() => apiClient.delete<T>(url, config));
    }
    
    try {
      return await apiClient.delete<T>(url, config);
    } catch (error: any) {
      if (error.response?.status === 401 || error.response?.status === 403) {
        return handleTokenRefreshAndRetry(() => apiClient.delete<T>(url, config));
      }
      throw error;
    }
  },

  patch: async <T>(url: string, data?: any, config?: any): Promise<any> => {
    const token = localStorage.getItem("token");
    
    // Check if token exists and is valid
    if (!token || !isValidToken(token)) {
      // If token doesn't exist or is invalid, we can't make the request
      throw new Error("Authentication required");
    }
    
    // Check if token is about to expire and refresh proactively
    if (isTokenAboutToExpire(token)) {
      return handleTokenRefreshAndRetry(() => apiClient.patch<T>(url, data, config));
    }
    
    try {
      return await apiClient.patch<T>(url, data, config);
    } catch (error: any) {
      if (error.response?.status === 401 || error.response?.status === 403) {
        return handleTokenRefreshAndRetry(() => apiClient.patch<T>(url, data, config));
      }
      throw error;
    }
  },
};

/**
 * Handle token refresh and retry the original request
 */
const handleTokenRefreshAndRetry = async (requestFn: () => Promise<any>) => {
  const refreshToken = localStorage.getItem("refreshToken");
  
  if (!refreshToken) {
    // No refresh token available, user needs to log in again
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    localStorage.removeItem("refreshToken");
    delete apiClient.defaults.headers.common["Authorization"];
    
    // Redirect to login
    window.location.href = "/login";
    throw new Error("Session expired. Please log in again.");
  }

  if (isRefreshing) {
    // If a refresh is already in progress, add this request to the queue
    return new Promise((resolve, reject) => {
      failedQueue.push({ resolve, reject });
    });
  }

  isRefreshing = true;

  try {
    const response = await refreshAuthToken();
    
    // Process the queue with the new token
    processQueue(null, response.access_token);
    
    // Retry the original request
    return await requestFn();
  } catch (error) {
    // If refresh fails, clear everything and redirect to login
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    localStorage.removeItem("refreshToken");
    delete apiClient.defaults.headers.common["Authorization"];
    
    // Process the queue with an error
    processQueue(error, null);
    
    // Redirect to login
    window.location.href = "/login";
    throw new Error("Session expired. Please log in again.");
  } finally {
    isRefreshing = false;
  }
};