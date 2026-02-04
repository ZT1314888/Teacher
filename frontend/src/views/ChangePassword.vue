<template>
  <div class="change-password">
    <h2>修改密码</h2>
    
    <el-card style="max-width: 600px; margin-top: 20px;">
      <el-form :model="form" :rules="rules" ref="passwordForm" label-width="100px">
        <el-form-item label="原密码" prop="old_password">
          <el-input v-model="form.old_password" type="password" placeholder="请输入原密码" />
        </el-form-item>
        
        <el-form-item label="新密码" prop="new_password">
          <el-input v-model="form.new_password" type="password" placeholder="至少6位" />
        </el-form-item>
        
        <el-form-item label="确认密码" prop="confirm_password">
          <el-input v-model="form.confirm_password" type="password" placeholder="再次输入新密码" />
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" @click="handleSubmit" :loading="loading">
            确认修改
          </el-button>
          <el-button @click="resetForm">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useStore } from 'vuex'
import { ElMessage } from 'element-plus'
import { changePassword } from '@/api/auth'

export default {
  name: 'ChangePassword',
  setup() {
    const store = useStore()
    const passwordForm = ref(null)
    const loading = ref(false)
    
    const form = ref({
      old_password: '',
      new_password: '',
      confirm_password: ''
    })
    
    const validatePass = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请再次输入密码'))
      } else if (value !== form.value.new_password) {
        callback(new Error('两次输入密码不一致'))
      } else {
        callback()
      }
    }
    
    const rules = {
      old_password: [
        { required: true, message: '请输入原密码', trigger: 'blur' }
      ],
      new_password: [
        { required: true, message: '请输入新密码', trigger: 'blur' },
        { min: 6, message: '密码长度至少6位', trigger: 'blur' }
      ],
      confirm_password: [
        { required: true, validator: validatePass, trigger: 'blur' }
      ]
    }
    
    const handleSubmit = async () => {
      if (!passwordForm.value) return
      
      await passwordForm.value.validate(async (valid) => {
        if (valid) {
          loading.value = true
          try {
            await changePassword(store.state.user.id, {
              old_password: form.value.old_password,
              new_password: form.value.new_password
            })
            ElMessage.success('密码修改成功，请重新登录')
            
            // 清除登录状态
            store.dispatch('logout')
            setTimeout(() => {
              window.location.href = '/login'
            }, 1500)
          } catch (error) {
            ElMessage.error(error.response?.data?.error || '密码修改失败')
          } finally {
            loading.value = false
          }
        }
      })
    }
    
    const resetForm = () => {
      if (passwordForm.value) {
        passwordForm.value.resetFields()
      }
    }
    
    return {
      form,
      rules,
      passwordForm,
      loading,
      handleSubmit,
      resetForm
    }
  }
}
</script>

<style scoped>
.change-password {
  padding: 20px;
}

h2 {
  margin-bottom: 20px;
  color: #333;
}
</style>
