<template>
  <div class="text-center py-12">
    <div class="inline-block w-8 h-8 border-4 border-primary border-t-transparent rounded-full animate-spin" />
    <p class="mt-4 text-gray-600">{{ text }}</p>
  </div>
</template>

<script setup>
defineProps({
  text: {
    type: String,
    default: '加载中...'
  }
})
</script>
