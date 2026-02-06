<template>
  <div class="min-h-screen bg-secondary-50 py-8">
    <PageHeader>
      <template #actions>
        <div class="flex items-center flex-wrap gap-4">
          <div class="flex items-center space-x-2 text-sm text-gray-600">
            <span class="w-2 h-2 bg-success rounded-full"></span>
            <span>可用</span>
          </div>
          <div class="flex items-center space-x-2 text-sm text-gray-600">
            <span class="w-2 h-2 bg-primary rounded-full"></span>
            <span>已选</span>
          </div>
          <div class="flex items-center space-x-2 text-sm text-gray-600">
            <span class="w-2 h-2 bg-secondary-300 rounded-full"></span>
            <span>已占用</span>
          </div>
        </div>
      </template>
    </PageHeader>

    <!-- 主内容区 -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="grid grid-cols-1 lg:grid-cols-4 gap-8">

        <!-- 左侧进度栏 -->
        <div class="lg:col-span-1">
          <div class="card sticky top-8">
            <!-- 步骤进度 -->
            <div class="mb-8">
              <h3 class="text-lg font-semibold text-gray-900 mb-6">预约进度</h3>

              <!-- 步骤 1 -->
              <div class="flex items-start mb-6">
                <div class="flex-shrink-0">
                  <div
                    class="w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium transition-all"
                    :class="getStepCircleClass(1)"
                  >
                    {{ isStepCompleted(1) ? '✓' : '1' }}
                  </div>
                </div>
                <div class="ml-4">
                  <p class="text-sm font-medium" :class="getStepTitleClass(1)">选择教室类型</p>
                  <p class="text-xs mt-1" :class="getStepDescClass(1)">
                    {{ selectedClassroomTypeLabel || '请选择教室类型' }}
                  </p>
                </div>
              </div>

              <!-- 步骤 2 -->
              <div class="flex items-start mb-6">
                <div class="flex-shrink-0">
                  <div
                    class="w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium transition-all"
                    :class="getStepCircleClass(2)"
                  >
                    {{ isStepCompleted(2) ? '✓' : '2' }}
                  </div>
                </div>
                <div class="ml-4">
                  <p class="text-sm font-medium" :class="getStepTitleClass(2)">选择日期与时间</p>
                  <p class="text-xs mt-1" :class="getStepDescClass(2)">
                    {{ selectedDate && selectedTimeSlot ? `${formatDate(selectedDate)} ${selectedTimeSlot.time}` : '请选择日期与时间' }}
                  </p>
                </div>
              </div>

              <!-- 步骤 3 -->
              <div class="flex items-start">
                <div class="flex-shrink-0">
                  <div
                    class="w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium transition-all"
                    :class="getStepCircleClass(3)"
                  >
                    3
                  </div>
                </div>
                <div class="ml-4">
                  <p class="text-sm font-medium" :class="getStepTitleClass(3)">确认与提交</p>
                  <p class="text-xs mt-1" :class="getStepDescClass(3)">
                    {{ selectedClassroomId ? `已选教室：${selectedClassroomName}` : '填写预约信息' }}
                  </p>
                </div>
              </div>
            </div>

            <!-- 用户信息摘要 -->
            <div class="border-t border-secondary-200 pt-6">
              <div class="flex items-center space-x-3">
                <div class="w-12 h-12 rounded-full bg-gradient-to-br from-primary to-primary-400 flex items-center justify-center text-white font-semibold">
                  {{ userInitial }}
                </div>
                <div>
                  <p class="text-sm font-medium text-gray-900">{{ userName }}</p>
                  <p class="text-xs text-gray-500">{{ userRole }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 右侧主内容区 -->
        <div class="lg:col-span-3">
          <div class="card">
            <!-- 教室类型选择 -->
            <div v-if="currentStep === 1" class="mb-8">
              <h2 class="text-xl font-semibold text-gray-900 mb-2">选择教室类型</h2>
              <p class="text-sm text-gray-500 mb-6">
                当前已选：
                <span v-if="selectedClassroomTypeLabel" class="text-primary font-semibold">
                  {{ selectedClassroomTypeLabel }}
                </span>
                <span v-else>未选择</span>
              </p>
              <p v-if="isCourseTypeLocked" class="text-sm text-primary font-semibold mb-6">
                当前来自课程「{{ courseName || '指定课程' }}」，教室类型已锁定为：{{ lockedTypeLabel || selectedClassroomTypeLabel }}
              </p>
              <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div
                  v-for="type in classroomTypes"
                  :key="type.value"
                  @click="selectClassroomType(type.value)"
                  :class="[
                    'classroom-card classroom-type-card cursor-pointer p-6 relative',
                    selectedClassroomType === type.value ? 'is-selected' : '',
                    isCourseTypeLocked && selectedClassroomType !== type.value ? 'is-locked-out' : ''
                  ]"
                >
                  <div class="text-center">
                    <div class="text-4xl mb-3">{{ type.icon }}</div>
                    <h3 class="font-semibold text-gray-900">{{ type.label }}</h3>
                    <p class="text-sm text-gray-500 mt-2">{{ type.description }}</p>
                  </div>
                  <div
                    v-if="selectedClassroomType === type.value"
                    class="selected-tip text-sm text-primary font-semibold mt-4 text-center"
                  >
                    当前预约将使用该类型筛选可用教室
                  </div>
                </div>
              </div>
              <div class="mt-8 flex justify-end">
                <button
                  @click="currentStep = 2"
                  :disabled="!selectedClassroomType"
                  class="btn-primary"
                  :class="{ 'opacity-50 cursor-not-allowed': !selectedClassroomType }"
                >
                  下一步
                </button>
              </div>
            </div>

            <!-- 日期时间选择 -->
            <div v-if="currentStep === 2">
              <h2 class="text-xl font-semibold text-gray-900 mb-6">选择日期与时间</h2>

              <!-- 月份导航 -->
              <div class="flex items-center justify-between mb-6">
                <button
                  @click="previousMonth"
                  class="p-2 rounded-lg hover:bg-secondary-100 transition-colors"
                >
                  <ChevronLeftIcon class="w-5 h-5 text-gray-600" />
                </button>
                <h3 class="text-lg font-medium text-gray-900">
                  {{ currentMonthLabel }}
                </h3>
                <button
                  @click="nextMonth"
                  class="p-2 rounded-lg hover:bg-secondary-100 transition-colors"
                >
                  <ChevronRightIcon class="w-5 h-5 text-gray-600" />
                </button>
              </div>

              <!-- 日历 -->
              <div class="mb-8">
                <!-- 星期标题 -->
                <div class="grid grid-cols-7 gap-2 mb-2">
                  <div
                    v-for="day in weekDays"
                    :key="day"
                    class="text-center text-sm font-medium text-gray-500 py-2"
                  >
                    {{ day }}
                  </div>
                </div>
                <!-- 日期 -->
                <div class="grid grid-cols-7 gap-2">
                  <div
                    v-for="date in calendarDays"
                    :key="date.date"
                    @click="selectDate(date)"
                    :class="[
                      'calendar-day relative',
                      date.isCurrentMonth ? '' : 'text-gray-300',
                      date.isDisabled ? 'text-gray-300 cursor-not-allowed bg-gray-50 pointer-events-none' : '',
                      date.isSelected ? 'selected' : '',
                      date.isToday ? 'today' : ''
                    ]"
                  >
                    {{ date.day }}
                    <span
                      v-if="date.isSelected"
                      class="absolute -bottom-1 left-1/2 transform -translate-x-1/2 w-1 h-1 bg-accent rounded-full"
                    ></span>
                  </div>
                </div>
              </div>

              <!-- 时间段选择 -->
              <div v-if="selectedDate">
                <h4 class="text-lg font-medium text-gray-900 mb-4">
                  {{ formatFullDate(selectedDate) }} - 可选时间段
                </h4>
                <p v-if="slotStatusLoading" class="text-sm text-gray-500 mb-4">正在同步后端可用性...</p>
                <div class="grid grid-cols-3 md:grid-cols-5 gap-4 mb-8">
                  <div
                    v-for="slot in timeSlots"
                    :key="slot.time"
                    @click="selectTimeSlot(slot)"
                    :class="[
                      'time-slot',
                      (slot.isOccupied || slot.isPast) ? 'occupied' : '',
                      slot.isNoMatch ? 'no-match' : '',
                      slot.isSelected ? 'selected' : ''
                    ]"
                  >
                    <div class="font-medium">{{ slot.time }}</div>
                    <div class="text-xs mt-1">
                      {{ slot.isNoMatch ? '无匹配教室' : (slot.isPast ? '已过时' : (slot.isOccupied ? '已占用' : '可用')) }}
                    </div>
                  </div>
                </div>
              </div>

              <!-- 底部操作栏 -->
              <div class="flex items-center justify-between pt-6 border-t border-secondary-200">
                <button
                  @click="currentStep = 1"
                  class="btn-secondary"
                >
                  上一步
                </button>
                <button
                  @click="enterStep3"
                  :disabled="!selectedTimeSlot"
                  class="btn-primary"
                  :class="{ 'opacity-50 cursor-not-allowed': !selectedTimeSlot }"
                >
                  下一步
                </button>
              </div>
            </div>

            <!-- 确认与提交 -->
            <div v-if="currentStep === 3">
              <h2 class="text-xl font-semibold text-gray-900 mb-6">确认预约信息</h2>

              <!-- 预约摘要 -->
              <div class="bg-secondary-50 rounded-xl p-6 mb-8">
                <div class="grid grid-cols-2 gap-6">
                  <div>
                    <p class="text-sm text-gray-500 mb-1">教室类型</p>
                    <p class="font-medium text-gray-900">{{ selectedClassroomTypeLabel || '未选择' }}</p>
                  </div>
                  <div>
                    <p class="text-sm text-gray-500 mb-1">预约日期</p>
                    <p class="font-medium text-gray-900">{{ formatFullDate(selectedDate) }}</p>
                  </div>
                  <div>
                    <p class="text-sm text-gray-500 mb-1">时间段</p>
                    <p class="font-medium text-gray-900">{{ selectedTimeSlot?.time }}</p>
                  </div>
                  <div>
                    <p class="text-sm text-gray-500 mb-1">所选教室</p>
                    <p class="font-medium text-gray-900">{{ selectedClassroomName }}</p>
                  </div>
                  <div>
                    <p class="text-sm text-gray-500 mb-1">状态</p>
                    <span class="badge badge-success">待审核</span>
                  </div>
                </div>
              </div>

              <!-- 具体教室选择 -->
              <div class="mb-8">
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  选择具体教室 <span class="text-danger">*</span>
                </label>
                <el-select
                  v-model="selectedClassroomId"
                  class="w-full"
                  :loading="classroomsLoading"
                  :disabled="classroomsLoading || availableClassrooms.length === 0"
                  :placeholder="classroomsLoading ? '加载可选教室中...' : (availableClassrooms.length === 0 ? '暂无可用教室' : '请选择具体教室')"
                  :no-data-text="classroomsLoading ? '加载可选教室中...' : '暂无可用教室'"
                >
                  <el-option
                    v-for="room in availableClassrooms"
                    :key="room.id"
                    :label="`${room.name}（${room.building}栋${room.room_number}，容量${room.capacity}）`"
                    :value="room.id"
                  />
                </el-select>
              </div>

              <!-- 预约用途 -->
              <div class="mb-8">
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  预约用途 <span class="text-danger">*</span>
                </label>
                <textarea
                  v-model="purpose"
                  rows="4"
                  class="input"
                  placeholder="请简要说明预约用途，如：课程教学、学术研讨等"
                ></textarea>
              </div>

              <!-- 参与人数 -->
              <div class="mb-8">
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  预计参与人数
                </label>
                <input
                  v-model.number="participantCount"
                  type="number"
                  class="input"
                  placeholder="请输入参与人数"
                  min="1"
                >
              </div>

              <!-- 底部操作栏 -->
              <div class="flex items-center justify-between pt-6 border-t border-secondary-200">
                <button
                  @click="currentStep = 2"
                  class="btn-secondary"
                >
                  上一步
                </button>
                <button
                  @click="submitReservation"
                  :disabled="!purpose || submitting"
                  class="btn-primary"
                  :class="{ 'opacity-50 cursor-not-allowed': !purpose || submitting }"
                >
                  {{ submitting ? '提交中...' : '提交预约' }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 成功提示 -->
    <div v-if="showSuccessModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-2xl p-8 max-w-md w-full mx-4 text-center">
        <div class="w-16 h-16 bg-success rounded-full flex items-center justify-center mx-auto mb-6">
          <CheckIcon class="w-8 h-8 text-white" />
        </div>
        <h3 class="text-2xl font-bold text-gray-900 mb-2">预约提交成功！</h3>
        <p class="text-gray-600 mb-6">您的预约已提交，请等待管理员审核。</p>
        <button
          @click="handleSuccessConfirm"
          class="btn-primary w-full"
        >
          确定
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ChevronLeftIcon, ChevronRightIcon, CheckIcon } from '@heroicons/vue/24/outline'
import { ElMessage } from 'element-plus'
import { useStore } from 'vuex'
import { getClassrooms, recommendClassrooms } from '@/api/classroom'
import { checkConflict, createReservation } from '@/api/reservation'
import PageHeader from '@/components/common/PageHeader.vue'

