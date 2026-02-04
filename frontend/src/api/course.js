import request from './request'

export const getMyCourses = () => {
  return request({
    url: '/courses/',
    method: 'get'
  })
}
