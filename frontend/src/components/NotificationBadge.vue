<template>
  <div class="notification-badge" @click="$emit('click')">
    <el-badge :value="unreadCount" :hidden="unreadCount <= 0" :max="99">
      <el-button text circle>
        <el-icon><Bell /></el-icon>
      </el-button>
    </el-badge>
  </div>
</template>

<script setup>
import { Bell } from '@element-plus/icons-vue'

defineProps({
  unreadCount: {
    type: Number,
    default: 0
  }
})

defineEmits(['click'])
</script>

<style scoped>
.notification-badge {
  display: inline-flex;
  align-items: center;
}
</style>