// 响应式数据
const currentStep = ref(1)
const selectedClassroomType = ref('')
const selectedDate = ref(null)
const selectedTimeSlot = ref(null)
const purpose = ref('')
const participantCount = ref(1)
const showSuccessModal = ref(false)
const submitting = ref(false)
const classroomsLoading = ref(false)
const slotStatusLoading = ref(false)
const availableClassrooms = ref([])
const store = useStore()
const route = useRoute()
const router = useRouter()
const courseId = ref(route.query.course_id ? Number(route.query.course_id) : null)
const courseName = ref(typeof route.query.course_name === 'string' ? route.query.course_name : '')
const courseClassroomType = ref(
  typeof route.query.course_classroom_type === 'string' ? route.query.course_classroom_type : ''
)
const preferredClassroomId = ref(route.query.classroom_id ? Number(route.query.classroom_id) : null)
const preferredClassroomType = ref(
  typeof route.query.classroom_type === 'string' ? route.query.classroom_type : ''
)
const selectedClassroomId = ref(preferredClassroomId.value || null)
let successRedirectTimer = null

const userName = computed(() => store.state.user?.username || '用户')
const userRole = computed(() => {
  const roleMap = { admin: '管理员', teacher: '教师', student: '学生' }
  return roleMap[store.state.user?.role] || '用户'
})
const userInitial = computed(() => userName.value?.charAt(0) || 'U')
const selectedClassroomName = computed(() => {
  const selected = availableClassrooms.value.find((item) => item.id === selectedClassroomId.value)
  return selected?.name || '未选择'
})
const selectedClassroomTypeLabel = computed(() => {
  const selected = classroomTypes.value.find((item) => item.value === selectedClassroomType.value)
  return selected?.label || ''
})
const isCourseTypeLocked = computed(() => Boolean(courseId.value && courseClassroomType.value))
const lockedTypeLabel = computed(() => {
  const matched = classroomTypes.value.find((item) => item.value === courseClassroomType.value)
  return matched?.label || ''
})

