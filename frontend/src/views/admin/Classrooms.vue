<template>
  <div class="admin-classrooms">
    <h2>Classroom Management</h2>
    <el-button type="primary">Add Classroom</el-button>
    <el-table :data="classrooms" border style="margin-top: 20px">
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="name" label="Name" />
    </el-table>
  </div>
</template>

<script>
import { ref } from 'vue'
export default {
  name: 'AdminClassrooms',
  setup() {
    const classrooms = ref([])
    return { classrooms }
  }
}
</script>

<style scoped>
.admin-classrooms { padding: 20px; }
</style>
