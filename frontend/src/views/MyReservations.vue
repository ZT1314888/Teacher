<template>
  <div class="min-h-screen bg-background py-8">
    <PageHeader>
      <template #actions>
        <div class="flex items-center space-x-2 text-sm text-gray-600">
          <UserGroupIcon class="w-5 h-5" />
          <span>{{ userName }}</span>
        </div>
      </template>
    </PageHeader>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="card">
        <div class="border-b border-secondary-200 mb-6">
          <nav class="flex space-x-8" aria-label="Tabs">
            <button
              v-for="tab in tabs"
              :key="tab.value"
              type="button"
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

        <LoadingState v-if="loading" />

        <EmptyState
          v-else-if="filteredReservations.length === 0"
          title="暂无预约记录"
          :description="`您还没有任何${currentTabLabel}的预约`"
          action-text="立即预约"
          @action="router.push('/booking')"
        >
          <template #icon>
            <CalendarIcon class="w-16 h-16 text-gray-300 mx-auto" />
          </template>
        </EmptyState>

        <div v-else class="space-y-4">
          <div
            v-for="reservation in filteredReservations"
            :key="reservation.id"
            class="flex items-center bg-white rounded-xl p-6 shadow-sm hover:shadow-md transition-shadow duration-200"
          >
            <div class="flex-shrink-0 w-20 text-center">
              <div class="text-3xl font-bold text-gray-900">{{ getDay(reservation.date) }}</div>
              <div class="text-sm text-gray-500">{{ getMonth(reservation.date) }}</div>
            </div>

            <div class="flex-1 ml-6">
              <div class="flex items-center justify-between mb-2">
                <h3 class="text-lg font-semibold text-gray-900">{{ reservation.classroom_name }}</h3>
                <ReservationStatusBadge :status="reservation.status" :label="reservation.status_display" />
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
              <p class="text-sm text-gray-500 mt-2 text-ellipsis-2">
                <span class="font-medium">用途：</span>{{ reservation.purpose || '无' }}
              </p>
            </div>

            <div class="flex-shrink-0">
              <button
                v-if="canCancel(reservation)"
                type="button"
                class="btn-danger text-sm"
                @click="handleCancel(reservation)"
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

    <ConfirmDialog
      v-model="showCancelModal"
      title="确认取消预约"
      :subtitle="`${currentReservation?.classroom_name || ''} · ${formatDateTime(currentReservation?.date)}`"
      content="取消后此预约将被释放，其他用户可以预约该时间段。确定要取消吗？"
      confirm-text="确认取消"
      cancel-text="取消"
      @confirm="confirmCancel"
      @cancel="currentReservation = null"
    />
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import { ElMessage } from 'element-plus'
import {
  UserGroupIcon,
  CalendarIcon,
  ClockIcon,
  ExclamationTriangleIcon
} from '@heroicons/vue/24/outline'
import PageHeader from '@/components/common/PageHeader.vue'
import LoadingState from '@/components/common/LoadingState.vue'
import EmptyState from '@/components/common/EmptyState.vue'
import ConfirmDialog from '@/components/common/ConfirmDialog.vue'
import ReservationStatusBadge from '@/components/reservation/ReservationStatusBadge.vue'
import { getMyReservations, cancelReservation } from '@/api/reservation'

const router = useRouter()
const store = useStore()

const loading = ref(false)
const reservations = ref([])
const activeTab = ref('active')
const showCancelModal = ref(false)
const currentReservation = ref(null)

const userName = computed(() => store.state.user?.username || '用户')
const userRole = computed(() => {
  const roleMap = {
    admin: '管理员',
    teacher: '教师',
    student: '学生'
  }
  return roleMap[store.state.user?.role] || '访客'
})

const tabs = computed(() => {
  const tabMap = [
    { label: '进行中', value: 'active' },
    { label: '已完成', value: 'completed' },
    { label: '已取消', value: 'cancelled' }
  ]

  return tabMap.map((tab) => ({
    ...tab,
    count: reservations.value.filter((r) => {
      if (tab.value === 'active') return r.status === 'pending' || r.status === 'approved'
      if (tab.value === 'completed') return r.status === 'approved' && isPast(r)
      if (tab.value === 'cancelled') return r.status === 'cancelled'
      return false
    }).length
  }))
})

const currentTabLabel = computed(() => tabs.value.find((t) => t.value === activeTab.value)?.label || '')

const filteredReservations = computed(() => {
  return reservations.value.filter((r) => {
    if (activeTab.value === 'active') return r.status === 'pending' || r.status === 'approved'
    if (activeTab.value === 'completed') return r.status === 'approved' && isPast(r)
    if (activeTab.value === 'cancelled') return r.status === 'cancelled'
    return false
  })
})

const normalizeList = (payload) => {
  if (Array.isArray(payload)) return payload
  if (Array.isArray(payload?.results)) return payload.results
  if (Array.isArray(payload?.data)) return payload.data
  return []
}

const fetchReservations = async () => {
  loading.value = true
  try {
    const data = await getMyReservations()
    reservations.value = normalizeList(data)
  } catch (error) {
    ElMessage.error('获取预约列表失败')
    reservations.value = []
  } finally {
    loading.value = false
  }
}

const canCancel = (reservation) => {
  if (reservation.status !== 'pending' && reservation.status !== 'approved') return false

  const startTime = new Date(`${reservation.date}T${reservation.start_time}`)
  const now = new Date()
  const hoursUntilStart = (startTime - now) / (1000 * 60 * 60)
  return hoursUntilStart >= 2
}

const cannotCancelReason = (reservation) => {
  if (reservation.status === 'cancelled') return '已取消'
  if (reservation.status === 'rejected') return '已拒绝'

  const startTime = new Date(`${reservation.date}T${reservation.start_time}`)
  const now = new Date()
  const hoursUntilStart = (startTime - now) / (1000 * 60 * 60)
  if (hoursUntilStart < 2) return '开始前2小时内不可取消'

  return null
}

const isPast = (reservation) => {
  const endTime = new Date(`${reservation.date}T${reservation.end_time}`)
  return new Date() > endTime
}

const getDay = (dateStr) => new Date(dateStr).getDate()

const getMonth = (dateStr) => {
  const months = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']
  return months[new Date(dateStr).getMonth()]
}

const formatDateTime = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return `${date.getMonth() + 1}月${date.getDate()}日`
}

const handleCancel = (reservation) => {
  currentReservation.value = reservation
  showCancelModal.value = true
}

const confirmCancel = async () => {
  if (!currentReservation.value) return

  try {
    await cancelReservation(currentReservation.value.id)
    showCancelModal.value = false
    currentReservation.value = null
    await fetchReservations()
    ElMessage.success('预约已取消')
  } catch (error) {
    ElMessage.error('取消预约失败')
  }
}

onMounted(fetchReservations)
</script>
