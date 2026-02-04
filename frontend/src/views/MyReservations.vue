<template>
  <div class="my-reservations">
    <h2>我的预约</h2>

    <el-table :data="reservations" border style="width: 100%">
      <el-table-column prop="classroom_name" label="教室" width="150" />
      <el-table-column prop="date" label="日期" width="120" />
      <el-table-column label="时间" width="150">
        <template #default="{ row }">
          {{ row.start_time }} - {{ row.end_time }}
        </template>
      </el-table-column>
      <el-table-column prop="purpose" label="使用目的" />
      <el-table-column prop="status_display" label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="getStatusType(row.status)">
            {{ row.status_display }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="申请时间" width="180">
        <template #default="{ row }">
          {{ formatDateTime(row.created_at) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="100">
        <template #default="{ row }">
          <el-button
            v-if="row.status === 'pending' || row.status === 'approved'"
            type="danger"
            size="small"
            @click="handleCancel(row.id)"
          >
            取消
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getMyReservations, cancelReservation } from '@/api/reservation'

export default {
  name: 'MyReservations',
  setup() {
    const reservations = ref([])

    const getStatusType = (status) => {
      const typeMap = {
        pending: 'warning',
        approved: 'success',
        rejected: 'danger',
        cancelled: 'info'
      }
      return typeMap[status] || 'info'
    }

    const formatDateTime = (dateTime) => {
      if (!dateTime) return ''
      return new Date(dateTime).toLocaleString('zh-CN')
    }

    const fetchReservations = async () => {
      try {
        const data = await getMyReservations()
        reservations.value = data
      } catch (error) {
        ElMessage.error('获取预约列表失败')
      }
    }

    const handleCancel = async (id) => {
      try {
        await ElMessageBox.confirm('确定要取消这个预约吗？', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })

        await cancelReservation(id)
        ElMessage.success('预约已取消')
        fetchReservations()
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('取消预约失败')
        }
      }
    }

    onMounted(() => {
      fetchReservations()
    })

    return {
      reservations,
      getStatusType,
      formatDateTime,
      handleCancel
    }
  }
}
</script>

<style scoped>
.my-reservations {
  padding: 20px;
}

h2 {
  margin-bottom: 20px;
}
</style>
