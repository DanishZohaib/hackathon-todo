export interface Todo {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  dueDate?: string | null;
  priority?: string;
  createdAt: string;
  updatedAt: string;
  userId: string;
}

// Interface for creating a new todo
export interface CreateTodoDto {
  title: string;
  description?: string;
}

// Interface for updating a todo
export interface UpdateTodoDto {
  title?: string;
  description?: string;
  completed?: boolean;
}

// Interface for the response from API when getting todos
export interface TodoApiResponse {
  todos: Todo[];
  count: number;
}