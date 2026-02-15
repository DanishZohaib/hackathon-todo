import axios, { AxiosInstance, InternalAxiosRequestConfig, AxiosResponse } from "axios";

// Get the API URL from environment variables
const API_BASE_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

// Create the axios instance
const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000, // 10 seconds timeout
  headers: {
    "Content-Type": "application/json",
  },
});

// Flag to prevent multiple simultaneous refresh attempts
let isRefreshing = false;
// Queue of requests waiting for token refresh
let failedQueue: Array<{resolve: (value: any) => void, reject: (error: any) => void}> = [];

// Process the queue of failed requests after token refresh
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

// Request interceptor to add auth token if available
apiClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = localStorage.getItem("token");
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  },
);

// Response interceptor to handle common errors and auto-refresh tokens
apiClient.interceptors.response.use(
  (response: AxiosResponse) => {
    return response;
  },
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 || error.response?.status === 403) {
      const refreshToken = localStorage.getItem("refreshToken");
      
      if (!refreshToken) {
        // No refresh token available, user needs to log in again
        localStorage.removeItem("token");
        localStorage.removeItem("user");
        localStorage.removeItem("refreshToken");
        delete apiClient.defaults.headers.common["Authorization"];
        
        // Redirect to login
        window.location.href = "/login";
        return Promise.reject(error);
      }

      if (isRefreshing) {
        // If a refresh is already in progress, add this request to the queue
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject });
        }).then(token => {
          originalRequest.headers['Authorization'] = `Bearer ${token}`;
          return apiClient(originalRequest);
        }).catch(err => {
          return Promise.reject(err);
        });
      }

      isRefreshing = true;

      try {
        // Attempt to refresh the token
        const refreshResponse = await axios.post(`${API_BASE_URL}/auth/refresh`, {}, {
          headers: {
            "Authorization": `Bearer ${refreshToken}`,
          }
        });

        if (refreshResponse.data.access_token) {
          // Update tokens in storage
          localStorage.setItem("token", refreshResponse.data.access_token);
          localStorage.setItem("refreshToken", refreshResponse.data.refresh_token);
          
          // Update the axios default header
          apiClient.defaults.headers.common["Authorization"] = `Bearer ${refreshResponse.data.access_token}`;
          
          // Process the queue with the new token
          processQueue(null, refreshResponse.data.access_token);
          
          // Retry the original request
          originalRequest.headers['Authorization'] = `Bearer ${refreshResponse.data.access_token}`;
          return apiClient(originalRequest);
        } else {
          // Refresh failed, redirect to login
          localStorage.removeItem("token");
          localStorage.removeItem("user");
          localStorage.removeItem("refreshToken");
          delete apiClient.defaults.headers.common["Authorization"];
          
          window.location.href = "/login";
          return Promise.reject(error);
        }
      } catch (refreshError) {
        // Refresh failed, clear everything and redirect to login
        localStorage.removeItem("token");
        localStorage.removeItem("user");
        localStorage.removeItem("refreshToken");
        delete apiClient.defaults.headers.common["Authorization"];
        
        // Process the queue with an error
        processQueue(refreshError, null);
        
        window.location.href = "/login";
        return Promise.reject(refreshError);
      } finally {
        isRefreshing = false;
      }
    }

    return Promise.reject(error);
  },
);

export default apiClient;
export { apiClient }; // Export the instance directly

// Utility functions for common operations
export const apiRequest = {
  get: <T>(url: string, config?: InternalAxiosRequestConfig): Promise<AxiosResponse<T>> => {
    return apiClient.get<T>(url, config);
  },

  post: <T>(url: string, data?: any, config?: InternalAxiosRequestConfig): Promise<AxiosResponse<T>> => {
    return apiClient.post<T>(url, data, config);
  },

  put: <T>(url: string, data?: any, config?: InternalAxiosRequestConfig): Promise<AxiosResponse<T>> => {
    return apiClient.put<T>(url, data, config);
  },

  delete: <T>(url: string, config?: InternalAxiosRequestConfig): Promise<AxiosResponse<T>> => {
    return apiClient.delete<T>(url, config);
  },

  patch: <T>(url: string, data?: any, config?: InternalAxiosRequestConfig): Promise<AxiosResponse<T>> => {
    return apiClient.patch<T>(url, data, config);
  },
};

// Function to set auth token
export const setAuthToken = (token: string | null) => {
  if (token) {
    localStorage.setItem("token", token);
    apiClient.defaults.headers.common["Authorization"] = `Bearer ${token}`;
  } else {
    localStorage.removeItem("token");
    delete apiClient.defaults.headers.common["Authorization"];
  }
};

// Function to get auth token
export const getAuthToken = (): string | null => {
  return localStorage.getItem("token");
};