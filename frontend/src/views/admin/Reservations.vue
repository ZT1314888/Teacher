<template>
  <div class='admin-reservations'>
    <h2>Reservation Management</h2>
    <el-table :data='reservations' border style='margin-top: 20px'>
      <el-table-column prop='id' label='ID' width='80' />
      <el-table-column prop='classroom_name' label='Classroom' />
      <el-table-column prop='user_name' label='User' width='120' />
      <el-table-column prop='status_display' label='Status' width='100' />
    </el-table>
  </div>
</template>

<script>
import { ref } from 'vue'
export default {
  name: 'AdminReservations',
  setup() {
    const reservations = ref([])
    return { reservations }
  }
}
</script>

<style scoped>
.admin-reservations { padding: 20px; }
</style>
