
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

import { apiClient } from '@/lib/api'

type Credentials = {
  email: string
  password: string
}

// Support two call styles: login({email,password}) and login(email,password)
async function login(arg1: any, arg2?: any) {
  let email: string
  let password: string
  if (typeof arg1 === 'string' && typeof arg2 === 'string') {
    email = arg1
    password = arg2
  } else {
    email = arg1?.email
    password = arg1?.password
  }
  const res = await apiClient.post('/auth/login', { email, password })
  const token = res?.data?.token
  if (typeof window !== 'undefined' && token) {
    localStorage.setItem('token', token)
  }
  return res.data
}

// Same flexibility for signup
async function signup(arg1: any, arg2?: any) {
  let email: string
  let password: string
  if (typeof arg1 === 'string' && typeof arg2 === 'string') {
    email = arg1
    password = arg2
  } else {
    email = arg1?.email
    password = arg1?.password
  }
  const res = await apiClient.post('/auth/signup', { email, password })
  const token = res?.data?.token
  if (typeof window !== 'undefined' && token) {
    localStorage.setItem('token', token)
  }
  return res.data
}

// alias used in some parts of the codebase
async function register(arg1: any, arg2?: any) {
  return signup(arg1, arg2)
}

function logout() {
  try {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('token')
    }
  } catch (e) {
    // ignore
  }
}

function getToken(): string | null {
  try {
    if (typeof window === 'undefined') return null
    return (
      localStorage.getItem('token') ||
      localStorage.getItem('todo_app_token') ||
      localStorage.getItem('jwt_token') ||
      localStorage.getItem('access_token')
    )
  } catch (e) {
    return null
  }
}

function isAuthenticated(): boolean {
  const t = getToken()
  return !!t
}

function getCurrentUserId(): string | null {
  try {
    const token = getToken()
    if (!token) return null
    // If token looks like a JWT, decode payload and return `sub` or `user_id`
    const parts = token.split('.')
    if (parts.length === 3) {
      try {
        const payload = JSON.parse(Buffer.from(parts[1], 'base64').toString())
        return payload.sub || payload.user_id || null
      } catch (e) {
        return null
      }
    }
    // fallback: check stored user id
    return localStorage.getItem('todo_user_id') || null
  } catch (e) {
    return null
  }
}

export const authService = {
  login,
  signup,
  register,
  logout,
  getToken,
  isAuthenticated,
  getCurrentUserId,
}

export default authService

