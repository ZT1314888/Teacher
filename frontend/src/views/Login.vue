<template>
  <AuthCard title="教室预约系统" subtitle="Classroom Reservation System" card-class="login-card-size">
    <template #icon>
      <School />
    </template>

    <el-form ref="loginForm" :model="form" :rules="rules" class="login-form">
      <el-form-item prop="username">
        <el-input
          v-model="form.username"
          placeholder="请输入用户名"
          size="large"
          prefix-icon="User"
        />
      </el-form-item>

      <el-form-item prop="password">
        <el-input
          v-model="form.password"
          type="password"
          placeholder="请输入密码"
          size="large"
          prefix-icon="Lock"
          @keyup.enter="handleLogin"
        />
      </el-form-item>

      <el-form-item>
        <el-button type="primary" class="login-btn" :loading="loading" @click="handleLogin">
          {{ loading ? '登录中...' : '登录系统' }}
        </el-button>
      </el-form-item>

      <AuthFooterLink text="还没有账号？" action-text="立即注册" @click="router.push('/register')" />
    </el-form>

    <div class="divider"><span>或</span></div>

    <div class="demo-credentials">
      <p class="demo-title">演示账号</p>
      <div class="demo-buttons">
        <el-button size="small" @click="fillDemo('teacher')">教师</el-button>
        <el-button size="small" @click="fillDemo('student')">学生</el-button>
      </div>
      <p class="demo-note">管理员请通过 Django 后台登录</p>
    </div>
  </AuthCard>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import { ElMessage } from 'element-plus'
import { School } from '@element-plus/icons-vue'
import { login } from '@/api/auth'
import AuthCard from '@/components/auth/AuthCard.vue'
import AuthFooterLink from '@/components/auth/AuthFooterLink.vue'

const router = useRouter()
const store = useStore()
const loginForm = ref(null)
const loading = ref(false)

const form = ref({
  username: '',
  password: ''
})

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
}

const demoCredentials = {
  teacher: { username: 'teacher', password: 'teacher123' },
  student: { username: 'student', password: 'student123' }
}

const fillDemo = (role) => {
  form.value = { ...demoCredentials[role] }
  ElMessage.info(`已填充${role === 'teacher' ? '教师' : '学生'}演示账号`)
}

const handleLogin = async () => {
  if (!loginForm.value || loading.value) return

  await loginForm.value.validate(async (valid) => {
    if (!valid) return

    loading.value = true
    try {
      const res = await login(form.value)
      store.dispatch('login', res)
      await store.dispatch('fetchUserInfo')
      ElMessage.success('登录成功')
      router.push('/')
    } catch (error) {
      ElMessage.error('登录失败，请检查用户名和密码')
    } finally {
      loading.value = false
    }
  })
}
</script>

<style scoped>
:deep(.login-card-size) {
  max-width: 440px;
  text-align: center;
}

.login-form {
  text-align: left;
}

:deep(.el-form-item:last-child) {
  margin-bottom: 0;
}

.login-btn {
  width: 100%;
  height: 48px;
  font-size: 1rem;
  font-weight: 600;
  border-radius: 12px;
}

.divider {
  position: relative;
  margin: 32px 0;
  text-align: center;
}

.divider::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  height: 1px;
  background: #e5e7eb;
}

.divider span {
  position: relative;
  background: white;
  padding: 0 16px;
  color: #9ca3af;
  font-size: 0.875rem;
}

.demo-credentials {
  text-align: center;
}

.demo-title {
  color: #6b7280;
  font-size: 0.875rem;
  margin: 0 0 16px;
}

.demo-buttons {
  display: flex;
  gap: 8px;
  justify-content: center;
}

.demo-buttons .el-button {
  border-radius: 8px;
  border-color: #e5e7eb;
  color: #6b7280;
}

.demo-buttons .el-button:hover {
  border-color: #00897b;
  color: #00897b;
  background: #e0f2f1;
}

.demo-note {
  color: #9ca3af;
  font-size: 0.75rem;
  margin-top: 12px;
  font-style: italic;
}

@media (max-width: 640px) {
  .demo-buttons {
    flex-direction: column;
  }

  .demo-buttons .el-button {
    width: 100%;
  }
}
</style>
