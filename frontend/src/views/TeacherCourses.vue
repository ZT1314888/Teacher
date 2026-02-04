<template>
  <div class="teacher-courses">
    <h2>关联课程</h2>

    <el-table :data="courses" border style="width: 100%">
      <el-table-column prop="name" label="课程名称" width="200" />
      <el-table-column prop="classroom_type_display" label="适用教室类型" width="150" />
      <el-table-column prop="description" label="课程描述" />
      <el-table-column prop="created_at" label="创建时间" width="180">
        <template #default="{ row }">
          {{ formatDateTime(row.created_at) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="160">
        <template #default="{ row }">
          <el-button type="primary" size="small" @click="goToClassrooms(row)">
            查看可预约教室
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getMyCourses } from '@/api/course'

export default {
  name: 'TeacherCourses',
  setup() {
    const router = useRouter()
    const courses = ref([])

    const formatDateTime = (dt) => {
      if (!dt) return ''
      return new Date(dt).toLocaleString('zh-CN')
    }

    const fetchCourses = async () => {
      try {
        const data = await getMyCourses()
        courses.value = data.results || data
      } catch (error) {
        ElMessage.error('获取课程列表失败')
      }
    }

    const goToClassrooms = (course) => {
      router.push({
        path: '/classrooms',
        query: { classroom_type: course.classroom_type }
      })
    }

    onMounted(() => {
      fetchCourses()
    })

    return {
      courses,
      formatDateTime,
      goToClassrooms
    }
  }
}
</script>

<style scoped>
.teacher-courses {
  padding: 20px;
}

h2 {
  margin-bottom: 20px;
}
</style>
