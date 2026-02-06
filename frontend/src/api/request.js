import axios from 'axios'
import { ElMessage } from 'element-plus'
import router from '@/router'

const request = axios.create({
  baseURL: 'http://localhost:8000/api',
  timeout: 10000
})

// 请求拦截器
request.interceptors.request.use(
  config => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
request.interceptors.response.use(
  response => {
    const payload = response.data
    if (
      payload &&
      typeof payload === 'object' &&
      Object.prototype.hasOwnProperty.call(payload, 'code') &&
      Object.prototype.hasOwnProperty.call(payload, 'data')
    ) {
      return payload.data
    }
    return payload
  },
  async error => {
    if (error.response) {
      switch (error.response.status) {
        case 400:
          break
        case 401:
          // Token 过期，尝试刷新
          const refreshToken = localStorage.getItem('refresh_token')
          if (refreshToken) {
            try {
              const res = await axios.post('http://localhost:8000/api/token/refresh/', {
                refresh: refreshToken
              })
              localStorage.setItem('access_token', res.data.access)
              // 重试原请求
              error.config.headers['Authorization'] = `Bearer ${res.data.access}`
              return axios(error.config)
            } catch (e) {
              localStorage.clear()
              router.push('/login')
              ElMessage.error('登录已过期，请重新登录')
            }
          } else {
            router.push('/login')
          }
          break
        case 403:
          ElMessage.error('没有权限访问')
          break
        case 404:
          ElMessage.error('请求的资源不存在')
          break
        case 500:
          // 服务器内部错误，交给具体页面处理，避免重复弹出通用错误
          break
        default:
          ElMessage.error(error.response.data.detail || '请求失败')
      }
    }
    return Promise.reject(error)
  }
)

export default request
