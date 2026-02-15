import React from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../../hooks/useAuth";
import Button from "../UI/Button";
import ThemeToggle from "../UI/ThemeToggle";

const Header: React.FC = () => {
  const { user, isAuthenticated, logout } = useAuth();

  return (
    <header className="glass-effect border-b border-[var(--bg-glass-border)] py-4 px-6 sticky top-0 z-10">
      <div className="container mx-auto flex justify-between items-center">
        <div className="flex items-center space-x-2">
          <Link to="/" className="text-xl font-bold gradient-text">
            Todo<span className="text-[var(--text-primary)]">AI</span>
          </Link>
          <span className="text-[var(--text-secondary)] text-sm hidden md:inline">AI-Powered Edition</span>
        </div>

        <nav className="hidden md:flex items-center space-x-6">
          <ThemeToggle />
          {isAuthenticated ? (
            <>
              <Link to="/dashboard" className="text-[var(--text-primary)] hover:text-[var(--neon-cyan)] transition-colors">
                Dashboard
              </Link>
              <Link to="/todos" className="text-[var(--text-primary)] hover:text-[var(--neon-cyan)] transition-colors">
                My Todos
              </Link>
              <span className="text-[var(--text-secondary)]">Welcome, {user?.name}</span>
              <Button variant="outline" size="sm" onClick={logout}>
                Logout
              </Button>
            </>
          ) : (
            <>
              <Link to="/login" className="text-[var(--text-primary)] hover:text-[var(--neon-cyan)] transition-colors">
                Login
              </Link>
              <Link to="/signup" className="text-[var(--text-primary)] hover:text-[var(--neon-cyan)] transition-colors">
                Sign Up
              </Link>
            </>
          )}
        </nav>

        {/* Mobile menu button */}
        <div className="md:hidden flex items-center space-x-2">
          <ThemeToggle />
          {isAuthenticated ? (
            <Button variant="outline" size="sm" onClick={logout}>
              Logout
            </Button>
          ) : (
            <Link to="/login">
              <Button variant="outline" size="sm">
                Login
              </Button>
            </Link>
          )}
        </div>
      </div>
    </header>
  );
};

export default Header;