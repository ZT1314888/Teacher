import request from './request'

export const getDashboardStats = () => request({ url: '/stats/dashboard/', method: 'get' })
export const getClassroomUsage = () => request({ url: '/stats/classroom-usage/', method: 'get' })
export const getDailySummary = () => request({ url: '/stats/daily-summary/', method: 'get' })
