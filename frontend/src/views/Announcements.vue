<template>
  <div class="announcements">
    <h2>系统公告</h2>
    
    <el-card v-for="announcement in announcements" :key="announcement.id" class="announcement-card">
      <template #header>
        <div class="card-header">
          <span class="title">{{ announcement.title }}</span>
          <span class="meta">{{ announcement.author_name }} · {{ formatDate(announcement.created_at) }}</span>
        </div>
      </template>
      <div class="content" v-html="announcement.content"></div>
      <el-button type="primary" link @click="viewDetail(announcement.id)">查看详情</el-button>
    </el-card>
    
    <el-empty v-if="announcements.length === 0" description="暂无公告" />
    
    <!-- 公告详情对话框 -->
    <el-dialog v-model="dialogVisible" :title="currentAnnouncement?.title" width="70%">
      <div class="announcement-detail">
        <div class="detail-meta">
          <span>发布人：{{ currentAnnouncement?.author_name }}</span>
          <span>发布时间：{{ formatDateTime(currentAnnouncement?.created_at) }}</span>
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
import { getAnnouncements, getAnnouncementDetail } from '@/api/announcement'

export default {
  name: 'Announcements',
  setup() {
    const announcements = ref([])
    const dialogVisible = ref(false)
    const currentAnnouncement = ref(null)
    
    const formatDate = (dateTime) => {
      if (!dateTime) return ''
      const date = new Date(dateTime)
      return date.toLocaleDateString('zh-CN')
    }
    
    const formatDateTime = (dateTime) => {
      if (!dateTime) return ''
      return new Date(dateTime).toLocaleString('zh-CN')
    }
    
    const fetchAnnouncements = async () => {
      try {
        const data = await getAnnouncements()
        announcements.value = data.results || data
      } catch (error) {
        ElMessage.error('获取公告列表失败')
      }
    }
    
    const viewDetail = async (id) => {
      try {
        const data = await getAnnouncementDetail(id)
        currentAnnouncement.value = data
        dialogVisible.value = true
      } catch (error) {
        ElMessage.error('获取公告详情失败')
      }
    }
    
    onMounted(() => {
      fetchAnnouncements()
    })
    
    return {
      announcements,
      dialogVisible,
      currentAnnouncement,
      formatDate,
      formatDateTime,
      viewDetail
    }
  }
}
</script>

<style scoped>
.announcements {
  padding: 20px;
}

h2 {
  margin-bottom: 20px;
}

.announcement-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.title {
  font-size: 18px;
  font-weight: 600;
  color: #333;
}

.meta {
  font-size: 14px;
  color: #999;
}

.content {
  margin: 15px 0;
  color: #666;
  line-height: 1.6;
  max-height: 100px;
  overflow: hidden;
}

.detail-meta {
  display: flex;
  gap: 30px;
  color: #666;
  font-size: 14px;
}

.detail-content {
  line-height: 1.8;
  color: #333;
}

.detail-content :deep(img) {
  max-width: 100%;
  height: auto;
  margin: 10px 0;
}

.detail-content :deep(video) {
  max-width: 100%;
  height: auto;
  margin: 10px 0;
}
</style>
