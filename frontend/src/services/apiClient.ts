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

// Response interceptor to handle common errors
apiClient.interceptors.response.use(
  (response: AxiosResponse) => {
    return response;
  },
  (error) => {
    if (error.response?.status === 401) {
      // Unauthorized - possibly log out the user
      localStorage.removeItem("token");
      localStorage.removeItem("user");
      window.location.href = "/login"; // Redirect to login
    }

    return Promise.reject(error);
  },
);

export default apiClient;

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