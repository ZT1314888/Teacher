<template>
  <div class="admin-requests">
    <h2>我的申请</h2>

    <div class="actions">
      <el-button
        type="primary"
        :disabled="hasPendingOrApproved"
        @click="showApplyDialog = true"
      >
        申请成为管理员
      </el-button>
      <span v-if="hasPendingOrApproved" class="hint">
        您已有待审核或已批准的申请，无法重复申请。
      </span>
    </div>

    <el-table :data="requests" border style="width: 100%; margin-top: 20px;">
      <el-table-column prop="created_at" label="申请时间" width="180">
        <template #default="{ row }">
          {{ formatDateTime(row.created_at) }}
        </template>
      </el-table-column>
      <el-table-column prop="reason" label="申请理由" />
      <el-table-column prop="status_display" label="状态" width="120" />
      <el-table-column prop="review_comment" label="审核意见" />
    </el-table>

    <el-dialog
      v-model="showApplyDialog"
      title="申请成为管理员"
      width="500px"
    >
      <el-form :model="form">
        <el-form-item label="申请理由" label-width="80px">
          <el-input
            v-model="form.reason"
            type="textarea"
            :rows="4"
            placeholder="请填写申请理由"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showApplyDialog = false">取 消</el-button>
        <el-button type="primary" :loading="submitting" @click="handleSubmit">
          提 交
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import { getAdminRequests, applyForAdmin } from '@/api/user'

export default {
  name: 'MyAdminRequests',
  setup() {
    const store = useStore()
    const router = useRouter()
    const requests = ref([])
    const showApplyDialog = ref(false)
    const submitting = ref(false)
    const form = ref({
      reason: ''
    })

    const formatDateTime = (dt) => {
      if (!dt) return ''
      return new Date(dt).toLocaleString('zh-CN')
    }

    const handleApprovedIfNeeded = async () => {
      // 如果发现申请已被批准，则自动退出当前前端登录，并跳转到后台管理登录
      if (requests.value.some(r => r.status === 'approved')) {
        ElMessage.success('您的管理员申请已通过，请使用管理员身份登录后台系统')
        await store.dispatch('logout')
        // 跳转到后端 Django admin 登录
        window.location.href = 'http://localhost:8000/admin/'
      }
    }

    const fetchRequests = async () => {
      try {
        const data = await getAdminRequests()
        requests.value = data.results || data
        await handleApprovedIfNeeded()
      } catch (error) {
        ElMessage.error('获取申请记录失败')
      }
    }

    const hasPendingOrApproved = computed(() => {
      return requests.value.some(r => r.status === 'pending' || r.status === 'approved')
    })

    const handleSubmit = async () => {
      if (!form.value.reason) {
        ElMessage.warning('请填写申请理由')
        return
      }
      submitting.value = true
      try {
        await applyForAdmin({ reason: form.value.reason })
        ElMessage.success('申请已提交')
        showApplyDialog.value = false
        form.value.reason = ''
        await fetchRequests()
      } catch (error) {
        let msg = '提交申请失败'
        if (error.response && error.response.data) {
          const data = error.response.data
          if (typeof data === 'string') {
            msg = data
          } else if (data.error) {
            msg = data.error
          } else if (data.detail) {
            msg = data.detail
          }
        }
        ElMessage.error(msg)
      } finally {
        submitting.value = false
      }
    }

    onMounted(() => {
      fetchRequests()
    })

    return {
      requests,
      showApplyDialog,
      submitting,
      form,
      formatDateTime,
      hasPendingOrApproved,
      handleSubmit
    }
  }
}
</script>

<style scoped>
.admin-requests {
  padding: 20px;
}

h2 {
  margin-bottom: 20px;
}

.actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.hint {
  color: #6b7280;
  font-size: 13px;
}
</style>
