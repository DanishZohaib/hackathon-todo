import React from 'react';

const Home = () => {
  return (
    <div className="container mx-auto px-4 py-8">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-gray-800 mb-4">Welcome to the Todo App</h1>
        <p className="text-lg text-gray-600 mb-8">
          Manage your tasks efficiently with our intuitive interface.
        </p>
        <div className="flex justify-center space-x-4">
          <a
            href="/signin"
            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
          >
            Sign In
          </a>
          <a
            href="/signup"
            className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded"
          >
            Sign Up
          </a>
        </div>
      </div>
    </div>
  );
};

export default Home;