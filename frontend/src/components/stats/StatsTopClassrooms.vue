<template>
  <section class="stats-panel">
    <div class="panel-header">
      <div>
        <h3 class="panel-title">热门教室 TOP 5</h3>
        <p class="panel-subtitle">按预约次数排序</p>
      </div>
    </div>

    <div v-if="loading" class="panel-loading">
      <div v-for="idx in 5" :key="idx" class="loading-item"></div>
    </div>

    <el-alert
      v-else-if="error"
      class="panel-alert"
      type="warning"
      :title="error"
      show-icon
      :closable="false"
    />

    <el-empty v-else-if="topRows.length === 0" description="暂无教室使用数据" />

    <ol v-else class="top-list">
      <li v-for="(item, idx) in topRows" :key="item.classroom_id || `${item.classroom_name}-${idx}`" class="top-item">
        <div class="item-head">
          <span class="rank">{{ idx + 1 }}</span>
          <span class="name">{{ item.classroom_name }}</span>
          <span class="count">{{ item.reservation_count }} 次</span>
        </div>
        <div class="item-track">
          <div class="item-fill" :style="{ width: `${getPercent(item.reservation_count)}%` }"></div>
        </div>
      </li>
    </ol>
  </section>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  rows: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  },
  error: {
    type: String,
    default: ''
  }
})

const normalizedRows = computed(() =>
  props.rows.map((row) => ({
    classroom_id: row.classroom_id,
    classroom_name: row.classroom_name || '未知教室',
    reservation_count: Number(row.reservation_count || 0)
  }))
)

const topRows = computed(() =>
  [...normalizedRows.value]
    .sort((a, b) => b.reservation_count - a.reservation_count)
    .slice(0, 5)
)

const maxCount = computed(() => Math.max(1, ...topRows.value.map((item) => item.reservation_count)))
const getPercent = (count) => Math.round((Number(count || 0) / maxCount.value) * 100)
</script>

<style scoped>
.stats-panel {
  background: #fff;
  border: 1px solid #f1f5f9;
  border-radius: 16px;
  padding: 20px;
  height: 100%;
}

.panel-header {
  margin-bottom: 16px;
}

.panel-title {
  margin: 0;
  font-size: 18px;
  font-weight: 700;
  color: #0f172a;
}

.panel-subtitle {
  margin: 4px 0 0;
  font-size: 13px;
  color: #64748b;
}

.panel-loading {
  display: grid;
  gap: 10px;
}

.loading-item {
  height: 44px;
  border-radius: 10px;
  background: linear-gradient(90deg, #f1f5f9 20%, #e2e8f0 45%, #f1f5f9 70%);
  background-size: 200% 100%;
  animation: shimmer 1.2s linear infinite;
}

.panel-alert {
  margin-bottom: 8px;
}

.top-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: grid;
  gap: 14px;
}

.top-item {
  display: grid;
  gap: 8px;
}

.item-head {
  display: grid;
  grid-template-columns: 26px 1fr auto;
  align-items: center;
  gap: 8px;
}

.rank {
  width: 22px;
  height: 22px;
  border-radius: 999px;
  background: #e6fffb;
  color: #0f766e;
  font-size: 12px;
  font-weight: 700;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.name {
  color: #334155;
  font-weight: 600;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.count {
  color: #64748b;
  font-size: 13px;
}

.item-track {
  height: 8px;
  border-radius: 999px;
  background: #e2e8f0;
  overflow: hidden;
}

.item-fill {
  height: 100%;
  border-radius: inherit;
  background: linear-gradient(90deg, #22d3ee 0%, #0ea5e9 100%);
}

@keyframes shimmer {
  from {
    background-position: 200% 0;
  }
  to {
    background-position: -200% 0;
  }
}
</style>
