import { apiClient, apiRequest, setAuthToken } from "./apiClient";

interface LoginCredentials {
  email: string;
  password: string;
}

interface RegisterCredentials {
  name: string;
  email: string;
  password: string;
}

interface User {
  id: string;
  name: string;
  email: string;
  created_at: string;
  updated_at: string;
  is_active: boolean;
}

interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

interface LoginResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  user: User;
}

interface RegisterResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  user: User;
}

// Login function
export const login = async (credentials: LoginCredentials): Promise<LoginResponse> => {
  try {
    const response = await apiRequest.post<LoginResponse>("/auth/signin", credentials);

    // Store access token in localStorage
    if (response.data.access_token) {
      localStorage.setItem("token", response.data.access_token);

      // Store refresh token separately for refresh operations
      if (response.data.refresh_token) {
        localStorage.setItem("refreshToken", response.data.refresh_token);
      }

      // Get user profile after successful login
      const userProfile = await getCurrentUser();
      localStorage.setItem("user", JSON.stringify(userProfile));
    }

    return response.data;
  } catch (error: any) {
    console.error("Login error:", error);

    // Handle different types of errors
    if (error.response) {
      // Server responded with error status
      const errorMessage = error.response.data?.detail || error.response.statusText || "Login failed";
      throw new Error(errorMessage);
    } else if (error.request) {
      // Request was made but no response received
      throw new Error("Network error: Unable to connect to server");
    } else {
      // Something else happened
      throw new Error("An unexpected error occurred during login");
    }
  }
};

// Register function
export const register = async (credentials: RegisterCredentials): Promise<RegisterResponse> => {
  try {
    // Transform the credentials to match backend expectations
    const transformedCredentials = {
      name: credentials.name,
      email: credentials.email,
      password: credentials.password,
    };

    const response = await apiRequest.post<RegisterResponse>("/auth/signup", transformedCredentials);

    // Store access token, refresh token, and user in localStorage
    if (response.data.access_token) {
      localStorage.setItem("token", response.data.access_token);

      // Store refresh token separately for refresh operations
      if (response.data.refresh_token) {
        localStorage.setItem("refreshToken", response.data.refresh_token);
      }

      // Note: The backend returns user info in the response for signup
      localStorage.setItem("user", JSON.stringify(response.data.user));
    }

    return response.data;
  } catch (error: any) {
    console.error("Registration error:", error);

    // Handle different types of errors
    if (error.response) {
      // Server responded with error status
      const errorMessage = error.response.data?.detail || error.response.statusText || "Registration failed";
      throw new Error(errorMessage);
    } else if (error.request) {
      // Request was made but no response received
      throw new Error("Network error: Unable to connect to server");
    } else {
      // Something else happened
      throw new Error("An unexpected error occurred during registration");
    }
  }
};

// Logout function
export const logout = async (): Promise<void> => {
  try {
    // Call the logout endpoint to invalidate the token on the server
    await apiRequest.post("/auth/signout");
  } catch (error) {
    // Even if the server-side logout fails, we should still clear the local session
    console.error("Logout error:", error);
  } finally {
    // Always clear local storage and auth header
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    localStorage.removeItem("refreshToken");

    // Remove auth header from axios instance
    setAuthToken(null);
  }
};

// Refresh token function
export const refreshToken = async (): Promise<TokenResponse> => {
  try {
    // Get the refresh token from local storage
    const refreshTokenFromStorage = localStorage.getItem("refreshToken");

    if (!refreshTokenFromStorage) {
      throw new Error("No refresh token available");
    }

    const response = await apiClient.post<TokenResponse>("/auth/refresh", {}, {
      headers: {
        "Authorization": `Bearer ${refreshTokenFromStorage}`,
      }
    });

    // Update the stored access token
    if (response.data.access_token) {
      localStorage.setItem("token", response.data.access_token);

      // Optionally store the new refresh token if rotation is implemented
      if (response.data.refresh_token) {
        localStorage.setItem("refreshToken", response.data.refresh_token);
      }
    }

    return response.data;
  } catch (error) {
    console.error("Token refresh error:", error);
    throw error;
  }
};

// Get current user function
export const getCurrentUser = async (): Promise<User> => {
  try {
    const response = await apiRequest.get<any>("/auth/profile");
    // Map the response to match the User interface
    return {
      id: response.data.id,
      name: response.data.name,
      email: response.data.email,
      created_at: response.data.created_at,
      updated_at: response.data.updated_at,
      is_active: response.data.is_active,
    };
  } catch (error: any) {
    console.error("Get current user error:", error);

    // Handle different types of errors
    if (error.response) {
      // Server responded with error status
      const errorMessage = error.response.data?.detail || error.response.statusText || "Failed to get user profile";
      throw new Error(errorMessage);
    } else if (error.request) {
      // Request was made but no response received
      throw new Error("Network error: Unable to connect to server");
    } else {
      // Something else happened
      throw new Error("An unexpected error occurred while fetching user profile");
    }
  }
};

// Forgot password function
export const forgotPassword = async (email: string): Promise<void> => {
  try {
    await apiRequest.post("/auth/forgot-password", { email });
  } catch (error) {
    console.error("Forgot password error:", error);
    throw error;
  }
};

// Reset password function
export const resetPassword = async (token: string, newPassword: string): Promise<void> => {
  try {
    await apiRequest.post("/auth/reset-password", {
      token,
      new_password: newPassword,  // Backend expects 'new_password' not 'newPassword'
    });
  } catch (error) {
    console.error("Reset password error:", error);
    throw error;
  }
};