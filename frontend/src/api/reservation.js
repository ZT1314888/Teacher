import request from './request'

export const getReservations = (params) => {
  return request({
    url: '/reservations/',
    method: 'get',
    params
  })
}

export const getMyReservations = () => {
  return request({
    url: '/reservations/my_reservations/',
    method: 'get'
  })
}

export const createReservation = (data) => {
  return request({
    url: '/reservations/',
    method: 'post',
    data
  })
}

export const checkConflict = (data) => {
  return request({
    url: '/reservations/check_conflict/',
    method: 'post',
    data
  })
}

export const approveReservation = (id, data) => {
  return request({
    url: `/reservations/${id}/approve/`,
    method: 'post',
    data
  })
}

export const rejectReservation = (id, data) => {
  return request({
    url: `/reservations/${id}/reject/`,
    method: 'post',
    data
  })
}

export const cancelReservation = (id) => {
  return request({
    url: `/reservations/${id}/cancel/`,
    method: 'post'
  })
}
