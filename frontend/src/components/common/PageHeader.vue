<template>
  <div class="page-header-wrap max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mb-6">
    <div class="page-header-rail" :class="{ 'page-header-rail--actions': !!$slots.actions }">
      <span class="page-header-dot" aria-hidden="true"></span>
      <span class="page-header-line" aria-hidden="true"></span>
      <div v-if="$slots.actions" class="actions">
        <slot name="actions" />
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    default: ''
  },
  subtitle: {
    type: String,
    default: ''
  }
})
</script>

<style scoped>
.page-header-rail {
  display: flex;
  align-items: center;
  min-height: 52px;
  padding: 0 4px;
}

.page-header-dot {
  width: 10px;
  height: 10px;
  border-radius: 999px;
  background: linear-gradient(135deg, #00a693 0%, #00897b 100%);
  box-shadow: 0 0 0 5px rgba(0, 137, 123, 0.12);
  flex-shrink: 0;
}

.page-header-line {
  height: 1px;
  margin-left: 12px;
  background: linear-gradient(90deg, rgba(0, 137, 123, 0.35) 0%, rgba(0, 137, 123, 0.08) 55%, rgba(0, 137, 123, 0) 100%);
  flex: 1;
}

.page-header-rail--actions .page-header-line {
  max-width: 260px;
}

.actions {
  margin-left: auto;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

@media (max-width: 640px) {
  .page-header-rail--actions .page-header-line {
    max-width: 120px;
  }
}
</style>
