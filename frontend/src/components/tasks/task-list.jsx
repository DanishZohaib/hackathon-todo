import React, { useState } from 'react';
import TaskToggle from './task-toggle';
import { taskService } from '../../services/api';

const TaskList = ({ tasks, onTaskUpdated, onTaskDeleted }) => {
  const [filter, setFilter] = useState('all'); // all, completed, pending

  const filteredTasks = tasks.filter(task => {
    if (filter === 'completed') return task.is_completed;
    if (filter === 'pending') return !task.is_completed;
    return true;
  });

  const handleDelete = async (taskId) => {
    try {
      await taskService.deleteTask(taskId);
      onTaskDeleted(taskId);
    } catch (err) {
      console.error('Failed to delete task:', err);
    }
  };

  const handleToggleComplete = async (taskId, isCompleted) => {
    try {
      const updatedTask = await taskService.updateTask(taskId, { is_completed: isCompleted });
      onTaskUpdated(updatedTask.data);
    } catch (err) {
      console.error('Failed to update task:', err);
    }
  };

  const handleUpdate = async (taskId, updates) => {
    try {
      const updatedTask = await taskService.updateTask(taskId, updates);
      onTaskUpdated(updatedTask.data);
    } catch (err) {
      console.error('Failed to update task:', err);
    }
  };

  return (
    <div className="task-list">
      <div className="task-list-header">
        <h2>My Tasks</h2>
        <div className="filter-controls">
          <button
            className={filter === 'all' ? 'active' : ''}
            onClick={() => setFilter('all')}
          >
            All
          </button>
          <button
            className={filter === 'pending' ? 'active' : ''}
            onClick={() => setFilter('pending')}
          >
            Pending
          </button>
          <button
            className={filter === 'completed' ? 'active' : ''}
            onClick={() => setFilter('completed')}
          >
            Completed
          </button>
        </div>
      </div>

      {filteredTasks.length === 0 ? (
        <div className="no-tasks">No tasks found</div>
      ) : (
        <ul className="task-items">
          {filteredTasks.map(task => (
            <li key={task.id} className={`task-item ${task.is_completed ? 'completed' : ''}`}>
              <div className="task-content">
                <TaskToggle
                  taskId={task.id}
                  isCompleted={task.is_completed}
                  onToggle={handleToggleComplete}
                />
                <div className="task-details">
                  <h3 className={task.is_completed ? 'completed' : ''}>{task.title}</h3>
                  {task.description && <p>{task.description}</p>}
                  <div className="task-meta">
                    {task.due_date && <span>Due: {new Date(task.due_date).toLocaleDateString()}</span>}
                    <span className={`priority priority-${task.priority}`}>{task.priority}</span>
                  </div>
                </div>
              </div>
              <div className="task-actions">
                <button
                  onClick={() => handleUpdate(task.id, { priority: task.priority === 'low' ? 'medium' : task.priority === 'medium' ? 'high' : 'low' })}
                  className="priority-btn"
                >
                  Change Priority
                </button>
                <button
                  onClick={() => handleDelete(task.id)}
                  className="delete-btn"
                >
                  Delete
                </button>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default TaskList;