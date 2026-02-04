<template>
  <div class="dashboard">
    <h1>欢迎使用教室预约系统</h1>
    <el-row :gutter="20" style="margin-top: 30px">
      <el-col :span="8">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>我的预约</span>
            </div>
          </template>
          <div class="stat-number">{{ myReservationsCount }}</div>
          <el-button type="primary" @click="$router.push('/my-reservations')">查看详情</el-button>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>可用教室</span>
            </div>
          </template>
          <div class="stat-number">{{ availableClassrooms }}</div>
          <el-button type="primary" @click="$router.push('/classrooms')">查看教室</el-button>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>快速预约</span>
            </div>
          </template>
          <div class="stat-number">-</div>
          <el-button type="primary" @click="$router.push('/reservations')">立即预约</el-button>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 30px">
      <el-col :span="24">
        <el-card>
          <template #header>
            <div class="card-header latest-header">
              <span>最新公告</span>
              <span v-if="latestAnnouncement" class="latest-meta">
                {{ latestAnnouncement.title }} · {{ latestAnnouncementTime }}
              </span>
            </div>
          </template>
          <div v-if="latestAnnouncement" class="announcement-content" v-html="latestAnnouncement.content"></div>
          <div v-else class="announcement-empty">暂无公告</div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { getMyReservations } from '@/api/reservation'
import { getAvailableClassrooms } from '@/api/classroom'
import { getLatestAnnouncements, getAnnouncementDetail } from '@/api/announcement'

export default {
  name: 'Dashboard',
  setup() {
    const myReservationsCount = ref(0)
    const availableClassrooms = ref(0)
    const latestAnnouncement = ref(null)
    const latestAnnouncementTime = ref('')
    
    onMounted(async () => {
      try {
        const [reservations, classrooms, latestList] = await Promise.all([
          getMyReservations(),
          getAvailableClassrooms(),
          getLatestAnnouncements()
        ])

        // 只统计未取消的预约
        myReservationsCount.value = (reservations || []).filter(
          item => item.status !== 'cancelled'
        ).length
        availableClassrooms.value = classrooms.length

        if (latestList && latestList.length > 0) {
          const latest = latestList[0]
          const detail = await getAnnouncementDetail(latest.id)
          latestAnnouncement.value = detail
          latestAnnouncementTime.value = new Date(detail.created_at).toLocaleString('zh-CN')
        }
      } catch (error) {
        console.error(error)
      }
    })
    
    return {
      myReservationsCount,
      availableClassrooms,
      latestAnnouncement,
      latestAnnouncementTime
    }
  }
}
</script>

<style scoped>
.dashboard {
  padding: 20px;
}

h1 {
  color: #333;
  margin-bottom: 20px;
}

.stat-number {
  font-size: 48px;
  font-weight: bold;
  color: #409eff;
  text-align: center;
  margin: 20px 0;
}

.card-header {
  font-weight: bold;
}

.latest-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.latest-meta {
  font-size: 12px;
  color: #909399;
}

.announcement-content {
  max-height: 400px;
  overflow: auto;
}

.announcement-content img,
.announcement-content video {
  max-width: 100%;
  height: auto;
  display: block;
}

.announcement-empty {
  text-align: center;
  color: #909399;
  padding: 40px 0;
}
</style>
