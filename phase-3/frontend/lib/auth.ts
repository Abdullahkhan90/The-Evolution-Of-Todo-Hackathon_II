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
    return localStorage.getItem('token')
  } catch (e) {
    return null
  }
}

function isAuthenticated(): boolean {
  const t = getToken()
  return !!t
}

export const authService = {
  login,
  signup,
  logout,
  getToken,
  isAuthenticated,
}

export default authService