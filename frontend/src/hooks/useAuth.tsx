import { useState, useEffect, useCallback, createContext, useContext } from "react";
import { apiClient, setAuthToken, getAuthToken } from "../services/apiClient";
import { login as loginService, register as registerService, logout as logoutService, getCurrentUser } from "../services/authService";
import { isValidToken, isTokenAboutToExpire } from "../utils/tokenUtils";

interface User {
  id: string;
  name: string;
  email: string;
  created_at: string;
  updated_at: string;
  is_active: boolean;
}

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  loading: boolean;
  login: (email: string, password: string) => Promise<boolean>;
  signup: (username: string, email: string, password: string) => Promise<boolean>;
  logout: () => void;
  refreshToken: () => Promise<boolean>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};

interface AuthProviderProps {
  children: React.ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(true);

  const logout = () => {
    // Call the actual logout service
    logoutService().catch(error => {
      console.error("Logout service error:", error);
      // Even if the service call fails, we should still clear local state
    });

    // Clear all auth-related data from localStorage
    setAuthToken(null);
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    localStorage.removeItem("refreshToken");

    // Update state
    setUser(null);
    setIsAuthenticated(false);
  };

  const refreshToken = useCallback(async (): Promise<boolean> => {
    try {
      const refreshTokenFromStorage = localStorage.getItem("refreshToken");
      if (!refreshTokenFromStorage) {
        throw new Error("No refresh token available");
      }

      // Make API call to refresh the access token
      const response = await apiClient.post("/auth/refresh", {}, {
        headers: {
          "Authorization": `Bearer ${refreshTokenFromStorage}`
        }
      });

      if (response.data.access_token) {
        // Update both tokens in storage
        setAuthToken(response.data.access_token);
        localStorage.setItem("refreshToken", response.data.refresh_token);

        // Update user data if needed
        const userProfile = await getCurrentUser();
        setUser(userProfile);
        setIsAuthenticated(true);

        return true;
      }

      return false;
    } catch (error) {
      console.error("Token refresh failed:", error);
      logout(); // If refresh fails, log out the user
      return false;
    }
  }, [setAuthToken, setUser, setIsAuthenticated, logout]); // Add dependencies as needed

  useEffect(() => {
    // Check if user is logged in on initial load
    const initializeAuth = async () => {
      const token = getAuthToken();

      if (token && isValidToken(token)) {
        try {
          // Attempt to get user info with the stored token
          const userProfile = await getCurrentUser();
          setUser(userProfile);
          setIsAuthenticated(true);
        } catch (error) {
          console.error("Failed to verify token:", error);
          // If token verification fails, clear it
          localStorage.removeItem("token");
          localStorage.removeItem("user");
          localStorage.removeItem("refreshToken");
        }
      } else if (token && !isValidToken(token)) {
        // Token exists but is expired, clear it
        console.log("Token is expired, clearing...");
        localStorage.removeItem("token");
        localStorage.removeItem("user");
        localStorage.removeItem("refreshToken");
        setAuthToken(null);
      }

      setLoading(false);
    };

    initializeAuth();
  }, []);

  // Set up interval to check for token expiration and refresh proactively
  useEffect(() => {
    const scheduleTokenRefresh = () => {
      const token = getAuthToken();
      
      if (token && isValidToken(token) && isTokenAboutToExpire(token)) {
        // Token is about to expire, refresh it now
        refreshToken().catch(error => {
          console.error("Automatic token refresh failed:", error);
        });
      }
    };

    // Check every minute for token expiration
    const interval = setInterval(scheduleTokenRefresh, 60000); // Check every minute

    return () => {
      clearInterval(interval);
    };
  }, [isAuthenticated, refreshToken]);

  const login = async (email: string, password: string): Promise<boolean> => {
    try {
      const response = await loginService({ email, password });

      // Update state with real user data
      if (response.access_token) {
        setAuthToken(response.access_token);

        // Get the user data from localStorage that was set by the service
        const storedUser = localStorage.getItem("user");
        if (storedUser) {
          const user = JSON.parse(storedUser);
          setUser(user);
          setIsAuthenticated(true);
        }
      }

      return true;
    } catch (error) {
      console.error("Login failed:", error);
      return false;
    }
  };

  const signup = async (name: string, email: string, password: string): Promise<boolean> => {
    try {
      const response = await registerService({ name, email, password });

      // Update state with real user data
      if (response.access_token) {
        setAuthToken(response.access_token);

        // Get the user data from localStorage that was set by the service
        const storedUser = localStorage.getItem("user");
        if (storedUser) {
          const user = JSON.parse(storedUser);
          setUser(user);
          setIsAuthenticated(true);
        }
      }

      return true;
    } catch (error) {
      console.error("Signup failed:", error);
      return false;
    }
  };

  const value = {
    user,
    isAuthenticated,
    loading,
    login,
    signup,
    logout,
    refreshToken,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};