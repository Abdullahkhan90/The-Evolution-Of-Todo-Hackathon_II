import axios, { AxiosInstance } from 'axios';

import { Task } from '@/types/task';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL;
// No fallback – production mein env miss hone pe crash hone do taaki pata chale
if (!API_BASE_URL) {
  console.error('NEXT_PUBLIC_API_URL is not set in environment variables!');
}

class ApiClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({ baseURL: API_BASE_URL, headers: { 'Content-Type': 'application/json' } });

    this.client.interceptors.request.use((config) => {
      try {
        if (typeof window !== 'undefined') {
          const token = this.getStoredToken();
          if (token && config.headers) {
            config.headers.Authorization = `Bearer ${token}`;
          }
        }
      } catch (e) {
        // ignore in SSR
      }
      return config;
    }, (error) => Promise.reject(error));

    this.client.interceptors.response.use((r) => r, (error) => {
      const status = error?.response?.status;
      if (status === 401) {
        try {
          if (typeof window !== 'undefined') {
            this.clearStoredToken();
            window.location.href = '/login';
          }
        } catch (e) {
          // ignore
        }
      }
      return Promise.reject(error);
    });
  }

  private getStoredToken(): string | null {
    if (typeof window === 'undefined') return null;
    const keys = ['token', 'todo_app_token', 'jwt_token', 'access_token'];
    for (const k of keys) {
      const t = localStorage.getItem(k);
      if (t) return t;
    }
    return null;
  }

  private clearStoredToken() {
    if (typeof window === 'undefined') return;
    const keys = ['token', 'todo_app_token', 'jwt_token', 'access_token'];
    for (const k of keys) localStorage.removeItem(k);
  }

  // Authentication helpers (used by some callers)
  async login(email: string, password: string) {
    const res = await this.client.post('/auth/login', { email, password });
    const token = res?.data?.access_token; // Backend returns access_token, not token
    if (typeof window !== 'undefined' && token) {
      localStorage.setItem('token', token);
    }
    return res.data;
  }

  async register(email: string, password: string, name?: string) {
    const res = await this.client.post('/auth/signup', { email, password, name });
    const token = res?.data?.access_token; // Backend returns access_token, not token
    if (typeof window !== 'undefined' && token) {
      localStorage.setItem('token', token);
    }
    return res.data;
  }

  async logout() {
    try {
      this.clearStoredToken();
    } catch (e) {
      // ignore
    }
  }

  getCurrentUserId(): string | null {
    try {
      const token = this.getStoredToken();
      if (!token) return null;
      const parts = token.split('.');
      if (parts.length !== 3) return null;
      const payload = JSON.parse(typeof atob === 'function' ? atob(parts[1]) : Buffer.from(parts[1], 'base64').toString('utf8'));
      return payload?.sub || payload?.user_id || null;
    } catch (e) {
      return null;
    }
  }

  isAuthenticated(): boolean {
    return !!this.getStoredToken();
  }

  // Task APIs
  async getTasks(userId: string): Promise<Task[]> {
    const res = await this.client.get(`/api/users/${userId}/tasks`);
    return res.data;
  }

  async createTask(userId: string, task: Omit<Task, 'id'>): Promise<Task> {
    const res = await this.client.post(`/api/users/${userId}/tasks`, task);
    return res.data;
  }

  async updateTask(userId: string, taskId: string, task: Partial<Task>): Promise<Task> {
    const res = await this.client.put(`/api/users/${userId}/tasks/${taskId}`, task);
    return res.data;
  }

  async deleteTask(userId: string, taskId: string): Promise<void> {
    await this.client.delete(`/api/users/${userId}/tasks/${taskId}`);
  }

  // Chat API
  async sendChatMessage(userId: string, message: string, conversationId: string | null) {
    const res = await this.client.post(`/api/${userId}/chat`, { message, conversation_id: conversationId });
    return res.data;
  }
}

export const apiClient = new ApiClient();
export default apiClient;
