<template>
  <div class="admin-users">
    <h2>User Management</h2>
    <el-button type="primary">Add User</el-button>
    <el-table :data="users" border style="margin-top: 20px">
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="username" label="Username" />
    </el-table>
  </div>
</template>

<script>
import { ref } from 'vue'
export default {
  name: 'AdminUsers',
  setup() {
    const users = ref([])
    return { users }
  }
}
</script>

<style scoped>
.admin-users { padding: 20px; }
</style>
