<template>
  <div class="change-password">
    <PageHeader />

    <div class="password-form-container">
      <div class="form-card">
        <div class="form-header">
          <div class="form-icon">
            <Lock />
          </div>
          <h3>修改密码</h3>
          <p>请输入您的新密码信息</p>
        </div>

        <el-form :model="form" :rules="rules" ref="passwordForm" label-position="top" class="password-form">
          <el-form-item label="原密码" prop="old_password">
            <el-input
              v-model="form.old_password"
              type="password"
              placeholder="请输入当前密码"
              size="large"
              show-password
            />
          </el-form-item>

          <el-form-item label="新密码" prop="new_password">
            <el-input
              v-model="form.new_password"
              type="password"
              placeholder="至少6位字符"
              size="large"
              show-password
            />
          </el-form-item>

          <el-form-item label="确认新密码" prop="confirm_password">
            <el-input
              v-model="form.confirm_password"
              type="password"
              placeholder="再次输入新密码"
              size="large"
              show-password
            />
          </el-form-item>

          <div class="password-tips">
            <p class="tips-title">密码要求：</p>
            <ul class="tips-list">
              <li>密码长度至少6位</li>
              <li>建议包含字母、数字和特殊字符</li>
              <li>不要使用过于简单的密码</li>
            </ul>
          </div>

          <div class="form-actions">
            <el-button @click="resetForm" size="large">重置</el-button>
            <el-button type="primary" @click="handleSubmit" :loading="loading" size="large">
              {{ loading ? '提交中...' : '确认修改' }}
            </el-button>
          </div>
        </el-form>
      </div>

      <div class="security-tips">
        <h4>
          <el-icon><InfoFilled /></el-icon>
          安全提示
        </h4>
        <ul>
          <li>定期更换密码可以有效保护您的账户安全</li>
          <li>修改密码后，您需要重新登录系统</li>
          <li>请勿与他人分享您的账户信息</li>
          <li>建议使用强密码并定期更新</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useStore } from 'vuex'
import { ElMessage } from 'element-plus'
import { Lock, InfoFilled } from '@element-plus/icons-vue'
import { changePassword } from '@/api/auth'
import PageHeader from '@/components/common/PageHeader.vue'

export default {
  name: 'ChangePassword',
  components: { Lock, InfoFilled, PageHeader },
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
            ElMessage.error(error.response?.data?.old_password?.[0] || error.response?.data?.error || '密码修改失败')
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
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 8px;
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.password-form-container {
  display: grid;
  grid-template-columns: 1fr 320px;
  gap: 24px;
  max-width: 1000px;
  margin: 0 auto;
}

.form-card {
  background: white;
  border-radius: 16px;
  border: 1px solid #f3f4f6;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
  padding: 32px;
}

.form-header {
  text-align: center;
  margin-bottom: 32px;
}

.form-icon {
  width: 64px;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px;
  background: linear-gradient(135deg, #00897b 0%, #00796b 100%);
  border-radius: 16px;
  color: white;
  font-size: 32px;
  box-shadow: 0 4px 12px rgba(0, 137, 123, 0.2);
}

.form-header h3 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 8px;
}

.form-header p {
  color: #6b7280;
  font-size: 0.875rem;
  margin: 0;
}

.password-form {
  margin-top: 24px;
}

:deep(.el-form-item) {
  margin-bottom: 24px;
}

:deep(.el-form-item__label) {
  font-weight: 600;
  color: #374151;
  font-size: 0.875rem;
}

.password-tips {
  background: #f9fafb;
  border-radius: 12px;
  padding: 16px;
  margin: 24px 0;
}

.tips-title {
  font-weight: 600;
  color: #374151;
  font-size: 0.875rem;
  margin: 0 0 12px;
}

.tips-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.tips-list li {
  font-size: 0.875rem;
  color: #6b7280;
  padding-left: 20px;
  position: relative;
  margin-bottom: 8px;
}

.tips-list li:last-child {
  margin-bottom: 0;
}

.tips-list li::before {
  content: '•';
  position: absolute;
  left: 8px;
  color: #00897b;
  font-weight: bold;
}

.form-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  margin-top: 32px;
}

.form-actions .el-button {
  min-width: 120px;
}

.security-tips {
  background: linear-gradient(135deg, #e0f2f1 0%, #b2dfdb 100%);
  border-radius: 16px;
  padding: 24px;
  height: fit-content;
}

.security-tips h4 {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 1rem;
  font-weight: 600;
  color: #004d40;
  margin: 0 0 16px;
}

.security-tips h4 .el-icon {
  font-size: 20px;
}

.security-tips ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.security-tips li {
  font-size: 0.875rem;
  color: #00695c;
  padding-left: 24px;
  position: relative;
  margin-bottom: 12px;
  line-height: 1.5;
}

.security-tips li:last-child {
  margin-bottom: 0;
}

.security-tips li::before {
  content: '✓';
  position: absolute;
  left: 0;
  color: #00897b;
  font-weight: bold;
}

@media (max-width: 768px) {
  .password-form-container {
    grid-template-columns: 1fr;
  }

  .form-card {
    padding: 24px;
  }

  .form-actions {
    flex-direction: column;
  }

  .form-actions .el-button {
    width: 100%;
  }
}
</style>
