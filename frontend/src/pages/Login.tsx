import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import Card from "../components/UI/Card";
import Input from "../components/UI/Input";
import Button from "../components/UI/Button";

const Login: React.FC = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const success = await login(email, password);
      if (success) {
        navigate("/dashboard");
      } else {
        setError("Invalid email or password. Please try again.");
      }
    } catch (err: any) {
      setError(err.message || "An error occurred during login. Please try again.");
      console.error("Login error:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-[var(--ai-primary)] to-[var(--ai-secondary)] p-4">
      <Card className="w-full max-w-md p-8 glass-effect">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold gradient-text">Welcome Back</h1>
          <p className="text-[var(--text-secondary)] mt-2">Sign in to your account</p>
        </div>

        {error && (
          <div className="mb-4 p-3 bg-[var(--error)] bg-opacity-20 text-white rounded-md border border-[var(--error)] glass-effect">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="space-y-4">
            <Input
              label="Email Address"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Enter your email"
              required
            />

            <Input
              label="Password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter your password"
              required
            />
          </div>

          <Button
            type="submit"
            className="w-full mt-6 bg-gradient-to-r from-[var(--neon-cyan)] to-[var(--neon-purple)] hover:from-[var(--neon-purple)] hover:to-[var(--neon-cyan)] text-white shadow-lg hover:shadow-glow"
            disabled={loading}
          >
            {loading ? "Signing in..." : "Sign In"}
          </Button>
        </form>

        <div className="mt-6 text-center text-sm text-[var(--text-secondary)]">
          Don't have an account?{" "}
          <Link to="/signup" className="text-[var(--neon-cyan)] hover:underline hover:text-[var(--neon-purple)]">
            Sign up
          </Link>
        </div>
      </Card>
    </div>
  );
};

export default Login;