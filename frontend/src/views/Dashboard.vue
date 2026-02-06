<template>
  <div class="db-dashboard">
    <PageHeader>
      <template #actions>
        <el-tag type="info" effect="light" size="large" class="db-user-chip">
          {{ user?.username || '用户' }}
        </el-tag>
      </template>
    </PageHeader>

    <el-row :gutter="24" class="db-stats-row">
      <el-col :xs="24" :sm="12" :lg="8">
        <div class="db-stat-card">
          <div class="db-stat-icon db-stat-icon-primary">
            <Calendar />
          </div>
          <div class="db-stat-content">
            <div class="db-stat-value">{{ myReservationsCount }}</div>
            <div class="db-stat-label">我的预约</div>
            <div class="db-stat-change positive" v-if="myReservationsCount > 0">
              进行中的预约
            </div>
          </div>
        </div>
      </el-col>
      <el-col :xs="24" :sm="12" :lg="8">
        <div class="db-stat-card">
          <div class="db-stat-icon db-stat-icon-success">
            <School />
          </div>
          <div class="db-stat-content">
            <div class="db-stat-value">{{ availableClassrooms }}</div>
            <div class="db-stat-label">可用教室</div>
            <el-button type="primary" link @click="$router.push('/classrooms')">
              查看全部 →
            </el-button>
          </div>
        </div>
      </el-col>
      <el-col :xs="24" :sm="12" :lg="8">
        <div class="db-stat-card">
          <div class="db-stat-icon db-stat-icon-accent">
            <Bell />
          </div>
          <div class="db-stat-content">
            <div class="db-stat-value">{{ announcementCount }}</div>
            <div class="db-stat-label">最新公告</div>
            <el-button type="primary" link @click="$router.push('/announcements')">
              查看详情 →
            </el-button>
          </div>
        </div>
      </el-col>
    </el-row>

    <el-row :gutter="24" class="db-content-row">
      <el-col :xs="24" :lg="16">
        <div class="db-card">
          <div class="db-card-header">
            <h3>
              <el-icon><Bell /></el-icon>
              最新公告
            </h3>
            <el-button type="primary" link @click="$router.push('/announcements')">
              查看全部
            </el-button>
          </div>
          <div v-if="latestAnnouncement" class="db-announcement-content">
            <div class="db-announcement-meta">
              <span class="db-announcement-title">{{ latestAnnouncement.title }}</span>
              <span class="db-announcement-time">{{ latestAnnouncementTime }}</span>
            </div>
            <div class="db-announcement-body" v-html="latestAnnouncement.content"></div>
          </div>
          <div v-else class="db-empty-state">
            <div class="db-empty-state-icon">📢</div>
            <div class="db-empty-state-title">暂无公告</div>
            <div class="db-empty-state-description">系统暂无新公告发布</div>
          </div>
        </div>
      </el-col>
      <el-col :xs="24" :lg="8">
        <div class="db-card">
          <div class="db-card-header">
            <h3>
              <el-icon><Lightning /></el-icon>
              快速操作
            </h3>
          </div>
          <div class="db-quick-actions">
            <el-button class="db-quick-action-btn" @click="$router.push('/booking')">
              <el-icon><Calendar /></el-icon>
              <span>预约教室</span>
            </el-button>
            <el-button class="db-quick-action-btn" @click="$router.push('/classrooms')">
              <el-icon><School /></el-icon>
              <span>浏览教室</span>
            </el-button>
            <el-button class="db-quick-action-btn" @click="$router.push('/my-reservations')">
              <el-icon><List /></el-icon>
              <span>我的预约</span>
            </el-button>
          </div>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useStore } from 'vuex'
import { getMyReservations } from '@/api/reservation'
import { getAvailableClassrooms } from '@/api/classroom'
import { getLatestAnnouncements, getAnnouncementDetail } from '@/api/announcement'
import { Calendar, School, Bell, Lightning, List } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import PageHeader from '@/components/common/PageHeader.vue'

