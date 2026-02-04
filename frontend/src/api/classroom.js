import request from './request'

export const getClassrooms = (params) => {
  return request({
    url: '/classrooms/',
    method: 'get',
    params
  })
}

export const getClassroomDetail = (id) => {
  return request({
    url: `/classrooms/${id}/`,
    method: 'get'
  })
}

export const createClassroom = (data) => {
  return request({
    url: '/classrooms/',
    method: 'post',
    data
  })
}

export const updateClassroom = (id, data) => {
  return request({
    url: `/classrooms/${id}/`,
    method: 'put',
    data
  })
}

export const deleteClassroom = (id) => {
  return request({
    url: `/classrooms/${id}/`,
    method: 'delete'
  })
}

export const getAvailableClassrooms = () => {
  return request({
    url: '/classrooms/available/',
    method: 'get'
  })
}
