<template>
  <AuthCard title="注册新账号" subtitle="创建您的教室预约系统账户" container-class="register-container-padding" card-class="register-card-size">
    <template #icon>
      <UserFilled />
    </template>

    <el-form ref="registerForm" :model="form" :rules="rules" label-position="top" class="register-form">
      <el-row :gutter="16">
        <el-col :span="12">
          <el-form-item label="用户名" prop="username">
            <el-input v-model="form.username" placeholder="请输入用户名" size="large" />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="姓名" prop="first_name">
            <el-input v-model="form.first_name" placeholder="请输入真实姓名" size="large" />
          </el-form-item>
        </el-col>
      </el-row>

      <el-form-item label="邮箱地址" prop="email">
        <el-input v-model="form.email" placeholder="example@email.com" size="large" />
      </el-form-item>

      <el-row :gutter="16">
        <el-col :span="12">
          <el-form-item label="密码" prop="password">
            <el-input v-model="form.password" type="password" placeholder="至少6位" size="large" show-password />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="确认密码" prop="password_confirm">
            <el-input v-model="form.password_confirm" type="password" placeholder="再次输入密码" size="large" show-password />
          </el-form-item>
        </el-col>
      </el-row>

      <el-row :gutter="16">
        <el-col :span="12">
          <el-form-item label="角色" prop="role">
            <el-select v-model="form.role" style="width: 100%" placeholder="请选择角色" size="large">
              <el-option label="学生" value="student">
                <div class="role-option">
                  <el-icon><User /></el-icon>
                  <span>学生</span>
                </div>
              </el-option>
              <el-option label="教师" value="teacher">
                <div class="role-option">
                  <el-icon><Reading /></el-icon>
                  <span>教师</span>
                </div>
              </el-option>
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="手机号" prop="phone">
            <el-input v-model="form.phone" placeholder="可选" size="large" />
          </el-form-item>
        </el-col>
      </el-row>

      <el-form-item>
        <el-button type="primary" class="submit-btn" :loading="loading" @click="handleRegister">
          {{ loading ? '注册中...' : '立即注册' }}
        </el-button>
      </el-form-item>

      <AuthFooterLink text="已有账号？" action-text="返回登录" @click="router.push('/login')" />
    </el-form>
  </AuthCard>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { UserFilled, User, Reading } from '@element-plus/icons-vue'
import { register } from '@/api/auth'
import AuthCard from '@/components/auth/AuthCard.vue'
import AuthFooterLink from '@/components/auth/AuthFooterLink.vue'

const router = useRouter()
const registerForm = ref(null)
const loading = ref(false)

const form = ref({
  username: '',
  email: '',
  password: '',
  password_confirm: '',
  first_name: '',
  role: 'student',
  phone: ''
})

const validatePass = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请再次输入密码'))
    return
  }

  if (value !== form.value.password) {
    callback(new Error('两次输入密码不一致'))
    return
  }

  callback()
}

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度在3-20个字符', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度至少6位', trigger: 'blur' }
  ],
  password_confirm: [{ required: true, validator: validatePass, trigger: 'blur' }],
  first_name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
  role: [{ required: true, message: '请选择角色', trigger: 'change' }]
}

const extractRegisterError = (error) => {
  let msg = '注册失败，请检查输入信息'
  const data = error?.response?.data
  if (!data) return msg

  if (typeof data === 'string') return data
  if (Array.isArray(data.username) && data.username.length) return data.username[0]
  if (Array.isArray(data.email) && data.email.length) return data.email[0]
  if (data.detail) return data.detail
  if (Array.isArray(data.non_field_errors) && data.non_field_errors.length) return data.non_field_errors[0]
  return msg
}

const handleRegister = async () => {
  if (!registerForm.value || loading.value) return

  await registerForm.value.validate(async (valid) => {
    if (!valid) return

    loading.value = true
    try {
      await register(form.value)
      ElMessage.success('注册成功，请登录')
      router.push('/login')
    } catch (error) {
      ElMessage.error(extractRegisterError(error))
    } finally {
      loading.value = false
    }
  })
}
</script>

<style scoped>
:deep(.register-container-padding) {
  padding: 40px 20px;
}

:deep(.register-card-size) {
  max-width: 580px;
}

.register-form {
  text-align: left;
}

:deep(.el-form-item__label) {
  font-weight: 600;
  color: #374151;
  font-size: 0.875rem;
  margin-bottom: 8px;
}

.submit-btn {
  width: 100%;
  height: 48px;
  font-size: 1rem;
  font-weight: 600;
  border-radius: 12px;
  margin-top: 8px;
}

.role-option {
  display: flex;
  align-items: center;
  gap: 8px;
}

@media (max-width: 640px) {
  :deep(.el-col) {
    width: 100% !important;
    flex: 0 0 100% !important;
    max-width: 100% !important;
  }
}
</style>
