import React from 'react';

const TaskToggle = ({ taskId, isCompleted, onToggle }) => {
  const handleToggle = () => {
    onToggle(taskId, !isCompleted);
  };

  return (
    <div className="task-toggle">
      <input
        type="checkbox"
        id={`task-${taskId}`}
        checked={isCompleted}
        onChange={handleToggle}
      />
      <label htmlFor={`task-${taskId}`} className="toggle-label">
        {isCompleted ? 'Completed' : 'Mark as complete'}
      </label>
    </div>
  );
};

export default TaskToggle;