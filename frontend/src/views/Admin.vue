<template>
  <div class="admin-layout">
    <el-container>
      <el-aside width="200px" class="admin-sidebar">
        <div class="sidebar-title">系统管理</div>
        <el-menu :default-active="$route.path" router>
          <el-menu-item index="/admin/announcements">
            <el-icon><Bell /></el-icon>
            <span>公告管理</span>
          </el-menu-item>
          <el-menu-item index="/admin/classrooms">
            <el-icon><School /></el-icon>
            <span>教室管理</span>
          </el-menu-item>
          <el-menu-item index="/admin/users">
            <el-icon><User /></el-icon>
            <span>用户管理</span>
          </el-menu-item>
          <el-menu-item index="/admin/reservations">
            <el-icon><Calendar /></el-icon>
            <span>预约管理</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      <el-main class="admin-content">
        <router-view />
      </el-main>
    </el-container>
  </div>
</template>

<script>
import { Bell, School, User, Calendar } from '@element-plus/icons-vue'

export default {
  name: 'Admin',
  components: { Bell, School, User, Calendar }
}
</script>

<style scoped>
.admin-layout {
  height: 100%;
}

.admin-sidebar {
  background-color: #f8fafc;
  border-right: 1px solid #e2e8f0;
  height: 100%;
}

.sidebar-title {
  padding: 20px;
  font-size: 18px;
  font-weight: 600;
  color: #333;
  border-bottom: 1px solid #e2e8f0;
}

:deep(.el-menu) {
  border-right: none;
  background-color: #f8fafc;
}

:deep(.el-menu-item) {
  border-radius: 8px;
  margin: 5px 10px;
  transition: all 0.3s;
}

:deep(.el-menu-item:hover) {
  background-color: #e0e7ff !important;
  color: #667eea !important;
}

:deep(.el-menu-item.is-active) {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
  color: white !important;
}

.admin-content {
  background-color: #fff;
  padding: 0;
}
</style>
