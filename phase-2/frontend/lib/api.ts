import axios, { AxiosInstance, AxiosRequestConfig } from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

class ApiClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
    });

    // Request interceptor to add JWT token
    this.client.interceptors.request.use(
      (config) => {
        const token = this.getStoredToken();
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // Response interceptor to handle token expiration
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          // Clear token and redirect to login if unauthorized
          this.clearToken();
          if (typeof window !== 'undefined') {
            window.location.href = '/login';
          }
        }
        return Promise.reject(error);
      }
    );
  }

  // Helper methods for token management
  private getStoredToken(): string | null {
    if (typeof window !== 'undefined') {
      return localStorage.getItem('jwt_token');
    }
    return null;
  }

  private setToken(token: string): void {
    if (typeof window !== 'undefined') {
      localStorage.setItem('jwt_token', token);
    }
  }

  private clearToken(): void {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('jwt_token');
    }
  }

  // User authentication
  async login(email: string, password: string) {
    try {
      const response = await this.client.post('/api/users/login', {
        email,
        password,
      });

      // Store JWT token
      if (response.data.access_token) {
        this.setToken(response.data.access_token);
      }

      return response.data;
    } catch (error: any) {
      // Handle specific error responses
      if (error.response?.data?.detail) {
        throw new Error(error.response.data.detail);
      }
      throw new Error('Login failed. Please try again.');
    }
  }

  async register(email: string, password: string) {
    try {
      const response = await this.client.post('/api/users/register', {
        email,
        password,
      });

      // Store JWT token if registration also returns a token
      if (response.data.access_token) {
        this.setToken(response.data.access_token);
      }

      return response.data;
    } catch (error: any) {
      // Handle specific error responses
      if (error.response?.data?.detail) {
        throw new Error(error.response.data.detail);
      }
      throw new Error('Registration failed. Please try again.');
    }
  }

  async logout() {
    this.clearToken();
  }

  // Task operations
  async getTasks(userId: string, skip: number = 0, limit: number = 100) {
    const response = await this.client.get(`/api/${userId}/`);
    return response.data;
  }

  async getTask(userId: string, taskId: string) {
    const response = await this.client.get(`/api/${userId}/${taskId}`);
    return response.data;
  }

  async createTask(userId: string, taskData: any) {
    const response = await this.client.post(`/api/${userId}/`, taskData);
    return response.data;
  }

  async updateTask(userId: string, taskId: string, taskData: any) {
    const response = await this.client.put(`/api/${userId}/${taskId}`, taskData);
    return response.data;
  }

  async deleteTask(userId: string, taskId: string) {
    const response = await this.client.delete(`/api/${userId}/${taskId}`);
    return response.data;
  }

  // Check if user is authenticated
  isAuthenticated() {
    const token = this.getStoredToken();
    return !!token;
  }

  // Get current user ID from token (decode JWT)
  getCurrentUserId(): string | null {
    const token = this.getStoredToken();
    if (!token) return null;

    try {
      // Split the token to get the payload part (second part)
      const parts = token.split('.');
      if (parts.length !== 3) {
        console.error('Invalid JWT token format');
        return null;
      }

      // Decode the payload part
      const payload = JSON.parse(atob(parts[1]));
      return payload.sub; // subject field contains user ID
    } catch (error) {
      console.error('Error decoding JWT token:', error);
      return null;
    }
  }
}

export const apiClient = new ApiClient();