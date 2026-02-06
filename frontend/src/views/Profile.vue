<template>
  <div class="min-h-screen bg-background py-8">
    <PageHeader>
      <template #actions>
        <el-button type="primary" plain @click="router.push('/change-password')">修改密码</el-button>
      </template>
    </PageHeader>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="profile-layout">
        <section class="profile-card">
          <div class="profile-avatar">
            {{ userInitial }}
          </div>
          <h2 class="profile-name">{{ profile.username || '用户' }}</h2>
          <p class="profile-role">{{ roleText }}</p>

          <div class="profile-meta">
            <div class="meta-item">
              <span class="meta-label">用户ID</span>
              <span class="meta-value">#{{ profile.id || '-' }}</span>
            </div>
            <div class="meta-item">
              <span class="meta-label">注册时间</span>
              <span class="meta-value">{{ formatDate(profile.date_joined) }}</span>
            </div>
            <div class="meta-item">
              <span class="meta-label">当前院系</span>
              <span class="meta-value">{{ profile.department_name || '未设置' }}</span>
            </div>
          </div>
        </section>

        <section class="profile-form-card">
          <div class="form-head">
            <h3>个人资料</h3>
            <p>更新后将同步到系统账户信息</p>
          </div>

          <el-form ref="formRef" :model="form" :rules="rules" label-position="top" v-loading="loading">
            <el-row :gutter="16">
              <el-col :xs="24" :sm="12">
                <el-form-item label="用户名">
                  <el-input v-model="profile.username" disabled />
                </el-form-item>
              </el-col>
              <el-col :xs="24" :sm="12">
                <el-form-item label="角色">
                  <el-input :model-value="roleText" disabled />
                </el-form-item>
              </el-col>
            </el-row>

            <el-row :gutter="16">
              <el-col :xs="24" :sm="12">
                <el-form-item label="姓" prop="first_name">
                  <el-input v-model="form.first_name" placeholder="请输入姓" />
                </el-form-item>
              </el-col>
              <el-col :xs="24" :sm="12">
                <el-form-item label="名" prop="last_name">
                  <el-input v-model="form.last_name" placeholder="请输入名" />
                </el-form-item>
              </el-col>
            </el-row>

            <el-row :gutter="16">
              <el-col :xs="24" :sm="12">
                <el-form-item label="邮箱" prop="email">
                  <el-input v-model="form.email" placeholder="请输入邮箱" />
                </el-form-item>
              </el-col>
              <el-col :xs="24" :sm="12">
                <el-form-item label="手机号" prop="phone">
                  <el-input v-model="form.phone" placeholder="请输入手机号（可选）" maxlength="11" />
                </el-form-item>
              </el-col>
            </el-row>

            <el-form-item label="院系" prop="department">
              <el-select v-model="form.department" placeholder="请选择院系" clearable style="width: 100%">
                <el-option
                  v-for="item in departments"
                  :key="item.id"
                  :label="item.name"
                  :value="item.id"
                />
              </el-select>
            </el-form-item>

            <div class="form-actions">
              <el-button @click="resetForm">重置</el-button>
              <el-button type="primary" :loading="saving" @click="submitForm">
                {{ saving ? '保存中...' : '保存资料' }}
              </el-button>
            </div>
          </el-form>
        </section>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import { ElMessage } from 'element-plus'
import PageHeader from '@/components/common/PageHeader.vue'
import { getDepartments, getUserInfo, updateMyProfile } from '@/api/user'

const router = useRouter()
const store = useStore()
const formRef = ref(null)

const loading = ref(false)
const saving = ref(false)
const departments = ref([])
const profile = ref({})

const form = reactive({
  email: '',
  first_name: '',
  last_name: '',
  phone: '',
  department: null
})

const rules = {
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '邮箱格式不正确', trigger: ['blur', 'change'] }
  ],
  first_name: [
    { required: true, message: '请输入姓', trigger: 'blur' }
  ],
  last_name: [
    { required: true, message: '请输入名', trigger: 'blur' }
  ],
  phone: [
    {
      validator: (_, value, callback) => {
        if (!value) {
          callback()
          return
        }
        const ok = /^1\d{10}$/.test(value)
        callback(ok ? undefined : new Error('手机号格式不正确'))
      },
      trigger: ['blur', 'change']
    }
  ]
}