// 教室类型
const classroomTypes = ref([
  {
    value: 'multimedia',
    label: '多媒体教室',
    icon: '📽️',
    description: '配备投影仪、音响、电脑等设备'
  },
  {
    value: 'lab',
    label: '实验室',
    icon: '🔬',
    description: '专业实验设备，适合实践课程'
  },
  {
    value: 'lecture',
    label: '普通教室',
    icon: '🏫',
    description: '基础教学设施，适合常规课程'
  }
])

if (preferredClassroomType.value) {
  const validTypes = new Set(classroomTypes.value.map((item) => item.value))
  if (validTypes.has(preferredClassroomType.value)) {
    selectedClassroomType.value = preferredClassroomType.value
  }
}

if (isCourseTypeLocked.value) {
  selectedClassroomType.value = courseClassroomType.value
}

const isStepCompleted = (step) => {
  if (step === 1) return Boolean(selectedClassroomType.value)
  if (step === 2) return Boolean(selectedDate.value && selectedTimeSlot.value)
  return false
}

const isStepActive = (step) => currentStep.value === step

const getStepCircleClass = (step) => {
  if (isStepCompleted(step)) {
    return 'bg-primary text-white'
  }
  if (isStepActive(step)) {
    return 'bg-primary text-white ring-4 ring-primary/20'
  }
  return 'bg-secondary-200 text-gray-500'
}

