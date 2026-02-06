<template>
  <div class="admin-requests">
    <PageHeader />

    <div class="content-section">
      <div class="info-card">
        <div class="info-icon">
          <InfoFilled />
        </div>
        <div class="info-content">
          <h3>管理员权限说明</h3>
          <p>成为管理员后，您将拥有系统管理权限，包括用户管理、教室管理和预约审核等功能。</p>
        </div>
      </div>

      <div class="actions-section">
        <el-button
          type="primary"
          :disabled="hasPendingOrApproved"
          @click="showApplyDialog = true"
          size="large"
        >
          <el-icon><Plus /></el-icon>
          申请成为管理员
        </el-button>
        <div v-if="hasPendingOrApproved" class="hint">
          <el-icon><WarningFilled /></el-icon>
          您已有待审核或已批准的申请，无法重复申请。
        </div>
      </div>

      <div class="requests-table">
        <el-table :data="requests" style="width: 100%" class="modern-table">
          <el-table-column prop="created_at" label="申请时间" width="180">
            <template #default="{ row }">
              {{ formatDateTime(row.created_at) }}
            </template>
          </el-table-column>
          <el-table-column prop="reason" label="申请理由" min-width="200" />
          <el-table-column prop="status_display" label="状态" width="120">
            <template #default="{ row }">
              <el-tag :type="getStatusType(row.status)" size="small">
                {{ row.status_display }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="review_comment" label="审核意见" min-width="150">
            <template #default="{ row }">
              {{ row.review_comment || '-' }}
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>

    <!-- 申请对话框 -->
    <el-dialog
      v-model="showApplyDialog"
      title="申请成为管理员"
      width="90%"
      :style="{ maxWidth: '500px' }"
      class="apply-dialog"
    >
      <el-form :model="form" label-position="top">
        <el-form-item label="申请理由" required>
          <el-input
            v-model="form.reason"
            type="textarea"
            :rows="5"
            placeholder="请详细说明您申请成为管理员的理由，例如：您的技术背景、管理经验、能为系统做出的贡献等..."
            maxlength="500"
            show-word-limit
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="showApplyDialog = false" size="large">取消</el-button>
          <el-button type="primary" :loading="submitting" @click="handleSubmit" size="large">
            提交申请
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { InfoFilled, WarningFilled, Plus } from '@element-plus/icons-vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import { getAdminRequests, applyForAdmin } from '@/api/user'
import PageHeader from '@/components/common/PageHeader.vue'

export default {
  name: 'MyAdminRequests',
  components: { InfoFilled, WarningFilled, Plus, PageHeader },
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
      return new Date(dt).toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      })
    }

    const getStatusType = (status) => {
      const typeMap = {
        pending: 'warning',
        approved: 'success',
        rejected: 'danger'
      }
      return typeMap[status] || 'info'
    }

    const handleApprovedIfNeeded = async () => {
      if (requests.value.some(r => r.status === 'approved')) {
        ElMessage.success('您的管理员申请已通过，请使用管理员身份登录后台系统')
        await store.dispatch('logout')
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
      if (!form.value.reason || form.value.reason.trim().length === 0) {
        ElMessage.warning('请填写申请理由')
        return
      }
      submitting.value = true
      try {
        await applyForAdmin({ reason: form.value.reason.trim() })
        ElMessage.success('申请已提交，请等待管理员审核')
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
      getStatusType,
      hasPendingOrApproved,
      handleSubmit
    }
  }
}
</script>

<style scoped>
.admin-requests {
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

.content-section {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.info-card {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  background: linear-gradient(135deg, #e0f2f1 0%, #b2dfdb 100%);
  border-radius: 16px;
  padding: 24px;
}

.info-icon {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: white;
  border-radius: 12px;
  color: #00897b;
  font-size: 24px;
  flex-shrink: 0;
}

.info-content h3 {
  font-size: 1rem;
  font-weight: 600;
  color: #004d40;
  margin: 0 0 8px;
}

.info-content p {
  font-size: 0.875rem;
  color: #00695c;
  margin: 0;
  line-height: 1.5;
}

.actions-section {
  display: flex;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
}

.hint {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 16px;
  background: #fef3c7;
  border-radius: 10px;
  color: #92400e;
  font-size: 0.875rem;
}

.hint .el-icon {
  font-size: 18px;
}

.requests-table {
  background: white;
  border-radius: 16px;
  border: 1px solid #f3f4f6;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
  overflow: hidden;
}

:deep(.modern-table) {
  border: none;
}

:deep(.modern-table .el-table__header-wrapper) {
  background: #f9fafb;
}

:deep(.modern-table th) {
  background: #f9fafb;
  border-bottom: 1px solid #f3f4f6;
  color: #374151;
  font-weight: 600;
}

:deep(.modern-table td) {
  border-bottom: 1px solid #f3f4f6;
}

:deep(.modern-table tr:last-child td) {
  border-bottom: none;
}

:deep(.modern-table tr:hover td) {
  background: #f9fafb;
}

.dialog-footer {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
}

@media (max-width: 640px) {
  .info-card {
    flex-direction: column;
    text-align: center;
  }

  .info-icon {
    margin: 0 auto;
  }

  .actions-section {
    flex-direction: column;
    align-items: stretch;
  }

  .actions-section .el-button {
    width: 100%;
  }

  .hint {
    justify-content: center;
  }
}
</style>
