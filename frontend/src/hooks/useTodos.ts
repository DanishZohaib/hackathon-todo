import { useState, useEffect } from "react";
import { Todo } from "../types/Todo";
import {
  getTodos,
  createTodo,
  updateTodo,
  deleteTodo,
  toggleTodoCompletion,
  deleteCompletedTodos,
} from "../services/todoService";

interface UseTodosReturn {
  todos: Todo[];
  loading: boolean;
  error: string | null;
  addTodo: (todoData: { title: string; description?: string }) => Promise<void>;
  toggleTodo: (id: string) => Promise<void>;
  deleteTodo: (id: string) => Promise<void>;
  updateTodo: (id: string, title: string, description?: string) => Promise<void>;
  deleteCompletedTodos: () => Promise<void>;
  refreshTodos: () => Promise<void>;
}

export const useTodos = (): UseTodosReturn => {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // Load todos on mount
  useEffect(() => {
    loadTodos();
  }, []);

  const loadTodos = async () => {
    try {
      setLoading(true);
      setError(null);
      const todosData = await getTodos();
      setTodos(todosData);
    } catch (err: any) {
      setError(err.message || "Failed to load todos. Please try again later.");
      console.error("Error loading todos:", err);
    } finally {
      setLoading(false);
    }
  };

  const addTodo = async (todoData: { title: string; description?: string }) => {
    try {
      setError(null);
      const newTodo = await createTodo(todoData);
      setTodos(prev => [newTodo, ...prev]);
    } catch (err: any) {
      setError(err.message || "Failed to add todo. Please try again.");
      console.error("Error adding todo:", err);
    }
  };

  const toggleTodo = async (id: string) => {
    try {
      setError(null);
      const updatedTodo = await toggleTodoCompletion(id);
      setTodos(prev =>
        prev.map(todo => (todo.id === id ? updatedTodo : todo)),
      );
    } catch (err: any) {
      setError(err.message || "Failed to update todo. Please try again.");
      console.error("Error toggling todo:", err);
    }
  };

  const deleteTodoById = async (id: string) => {
    try {
      setError(null);
      await deleteTodo(id);
      setTodos(prev => prev.filter(todo => todo.id !== id));
    } catch (err: any) {
      setError(err.message || "Failed to delete todo. Please try again.");
      console.error("Error deleting todo:", err);
    }
  };

  const updateTodoById = async (id: string, title: string, description?: string) => {
    try {
      setError(null);
      const updateData: { title?: string; description?: string } = { title };
      if (description !== undefined) {
        updateData.description = description;
      }
      const updatedTodo = await updateTodo(id, updateData);
      setTodos(prev =>
        prev.map(todo => (todo.id === id ? updatedTodo : todo)),
      );
    } catch (err: any) {
      setError(err.message || "Failed to update todo. Please try again.");
      console.error("Error updating todo:", err);
    }
  };

  const deleteCompletedTodosHandler = async () => {
    try {
      setError(null);
      await deleteCompletedTodos();
      setTodos(prev => prev.filter(todo => !todo.completed));
    } catch (err: any) {
      setError(err.message || "Failed to delete completed todos. Please try again.");
      console.error("Error deleting completed todos:", err);
    }
  };

  const refreshTodos = async () => {
    await loadTodos();
  };

  return {
    todos,
    loading,
    error,
    addTodo,
    toggleTodo,
    deleteTodo: deleteTodoById,
    updateTodo: updateTodoById,
    deleteCompletedTodos: deleteCompletedTodosHandler,
    refreshTodos,
  };
};