const getStepTitleClass = (step) => {
  if (isStepCompleted(step) || isStepActive(step)) {
    return 'text-gray-900'
  }
  return 'text-gray-500'
}

const getStepDescClass = (step) => {
  if (isStepCompleted(step) || isStepActive(step)) {
    return 'text-gray-500'
  }
  return 'text-gray-400'
}

// 星期标题
const weekDays = ['日', '一', '二', '三', '四', '五', '六']

// 当前月份
const currentMonth = ref(new Date())

// 月份标签
const currentMonthLabel = computed(() => {
  const year = currentMonth.value.getFullYear()
  const month = currentMonth.value.getMonth() + 1
  return `${year}年${month}月`
})

const pad2 = (value) => String(value).padStart(2, '0')
const formatLocalDate = (date) => `${date.getFullYear()}-${pad2(date.getMonth() + 1)}-${pad2(date.getDate())}`

// 日历日期
const calendarDays = computed(() => {
  const year = currentMonth.value.getFullYear()
  const month = currentMonth.value.getMonth()
  const todayStr = formatLocalDate(new Date())

  const firstDay = new Date(year, month, 1)
  const lastDay = new Date(year, month + 1, 0)
  const startDayOfWeek = firstDay.getDay()

  const days = []

  // 上个月的日期
  for (let i = 0; i < startDayOfWeek; i++) {
    const day = new Date(year, month, -startDayOfWeek + i + 1)
    days.push({
      date: formatLocalDate(day),
      day: day.getDate(),
      isCurrentMonth: false,
      isToday: false,
      isPast: formatLocalDate(day) < todayStr,
      isDisabled: true,
      isSelected: false
    })
  }

  // 当前月份的日期
  for (let i = 1; i <= lastDay.getDate(); i++) {
    const day = new Date(year, month, i)
    const dateStr = formatLocalDate(day)
    const today = formatLocalDate(new Date())

    days.push({
      date: dateStr,
      day: i,
      isCurrentMonth: true,
      isToday: dateStr === today,
      isPast: dateStr < todayStr,
      isDisabled: dateStr < todayStr,
      isSelected: selectedDate.value === dateStr
    })
  }

  // 下个月的日期（补齐到42天）
  const remainingDays = 42 - days.length
  for (let i = 1; i <= remainingDays; i++) {
    const day = new Date(year, month + 1, i)
    days.push({
      date: formatLocalDate(day),
      day: i,
      isCurrentMonth: false,
      isToday: false,
      isPast: formatLocalDate(day) < todayStr,
      isDisabled: true,
      isSelected: false
    })
  }

  return days
})

