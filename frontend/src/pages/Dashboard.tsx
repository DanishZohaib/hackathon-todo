import React from "react";
import { useTodoContext } from "../context/TodoContext";
import DashboardLayout from "../components/Layout/DashboardLayout";
import TodoForm from "../components/Todo/TodoForm";
import TodoList from "../components/Todo/TodoList";
import Chatbot from "../components/Todo/Chatbot";
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
  } = useTodoContext();

  return (
    <DashboardLayout title="Todo Dashboard">
      {error && (
        <div className="mb-4 p-3 bg-[var(--error-red)] bg-opacity-100 text-white rounded-md border border-[var(--error-red)]">
          {error}
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <Card className="p-6 glass-effect">
            <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-6">
              <div>
                <h2 className="text-2xl font-bold gradient-text">Manage Your Tasks</h2>
                <p className="text-[var(--text-secondary)]">
                  {todos.length} {todos.length === 1 ? "task" : "tasks"} total
                </p>
              </div>

              {todos.some(todo => todo.completed) && (
                <Button
                  variant="outline"
                  onClick={deleteCompletedTodos}
                  className="self-start bg-gradient-to-r from-[var(--neon-purple)] to-[var(--neon-cyan)] text-white hover:from-[var(--neon-cyan)] hover:to-[var(--neon-purple)]"
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
                <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-[var(--neon-cyan)] glow-cyan"></div>
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
        </div>

        <div>
          <Card className="p-6 glass-effect h-full">
            <h2 className="text-xl font-bold gradient-text mb-4">AI Assistant</h2>
            <Chatbot />
          </Card>
        </div>
      </div>
    </DashboardLayout>
  );
};

export default Dashboard;