<template>
  <div class="min-h-screen bg-secondary-50 py-8">
    <!-- 页面头部 -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mb-8">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-3xl font-bold text-gray-900">欢迎回来，{{ userName }}</h1>
          <p class="mt-2 text-gray-600">{{ userRole }} · 个人中心</p>
        </div>
        <div class="flex items-center space-x-4">
          <div class="flex items-center space-x-2 text-sm text-gray-600">
            <UserGroupIcon class="w-5 h-5" />
            <span>{{ userName }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 主内容区 -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="card">
        <!-- Tabs 标签页 -->
        <div class="border-b border-secondary-200 mb-6">
          <nav class="flex space-x-8" aria-label="Tabs">
            <button
              v-for="tab in tabs"
              :key="tab.value"
              @click="activeTab = tab.value"
              :class="[
                'whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm transition-colors',
                activeTab === tab.value
                  ? 'border-primary text-primary'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              ]"
            >
              {{ tab.label }}
              <span
                v-if="tab.count > 0"
                class="ml-2 py-0.5 px-2 rounded-full text-xs"
                :class="activeTab === tab.value ? 'bg-primary text-white' : 'bg-gray-100 text-gray-600'"
              >
                {{ tab.count }}
              </span>
            </button>
          </nav>
        </div>

        <!-- 预约列表 -->
        <div v-if="loading" class="text-center py-12">
          <div class="inline-block w-8 h-8 border-4 border-primary border-t-transparent rounded-full animate-spin"></div>
          <p class="mt-4 text-gray-600">加载中...</p>
        </div>

        <div v-else-if="filteredReservations.length === 0" class="text-center py-12">
          <CalendarIcon class="w-16 h-16 text-gray-300 mx-auto mb-4" />
          <h3 class="text-lg font-medium text-gray-900 mb-2">暂无预约记录</h3>
          <p class="text-gray-500 mb-6">您还没有任何{{ currentTabLabel }}的预约</p>
          <router-link to="/booking" class="btn-primary inline-block">
            立即预约
          </router-link>
        </div>

        <div v-else class="space-y-4">
          <div
            v-for="reservation in filteredReservations"
            :key="reservation.id"
            class="flex items-center bg-white rounded-xl p-6 shadow-sm hover:shadow-md transition-shadow duration-200"
          >
            <!-- 日期块 -->
            <div class="flex-shrink-0 w-20 text-center">
              <div class="text-3xl font-bold text-gray-900">
                {{ getDay(reservation.date) }}
              </div>
              <div class="text-sm text-gray-500">
                {{ getMonth(reservation.date) }}
              </div>
            </div>

            <!-- 预约信息 -->
            <div class="flex-1 ml-6">
              <div class="flex items-center justify-between mb-2">
                <h3 class="text-lg font-semibold text-gray-900">
                  {{ reservation.classroom_name }}
                </h3>
                <span
                  :class="[
                    'badge',
                    getStatusBadgeClass(reservation.status)
                  ]"
                >
                  {{ reservation.status_display }}
                </span>
              </div>
              <div class="flex items-center space-x-6 text-sm text-gray-600">
                <div class="flex items-center space-x-2">
                  <ClockIcon class="w-4 h-4" />
                  <span>{{ reservation.start_time }} - {{ reservation.end_time }}</span>
                </div>
                <div class="flex items-center space-x-2">
                  <UserGroupIcon class="w-4 h-4" />
                  <span>{{ reservation.participant_count || 0 }}人</span>
                </div>
              </div>
              <p class="text-sm text-gray-500 mt-2 line-clamp-2">
                <span class="font-medium">用途：</span>{{ reservation.purpose || '无' }}
              </p>
            </div>

            <!-- 操作区 -->
            <div class="flex-shrink-0">
              <button
                v-if="canCancel(reservation)"
                @click="handleCancel(reservation)"
                class="btn-danger text-sm"
              >
                取消预约
              </button>
              <div v-else-if="cannotCancelReason(reservation)" class="text-sm text-gray-400">
                <span class="flex items-center space-x-1">
                  <ExclamationTriangleIcon class="w-4 h-4" />
                  <span>{{ cannotCancelReason(reservation) }}</span>
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 取消确认对话框 -->
    <div v-if="showCancelModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-2xl p-8 max-w-md w-full mx-4">
        <div class="flex items-center space-x-3 mb-6">
          <div class="w-12 h-12 rounded-full bg-warning-light flex items-center justify-center">
            <ExclamationTriangleIcon class="w-6 h-6 text-warning-dark" />
          </div>
          <div>
            <h3 class="text-lg font-semibold text-gray-900">确认取消预约</h3>
            <p class="text-sm text-gray-500 mt-1">
              {{ currentReservation?.classroom_name }} · {{ formatDateTime(currentReservation?.date) }}
            </p>
          </div>
        </div>

        <div class="mb-6">
          <p class="text-sm text-gray-600">
            取消后此预约将被释放，其他用户可以预约该时间段。确定要取消吗？
          </p>
        </div>

        <div class="flex space-x-3">
          <button @click="showCancelModal = false" class="btn-secondary flex-1">
            取消
          </button>
          <button @click="confirmCancel" class="btn-danger flex-1">
            确认取消
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { UserGroupIcon, CalendarIcon, ClockIcon, ExclamationTriangleIcon } from '@heroicons/vue/24/outline'

// 响应式数据
const loading = ref(false)
const reservations = ref([])
const activeTab = ref('active')
const showCancelModal = ref(false)
const currentReservation = ref(null)

