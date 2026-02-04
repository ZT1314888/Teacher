<template>
  <div class="classrooms">
    <h2>教室列表</h2>
    
    <el-form :inline="true" class="search-form">
      <el-form-item label="教室类型">
        <el-select v-model="searchForm.classroom_type" placeholder="请选择类型" clearable style="width: 150px">
          <el-option label="全部" value="" />
          <el-option label="普通教室" value="lecture" />
          <el-option label="实验室" value="lab" />
          <el-option label="多媒体教室" value="multimedia" />
          <el-option label="会议室" value="conference" />
          <el-option label="艺术室" value="art" />
        </el-select>
      </el-form-item>
      <el-form-item label="楼栋">
        <el-input v-model="searchForm.building" placeholder="请输入楼栋" clearable style="width: 150px" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="fetchClassrooms">查询</el-button>
        <el-button @click="resetSearch">重置</el-button>
      </el-form-item>
    </el-form>

    <el-table :data="classrooms" border style="width: 100%">
      <el-table-column prop="name" label="教室名称" width="150" />
      <el-table-column prop="building" label="楼栋" width="100" />
      <el-table-column prop="floor" label="楼层" width="80" />
      <el-table-column prop="room_number" label="房间号" width="100" />
      <el-table-column prop="capacity" label="容量" width="80" />
      <el-table-column prop="classroom_type_display" label="类型" width="120" />
      <el-table-column label="设备">
        <template #default="{ row }">
          <el-tag v-if="row.has_projector" size="small" style="margin: 2px">投影仪</el-tag>
          <el-tag v-if="row.has_computer" size="small" style="margin: 2px">电脑</el-tag>
          <el-tag v-if="row.has_microphone" size="small" style="margin: 2px">麦克风</el-tag>
          <el-tag v-if="row.has_whiteboard" size="small" style="margin: 2px">白板</el-tag>
          <el-tag v-if="row.has_air_conditioning" size="small" style="margin: 2px">空调</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="is_available" label="状态" width="80">
        <template #default="{ row }">
          <el-tag :type="row.is_available ? 'success' : 'danger'">
            {{ row.is_available ? '可用' : '不可用' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="150">
        <template #default="{ row }">
          <el-button type="primary" size="small" @click="goToReservation(row)">
            预约
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getClassrooms } from '@/api/classroom'

export default {
  name: 'Classrooms',
  setup() {
    const router = useRouter()
    const route = useRoute()
    const classrooms = ref([])
    const searchForm = ref({
      classroom_type: route.query.classroom_type || '',
      building: ''
    })

    const fetchClassrooms = async () => {
      try {
        const params = {}
        if (searchForm.value.classroom_type) {
          params.classroom_type = searchForm.value.classroom_type
        }
        if (searchForm.value.building) {
          params.building = searchForm.value.building
        }
        const data = await getClassrooms(params)
        classrooms.value = data.results || data
      } catch (error) {
        ElMessage.error('获取教室列表失败')
      }
    }

    const resetSearch = () => {
      searchForm.value = {
        classroom_type: '',
        building: ''
      }
      fetchClassrooms()
    }

    const goToReservation = (classroom) => {
      router.push({
        path: '/reservations',
        query: { classroom_id: classroom.id }
      })
    }

    onMounted(() => {
      fetchClassrooms()
    })

    return {
      classrooms,
      searchForm,
      fetchClassrooms,
      resetSearch,
      goToReservation
    }
  }
}
</script>

<style scoped>
.classrooms {
  padding: 20px;
}

h2 {
  margin-bottom: 20px;
}

.search-form {
  margin-bottom: 20px;
}
</style>
