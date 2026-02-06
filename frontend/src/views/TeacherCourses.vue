<template>
  <div class="teacher-courses-page">
    <PageHeader>
      <template #actions>
        <el-button type="primary" plain :loading="loading" @click="fetchCourses">
          {{ loading ? '刷新中...' : '刷新课程' }}
        </el-button>
      </template>
    </PageHeader>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <section v-if="loading" class="state-card">
        <el-skeleton :rows="8" animated />
      </section>

      <section v-else-if="error" class="state-card">
        <el-result icon="warning" title="课程数据加载失败" :sub-title="error">
          <template #extra>
            <div class="state-actions">
              <el-button type="primary" @click="fetchCourses">重试</el-button>
              <el-button @click="goToBooking">去预约教室</el-button>
            </div>
          </template>
        </el-result>
      </section>

      <section v-else-if="courses.length === 0" class="state-card empty-card">
        <div class="empty-icon">📚</div>
        <h3 class="empty-title">暂无关联课程</h3>
        <p class="empty-description">请联系管理员在 Django Admin 分配课程后，再返回查看。</p>
        <div class="empty-note">
          前台仅展示课程，不提供课程创建与分配功能。
        </div>
        <div class="state-actions">
          <el-button type="primary" @click="fetchCourses">刷新课程</el-button>
          <el-button @click="goToBooking">去预约教室</el-button>
        </div>
      </section>

      <section v-else class="courses-grid">
        <article
          v-for="course in courses"
          :key="course.id"
          class="course-card"
        >
          <div class="course-icon">
            <el-icon><Reading /></el-icon>
          </div>

          <div class="course-content">
            <h3 class="course-name">{{ course.name }}</h3>
            <p class="course-description">{{ course.description || '暂无描述' }}</p>
            <div class="course-meta">
              <el-tag type="success" effect="plain">{{ course.classroom_type_display }}</el-tag>
              <span class="course-date">
                <el-icon><Calendar /></el-icon>
                {{ formatDateTime(course.created_at) }}
              </span>
            </div>
          </div>

          <div class="course-actions">
            <el-button type="primary" class="action-btn" @click="goToClassrooms(course)">
              查看可预约教室
            </el-button>
          </div>
        </article>
      </section>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Reading, Calendar } from '@element-plus/icons-vue'
import { getMyCourses } from '@/api/course'
import PageHeader from '@/components/common/PageHeader.vue'

const router = useRouter()
const loading = ref(false)
const error = ref('')
const courses = ref([])

const toList = (payload) => {
  if (Array.isArray(payload)) return payload
  if (Array.isArray(payload?.results)) return payload.results
  if (Array.isArray(payload?.data)) return payload.data
  return []
}

const formatDateTime = (dt) => {
  if (!dt) return ''
  return new Date(dt).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  })
}

const fetchCourses = async () => {
  loading.value = true
  error.value = ''
  try {
    const data = await getMyCourses()
    courses.value = toList(data)
  } catch (e) {
    courses.value = []
    error.value = e?.response?.data?.detail || '请检查登录状态或稍后重试。'
    ElMessage.error('获取课程列表失败')
  } finally {
    loading.value = false
  }
}

const goToClassrooms = (course) => {
  router.push({
    path: '/classrooms',
    query: {
      classroom_type: course.classroom_type,
      course_id: String(course.id),
      course_name: course.name || '',
      course_classroom_type: course.classroom_type
    }
  })
}

const goToBooking = () => {
  router.push('/booking')
}

onMounted(() => {
  fetchCourses()
})
</script>

<style scoped>
.teacher-courses-page {
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

.state-card {
  background: #ffffff;
  border: 1px solid #eef2f7;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 6px 16px rgba(15, 23, 42, 0.04);
}

.empty-card {
  text-align: center;
  padding: 56px 24px;
}

.empty-icon {
  font-size: 52px;
  line-height: 1;
  margin-bottom: 16px;
}

.empty-title {
  margin: 0 0 8px;
  font-size: 20px;
  color: #0f172a;
  font-weight: 700;
}

.empty-description {
  margin: 0 0 8px;
  color: #64748b;
  font-size: 14px;
}

.empty-note {
  margin: 0 auto 20px;
  max-width: 520px;
  font-size: 13px;
  color: #94a3b8;
}

.state-actions {
  display: inline-flex;
  gap: 10px;
  align-items: center;
  justify-content: center;
  flex-wrap: wrap;
}

.courses-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 20px;
}

.course-card {
  background: #ffffff;
  border-radius: 16px;
  border: 1px solid #f1f5f9;
  box-shadow: 0 2px 12px rgba(15, 23, 42, 0.05);
  padding: 22px;
  display: flex;
  flex-direction: column;
  transition: all 0.2s ease;
}

.course-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(15, 23, 42, 0.08);
  border-color: #dbeafe;
}

.course-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: linear-gradient(135deg, #00897b 0%, #00796b 100%);
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  margin-bottom: 16px;
}

.course-content {
  flex: 1;
  margin-bottom: 18px;
}

.course-name {
  font-size: 18px;
  font-weight: 700;
  color: #0f172a;
  margin: 0 0 8px;
}

.course-description {
  margin: 0 0 14px;
  font-size: 14px;
  color: #64748b;
  line-height: 1.55;
  min-height: 42px;
}

.course-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
}

.course-date {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  color: #64748b;
  font-size: 13px;
}

.course-actions {
  padding-top: 16px;
  border-top: 1px solid #f1f5f9;
}

.action-btn {
  width: 100%;
}

@media (max-width: 768px) {
  .courses-grid {
    grid-template-columns: 1fr;
  }
}
</style>
