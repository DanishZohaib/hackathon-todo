import React, { useState, useEffect } from "react";
import { Todo } from "../../types/Todo";
import Card from "../UI/Card";
import Button from "../UI/Button";

interface TodoCardProps {
  todo: Todo;
  onToggle: (id: string) => void;
  onDelete: (id: string) => void;
  onEdit?: (id: string, title: string, description?: string) => void;
}

const TodoCard: React.FC<TodoCardProps> = ({ todo, onToggle, onDelete, onEdit }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [editValue, setEditValue] = useState(todo.title);
  const [editDescription, setEditDescription] = useState(todo.description || "");
  const [isDeleting, setIsDeleting] = useState(false);
  const [isToggling, setIsToggling] = useState(false);

  useEffect(() => {
    if (isDeleting) {
      // After animation completes, trigger the actual delete
      const timer = setTimeout(() => {
        onDelete(todo.id);
      }, 300);
      return () => clearTimeout(timer);
    }
  }, [isDeleting, onDelete, todo.id]);

  useEffect(() => {
    if (isToggling) {
      // After animation completes, trigger the actual toggle
      const timer = setTimeout(() => {
        onToggle(todo.id);
        setIsToggling(false);
      }, 150);
      return () => clearTimeout(timer);
    }
  }, [isToggling, onToggle, todo.id]);

  const handleSave = () => {
    if (onEdit && editValue.trim()) {
      onEdit(todo.id, editValue, editDescription);
      setIsEditing(false);
    }
  };

  const handleCancel = () => {
    setEditValue(todo.title);
    setIsEditing(false);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter") {
      handleSave();
    } else if (e.key === "Escape") {
      handleCancel();
    }
  };

  if (isDeleting) {
    return (
      <div className={"p-4 mb-3 opacity-0 translate-y-[-10px] transition-all duration-300 ease-in-out"}>
        <div className="bg-[var(--bg-secondary)] border border-[var(--pak-green-primary)]/30 rounded-lg p-4">
          Deleting...
        </div>
      </div>
    );
  }

  return (
    <Card
      className={`p-4 mb-3 transition-all duration-300 ${
        isToggling
          ? "scale-95 opacity-75"
          : "scale-100 opacity-100"
      } ${
        todo.completed
          ? "glass-effect border border-[var(--neon-green)]/30"
          : "glass-effect border border-[var(--bg-glass-border)]"
      }`}
      elevation="medium"
    >
      <div className="flex items-start gap-3">
        <input
          type="checkbox"
          checked={todo.completed}
          onChange={() => setIsToggling(true)}
          className="mt-1 h-5 w-5 rounded border-[var(--border-color)] text-[var(--neon-cyan)] focus:ring-[var(--neon-cyan)] cursor-pointer bg-[var(--bg-tertiary)]"
        />

        <div className="flex-1">
          {isEditing ? (
            <div className="flex flex-col gap-2">
              <input
                type="text"
                value={editValue}
                onChange={(e) => setEditValue(e.target.value)}
                onKeyDown={handleKeyDown}
                autoFocus
                className="w-full px-3 py-2 bg-[var(--bg-tertiary)] text-[var(--text-primary)] border border-[var(--neon-cyan)] rounded-md focus:outline-none focus:ring-2 focus:ring-[var(--neon-cyan)]"
              />
              <input
                type="text"
                value={editDescription}
                onChange={(e) => setEditDescription(e.target.value)}
                className="w-full px-3 py-2 bg-[var(--bg-tertiary)] text-[var(--text-primary)] border border-[var(--neon-cyan)] rounded-md focus:outline-none focus:ring-2 focus:ring-[var(--neon-cyan)]"
                placeholder="Description (optional)"
              />
              <div className="flex gap-2 mt-2">
                <Button size="sm" onClick={handleSave} className="bg-gradient-to-r from-[var(--neon-cyan)] to-[var(--neon-purple)] hover:from-[var(--neon-purple)] hover:to-[var(--neon-cyan)]">Save</Button>
                <Button variant="outline" size="sm" onClick={handleCancel}>Cancel</Button>
              </div>
            </div>
          ) : (
            <div className="flex flex-col">
              <div className="flex items-center gap-2 mb-1">
                <span
                  className={`text-[var(--text-primary)] ${
                    todo.completed
                      ? "line-through text-[var(--text-tertiary)]"
                      : "text-[var(--text-primary)]"
                  }`}
                >
                  {todo.title}
                </span>
                <span
                  className={`px-2 py-0.5 rounded-full text-xs font-medium ${
                    todo.completed
                      ? "bg-[var(--neon-green)] text-[var(--bg-primary)]"
                      : "bg-[var(--neon-blue)]/20 text-[var(--neon-blue)] border border-[var(--neon-blue)]/30"
                  }`}
                >
                  {todo.completed ? "Completed" : "Pending"}
                </span>
              </div>
              {todo.description && (
                <div className="text-sm text-[var(--text-secondary)] mb-1 italic">
                  {todo.description}
                </div>
              )}
              <div className="text-xs text-[var(--text-tertiary)]">
                Created: {new Date(todo.createdAt).toLocaleDateString()}
              </div>
            </div>
          )}
        </div>

        <div className="flex gap-2">
          {!isEditing && (
            <button
              type="button"
              onClick={() => setIsEditing(true)}
              className="p-2 rounded-full hover:bg-[var(--neon-cyan)]/20 transition-colors border border-transparent hover:border-[var(--neon-cyan)]/30"
              aria-label="Edit todo"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 text-[var(--neon-cyan)]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
              </svg>
            </button>
          )}
          <button
            type="button"
            onClick={() => setIsDeleting(true)}
            className="p-2 rounded-full hover:bg-[var(--error)]/20 transition-colors border border-transparent hover:border-[var(--error)]/30"
            aria-label="Delete todo"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 text-[var(--error)]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
          </button>
        </div>
      </div>
    </Card>
  );
};

export default TodoCard;