import React, { useState } from "react";
import Input from "../UI/Input";
import Button from "../UI/Button";

interface TodoFormProps {
  onAdd: (title: string) => void;
  loading?: boolean;
}

const TodoForm: React.FC<TodoFormProps> = ({ onAdd, loading = false }) => {
  const [title, setTitle] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (title.trim()) {
      onAdd(title.trim());
      setTitle("");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="mb-6">
      <div className="flex gap-3">
        <Input
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Enter a new task..."
          className="flex-1"
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