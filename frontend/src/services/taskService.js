import api from './api';

export const taskService = {
  // Get all tasks for the current user
  async getTasks() {
    try {
      const response = await api.get('/tasks');
      // The backend returns a TaskListResponse object with a tasks property
      return response.data.tasks || response.data;
    } catch (error) {
      console.error('Error fetching tasks:', error);
      throw error;
    }
  },

  // Create a new task
  async createTask(taskData) {
    try {
      const response = await api.post('/tasks', taskData);
      return response.data;
    } catch (error) {
      console.error('Error creating task:', error);
      throw error;
    }
  },

  // Update a task
  async updateTask(taskId, taskData) {
    try {
      const response = await api.put(`/tasks/${taskId}`, taskData);
      return response.data;
    } catch (error) {
      console.error('Error updating task:', error);
      throw error;
    }
  },

  // Toggle task completion status
  async toggleTaskCompletion(taskId, isCompleted) {
    try {
      const response = await api.patch(`/tasks/${taskId}/complete?is_completed=${isCompleted}`);
      return response.data;
    } catch (error) {
      console.error('Error toggling task completion:', error);
      throw error;
    }
  },

  // Delete a task
  async deleteTask(taskId) {
    try {
      const response = await api.delete(`/tasks/${taskId}`);
      return response.data;
    } catch (error) {
      console.error('Error deleting task:', error);
      throw error;
    }
  }
};