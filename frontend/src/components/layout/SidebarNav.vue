<template>
  <aside class="sidebar-aside">
    <nav class="sidebar-nav">
      <router-link
        v-for="item in mainItems"
        :key="item.to"
        :to="item.to"
        class="sidebar-item"
        :class="{ active: isActive(item) }"
      >
        <el-icon><component :is="item.icon" /></el-icon>
        <span>{{ item.label }}</span>
      </router-link>

      <div class="nav-section">
        <div class="nav-section-title">个人中心</div>
        <router-link
          v-for="item in profileItems"
          :key="item.to"
          :to="item.to"
          class="sidebar-item"
          :class="{ active: isActive(item) }"
        >
          <el-icon><component :is="item.icon" /></el-icon>
          <span>{{ item.label }}</span>
        </router-link>
      </div>
    </nav>
  </aside>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { House, School, Calendar, Bell, List, Lock, Reading, DataAnalysis, User } from '@element-plus/icons-vue'

const props = defineProps({
  userRole: {
    type: String,
    default: ''
  }
})

const route = useRoute()

const mainItems = [
  { to: '/dashboard', label: '首页', icon: House, match: (path) => path === '/dashboard' },
  { to: '/classrooms', label: '教室列表', icon: School, match: (path) => path.startsWith('/classrooms') },
  { to: '/booking', label: '预约教室', icon: Calendar, match: (path) => path.startsWith('/booking') },
  { to: '/announcements', label: '系统公告', icon: Bell, match: (path) => path.startsWith('/announcements') },
  { to: '/stats', label: '统计报表', icon: DataAnalysis, match: (path) => path.startsWith('/stats') }
]

const profileItems = computed(() => {
  const baseItems = [
    { to: '/profile', label: '个人资料', icon: User, match: (path) => path === '/profile' },
    { to: '/my-reservations', label: '我的预约', icon: List, match: (path) => path === '/my-reservations' },
    { to: '/change-password', label: '修改密码', icon: Lock, match: (path) => path === '/change-password' }
  ]

  if (props.userRole === 'teacher') {
    baseItems.push({ to: '/teacher-courses', label: '关联课程', icon: Reading, match: (path) => path === '/teacher-courses' })
  }

  return baseItems
})

const isActive = (item) => item.match(route.path)
</script>

<style scoped>
.sidebar-aside {
  flex: 0 0 220px;
  width: 220px;
  max-width: 220px;
  box-sizing: border-box;
  background-color: #ffffff;
  border-right: 1px solid #e5e7eb;
  padding: 16px 12px;
  overflow-y: auto;
}

.sidebar-nav {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.nav-section {
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #f3f4f6;
}

.nav-section-title {
  padding: 8px 16px;
  font-size: 0.75rem;
  font-weight: 600;
  color: #9ca3af;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.sidebar-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border-radius: 10px;
  color: #6b7280;
  font-weight: 500;
  font-size: 0.875rem;
  text-decoration: none;
  transition: all 0.2s ease;
  border: 2px solid transparent;
}

.sidebar-item:hover {
  background-color: #f9fafb;
  color: #00897b;
}

.sidebar-item.active {
  background-color: #e0f2f1;
  color: #00897b;
  border-left: 4px solid #00897b;
  padding-left: 14px;
}

.sidebar-item .el-icon {
  font-size: 18px;
}

@media (max-width: 768px) {
  .sidebar-aside {
    flex: 0 0 60px;
    width: 60px;
    max-width: 60px;
    padding: 16px 8px;
  }

  .sidebar-item span,
  .nav-section-title {
    display: none;
  }

  .sidebar-item {
    justify-content: center;
    padding: 12px;
  }

  .sidebar-item.active {
    padding-left: 12px;
    border-left: none;
    border-bottom: 3px solid #00897b;
  }
}
</style>
