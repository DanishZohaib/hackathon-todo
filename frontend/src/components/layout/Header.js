import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { isAuthenticated, removeAuthToken } from '../../utils/auth';

const Header = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    removeAuthToken();
    navigate('/signin');
  };

  return (
    <header className="bg-blue-600 text-white shadow-md">
      <div className="container mx-auto px-4 py-3">
        <div className="flex justify-between items-center">
          <Link to="/" className="text-xl font-bold">
            Todo App
          </Link>

          <nav>
            {isAuthenticated() ? (
              <div className="flex items-center space-x-4">
                <Link to="/dashboard" className="hover:text-blue-200 transition">
                  Dashboard
                </Link>
                <button
                  onClick={handleLogout}
                  className="bg-red-500 hover:bg-red-600 px-4 py-2 rounded transition"
                >
                  Logout
                </button>
              </div>
            ) : (
              <div className="flex space-x-4">
                <Link to="/signin" className="hover:text-blue-200 transition">
                  Sign In
                </Link>
                <Link to="/signup" className="hover:text-blue-200 transition">
                  Sign Up
                </Link>
              </div>
            )}
          </nav>
        </div>
      </div>
    </header>
  );
};

export default Header;