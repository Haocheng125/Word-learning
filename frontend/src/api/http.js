import axios from 'axios'

const http = axios.create({
  baseURL: '/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器 - 添加 Token
http.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器 - 处理错误
http.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    if (error.response) {
      const { status, data } = error.response
      
      if (status === 401) {
        // Token 过期，清除登录状态
        localStorage.removeItem('access_token')
        localStorage.removeItem('user')
        window.location.href = '/login'
      }
      
      return Promise.reject(data)
    }
    return Promise.reject({ message: '网络错误，请稍后重试' })
  }
)

export default http
