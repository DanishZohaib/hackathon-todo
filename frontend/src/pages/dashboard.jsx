import React, { useState, useEffect } from 'react';
import { taskService } from '../services/taskService';
import TaskList from '../components/tasks/task-list';
import TaskForm from '../components/tasks/task-form';
import { authService } from '../services/authService';

const Dashboard = () => {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      const response = await taskService.getTasks();
      setTasks(response.data.tasks);
    } catch (err) {
      setError('Failed to load tasks');
    } finally {
      setLoading(false);
    }
  };

  const handleTaskCreated = (newTask) => {
    setTasks([newTask, ...tasks]);
  };

  const handleTaskUpdated = (updatedTask) => {
    setTasks(tasks.map(task =>
      task.id === updatedTask.id ? updatedTask : task
    ));
  };

  const handleTaskDeleted = (taskId) => {
    setTasks(tasks.filter(task => task.id !== taskId));
  };

  const handleLogout = () => {
    authService.logout();
    window.location.href = '/signin';
  };

  if (loading) {
    return <div>Loading tasks...</div>;
  }

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1>Todo Dashboard</h1>
        <button onClick={handleLogout} className="logout-btn">Logout</button>
      </header>

      {error && <div className="error-message">{error}</div>}

      <div className="dashboard-content">
        <div className="task-form-section">
          <TaskForm onTaskCreated={handleTaskCreated} />
        </div>

        <div className="task-list-section">
          <TaskList
            tasks={tasks}
            onTaskUpdated={handleTaskUpdated}
            onTaskDeleted={handleTaskDeleted}
          />
        </div>
      </div>
    </div>
  );
};

export default Dashboard;