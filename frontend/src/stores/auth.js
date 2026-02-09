import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import http from '../api/http'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const token = ref(null)
  
  const isAuthenticated = computed(() => !!token.value)
  const isAdmin = computed(() => user.value?.is_admin || false)
  
  function checkAuth() {
    const savedToken = localStorage.getItem('access_token')
    const savedUser = localStorage.getItem('user')
    
    if (savedToken && savedUser) {
      token.value = savedToken
      user.value = JSON.parse(savedUser)
    }
  }
  
  async function login(email, password) {
    const response = await http.post('/auth/login', { email, password })
    
    if (response.success) {
      token.value = response.access_token
      user.value = response.user
      
      localStorage.setItem('access_token', response.access_token)
      localStorage.setItem('user', JSON.stringify(response.user))
    }
    
    return response
  }
  
  async function register(username, email, password) {
    const response = await http.post('/auth/register', { username, email, password })
    return response
  }
  
  function logout() {
    token.value = null
    user.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('user')
  }
  
  return {
    user,
    token,
    isAuthenticated,
    isAdmin,
    checkAuth,
    login,
    register,
    logout
  }
})
