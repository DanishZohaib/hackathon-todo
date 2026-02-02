import React, { useState } from "react";
import { useAuth } from "../../hooks/useAuth";
import { useNavigate } from "react-router-dom";
import Input from "../UI/Input";
import Button from "../UI/Button";

interface LoginFormProps {
  onSuccess?: () => void;
  onError?: (error: string) => void;
}

const LoginForm: React.FC<LoginFormProps> = ({ onSuccess, onError }) => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const success = await login(email, password);
      if (success) {
        onSuccess ? onSuccess() : navigate("/dashboard");
      } else {
        const errorMsg = "Invalid email or password. Please try again.";
        setError(errorMsg);
        if (onError) onError(errorMsg);
      }
    } catch (err) {
      const errorMsg = "An error occurred during login. Please try again.";
      setError(errorMsg);
      if (onError) onError(errorMsg);
      console.error("Login error:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      {error && (
        <div className="mb-4 p-3 bg-[var(--error-red)] bg-opacity-100 text-white rounded-md border border-[var(--error-red)] text-sm">
          {error}
        </div>
      )}

      <div className="space-y-4">
        <Input
          label="Email Address"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Enter your email"
          required
          error={error ? "Please check your credentials" : ""}
        />

        <Input
          label="Password"
          type={showPassword ? "text" : "password"}
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Enter your password"
          required
          endAdornment={
            <button
              type="button"
              onClick={() => setShowPassword(!showPassword)}
              className="text-[var(--text-secondary)] hover:text-[var(--pak-green-primary)]"
            >
              {showPassword ? "Hide" : "Show"}
            </button>
          }
          error={error ? "Please check your credentials" : ""}
        />
      </div>

      <Button
        type="submit"
        className="w-full mt-6"
        disabled={loading}
      >
        {loading ? (
          <span className="flex items-center justify-center">
            <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Signing in...
          </span>
        ) : "Sign In"}
      </Button>
    </form>
  );
};

export default LoginForm;