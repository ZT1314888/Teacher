<template>
  <el-container class="layout-container">
    <el-header>
      <div class="header-content">
        <h2>教室预约管理系统</h2>
        <div class="user-info">
          <span>{{ user?.username }} ({{ roleText }})</span>
          <el-button type="danger" size="small" @click="handleLogout">退出</el-button>
        </div>
      </div>
    </el-header>
    <el-container>
      <el-aside width="200px">
        <el-menu :default-active="$route.path" router>
          <el-menu-item index="/dashboard">
            <el-icon><House /></el-icon>
            <span>首页</span>
          </el-menu-item>
          <el-menu-item index="/classrooms">
            <el-icon><School /></el-icon>
            <span>教室列表</span>
          </el-menu-item>
          <el-menu-item index="/booking">
            <el-icon><Calendar /></el-icon>
            <span>预约教室</span>
          </el-menu-item>
          <el-menu-item index="/announcements">
            <el-icon><Bell /></el-icon>
            <span>系统公告</span>
          </el-menu-item>
          <el-sub-menu index="personal">
            <template #title>
              <el-icon><User /></el-icon>
              <span>个人中心</span>
            </template>
            <el-menu-item index="/my-reservations">
              <el-icon><List /></el-icon>
              <span>我的预约</span>
            </el-menu-item>
            <el-menu-item index="/change-password">
              <el-icon><Lock /></el-icon>
              <span>修改密码</span>
            </el-menu-item>
            <el-menu-item index="/teacher-courses" v-if="user?.role === 'teacher'">
              <el-icon><List /></el-icon>
              <span>关联课程</span>
            </el-menu-item>
          </el-sub-menu>
          <el-menu-item index="/admin" v-if="isAdmin">
            <el-icon><Setting /></el-icon>
            <span>系统管理</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
import { computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import { House, School, Calendar, List, Setting, User, Lock, Bell } from '@element-plus/icons-vue'

export default {
  name: 'Layout',
  components: { House, School, Calendar, List, Setting, User, Lock, Bell },
  setup() {
    const store = useStore()
    const router = useRouter()
    
    const user = computed(() => store.state.user)
    const isAdmin = computed(() => store.getters.isAdmin)
    
    const roleText = computed(() => {
      const roleMap = {
        admin: '管理员',
        teacher: '教师',
        student: '学生'
      }
      return roleMap[user.value?.role] || ''
    })
    
    const handleLogout = () => {
      store.dispatch('logout')
      router.push('/login')
    }
    
    return {
      user,
      isAdmin,
      roleText,
      handleLogout
    }
  }
}
</script>

<style scoped>
.layout-container {
  height: 100vh;
}

.el-header {
  background: linear-gradient(135deg, #0F4C3A 0%, #1a6b54 100%);
  color: white;
  display: flex;
  align-items: center;
  box-shadow: 0 2px 10px rgba(15, 76, 58, 0.15);
}

.header-content {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-content h2 {
  margin: 0;
  color: white;
  font-weight: 600;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 15px;
}

.user-info span {
  font-weight: 500;
}

.el-aside {
  background-color: #f9fafb;
  border-right: 1px solid #e5e7eb;
}

:deep(.el-menu) {
  border-right: none;
  background-color: #f9fafb;
}

:deep(.el-menu-item) {
  border-radius: 8px;
  margin: 5px 10px;
  transition: all 0.3s;
}

:deep(.el-menu-item:hover) {
  background-color: #e0f2ea !important;
  color: #0F4C3A !important;
}

:deep(.el-menu-item.is-active) {
  background: linear-gradient(135deg, #0F4C3A 0%, #1a6b54 100%) !important;
  color: white !important;
}

:deep(.el-sub-menu__title) {
  border-radius: 8px;
  margin: 5px 10px;
  transition: all 0.3s;
}

:deep(.el-sub-menu__title:hover) {
  background-color: #e0f2ea !important;
  color: #0F4C3A !important;
}

:deep(.el-sub-menu.is-active .el-sub-menu__title) {
  color: #0F4C3A !important;
}

.el-main {
  background-color: #f3f4f6;
  padding: 20px;
}

:deep(.el-button--danger) {
  background: #ef4444;
  border-color: #ef4444;
}

:deep(.el-button--danger:hover) {
  background: #dc2626;
  border-color: #dc2626;
}
</style>
