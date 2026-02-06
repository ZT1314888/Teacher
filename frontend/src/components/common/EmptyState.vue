<template>
  <div class="text-center py-12">
    <div class="mb-4 text-gray-300 empty-icon">
      <slot name="icon">
        <span class="text-5xl">{{ icon }}</span>
      </slot>
    </div>
    <h3 class="text-lg font-medium text-gray-900 mb-2">{{ title }}</h3>
    <p class="text-gray-500" :class="{ 'mb-6': actionText }">{{ description }}</p>
    <button v-if="actionText" type="button" class="btn-primary" @click="$emit('action')">
      {{ actionText }}
    </button>
  </div>
</template>

<script setup>
defineProps({
  icon: {
    type: String,
    default: '📭'
  },
  title: {
    type: String,
    required: true
  },
  description: {
    type: String,
    required: true
  },
  actionText: {
    type: String,
    default: ''
  }
})

defineEmits(['action'])
</script>

<style scoped>
.empty-icon {
  line-height: 1;
}
</style>
