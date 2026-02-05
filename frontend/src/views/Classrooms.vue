<template>
  <div class="min-h-screen bg-secondary-50 py-8">
    <!-- 页面头部 -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mb-8">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-3xl font-bold text-gray-900">教室列表</h1>
          <p class="mt-2 text-gray-600">浏览和预约可用教室</p>
        </div>
        <router-link to="/booking" class="btn-primary">
          快速预约
        </router-link>
      </div>
    </div>

    <!-- 筛选栏 -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mb-8">
      <div class="card">
        <div class="grid grid-cols-1 md:grid-cols-5 gap-4">
          <!-- 教室类型筛选 -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              教室类型
            </label>
            <select v-model="searchForm.classroom_type" class="input">
              <option value="">全部</option>
              <option value="lecture">普通教室</option>
              <option value="lab">实验室</option>
              <option value="multimedia">多媒体教室</option>
              <option value="conference">会议室</option>
              <option value="art">艺术室</option>
            </select>
          </div>

          <!-- 楼层筛选 -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              楼栋
            </label>
            <input
              v-model="searchForm.building"
              type="text"
              class="input"
              placeholder="输入楼栋"
            >
          </div>

          <!-- 容量筛选 -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              容量
            </label>
            <select v-model="searchForm.capacity" class="input">
              <option value="">全部</option>
              <option value="30">30人以下</option>
              <option value="50">30-50人</option>
              <option value="100">50-100人</option>
              <option value="101">100人以上</option>
            </select>
          </div>

          <!-- 搜索框 -->
          <div class="md:col-span-2">
            <label class="block text-sm font-medium text-gray-700 mb-2">
              搜索教室
            </label>
            <div class="relative">
              <input
                v-model="searchForm.search"
                type="text"
                class="input pl-10"
                placeholder="输入教室编号或名称"
              >
              <svg class="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
          </div>
        </div>
        <!-- 操作按钮 -->
        <div class="flex space-x-3 mt-4">
          <button @click="fetchClassrooms" class="btn-primary">
            查询
          </button>
          <button @click="resetSearch" class="btn-secondary">
            重置
          </button>
        </div>
      </div>
    </div>

    <!-- 教室卡片网格 -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div v-if="loading" class="text-center py-12">
        <div class="inline-block w-8 h-8 border-4 border-primary border-t-transparent rounded-full animate-spin"></div>
        <p class="mt-4 text-gray-600">加载中...</p>
      </div>

      <div v-else-if="classrooms.length === 0" class="text-center py-12">
        <svg class="w-16 h-16 text-gray-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
        </svg>
        <h3 class="text-lg font-medium text-gray-900 mb-2">暂无教室</h3>
        <p class="text-gray-500">请调整筛选条件后重试</p>
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div
          v-for="classroom in classrooms"
          :key="classroom.id"
          :class="[
            'classroom-card',
            !classroom.is_available && 'opacity-60'
          ]"
        >
          <!-- 教室图片占位 -->
          <div class="h-48 bg-gradient-to-br from-primary/20 to-primary/10 flex items-center justify-center">
            <svg class="w-16 h-16 text-primary/40" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
            </svg>
          </div>

          <!-- 教室信息 -->
          <div class="p-6">
            <div class="flex items-start justify-between mb-4">
              <div>
                <h3 class="text-lg font-semibold text-gray-900">
                  {{ classroom.name }}
                </h3>
                <p class="text-sm text-gray-500 mt-1">
                  {{ classroom.building }}栋 {{ classroom.floor }}层 {{ classroom.room_number }}室
                </p>
              </div>
              <span
                v-if="!classroom.is_available"
                class="badge badge-warning"
              >
                维护中
              </span>
              <span v-else class="badge badge-success">
                可用
              </span>
            </div>

            <!-- 设施图标 -->
            <div class="flex flex-wrap gap-2 mb-4">
              <span
                v-if="classroom.has_projector"
                class="inline-flex items-center px-2 py-1 bg-secondary-100 rounded text-xs text-gray-600"
              >
                📽️ 投影仪
              </span>
              <span
                v-if="classroom.has_computer"
                class="inline-flex items-center px-2 py-1 bg-secondary-100 rounded text-xs text-gray-600"
              >
                💻 电脑
              </span>
              <span
                v-if="classroom.has_microphone"
                class="inline-flex items-center px-2 py-1 bg-secondary-100 rounded text-xs text-gray-600"
              >
                🎤 麦克风
              </span>
              <span
                v-if="classroom.has_whiteboard"
                class="inline-flex items-center px-2 py-1 bg-secondary-100 rounded text-xs text-gray-600"
              >
                📝 白板
              </span>
              <span
                v-if="classroom.has_air_conditioning"
                class="inline-flex items-center px-2 py-1 bg-secondary-100 rounded text-xs text-gray-600"
              >
                ❄️ 空调
              </span>
            </div>

            <!-- 容量信息 -->
            <div class="flex items-center justify-between mb-4">
              <div class="flex items-center space-x-2 text-sm text-gray-600">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20H2a2 2 0 01-2-2v-2a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2zm2.5-8.25h.008v.008h-.008V9.75h.008zM12 14.5a.5.5 0 01-.5.5h-5a.5.5 0 010-1h5a.5.5 0 01.5.5zm5 0a.5.5 0 01-.5.5h-5a.5.5 0 010-1h5a.5.5 0 01.5.5z" />
                </svg>
                <span>{{ classroom.capacity }}人</span>
              </div>
              <div class="text-xs text-gray-500">
                {{ classroom.classroom_type_display }}
              </div>
            </div>

            <!-- 操作按钮 -->
            <div class="flex space-x-3">
              <button
                @click="viewDetail(classroom)"
                class="flex-1 btn-secondary text-sm py-2"
              >
                详情
              </button>
              <button
                @click="goToReservation(classroom)"
                :disabled="!classroom.is_available"
                class="flex-1 btn-primary text-sm py-2"
                :class="{ 'opacity-50 cursor-not-allowed': !classroom.is_available }"
              >
                {{ classroom.is_available ? '预约' : '不可用' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// 响应式数据
const loading = ref(false)
const classrooms = ref([])
const searchForm = ref({
  classroom_type: '',
  building: '',
  capacity: '',
  search: ''
})

// 获取教室列表
const fetchClassrooms = async () => {
  loading.value = true
  try {
    // TODO: 调用 API 获取教室列表
    // const params = {}
    // if (searchForm.value.classroom_type) {
    //   params.classroom_type = searchForm.value.classroom_type
    // }
    // if (searchForm.value.building) {
    //   params.building = searchForm.value.building
    // }
    // const data = await getClassrooms(params)
    // classrooms.value = data.results || data

    // 模拟数据
    classrooms.value = [
      {
        id: 1,
        name: 'A-101多媒体教室',
        building: 'A',
        floor: 1,
        room_number: '101',
        capacity: 50,
        classroom_type: 'multimedia',
        classroom_type_display: '多媒体教室',
        is_available: true,
        has_projector: true,
        has_computer: true,
        has_microphone: true,
        has_whiteboard: true,
        has_air_conditioning: true
      },
      {
        id: 2,
        name: 'B-201实验室',
        building: 'B',
        floor: 2,
        room_number: '201',
        capacity: 40,
        classroom_type: 'lab',
        classroom_type_display: '实验室',
        is_available: false,
        has_projector: true,
        has_computer: true,
        has_microphone: false,
        has_whiteboard: true,
        has_air_conditioning: true
      },
      {
        id: 3,
        name: 'C-301普通教室',
        building: 'C',
        floor: 3,
        room_number: '301',
        capacity: 60,
        classroom_type: 'lecture',
        classroom_type_display: '普通教室',
        is_available: true,
        has_projector: false,
        has_computer: false,
        has_microphone: false,
        has_whiteboard: true,
        has_air_conditioning: true
      },
      {
        id: 4,
        name: 'A-102多媒体教室',
        building: 'A',
        floor: 1,
        room_number: '102',
        capacity: 80,
        classroom_type: 'multimedia',
        classroom_type_display: '多媒体教室',
        is_available: true,
        has_projector: true,
        has_computer: true,
        has_microphone: true,
        has_whiteboard: true,
        has_air_conditioning: true
      },
      {
        id: 5,
        name: 'D-101会议室',
        building: 'D',
        floor: 1,
        room_number: '101',
        capacity: 20,
        classroom_type: 'conference',
        classroom_type_display: '会议室',
        is_available: true,
        has_projector: true,
        has_computer: false,
        has_microphone: true,
        has_whiteboard: true,
        has_air_conditioning: true
      },
      {
        id: 6,
        name: '艺术室-101',
        building: 'E',
        floor: 1,
        room_number: '101',
        capacity: 30,
        classroom_type: 'art',
        classroom_type_display: '艺术室',
        is_available: true,
        has_projector: true,
        has_computer: false,
        has_microphone: false,
        has_whiteboard: true,
        has_air_conditioning: true
      }
    ]
  } catch (error) {
    console.error('获取教室列表失败:', error)
  } finally {
    loading.value = false
  }
}

// 重置搜索
const resetSearch = () => {
  searchForm.value = {
    classroom_type: '',
    building: '',
    capacity: '',
    search: ''
  }
  fetchClassrooms()
}

// 查看详情
const viewDetail = (classroom) => {
  console.log('查看教室详情:', classroom)
  // TODO: 打开详情弹窗或跳转到详情页
}

// 跳转到预约
const goToReservation = (classroom) => {
  if (!classroom.is_available) return
  router.push({
    path: '/booking',
    query: { classroom_id: classroom.id }
  })
}

onMounted(() => {
  fetchClassrooms()
})
</script>
