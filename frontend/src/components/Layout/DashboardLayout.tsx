import React from "react";
import { Navigate } from "react-router-dom";
import { useAuth } from "../../hooks/useAuth";
import Header from "./Header";

interface DashboardLayoutProps {
  children: React.ReactNode;
  title?: string;
  requireAuth?: boolean;
}

const DashboardLayout: React.FC<DashboardLayoutProps> = ({
  children,
  title,
  requireAuth = true,
}) => {
  const { isAuthenticated, loading } = useAuth();

  // If auth is required and user is not authenticated, redirect to login
  if (requireAuth && !loading && !isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  // If still loading auth state, show loading indicator
  if (requireAuth && loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-[var(--bg-primary)]">
        <div className="text-[var(--text-primary)]">Loading...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[var(--bg-primary)] text-[var(--text-primary)]">
      <Header />
      <main className="container mx-auto py-8 px-4">
        {title && (
          <h1 className="text-3xl font-bold mb-6 text-[var(--text-primary)]">
            {title}
          </h1>
        )}
        <div className="mt-6">
          {children}
        </div>
      </main>
    </div>
  );
};

export default DashboardLayout;