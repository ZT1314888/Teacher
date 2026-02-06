<template>
  <div class="form-footer">
    <span class="footer-text">{{ text }}</span>
    <el-button class="action-link" text @click="$emit('click')">
      {{ actionText }}
    </el-button>
  </div>
</template>

<script setup>
defineProps({
  text: {
    type: String,
    required: true
  },
  actionText: {
    type: String,
    required: true
  }
})

defineEmits(['click'])
</script>

<style scoped>
.form-footer {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-top: 24px;
}

.footer-text {
  color: #6b7280;
  font-size: 0.875rem;
}

.action-link {
  color: #00897b;
  font-weight: 600;
  padding: 0;
  font-size: 0.875rem;
}

.action-link:hover {
  color: #00796b;
}
</style>