export default {
  name: 'Dashboard',
  components: { Calendar, School, Bell, Lightning, List, PageHeader },
  setup() {
    const store = useStore()
    const myReservationsCount = ref(0)
    const availableClassrooms = ref(0)
    const announcementCount = ref(0)
    const latestAnnouncement = ref(null)
    const latestAnnouncementTime = ref('')

    const user = computed(() => store.state.user)

    const toList = (payload) => {
      if (Array.isArray(payload)) return payload
      if (Array.isArray(payload?.results)) return payload.results
      if (Array.isArray(payload?.data)) return payload.data
      return []
    }

    onMounted(async () => {
      const [reservationsRes, classroomsRes, latestRes] = await Promise.allSettled([
        getMyReservations(),
        getAvailableClassrooms(),
        getLatestAnnouncements()
      ])

      if (reservationsRes.status === 'fulfilled') {
        const reservations = toList(reservationsRes.value)
        myReservationsCount.value = reservations.filter(
          (item) => item.status === 'pending' || item.status === 'approved'
        ).length
      }

      if (classroomsRes.status === 'fulfilled') {
        const classrooms = toList(classroomsRes.value)
        availableClassrooms.value = classrooms.length
      }

      if (latestRes.status === 'fulfilled') {
        const latestList = toList(latestRes.value)
        announcementCount.value = latestList.length

        if (latestList.length > 0) {
          const latest = latestList[0]
          try {
            const detail = await getAnnouncementDetail(latest.id)
            latestAnnouncement.value = detail
            if (detail?.created_at) {
              latestAnnouncementTime.value = new Date(detail.created_at).toLocaleString('zh-CN', {
                year: 'numeric',
                month: '2-digit',
                day: '2-digit',
                hour: '2-digit',
                minute: '2-digit'
              })
            }
          } catch (error) {
            // 详情获取失败时退化为列表首条，避免整个卡片空白
            latestAnnouncement.value = latest
          }
        }
      }

      if (
        reservationsRes.status === 'rejected' &&
        classroomsRes.status === 'rejected' &&
        latestRes.status === 'rejected'
      ) {
        ElMessage.error('首页数据加载失败')
      }
    })

    return {
      user,
      myReservationsCount,
      availableClassrooms,
      announcementCount,
      latestAnnouncement,
      latestAnnouncementTime
    }
  }
}
</script>

<style scoped>
.db-dashboard {
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

.db-user-chip {
  border-radius: 999px;
  border: 1px solid #d5ece8;
  color: #0f766e;
}

.db-stats-row {
  margin-bottom: 24px;
}

.db-stat-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 24px;
  background: white;
  border-radius: 16px;
  border: 1px solid #f3f4f6;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  height: 100%;
}

.db-stat-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  transform: translateY(-2px);
}

.db-stat-icon {
  width: 56px;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 14px;
  font-size: 24px;
  flex-shrink: 0;
}

.db-stat-icon-primary {
  background: linear-gradient(135deg, #00897b 0%, #00796b 100%);
  color: white;
}

.db-stat-icon-success {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
}

.db-stat-icon-accent {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  color: white;
}

.db-stat-content {
  flex: 1;
  min-width: 0;
}

.db-stat-value {
  font-size: 28px;
  font-weight: 700;
  color: #1f2937;
  line-height: 1;
}

.db-stat-label {
  font-size: 0.875rem;
  color: #6b7280;
  margin-top: 4px;
  font-weight: 500;
}

.db-stat-change {
  margin-top: 8px;
}

.db-stat-change.positive {
  color: #059669;
  font-weight: 500;
}

.db-content-row {
  margin-top: 24px;
}

.db-card {
  background: white;
  border-radius: 16px;
  border: 1px solid #f3f4f6;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
  overflow: hidden;
}

.db-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  border-bottom: 1px solid #f3f4f6;
}

.db-card-header h3 {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
  color: #1f2937;
}

.db-announcement-content {
  padding: 24px;
}

.db-announcement-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
  padding-bottom: 16px;
  border-bottom: 1px solid #f3f4f6;
}

.db-announcement-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1f2937;
}

.db-announcement-time {
  font-size: 0.875rem;
  color: #9ca3af;
}

.db-announcement-body {
  color: #4b5563;
  line-height: 1.75;
  max-height: 300px;
  overflow-y: auto;
}

.db-announcement-body img,
.db-announcement-body video {
  max-width: 100%;
  height: auto;
  display: block;
  margin: 16px 0;
  border-radius: 8px;
}

.db-quick-actions {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 24px;
}

.db-quick-action-btn {
  width: 100% !important;
  min-height: 52px;
  margin: 0 !important;
  padding: 12px 16px;
  display: flex;
  align-items: center;
  justify-content: flex-start;
  gap: 10px;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
  background: white;
  color: #374151;
  font-weight: 500;
  transition: all 0.2s ease;
  height: auto;
}

.db-quick-action-btn:hover {
  border-color: #00897b;
  color: #00897b;
  background: #e0f2f1;
  transform: translateX(4px);
}

.db-quick-action-btn .el-icon {
  font-size: 20px;
  flex: 0 0 20px;
}

.db-quick-action-btn span {
  flex: 1;
  text-align: center;
}

.db-quick-actions :deep(.el-button + .el-button) {
  margin-left: 0;
}

.db-quick-actions :deep(.el-button) {
  width: 100%;
}

.db-empty-state {
  padding: 48px 24px;
  text-align: center;
}

.db-empty-state-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.db-empty-state-title {
  font-size: 1rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 8px;
}

.db-empty-state-description {
  font-size: 0.875rem;
  color: #6b7280;
}

@media (max-width: 768px) {
  .db-stat-card {
    flex-direction: column;
    text-align: center;
  }

  .db-stat-icon {
    width: 48px;
    height: 48px;
    font-size: 20px;
  }

  .db-stat-value {
    font-size: 24px;
  }

  .db-card-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
}
</style>
