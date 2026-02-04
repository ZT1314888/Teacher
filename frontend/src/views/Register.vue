<template>
  <div class="register-container">
    <div class="register-card">
      <div class="icon">📝</div>
      <h1>注册新账号</h1>
      <p class="subtitle">Classroom Reservation System</p>
      
      <el-form :model="form" :rules="rules" ref="registerForm" label-width="90px" class="register-form">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="form.username" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="form.email" placeholder="请输入邮箱" />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="form.password" type="password" placeholder="至少6位" />
        </el-form-item>
        <el-form-item label="确认密码" prop="password_confirm">
          <el-input v-model="form.password_confirm" type="password" placeholder="再次输入密码" />
        </el-form-item>
        <el-form-item label="姓名" prop="first_name">
          <el-input v-model="form.first_name" placeholder="请输入真实姓名" />
        </el-form-item>
        <el-form-item label="角色" prop="role">
          <el-select v-model="form.role" style="width: 100%" placeholder="请选择角色">
            <el-option label="学生" value="student" />
            <el-option label="教师" value="teacher" />
          </el-select>
        </el-form-item>
        <el-form-item label="手机号" prop="phone">
          <el-input v-model="form.phone" placeholder="请输入手机号（可选）" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" class="submit-btn" @click="handleRegister" :loading="loading">
            立即注册
          </el-button>
        </el-form-item>
        <el-form-item>
          <el-button class="back-btn" @click="$router.push('/login')">
            返回登录
          </el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { register } from '@/api/auth'

export default {
  name: 'Register',
  setup() {
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
      } else if (value !== form.value.password) {
        callback(new Error('两次输入密码不一致'))
      } else {
        callback()
      }
    }
    
    const rules = {
      username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
      email: [
        { required: true, message: '请输入邮箱', trigger: 'blur' },
        { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
      ],
      password: [
        { required: true, message: '请输入密码', trigger: 'blur' },
        { min: 6, message: '密码长度至少6位', trigger: 'blur' }
      ],
      password_confirm: [
        { required: true, validator: validatePass, trigger: 'blur' }
      ],
      first_name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
      role: [{ required: true, message: '请选择角色', trigger: 'change' }]
    }
    
    const handleRegister = async () => {
      if (!registerForm.value) return
      
      await registerForm.value.validate(async (valid) => {
        if (valid) {
          loading.value = true
          try {
            await register(form.value)
            ElMessage.success('注册成功，请登录')
            router.push('/login')
          } catch (error) {
            // 优先展示后端返回的具体错误信息（例如：邮箱已注册）
            let msg = '注册失败，请检查输入信息'
            if (error.response && error.response.data) {
              const data = error.response.data
              if (typeof data === 'string') {
                msg = data
              } else if (data.username && Array.isArray(data.username) && data.username.length) {
                msg = data.username[0]
              } else if (data.email && Array.isArray(data.email) && data.email.length) {
                msg = data.email[0]
              } else if (data.detail) {
                msg = data.detail
              } else if (data.non_field_errors && data.non_field_errors.length) {
                msg = data.non_field_errors[0]
              }
            }
            ElMessage.error(msg)
          } finally {
            loading.value = false
          }
        }
      })
    }
    
    return {
      form,
      rules,
      registerForm,
      loading,
      handleRegister
    }
  }
}
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 40px 20px;
}

.register-card {
  background: white;
  border-radius: 20px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  padding: 40px;
  max-width: 550px;
  width: 100%;
  text-align: center;
}

.icon {
  font-size: 3.5em;
  margin-bottom: 15px;
}

h1 {
  color: #667eea;
  margin-bottom: 10px;
  font-size: 2em;
}

.subtitle {
  color: #666;
  margin-bottom: 30px;
  font-size: 1em;
}

.register-form {
  text-align: left;
}

.submit-btn {
  width: 100%;
  height: 45px;
  font-size: 16px;
  font-weight: 600;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  border-radius: 8px;
  transition: all 0.3s;
}

.submit-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
}

.back-btn {
  width: 100%;
  height: 45px;
  font-size: 16px;
  font-weight: 600;
  background: white;
  color: #667eea;
  border: 2px solid #667eea;
  border-radius: 8px;
  transition: all 0.3s;
}

.back-btn:hover {
  background: #f0f4ff;
  transform: translateY(-2px);
}

:deep(.el-input__wrapper) {
  border-radius: 8px;
}

:deep(.el-form-item__label) {
  font-weight: 600;
  color: #333;
}
</style>
