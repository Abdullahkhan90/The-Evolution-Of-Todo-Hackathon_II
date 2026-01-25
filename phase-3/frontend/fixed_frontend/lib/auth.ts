// Mock authentication service for the Todo App
// This would normally connect to your backend authentication system

class AuthService {
  private readonly TOKEN_KEY = 'todo_app_token';
  private readonly USER_ID_KEY = 'todo_user_id';

  isAuthenticated(): boolean {
    // Check if token exists in localStorage
    const token = localStorage.getItem(this.TOKEN_KEY);
    return !!token;
  }

  getCurrentUserId(): string | null {
    // Retrieve user ID from localStorage
    return localStorage.getItem(this.USER_ID_KEY);
  }

  async login(email: string, password: string): Promise<{ success: boolean; userId?: string; error?: string }> {
    try {
      // In a real app, this would be an API call to your backend
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();

      if (response.ok) {
        // Store token and user ID in localStorage
        localStorage.setItem(this.TOKEN_KEY, data.token);
        localStorage.setItem(this.USER_ID_KEY, data.userId);
        return { success: true, userId: data.userId };
      } else {
        return { success: false, error: data.message || 'Login failed' };
      }
    } catch (error) {
      console.error('Login error:', error);
      return { success: false, error: 'Network error occurred' };
    }
  }

  async signup(email: string, password: string, name: string): Promise<{ success: boolean; userId?: string; error?: string }> {
    try {
      // In a real app, this would be an API call to your backend
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password, name }),
      });

      const data = await response.json();

      if (response.ok) {
        // Store token and user ID in localStorage
        localStorage.setItem(this.TOKEN_KEY, data.token);
        localStorage.setItem(this.USER_ID_KEY, data.userId);
        return { success: true, userId: data.userId };
      } else {
        return { success: false, error: data.message || 'Signup failed' };
      }
    } catch (error) {
      console.error('Signup error:', error);
      return { success: false, error: 'Network error occurred' };
    }
  }

  // Alias for register method to match what the signup page expects
  async register(email: string, password: string, name: string = "New User"): Promise<{ success: boolean; userId?: string; error?: string }> {
    return await this.signup(email, password, name);
  }

  async logout(): Promise<void> {
    // Remove token and user ID from localStorage
    localStorage.removeItem(this.TOKEN_KEY);
    localStorage.removeItem(this.USER_ID_KEY);
  }

  getToken(): string | null {
    return localStorage.getItem(this.TOKEN_KEY);
  }
}

export const authService = new AuthService();