const baseTimeSlots = [
  { time: '08:00-10:00' },
  { time: '10:00-12:00' },
  { time: '14:00-16:00' },
  { time: '16:00-18:00' },
  { time: '19:00-21:00' }
]

const timeSlots = ref(baseTimeSlots.map((slot) => ({
  ...slot,
  isOccupied: false,
  isPast: false,
  isNoMatch: false,
  isSelected: false
})))
let slotAvailabilitySeq = 0

// 方法
const previousMonth = () => {
  currentMonth.value = new Date(currentMonth.value.getFullYear(), currentMonth.value.getMonth() - 1, 1)
}

const nextMonth = () => {
  currentMonth.value = new Date(currentMonth.value.getFullYear(), currentMonth.value.getMonth() + 1, 1)
}

const selectClassroomType = (typeValue) => {
  if (isCourseTypeLocked.value && typeValue !== courseClassroomType.value) {
    return
  }
  selectedClassroomType.value = typeValue
}

const selectDate = (date) => {
  if (!date.isCurrentMonth || date.isDisabled) return
  selectedDate.value = date.date
  selectedTimeSlot.value = null
  timeSlots.value = timeSlots.value.map((slot) => ({
    ...slot,
    isSelected: false
  }))
  updateTimeSlotAvailability()
}

