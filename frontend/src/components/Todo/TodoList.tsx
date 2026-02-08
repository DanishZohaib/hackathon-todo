import React from "react";
import { Todo } from "../../types/Todo";
import TodoCard from "./TodoCard";

interface TodoListProps {
  todos: Todo[];
  onToggle: (id: string) => void;
  onDelete: (id: string) => void;
  onEdit?: (id: string, title: string, description?: string) => void;
}

const TodoList: React.FC<TodoListProps> = ({ todos, onToggle, onDelete, onEdit }) => {
  // Separate completed and pending todos
  const completedTodos = todos.filter(todo => todo.completed);
  const pendingTodos = todos.filter(todo => !todo.completed);

  return (
    <div className="w-full">
      {pendingTodos.length > 0 && (
        <div className="mb-6">
          <h2 className="text-xl font-semibold mb-4 text-[var(--text-primary)]">Pending Tasks</h2>
          <div className="space-y-3">
            {pendingTodos.map(todo => (
              <TodoCard
                key={todo.id}
                todo={todo}
                onToggle={onToggle}
                onDelete={onDelete}
                onEdit={onEdit}
              />
            ))}
          </div>
        </div>
      )}

      {completedTodos.length > 0 && (
        <div>
          <h2 className="text-xl font-semibold mb-4 text-[var(--text-primary)]">Completed Tasks</h2>
          <div className="space-y-3">
            {completedTodos.map(todo => (
              <TodoCard
                key={todo.id}
                todo={todo}
                onToggle={onToggle}
                onDelete={onDelete}
                onEdit={onEdit}
              />
            ))}
          </div>
        </div>
      )}

      {todos.length === 0 && (
        <div className="text-center py-12">
          <p className="text-[var(--text-secondary)]">No tasks yet. Add your first task to get started!</p>
        </div>
      )}
    </div>
  );
};

export default TodoList;