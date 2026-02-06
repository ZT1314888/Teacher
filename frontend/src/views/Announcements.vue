<template>
  <div class="announcements">
    <PageHeader />

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div v-if="loading" class="text-center py-12">
        <div class="inline-block w-8 h-8 border-4 border-primary border-t-transparent rounded-full animate-spin"></div>
        <p class="mt-4 text-gray-600">加载中...</p>
      </div>

      <div v-else-if="announcements.length === 0" class="empty-state">
        <div class="empty-state-icon">📢</div>
        <div class="empty-state-title">暂无公告</div>
        <div class="empty-state-description">系统暂无新公告发布</div>
      </div>

      <div v-else class="announcements-list">
        <div
          v-for="announcement in announcements"
          :key="announcement.id"
          class="announcement-card"
          @click="viewDetail(announcement.id)"
        >
          <div class="announcement-header">
            <h3 class="announcement-title">{{ announcement.title }}</h3>
            <div class="announcement-meta">
              <span class="announcement-author">
                <el-icon><User /></el-icon>
                {{ announcement.author_name }}
              </span>
              <span class="announcement-date">{{ formatDate(announcement.created_at) }}</span>
            </div>
          </div>
          <div class="announcement-preview" v-html="getPreview(announcement.content)"></div>
          <div class="announcement-footer">
            <el-button type="primary" link>
              查看详情 <el-icon><ArrowRight /></el-icon>
            </el-button>
          </div>
        </div>
      </div>
    </div>

    <!-- 公告详情对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="currentAnnouncement?.title"
      width="90%"
      :style="{ maxWidth: '800px' }"
      class="announcement-dialog"
    >
      <div class="announcement-detail">
        <div class="detail-meta">
          <span class="meta-item">
            <el-icon><User /></el-icon>
            发布人：{{ currentAnnouncement?.author_name }}
          </span>
          <span class="meta-item">
            <el-icon><Calendar /></el-icon>
            发布时间：{{ formatDateTime(currentAnnouncement?.created_at) }}
          </span>
        </div>
        <el-divider />
        <div class="detail-content" v-html="currentAnnouncement?.content"></div>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { User, ArrowRight, Calendar } from '@element-plus/icons-vue'
import { getAnnouncements, getAnnouncementDetail } from '@/api/announcement'
import { markAnnouncementRead } from '@/api/notification'
import PageHeader from '@/components/common/PageHeader.vue'

export default {
  name: 'Announcements',
  components: { User, ArrowRight, Calendar, PageHeader },
  setup() {
    const loading = ref(false)
    const announcements = ref([])
    const dialogVisible = ref(false)
    const currentAnnouncement = ref(null)
    const viewedAnnouncementIds = ref(new Set())

    const formatDate = (dateTime) => {
      if (!dateTime) return ''
      const date = new Date(dateTime)
      return date.toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit'
      })
    }

    const formatDateTime = (dateTime) => {
      if (!dateTime) return ''
      return new Date(dateTime).toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      })
    }

    const getPreview = (content) => {
      if (!content) return ''
      // 移除HTML标签并截取前150个字符
      const text = content.replace(/<[^>]*>/g, '')
      return text.length > 150 ? text.substring(0, 150) + '...' : text
    }

    const fetchAnnouncements = async () => {
      loading.value = true
      try {
        const data = await getAnnouncements()
        announcements.value = data.results || data
      } catch (error) {
        ElMessage.error('获取公告列表失败')
      } finally {
        loading.value = false
      }
    }

    const viewDetail = async (id) => {
      try {
        const data = await getAnnouncementDetail(id)
        currentAnnouncement.value = data
        dialogVisible.value = true

        // 已查看公告后只减少一条对应未读通知
        if (!viewedAnnouncementIds.value.has(id)) {
          viewedAnnouncementIds.value.add(id)
          await markAnnouncementRead(id).catch(() => {})
          window.dispatchEvent(new Event('notification:changed'))
        }
      } catch (error) {
        ElMessage.error('获取公告详情失败')
      }
    }

    onMounted(() => {
      fetchAnnouncements()
    })

    return {
      loading,
      announcements,
      dialogVisible,
      currentAnnouncement,
      formatDate,
      formatDateTime,
      getPreview,
      viewDetail
    }
  }
}
</script>

<style scoped>
.announcements {
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

.announcements-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.announcement-card {
  background: white;
  border-radius: 16px;
  border: 1px solid #f3f4f6;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
  padding: 24px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.announcement-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  transform: translateY(-2px);
  border-color: #e0f2f1;
}

.announcement-header {
  margin-bottom: 16px;
}

.announcement-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 8px;
}

.announcement-meta {
  display: flex;
  align-items: center;
  gap: 16px;
  font-size: 0.875rem;
}

.announcement-author,
.announcement-date {
  display: flex;
  align-items: center;
  gap: 4px;
  color: #6b7280;
}

.announcement-author .el-icon,
.announcement-date .el-icon {
  font-size: 16px;
}

.announcement-preview {
  color: #4b5563;
  line-height: 1.75;
  margin-bottom: 16px;
  max-height: 100px;
  overflow: hidden;
}

.announcement-footer {
  display: flex;
  justify-content: flex-end;
}

.announcement-footer .el-button {
  display: flex;
  align-items: center;
  gap: 4px;
  font-weight: 500;
}

.detail-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 24px;
  color: #6b7280;
  font-size: 0.875rem;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 6px;
}

.detail-content {
  line-height: 1.8;
  color: #1f2937;
}

.detail-content :deep(img),
.detail-content :deep(video) {
  max-width: 100%;
  height: auto;
  margin: 16px 0;
  border-radius: 8px;
}

.detail-content :deep(p) {
  margin-bottom: 16px;
}

.detail-content :deep(h1),
.detail-content :deep(h2),
.detail-content :deep(h3) {
  margin-top: 24px;
  margin-bottom: 16px;
  font-weight: 600;
}

.detail-content :deep(ul),
.detail-content :deep(ol) {
  margin-left: 24px;
  margin-bottom: 16px;
}

.detail-content :deep(li) {
  margin-bottom: 8px;
}

.empty-state {
  text-align: center;
  padding: 48px 24px;
}

.empty-state-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.empty-state-title {
  font-size: 1rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 8px;
}

.empty-state-description {
  font-size: 0.875rem;
  color: #6b7280;
}
</style>