const selectTimeSlot = (slot) => {
  if (slot.isOccupied || slot.isNoMatch || slot.isPast) return
  timeSlots.value = timeSlots.value.map((item) => ({
    ...item,
    isSelected: item.time === slot.time
  }))
  selectedTimeSlot.value = { ...slot, isSelected: true }
}

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const [year, month, day] = dateStr.split('-').map(Number)
  if (!year || !month || !day) return dateStr
  return `${month}月${day}日`
}

const formatFullDate = (dateStr) => {
  if (!dateStr) return ''
  const [year, month, day] = dateStr.split('-').map(Number)
  if (!year || !month || !day) return dateStr
  const date = new Date(year, month - 1, day)
  const weekDays = ['周日', '周一', '周二', '周三', '周四', '周五', '周六']
  return `${year}年${month}月${day}日 ${weekDays[date.getDay()]}`
}
const toMinutes = (hhmm) => {
  const [h, m] = (hhmm || '').split(':').map(Number)
  if (Number.isNaN(h) || Number.isNaN(m)) return 0
  return h * 60 + m
}

const toList = (payload) => {
  if (Array.isArray(payload)) return payload
  if (Array.isArray(payload?.results)) return payload.results
  if (Array.isArray(payload?.data)) return payload.data
  return []
}

