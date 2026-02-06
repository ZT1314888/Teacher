<template>
  <el-header class="app-header">
    <div class="header-content">
      <div class="logo-section">
        <div class="logo-icon">
          <School />
        </div>
        <h1>教室预约管理系统</h1>
      </div>

      <div class="user-info">
        <NotificationBadge :unread-count="unreadCount" @click="$emit('notifications')" />
        <div class="user-details">
          <span class="user-name">{{ user?.username }}</span>
          <span class="user-role">{{ roleText }}</span>
        </div>
        <el-dropdown trigger="click" @command="$emit('command', $event)">
          <div class="avatar-container">
            <div class="avatar">
              {{ user?.username?.charAt(0)?.toUpperCase() || '?' }}
            </div>
          </div>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="profile">
                <el-icon><User /></el-icon>
                <span>个人资料</span>
              </el-dropdown-item>
              <el-dropdown-item command="settings">
                <el-icon><Setting /></el-icon>
                <span>设置</span>
              </el-dropdown-item>
              <el-dropdown-item divided command="logout">
                <el-icon><SwitchButton /></el-icon>
                <span>退出登录</span>
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </div>
  </el-header>
</template>

<script setup>
import { School, User, Setting, SwitchButton } from '@element-plus/icons-vue'
import NotificationBadge from '@/components/NotificationBadge.vue'

defineProps({
  user: {
    type: Object,
    default: () => ({})
  },
  roleText: {
    type: String,
    default: ''
  },
  unreadCount: {
    type: Number,
    default: 0
  }
})

defineEmits(['command', 'notifications'])
</script>

<style scoped>
.app-header {
  background: #ffffff;
  color: #1f2937;
  display: flex;
  align-items: center;
  border-bottom: 1px solid #e5e7eb;
  padding: 0 24px;
  height: 64px;
}

.header-content {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo-section {
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: 0;
}

.logo-icon {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #00897b 0%, #00796b 100%);
  border-radius: 10px;
  color: white;
  font-size: 20px;
}

h1 {
  margin: 0;
  color: #1f2937;
  font-weight: 600;
  font-size: 1.25rem;
  letter-spacing: -0.025em;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 16px;
}

.user-details {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 2px;
}

.user-name {
  font-weight: 600;
  font-size: 0.875rem;
  color: #1f2937;
}

.user-role {
  font-size: 0.75rem;
  color: #6b7280;
  padding: 2px 8px;
  background: #f3f4f6;
  border-radius: 12px;
}

.avatar-container {
  cursor: pointer;
  transition: all 0.2s ease;
}

.avatar-container:hover {
  transform: scale(1.05);
}

.avatar {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #00897b 0%, #00796b 100%);
  color: white;
  font-weight: 600;
  font-size: 1rem;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 137, 123, 0.15);
}

:deep(.el-dropdown-menu__item) {
  display: flex;
  align-items: center;
  gap: 8px;
}

@media (max-width: 768px) {
  .user-details {
    display: none;
  }

  h1 {
    font-size: 1rem;
  }
}
</style>
