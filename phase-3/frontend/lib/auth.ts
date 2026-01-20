import { apiClient } from '@/lib/api'

type Credentials = {
  email: string
  password: string
}

async function login({ email, password }: Credentials) {
  const res = await apiClient.post('/auth/login', { email, password })
  const token = res?.data?.token
  if (typeof window !== 'undefined' && token) {
    localStorage.setItem('token', token)
  }
  return res.data
}

async function signup({ email, password }: Credentials) {
  const res = await apiClient.post('/auth/signup', { email, password })
  const token = res?.data?.token
  if (typeof window !== 'undefined' && token) {
    localStorage.setItem('token', token)
  }
  return res.data
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
  logout,
  getToken,
  isAuthenticated,
  getCurrentUserId,
}

export default authService