const roleText = computed(() => {
  const roleMap = {
    admin: '管理员',
    teacher: '教师',
    student: '学生'
  }
  return roleMap[profile.value?.role] || '用户'
})

const userInitial = computed(() => (profile.value?.username?.[0] || '?').toUpperCase())

const normalizeList = (payload) => {
  if (Array.isArray(payload)) return payload
  if (Array.isArray(payload?.results)) return payload.results
  if (Array.isArray(payload?.data)) return payload.data
  return []
}

const patchForm = (user) => {
  form.email = user?.email || ''
  form.first_name = user?.first_name || ''
  form.last_name = user?.last_name || ''
  form.phone = user?.phone || ''
  form.department = user?.department ?? null
}

const loadProfile = async () => {
  loading.value = true
  try {
    const data = await getUserInfo()
    profile.value = data || {}
    patchForm(profile.value)
  } catch (error) {
    ElMessage.error('获取个人资料失败')
  } finally {
    loading.value = false
  }
}

const loadDepartments = async () => {
  try {
    const data = await getDepartments()
    departments.value = normalizeList(data)
  } catch (error) {
    departments.value = []
  }
}

const resetForm = () => {
  patchForm(profile.value)
  if (formRef.value) formRef.value.clearValidate()
}

const submitForm = async () => {
  if (!formRef.value) return
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return

  saving.value = true
  try {
    const payload = {
      email: form.email,
      first_name: form.first_name,
      last_name: form.last_name,
      phone: form.phone || null,
      department: form.department || null
    }
    const data = await updateMyProfile(payload)
    profile.value = data || {}
    patchForm(profile.value)
    store.commit('SET_USER', profile.value)
    ElMessage.success('个人资料保存成功')
  } catch (error) {
    ElMessage.error(error?.response?.data?.email?.[0] || '个人资料保存失败')
  } finally {
    saving.value = false
  }
}

const formatDate = (dateText) => {
  if (!dateText) return '-'
  const date = new Date(dateText)
  if (Number.isNaN(date.getTime())) return '-'
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  })
}

onMounted(async () => {
  await Promise.allSettled([loadProfile(), loadDepartments()])
})
</script>

<style scoped>
.profile-layout {
  display: grid;
  grid-template-columns: 280px minmax(0, 1fr);
  gap: 20px;
}

.profile-card {
  background: #fff;
  border: 1px solid #f1f5f9;
  border-radius: 16px;
  padding: 24px;
  text-align: center;
  height: fit-content;
}

.profile-avatar {
  width: 84px;
  height: 84px;
  border-radius: 999px;
  margin: 0 auto 12px;
  background: linear-gradient(135deg, #10b981 0%, #0f766e 100%);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 30px;
  font-weight: 700;
}

.profile-name {
  margin: 0;
  font-size: 20px;
  font-weight: 700;
  color: #0f172a;
}

.profile-role {
  margin: 8px 0 16px;
  color: #475569;
  font-size: 13px;
}

.profile-meta {
  display: grid;
  gap: 12px;
  text-align: left;
}

.meta-item {
  border: 1px solid #f1f5f9;
  border-radius: 10px;
  padding: 10px 12px;
  display: flex;
  justify-content: space-between;
  gap: 12px;
}

.meta-label {
  color: #64748b;
  font-size: 12px;
}

.meta-value {
  color: #0f172a;
  font-weight: 600;
  font-size: 12px;
}

.profile-form-card {
  background: #fff;
  border: 1px solid #f1f5f9;
  border-radius: 16px;
  padding: 24px;
}

.form-head h3 {
  margin: 0;
  color: #0f172a;
  font-size: 20px;
}

.form-head p {
  margin: 6px 0 18px;
  color: #64748b;
  font-size: 13px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 8px;
}

@media (max-width: 1024px) {
  .profile-layout {
    grid-template-columns: 1fr;
  }
}
</style>