// 用户信息（模拟数据，实际应从 store 获取）
const userName = ref('张三')
const userRole = ref('学生')

// 标签页
const tabs = computed(() => {
  const tabMap = {
    active: { label: '进行中', value: 'active' },
    completed: { label: '已完成', value: 'completed' },
    cancelled: { label: '已取消', value: 'cancelled' }
  }
  return Object.values(tabMap).map(tab => ({
    ...tab,
    count: reservations.value.filter(r => {
      if (tab.value === 'active') return r.status === 'pending' || r.status === 'approved'
      if (tab.value === 'completed') return r.status === 'approved' && isPast(reservation)
      if (tab.value === 'cancelled') return r.status === 'cancelled'
      return false
    }).length
  }))
})

// 当前标签页标签
const currentTabLabel = computed(() => {
  return tabs.value.find(t => t.value === activeTab.value)?.label || ''
})

// 筛选后的预约列表
const filteredReservations = computed(() => {
  return reservations.value.filter(r => {
    if (activeTab.value === 'active') return r.status === 'pending' || r.status === 'approved'
    if (activeTab.value === 'completed') return r.status === 'approved' && isPast(r)
    if (activeTab.value === 'cancelled') return r.status === 'cancelled'
    return false
  })
})

// 获取预约列表
const fetchReservations = async () => {
  loading.value = true
  try {
    // TODO: 调用 API 获取预约列表
    // const data = await getMyReservations()
    // reservations.value = data

    // 模拟数据
    reservations.value = [
      {
        id: 1,
        classroom_name: 'A-101多媒体教室',
        date: '2026-02-10',
        start_time: '08:00',
        end_time: '10:00',
        purpose: '计算机网络课程教学',
        status: 'pending',
        status_display: '待审核',
        participant_count: 50,
        created_at: '2026-02-05T10:30:00Z'
      },
      {
        id: 2,
        classroom_name: 'C-301普通教室',
        date: '2026-02-08',
        start_time: '14:00',
        end_time: '16:00',
        purpose: '学术研讨会',
        status: 'approved',
        status_display: '已通过',
        participant_count: 30,
        created_at: '2026-02-04T15:20:00Z'
      },
      {
        id: 3,
        classroom_name: 'A-102多媒体教室',
        date: '2026-02-06',
        start_time: '19:00',
        end_time: '21:00',
        purpose: '社团活动',
        status: 'cancelled',
        status_display: '已取消',
        participant_count: 25,
        created_at: '2026-02-03T09:15:00Z'
      },
      {
        id: 4,
        classroom_name: 'D-101会议室',
        date: '2026-02-15',
        start_time: '10:00',
        end_time: '12:00',
        purpose: '项目讨论',
        status: 'approved',
        status_display: '已通过',
        participant_count: 15,
        created_at: '2026-02-05T14:00:00Z'
      }
    ]
  } catch (error) {
    console.error('获取预约列表失败:', error)
  } finally {
    loading.value = false
  }
}

// 状态徽章样式
const getStatusBadgeClass = (status) => {
  const classMap = {
    pending: 'badge-warning',
    approved: 'badge-success',
    rejected: 'badge-danger',
    cancelled: 'bg-gray-100 text-gray-500'
  }
  return classMap[status] || 'bg-gray-100 text-gray-500'
}

// 是否可以取消
const canCancel = (reservation) => {
  if (reservation.status !== 'pending' && reservation.status !== 'approved') {
    return false
  }
  // 检查是否在开始前2小时内
  const startTime = new Date(`${reservation.date}T${reservation.start_time}`)
  const now = new Date()
  const hoursUntilStart = (startTime - now) / (1000 * 60 * 60)
  return hoursUntilStart >= 2
}

// 不能取消的原因
const cannotCancelReason = (reservation) => {
  if (reservation.status === 'cancelled') return '已取消'
  if (reservation.status === 'rejected') return '已拒绝'

  const startTime = new Date(`${reservation.date}T${reservation.start_time}`)
  const now = new Date()
  const hoursUntilStart = (startTime - now) / (1000 * 60 * 60)
  if (hoursUntilStart < 2) {
    return '开始前1小时内不可取消'
  }
  return null
}

// 检查预约是否已过期
const isPast = (reservation) => {
  const endTime = new Date(`${reservation.date}T${reservation.end_time}`)
  return new Date() > endTime
}

// 日期格式化
const getDay = (dateStr) => {
  const date = new Date(dateStr)
  return date.getDate()
}

const getMonth = (dateStr) => {
  const date = new Date(dateStr)
  const months = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']
  return months[date.getMonth()]
}

const formatDateTime = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return `${date.getMonth() + 1}月${date.getDate()}日`
}

// 取消预约
const handleCancel = (reservation) => {
  currentReservation.value = reservation
  showCancelModal.value = true
}

const confirmCancel = async () => {
  try {
    // TODO: 调用 API 取消预约
    // await cancelReservation(currentReservation.value.id)

    // 模拟取消
    const index = reservations.value.findIndex(r => r.id === currentReservation.value.id)
    if (index !== -1) {
      reservations.value[index].status = 'cancelled'
      reservations.value[index].status_display = '已取消'
    }

    showCancelModal.value = false
    currentReservation.value = null

    // 显示成功提示
    alert('预约已取消')
  } catch (error) {
    console.error('取消预约失败:', error)
    alert('取消预约失败')
  }
}

onMounted(() => {
  fetchReservations()
})
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
