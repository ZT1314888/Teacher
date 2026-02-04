import request from './request'

export const login = (data) => {
  return request({
    url: '/token/',
    method: 'post',
    data
  })
}

export const register = (data) => {
  return request({
    url: '/users/',
    method: 'post',
    data
  })
}

export const getUserInfo = () => {
  return request({
    url: '/users/me/',
    method: 'get'
  })
}

export const changePassword = (userId, data) => {
  return request({
    url: `/users/${userId}/change_password/`,
    method: 'post',
    data
  })
}
