import { createRouter, createWebHistory } from 'vue-router'
import { ElMessage } from 'element-plus'
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
        path: 'profile',
        name: 'Profile',
        component: () => import('@/views/Profile.vue'),
        meta: { requiresAuth: true }
      },
      {
        path: 'teacher-courses',
        name: 'TeacherCourses',
        component: () => import('@/views/TeacherCourses.vue'),
        meta: { requiresAuth: true, roles: ['teacher'] }
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
        path: 'stats',
        name: 'Stats',
        component: () => import('@/views/Stats.vue')
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach(async (to, _, next) => {
  const isAuthenticated = store.getters.isAuthenticated
  
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login')
    return
  }

  if (isAuthenticated && !store.state.user) {
    try {
      await store.dispatch('fetchUserInfo')
    } catch (error) {
      next('/login')
      return
    }
  }

  if (to.meta.requiresAdmin && !store.getters.isAdmin) {
    next('/dashboard')
    return
  }

  const routeRoles = Array.isArray(to.meta.roles) ? to.meta.roles : []
  if (routeRoles.length > 0) {
    const currentRole = store.state.user?.role
    if (!routeRoles.includes(currentRole)) {
      ElMessage.warning('仅教师可访问关联课程')
      next('/dashboard')
      return
    }
  }

  next()
})

export default router
