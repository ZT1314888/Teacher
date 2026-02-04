import request from './request'

export const getUsers = (params) => {
  return request({
    url: '/users/',
    method: 'get',
    params
  })
}

export const getUserInfo = () => {
  return request({
    url: '/users/me/',
    method: 'get'
  })
}

export const applyForAdmin = (data) => {
  return request({
    url: '/users/admin-requests/',
    method: 'post',
    data
  })
}

export const getAdminRequests = () => {
  return request({
    url: '/users/admin-requests/',
    method: 'get'
  })
}

export const approveAdminRequest = (id, data) => {
  return request({
    url: `/users/admin-requests/${id}/approve/`,
    method: 'post',
    data
  })
}

export const rejectAdminRequest = (id, data) => {
  return request({
    url: `/users/admin-requests/${id}/reject/`,
    method: 'post',
    data
  })
}
