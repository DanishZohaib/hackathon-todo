import { Todo, CreateTodoDto, UpdateTodoDto } from "../types/Todo";
import { secureApiRequest } from "./secureApiService";

// Get all todos for the authenticated user
export const getTodos = async (): Promise<Todo[]> => {
  console.log("Attempting to fetch todos from backend...");
  try {
    const response = await secureApiRequest.get<{tasks: any[], total_count: number, limit: number, offset: number}>("/todos/");
    console.log("Received response from backend:", response.data);
    
    // Transform backend response to match frontend Todo interface
    const todos = response.data.tasks.map((task: any) => ({
      id: task.id,
      title: task.title,
      description: task.description,
      completed: task.is_completed, // Map backend field to frontend field
      dueDate: task.due_date,      // Map backend field to frontend field
      priority: task.priority,     // Map backend field to frontend field
      createdAt: task.created_at,   // Map backend field to frontend field
      updatedAt: task.updated_at,   // Map backend field to frontend field
      userId: task.user_id          // Map backend field to frontend field
    }));
    
    console.log(`Fetched ${todos.length} todos from backend`);
    return todos;
  } catch (error: any) {
    console.error("Error fetching todos:", error);

    // Handle different types of errors
    if (error.response) {
      // Server responded with error status
      const errorMessage = error.response.data?.detail || error.response.statusText || "Failed to fetch todos";
      throw new Error(errorMessage);
    } else if (error.request) {
      // Request was made but no response received
      throw new Error("Network error: Unable to connect to server");
    } else {
      // Something else happened
      throw new Error("An unexpected error occurred while fetching todos");
    }
  }
};

// Get a specific todo by ID
export const getTodoById = async (id: string): Promise<Todo> => {
  try {
    const response = await secureApiRequest.get<any>(`/todos/${id}`);
    const task: any = response.data;
    return {
      id: task.id,
      title: task.title,
      description: task.description,
      completed: task.is_completed, // Map backend field to frontend field
      dueDate: task.due_date,      // Map backend field to frontend field
      priority: task.priority,     // Map backend field to frontend field
      createdAt: task.created_at,   // Map backend field to frontend field
      updatedAt: task.updated_at,   // Map backend field to frontend field
      userId: task.user_id          // Map backend field to frontend field
    };
  } catch (error: any) {
    console.error(`Error fetching todo with ID ${id}:`, error);

    // Handle different types of errors
    if (error.response) {
      // Server responded with error status
      const errorMessage = error.response.data?.detail || error.response.statusText || `Failed to fetch todo with ID ${id}`;
      throw new Error(errorMessage);
    } else if (error.request) {
      // Request was made but no response received
      throw new Error("Network error: Unable to connect to server");
    } else {
      // Something else happened
      throw new Error(`An unexpected error occurred while fetching todo with ID ${id}`);
    }
  }
};

// Create a new todo
export const createTodo = async (todoData: CreateTodoDto): Promise<Todo> => {
  try {
    const response = await secureApiRequest.post<any>("/todos/", todoData);
    const task: any = response.data;
    return {
      id: task.id,
      title: task.title,
      description: task.description,
      completed: task.is_completed, // Map backend field to frontend field
      createdAt: task.created_at,   // Map backend field to frontend field
      updatedAt: task.updated_at,   // Map backend field to frontend field
      userId: task.user_id          // Map backend field to frontend field
    };
  } catch (error: any) {
    console.error("Error creating todo:", error);

    // Handle different types of errors
    if (error.response) {
      // Server responded with error status
      const errorMessage = error.response.data?.detail || error.response.statusText || "Failed to create todo";
      throw new Error(errorMessage);
    } else if (error.request) {
      // Request was made but no response received
      throw new Error("Network error: Unable to connect to server");
    } else {
      // Something else happened
      throw new Error("An unexpected error occurred while creating todo");
    }
  }
};

// Update a todo
export const updateTodo = async (id: string, todoData: UpdateTodoDto): Promise<Todo> => {
  try {
    const response = await secureApiRequest.put<any>(`/todos/${id}`, todoData);
    const task: any = response.data;
    return {
      id: task.id,
      title: task.title,
      description: task.description,
      completed: task.is_completed, // Map backend field to frontend field
      createdAt: task.created_at,   // Map backend field to frontend field
      updatedAt: task.updated_at,   // Map backend field to frontend field
      userId: task.user_id          // Map backend field to frontend field
    };
  } catch (error: any) {
    console.error(`Error updating todo with ID ${id}:`, error);

    // Handle different types of errors
    if (error.response) {
      // Server responded with error status
      const errorMessage = error.response.data?.detail || error.response.statusText || `Failed to update todo with ID ${id}`;
      throw new Error(errorMessage);
    } else if (error.request) {
      // Request was made but no response received
      throw new Error("Network error: Unable to connect to server");
    } else {
      // Something else happened
      throw new Error(`An unexpected error occurred while updating todo with ID ${id}`);
    }
  }
};

// Delete a todo
export const deleteTodo = async (id: string): Promise<void> => {
  try {
    await secureApiRequest.delete(`/todos/${id}`);
  } catch (error: any) {
    console.error(`Error deleting todo with ID ${id}:`, error);

    // Handle different types of errors
    if (error.response) {
      // Server responded with error status
      const errorMessage = error.response.data?.detail || error.response.statusText || `Failed to delete todo with ID ${id}`;
      throw new Error(errorMessage);
    } else if (error.request) {
      // Request was made but no response received
      throw new Error("Network error: Unable to connect to server");
    } else {
      // Something else happened
      throw new Error(`An unexpected error occurred while deleting todo with ID ${id}`);
    }
  }
};

// Toggle todo completion status
export const toggleTodoCompletion = async (id: string): Promise<Todo> => {
  try {
    const response = await secureApiRequest.patch<any>(`/todos/${id}/toggle`);
    const task: any = response.data;
    return {
      id: task.id,
      title: task.title,
      description: task.description,
      completed: task.is_completed, // Map backend field to frontend field
      createdAt: task.created_at,   // Map backend field to frontend field
      updatedAt: task.updated_at,   // Map backend field to frontend field
      userId: task.user_id          // Map backend field to frontend field
    };
  } catch (error: any) {
    console.error(`Error toggling todo completion with ID ${id}:`, error);

    // Handle different types of errors
    if (error.response) {
      // Server responded with error status
      const errorMessage = error.response.data?.detail || error.response.statusText || `Failed to toggle todo completion with ID ${id}`;
      throw new Error(errorMessage);
    } else if (error.request) {
      // Request was made but no response received
      throw new Error("Network error: Unable to connect to server");
    } else {
      // Something else happened
      throw new Error(`An unexpected error occurred while toggling todo completion with ID ${id}`);
    }
  }
};

// Bulk delete completed todos
export const deleteCompletedTodos = async (): Promise<void> => {
  try {
    await secureApiRequest.delete("/todos/");
  } catch (error: any) {
    console.error("Error deleting completed todos:", error);

    // Handle different types of errors
    if (error.response) {
      // Server responded with error status
      const errorMessage = error.response.data?.detail || error.response.statusText || "Failed to delete completed todos";
      throw new Error(errorMessage);
    } else if (error.request) {
      // Request was made but no response received
      throw new Error("Network error: Unable to connect to server");
    } else {
      // Something else happened
      throw new Error("An unexpected error occurred while deleting completed todos");
    }
  }
};
