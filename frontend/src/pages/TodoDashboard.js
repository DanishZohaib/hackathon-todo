import React, { useState, useEffect } from 'react';
import { taskService } from '../services/taskService';

const TodoDashboard = () => {
  const [todos, setTodos] = useState([]);
  const [newTodo, setNewTodo] = useState('');
  const [editingTodoId, setEditingTodoId] = useState(null);
  const [editingTodoTitle, setEditingTodoTitle] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  // Fetch todos on component mount
  useEffect(() => {
    fetchTodos();
  }, []);

  const fetchTodos = async () => {
    try {
      setLoading(true);
      const data = await taskService.getTasks();
      setTodos(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleAddTodo = async (e) => {
    e.preventDefault();
    if (!newTodo.trim()) return;

    try {
      const newTodoItem = await taskService.createTask({ title: newTodo, description: newTodo });
      setTodos([newTodoItem, ...todos]);
      setNewTodo('');
    } catch (err) {
      setError(err.message);
    }
  };

  const handleToggleTodo = async (todoId, currentStatus) => {
    try {
      const updatedTodo = await taskService.toggleTaskCompletion(todoId, !currentStatus);
      setTodos(todos.map(todo =>
        todo.id === todoId ? updatedTodo : todo
      ));
    } catch (err) {
      setError(err.message);
    }
  };

  const handleDeleteTodo = async (todoId) => {
    try {
      await taskService.deleteTask(todoId);
      setTodos(todos.filter(todo => todo.id !== todoId));
    } catch (err) {
      setError(err.message);
    }
  };

  const startEditingTodo = (todoId, currentTitle) => {
    setEditingTodoId(todoId);
    setEditingTodoTitle(currentTitle);
  };

  const finishEditingTodo = async (todoId) => {
    if (!editingTodoTitle.trim()) {
      // If title is empty, cancel editing
      setEditingTodoId(null);
      return;
    }

    try {
      const updatedTodo = await taskService.updateTask(todoId, { title: editingTodoTitle });
      setTodos(todos.map(todo =>
        todo.id === todoId ? updatedTodo : todo
      ));
      setEditingTodoId(null);
    } catch (err) {
      setError(err.message);
    }
  };

  const cancelEditingTodo = () => {
    setEditingTodoId(null);
  };

  if (loading) {
    return (
      <div className="max-w-4xl mx-auto p-6">
        <h1 className="text-2xl font-bold mb-6">Loading your tasks...</h1>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-6">Todo Dashboard</h1>

      {error && (
        <div className="mb-4 p-3 bg-red-100 text-red-700 rounded-md">
          {error}
        </div>
      )}

      {/* Add new todo form */}
      <form onSubmit={handleAddTodo} className="mb-8">
        <div className="flex gap-2">
          <input
            type="text"
            value={newTodo}
            onChange={(e) => setNewTodo(e.target.value)}
            placeholder="Add a new task..."
            className="flex-grow px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            type="submit"
            className="bg-blue-600 text-white px-6 py-2 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
          >
            Add
          </button>
        </div>
      </form>

      {/* Todo list */}
      <div className="bg-white rounded-lg shadow-md overflow-hidden">
        <h2 className="text-lg font-semibold p-4 border-b">Your Tasks</h2>

        {todos.length === 0 ? (
          <div className="p-8 text-center text-gray-500">
            <p>No tasks yet. Add a new task to get started!</p>
          </div>
        ) : (
          <ul className="divide-y divide-gray-200">
            {todos.map((todo) => (
              <li key={todo.id} className="p-4 flex items-center justify-between">
                <div className="flex items-center">
                  <input
                    type="checkbox"
                    checked={todo.is_completed}
                    onChange={() => handleToggleTodo(todo.id, todo.is_completed)}
                    className="h-5 w-5 text-blue-600 rounded focus:ring-blue-500"
                  />
                  {editingTodoId === todo.id ? (
                    <div className="flex items-center ml-3">
                      <input
                        type="text"
                        value={editingTodoTitle}
                        onChange={(e) => setEditingTodoTitle(e.target.value)}
                        className="px-2 py-1 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
                        autoFocus
                        onKeyDown={(e) => {
                          if (e.key === 'Enter') {
                            finishEditingTodo(todo.id);
                          } else if (e.key === 'Escape') {
                            cancelEditingTodo();
                          }
                        }}
                      />
                      <button
                        onClick={() => finishEditingTodo(todo.id)}
                        className="ml-2 bg-green-600 text-white px-2 py-1 rounded text-sm hover:bg-green-700"
                      >
                        Save
                      </button>
                      <button
                        onClick={cancelEditingTodo}
                        className="ml-1 bg-gray-600 text-white px-2 py-1 rounded text-sm hover:bg-gray-700"
                      >
                        Cancel
                      </button>
                    </div>
                  ) : (
                    <div className="flex items-center">
                      <span
                        className={`ml-3 ${todo.is_completed ? 'line-through text-gray-500' : 'text-gray-800'}`}
                        onDoubleClick={() => startEditingTodo(todo.id, todo.title)}
                      >
                        {todo.title}
                      </span>
                      <button
                        onClick={() => startEditingTodo(todo.id, todo.title)}
                        className="ml-4 text-blue-600 hover:text-blue-800 text-sm"
                      >
                        Edit
                      </button>
                    </div>
                  )}
                </div>
                <button
                  onClick={() => handleDeleteTodo(todo.id)}
                  className="text-red-600 hover:text-red-800 focus:outline-none"
                >
                  Delete
                </button>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
};

export default TodoDashboard;