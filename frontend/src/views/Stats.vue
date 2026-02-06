<template>
  <div class="stats-page">
    <PageHeader>
      <template #actions>
        <el-button type="primary" plain @click="refreshAll" :loading="refreshing">
          {{ refreshing ? '刷新中...' : '刷新数据' }}
        </el-button>
      </template>
    </PageHeader>

    <div class="stats-content max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <el-row :gutter="16" class="stats-kpi-layout">
        <el-col :xs="24" :lg="16">
          <div class="kpi-grid kpi-grid-left">
            <template v-if="loadingDashboard">
              <div v-for="idx in 3" :key="`left-skeleton-${idx}`" class="kpi-skeleton"></div>
            </template>
            <template v-else>
              <StatCard
                :value="dashboard.total_classrooms"
                label="教室总数"
                trend="资源规模"
                trend-type="neutral"
                hint="系统内登记教室数量"
              >
                <template #icon><el-icon><School /></el-icon></template>
              </StatCard>
              <StatCard
                :value="dashboard.available_classrooms"
                label="可用教室"
                :trend="`可用率 ${availabilityRate}%`"
                trend-type="positive"
                hint="当前可预约的教室数量"
              >
                <template #icon><el-icon><OfficeBuilding /></el-icon></template>
              </StatCard>
              <StatCard
                :value="dashboard.total_reservations"
                label="预约总数"
                trend="累计预约"
                trend-type="neutral"
                hint="按当前权限范围统计"
              >
                <template #icon><el-icon><DataAnalysis /></el-icon></template>
              </StatCard>
            </template>
          </div>
        </el-col>

        <el-col :xs="24" :lg="8">
          <div class="kpi-grid kpi-grid-right">
            <template v-if="loadingDashboard">
              <div v-for="idx in 2" :key="`right-skeleton-${idx}`" class="kpi-skeleton"></div>
            </template>
            <template v-else>
              <StatCard
                :value="dashboard.pending_reservations"
                label="待审核"
                :trend="`占比 ${pendingRate}%`"
                :trend-type="dashboard.pending_reservations > 0 ? 'negative' : 'positive'"
                hint="待管理员处理预约"
              >
                <template #icon><el-icon><Bell /></el-icon></template>
              </StatCard>
              <StatCard
                :value="dashboard.approved_reservations"
                label="已通过"
                :trend="`通过率 ${approvedRate}%`"
                trend-type="positive"
                hint="审核通过预约数量"
              >
                <template #icon><el-icon><Calendar /></el-icon></template>
              </StatCard>
            </template>
          </div>
        </el-col>
      </el-row>

      <el-row :gutter="16" class="stats-main-row">
        <el-col :xs="24" :lg="16">
          <StatsDailyTable
            :rows="dailySummary"
            :loading="loadingDailySummary"
            :error="dailySummaryError"
          />
        </el-col>

        <el-col :xs="24" :lg="8">
          <StatsTopClassrooms
            :rows="classroomUsage"
            :loading="loadingClassroomUsage"
            :error="classroomUsageError"
          />
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { School, Calendar, Bell, DataAnalysis, OfficeBuilding } from '@element-plus/icons-vue'
import StatCard from '@/components/StatCard.vue'
import PageHeader from '@/components/common/PageHeader.vue'
import StatsDailyTable from '@/components/stats/StatsDailyTable.vue'
import StatsTopClassrooms from '@/components/stats/StatsTopClassrooms.vue'
import { getClassroomUsage, getDailySummary, getDashboardStats } from '@/api/stats'

const dashboard = ref({
  total_classrooms: 0,
  available_classrooms: 0,
  total_reservations: 0,
  pending_reservations: 0,
  approved_reservations: 0
})

const dailySummary = ref([])
const classroomUsage = ref([])
const refreshing = ref(false)

const loadingDashboard = ref(false)
const loadingDailySummary = ref(false)
const loadingClassroomUsage = ref(false)

const dailySummaryError = ref('')
const classroomUsageError = ref('')
let statsPollTimer = null

const toList = (payload) => {
  if (Array.isArray(payload)) return payload
  if (Array.isArray(payload?.results)) return payload.results
  if (Array.isArray(payload?.rows)) return payload.rows
  if (Array.isArray(payload?.data)) return payload.data
  return []
}

