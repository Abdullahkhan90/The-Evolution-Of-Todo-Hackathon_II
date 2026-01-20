import axios from 'axios'

const baseURL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export const apiClient = axios.create({
  baseURL,
  headers: {
    'Content-Type': 'application/json',
  },
})

apiClient.interceptors.request.use(
  (config) => {
    try {
      if (typeof window !== 'undefined') {
        const token = localStorage.getItem('token')
        if (token && config.headers) {
          config.headers.Authorization = `Bearer ${token}`
        }
      }
    } catch (e) {
      // ignore in SSR
    }
    return config
  },
  (error) => Promise.reject(error)
)

export default apiClient
// API client for the Todo App
// This connects to your backend API

import { Task } from '@/types/task';

class ApiClient {
  private getAuthHeaders(): HeadersInit {
    const token = localStorage.getItem('todo_app_token');
    return {
      'Content-Type': 'application/json',
      ...(token && { Authorization: `Bearer ${token}` })
    };
  }

  async getTasks(userId: string): Promise<Task[]> {
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/users/${userId}/tasks`,
        { headers: this.getAuthHeaders() }
      );

      if (!response.ok) {
        throw new Error(`Failed to fetch tasks: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error fetching tasks:', error);
      throw error;
    }
  }

  async createTask(userId: string, task: Omit<Task, 'id'>): Promise<Task> {
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/users/${userId}/tasks`,
        {
          method: 'POST',
          headers: this.getAuthHeaders(),
          body: JSON.stringify(task),
        }
      );

      if (!response.ok) {
        throw new Error(`Failed to create task: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error creating task:', error);
      throw error;
    }
  }

  async updateTask(userId: string, taskId: string, task: Partial<Task>): Promise<Task> {
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/users/${userId}/tasks/${taskId}`,
        {
          method: 'PUT',
          headers: this.getAuthHeaders(),
          body: JSON.stringify(task),
        }
      );

      if (!response.ok) {
        throw new Error(`Failed to update task: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error updating task:', error);
      throw error;
    }
  }

  async deleteTask(userId: string, taskId: string): Promise<void> {
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/users/${userId}/tasks/${taskId}`,
        {
          method: 'DELETE',
          headers: this.getAuthHeaders(),
        }
      );

      if (!response.ok) {
        throw new Error(`Failed to delete task: ${response.status}`);
      }
    } catch (error) {
      console.error('Error deleting task:', error);
      throw error;
    }
  }

  async sendChatMessage(userId: string, message: string, conversationId: string | null): Promise<any> {
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/${userId}/chat`,
        {
          method: 'POST',
          headers: this.getAuthHeaders(),
          body: JSON.stringify({
            message,
            conversation_id: conversationId
          }),
        }
      );

      if (!response.ok) {
        throw new Error(`Failed to send chat message: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error sending chat message:', error);
      throw error;
    }
  }
}

export const apiClient = new ApiClient();