import React from "react";
import { useTodos } from "../hooks/useTodos";
import DashboardLayout from "../components/Layout/DashboardLayout";
import TodoForm from "../components/Todo/TodoForm";
import TodoList from "../components/Todo/TodoList";
import Button from "../components/UI/Button";
import Card from "../components/UI/Card";

const Dashboard: React.FC = () => {
  const {
    todos,
    loading,
    error,
    addTodo,
    toggleTodo,
    deleteTodo,
    updateTodo,
    deleteCompletedTodos,
  } = useTodos();

  return (
    <DashboardLayout title="Todo Dashboard">
      {error && (
        <div className="mb-4 p-3 bg-[var(--error-red)] bg-opacity-100 text-white rounded-md border border-[var(--error-red)]">
          {error}
        </div>
      )}

      <Card className="p-6 bg-[var(--bg-secondary)]">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-6">
          <div>
            <h2 className="text-2xl font-bold text-[var(--text-primary)]">Manage Your Tasks</h2>
            <p className="text-[var(--text-secondary)]">
              {todos.length} {todos.length === 1 ? "task" : "tasks"} total
            </p>
          </div>

          {todos.some(todo => todo.completed) && (
            <Button
              variant="outline"
              onClick={deleteCompletedTodos}
              className="self-start"
            >
              Delete Completed
            </Button>
          )}
        </div>

        <TodoForm
          onAdd={addTodo}
          loading={loading}
        />

        {loading ? (
          <div className="flex justify-center items-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-[var(--pak-green-primary)]"></div>
          </div>
        ) : (
          <TodoList
            todos={todos}
            onToggle={toggleTodo}
            onDelete={deleteTodo}
            onEdit={updateTodo}
          />
        )}
      </Card>
    </DashboardLayout>
  );
};

export default Dashboard;