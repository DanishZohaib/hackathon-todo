import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import Card from "../components/UI/Card";
import Input from "../components/UI/Input";
import Button from "../components/UI/Button";

const Signup: React.FC = () => {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const { signup } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (password !== confirmPassword) {
      setError("Passwords do not match");
      return;
    }

    setError("");
    setLoading(true);

    try {
      const success = await signup(name, email, password);
      if (success) {
        navigate("/dashboard");
      } else {
        setError("An error occurred during signup. Please try again.");
      }
    } catch (err: any) {
      setError(err.message || "An error occurred during signup. Please try again.");
      console.error("Signup error:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-[var(--ai-primary)] to-[var(--ai-secondary)] p-4">
      <Card className="w-full max-w-md p-8 glass-effect">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold gradient-text">Create Account</h1>
          <p className="text-[var(--text-secondary)] mt-2">Join our community today</p>
        </div>

        {error && (
          <div className="mb-4 p-3 bg-[var(--error)] bg-opacity-20 text-white rounded-md border border-[var(--error)] glass-effect">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="space-y-4">
            <Input
              label="Full Name"
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="Enter your full name"
              required
            />

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
              placeholder="Create a password"
              required
            />

            <Input
              label="Confirm Password"
              type="password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              placeholder="Confirm your password"
              required
            />
          </div>

          <Button
            type="submit"
            className="w-full mt-6 bg-gradient-to-r from-[var(--neon-cyan)] to-[var(--neon-purple)] hover:from-[var(--neon-purple)] hover:to-[var(--neon-cyan)] text-white shadow-lg hover:shadow-glow"
            disabled={loading}
          >
            {loading ? "Creating account..." : "Sign Up"}
          </Button>
        </form>

        <div className="mt-6 text-center text-sm text-[var(--text-secondary)]">
          Already have an account?{" "}
          <Link to="/login" className="text-[var(--neon-cyan)] hover:underline hover:text-[var(--neon-purple)]">
            Sign in
          </Link>
        </div>
      </Card>
    </div>
  );
};

export default Signup;