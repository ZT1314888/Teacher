<template>
  <div class="login-container">
    <div class="login-card">
      <div class="icon">🏫</div>
      <h1>教室预约系统</h1>
      <p class="subtitle">Classroom Reservation System</p>
      
      <el-form :model="form" :rules="rules" ref="loginForm" class="login-form">
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
          <el-button 
            type="primary" 
            class="login-btn"
            @click="handleLogin" 
            :loading="loading"
          >
            登录系统
          </el-button>
        </el-form-item>
        <el-form-item>
          <el-button 
            class="register-btn"
            @click="$router.push('/register')"
          >
            注册新账号
          </el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import { ElMessage } from 'element-plus'
import { login } from '@/api/auth'

export default {
  name: 'Login',
  setup() {
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
    
    const handleLogin = async () => {
      if (!loginForm.value) return
      
      await loginForm.value.validate(async (valid) => {
        if (valid) {
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
        }
      })
    }
    
    return {
      form,
      rules,
      loginForm,
      loading,
      handleLogin
    }
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.login-card {
  background: white;
  border-radius: 20px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  padding: 50px 40px;
  max-width: 450px;
  width: 100%;
  text-align: center;
}

.icon {
  font-size: 4em;
  margin-bottom: 20px;
}

h1 {
  color: #667eea;
  margin-bottom: 10px;
  font-size: 2em;
}

.subtitle {
  color: #666;
  margin-bottom: 40px;
  font-size: 1em;
}

.login-form {
  text-align: left;
}

.login-btn {
  width: 100%;
  height: 45px;
  font-size: 16px;
  font-weight: 600;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  border-radius: 8px;
  transition: all 0.3s;
}

.login-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
}

.register-btn {
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

.register-btn:hover {
  background: #f0f4ff;
  transform: translateY(-2px);
}

:deep(.el-input__wrapper) {
  border-radius: 8px;
  padding: 8px 15px;
}

:deep(.el-input__inner) {
  font-size: 15px;
}
</style>