const updateTimeSlotAvailability = async () => {
  if (!selectedDate.value || !selectedClassroomType.value) {
    timeSlots.value = baseTimeSlots.map((slot) => ({
      ...slot,
      isOccupied: false,
      isPast: false,
      isNoMatch: false,
      isSelected: selectedTimeSlot.value?.time === slot.time
    }))
    return
  }

  const seq = ++slotAvailabilitySeq
  slotStatusLoading.value = true

  try {
    const todayStr = formatLocalDate(new Date())
    const now = new Date()
    const nowMinutes = now.getHours() * 60 + now.getMinutes()
    const isToday = selectedDate.value === todayStr

    const classroomsResp = await getClassrooms({
      classroom_type: selectedClassroomType.value,
      is_available: true
    })
    const baseCandidates = toList(classroomsResp).filter(
      (item) => Number(item.capacity) >= Number(participantCount.value || 1)
    )

    if (!baseCandidates.length) {
      if (seq !== slotAvailabilitySeq) return
      selectedTimeSlot.value = null
      timeSlots.value = baseTimeSlots.map((slot) => ({
        ...slot,
        isOccupied: false,
        isPast: false,
        isNoMatch: true,
        isSelected: false
      }))
      return
    }

    const checks = await Promise.all(
      baseTimeSlots.map(async (slot) => {
        const [startTime, endTime] = slot.time.split('-')
        if (isToday && toMinutes(endTime) <= nowMinutes) {
          return {
            time: slot.time,
            isOccupied: false,
            isPast: true,
            isNoMatch: false
          }
        }
        const resp = await recommendClassrooms({
          date: selectedDate.value,
          start_time: startTime,
          end_time: endTime,
          participant_count: Number(participantCount.value || 1),
          classroom_type: selectedClassroomType.value,
          requirements: {}
        })
        const recommendations = Array.isArray(resp?.recommendations) ? resp.recommendations : []
        return {
          time: slot.time,
          isOccupied: recommendations.length === 0,
          isPast: false,
          isNoMatch: false
        }
      })
    )

    if (seq !== slotAvailabilitySeq) return

    const currentSelectedTime = selectedTimeSlot.value?.time
    timeSlots.value = checks.map((slot) => ({
      ...slot,
      isSelected: currentSelectedTime === slot.time && !slot.isOccupied && !slot.isNoMatch && !slot.isPast
    }))

    if (currentSelectedTime) {
      const stillAvailable = checks.some((slot) => slot.time === currentSelectedTime && !slot.isOccupied && !slot.isNoMatch && !slot.isPast)
      if (!stillAvailable) {
        selectedTimeSlot.value = null
      }
    }
  } catch (error) {
    if (seq !== slotAvailabilitySeq) return
    timeSlots.value = baseTimeSlots.map((slot) => ({
      ...slot,
      isOccupied: false,
      isPast: false,
      isNoMatch: false,
      isSelected: selectedTimeSlot.value?.time === slot.time
    }))
    ElMessage.warning('时间段可用性获取失败，已显示默认可选状态')
  } finally {
    if (seq === slotAvailabilitySeq) {
      slotStatusLoading.value = false
    }
  }
}

const loadAvailableClassrooms = async () => {
  if (!selectedClassroomType.value) return
  classroomsLoading.value = true
  try {
    const classroomResp = await getClassrooms({
      classroom_type: selectedClassroomType.value,
      is_available: true
    })
    const candidates = toList(classroomResp)
      .filter((item) => Number(item.capacity) >= Number(participantCount.value || 1))
      .sort((a, b) => Number(a.capacity) - Number(b.capacity))

    availableClassrooms.value = candidates

    if (!candidates.length) {
      selectedClassroomId.value = null
      return
    }

    if (preferredClassroomId.value && candidates.some((item) => item.id === preferredClassroomId.value)) {
      selectedClassroomId.value = preferredClassroomId.value
      return
    }

    if (selectedClassroomId.value && candidates.some((item) => item.id === selectedClassroomId.value)) {
      return
    }

    selectedClassroomId.value = candidates[0].id
  } catch (error) {
    availableClassrooms.value = []
    selectedClassroomId.value = null
    ElMessage.error('加载可选教室失败')
  } finally {
    classroomsLoading.value = false
  }
}

const enterStep3 = async () => {
  if (!selectedTimeSlot.value) {
    ElMessage.warning('请先选择时间段')
    return
  }

  currentStep.value = 3
  await loadAvailableClassrooms()
  if (!availableClassrooms.value.length) {
    ElMessage.warning('当前条件下暂无可用教室，请调整人数或时间段')
  }
}

const resetBookingToHome = async () => {
  currentStep.value = 1
  selectedClassroomType.value = ''
  selectedDate.value = null
  selectedTimeSlot.value = null
  selectedClassroomId.value = null
  purpose.value = ''
  participantCount.value = 1
  showSuccessModal.value = false
  availableClassrooms.value = []
  preferredClassroomId.value = null
  preferredClassroomType.value = ''
  courseId.value = null
  courseName.value = ''
  courseClassroomType.value = ''
  slotAvailabilitySeq += 1
  slotStatusLoading.value = false
  timeSlots.value = baseTimeSlots.map((slot) => ({
    ...slot,
    isOccupied: false,
    isPast: false,
    isNoMatch: false,
    isSelected: false
  }))
  await router.replace({ path: '/booking' })
}

