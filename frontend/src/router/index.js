import { createRouter, createWebHistory } from 'vue-router'
import store from '@/store'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/Register.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/',
    component: () => import('@/views/Layout.vue'),
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        redirect: '/dashboard'
      },
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('@/views/Dashboard.vue')
      },
      {
        path: 'classrooms',
        name: 'Classrooms',
        component: () => import('@/views/Classrooms.vue')
      },
      {
        path: 'booking',
        name: 'Booking',
        component: () => import('@/views/Booking.vue')
      },
      {
        path: 'reservations',
        name: 'Reservations',
        component: () => import('@/views/Reservations.vue')
      },
      {
        path: 'my-reservations',
        name: 'MyReservations',
        component: () => import('@/views/MyReservations.vue'),
        meta: { requiresAuth: true }
      },
      {
        path: 'teacher-courses',
        name: 'TeacherCourses',
        component: () => import('@/views/TeacherCourses.vue'),
        meta: { requiresAuth: true }
      },
      {
        path: 'change-password',
        name: 'ChangePassword',
        component: () => import('@/views/ChangePassword.vue')
      },
      {
        path: 'announcements',
        name: 'Announcements',
        component: () => import('@/views/Announcements.vue')
      },
      {
        path: 'admin',
        name: 'Admin',
        component: () => import('@/views/Admin.vue'),
        meta: { requiresAuth: true, requiresAdmin: true },
        redirect: '/admin/announcements',
        children: [
          {
            path: 'announcements',
            name: 'AdminAnnouncements',
            component: () => import('@/views/admin/Announcements.vue')
          },
          {
            path: 'classrooms',
            name: 'AdminClassrooms',
            component: () => import('@/views/admin/Classrooms.vue')
          },
          {
            path: 'users',
            name: 'AdminUsers',
            component: () => import('@/views/admin/Users.vue')
          },
          {
            path: 'reservations',
            name: 'AdminReservations',
            component: () => import('@/views/admin/Reservations.vue')
          }
        ]
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach(async (to, from, next) => {
  const isAuthenticated = store.getters.isAuthenticated
  
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login')
  } else if (to.meta.requiresAdmin && !store.getters.isAdmin) {
    next('/dashboard')
  } else {
    if (isAuthenticated && !store.state.user) {
      try {
        await store.dispatch('fetchUserInfo')
      } catch (error) {
        next('/login')
        return
      }
    }
    next()
  }
})

export default router
