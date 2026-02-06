<template>
  <div class="min-h-screen bg-background py-8">
    <PageHeader>
      <template #actions>
        <router-link to="/booking" class="btn-primary">快速预约</router-link>
      </template>
    </PageHeader>

    <ClassroomFilterBar
      v-model="searchForm"
      :classroom-type-locked="classroomTypeLocked"
      @search="fetchClassrooms"
      @reset="resetSearch"
    />

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <LoadingState v-if="loading" />

      <EmptyState
        v-else-if="classrooms.length === 0"
        title="暂无教室"
        description="请调整筛选条件后重试"
      >
        <template #icon>
          <svg class="w-16 h-16 text-gray-300 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
          </svg>
        </template>
      </EmptyState>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <ClassroomCard
          v-for="classroom in classrooms"
          :key="classroom.id"
          :classroom="classroom"
          @detail="viewDetail"
          @reserve="goToReservation"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getClassrooms } from '@/api/classroom'
import PageHeader from '@/components/common/PageHeader.vue'
import LoadingState from '@/components/common/LoadingState.vue'
import EmptyState from '@/components/common/EmptyState.vue'
import ClassroomFilterBar from '@/components/classroom/ClassroomFilterBar.vue'
import ClassroomCard from '@/components/classroom/ClassroomCard.vue'

const router = useRouter()
const route = useRoute()
const loading = ref(false)
const classrooms = ref([])
const courseId = ref(route.query.course_id ? Number(route.query.course_id) : null)
const courseName = ref(typeof route.query.course_name === 'string' ? route.query.course_name : '')
const courseClassroomType = ref(typeof route.query.course_classroom_type === 'string' ? route.query.course_classroom_type : '')
const classroomTypeLocked = computed(() => Boolean(courseId.value && courseClassroomType.value))
const searchForm = ref({
  classroom_type: courseClassroomType.value || '',
  building: '',
  capacity: '',
  search: ''
})

const normalizeList = (payload) => {
  if (Array.isArray(payload)) return payload
  if (Array.isArray(payload?.results)) return payload.results
  if (Array.isArray(payload?.data)) return payload.data
  return []
}

const filterByCapacity = (list) => {
  const cap = Number(searchForm.value.capacity)
  if (!cap) return list
  if (cap === 30) return list.filter((item) => Number(item.capacity) < 30)
  if (cap === 50) return list.filter((item) => Number(item.capacity) >= 30 && Number(item.capacity) <= 50)
  if (cap === 100) return list.filter((item) => Number(item.capacity) > 50 && Number(item.capacity) <= 100)
  if (cap === 101) return list.filter((item) => Number(item.capacity) > 100)
  return list
}

const fetchClassrooms = async () => {
  loading.value = true
  try {
    const params = {}
    if (searchForm.value.classroom_type) params.classroom_type = searchForm.value.classroom_type
    if (searchForm.value.building) params.building = searchForm.value.building
    if (searchForm.value.search) params.search = searchForm.value.search

    const data = await getClassrooms(params)
    const list = normalizeList(data)
    classrooms.value = filterByCapacity(list)
  } catch (error) {
    ElMessage.error('获取教室列表失败')
    classrooms.value = []
  } finally {
    loading.value = false
  }
}

const resetSearch = () => {
  searchForm.value = {
    classroom_type: classroomTypeLocked.value ? courseClassroomType.value : '',
    building: '',
    capacity: '',
    search: ''
  }
  fetchClassrooms()
}

const viewDetail = (classroom) => {
  ElMessage.info(`查看教室详情：${classroom.name}`)
}

const goToReservation = (classroom) => {
  if (!classroom.is_available) return

  if (classroomTypeLocked.value && classroom.classroom_type !== courseClassroomType.value) {
    ElMessage.warning('该课程仅可预约指定类型教室')
    return
  }

  router.push({
    path: '/booking',
    query: {
      classroom_id: classroom.id,
      classroom_type: classroom.classroom_type,
      ...(classroomTypeLocked.value
        ? {
            course_id: String(courseId.value),
            course_name: courseName.value,
            course_classroom_type: courseClassroomType.value
          }
        : {})
    }
  })
}

watch(
  () => route.query,
  (query) => {
    courseId.value = query.course_id ? Number(query.course_id) : null
    courseName.value = typeof query.course_name === 'string' ? query.course_name : ''
    courseClassroomType.value = typeof query.course_classroom_type === 'string' ? query.course_classroom_type : ''
    if (classroomTypeLocked.value) {
      searchForm.value = {
        ...searchForm.value,
        classroom_type: courseClassroomType.value
      }
    }
    fetchClassrooms()
  },
  { immediate: true }
)

onMounted(() => {
  if (classroomTypeLocked.value) {
    ElMessage.info(`课程「${courseName.value || '当前课程'}」仅允许预约${searchForm.value.classroom_type === 'lecture' ? '普通教室' : '该类型教室'}`)
  }
})
</script>
