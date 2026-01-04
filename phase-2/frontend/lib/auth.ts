import { apiClient } from './api';

interface User {
  id: string;
  email: string;
  created_at: string;
}

class AuthService {
  private user: User | null = null;

  async login(email: string, password: string): Promise<{ user: User | null; error?: string }> {
    try {
      const response = await apiClient.login(email, password);

      // Get user info after login
      const userId = apiClient.getCurrentUserId();
      if (userId) {
        // For now, we'll just return the ID since the login response doesn't include user details
        this.user = {
          id: userId,
          email,
          created_at: new Date().toISOString()
        };
      }

      return { user: this.user };
    } catch (error: any) {
      console.error('Login error:', error);
      return {
        user: null,
        error: error.message || 'Login failed'
      };
    }
  }

  async register(email: string, password: string): Promise<{ user: User | null; error?: string }> {
    try {
      const response = await apiClient.register(email, password);

      // After registration, try to login automatically
      return await this.login(email, password);
    } catch (error: any) {
      console.error('Registration error:', error);
      return {
        user: null,
        error: error.message || 'Registration failed'
      };
    }
  }

  async logout(): Promise<void> {
    await apiClient.logout();
    this.user = null;
  }

  getCurrentUser(): User | null {
    if (!this.user && apiClient.getCurrentUserId()) {
      // Try to get user from token if not stored
      const userId = apiClient.getCurrentUserId();
      if (userId) {
        this.user = {
          id: userId,
          email: 'unknown@example.com', // We don't have email without an additional API call
          created_at: new Date().toISOString()
        };
      }
    }
    return this.user;
  }

  isAuthenticated(): boolean {
    return apiClient.isAuthenticated();
  }

  getCurrentUserId(): string | null {
    return apiClient.getCurrentUserId();
  }
}

export const authService = new AuthService();