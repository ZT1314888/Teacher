<template>
  <div class="stat-card-wrap">
    <div class="stat-icon"><slot name="icon" /></div>
    <div class="stat-body">
      <div class="stat-value">{{ value }}</div>
      <div class="stat-label">{{ label }}</div>
      <div v-if="trend" class="stat-trend" :class="trendClass">{{ trend }}</div>
      <div v-if="hint" class="stat-hint">{{ hint }}</div>
      <div v-if="$slots.action" class="stat-action"><slot name="action" /></div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  value: {
    type: [Number, String],
    default: 0
  },
  label: {
    type: String,
    required: true
  },
  trend: {
    type: String,
    default: ''
  },
  trendType: {
    type: String,
    default: 'neutral'
  },
  hint: {
    type: String,
    default: ''
  }
})

const trendClass = computed(() => {
  if (props.trendType === 'positive') return 'is-positive'
  if (props.trendType === 'negative') return 'is-negative'
  return 'is-neutral'
})
</script>

<style scoped>
.stat-card-wrap {
  display: flex;
  align-items: center;
  gap: 12px;
  width: 100%;
  min-height: 124px;
  background: #fff;
  border: 1px solid #f1f5f9;
  border-radius: 14px;
  padding: 20px;
  box-sizing: border-box;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.stat-card-wrap:hover {
  border-color: #dbe7f0;
  box-shadow: 0 8px 20px rgba(15, 23, 42, 0.05);
}

.stat-icon {
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 10px;
  background: #e6fffb;
  color: #00897b;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  line-height: 1;
}

.stat-label {
  font-size: 14px;
  color: #64748b;
  margin-top: 2px;
}

.stat-trend {
  margin-top: 8px;
  font-size: 12px;
  font-weight: 600;
}

.stat-trend.is-positive {
  color: #059669;
}

.stat-trend.is-negative {
  color: #dc2626;
}

.stat-trend.is-neutral {
  color: #0891b2;
}

.stat-hint {
  margin-top: 4px;
  font-size: 12px;
  color: #94a3b8;
}

.stat-action {
  margin-top: 8px;
}
</style>