const availabilityRate = computed(() => {
  if (!dashboard.value.total_classrooms) return 0
  return Math.round((dashboard.value.available_classrooms / dashboard.value.total_classrooms) * 100)
})

const pendingRate = computed(() => {
  if (!dashboard.value.total_reservations) return 0
  return Math.round((dashboard.value.pending_reservations / dashboard.value.total_reservations) * 100)
})

const approvedRate = computed(() => {
  if (!dashboard.value.total_reservations) return 0
  return Math.round((dashboard.value.approved_reservations / dashboard.value.total_reservations) * 100)
})

const fetchDashboard = async () => {
  loadingDashboard.value = true
  try {
    const data = await getDashboardStats()
    dashboard.value = {
      total_classrooms: Number(data?.total_classrooms || 0),
      available_classrooms: Number(data?.available_classrooms || 0),
      total_reservations: Number(data?.total_reservations || 0),
      pending_reservations: Number(data?.pending_reservations || 0),
      approved_reservations: Number(data?.approved_reservations || 0)
    }
    return true
  } catch (error) {
    return false
  } finally {
    loadingDashboard.value = false
  }
}

const fetchDailySummary = async () => {
  loadingDailySummary.value = true
  dailySummaryError.value = ''
  try {
    const data = await getDailySummary()
    dailySummary.value = toList(data)
    return true
  } catch (error) {
    dailySummary.value = []
    dailySummaryError.value = '趋势数据加载失败，请稍后重试'
    return false
  } finally {
    loadingDailySummary.value = false
  }
}

const fetchClassroomUsage = async () => {
  loadingClassroomUsage.value = true
  classroomUsageError.value = ''
  try {
    const data = await getClassroomUsage()
    classroomUsage.value = toList(data)
    return true
  } catch (error) {
    classroomUsage.value = []
    classroomUsageError.value = '热门教室数据加载失败，请稍后重试'
    return false
  } finally {
    loadingClassroomUsage.value = false
  }
}

const refreshAll = async (silent = false) => {
  refreshing.value = true
  const results = await Promise.allSettled([
    fetchDashboard(),
    fetchDailySummary(),
    fetchClassroomUsage()
  ])

  const successCount = results.filter((item) => item.status === 'fulfilled' && item.value).length
  const failedCount = results.length - successCount

  if (!silent) {
    if (failedCount === results.length) {
      ElMessage.error('统计数据加载失败')
    } else if (failedCount > 0) {
      ElMessage.warning('部分统计模块加载失败，页面已显示可用数据')
    }
  }
  refreshing.value = false
}

const handleWindowFocus = () => {
  refreshAll(true)
}

onMounted(() => {
  refreshAll()
  statsPollTimer = window.setInterval(() => {
    refreshAll(true)
  }, 10000)
  window.addEventListener('focus', handleWindowFocus)
})

onUnmounted(() => {
  if (statsPollTimer) {
    window.clearInterval(statsPollTimer)
    statsPollTimer = null
  }
  window.removeEventListener('focus', handleWindowFocus)
})
</script>

<style scoped>
.stats-page {
  width: 100%;
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

.stats-content {
  display: grid;
  gap: 16px;
}

.kpi-skeleton {
  height: 124px;
  border-radius: 14px;
  background: linear-gradient(90deg, #f1f5f9 20%, #e2e8f0 45%, #f1f5f9 70%);
  background-size: 200% 100%;
  animation: shimmer 1.2s linear infinite;
}

.stats-kpi-layout {
  margin-bottom: 0;
}

.kpi-grid {
  display: grid;
  gap: 16px;
}

.kpi-grid-left {
  grid-template-columns: repeat(3, minmax(0, 1fr));
}

.kpi-grid-right {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.stats-main-row {
  margin-top: 0;
}

@media (max-width: 1200px) {
  .kpi-grid-left {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 992px) {
  .kpi-grid-left,
  .kpi-grid-right {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 768px) {
  .kpi-grid-left,
  .kpi-grid-right {
    grid-template-columns: 1fr;
  }
}

@keyframes shimmer {
  from {
    background-position: 200% 0;
  }
  to {
    background-position: -200% 0;
  }
}
</style>
