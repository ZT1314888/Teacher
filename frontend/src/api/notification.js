import request from './request'

export const getNotifications = () => request({ url: '/notifications/', method: 'get' })
export const markNotificationRead = (id) => request({ url: '/notifications/mark_read/', method: 'post', data: { id } })
export const markAllNotificationsRead = () => request({ url: '/notifications/mark_all_read/', method: 'post' })
export const markAnnouncementRead = (announcementId) =>
  request({ url: '/notifications/mark_announcement_read/', method: 'post', data: { announcement_id: announcementId } })