const scheduleBookingHomeRedirect = () => {
  if (successRedirectTimer) {
    window.clearTimeout(successRedirectTimer)
  }
  successRedirectTimer = window.setTimeout(() => {
    successRedirectTimer = null
    resetBookingToHome()
  }, 900)
}

const submitReservation = async () => {
  if (!selectedClassroomType.value || !selectedDate.value || !selectedTimeSlot.value) {
    ElMessage.warning('请先选择教室类型、日期和时间段')
    return
  }
  if (!selectedClassroomId.value) {
    ElMessage.warning('请选择具体教室')
    return
  }
  if (!purpose.value.trim()) {
    ElMessage.warning('请填写使用目的')
    return
  }
  if (participantCount.value <= 0) {
    ElMessage.warning('参与人数必须大于0')
    return
  }
  if (isCourseTypeLocked.value && selectedClassroomType.value !== courseClassroomType.value) {
    ElMessage.warning('当前课程仅允许预约指定教室类型')
    return
  }

  submitting.value = true
  try {
    const [startTime, endTime] = selectedTimeSlot.value.time.split('-')
    const selectedClassroom = availableClassrooms.value.find((item) => item.id === selectedClassroomId.value)
    if (!selectedClassroom) {
      ElMessage.warning('所选教室不可用，请重新选择')
      return
    }

    const payload = {
      classroom: selectedClassroom.id,
      date: selectedDate.value,
      start_time: startTime,
      end_time: endTime,
      purpose: purpose.value.trim(),
      participant_count: Number(participantCount.value),
      description: `类型:${selectedClassroomType.value}; 用户选择教室:${selectedClassroom.name}`
    }
    if (courseId.value) {
      payload.course_id = courseId.value
    }

    const conflict = await checkConflict(payload)
    if (conflict?.has_conflict) {
      ElMessage.warning('该时间段已被占用，请选择其他时间段')
      return
    }

    await createReservation(payload)
    showSuccessModal.value = true
    scheduleBookingHomeRedirect()
  } catch (error) {
    ElMessage.error('预约提交失败，请稍后重试')
  } finally {
    submitting.value = false
  }
}

const handleSuccessConfirm = () => {
  if (successRedirectTimer) {
    window.clearTimeout(successRedirectTimer)
    successRedirectTimer = null
  }
  resetBookingToHome()
}

watch(
  () => participantCount.value,
  () => {
    if (currentStep.value === 3) {
      loadAvailableClassrooms()
    }
    if (currentStep.value >= 2 && selectedDate.value && selectedClassroomType.value) {
      updateTimeSlotAvailability()
    }
  }
)

watch(
  () => selectedClassroomType.value,
  () => {
    selectedDate.value = null
    selectedTimeSlot.value = null
    timeSlots.value = baseTimeSlots.map((slot) => ({
      ...slot,
      isOccupied: false,
      isPast: false,
      isNoMatch: false,
      isSelected: false
    }))
  }
)

onUnmounted(() => {
  if (successRedirectTimer) {
    window.clearTimeout(successRedirectTimer)
    successRedirectTimer = null
  }
})
</script>

<style scoped>
.classroom-type-card {
  border-width: 2px;
  border-color: #e5e7eb;
  transition: all 0.2s ease;
}

.classroom-type-card:hover {
  border-color: #80cbc4;
}

.classroom-type-card.is-selected {
  border-color: #00897b;
  box-shadow: 0 0 0 3px rgba(0, 137, 123, 0.12), 0 8px 20px rgba(0, 137, 123, 0.12);
  background: linear-gradient(180deg, #ffffff 0%, #f5fffc 100%);
}

.classroom-type-card.is-locked-out {
  opacity: 0.45;
  cursor: not-allowed;
}

</style>
