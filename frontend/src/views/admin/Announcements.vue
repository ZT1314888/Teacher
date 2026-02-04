<template>
  <div class="admin-announcements">
    <h2>Announcement Management</h2>
    <el-button type="primary">Add Announcement</el-button>
    <el-table :data="announcements" border style="margin-top: 20px">
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="title" label="Title" />
    </el-table>
  </div>
</template>

<script>
import { ref } from 'vue'
export default {
  name: 'AdminAnnouncements',
  setup() {
    const announcements = ref([])
    return { announcements }
  }
}
</script>

<style scoped>
.admin-announcements { padding: 20px; }
</style>
