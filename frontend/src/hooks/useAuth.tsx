import { useState, useEffect, createContext, useContext } from "react";
import { setAuthToken, getAuthToken } from "../services/apiClient";
import { login as loginService, register as registerService, logout as logoutService, getCurrentUser } from "../services/authService";

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

  useEffect(() => {
    // Check if user is logged in on initial load
    const initializeAuth = async () => {
      const token = getAuthToken();
      if (token) {
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
        }
      }
      setLoading(false);
    };

    initializeAuth();
  }, []);

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

  const logout = () => {
    // Call the actual logout service
    logoutService().catch(error => {
      console.error("Logout service error:", error);
      // Even if the service call fails, we should still clear local state
    });

    // Clear token and user from localStorage
    setAuthToken(null);
    localStorage.removeItem("user");

    // Update state
    setUser(null);
    setIsAuthenticated(false);
  };

  const refreshToken = async (): Promise<boolean> => {
    try {
      // The backend doesn't have a refresh endpoint implemented yet, so we'll just return true
      // In a real implementation, this would make an API call to refresh the token
      // const response = await apiRequest.post('/auth/refresh');
      // const { newToken } = response.data;
      // setAuthToken(newToken);

      // For now, we'll just return true to indicate success
      return true;
    } catch (error) {
      console.error("Token refresh failed:", error);
      logout(); // If refresh fails, log out the user
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