<template>
  <div class="min-h-screen bg-secondary-50 py-8">
    <!-- 页面头部 -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mb-8">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-3xl font-bold text-gray-900">教室预约</h1>
          <p class="mt-2 text-gray-600">选择您需要的教室和时间</p>
        </div>
        <div class="flex items-center space-x-4">
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
      </div>
    </div>

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
                  <div class="w-8 h-8 rounded-full bg-primary text-white flex items-center justify-center text-sm font-medium">
                    ✓
                  </div>
                </div>
                <div class="ml-4">
                  <p class="text-sm font-medium text-gray-900">选择教室类型</p>
                  <p class="text-xs text-gray-500 mt-1">{{ selectedClassroomType || '多媒体教室' }}</p>
                </div>
              </div>

              <!-- 步骤 2 -->
              <div class="flex items-start mb-6">
                <div class="flex-shrink-0">
                  <div class="w-8 h-8 rounded-full bg-primary text-white flex items-center justify-center text-sm font-medium ring-4 ring-accent">
                    2
                  </div>
                </div>
                <div class="ml-4">
                  <p class="text-sm font-medium text-gray-900">选择日期与时间</p>
                  <p class="text-xs text-gray-500 mt-1">{{ selectedDate ? formatDate(selectedDate) : '请选择日期' }}</p>
                </div>
              </div>

              <!-- 步骤 3 -->
              <div class="flex items-start">
                <div class="flex-shrink-0">
                  <div class="w-8 h-8 rounded-full bg-secondary-200 text-gray-500 flex items-center justify-center text-sm font-medium">
                    3
                  </div>
                </div>
                <div class="ml-4">
                  <p class="text-sm font-medium text-gray-500">确认与提交</p>
                  <p class="text-xs text-gray-400 mt-1">填写预约信息</p>
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
              <h2 class="text-xl font-semibold text-gray-900 mb-6">选择教室类型</h2>
              <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div
                  v-for="type in classroomTypes"
                  :key="type.value"
                  @click="selectedClassroomType = type.value"
                  :class="[
                    'classroom-card cursor-pointer p-6',
                    selectedClassroomType === type.value ? 'ring-2 ring-primary' : ''
                  ]"
                >
                  <div class="text-center">
                    <div class="text-4xl mb-3">{{ type.icon }}</div>
                    <h3 class="font-semibold text-gray-900">{{ type.label }}</h3>
                    <p class="text-sm text-gray-500 mt-2">{{ type.description }}</p>
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
                <div class="grid grid-cols-3 md:grid-cols-5 gap-4 mb-8">
                  <div
                    v-for="slot in timeSlots"
                    :key="slot.time"
                    @click="selectTimeSlot(slot)"
                    :class="[
                      'time-slot',
                      slot.isOccupied ? 'occupied' : '',
                      slot.isSelected ? 'selected' : ''
                    ]"
                  >
                    <div class="font-medium">{{ slot.time }}</div>
                    <div class="text-xs mt-1">
                      {{ slot.isOccupied ? '已占用' : '可用' }}
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
                  @click="currentStep = 3"
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
                    <p class="font-medium text-gray-900">{{ selectedClassroomType }}</p>
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
                    <p class="text-sm text-gray-500 mb-1">状态</p>
                    <span class="badge badge-success">待审核</span>
                  </div>
                </div>
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
                  :disabled="!purpose"
                  class="btn-primary"
                  :class="{ 'opacity-50 cursor-not-allowed': !purpose }"
                >
                  提交预约
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
          @click="showSuccessModal = false"
          class="btn-primary w-full"
        >
          确定
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { ChevronLeftIcon, ChevronRightIcon, CheckIcon } from '@heroicons/vue/24/outline'

// 响应式数据
const currentStep = ref(1)
const selectedClassroomType = ref('')
const selectedDate = ref(null)
const selectedTimeSlot = ref(null)
const purpose = ref('')
const participantCount = ref(1)
const showSuccessModal = ref(false)

