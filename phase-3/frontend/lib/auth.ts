import { apiClient } from '@/lib/api';

class AuthService {
  private user: any = null;

  async login(email: string, password: string) {
    try {
      const resp = await apiClient.login(email, password);
      // Optionally populate a simple user object from token
      const userId = apiClient.getCurrentUserId();
      if (userId) this.user = { id: userId, email };
      return { user: this.user, data: resp };
    } catch (e: any) {
      console.error('Login error:', e);
      return { user: null, error: e?.message || 'Login failed' };
    }
  }

  async register(email: string, password: string, name?: string) {
    try {
      const resp = await apiClient.register(email, password, name);
      // after register, try to login/derive user
      const userId = apiClient.getCurrentUserId();
      if (userId) this.user = { id: userId, email };
      return { user: this.user, data: resp };
    } catch (e: any) {
      console.error('Registration error:', e);
      return { user: null, error: e?.message || 'Registration failed' };
    }
  }

  // alias used across the codebase
  async signup(email: string, password: string, name?: string) {
    return this.register(email, password, name);
  }

  async logout() {
    await apiClient.logout();
    this.user = null;
  }

  getCurrentUser() {
    if (!this.user) {
      const id = apiClient.getCurrentUserId();
      if (id) this.user = { id, email: 'unknown@example.com' };
    }
    return this.user;
  }

  getCurrentUserId(): string | null {
    return apiClient.getCurrentUserId();
  }

  isAuthenticated(): boolean {
    return apiClient.isAuthenticated();
  }
}

export const authService = new AuthService();
export default authService;