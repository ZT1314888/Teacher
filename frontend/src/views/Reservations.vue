<template>
  <div class="reservations">
    <PageHeader />
    
    <el-form :model="form" :rules="rules" ref="reservationForm" label-width="100px">
      <el-form-item label="选择教室" prop="classroom">
        <el-select v-model="form.classroom" placeholder="请选择教室" style="width: 100%">
          <el-option
            v-for="classroom in classrooms"
            :key="classroom.id"
            :label="`${classroom.name} (${classroom.building}-${classroom.room_number})`"
            :value="classroom.id"
          />
        </el-select>
      </el-form-item>

      <el-form-item label="预约日期" prop="date">
        <el-date-picker
          v-model="form.date"
          type="date"
          placeholder="选择日期"
          style="width: 100%"
          :disabled-date="disabledDate"
        />
      </el-form-item>

      <el-form-item label="开始时间" prop="start_time">
        <el-time-picker
          v-model="form.start_time"
          placeholder="选择开始时间"
          format="HH:mm"
          style="width: 100%"
        />
      </el-form-item>

      <el-form-item label="结束时间" prop="end_time">
        <el-time-picker
          v-model="form.end_time"
          placeholder="选择结束时间"
          format="HH:mm"
          style="width: 100%"
        />
      </el-form-item>

      <el-form-item label="使用目的" prop="purpose">
        <el-input v-model="form.purpose" placeholder="请输入使用目的" />
      </el-form-item>

      <el-form-item label="参与人数" prop="participant_count">
        <el-input-number v-model="form.participant_count" :min="1" :max="500" />
      </el-form-item>

      <el-form-item label="详细说明" prop="description">
        <el-input
          v-model="form.description"
          type="textarea"
          :rows="3"
          placeholder="请输入详细说明（可选）"
        />
      </el-form-item>

      <el-form-item>
        <el-button type="primary" @click="handleSubmit" :loading="loading">
          提交预约
        </el-button>
        <el-button @click="resetForm">重置</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getAvailableClassrooms } from '@/api/classroom'
import { createReservation, checkConflict } from '@/api/reservation'
import PageHeader from '@/components/common/PageHeader.vue'

export default {
  name: 'Reservations',
  components: { PageHeader },
  setup() {
    const router = useRouter()
    const route = useRoute()
    const reservationForm = ref(null)
    const loading = ref(false)
    const classrooms = ref([])

    const form = ref({
      classroom: null,
      date: '',
      start_time: '',
      end_time: '',
      purpose: '',
      participant_count: 1,
      description: ''
    })

    const rules = {
      classroom: [{ required: true, message: '请选择教室', trigger: 'change' }],
      date: [{ required: true, message: '请选择日期', trigger: 'change' }],
      start_time: [{ required: true, message: '请选择开始时间', trigger: 'change' }],
      end_time: [{ required: true, message: '请选择结束时间', trigger: 'change' }],
      purpose: [{ required: true, message: '请输入使用目的', trigger: 'blur' }],
      participant_count: [{ required: true, message: '请输入参与人数', trigger: 'blur' }]
    }

    const disabledDate = (time) => {
      return time.getTime() < Date.now() - 8.64e7
    }

    const formatDate = (date) => {
      const d = new Date(date)
      const year = d.getFullYear()
      const month = String(d.getMonth() + 1).padStart(2, '0')
      const day = String(d.getDate()).padStart(2, '0')
      return `${year}-${month}-${day}`
    }

    const formatTime = (time) => {
      const d = new Date(time)
      const hours = String(d.getHours()).padStart(2, '0')
      const minutes = String(d.getMinutes()).padStart(2, '0')
      return `${hours}:${minutes}:00`
    }

    const handleSubmit = async () => {
      if (!reservationForm.value) return

      await reservationForm.value.validate(async (valid) => {
        if (valid) {
          loading.value = true
          try {
            const data = {
              classroom: form.value.classroom,
              date: formatDate(form.value.date),
              start_time: formatTime(form.value.start_time),
              end_time: formatTime(form.value.end_time),
              purpose: form.value.purpose,
              participant_count: form.value.participant_count,
              description: form.value.description
            }

            const conflictCheck = await checkConflict(data)
            if (conflictCheck.has_conflict) {
              ElMessage.warning('该时间段已被预约，请选择其他时间')
              return
            }

            await createReservation(data)
            ElMessage.success('预约提交成功，等待审核')
            router.push('/my-reservations')
          } catch (error) {
            let msg = '预约失败，请检查输入信息'
            if (error && error.response && error.response.data) {
              const data = error.response.data
              if (Array.isArray(data.non_field_errors) && data.non_field_errors.length > 0) {
                msg = data.non_field_errors[0]
              } else if (typeof data.detail === 'string') {
                msg = data.detail
              }
            }
            ElMessage.error(msg)
          } finally {
            loading.value = false
          }
        }
      })
    }

    const resetForm = () => {
      if (reservationForm.value) {
        reservationForm.value.resetFields()
      }
    }

    onMounted(async () => {
      try {
        const data = await getAvailableClassrooms()
        classrooms.value = data
        
        if (route.query.classroom_id) {
          form.value.classroom = parseInt(route.query.classroom_id)
        }
      } catch (error) {
        ElMessage.error('获取教室列表失败')
      }
    })

    return {
      form,
      rules,
      reservationForm,
      loading,
      classrooms,
      disabledDate,
      handleSubmit,
      resetForm
    }
  }
}
</script>

<style scoped>
.reservations {
  padding: 20px;
  max-width: 800px;
}
</style>