// 用户信息（模拟数据，实际应从 store 获取）
const userName = ref('张三')
const userRole = ref('学生')
const userInitial = computed(() => userName.value?.charAt(0) || 'U')

// 教室类型
const classroomTypes = ref([
  {
    value: 'multimedia',
    label: '多媒体教室',
    icon: '📽️',
    description: '配备投影仪、音响、电脑等设备'
  },
  {
    value: 'laboratory',
    label: '实验室',
    icon: '🔬',
    description: '专业实验设备，适合实践课程'
  },
  {
    value: 'ordinary',
    label: '普通教室',
    icon: '🏫',
    description: '基础教学设施，适合常规课程'
  }
])

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

// 日历日期
const calendarDays = computed(() => {
  const year = currentMonth.value.getFullYear()
  const month = currentMonth.value.getMonth()

  const firstDay = new Date(year, month, 1)
  const lastDay = new Date(year, month + 1, 0)
  const startDayOfWeek = firstDay.getDay()

  const days = []

  // 上个月的日期
  for (let i = 0; i < startDayOfWeek; i++) {
    const day = new Date(year, month, -startDayOfWeek + i + 1)
    days.push({
      date: day.toISOString().split('T')[0],
      day: day.getDate(),
      isCurrentMonth: false,
      isToday: false,
      isSelected: false
    })
  }

  // 当前月份的日期
  for (let i = 1; i <= lastDay.getDate(); i++) {
    const day = new Date(year, month, i)
    const dateStr = day.toISOString().split('T')[0]
    const today = new Date().toISOString().split('T')[0]

    days.push({
      date: dateStr,
      day: i,
      isCurrentMonth: true,
      isToday: dateStr === today,
      isSelected: selectedDate.value === dateStr
    })
  }

  // 下个月的日期（补齐到42天）
  const remainingDays = 42 - days.length
  for (let i = 1; i <= remainingDays; i++) {
    const day = new Date(year, month + 1, i)
    days.push({
      date: day.toISOString().split('T')[0],
      day: i,
      isCurrentMonth: false,
      isToday: false,
      isSelected: false
    })
  }

  return days
})

// 时间段（模拟数据）
const timeSlots = ref([
  { time: '08:00-10:00', isOccupied: false, isSelected: false },
  { time: '10:00-12:00', isOccupied: true, isSelected: false },
  { time: '14:00-16:00', isOccupied: false, isSelected: false },
  { time: '16:00-18:00', isOccupied: false, isSelected: false },
  { time: '19:00-21:00', isOccupied: true, isSelected: false },
])

// 方法
const previousMonth = () => {
  currentMonth.value = new Date(currentMonth.value.getFullYear(), currentMonth.value.getMonth() - 1, 1)
}

const nextMonth = () => {
  currentMonth.value = new Date(currentMonth.value.getFullYear(), currentMonth.value.getMonth() + 1, 1)
}

const selectDate = (date) => {
  if (!date.isCurrentMonth) return
  selectedDate.value = date.date
  selectedTimeSlot.value = null
  // 重置时间段选中状态
  timeSlots.value.forEach(slot => slot.isSelected = false)
}

const selectTimeSlot = (slot) => {
  if (slot.isOccupied) return
  timeSlots.value.forEach(s => s.isSelected = false)
  slot.isSelected = true
  selectedTimeSlot.value = slot
}

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return `${date.getMonth() + 1}月${date.getDate()}日`
}

const formatFullDate = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  const weekDays = ['周日', '周一', '周二', '周三', '周四', '周五', '周六']
  return `${date.getFullYear()}年${date.getMonth() + 1}月${date.getDate()}日 ${weekDays[date.getDay()]}`
}

const submitReservation = () => {
  // TODO: 调用 API 提交预约
  console.log({
    classroomType: selectedClassroomType.value,
    date: selectedDate.value,
    timeSlot: selectedTimeSlot.value?.time,
    purpose: purpose.value,
    participantCount: participantCount.value
  })

  showSuccessModal.value = true
}
</script>
