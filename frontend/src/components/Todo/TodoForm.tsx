import React, { useState } from "react";
import Input from "../UI/Input";
import Button from "../UI/Button";

interface TodoFormProps {
  onAdd: (todoData: { title: string; description?: string }) => void;
  loading?: boolean;
}

const TodoForm: React.FC<TodoFormProps> = ({ onAdd, loading = false }) => {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (title.trim()) {
      onAdd({ title: title.trim(), description: description.trim() || undefined });
      setTitle("");
      setDescription("");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="mb-6">
      <div className="flex flex-col gap-3">
        <Input
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Enter a new task..."
          className="w-full"
          disabled={loading}
        />
        <Input
          type="text"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Add a description (optional)..."
          className="w-full"
          disabled={loading}
        />
        <Button type="submit" disabled={loading || !title.trim()}>
          {loading ? "Adding..." : "Add Task"}
        </Button>
      </div>
    </form>
  );
};

export default TodoForm;