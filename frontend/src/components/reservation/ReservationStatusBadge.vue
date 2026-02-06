<template>
  <span :class="['badge', statusClass]">{{ label }}</span>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  status: {
    type: String,
    required: true
  },
  label: {
    type: String,
    required: true
  }
})

const statusClass = computed(() => {
  const classMap = {
    pending: 'badge-warning',
    approved: 'badge-success',
    rejected: 'badge-danger',
    cancelled: 'badge-neutral'
  }
  return classMap[props.status] || 'badge-neutral'
})
</script>
